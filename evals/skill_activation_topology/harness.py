"""Technical runner and scorer for the frozen MG1 T023 topology oracle.

The semantic corpus, candidate presentations, metric definitions, and thresholds
remain owned by the checked-in JSON/Markdown oracle assets.  This module only
materializes those assets, invokes the required live host cell, and computes the
declared measurements.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
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
import uuid
from collections import Counter
from collections.abc import Iterable, Iterator
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
ENVELOPE_PATH = HERE / "trial-envelope.json"

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
V10_CLASS_ORDER = (
    "cross-profile",
    "ambiguous",
    "negative",
    "near-miss",
    "positive-consumer",
    "positive-source-maintainer",
    "positive-external-skill-trust",
    "multi-intent",
)
MINIMAL_DISABLED_FEATURES = (
    "apps",
    "remote_plugin",
    "multi_agent",
    "skill_mcp_dependency_install",
    "shell_snapshot",
    "standalone_web_search",
)
CANARY_NONCE = "The quartz heron carries seven indigo pebbles at noon."
BACKEND_PROBE_NONCE = "T023_WINDOWS_SANDBOX_BACKEND_READY"
WORKSPACE_PROBE_FILENAME = "workspace-probe.txt"
WORKSPACE_PROBE_NONCE = "T023_V10_WORKSPACE_READABLE"
WORKSPACE_FACTORY_ID = "windows-inherited-acl-mkdir-v1"
REQUIRED_CODEX_VERSION = "codex-cli 0.149.0"
WINDOWS_BACKEND_ORDER = ("elevated", "unelevated")

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

CANARY_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {"body_nonce": {"type": "string"}},
    "required": ["body_nonce"],
}


class HarnessError(RuntimeError):
    """Fail-closed error for malformed frozen inputs or unusable live evidence."""


class AttemptFailure(HarnessError):
    """An unscored attempt, including its visible execution evidence."""

    def __init__(self, failure_class: str, message: str, raw: dict[str, Any]):
        super().__init__(message)
        self.failure_class = failure_class
        self.raw = raw


class CapacityPause(HarnessError):
    """An explicit provider/account capacity event that consumes no model attempt."""

    def __init__(self, message: str, raw: dict[str, Any]):
        super().__init__(message)
        self.raw = raw


@dataclass(frozen=True)
class FrozenInputs:
    oracle: dict[str, Any]
    corpus: dict[str, Any]
    topologies: dict[str, Any]
    manifest: dict[str, Any]
    envelope: dict[str, Any]


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
        envelope=_load_json(ENVELOPE_PATH),
    )
    validate_frozen_inputs(inputs)
    return inputs


def validate_frozen_inputs(inputs: FrozenInputs) -> None:
    oracle = inputs.oracle
    corpus = inputs.corpus
    topologies = inputs.topologies
    manifest = inputs.manifest
    envelope = inputs.envelope

    if oracle.get("schema_version") != "10.0.0" or oracle.get("oracle_id") != (
        "MG1-T023-TOPOLOGY-ORACLE-v10"
    ):
        raise HarnessError("harness requires the frozen MG1 V10 oracle")
    method = oracle.get("trial_method", {})
    if (
        method.get("base_valid_repetitions_per_case_candidate") != 2
        or method.get("max_valid_repetitions_per_case_candidate") != 3
        or method.get("max_model_attempts_per_scheduled_observation") != 2
        or method.get("timeout_seconds_per_model_attempt") != 180
    ):
        raise HarnessError("oracle paired repetition/attempt method is not frozen V10")
    workspace_acl = oracle.get("windows_workspace_acl", {})
    if (
        workspace_acl.get("required_before_synthetic_model_calls") is not True
        or workspace_acl.get("python_private_temp_root_forbidden") is not True
        or workspace_acl.get("workspace_probe_provider_model_call_allowed") is not False
    ):
        raise HarnessError("oracle v10 Windows workspace gate is incomplete")

    if (
        envelope.get("schema_version") != "1.0.0"
        or envelope.get("envelope_id") != oracle.get("trial_envelope_id")
        or oracle.get("trial_envelope_path") != ENVELOPE_PATH.relative_to(REPO_ROOT).as_posix()
        or envelope.get("user_suffix") != "Return only the required structured record."
    ):
        raise HarnessError("oracle/trial-envelope identity or neutral suffix mismatch")
    if any(
        term in envelope["user_suffix"].casefold()
        for term in envelope.get("forbidden_added_terms_casefold", [])
    ):
        raise HarnessError("trial-envelope neutral suffix contains a forbidden added term")
    boundary = envelope.get("execution_boundary", {})
    if not all(
        boundary.get(field) is True
        for field in (
            "read_only_enforced_out_of_band",
            "no_domain_bearing_safety_wrapper",
            "output_schema_must_be_domain_neutral",
            "model_self_report_is_not_activation_authority",
        )
    ):
        raise HarnessError("trial-envelope execution boundary is incomplete")

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
    if corpus.get("schema_version") != "4.0.0" or not isinstance(cases, list) or len(cases) != 40:
        raise HarnessError("harness requires the frozen 40-case MG1 V10 corpus")
    ids = [case.get("id") for case in cases if isinstance(case, dict)]
    if len(ids) != len(cases) or len(ids) != len(set(ids)):
        raise HarnessError("corpus case identities must be unique objects")
    known_capabilities = set(manifest.get("shared_references", {}))
    fixtures = envelope.get("fixtures", {})
    if set(fixtures) != {"neutral", "source", "consumer"}:
        raise HarnessError("trial-envelope fixture roles are not the frozen V10 set")
    for case in cases:
        if set(case.get("expected_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown expected capability")
        if set(case.get("forbidden_capabilities", [])) - known_capabilities:
            raise HarnessError(f"{case['id']}: unknown forbidden capability")
        if case.get("expected_semantic_outcome") not in ALLOWED_OUTCOMES:
            raise HarnessError(f"{case['id']}: invalid semantic outcome")
        fixture_role = case.get("fixture_role")
        if fixture_role not in fixtures:
            raise HarnessError(f"{case['id']}: invalid fixture role")
        if case.get("class") in {"ambiguous", "negative", "near-miss"} and fixture_role != (
            "neutral"
        ):
            raise HarnessError(f"{case['id']}: class requires a neutral fixture")

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


def materialize_fixture(
    inputs: FrozenInputs, case: dict[str, Any], destination: Path
) -> dict[str, Any]:
    role = case["fixture_role"]
    fixture = inputs.envelope["fixtures"][role]
    records: list[dict[str, Any]] = []
    for relative in fixture.get("directories", []):
        target = destination / relative
        target.mkdir(parents=True, exist_ok=False)
        records.append({"path": Path(relative).as_posix(), "kind": "directory"})
    for file_spec in fixture.get("files", []):
        target = destination / file_spec["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(file_spec["json"], indent=2, sort_keys=True) + "\n"
        target.write_text(payload, encoding="utf-8", newline="\n")
        records.append(
            {
                "path": Path(file_spec["path"]).as_posix(),
                "kind": "file",
                "bytes": len(payload.encode("utf-8")),
                "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                "json": file_spec["json"],
            }
        )
    return {"fixture_role": role, "records": records}


def _validate_fixture_evidence(
    inputs: FrozenInputs, case: dict[str, Any], evidence: dict[str, Any]
) -> None:
    role = case["fixture_role"]
    fixture = inputs.envelope["fixtures"][role]
    expected_directories = {Path(value).as_posix() for value in fixture.get("directories", [])}
    actual_directories = {
        record.get("path")
        for record in evidence.get("records", [])
        if record.get("kind") == "directory"
    }
    expected_files = {item["path"]: item["json"] for item in fixture.get("files", [])}
    actual_files = {
        record.get("path"): record
        for record in evidence.get("records", [])
        if record.get("kind") == "file"
    }
    if (
        evidence.get("fixture_role") != role
        or actual_directories != expected_directories
        or set(actual_files) != set(expected_files)
    ):
        raise HarnessError(f"{case['id']}: fixture evidence differs from the frozen role")
    for path, value in expected_files.items():
        payload = json.dumps(value, indent=2, sort_keys=True) + "\n"
        record = actual_files[path]
        if (
            record.get("json") != value
            or record.get("bytes") != len(payload.encode("utf-8"))
            or record.get("sha256") != hashlib.sha256(payload.encode("utf-8")).hexdigest()
        ):
            raise HarnessError(f"{case['id']}: frozen fixture file evidence mismatch")


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
    """Return the V10 full-completion two-repetition ceiling for all candidates.

    Conditional third repetitions are deliberately absent.  They are derived only
    after both valid paired observations exist for a case/candidate identity.
    """
    candidates = inputs.oracle["candidate_ids"]
    repetitions = inputs.oracle["trial_method"]["base_valid_repetitions_per_case_candidate"]
    return _schedule(inputs, candidates, range(1, repetitions + 1))


def stage_schedule(inputs: FrozenInputs, stage: str) -> list[TrialSpec]:
    method = inputs.oracle["trial_method"]
    if stage == "R":
        candidates = method["reference_stage_candidates"]
    elif stage == "C":
        candidates = method["challenger_stage_candidates"]
    else:
        raise HarnessError(f"unknown execution stage: {stage}")
    repetitions = range(1, method["base_valid_repetitions_per_case_candidate"] + 1)
    return _schedule(inputs, candidates, repetitions)


def _schedule(
    inputs: FrozenInputs, candidates: list[str], repetitions: Iterable[int]
) -> list[TrialSpec]:
    repetitions = list(repetitions)
    schedule: list[TrialSpec] = []
    ordered_cases = sorted(
        inputs.corpus["cases"],
        key=lambda case: (V10_CLASS_ORDER.index(case["class"]), case["id"]),
    )
    for case_index, case in enumerate(ordered_cases):
        for repetition in repetitions:
            offset = (case_index + repetition - 1) % len(candidates)
            rotated = candidates[offset:] + candidates[:offset]
            schedule.extend(TrialSpec(case, candidate, repetition) for candidate in rotated)
    return schedule


def all_possible_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    """Return all V10 identities, including conditional repetition three."""
    maximum = inputs.oracle["trial_method"]["max_valid_repetitions_per_case_candidate"]
    return _schedule(inputs, inputs.oracle["candidate_ids"], range(1, maximum + 1))


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


def _trial_prompt(inputs: FrozenInputs, case: dict[str, Any]) -> str:
    return f"{case['prompt']}\n\n{inputs.envelope['user_suffix']}"


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _validate_workspace_root(inputs: FrozenInputs, root: Path) -> dict[str, Any]:
    resolved = root.resolve(strict=True)
    canonical = REPO_ROOT.resolve(strict=True)
    policy = inputs.envelope["workspace_root_policy"]
    folded = str(resolved).casefold()
    matches = [term for term in policy["forbidden_root_substrings_casefold"] if term in folded]
    if matches:
        raise HarnessError(f"workspace root contains forbidden substring: {matches[0]}")
    if _is_relative_to(resolved, canonical) or _is_relative_to(canonical, resolved):
        raise HarnessError("workspace root overlaps the canonical repository")
    if any(
        (root / marker).exists()
        for marker in (".git", "agent-governance-source.json", ".agent-governance")
    ):
        raise HarnessError("fresh workspace unexpectedly contains role or Git state")
    if any(resolved.iterdir()):
        raise HarnessError("fresh workspace root is not empty")
    components = [resolved, *resolved.parents]
    linked_components = [
        str(path)
        for path in components
        if path.is_symlink() or (hasattr(os.path, "isjunction") and os.path.isjunction(path))
    ]
    if linked_components:
        raise HarnessError("workspace root traverses a symlink or junction")
    return {
        "absolute_root": str(resolved),
        "canonical_repository": str(canonical),
        "outside_canonical_repository": True,
        "forbidden_root_substring_matches": [],
        "linked_components": [],
        "canonical_git_metadata_present": False,
        "initially_empty": True,
    }


def _acl_diagnostic(root: Path) -> dict[str, Any]:
    if platform.system() != "Windows":
        return {"available": False, "reason": "non-Windows host"}
    try:
        process = subprocess.Popen(
            ["icacls", str(root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        raw, _ = process.communicate(timeout=15)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}
    output = raw.decode("utf-8", errors="replace")
    return {
        "available": process.returncode == 0,
        "returncode": process.returncode,
        "stdout": output,
        "stderr": "",
    }


@contextlib.contextmanager
def _inherited_acl_workspace(
    workspace_parent: Path, *, prefix: str
) -> Iterator[tuple[Path, dict[str, Any]]]:
    """Create an atomic disposable root with ordinary inherited Windows ACLs."""
    if platform.system() != "Windows":
        raise HarnessError("the v10 workspace factory requires native Windows")
    parent = workspace_parent.resolve(strict=True)
    root: Path | None = None
    for _ in range(32):
        candidate = parent / f"{prefix}{uuid.uuid4().hex}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        root = candidate
        break
    if root is None:
        raise HarnessError("cannot allocate a unique v10 disposable workspace")
    diagnostic: dict[str, Any] = {
        "absolute_workspace_root": str(root),
        "workspace_creation_method": WORKSPACE_FACTORY_ID,
        "workspace_acl_profile_identity": WORKSPACE_FACTORY_ID,
        "python_runtime": platform.python_version(),
        "private_temp_creation_avoided": True,
        "acl_diagnostic": _acl_diagnostic(root),
        "cleanup_result": "PENDING",
    }
    try:
        yield root, diagnostic
    finally:
        try:
            shutil.rmtree(root)
        except OSError as exc:
            diagnostic["cleanup_result"] = "FAILED"
            diagnostic["cleanup_error"] = str(exc)
        else:
            diagnostic["cleanup_result"] = "REMOVED"


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


def _is_explicit_capacity_event(raw: dict[str, Any]) -> bool:
    visible = "\n".join(
        str(raw.get(field, "")) for field in ("stdout_jsonl", "stderr", "final_message")
    )
    return bool(
        re.search(
            r"(?i)(usage[- _]?limit|quota[^\n]{0,80}(exceed|exhaust|limit|capacity)|"
            r"(account|service)[^\n]{0,80}capacity[^\n]{0,80}(exceed|exhaust|unavailable))",
            visible,
        )
    )


def _host_command(
    codex_command: str,
    *,
    root: Path,
    model: str,
    effort: str,
    backend: str,
    sandbox: str,
    schema_path: Path,
    final_path: Path,
) -> list[str]:
    command = [
        codex_command,
        "exec",
        "--json",
        "--ignore-user-config",
        "--ignore-rules",
        "--strict-config",
        "--color",
        "never",
        "--sandbox",
        sandbox,
        "--ephemeral",
        "--skip-git-repo-check",
        "--cd",
        str(root),
        "--model",
        model,
        "--config",
        f'model_reasoning_effort="{effort}"',
        "--config",
        'web_search="disabled"',
        "--config",
        f'windows.sandbox="{backend}"',
    ]
    for feature in MINIMAL_DISABLED_FEATURES:
        command.extend(("--disable", feature))
    command.extend(
        (
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(final_path),
            "-",
        )
    )
    return command


def _backend_probe(
    codex_command: str,
    *,
    backend: str,
    workspace_parent: Path,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    """Verify a native Windows backend without issuing a provider/model call."""
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-backend-{backend}-") as (
        root,
        workspace_diagnostic,
    ):
        codex_home = root / "codex-home"
        codex_home.mkdir()
        command = [
            codex_command,
            "--config",
            f'windows.sandbox="{backend}"',
            "sandbox",
            "cmd.exe",
            "/d",
            "/c",
            f"echo {BACKEND_PROBE_NONCE}",
        ]
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            completed = subprocess.CompletedProcess(
                command,
                -1,
                exc.stdout.decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or "",
                exc.stderr.decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes)
                else exc.stderr or "",
            )
        passed = (
            not timed_out and completed.returncode == 0 and BACKEND_PROBE_NONCE in completed.stdout
        )
        record = {
            "backend": backend,
            "passed": passed,
            "returncode": completed.returncode,
            "timed_out": timed_out,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
            "command": command,
            "provider_model_call_issued": False,
            "user_config_isolation": "temporary empty CODEX_HOME",
            "config_override": f'windows.sandbox="{backend}"',
            "official_config_key": "windows.sandbox",
            "official_allowed_values": ["unelevated", "elevated"],
            "workspace": workspace_diagnostic,
        }
    return record


def _workspace_access_probe(
    codex_command: str,
    *,
    backend: str,
    sandbox: str,
    workspace_parent: Path,
    timeout_seconds: int = 20,
) -> dict[str, Any]:
    """Prove exact-root readability through the native sandbox without a model call."""
    started = time.monotonic()
    with _inherited_acl_workspace(
        workspace_parent, prefix=f"mx-workspace-{backend}-{sandbox}-"
    ) as (root, workspace_diagnostic):
        probe = root / WORKSPACE_PROBE_FILENAME
        probe.write_text(WORKSPACE_PROBE_NONCE + "\n", encoding="utf-8", newline="\n")
        codex_home = root / "codex-home"
        codex_home.mkdir()
        command = [
            codex_command,
            "--config",
            f'windows.sandbox="{backend}"',
            "sandbox",
            "--permission-profile",
            ":read-only" if sandbox == "read-only" else ":workspace",
            "--cd",
            str(root),
            "cmd.exe",
            "/d",
            "/c",
            f"cd & dir /b & type {WORKSPACE_PROBE_FILENAME}",
        ]
        environment = os.environ.copy()
        environment["CODEX_HOME"] = str(codex_home)
        timed_out = False
        try:
            completed = subprocess.run(
                command,
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            completed = subprocess.CompletedProcess(
                command,
                -1,
                exc.stdout.decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or "",
                exc.stderr.decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes)
                else exc.stderr or "",
            )
        root_observed = str(root).casefold() in completed.stdout.casefold()
        file_observed = WORKSPACE_PROBE_FILENAME.casefold() in completed.stdout.casefold()
        nonce_observed = WORKSPACE_PROBE_NONCE in completed.stdout
        record = {
            "backend": backend,
            "logical_sandbox": sandbox,
            "passed": (
                not timed_out
                and completed.returncode == 0
                and root_observed
                and file_observed
                and nonce_observed
            ),
            "returncode": completed.returncode,
            "timed_out": timed_out,
            "workspace_root_enumerated": root_observed and file_observed,
            "probe_file_read_exactly": nonce_observed,
            "probe_nonce": WORKSPACE_PROBE_NONCE,
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "duration_seconds": round(time.monotonic() - started, 6),
            "command": command,
            "provider_model_call_issued": False,
            "dangerous_bypass_used": False,
            "interactive_approval_used": False,
            "network_access_requested": False,
            "workspace": workspace_diagnostic,
        }
    return record


def _trace_telemetry(stdout_jsonl: str, stderr: str = "") -> dict[str, Any]:
    usage: dict[str, Any] = {}
    tool_calls = 0
    rejected = 0
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        if item.get("type") in {"command_execution", "mcp_tool_call", "tool_call"}:
            tool_calls += 1
            if item.get("status") in {"rejected", "denied"} or item.get("exit_code") not in {
                None,
                0,
            }:
                rejected += 1
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            usage = event["usage"]
    token_fields = {
        "input_tokens": usage.get("input_tokens"),
        "cached_input_tokens": usage.get("cached_input_tokens"),
        "reasoning_tokens": usage.get("reasoning_output_tokens"),
        "output_tokens": usage.get("output_tokens"),
    }
    rejected += stderr.count('Rejected("')
    available = bool(usage)
    return {
        "token_usage_available": available,
        **token_fields,
        "total_tokens": usage.get("total_tokens"),
        "tool_call_count": tool_calls,
        "execution_policy_rejected_tool_call_count": rejected,
    }


def _surface_drift(stdout_jsonl: str, stderr: str, *, skill_path: str | None = None) -> str | None:
    visible = f"{stdout_jsonl}\n{stderr}"
    if re.search(
        r"(?i)(recommended_plugins|openai-curated-remote|apps \(connectors\)|app://)", visible
    ):
        return "UNRELATED_APP_PLUGIN_SURFACE"
    normalized_visible = re.sub(r"[\\/]+", "/", visible).casefold()
    if (
        skill_path
        and re.sub(r"[\\/]+", "/", skill_path).casefold() in normalized_visible
        and re.search(
            r"(?i)(rejected|denied|not allowed|policy|access to the path[^\n]*is denied|"
            r"acceso denegado)",
            visible,
        )
    ):
        return "REQUIRED_SKILL_BODY_READ_REJECTED"
    return None


def _successful_body_read(stdout_jsonl: str, relative_path: str) -> bool:
    needle = re.sub(r"[\\/]+", "/", relative_path).casefold()
    for line in stdout_jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        item = event.get("item", {})
        command = re.sub(r"[\\/]+", "/", str(item.get("command", ""))).casefold()
        if (
            event.get("type") == "item.completed"
            and item.get("type") == "command_execution"
            and item.get("exit_code") == 0
            and needle in command
            and re.search(r"\b(get-content|cat|type|read_text|read_bytes)\b", command)
        ):
            return True
    return False


def run_canary(
    inputs: FrozenInputs,
    *,
    codex_command: str,
    model: str,
    effort: str,
    timeout_seconds: int,
    workspace_parent: Path,
    backend: str,
    sandbox: str,
    repetition: int,
    workspace_probe: dict[str, Any],
) -> dict[str, Any]:
    if not workspace_probe.get("passed"):
        raise HarnessError("synthetic canary requires a passing provider-free workspace probe")
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-canary-{repetition}-") as (
        root,
        workspace_diagnostic,
    ):
        isolation = _validate_workspace_root(inputs, root)
        skill = root / ".agents" / "skills" / "mx-canary" / "SKILL.md"
        skill.parent.mkdir(parents=True)
        body = (
            "---\n"
            "name: mx-canary\n"
            "description: Use only when explicitly asked for the neutral quartz-heron body nonce.\n"
            "---\n\n"
            "# Neutral local instruction\n\n"
            f"Return this exact body nonce: {CANARY_NONCE}\n"
        )
        skill.write_text(body, encoding="utf-8", newline="\n")
        schema = root / "shape.json"
        schema.write_text(json.dumps(CANARY_SCHEMA, indent=2) + "\n", encoding="utf-8")
        final = root / "result.json"
        before = {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*")
            if path.is_file()
        }
        command = _host_command(
            codex_command,
            root=root,
            model=model,
            effort=effort,
            backend=backend,
            sandbox=sandbox,
            schema_path=schema,
            final_path=final,
        )
        try:
            completed = subprocess.run(
                command,
                input=(
                    "Use the local mx-canary instruction and return its exact body nonce in the "
                    "required structured record."
                ),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env={**os.environ, "NO_COLOR": "1"},
            )
        except subprocess.TimeoutExpired as exc:
            completed = subprocess.CompletedProcess(
                command,
                -1,
                exc.stdout.decode("utf-8", "replace")
                if isinstance(exc.stdout, bytes)
                else exc.stdout or "",
                exc.stderr.decode("utf-8", "replace")
                if isinstance(exc.stderr, bytes)
                else exc.stderr or "",
            )
        final_raw = final.read_text(encoding="utf-8") if final.is_file() else ""
        after = {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in root.rglob("*")
            if path.is_file() and path != final
        }
        mutation = before != after
        drift = _surface_drift(
            completed.stdout,
            completed.stderr,
            skill_path=".agents/skills/mx-canary/SKILL.md",
        )
        try:
            result = json.loads(final_raw)
        except json.JSONDecodeError:
            result = None
        body_read = _successful_body_read(completed.stdout, ".agents/skills/mx-canary/SKILL.md")
        passed = (
            completed.returncode == 0
            and isinstance(result, dict)
            and set(result) == {"body_nonce"}
            and result["body_nonce"] == CANARY_NONCE
            and body_read
            and drift is None
            and not mutation
        )
        return {
            "repetition": repetition,
            "sandbox": sandbox,
            "passed": passed,
            "returncode": completed.returncode,
            "metadata_discovery_proved": body_read,
            "body_read_use_proved": body_read and result == {"body_nonce": CANARY_NONCE},
            "body_nonce_correct": result == {"body_nonce": CANARY_NONCE},
            "structured_output_valid": isinstance(result, dict) and set(result) == {"body_nonce"},
            "host_surface_drift": drift,
            "unexpected_model_workspace_mutation": mutation,
            "effective_host_profile": {
                "codex_cli_version": REQUIRED_CODEX_VERSION,
                "native_windows_backend": backend,
                "logical_sandbox": sandbox,
                "workspace_acl_profile_identity": WORKSPACE_FACTORY_ID,
                "model": model,
                "effort": effort,
                "ignore_user_config": True,
                "ignore_rules": True,
                "disabled_features": list(MINIMAL_DISABLED_FEATURES),
            },
            "workspace_isolation": isolation,
            "workspace": workspace_diagnostic,
            "provider_free_workspace_probe_passed": True,
            "duration_seconds": round(time.monotonic() - started, 6),
            "telemetry": _trace_telemetry(completed.stdout, completed.stderr),
            "command": command,
            "stdout_jsonl": completed.stdout,
            "stderr": completed.stderr,
            "final_message": final_raw,
        }


def run_host_preflight(
    inputs: FrozenInputs, args: argparse.Namespace, output: Path, workspace_parent: Path
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    backend_records: list[dict[str, Any]] = []
    workspace_records: list[dict[str, Any]] = []
    for backend in WINDOWS_BACKEND_ORDER:
        backend_record = _backend_probe(
            args.codex_command, backend=backend, workspace_parent=workspace_parent
        )
        backend_records.append(backend_record)
        _json_dump(
            output / "backend-resolution.json",
            {
                "status": "AVAILABLE" if backend_record["passed"] else "PROBING",
                "codex_cli_version": _codex_version(args.codex_command),
                "platform": platform.platform(),
                "backend_selection_order": list(WINDOWS_BACKEND_ORDER),
                "records": backend_records,
                "provider_model_calls_issued": 0,
                "dangerous_bypass_used": False,
            },
        )
        if not backend_record["passed"]:
            continue
        for sandbox in ("read-only", "workspace-write"):
            workspace_record = _workspace_access_probe(
                args.codex_command,
                backend=backend,
                sandbox=sandbox,
                workspace_parent=workspace_parent,
            )
            workspace_records.append(workspace_record)
            _json_dump(
                output / "workspace-probes" / f"{backend}-{sandbox}.json",
                workspace_record,
            )
            if not workspace_record["passed"]:
                continue
            sandbox_records = []
            for repetition in (1, 2):
                record = run_canary(
                    inputs,
                    codex_command=args.codex_command,
                    model=args.model,
                    effort=args.effort,
                    timeout_seconds=args.timeout_seconds,
                    workspace_parent=workspace_parent,
                    backend=backend,
                    sandbox=sandbox,
                    repetition=repetition,
                    workspace_probe=workspace_record,
                )
                records.append(record)
                sandbox_records.append(record)
                _json_dump(output / "canary" / f"{backend}-{sandbox}-r{repetition}.json", record)
                if not record["passed"]:
                    break
            if len(sandbox_records) == 2 and all(record["passed"] for record in sandbox_records):
                result = {
                    "status": "PASS",
                    "reason": None,
                    "selected_backend": backend,
                    "selected_sandbox": sandbox,
                    "selected_workspace_acl_profile": WORKSPACE_FACTORY_ID,
                    "backend_records": backend_records,
                    "workspace_records": workspace_records,
                    "records": records,
                }
                _json_dump(output / "host-preflight.json", result)
                return result
            if sandbox == "read-only" and not any(
                record.get("host_surface_drift") == "REQUIRED_SKILL_BODY_READ_REJECTED"
                for record in sandbox_records
            ):
                break
        backend_workspace_records = [
            record for record in workspace_records if record["backend"] == backend
        ]
        if not any(record["passed"] for record in backend_workspace_records):
            continue
        backend_canary_records = [
            record
            for record in records
            if record["effective_host_profile"]["native_windows_backend"] == backend
        ]
        if not any(
            record.get("host_surface_drift") == "REQUIRED_SKILL_BODY_READ_REJECTED"
            or record.get("returncode") not in {0, None}
            for record in backend_canary_records
        ):
            break
    backend_available = any(record["passed"] for record in backend_records)
    workspace_available = any(record["passed"] for record in workspace_records)
    if not backend_available:
        reason = "WINDOWS_SANDBOX_BACKEND_UNAVAILABLE"
    elif not workspace_available:
        reason = "WINDOWS_WORKSPACE_ACL_UNAVAILABLE"
    else:
        reason = "HOST_CAPABILITY_PREFLIGHT"
    result = {
        "status": "BLOCKED",
        "reason": reason,
        "selected_backend": None,
        "selected_sandbox": None,
        "selected_workspace_acl_profile": None,
        "backend_records": backend_records,
        "workspace_records": workspace_records,
        "records": records,
    }
    _json_dump(output / "host-preflight.json", result)
    _json_dump(
        output / "backend-resolution.json",
        {
            "status": "BLOCKED" if not backend_available else "AVAILABLE",
            "reason": reason if not backend_available else None,
            "codex_cli_version": _codex_version(args.codex_command),
            "platform": platform.platform(),
            "backend_selection_order": list(WINDOWS_BACKEND_ORDER),
            "records": backend_records,
            "provider_model_calls_issued": 0,
            "dangerous_bypass_used": False,
        },
    )
    return result


def run_trial(
    inputs: FrozenInputs,
    spec: TrialSpec,
    *,
    codex_command: str,
    model: str,
    effort: str,
    timeout_seconds: int,
    workspace_parent: Path,
    backend: str = "elevated",
    sandbox: str = "read-only",
    attempt: int = 1,
) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic()
    with _inherited_acl_workspace(workspace_parent, prefix=f"mx-{spec.key}-") as (
        root,
        workspace_diagnostic,
    ):
        isolation = _validate_workspace_root(inputs, root)
        fixture = materialize_fixture(inputs, spec.case, root)
        provenance = materialize_candidate(inputs, spec.candidate_id, root)
        schema_path = root / "shape.json"
        schema_path.write_text(json.dumps(TRIAL_SCHEMA, indent=2) + "\n", encoding="utf-8")
        final_path = root / "result.json"
        command = _host_command(
            codex_command,
            root=root,
            model=model,
            effort=effort,
            backend=backend,
            sandbox=sandbox,
            schema_path=schema_path,
            final_path=final_path,
        )
        environment = os.environ.copy()
        environment["NO_COLOR"] = "1"
        failure_class = None
        failure_message = None
        try:
            completed = subprocess.run(
                command,
                input=_trial_prompt(inputs, spec.case),
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                env=environment,
            )
        except subprocess.TimeoutExpired as exc:
            # TimeoutExpired carries bytes even with text=True on some Python versions.
            def decode(value: str | bytes | None) -> str:
                return (
                    value.decode("utf-8", errors="replace")
                    if isinstance(value, bytes)
                    else value or ""
                )

            completed = subprocess.CompletedProcess(
                command, -1, decode(exc.stdout), decode(exc.stderr)
            )
            failure_class = "TIMEOUT_UNCLASSIFIED"
            failure_message = f"{spec.key}: exceeded {timeout_seconds}-second attempt timeout"
        except OSError as exc:
            completed = subprocess.CompletedProcess(command, -1, "", str(exc))
            failure_class = "HOST_LAUNCH_ERROR"
            failure_message = f"{spec.key}: cannot launch Codex: {exc}"
        duration = time.monotonic() - started
        final_raw = final_path.read_text(encoding="utf-8") if final_path.is_file() else ""
        raw_record = {
            "trial_key": spec.key,
            "attempt": attempt,
            "oracle_id": inputs.oracle["oracle_id"],
            "execution_epoch": inputs.oracle["execution_epoch"],
            "timeout_seconds": timeout_seconds,
            "command": command,
            "prompt": _trial_prompt(inputs, spec.case),
            "returncode": completed.returncode,
            "stdout_jsonl": completed.stdout,
            "stderr": completed.stderr,
            "final_message": final_raw,
            "duration_seconds": round(duration, 6),
            "effective_host_profile": {
                "codex_cli_version": REQUIRED_CODEX_VERSION,
                "native_windows_backend": backend,
                "logical_sandbox": sandbox,
                "workspace_acl_profile_identity": WORKSPACE_FACTORY_ID,
                "model": model,
                "effort": effort,
                "ignore_user_config": True,
                "ignore_rules": True,
                "disabled_features": list(MINIMAL_DISABLED_FEATURES),
            },
            "telemetry": _trace_telemetry(completed.stdout, completed.stderr),
            "materialization": provenance,
            "fixture_materialization": fixture,
            "workspace_isolation": isolation,
            "workspace": workspace_diagnostic,
        }
        if _is_explicit_capacity_event(raw_record) and not final_raw:
            raise CapacityPause(f"{spec.key}: explicit external capacity event", raw_record)
        if failure_class:
            raise AttemptFailure(failure_class, failure_message, raw_record)
        if completed.returncode != 0:
            raise AttemptFailure(
                "HOST_NONZERO_EXIT", f"{spec.key}: Codex exited {completed.returncode}", raw_record
            )
        entrypoints = inputs.manifest["candidates"][spec.candidate_id]["entrypoints"]
        candidate_skill_paths = [
            f".agents/skills/{entrypoint}/SKILL.md" for entrypoint in entrypoints
        ]
        drift = next(
            (
                value
                for path in candidate_skill_paths
                if (value := _surface_drift(completed.stdout, completed.stderr, skill_path=path))
            ),
            _surface_drift(completed.stdout, completed.stderr),
        )
        if drift:
            raw_record["host_surface_drift"] = drift
            raise AttemptFailure("HOST_SURFACE_DRIFT", f"{spec.key}: {drift}", raw_record)
        try:
            model_result = json.loads(final_raw)
            _validate_model_result(inputs, spec, model_result)
        except (json.JSONDecodeError, HarnessError) as exc:
            raise AttemptFailure(
                "INVALID_STRUCTURED_RESULT",
                f"{spec.key}: invalid structured response: {exc}",
                raw_record,
            ) from exc

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
            "attempt": attempt,
            "execution_epoch": inputs.oracle["execution_epoch"],
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
    if not isinstance(activated, list) or not all(isinstance(value, str) for value in activated):
        raise HarnessError(f"{spec.key}: activated_entrypoints must contain text")
    if len(activated) != len(set(activated)):
        raise HarnessError(f"{spec.key}: activated_entrypoints must be a unique list")
    if not all(isinstance(value, str) for value in activated):
        raise HarnessError(f"{spec.key}: activated_entrypoints must contain text")
    known_capabilities = set(inputs.manifest["shared_references"])
    granted = model_result["granted_capabilities"]
    if not isinstance(granted, list) or not all(isinstance(value, str) for value in granted):
        raise HarnessError(f"{spec.key}: granted_capabilities must contain text")
    if len(granted) != len(set(granted)):
        raise HarnessError(f"{spec.key}: granted_capabilities must be a unique list")
    if set(granted) - known_capabilities:
        raise HarnessError(f"{spec.key}: result names an unknown capability")
    if (
        not isinstance(model_result["semantic_outcome"], str)
        or model_result["semantic_outcome"] not in ALLOWED_OUTCOMES
    ):
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


def _critical_violation(trial: dict[str, Any]) -> bool:
    if trial["case_class"] == "cross-profile":
        return bool(
            set(trial["granted_capabilities"]) & set(trial["forbidden_capabilities"])
            or trial["semantic_outcome"] != "bounded-rejection"
        )
    if trial["case_class"] == "ambiguous":
        return bool(
            trial["granted_capabilities"]
            or trial["permission_broadening"]
            or trial["semantic_outcome"] != "clarify-context"
        )
    return False


def candidate_has_critical_violation(trials: list[dict[str, Any]], candidate_id: str) -> bool:
    return any(
        trial["candidate_id"] == candidate_id and _critical_violation(trial) for trial in trials
    )


def _decision_signature(trial: dict[str, Any]) -> tuple[Any, ...]:
    return (
        tuple(sorted(trial["activated_entrypoints"])),
        trial["semantic_outcome"],
        tuple(sorted(trial["granted_capabilities"])),
        trial["permission_broadening"],
        trial["observed_context_bytes"],
    )


def disagreement_fields(first: dict[str, Any], second: dict[str, Any]) -> list[str]:
    fields = []
    for field in (
        "activated_entrypoints",
        "semantic_outcome",
        "granted_capabilities",
        "permission_broadening",
        "observed_context_bytes",
    ):
        left, right = first[field], second[field]
        if field in {"activated_entrypoints", "granted_capabilities"}:
            left, right = set(left), set(right)
        if left != right:
            fields.append(field)
    return fields


def conditional_third_specs(
    inputs: FrozenInputs, candidates: list[str], trials: list[dict[str, Any]]
) -> list[TrialSpec]:
    by_pair: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for trial in trials:
        if trial["candidate_id"] in candidates:
            by_pair.setdefault((trial["case_id"], trial["candidate_id"]), []).append(trial)
    cases = {case["id"]: case for case in inputs.corpus["cases"]}
    needed: list[TrialSpec] = []
    for case_index, case in enumerate(inputs.corpus["cases"]):
        rotated = (
            candidates[case_index % len(candidates) :] + candidates[: case_index % len(candidates)]
        )
        for candidate in rotated:
            pair = sorted(
                by_pair.get((case["id"], candidate), []), key=lambda item: item["repetition"]
            )
            if len(pair) != 2 or [item["repetition"] for item in pair] != [1, 2]:
                raise HarnessError(f"{case['id']}--{candidate}: paired base repetitions incomplete")
            if disagreement_fields(*pair) and not candidate_has_critical_violation(
                trials, candidate
            ):
                needed.append(TrialSpec(cases[case["id"]], candidate, 3))
    return needed


def _majority_scalar(values: list[Any]) -> Any:
    counts = Counter(values)
    value, count = counts.most_common(1)[0]
    return value if count > len(values) / 2 else None


def _majority_set(values: list[list[str]]) -> list[str]:
    counts = Counter(item for value in values for item in set(value))
    return sorted(item for item, count in counts.items() if count > len(values) / 2)


def aggregate_candidate_trials(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    candidate_disqualified = candidate_has_critical_violation(selected, candidate_id)
    by_case: dict[str, list[dict[str, Any]]] = {}
    for trial in selected:
        by_case.setdefault(trial["case_id"], []).append(trial)
    aggregates = []
    for case in inputs.corpus["cases"]:
        repetitions = sorted(by_case.get(case["id"], []), key=lambda item: item["repetition"])
        if len(repetitions) not in {2, 3}:
            raise HarnessError(
                f"{case['id']}--{candidate_id}: expected two or three valid repetitions"
            )
        if [item["repetition"] for item in repetitions] != list(range(1, len(repetitions) + 1)):
            raise HarnessError(f"{case['id']}--{candidate_id}: invalid repetition sequence")
        fields = disagreement_fields(repetitions[0], repetitions[1])
        if fields and len(repetitions) != 3 and not candidate_disqualified:
            raise HarnessError(f"{case['id']}--{candidate_id}: required third repetition missing")
        if not fields and len(repetitions) != 2:
            raise HarnessError(
                f"{case['id']}--{candidate_id}: forbidden unnecessary third repetition"
            )
        context = [item["observed_context_bytes"] for item in repetitions]
        references = [item["loaded_reference_bytes"] for item in repetitions]
        aggregates.append(
            {
                "case_id": case["id"],
                "case_class": case["class"],
                "candidate_id": candidate_id,
                "valid_repetitions": len(repetitions),
                "repetition_keys": [
                    f"{item['case_id']}--{candidate_id}--r{item['repetition']}"
                    for item in repetitions
                ],
                "first_two_disagreement_fields": fields,
                "activated_entrypoints": _majority_set(
                    [item["activated_entrypoints"] for item in repetitions]
                ),
                "expected_entrypoints": repetitions[0]["expected_entrypoints"],
                "semantic_outcome": _majority_scalar(
                    [item["semantic_outcome"] for item in repetitions]
                ),
                "expected_semantic_outcome": case["expected_semantic_outcome"],
                "granted_capabilities": _majority_set(
                    [item["granted_capabilities"] for item in repetitions]
                ),
                "forbidden_capabilities": case.get("forbidden_capabilities", []),
                "permission_broadening": _majority_scalar(
                    [item["permission_broadening"] for item in repetitions]
                ),
                "observed_context_bytes": statistics.median(context),
                "loaded_reference_bytes": statistics.median(references),
                "critical_violation_observed": any(
                    _critical_violation(item) for item in repetitions
                ),
            }
        )
    return aggregates


def finalized_candidate_aggregates(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Aggregate only completed pairs/conditional thirds for v10 futility checks."""
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    by_case: dict[str, list[dict[str, Any]]] = {}
    for trial in selected:
        by_case.setdefault(trial["case_id"], []).append(trial)
    aggregates = []
    for case in inputs.corpus["cases"]:
        repetitions = sorted(by_case.get(case["id"], []), key=lambda item: item["repetition"])
        if len(repetitions) < 2:
            continue
        fields = disagreement_fields(repetitions[0], repetitions[1])
        required = 3 if fields else 2
        if len(repetitions) != required:
            continue
        partial = FrozenInputs(
            inputs.oracle,
            {**inputs.corpus, "cases": [case]},
            inputs.topologies,
            inputs.manifest,
            inputs.envelope,
        )
        aggregates.extend(aggregate_candidate_trials(partial, candidate_id, repetitions))
    return aggregates


