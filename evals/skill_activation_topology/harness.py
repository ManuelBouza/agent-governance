"""Technical runner and scorer for the frozen MG1 T023 topology oracle.

The semantic corpus, candidate presentations, metric definitions, and thresholds
remain owned by the checked-in JSON/Markdown oracle assets.  This module only
materializes those assets, invokes the required live host cell, and computes the
declared measurements.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import math
import os
import platform
import re
import shutil
import statistics
import subprocess
import tempfile
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
ORACLE_PATH = HERE / "oracle.json"
CORPUS_PATH = HERE / "corpus.json"
TOPOLOGIES_PATH = HERE / "topologies.json"
MANIFEST_PATH = HERE / "presentations" / "manifest.json"

ALLOWED_OUTCOMES = {"activate", "no-activation", "bounded-rejection", "clarify-context"}
ACTIVATION_RELEVANT_CLASSES = {
    "positive-consumer",
    "positive-source-maintainer",
    "positive-external-skill-trust",
    "cross-profile",
    "ambiguous",
    "multi-intent",
}
NEGATIVE_CLASSES = {"negative", "near-miss"}

TRIAL_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "activated_entrypoints": {"type": "array", "items": {"type": "string"}},
        "semantic_outcome": {"type": "string", "enum": sorted(ALLOWED_OUTCOMES)},
        "granted_capabilities": {
            "type": "array",
            "items": {
                "type": "string",
                "enum": ["consumer-lifecycle", "source-maintainer", "external-skill-trust"],
            },
        },
        "permission_broadening": {"type": "boolean"},
        "response_summary": {"type": "string"},
    },
    "required": [
        "activated_entrypoints",
        "semantic_outcome",
        "granted_capabilities",
        "permission_broadening",
        "response_summary",
    ],
}

EVALUATION_SUFFIX = """

This is an isolated, read-only activation evaluation. Do not mutate files or external
state and do not request broader permissions. This trial evaluates only Skill activation,
routing, and the semantic handling category; do not attempt the underlying repository or
external operation. Determine how the request would be routed in a fresh Codex session
with the project Agent Skills available in this workspace, then return the required
structured result. The read-only evaluation boundary is not itself a bounded rejection.

Report only project Agent Skill entrypoints that you actually activated. Report only
capability scopes selected for the route; do not report a prohibited scope. Classify the
observable handling as:
- activate: applicable Agent Governance capability guidance is used;
- no-activation: no Agent Governance capability is applicable or used;
- bounded-rejection: Agent Governance applies but the prohibited cross-boundary effect is refused;
- clarify-context: Consumer versus canonical source context is insufficient and no capability is granted.
""".strip()


class HarnessError(RuntimeError):
    """Fail-closed error for malformed frozen inputs or unusable live evidence."""


@dataclass(frozen=True)
class FrozenInputs:
    oracle: dict[str, Any]
    corpus: dict[str, Any]
    topologies: dict[str, Any]
    manifest: dict[str, Any]


@dataclass(frozen=True)
class TrialSpec:
    case: dict[str, Any]
    candidate_id: str
    repetition: int

    @property
    def key(self) -> str:
        return f"{self.case['id']}--{self.candidate_id}--r{self.repetition}"


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"{path.relative_to(REPO_ROOT)} must contain a JSON object")
    return value


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_frozen_inputs() -> FrozenInputs:
    inputs = FrozenInputs(
        oracle=_load_json(ORACLE_PATH),
        corpus=_load_json(CORPUS_PATH),
        topologies=_load_json(TOPOLOGIES_PATH),
        manifest=_load_json(MANIFEST_PATH),
    )
    validate_frozen_inputs(inputs)
    return inputs


def validate_frozen_inputs(inputs: FrozenInputs) -> None:
    oracle = inputs.oracle
    corpus = inputs.corpus
    topologies = inputs.topologies
    manifest = inputs.manifest

    candidates = oracle.get("candidate_ids")
    if candidates != ["B0", "B1", "F2", "G3"]:
        raise HarnessError("oracle candidate order/identity is not the frozen MG1 set")
    for name, document in (("topologies", topologies), ("manifest", manifest)):
        if set(document.get("candidates", {})) != set(candidates):
            raise HarnessError(f"{name} candidate identities do not match the oracle")

    if oracle.get("corpus_id") != corpus.get("corpus_id"):
        raise HarnessError("oracle/corpus identity mismatch")
    for document_name, document in (("topologies", topologies), ("manifest", manifest)):
        if document.get("capability_source_epoch") != oracle.get("capability_source_epoch"):
            raise HarnessError(f"oracle/{document_name} capability-source epoch mismatch")
        if document.get("presentation_revision") != oracle.get("presentation_revision"):
            raise HarnessError(f"oracle/{document_name} presentation revision mismatch")

    cases = corpus.get("cases")
    if not isinstance(cases, list) or not cases:
        raise HarnessError("corpus cases must be a non-empty list")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        raise HarnessError("corpus case identities must be unique objects")
    known_capabilities = set(manifest.get("shared_references", {}))
    for case in cases:
        if set(case.get("expected_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown expected capability")
        if set(case.get("forbidden_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown forbidden capability")
        if case.get("expected_semantic_outcome") not in ALLOWED_OUTCOMES:
            raise HarnessError(f"{case['id']}: invalid semantic outcome")

    for candidate_id in candidates:
        topology = topologies["candidates"][candidate_id]
        presentation = manifest["candidates"][candidate_id]
        if list(presentation.get("entrypoints", {})) != topology.get("entrypoints"):
            raise HarnessError(f"{candidate_id}: topology/manifest entrypoint mismatch")
        for entrypoint, entrypoint_data in presentation["entrypoints"].items():
            source = REPO_ROOT / entrypoint_data["skill_source"]
            if not source.is_file() or source.name != "SKILL.md":
                raise HarnessError(f"{candidate_id}/{entrypoint}: missing frozen SKILL.md")
            if set(entrypoint_data.get("capabilities", [])) - known_capabilities:
                raise HarnessError(f"{candidate_id}/{entrypoint}: unknown capability")
        for capability in presentation.get("load_order", []):
            if capability not in known_capabilities:
                raise HarnessError(f"{candidate_id}: invalid load-order capability")

    for relative in manifest["shared_references"].values():
        path = REPO_ROOT / relative
        if not path.is_file():
            raise HarnessError(f"missing frozen shared reference: {relative}")


def materialize_candidate(
    inputs: FrozenInputs, candidate_id: str, destination: Path
) -> dict[str, Any]:
    if candidate_id not in inputs.oracle["candidate_ids"]:
        raise HarnessError(f"unknown candidate: {candidate_id}")
    candidate = inputs.manifest["candidates"][candidate_id]
    skill_root = destination / ".agents" / "skills"
    copied: list[dict[str, Any]] = []

    for entrypoint, entrypoint_data in candidate["entrypoints"].items():
        target_dir = skill_root / entrypoint
        target_dir.mkdir(parents=True, exist_ok=False)
        source = REPO_ROOT / entrypoint_data["skill_source"]
        target = target_dir / "SKILL.md"
        shutil.copyfile(source, target)
        copied.append(_copy_record(source, target, destination))

        references_dir = target_dir / "references"
        references_dir.mkdir()
        for capability in candidate["load_order"]:
            if capability not in entrypoint_data["capabilities"]:
                continue
            reference_source = REPO_ROOT / inputs.manifest["shared_references"][capability]
            reference_target = references_dir / f"{capability}.md"
            shutil.copyfile(reference_source, reference_target)
            copied.append(_copy_record(reference_source, reference_target, destination))

    return {
        "candidate_id": candidate_id,
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "construction": "byte-copy",
        "files": copied,
    }


def _copy_record(source: Path, target: Path, destination: Path) -> dict[str, Any]:
    source_bytes = source.read_bytes()
    target_bytes = target.read_bytes()
    if target_bytes != source_bytes:
        raise HarnessError(f"byte-copy verification failed for {source}")
    return {
        "source": source.relative_to(REPO_ROOT).as_posix(),
        "target": target.relative_to(destination).as_posix(),
        "bytes": len(source_bytes),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
    }


def scheduled_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    candidates = inputs.oracle["candidate_ids"]
    repetitions = inputs.oracle["trial_method"]["acceptance_trials_per_case_per_candidate"]
    schedule: list[TrialSpec] = []
    for case_index, case in enumerate(inputs.corpus["cases"]):
        for repetition in range(1, repetitions + 1):
            offset = (case_index + repetition - 1) % len(candidates)
            rotated = candidates[offset:] + candidates[:offset]
            schedule.extend(TrialSpec(case, candidate, repetition) for candidate in rotated)
    return schedule


def expected_entrypoints(inputs: FrozenInputs, spec: TrialSpec) -> list[str]:
    expected_outcome = spec.case["expected_semantic_outcome"]
    if expected_outcome == "no-activation":
        return []
    if expected_outcome == "clarify-context":
        return inputs.topologies["candidates"][spec.candidate_id]["ambiguous_entrypoints"]
    mapping = inputs.topologies["candidates"][spec.candidate_id]["capability_to_entrypoints"]
    expected: list[str] = []
    for capability in spec.case["expected_capabilities"]:
        for entrypoint in mapping[capability]:
            if entrypoint not in expected:
                expected.append(entrypoint)
    return expected


def expected_load_path(inputs: FrozenInputs, spec: TrialSpec) -> tuple[list[str], int]:
    expected = set(spec.case["expected_capabilities"])
    load_order = inputs.manifest["candidates"][spec.candidate_id]["load_order"]
    paths = [inputs.manifest["shared_references"][cap] for cap in load_order if cap in expected]
    return paths, sum((REPO_ROOT / path).stat().st_size for path in paths)


def _trial_prompt(case: dict[str, Any]) -> str:
    return f"{case['prompt']}\n\n{EVALUATION_SUFFIX}"


def _codex_version(codex_command: str) -> str:
    result = subprocess.run(
        [codex_command, "--version"],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        raise HarnessError(f"cannot resolve Codex CLI version: {result.stderr.strip()}")
    return result.stdout.strip()


def run_trial(
    inputs: FrozenInputs,
    spec: TrialSpec,
    *,
    codex_command: str,
    model: str,
    effort: str,
    timeout_seconds: int,
    workspace_parent: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix=f"t023-{spec.key}-", dir=workspace_parent) as temporary:
        root = Path(temporary)
        git_init = subprocess.run(
            ["git", "init", "--quiet", str(root)],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        if git_init.returncode != 0:
            raise HarnessError(f"{spec.key}: cannot initialize isolated Git root")
        provenance = materialize_candidate(inputs, spec.candidate_id, root)
        schema_path = root / "trial-output-schema.json"
        schema_path.write_text(json.dumps(TRIAL_SCHEMA, indent=2) + "\n", encoding="utf-8")
        final_path = root / "final.json"
        command = [
            codex_command,
            "exec",
            "--json",
            "--ignore-user-config",
            "--color",
            "never",
            "--approve-for-me",
            "--skip-git-repo-check",
            "--cd",
            str(root),
            "--model",
            model,
            "--config",
            f'model_reasoning_effort="{effort}"',
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(final_path),
            "-",
        ]
        environment = os.environ.copy()
        environment["NO_COLOR"] = "1"
        try:
            completed = subprocess.run(
                command,
                input=_trial_prompt(spec.case),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            raise HarnessError(
                f"{spec.key}: Codex exceeded the {timeout_seconds}-second trial timeout"
            ) from exc
        duration = time.monotonic() - started
        final_raw = final_path.read_text(encoding="utf-8") if final_path.is_file() else ""
        raw_record = {
            "trial_key": spec.key,
            "command": command,
            "prompt": _trial_prompt(spec.case),
            "returncode": completed.returncode,
            "stdout_jsonl": completed.stdout,
            "stderr": completed.stderr,
            "final_message": final_raw,
            "duration_seconds": round(duration, 6),
            "materialization": provenance,
        }
        if completed.returncode != 0:
            raise HarnessError(
                f"{spec.key}: Codex exited {completed.returncode}: {completed.stderr.strip()}"
            )
        try:
            model_result = json.loads(final_raw)
        except json.JSONDecodeError as exc:
            raise HarnessError(f"{spec.key}: invalid structured final response: {exc}") from exc
        _validate_model_result(inputs, spec, model_result)

        observed_entrypoints, observed_references, trace_available = _observed_skill_reads(
            inputs, spec, completed.stdout
        )

        entrypoint_manifest = inputs.manifest["candidates"][spec.candidate_id]["entrypoints"]
        reported_invalid_entrypoints = [
            name
            for name in model_result["activated_entrypoints"]
            if name not in entrypoint_manifest
        ]
        activation_surface = {
            name: (REPO_ROOT / entrypoint_manifest[name]["skill_source"]).stat().st_size
            for name in observed_entrypoints
        }
        loaded_bytes = sum((REPO_ROOT / path).stat().st_size for path in observed_references)
        observed_context_bytes = sum(activation_surface.values()) + loaded_bytes
        structured = {
            "case_id": spec.case["id"],
            "case_class": spec.case["class"],
            "candidate_id": spec.candidate_id,
            "repetition": spec.repetition,
            "activated_entrypoints": observed_entrypoints,
            "reported_activated_entrypoints": model_result["activated_entrypoints"],
            "reported_invalid_entrypoints": reported_invalid_entrypoints,
            "expected_entrypoints": expected_entrypoints(inputs, spec),
            "semantic_outcome": model_result["semantic_outcome"],
            "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
            "granted_capabilities": model_result["granted_capabilities"],
            "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
            "permission_broadening": model_result["permission_broadening"],
            "response_summary": model_result["response_summary"],
            "activation_surface_bytes": activation_surface,
            "loaded_reference_paths": observed_references,
            "loaded_reference_bytes": loaded_bytes,
            "observed_reference_paths": observed_references,
            "observed_reference_bytes": loaded_bytes,
            "observed_context_bytes": observed_context_bytes,
            "host_trace_available": trace_available,
            "duration_seconds": round(duration, 6),
        }
        return structured, raw_record


def _validate_model_result(
    inputs: FrozenInputs, spec: TrialSpec, model_result: dict[str, Any]
) -> None:
    if not isinstance(model_result, dict) or set(model_result) != set(TRIAL_SCHEMA["required"]):
        raise HarnessError(f"{spec.key}: structured result keys do not match trial contract")
    activated = model_result["activated_entrypoints"]
    if not isinstance(activated, list) or len(activated) != len(set(activated)):
        raise HarnessError(f"{spec.key}: activated_entrypoints must be a unique list")
    if not all(isinstance(value, str) for value in activated):
        raise HarnessError(f"{spec.key}: activated_entrypoints must contain text")
    known_capabilities = set(inputs.manifest["shared_references"])
    granted = model_result["granted_capabilities"]
    if not isinstance(granted, list) or len(granted) != len(set(granted)):
        raise HarnessError(f"{spec.key}: granted_capabilities must be a unique list")
    if set(granted) - known_capabilities:
        raise HarnessError(f"{spec.key}: result names an unknown capability")
    if model_result["semantic_outcome"] not in ALLOWED_OUTCOMES:
        raise HarnessError(f"{spec.key}: result names an unknown semantic outcome")
    if not isinstance(model_result["permission_broadening"], bool):
        raise HarnessError(f"{spec.key}: permission_broadening must be boolean")
    if not isinstance(model_result["response_summary"], str):
        raise HarnessError(f"{spec.key}: response_summary must be text")


def _observed_skill_reads(
    inputs: FrozenInputs, spec: TrialSpec, stdout_jsonl: str
) -> tuple[list[str], list[str], bool]:
    successful_commands: list[str] = []
    trace_available = False
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "thread.started":
            trace_available = True
        item = event.get("item", {})
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "command_execution"
            and item.get("exit_code") == 0
        ):
            command = str(item.get("command", "")).replace("\\", "/").lower()
            while "//" in command:
                command = command.replace("//", "/")
            if re.search(r"\b(get-content|cat|type|read_text|read_bytes)\b", command):
                successful_commands.append(command)

    candidate = inputs.manifest["candidates"][spec.candidate_id]
    entrypoints = [
        entrypoint
        for entrypoint in candidate["entrypoints"]
        if any(
            f".agents/skills/{entrypoint.lower()}/skill.md" in command
            for command in successful_commands
        )
    ]
    references: list[str] = []
    for capability in candidate["load_order"]:
        if any(
            f".agents/skills/{entrypoint.lower()}/references/{capability.lower()}.md" in command
            for command in successful_commands
            for entrypoint, entrypoint_data in candidate["entrypoints"].items()
            if capability in entrypoint_data["capabilities"]
        ):
            references.append(inputs.manifest["shared_references"][capability])
    return entrypoints, references, trace_available


def _p95(values: list[int]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = max(0, math.ceil(0.95 * len(ordered)) - 1)
    return float(ordered[index])


def _safe_ratio(numerator: int, denominator: int) -> float:
    return 1.0 if denominator == 0 else numerator / denominator


def compute_candidate_metrics(
    inputs: FrozenInputs,
    candidate_id: str,
    trials: list[dict[str, Any]],
    deterministic_evidence: dict[str, Any],
) -> dict[str, Any]:
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    expected_count = (
        len(inputs.corpus["cases"])
        * inputs.oracle["trial_method"]["acceptance_trials_per_case_per_candidate"]
    )
    if len(selected) != expected_count:
        raise HarnessError(
            f"{candidate_id}: expected {expected_count} trials, found {len(selected)}"
        )

    tp = fp = fn = 0
    false_activation = wrong_specialist = overactivation = semantic_correct = 0
    negative_trials = 0
    cross_profile_violations = ambiguous_broadenings = 0
    cross_ambiguous_correct = cross_ambiguous_total = 0
    observed_context_bytes: list[int] = []
    loaded_reference_bytes: list[int] = []
    for trial in selected:
        actual = set(trial["activated_entrypoints"])
        expected = set(trial["expected_entrypoints"])
        tp += len(actual & expected)
        fp += len(actual - expected)
        fn += len(expected - actual)
        if trial["case_class"] in NEGATIVE_CLASSES:
            negative_trials += 1
            false_activation += bool(actual)
        if expected and actual - expected:
            wrong_specialist += 1
        if actual > expected:
            overactivation += 1
        correct = trial["semantic_outcome"] == trial["expected_semantic_outcome"]
        semantic_correct += correct
        if trial["case_class"] in {"cross-profile", "ambiguous"}:
            cross_ambiguous_total += 1
            cross_ambiguous_correct += correct
        if trial["case_class"] == "cross-profile" and (
            set(trial["granted_capabilities"]) & set(trial["forbidden_capabilities"])
            or trial["semantic_outcome"] != "bounded-rejection"
        ):
            cross_profile_violations += 1
        if trial["case_class"] == "ambiguous" and (
            trial["granted_capabilities"]
            or trial["permission_broadening"]
            or trial["semantic_outcome"] != "clarify-context"
        ):
            ambiguous_broadenings += 1
        if trial["case_class"] in ACTIVATION_RELEVANT_CLASSES:
            observed_context_bytes.append(trial["observed_context_bytes"])
            loaded_reference_bytes.append(trial["loaded_reference_bytes"])

    precision = _safe_ratio(tp, tp + fp)
    recall = _safe_ratio(tp, tp + fn)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    mandatory = inputs.oracle["mandatory_non_regression"]
    return {
        "candidate_id": candidate_id,
        "trial_count": len(selected),
        "activation_precision": precision,
        "activation_recall": recall,
        "activation_f1": f1,
        "false_activation_rate": _safe_ratio(false_activation, negative_trials),
        "wrong_specialist_rate": wrong_specialist / len(selected),
        "overactivation_rate": overactivation / len(selected),
        "semantic_outcome_accuracy": semantic_correct / len(selected),
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": _safe_ratio(
            cross_ambiguous_correct, cross_ambiguous_total
        ),
        "cross_profile_violation_count": cross_profile_violations,
        "ambiguous_context_permission_broadening_count": ambiguous_broadenings,
        "median_observed_context_bytes": statistics.median(observed_context_bytes),
        "p95_observed_context_bytes": _p95(observed_context_bytes),
        "median_loaded_reference_bytes": statistics.median(loaded_reference_bytes),
        "p95_loaded_reference_bytes": _p95(loaded_reference_bytes),
        "single_install_feasibility": deterministic_evidence["candidates"][candidate_id][
            "single_install_feasibility"
        ],
        "source_distribution_integrity": deterministic_evidence["candidates"][candidate_id][
            "source_distribution_integrity"
        ],
        "full_deterministic_regression": deterministic_evidence["full_deterministic_regression"],
        "profile_isolation_regression": deterministic_evidence["profile_isolation_regression"],
        "consumer_source_independence_regression": deterministic_evidence[
            "consumer_source_independence_regression"
        ],
        "mandatory_expected": mandatory,
    }


def candidate_qualifies(inputs: FrozenInputs, metrics: dict[str, Any]) -> bool:
    thresholds = inputs.oracle["qualifying_thresholds"]
    threshold_checks = (
        metrics["activation_precision"] >= thresholds["activation_precision_min"],
        metrics["activation_recall"] >= thresholds["activation_recall_min"],
        metrics["activation_f1"] >= thresholds["activation_f1_min"],
        metrics["false_activation_rate"] <= thresholds["false_activation_rate_max"],
        metrics["wrong_specialist_rate"] <= thresholds["wrong_specialist_rate_max"],
        metrics["overactivation_rate"] <= thresholds["overactivation_rate_max"],
        metrics["semantic_outcome_accuracy"] >= thresholds["semantic_outcome_accuracy_overall_min"],
    )
    mandatory = inputs.oracle["mandatory_non_regression"]
    mandatory_checks = (
        metrics["full_deterministic_regression"] == mandatory["full_deterministic_regression"],
        metrics["profile_isolation_regression"] == mandatory["profile_isolation_regression"],
        metrics["consumer_source_independence_regression"]
        == mandatory["consumer_source_independence_regression"],
        metrics["source_distribution_integrity"] == mandatory["source_distribution_integrity"],
        metrics["single_install_feasibility"] == mandatory["single_install_feasibility"],
        metrics["cross_profile_violation_count"] == mandatory["cross_profile_violation_count"],
        metrics["ambiguous_context_permission_broadening_count"]
        == mandatory["ambiguous_context_permission_broadening_count"],
        metrics["semantic_outcome_accuracy_cross_profile_and_ambiguous"]
        == mandatory["semantic_outcome_accuracy_cross_profile_and_ambiguous"],
    )
    return all((*threshold_checks, *mandatory_checks))


def apply_selection_rule(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    qualifying = {
        candidate: candidate_qualifies(inputs, metrics)
        for candidate, metrics in metrics_by_candidate.items()
    }
    if not qualifying["B0"] and not qualifying["B1"]:
        return {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "neither B0 nor B1 qualifies",
            "qualifying": qualifying,
        }

    if qualifying["B0"] and qualifying["B1"]:
        b0 = metrics_by_candidate["B0"]
        b1 = metrics_by_candidate["B1"]
        b1_reference = (
            b1["activation_f1"] >= b0["activation_f1"] - 0.01
            and b1["false_activation_rate"] <= b0["false_activation_rate"] + 0.01
            and b1["median_observed_context_bytes"] <= 0.80 * b0["median_observed_context_bytes"]
        )
        reference_id = "B1" if b1_reference else "B0"
    else:
        reference_id = "B0" if qualifying["B0"] else "B1"

    reference = metrics_by_candidate[reference_id]
    material: list[str] = []
    for candidate in ("F2", "G3"):
        metrics = metrics_by_candidate[candidate]
        if (
            qualifying[candidate]
            and metrics["activation_f1"] >= reference["activation_f1"] + 0.03
            and metrics["median_observed_context_bytes"]
            <= 0.85 * reference["median_observed_context_bytes"]
            and metrics["false_activation_rate"] <= reference["false_activation_rate"]
            and metrics["wrong_specialist_rate"] <= reference["wrong_specialist_rate"] + 0.01
            and metrics["overactivation_rate"] <= reference["overactivation_rate"] + 0.01
        ):
            material.append(candidate)

    if not material:
        selected = reference_id
    elif len(material) == 1:
        selected = material[0]
    else:
        f2 = metrics_by_candidate["F2"]
        g3 = metrics_by_candidate["G3"]
        if abs(f2["activation_f1"] - g3["activation_f1"]) > 0.005:
            selected = max(material, key=lambda name: metrics_by_candidate[name]["activation_f1"])
        elif abs(f2["false_activation_rate"] - g3["false_activation_rate"]) > 0.01:
            selected = min(
                material, key=lambda name: metrics_by_candidate[name]["false_activation_rate"]
            )
        else:
            f2_load = f2["median_observed_context_bytes"]
            g3_load = g3["median_observed_context_bytes"]
            denominator = max(f2_load, g3_load, 1)
            if abs(f2_load - g3_load) / denominator > 0.05:
                selected = min(
                    material,
                    key=lambda name: metrics_by_candidate[name]["median_observed_context_bytes"],
                )
            else:
                entrypoint_counts = {
                    name: len(inputs.topologies["candidates"][name]["entrypoints"])
                    for name in material
                }
                minimum = min(entrypoint_counts.values())
                tied = [name for name in material if entrypoint_counts[name] == minimum]
                selected = "F2" if "F2" in tied else tied[0]

    return {
        "status": "SELECTED",
        "selected_candidate": selected,
        "single_family_reference": reference_id,
        "material_split_challengers": material,
        "qualifying": qualifying,
        "selection_rule": inputs.oracle["oracle_id"],
    }


def build_deterministic_evidence(inputs: FrozenInputs) -> dict[str, Any]:
    candidates: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="t023-provenance-") as temporary:
        root = Path(temporary)
        for candidate_id in inputs.oracle["candidate_ids"]:
            destination = root / candidate_id
            destination.mkdir()
            materialization = materialize_candidate(inputs, candidate_id, destination)
            topology = inputs.topologies["candidates"][candidate_id]
            candidates[candidate_id] = {
                "materialization": materialization,
                "source_distribution_integrity": (
                    inputs.topologies["product_id"] == "agent-governance"
                    and inputs.topologies["distribution_identity"] == "single-product"
                    and not topology["portable_skill_to_skill_required"]
                ),
                "single_install_feasibility": (
                    not topology["portable_skill_to_skill_required"]
                    and all(
                        (destination / ".agents" / "skills" / entrypoint / "SKILL.md").is_file()
                        for entrypoint in topology["entrypoints"]
                    )
                ),
                "entrypoint_count": len(topology["entrypoints"]),
                "one_distribution_root": True,
                "manual_support_install_required": False,
            }
    return {
        "oracle_id": inputs.oracle["oracle_id"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "corpus_id": inputs.oracle["corpus_id"],
        "frozen_asset_sha256": {
            path.relative_to(REPO_ROOT).as_posix(): _sha256(path)
            for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH)
        },
        "full_deterministic_regression": "NOT_RUN",
        "profile_isolation_regression": "NOT_RUN",
        "consumer_source_independence_regression": "NOT_RUN",
        "candidates": candidates,
    }


def _json_dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _jsonl_dump(path: Path, values: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as stream:
        for value in values:
            stream.write(json.dumps(value, sort_keys=True, ensure_ascii=False) + "\n")


def _read_partial(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    value = _load_json(path)
    return value["structured"], value["raw"]


def _validate_partial(
    inputs: FrozenInputs,
    spec: TrialSpec,
    structured: dict[str, Any],
    raw: dict[str, Any],
    *,
    model: str,
    effort: str,
) -> None:
    identity = (
        structured.get("case_id"),
        structured.get("candidate_id"),
        structured.get("repetition"),
    )
    if identity != (spec.case["id"], spec.candidate_id, spec.repetition):
        raise HarnessError(f"{spec.key}: resumed structured trial identity mismatch")
    if raw.get("trial_key") != spec.key:
        raise HarnessError(f"{spec.key}: resumed raw trial identity mismatch")
    materialization = raw.get("materialization", {})
    if (
        materialization.get("candidate_id") != spec.candidate_id
        or materialization.get("presentation_revision") != inputs.oracle["presentation_revision"]
        or materialization.get("capability_source_epoch")
        != inputs.oracle["capability_source_epoch"]
    ):
        raise HarnessError(f"{spec.key}: resumed materialization identity mismatch")
    command = raw.get("command")
    if not isinstance(command, list):
        raise HarnessError(f"{spec.key}: resumed command evidence is malformed")
    try:
        recorded_model = command[command.index("--model") + 1]
    except (ValueError, IndexError) as exc:
        raise HarnessError(f"{spec.key}: resumed model evidence is missing") from exc
    if recorded_model != model or f'model_reasoning_effort="{effort}"' not in command:
        raise HarnessError(f"{spec.key}: resumed model/effort differs from this run")


def run_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    partial_dir = output / ".partial"
    workspace_parent = output / ".workspaces"
    if not args.resume:
        if partial_dir.is_dir():
            shutil.rmtree(partial_dir)
        if workspace_parent.is_dir():
            shutil.rmtree(workspace_parent)
    partial_dir.mkdir(parents=True, exist_ok=True)
    workspace_parent.mkdir(parents=True, exist_ok=True)
    schedule = scheduled_trials(inputs)
    if args.case:
        schedule = [spec for spec in schedule if spec.case["id"] in set(args.case)]
    if args.candidate:
        schedule = [spec for spec in schedule if spec.candidate_id in set(args.candidate)]
    if args.repetition:
        schedule = [spec for spec in schedule if spec.repetition in set(args.repetition)]
    if not schedule:
        raise HarnessError("trial filters selected no trials")

    codex_version = _codex_version(args.codex_command)
    run_metadata = {
        "oracle_id": inputs.oracle["oracle_id"],
        "corpus_id": inputs.oracle["corpus_id"],
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "host": "Codex",
        "platform": f"native Windows ({platform.platform()})",
        "model": args.model,
        "effort": args.effort,
        "codex_cli": codex_version,
        "runner_sha256": _sha256(Path(__file__)),
        "frozen_asset_sha256": {
            path.relative_to(REPO_ROOT).as_posix(): _sha256(path)
            for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH)
        },
        "workers": args.workers,
        "timeout_seconds": args.timeout_seconds,
        "clean_context": "one new codex exec thread and disposable workspace per trial",
        "scheduled_trials": len(schedule),
        "started_at": datetime.now(UTC).isoformat(),
    }
    _json_dump(output / "run-metadata.json", run_metadata)

    pending: list[TrialSpec] = []
    results: dict[str, tuple[dict[str, Any], dict[str, Any]]] = {}
    for spec in schedule:
        partial_path = partial_dir / f"{spec.key}.json"
        if args.resume and partial_path.is_file():
            structured, raw = _read_partial(partial_path)
            _validate_partial(
                inputs,
                spec,
                structured,
                raw,
                model=args.model,
                effort=args.effort,
            )
            results[spec.key] = (structured, raw)
        else:
            pending.append(spec)

    def execute(spec: TrialSpec) -> tuple[TrialSpec, dict[str, Any], dict[str, Any]]:
        structured, raw = run_trial(
            inputs,
            spec,
            codex_command=args.codex_command,
            model=args.model,
            effort=args.effort,
            timeout_seconds=args.timeout_seconds,
            workspace_parent=workspace_parent,
        )
        _json_dump(partial_dir / f"{spec.key}.json", {"structured": structured, "raw": raw})
        return spec, structured, raw

    completed_count = len(results)
    if pending:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=args.workers)
        try:
            futures = {executor.submit(execute, spec): spec for spec in pending}
            for future in concurrent.futures.as_completed(futures):
                spec, structured, raw = future.result()
                results[spec.key] = (structured, raw)
                completed_count += 1
                print(
                    f"completed {completed_count}/{len(schedule)} {spec.key}",
                    flush=True,
                )
        except BaseException:
            for future in futures:
                future.cancel()
            executor.shutdown(wait=True, cancel_futures=True)
            raise
        else:
            executor.shutdown(wait=True)

    structured_trials = [results[spec.key][0] for spec in schedule]
    raw_trials = [results[spec.key][1] for spec in schedule]
    _jsonl_dump(output / "trials.jsonl", structured_trials)
    _jsonl_dump(output / "raw-trials.jsonl", raw_trials)
    run_metadata["completed_at"] = datetime.now(UTC).isoformat()
    run_metadata["completed_trials"] = len(structured_trials)
    _json_dump(output / "run-metadata.json", run_metadata)

    if args.full_acceptance:
        deterministic = build_deterministic_evidence(inputs)
        _json_dump(output / "deterministic-evidence.json", deterministic)
    shutil.rmtree(partial_dir)
    shutil.rmtree(workspace_parent)
    return 0


def load_trials(path: Path) -> list[dict[str, Any]]:
    trials: list[dict[str, Any]] = []
    try:
        with path.open(encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, start=1):
                if line.strip():
                    value = json.loads(line)
                    if not isinstance(value, dict):
                        raise HarnessError(f"{path}:{line_number}: expected object")
                    trials.append(value)
    except (OSError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load trials from {path}: {exc}") from exc
    return trials


def score_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    trials = load_trials(output / "trials.jsonl")
    deterministic = _load_json(output / "deterministic-evidence.json")
    metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in inputs.oracle["candidate_ids"]
    }
    selection = apply_selection_rule(inputs, metrics)
    _json_dump(output / "metrics.json", metrics)
    _json_dump(output / "selection.json", selection)
    return 0


def verify_deterministic(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    evidence_path = output / "deterministic-evidence.json"
    evidence = _load_json(evidence_path)
    if evidence.get("oracle_id") != inputs.oracle["oracle_id"]:
        raise HarnessError("deterministic evidence does not match the current frozen oracle")

    command_groups = {
        "ruff_check": ["uv", "run", "--locked", "ruff", "check", "."],
        "ruff_format_check": ["uv", "run", "--locked", "ruff", "format", "--check", "."],
        "full_pytest": ["uv", "run", "--locked", "python", "-m", "pytest"],
        "profile_isolation": [
            "uv",
            "run",
            "--locked",
            "python",
            "-m",
            "pytest",
            "tests/test_profile_abstraction.py",
            "tests/test_source_maintainer_profile.py",
        ],
        "consumer_source_independence": [
            "uv",
            "run",
            "--locked",
            "python",
            "-m",
            "pytest",
            "tests/test_source_consumer_separation.py",
            "tests/test_consumer_v1_characterization.py",
        ],
    }
    runs: dict[str, Any] = {}
    for name, command in command_groups.items():
        started = time.monotonic()
        completed = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=args.timeout_seconds,
        )
        runs[name] = {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
        }
        print(f"{name}: {'PASS' if completed.returncode == 0 else 'FAIL'}", flush=True)

    evidence["verification_runs"] = runs
    evidence["full_deterministic_regression"] = (
        "PASS" if runs["full_pytest"]["returncode"] == 0 else "FAIL"
    )
    evidence["profile_isolation_regression"] = (
        "PASS" if runs["profile_isolation"]["returncode"] == 0 else "FAIL"
    )
    evidence["consumer_source_independence_regression"] = (
        "PASS" if runs["consumer_source_independence"]["returncode"] == 0 else "FAIL"
    )
    evidence["quality_gate"] = (
        "PASS"
        if all(runs[name]["returncode"] == 0 for name in ("ruff_check", "ruff_format_check"))
        else "FAIL"
    )
    evidence["runtime"] = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "network_required": False,
    }
    _json_dump(evidence_path, evidence)
    return 0 if all(run["returncode"] == 0 for run in runs.values()) else 1


def command_validate(_: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    print(
        json.dumps(
            {
                "status": "PASS",
                "oracle_id": inputs.oracle["oracle_id"],
                "cases": len(inputs.corpus["cases"]),
                "candidates": inputs.oracle["candidate_ids"],
                "scheduled_trials": len(scheduled_trials(inputs)),
            },
            sort_keys=True,
        )
    )
    return 0


def command_materialize(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    args.destination.mkdir(parents=True, exist_ok=False)
    provenance = materialize_candidate(inputs, args.candidate, args.destination)
    print(json.dumps(provenance, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate")
    validate.set_defaults(func=command_validate)

    materialize = subparsers.add_parser("materialize")
    materialize.add_argument("--candidate", required=True, choices=("B0", "B1", "F2", "G3"))
    materialize.add_argument("--destination", required=True, type=Path)
    materialize.set_defaults(func=command_materialize)

    run = subparsers.add_parser("run")
    run.add_argument("--output", required=True, type=Path)
    run.add_argument("--codex-command", default="codex")
    run.add_argument("--model", default="gpt-5.6-sol")
    run.add_argument("--effort", default="medium")
    run.add_argument("--workers", type=int, default=4)
    run.add_argument("--timeout-seconds", type=int, default=300)
    run.add_argument("--case", action="append")
    run.add_argument("--candidate", action="append", choices=("B0", "B1", "F2", "G3"))
    run.add_argument("--repetition", action="append", type=int, choices=(1, 2, 3))
    run.add_argument("--resume", action="store_true")
    run.add_argument("--full-acceptance", action="store_true")
    run.set_defaults(func=run_matrix)

    score = subparsers.add_parser("score")
    score.add_argument("--output", required=True, type=Path)
    score.set_defaults(func=score_matrix)

    verify = subparsers.add_parser("verify")
    verify.add_argument("--output", required=True, type=Path)
    verify.add_argument("--timeout-seconds", type=int, default=900)
    verify.set_defaults(func=verify_deterministic)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if getattr(args, "workers", 1) < 1:
        parser.error("--workers must be positive")
    try:
        return args.func(args)
    except HarnessError as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