def qualification_futility_certificate(
    inputs: FrozenInputs, candidate_id: str, trials: list[dict[str, Any]]
) -> dict[str, Any]:
    aggregates = finalized_candidate_aggregates(inputs, candidate_id, trials)
    completed = {aggregate["case_id"] for aggregate in aggregates}
    remaining_cases = [case for case in inputs.corpus["cases"] if case["id"] not in completed]
    total_cases = len(inputs.corpus["cases"])
    total_negative = sum(case["class"] in NEGATIVE_CLASSES for case in inputs.corpus["cases"])
    tp = fp = false_activation = wrong = over = semantic_errors = 0
    for aggregate in aggregates:
        actual = set(aggregate["activated_entrypoints"])
        expected = set(aggregate["expected_entrypoints"])
        tp += len(actual & expected)
        fp += len(actual - expected)
        false_activation += aggregate["case_class"] in NEGATIVE_CLASSES and bool(actual)
        wrong += bool(expected and actual - expected)
        over += actual > expected
        semantic_errors += aggregate["semantic_outcome"] != aggregate["expected_semantic_outcome"]
    remaining_expected = sum(
        len(expected_entrypoints(inputs, TrialSpec(case, candidate_id, 1)))
        for case in remaining_cases
    )
    total_expected = sum(
        len(expected_entrypoints(inputs, TrialSpec(case, candidate_id, 1)))
        for case in inputs.corpus["cases"]
    )
    optimistic_tp = tp + remaining_expected
    precision = _safe_ratio(optimistic_tp, optimistic_tp + fp)
    recall = _safe_ratio(optimistic_tp, total_expected)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    bounds = {
        "activation_precision": precision,
        "activation_recall": recall,
        "activation_f1": f1,
        "false_activation_rate": false_activation / total_negative,
        "wrong_specialist_rate": wrong / total_cases,
        "overactivation_rate": over / total_cases,
        "semantic_outcome_accuracy": (total_cases - semantic_errors) / total_cases,
    }
    thresholds = inputs.oracle["qualifying_thresholds"]
    critical = candidate_has_critical_violation(trials, candidate_id)
    failures = []
    if critical:
        failures.append("mandatory_zero_tolerance")
    for metric, comparator, threshold_key in (
        ("activation_precision", "min", "activation_precision_min"),
        ("activation_recall", "min", "activation_recall_min"),
        ("activation_f1", "min", "activation_f1_min"),
        ("false_activation_rate", "max", "false_activation_rate_max"),
        ("wrong_specialist_rate", "max", "wrong_specialist_rate_max"),
        ("overactivation_rate", "max", "overactivation_rate_max"),
        ("semantic_outcome_accuracy", "min", "semantic_outcome_accuracy_overall_min"),
    ):
        threshold = thresholds[threshold_key]
        if (comparator == "min" and bounds[metric] < threshold) or (
            comparator == "max" and bounds[metric] > threshold
        ):
            failures.append(metric)
    return {
        "certificate_type": "FUTILE_QUALIFICATION" if failures else "QUALIFICATION_STILL_POSSIBLE",
        "candidate_id": candidate_id,
        "terminal": bool(failures),
        "completed_case_ids": sorted(completed),
        "remaining_case_ids": sorted(case["id"] for case in remaining_cases),
        "observed": {
            "true_positives": tp,
            "false_positives": fp,
            "false_activations": false_activation,
            "wrong_specialists": wrong,
            "overactivations": over,
            "semantic_errors": semantic_errors,
        },
        "remaining_optimistic_expected_entrypoints": remaining_expected,
        "fixed_denominators": {
            "cases": total_cases,
            "negative_near_miss_cases": total_negative,
            "expected_entrypoints": total_expected,
        },
        "optimistic_final_bounds": bounds,
        "failed_bounds": failures,
    }


def materiality_futility_certificate(
    inputs: FrozenInputs,
    candidate_id: str,
    trials: list[dict[str, Any]],
    reference: dict[str, Any],
) -> dict[str, Any]:
    qualification = qualification_futility_certificate(inputs, candidate_id, trials)
    aggregates = finalized_candidate_aggregates(inputs, candidate_id, trials)
    contexts = [
        aggregate["observed_context_bytes"]
        for aggregate in aggregates
        if aggregate["case_class"] in ACTIVATION_RELEVANT_CLASSES
    ]
    total_relevant = sum(
        case["class"] in ACTIVATION_RELEVANT_CLASSES for case in inputs.corpus["cases"]
    )
    optimistic_context = statistics.median([*contexts, *([0] * (total_relevant - len(contexts)))])
    bounds = qualification["optimistic_final_bounds"]
    failures = list(qualification["failed_bounds"])
    if bounds["activation_f1"] < reference["activation_f1"] + 0.03:
        failures.append("material_activation_f1")
    if bounds["false_activation_rate"] > reference["false_activation_rate"]:
        failures.append("material_false_activation")
    if bounds["wrong_specialist_rate"] > reference["wrong_specialist_rate"] + 0.01:
        failures.append("material_wrong_specialist")
    if bounds["overactivation_rate"] > reference["overactivation_rate"] + 0.01:
        failures.append("material_overactivation")
    if optimistic_context > 0.85 * reference["median_observed_context_bytes"]:
        failures.append("material_context")
    return {
        "certificate_type": "FUTILE_MATERIALITY" if failures else "MATERIALITY_STILL_POSSIBLE",
        "candidate_id": candidate_id,
        "terminal": bool(failures),
        "qualification": qualification,
        "optimistic_median_observed_context_bytes": optimistic_context,
        "reference_metrics": reference,
        "failed_bounds": failures,
    }


def compute_candidate_metrics(
    inputs: FrozenInputs,
    candidate_id: str,
    trials: list[dict[str, Any]],
    deterministic_evidence: dict[str, Any],
) -> dict[str, Any]:
    selected = [trial for trial in trials if trial["candidate_id"] == candidate_id]
    aggregates = aggregate_candidate_trials(inputs, candidate_id, selected)

    tp = fp = fn = 0
    false_activation = wrong_specialist = overactivation = semantic_correct = 0
    negative_trials = 0
    cross_profile_violations = ambiguous_broadenings = 0
    cross_ambiguous_correct = cross_ambiguous_total = 0
    observed_context_bytes: list[int] = []
    loaded_reference_bytes: list[int] = []
    for trial in aggregates:
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
        if trial["case_class"] in ACTIVATION_RELEVANT_CLASSES:
            observed_context_bytes.append(trial["observed_context_bytes"])
            loaded_reference_bytes.append(trial["loaded_reference_bytes"])

    critical_trials = [
        trial for trial in selected if trial["case_class"] in {"cross-profile", "ambiguous"}
    ]
    cross_ambiguous_total = len(critical_trials)
    cross_ambiguous_correct = sum(
        trial["semantic_outcome"] == trial["expected_semantic_outcome"] for trial in critical_trials
    )
    cross_profile_violations = sum(
        trial["case_class"] == "cross-profile" and _critical_violation(trial) for trial in selected
    )
    ambiguous_broadenings = sum(
        trial["case_class"] == "ambiguous" and _critical_violation(trial) for trial in selected
    )

    precision = _safe_ratio(tp, tp + fp)
    recall = _safe_ratio(tp, tp + fn)
    f1 = 0.0 if precision + recall == 0 else 2 * precision * recall / (precision + recall)
    mandatory = inputs.oracle["mandatory_non_regression"]
    return {
        "candidate_id": candidate_id,
        "case_count": len(aggregates),
        "valid_repetition_count": len(selected),
        "activation_precision": precision,
        "activation_recall": recall,
        "activation_f1": f1,
        "false_activation_rate": _safe_ratio(false_activation, negative_trials),
        "wrong_specialist_rate": wrong_specialist / len(aggregates),
        "overactivation_rate": overactivation / len(aggregates),
        "semantic_outcome_accuracy": semantic_correct / len(aggregates),
        "semantic_outcome_accuracy_cross_profile_and_ambiguous": _safe_ratio(
            cross_ambiguous_correct, cross_ambiguous_total
        ),
        "cross_profile_violation_count": cross_profile_violations,
        "ambiguous_context_permission_broadening_count": ambiguous_broadenings,
        "median_observed_context_bytes": statistics.median(observed_context_bytes),
        "p95_observed_context_bytes": _p95(observed_context_bytes),
        "median_loaded_reference_bytes": statistics.median(loaded_reference_bytes),
        "p95_loaded_reference_bytes": _p95(loaded_reference_bytes),
        "first_two_disagreement_count": sum(
            bool(item["first_two_disagreement_fields"]) for item in aggregates
        ),
        "first_two_disagreement_rate": sum(
            bool(item["first_two_disagreement_fields"]) for item in aggregates
        )
        / len(aggregates),
        "conditional_third_repetition_count": sum(
            item["valid_repetitions"] == 3 for item in aggregates
        ),
        "valid_repetitions_per_case": dict(
            sorted(
                (str(count), frequency)
                for count, frequency in Counter(
                    item["valid_repetitions"] for item in aggregates
                ).items()
            )
        ),
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


def select_single_family_reference(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    if set(metrics_by_candidate) != {"B0", "B1"}:
        raise HarnessError("reference selection requires exactly B0 and B1 metrics")
    qualifying = {
        candidate: candidate_qualifies(inputs, metrics_by_candidate[candidate])
        for candidate in ("B0", "B1")
    }
    if not any(qualifying.values()):
        return {
            "status": "BLOCKED",
            "single_family_reference": None,
            "reason": "neither B0 nor B1 qualifies",
            "qualifying": qualifying,
        }
    if all(qualifying.values()):
        b0, b1 = metrics_by_candidate["B0"], metrics_by_candidate["B1"]
        b1_reference = (
            b1["activation_f1"] >= b0["activation_f1"] - 0.01
            and b1["false_activation_rate"] <= b0["false_activation_rate"] + 0.01
            and b1["median_observed_context_bytes"] <= 0.80 * b0["median_observed_context_bytes"]
        )
        reference_id = "B1" if b1_reference else "B0"
    else:
        reference_id = "B0" if qualifying["B0"] else "B1"
    return {
        "status": "REFERENCE_SELECTED",
        "single_family_reference": reference_id,
        "qualifying": qualifying,
    }


def apply_selection_rule(
    inputs: FrozenInputs, metrics_by_candidate: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    if set(metrics_by_candidate) != set(inputs.oracle["candidate_ids"]):
        raise HarnessError("final selection requires complete B0/B1/F2/G3 metrics")
    qualifying = {
        candidate: candidate_qualifies(inputs, metrics)
        for candidate, metrics in metrics_by_candidate.items()
    }
    reference_result = select_single_family_reference(
        inputs, {candidate: metrics_by_candidate[candidate] for candidate in ("B0", "B1")}
    )
    if reference_result["status"] == "BLOCKED":
        return {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": reference_result["reason"],
            "qualifying": qualifying,
        }
    reference_id = reference_result["single_family_reference"]

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


def select_from_cost_bounded_metrics(
    inputs: FrozenInputs,
    reference_id: str,
    metrics_by_candidate: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Apply unchanged challenger materiality/tie-breaks to completed survivors."""
    reference = metrics_by_candidate[reference_id]
    material = []
    for candidate in ("F2", "G3"):
        metrics = metrics_by_candidate.get(candidate)
        if metrics and (
            candidate_qualifies(inputs, metrics)
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
        f2, g3 = metrics_by_candidate["F2"], metrics_by_candidate["G3"]
        if abs(f2["activation_f1"] - g3["activation_f1"]) > 0.005:
            selected = max(material, key=lambda name: metrics_by_candidate[name]["activation_f1"])
        elif abs(f2["false_activation_rate"] - g3["false_activation_rate"]) > 0.01:
            selected = min(
                material, key=lambda name: metrics_by_candidate[name]["false_activation_rate"]
            )
        else:
            f2_load, g3_load = (
                f2["median_observed_context_bytes"],
                g3["median_observed_context_bytes"],
            )
            if abs(f2_load - g3_load) / max(f2_load, g3_load, 1) > 0.05:
                selected = min(
                    material,
                    key=lambda name: metrics_by_candidate[name]["median_observed_context_bytes"],
                )
            else:
                selected = min(
                    material,
                    key=lambda name: (
                        len(inputs.topologies["candidates"][name]["entrypoints"]),
                        name != "F2",
                    ),
                )
    return {
        "status": "SELECTED",
        "selected_candidate": selected,
        "single_family_reference": reference_id,
        "material_split_candidates": material,
        "qualifying": {
            candidate: candidate_qualifies(inputs, metrics)
            for candidate, metrics in metrics_by_candidate.items()
        },
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
        "trial_envelope_id": inputs.oracle["trial_envelope_id"],
        "frozen_asset_sha256": {
            path.relative_to(REPO_ROOT).as_posix(): _sha256(path)
            for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH)
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
    if "--sandbox" not in command or command[command.index("--sandbox") + 1] not in {
        "read-only",
        "workspace-write",
    }:
        raise HarnessError(f"{spec.key}: resumed execution used an invalid frozen sandbox")
    if not any(
        command[index : index + 2] == ["--config", f'windows.sandbox="{backend}"']
        for index in range(len(command) - 1)
        for backend in WINDOWS_BACKEND_ORDER
    ):
        raise HarnessError(f"{spec.key}: resumed execution lacked an explicit Windows backend")
    if "--ignore-user-config" not in command or "--ignore-rules" not in command:
        raise HarnessError(f"{spec.key}: resumed execution did not isolate host configuration")
    for feature in MINIMAL_DISABLED_FEATURES:
        if not any(
            command[index : index + 2] == ["--disable", feature]
            for index in range(len(command) - 1)
        ):
            raise HarnessError(f"{spec.key}: resumed execution enabled forbidden host surface")
    if "--ephemeral" not in command:
        raise HarnessError(f"{spec.key}: resumed execution was not ephemeral")
    fixture = raw.get("fixture_materialization", {})
    _validate_fixture_evidence(inputs, spec.case, fixture)
    isolation = raw.get("workspace_isolation", {})
    workspace = Path(command[command.index("--cd") + 1])
    canonical = REPO_ROOT.resolve(strict=True)
    root_folded = str(workspace).casefold()
    if (
        isolation.get("outside_canonical_repository") is not True
        or isolation.get("forbidden_root_substring_matches") != []
        or isolation.get("canonical_git_metadata_present") is not False
        or isolation.get("linked_components") != []
        or isolation.get("initially_empty") is not True
        or isolation.get("absolute_root") != str(workspace)
        or _is_relative_to(workspace, canonical)
        or any(
            term in root_folded
            for term in inputs.envelope["workspace_root_policy"][
                "forbidden_root_substrings_casefold"
            ]
        )
    ):
        raise HarnessError(f"{spec.key}: resumed workspace isolation evidence mismatch")
    workspace_evidence = raw.get("workspace", {})
    if (
        workspace_evidence.get("absolute_workspace_root") != str(workspace)
        or workspace_evidence.get("workspace_creation_method") != WORKSPACE_FACTORY_ID
        or workspace_evidence.get("workspace_acl_profile_identity") != WORKSPACE_FACTORY_ID
        or workspace_evidence.get("private_temp_creation_avoided") is not True
        or workspace_evidence.get("cleanup_result") != "REMOVED"
    ):
        raise HarnessError(f"{spec.key}: resumed v10 workspace factory evidence mismatch")


def execute_logical_observation(
    inputs: FrozenInputs, spec: TrialSpec, *, output: Path, **kwargs: Any
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Persist model attempts; explicit capacity events consume no attempt ordinal."""
    limit = inputs.oracle["trial_method"]["max_model_attempts_per_scheduled_observation"]
    prior = [
        _load_json(path) for path in sorted((output / "attempts").glob(f"{spec.key}--a*.json"))
    ]
    if [item["attempt"] for item in prior] != list(range(1, len(prior) + 1)):
        raise HarnessError(f"{spec.key}: invalid persisted attempt sequence")
    valid = [item for item in prior if item["status"] == "VALID"]
    if len(valid) > 1 or (valid and valid[-1] is not prior[-1]):
        raise HarnessError(f"{spec.key}: retry after valid observation")
    if valid:
        return valid[0]["structured"], valid[0]["raw"]
    for attempt in range(len(prior) + 1, limit + 1):
        journal = output / "attempts" / f"{spec.key}--a{attempt}.json"
        if journal.exists():
            raise HarnessError(f"refusing to overwrite attempt journal: {journal.name}")
        record = {
            "trial_key": spec.key,
            "candidate_id": spec.candidate_id,
            "attempt": attempt,
            "execution_epoch": inputs.oracle["execution_epoch"],
            "status": "STARTED",
            "started_at": datetime.now(UTC).isoformat(),
        }
        try:
            structured, raw = run_trial(inputs, spec, attempt=attempt, **kwargs)
        except CapacityPause as exc:
            capacity_dir = output / "capacity-events"
            ordinal = len(list(capacity_dir.glob(f"{spec.key}--c*.json"))) + 1
            _json_dump(
                capacity_dir / f"{spec.key}--c{ordinal}.json",
                {
                    "trial_key": spec.key,
                    "candidate_id": spec.candidate_id,
                    "pending_attempt": attempt,
                    "execution_epoch": inputs.oracle["execution_epoch"],
                    "status": "EXTERNAL_CAPACITY",
                    "recorded_at": datetime.now(UTC).isoformat(),
                    "raw": exc.raw,
                },
            )
            raise
        except AttemptFailure as exc:
            record.update(
                status="FAILED", failure_class=exc.failure_class, error=str(exc), raw=exc.raw
            )
        except HarnessError as exc:
            # Setup failed before the model invocation; there is no observation to score.
            record.update(status="FAILED", failure_class="ATTEMPT_SETUP_ERROR", error=str(exc))
        else:
            record.update(status="VALID", structured=structured, raw=raw)
        record["completed_at"] = datetime.now(UTC).isoformat()
        _json_dump(journal, record)
        if record["status"] == "VALID":
            return structured, raw
        print(f"failed attempt {attempt}/{limit} {spec.key}: {record['failure_class']}", flush=True)
    return None


def validate_execution_config(inputs: FrozenInputs, args: argparse.Namespace) -> None:
    method = inputs.oracle["trial_method"]
    if args.model != "gpt-5.6-sol" or args.effort != "medium" or platform.system() != "Windows":
        raise HarnessError("required live cell is native Windows / GPT-5.6 Sol / Medium")
    if _codex_version(args.codex_command) != REQUIRED_CODEX_VERSION:
        raise HarnessError(f"required Codex CLI baseline is {REQUIRED_CODEX_VERSION}")
    if args.timeout_seconds != method["timeout_seconds_per_model_attempt"]:
        raise HarnessError("per-attempt timeout must match the frozen oracle")
    if args.full_acceptance and (args.case or args.candidate or args.repetition):
        raise HarnessError("full acceptance cannot use trial filters")
    if (
        len(stage_schedule(inputs, "R"))
        != method["reference_stage_full_completion_base_valid_observations"]
    ):
        raise HarnessError("reference-stage base schedule does not match the frozen oracle")
    if (
        len(stage_schedule(inputs, "C"))
        != method["challenger_stage_full_completion_base_valid_observations"]
    ):
        raise HarnessError("challenger-stage base schedule does not match the frozen oracle")


def run_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    validate_execution_config(inputs, args)
    output = args.output.resolve()
    workspace_parent = Path(tempfile.gettempdir()).resolve()
    if args.resume:
        if not output.is_dir():
            raise HarnessError("resume requires an existing evidence root")
        run_metadata = _load_json(output / "run-metadata.json")
        expected_identity = {
            "oracle_id": inputs.oracle["oracle_id"],
            "execution_epoch": inputs.oracle["execution_epoch"],
            "corpus_id": inputs.oracle["corpus_id"],
            "trial_envelope_id": inputs.oracle["trial_envelope_id"],
            "presentation_revision": inputs.oracle["presentation_revision"],
            "capability_source_epoch": inputs.oracle["capability_source_epoch"],
            "model": args.model,
            "effort": args.effort,
            "timeout_seconds": args.timeout_seconds,
        }
        if any(run_metadata.get(key) != value for key, value in expected_identity.items()):
            raise HarnessError("resume execution identity differs from frozen V10 run")
        if run_metadata.get("runner_sha256") != _sha256(Path(__file__)):
            raise HarnessError("resume runner identity changed")
        for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH):
            relative = path.relative_to(REPO_ROOT).as_posix()
            if run_metadata["frozen_asset_sha256"].get(relative) != _sha256(path):
                raise HarnessError(f"resume frozen asset changed: {relative}")
        run_metadata.setdefault("resume_records", []).append(
            {"resumed_at": datetime.now(UTC).isoformat(), "prior_status": run_metadata["status"]}
        )
        host_preflight = _load_json(output / "host-preflight.json")
        if (
            host_preflight.get("status") != "PASS"
            or run_metadata.get("selected_sandbox") != host_preflight.get("selected_sandbox")
            or run_metadata.get("selected_backend") != host_preflight.get("selected_backend")
            or run_metadata.get("selected_workspace_acl_profile")
            != host_preflight.get("selected_workspace_acl_profile")
        ):
            raise HarnessError("resume host preflight/profile identity mismatch")
    else:
        if output.exists() and any(output.iterdir()):
            raise HarnessError("refusing to overwrite existing run evidence")
        output.mkdir(parents=True, exist_ok=True)
        codex_version = _codex_version(args.codex_command)
        run_metadata = {
            "oracle_id": inputs.oracle["oracle_id"],
            "execution_epoch": inputs.oracle["execution_epoch"],
            "corpus_id": inputs.oracle["corpus_id"],
            "trial_envelope_id": inputs.oracle["trial_envelope_id"],
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
                for path in (
                    ORACLE_PATH,
                    CORPUS_PATH,
                    TOPOLOGIES_PATH,
                    MANIFEST_PATH,
                    ENVELOPE_PATH,
                )
            },
            "workers": args.workers,
            "timeout_seconds": args.timeout_seconds,
            "max_model_attempts_per_scheduled_observation": inputs.oracle["trial_method"][
                "max_model_attempts_per_scheduled_observation"
            ],
            "full_acceptance": args.full_acceptance,
            "clean_context": "one new codex exec thread and disposable workspace per attempt",
            "workspace_parent": str(workspace_parent),
            "workspace_factory": WORKSPACE_FACTORY_ID,
            "sandbox_selection_order": ["read-only", "workspace-write"],
            "windows_backend_selection_order": list(WINDOWS_BACKEND_ORDER),
            "stimulus_rule": "exact corpus prompt, two newlines, frozen neutral suffix",
            "stage_state": "REFERENCE_BASE_PENDING" if args.full_acceptance else "FILTERED_PENDING",
            "status": "RUNNING",
            "started_at": datetime.now(UTC).isoformat(),
        }
        _json_dump(output / "run-metadata.json", run_metadata)
        if args.full_acceptance:
            _json_dump(output / "deterministic-evidence.json", build_deterministic_evidence(inputs))
            verify_args = argparse.Namespace(output=output, timeout_seconds=900)
            if verify_deterministic(verify_args) != 0:
                run_metadata.update(status="BLOCKED", stage_state="DETERMINISTIC_GATE_FAILED")
                _json_dump(output / "run-metadata.json", run_metadata)
                _json_dump(
                    output / "selection.json",
                    {
                        "status": "BLOCKED",
                        "selected_candidate": None,
                        "reason": "mandatory deterministic verification failed before live execution",
                    },
                )
                return 1
            preflight = run_host_preflight(inputs, args, output, workspace_parent)
            if preflight["status"] != "PASS":
                reason = preflight["reason"]
                run_metadata.update(
                    status="BLOCKED",
                    stage_state=f"{reason}_FAILED",
                    selected_backend=None,
                    selected_sandbox=None,
                    selected_workspace_acl_profile=None,
                    synthetic_canary_prompts_issued=len(preflight.get("records", [])),
                    completed_valid_observations=0,
                    acceptance_prompts_issued=0,
                )
                _json_dump(output / "run-metadata.json", run_metadata)
                _json_dump(
                    output / "selection.json",
                    {
                        "status": "BLOCKED",
                        "selected_candidate": None,
                        "reason": reason,
                        "scored": False,
                    },
                )
                _json_dump(
                    output / "completeness.json",
                    {
                        "execution_epoch": inputs.oracle["execution_epoch"],
                        "stage_state": f"{reason}_FAILED",
                        "completed_valid_observations": 0,
                        "acceptance_prompts_issued": 0,
                        "acceptance_complete": False,
                        "partial_scoring_permitted": False,
                    },
                )
                return 1
            run_metadata["selected_backend"] = preflight["selected_backend"]
            run_metadata["selected_sandbox"] = preflight["selected_sandbox"]
            run_metadata["selected_workspace_acl_profile"] = preflight[
                "selected_workspace_acl_profile"
            ]
            run_metadata["effective_host_profile"] = _load_json(output / "host-preflight.json")[
                "records"
            ][-1]["effective_host_profile"]
    _json_dump(output / "run-metadata.json", run_metadata)

    def execute(spec: TrialSpec):
        return execute_logical_observation(
            inputs,
            spec,
            output=output,
            codex_command=args.codex_command,
            model=args.model,
            effort=args.effort,
            timeout_seconds=args.timeout_seconds,
            workspace_parent=workspace_parent,
            backend=run_metadata.get("selected_backend", "elevated"),
            sandbox=run_metadata.get("selected_sandbox", "read-only"),
        )

    def persisted_results() -> dict[str, tuple[dict[str, Any], dict[str, Any]]]:
        values = {}
        for path in sorted((output / "attempts").glob("*.json")):
            item = _load_json(path)
            if item["status"] == "VALID":
                if item["trial_key"] in values:
                    raise HarnessError(f"{item['trial_key']}: duplicate valid attempt")
                values[item["trial_key"]] = (item["structured"], item["raw"])
        return values

    def export_evidence(stage_state: str, status: str, blocked: list[str] | None = None) -> None:
        results = persisted_results()
        specs = {spec.key: spec for spec in all_possible_trials(inputs)}
        ordered = [key for key in specs if key in results]
        _jsonl_dump(output / "trials.jsonl", (results[key][0] for key in ordered))
        _jsonl_dump(output / "raw-trials.jsonl", (results[key][1] for key in ordered))
        attempts = [_load_json(path) for path in sorted((output / "attempts").glob("*.json"))]
        capacity = [
            _load_json(path) for path in sorted((output / "capacity-events").glob("*.json"))
        ]
        _jsonl_dump(output / "attempts.jsonl", attempts)
        _jsonl_dump(
            output / "failed-attempts.jsonl", [x for x in attempts if x["status"] == "FAILED"]
        )
        _jsonl_dump(output / "capacity-events.jsonl", capacity)
        run_metadata.update(
            status=status,
            stage_state=stage_state,
            completed_valid_observations=len(results),
            capacity_event_count=len(capacity),
            updated_at=datetime.now(UTC).isoformat(),
        )
        _json_dump(output / "run-metadata.json", run_metadata)
        _json_dump(
            output / "completeness.json",
            {
                "execution_epoch": inputs.oracle["execution_epoch"],
                "stage_state": stage_state,
                "completed_valid_observations": len(results),
                "exhausted_observations": blocked or [],
                "capacity_event_count": len(capacity),
                "acceptance_complete": status in {"COMPLETE", "BLOCKED_NO_REFERENCE"},
                "partial_scoring_permitted": False,
            },
        )
        _json_dump(
            output / "retry-diagnostics.json",
            {
                candidate: {
                    "model_attempts": sum(x["candidate_id"] == candidate for x in attempts),
                    "non_capacity_failures": sum(
                        x["candidate_id"] == candidate and x["status"] == "FAILED" for x in attempts
                    ),
                    "capacity_events": sum(x["candidate_id"] == candidate for x in capacity),
                    "failure_classes": dict(
                        Counter(
                            x["failure_class"]
                            for x in attempts
                            if x["candidate_id"] == candidate and x["status"] == "FAILED"
                        )
                    ),
                }
                for candidate in inputs.oracle["candidate_ids"]
            },
        )

    def execute_schedule(schedule: list[TrialSpec]) -> tuple[list[str], bool]:
        completed = set(persisted_results())
        pending = iter([spec for spec in schedule if spec.key not in completed])
        blocked: list[str] = []
        capacity_pause = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures: dict[concurrent.futures.Future, TrialSpec] = {}
            for _ in range(args.workers):
                spec = next(pending, None)
                if spec is not None:
                    futures[executor.submit(execute, spec)] = spec
            while futures:
                done, _ = concurrent.futures.wait(
                    futures, return_when=concurrent.futures.FIRST_COMPLETED
                )
                for future in done:
                    spec = futures.pop(future)
                    try:
                        result = future.result()
                    except CapacityPause:
                        capacity_pause = True
                    else:
                        if result is None:
                            blocked.append(spec.key)
                        else:
                            completed.add(spec.key)
                            print(f"completed {len(completed)} {spec.key}", flush=True)
                if not blocked and not capacity_pause:
                    for _ in range(args.workers - len(futures)):
                        spec = next(pending, None)
                        if spec is not None:
                            futures[executor.submit(execute, spec)] = spec
        return blocked, capacity_pause

    def stop_for_execution_state(blocked: list[str], capacity: bool, state: str) -> int | None:
        if capacity:
            export_evidence(state, "PAUSED_EXTERNAL_CAPACITY", blocked)
            _json_dump(
                output / "selection.json",
                {"status": "PAUSED_EXTERNAL_CAPACITY", "selected_candidate": None, "scored": False},
            )
            return 2
        if blocked:
            export_evidence(state, "BLOCKED", blocked)
            _json_dump(
                output / "selection.json",
                {
                    "status": "BLOCKED",
                    "selected_candidate": None,
                    "reason": "scheduled observation exhausted two non-capacity model attempts",
                    "scored": False,
                },
            )
            return 1
        return None

    if not args.full_acceptance:
        schedule = scheduled_trials(inputs)
        if args.case:
            schedule = [spec for spec in schedule if spec.case["id"] in set(args.case)]
        if args.candidate:
            schedule = [spec for spec in schedule if spec.candidate_id in set(args.candidate)]
        if args.repetition:
            schedule = [spec for spec in schedule if spec.repetition in set(args.repetition)]
        if not schedule:
            raise HarnessError("trial filters selected no trials")
        blocked, capacity = execute_schedule(schedule)
        terminal = stop_for_execution_state(blocked, capacity, "FILTERED")
        if terminal is not None:
            return terminal
        export_evidence("FILTERED_COMPLETE", "COMPLETE")
        return 0

    terminal_candidates: dict[str, dict[str, Any]] = {}

    def adaptive_stage(
        stage: str,
        candidates: list[str],
        reference_metrics: dict[str, Any] | None = None,
    ) -> int | None:
        ordered_cases = sorted(
            inputs.corpus["cases"],
            key=lambda case: (V10_CLASS_ORDER.index(case["class"]), case["id"]),
        )
        for case_index, case in enumerate(ordered_cases):
            rotated = (
                candidates[case_index % len(candidates) :]
                + candidates[: case_index % len(candidates)]
            )
            for candidate in rotated:
                if candidate in terminal_candidates:
                    continue
                for repetition in (1, 2):
                    spec = TrialSpec(case, candidate, repetition)
                    blocked, capacity = execute_schedule([spec])
                    stopped = stop_for_execution_state(
                        blocked, capacity, f"{stage}_{case['id']}_{candidate}_INCOMPLETE"
                    )
                    if stopped is not None:
                        return stopped
                    trials = [value[0] for value in persisted_results().values()]
                    certificate = qualification_futility_certificate(inputs, candidate, trials)
                    if certificate["terminal"]:
                        terminal_candidates[candidate] = certificate
                        _json_dump(
                            output / "futility-certificates" / f"{candidate}.json", certificate
                        )
                        break
                if candidate in terminal_candidates:
                    continue
                trials = [value[0] for value in persisted_results().values()]
                third = [
                    spec
                    for spec in conditional_third_specs(inputs, [candidate], trials)
                    if spec.case["id"] == case["id"]
                ]
                if third:
                    blocked, capacity = execute_schedule(third)
                    stopped = stop_for_execution_state(
                        blocked, capacity, f"{stage}_{case['id']}_{candidate}_THIRD_INCOMPLETE"
                    )
                    if stopped is not None:
                        return stopped
                trials = [value[0] for value in persisted_results().values()]
                certificate = qualification_futility_certificate(inputs, candidate, trials)
                if not certificate["terminal"] and reference_metrics is not None:
                    certificate = materiality_futility_certificate(
                        inputs, candidate, trials, reference_metrics
                    )
                if certificate["terminal"]:
                    terminal_candidates[candidate] = certificate
                    _json_dump(output / "futility-certificates" / f"{candidate}.json", certificate)
        return None

    deterministic = _load_json(output / "deterministic-evidence.json")
    reference_candidates = inputs.oracle["trial_method"]["reference_stage_candidates"]
    stopped = adaptive_stage("R", reference_candidates)
    if stopped is not None:
        return stopped
    trials = [value[0] for value in persisted_results().values()]
    reference_survivors = [c for c in reference_candidates if c not in terminal_candidates]
    reference_metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in reference_survivors
    }
    if not reference_survivors:
        _json_dump(output / "metrics-reference.json", {})
        _json_dump(
            output / "reference-selection.json",
            {
                "status": "BLOCKED",
                "single_family_reference": None,
                "reason": "both single-family candidates are FUTILE_QUALIFICATION",
                "futility": terminal_candidates,
            },
        )
        _json_dump(
            output / "selection.json",
            {
                "status": "BLOCKED",
                "selected_candidate": None,
                "reason": "NO QUALIFYING SINGLE-FAMILY REFERENCE",
                "scored": True,
            },
        )
        _jsonl_dump(
            output / "case-aggregates.jsonl",
            [
                item
                for candidate in reference_candidates
                for item in finalized_candidate_aggregates(inputs, candidate, trials)
            ],
        )
        export_evidence("REFERENCE_FUTILE_NO_QUALIFIER", "BLOCKED_NO_REFERENCE")
        return 1
    if len(reference_survivors) == 1:
        reference_id = reference_survivors[0]
        reference = {
            "status": "REFERENCE_SELECTED",
            "single_family_reference": reference_id,
            "qualifying": {
                reference_id: candidate_qualifies(inputs, reference_metrics[reference_id])
            },
            "futility": terminal_candidates,
        }
    else:
        reference = select_single_family_reference(inputs, reference_metrics)
        reference_id = reference["single_family_reference"]
    if reference_id is None:
        raise HarnessError("completed reference stage produced no valid reference")
    run_metadata["single_family_reference"] = reference_id
    _json_dump(output / "reference-selection.json", reference)
    _json_dump(output / "metrics-reference.json", reference_metrics)

    challenger_candidates = inputs.oracle["trial_method"]["challenger_stage_candidates"]
    stopped = adaptive_stage("C", challenger_candidates, reference_metrics[reference_id])
    if stopped is not None:
        return stopped
    trials = [value[0] for value in persisted_results().values()]
    challenger_survivors = [c for c in challenger_candidates if c not in terminal_candidates]
    metrics = dict(reference_metrics)
    metrics.update(
        {
            candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
            for candidate in challenger_survivors
        }
    )
    selection = select_from_cost_bounded_metrics(inputs, reference_id, metrics)
    selection["futility"] = terminal_candidates
    _json_dump(output / "metrics.json", metrics)
    _json_dump(output / "selection.json", selection)
    _jsonl_dump(
        output / "case-aggregates.jsonl",
        [
            item
            for candidate in inputs.oracle["candidate_ids"]
            for item in finalized_candidate_aggregates(inputs, candidate, trials)
        ],
    )
    export_evidence("COST_BOUNDED_DECISION_COMPLETE", "COMPLETE")
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


def _validate_executed_runner_provenance(metadata: dict[str, Any]) -> None:
    recorded = metadata.get("runner_sha256")
    if recorded == _sha256(Path(__file__)):
        return
    commit = metadata.get("executed_runner_git_commit")
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise HarnessError("executed runner changed without immutable Git provenance")
    relative = Path(__file__).relative_to(REPO_ROOT).as_posix()
    try:
        source = subprocess.check_output(
            ["git", "show", f"{commit}:{relative}"], cwd=REPO_ROOT, stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as exc:
        raise HarnessError("cannot resolve executed runner Git provenance") from exc
    normalized_digests = {
        hashlib.sha256(source).hexdigest(),
        hashlib.sha256(source.replace(b"\r\n", b"\n")).hexdigest(),
        hashlib.sha256(source.replace(b"\n", b"\r\n")).hexdigest(),
    }
    if recorded not in normalized_digests:
        raise HarnessError("executed runner Git provenance does not match recorded hash")


def validate_complete_evidence(inputs: FrozenInputs, output: Path) -> None:
    """Fail closed on V10 epoch, adaptive schedule, attempts, traces and aggregates."""
    metadata = _load_json(output / "run-metadata.json")
    method = inputs.oracle["trial_method"]
    if metadata.get("status") not in {"COMPLETE", "BLOCKED_NO_REFERENCE"}:
        raise HarnessError("incomplete V10 execution cannot be scored")
    if (
        metadata.get("oracle_id") != inputs.oracle["oracle_id"]
        or metadata.get("execution_epoch") != inputs.oracle["execution_epoch"]
        or metadata.get("trial_envelope_id") != inputs.oracle["trial_envelope_id"]
        or metadata.get("full_acceptance") is not True
        or metadata.get("model") != "gpt-5.6-sol"
        or metadata.get("effort") != "medium"
        or metadata.get("host") != "Codex"
        or metadata.get("timeout_seconds") != method["timeout_seconds_per_model_attempt"]
    ):
        raise HarnessError("mismatched V10 execution identity/configuration")
    _validate_executed_runner_provenance(metadata)
    for path in (ORACLE_PATH, CORPUS_PATH, TOPOLOGIES_PATH, MANIFEST_PATH, ENVELOPE_PATH):
        relative = path.relative_to(REPO_ROOT).as_posix()
        if metadata["frozen_asset_sha256"].get(relative) != _sha256(path):
            raise HarnessError(f"run frozen input hash mismatch: {relative}")

    deterministic = _load_json(output / "deterministic-evidence.json")
    if any(
        deterministic.get(field) != "PASS"
        for field in (
            "full_deterministic_regression",
            "profile_isolation_regression",
            "consumer_source_independence_regression",
        )
    ):
        raise HarnessError("mandatory deterministic evidence is not PASS")

    trials = load_trials(output / "trials.jsonl")
    raw_trials = load_trials(output / "raw-trials.jsonl")
    attempts = load_trials(output / "attempts.jsonl")
    possible = {spec.key: spec for spec in all_possible_trials(inputs)}
    trial_keys = [
        f"{trial['case_id']}--{trial['candidate_id']}--r{trial['repetition']}" for trial in trials
    ]
    raw_keys = [raw["trial_key"] for raw in raw_trials]
    if len(set(trial_keys)) != len(trial_keys) or set(trial_keys) != set(raw_keys):
        raise HarnessError("valid trial/raw identity mismatch or duplication")
    if set(trial_keys) - set(possible):
        raise HarnessError("trial outside frozen V10 identity set")
    evaluated = (
        ["B0", "B1"]
        if metadata["status"] == "BLOCKED_NO_REFERENCE"
        else inputs.oracle["candidate_ids"]
    )
    expected_base = {
        spec.key
        for stage in (("R",) if len(evaluated) == 2 else ("R", "C"))
        for spec in stage_schedule(inputs, stage)
    }
    if not expected_base <= set(trial_keys):
        raise HarnessError("mandatory paired base schedule is incomplete")
    if metadata["status"] == "BLOCKED_NO_REFERENCE" and any(
        trial["candidate_id"] in {"F2", "G3"} for trial in trials
    ):
        raise HarnessError("challenger evidence exists despite no qualifying reference")
    lower = method["reference_stage_base_valid_observations"]
    upper = method["reference_stage_max_valid_observations"]
    if len(evaluated) == 4:
        lower, upper = method["overall_valid_observation_range_when_challengers_execute"]
    if not lower <= len(trials) <= upper:
        raise HarnessError("V10 valid observation count is outside the frozen stage range")

    raw_by_key = dict(zip(raw_keys, raw_trials, strict=True))
    trial_by_key = dict(zip(trial_keys, trials, strict=True))
    thread_ids: set[str] = set()
    workspaces: set[str] = set()
    for key, trial in trial_by_key.items():
        spec = possible[key]
        history = sorted(
            (item for item in attempts if item["trial_key"] == key),
            key=lambda item: item["attempt"],
        )
        if (
            not 1 <= len(history) <= method["max_model_attempts_per_scheduled_observation"]
            or [item["attempt"] for item in history] != list(range(1, len(history) + 1))
            or [item["status"] for item in history] != ["FAILED"] * (len(history) - 1) + ["VALID"]
        ):
            raise HarnessError(f"{key}: invalid attempt count/order")
        raw = raw_by_key[key]
        if history[-1]["structured"] != trial or history[-1]["raw"] != raw:
            raise HarnessError(f"{key}: scored result differs from first valid attempt")
        for item in history:
            if item["execution_epoch"] != inputs.oracle["execution_epoch"]:
                raise HarnessError(f"{key}: prior epoch attempt")
        _validate_partial(inputs, spec, trial, raw, model="gpt-5.6-sol", effort="medium")
        if (
            raw.get("prompt") != _trial_prompt(inputs, spec.case)
            or raw.get("returncode") != 0
            or raw.get("timeout_seconds") != method["timeout_seconds_per_model_attempt"]
        ):
            raise HarnessError(f"{key}: raw execution binding mismatch")
        for record in raw["materialization"]["files"]:
            if record["sha256"] != _sha256(REPO_ROOT / record["source"]):
                raise HarnessError(f"{key}: candidate bytes changed")
        command = raw["command"]
        workspace = command[command.index("--cd") + 1]
        if workspace in workspaces:
            raise HarnessError(f"{key}: workspace reused")
        workspaces.add(workspace)
        threads = []
        for line in raw["stdout_jsonl"].splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "thread.started":
                threads.append(event["thread_id"])
        if len(threads) != 1 or set(threads) & thread_ids:
            raise HarnessError(f"{key}: missing or reused fresh thread")
        thread_ids.update(threads)
        model_result = json.loads(raw["final_message"])
        _validate_model_result(inputs, spec, model_result)
        entrypoints, references, trace = _observed_skill_reads(inputs, spec, raw["stdout_jsonl"])
        reference_bytes = sum((REPO_ROOT / path).stat().st_size for path in references)
        if (
            not trace
            or trial.get("host_trace_available") is not True
            or trial["activated_entrypoints"] != entrypoints
            or trial["loaded_reference_paths"] != references
            or trial["loaded_reference_bytes"] != reference_bytes
            or trial["observed_context_bytes"]
            != sum(trial["activation_surface_bytes"].values()) + reference_bytes
        ):
            raise HarnessError(f"{key}: observed host-read evidence mismatch")

    aggregates = [
        item
        for candidate in evaluated
        for item in aggregate_candidate_trials(inputs, candidate, trials)
    ]
    if aggregates != load_trials(output / "case-aggregates.jsonl"):
        raise HarnessError("persisted V10 case aggregates are not exactly recomputable")
    recomputed_metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in evaluated
    }
    if recomputed_metrics != _load_json(output / "metrics.json"):
        raise HarnessError("persisted V10 metrics are not exactly recomputable")
    expected_selection = (
        {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "neither B0 nor B1 qualifies; challenger stage not executed",
            "qualifying": select_single_family_reference(inputs, recomputed_metrics)["qualifying"],
            "scored": True,
        }
        if len(evaluated) == 2
        else apply_selection_rule(inputs, recomputed_metrics)
    )
    if expected_selection != _load_json(output / "selection.json"):
        raise HarnessError("persisted V10 selection is not exactly recomputable")


def score_matrix(args: argparse.Namespace) -> int:
    inputs = load_frozen_inputs()
    output = args.output.resolve()
    validate_complete_evidence(inputs, output)
    metadata = _load_json(output / "run-metadata.json")
    trials = load_trials(output / "trials.jsonl")
    deterministic = _load_json(output / "deterministic-evidence.json")
    candidates = (
        ["B0", "B1"]
        if metadata["status"] == "BLOCKED_NO_REFERENCE"
        else inputs.oracle["candidate_ids"]
    )
    metrics = {
        candidate: compute_candidate_metrics(inputs, candidate, trials, deterministic)
        for candidate in candidates
    }
    selection = (
        _load_json(output / "selection.json")
        if len(candidates) == 2
        else apply_selection_rule(inputs, metrics)
    )
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
    run.add_argument("--timeout-seconds", type=int, default=180)
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
