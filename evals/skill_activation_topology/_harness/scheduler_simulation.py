"""Provider-free characterization of the MG1 v12 adaptive scheduler."""

from __future__ import annotations

import hashlib
import tempfile
from collections.abc import Callable
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from .models import V12_CLASS_ORDER, FrozenInputs, HarnessError, TrialSpec
from .run_support import Observation, RunContext
from .scheduling import expected_entrypoints
from .storage import _json_dump


def _scripted_observation(inputs: FrozenInputs, spec: TrialSpec) -> dict[str, Any]:
    expected = expected_entrypoints(inputs, spec)
    return {
        "case_id": spec.case["id"],
        "case_class": spec.case["class"],
        "candidate_id": spec.candidate_id,
        "repetition": spec.repetition,
        "activated_entrypoints": expected,
        "expected_entrypoints": expected,
        "semantic_outcome": spec.case["expected_semantic_outcome"],
        "expected_semantic_outcome": spec.case["expected_semantic_outcome"],
        "granted_capabilities": spec.case["expected_capabilities"],
        "forbidden_capabilities": spec.case.get("forbidden_capabilities", []),
        "permission_broadening": False,
        "observed_context_bytes": 1000,
        "loaded_reference_bytes": 0,
    }


def _simulation_context(
    inputs: FrozenInputs,
    output: Path,
    mutate: Callable[[dict[str, Any], TrialSpec], None] | None = None,
) -> tuple[RunContext, list[str]]:
    calls: list[str] = []

    def fake_adapter(
        simulation_inputs: FrozenInputs, spec: TrialSpec, *, output: Path, **_: Any
    ) -> Observation:
        calls.append(spec.key)
        structured = _scripted_observation(simulation_inputs, spec)
        if mutate is not None:
            mutate(structured, spec)
        raw = {"trial_key": spec.key, "provider_model_call_issued": False}
        _json_dump(
            output / "attempts" / f"{spec.key}--a1.json",
            {
                "trial_key": spec.key,
                "candidate_id": spec.candidate_id,
                "attempt": 1,
                "execution_epoch": simulation_inputs.oracle["execution_epoch"],
                "status": "VALID",
                "structured": structured,
                "raw": raw,
            },
        )
        return structured, raw

    args = SimpleNamespace(
        codex_command="PROVIDER_FREE_FAKE",
        model="PROVIDER_FREE_FAKE",
        effort="none",
        timeout_seconds=0,
        workers=1,
    )
    return RunContext(inputs, args, output, output, {}, fake_adapter), calls


def _run_pairs(context: RunContext, cases: list[dict[str, Any]], error: str) -> None:
    for case in cases:
        if context._candidate_case("R", case, "B0", None) is not None:
            raise HarnessError(error)


def _agreeing_scenario(
    inputs: FrozenInputs, root: Path, ordered: list[dict[str, Any]]
) -> list[str]:
    context, calls = _simulation_context(inputs, root / "agree")
    _run_pairs(context, ordered[:2], "scheduler simulation agreeing path stopped unexpectedly")
    expected = [f"{case['id']}--B0--r{rep}" for case in ordered[:2] for rep in (1, 2)]
    if calls != expected:
        raise HarnessError("scheduler simulation agreeing path did not advance pair-scoped")
    return calls


def _conditional_scenario(
    inputs: FrozenInputs, root: Path, ordered: list[dict[str, Any]]
) -> list[str]:
    first_id = ordered[0]["id"]

    def disagree(record: dict[str, Any], spec: TrialSpec) -> None:
        if (spec.case["id"], spec.candidate_id, spec.repetition) == (first_id, "B0", 2):
            record["observed_context_bytes"] += 1

    context, calls = _simulation_context(inputs, root / "third", disagree)
    _run_pairs(context, ordered[:2], "scheduler simulation conditional-third path stopped")
    expected = [
        f"{first_id}--B0--r1",
        f"{first_id}--B0--r2",
        f"{first_id}--B0--r3",
        f"{ordered[1]['id']}--B0--r1",
        f"{ordered[1]['id']}--B0--r2",
    ]
    if calls != expected:
        raise HarnessError("scheduler simulation did not schedule exactly one pair-scoped third")
    try:
        context.execute(TrialSpec(ordered[0], "B0", 4))
    except HarnessError:
        return calls
    raise HarnessError("scheduler simulation accepted forbidden fourth repetition")


def _critical_scenario(
    inputs: FrozenInputs, root: Path, ordered: list[dict[str, Any]]
) -> list[str]:
    def critical(record: dict[str, Any], spec: TrialSpec) -> None:
        if spec.repetition == 1:
            record["semantic_outcome"] = "activate"

    context, calls = _simulation_context(inputs, root / "critical", critical)
    _run_pairs(context, ordered[:1], "scheduler simulation critical path execution failure")
    if calls != [f"{ordered[0]['id']}--B0--r1"] or "B0" not in (context.terminal_candidates or {}):
        raise HarnessError("scheduler simulation did not terminate critical candidate immediately")
    return calls


def _full_reference_scenario(
    inputs: FrozenInputs, root: Path, ordered: list[dict[str, Any]]
) -> int:
    context, calls = _simulation_context(inputs, root / "full-reference")
    if context.adaptive_stage("R", ["B0", "B1"]) is not None:
        raise HarnessError("scheduler simulation full reference stage stopped unexpectedly")
    expected = len(ordered) * 2 * 2
    if len(calls) != expected or context.terminal_candidates:
        raise HarnessError("scheduler simulation did not traverse the full reference stage")
    return len(calls)


def _tested_module_hashes() -> dict[str, str]:
    modules = (
        Path(__file__).with_name(name)
        for name in (
            "run_support.py",
            "aggregation.py",
            "scheduling.py",
            "scheduler_simulation.py",
        )
    )
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in modules}


def run_provider_free_scheduler_simulation(inputs: FrozenInputs) -> dict[str, Any]:
    """Exercise v12 adaptive scheduling with an injected non-provider adapter."""
    ordered = sorted(
        inputs.corpus["cases"],
        key=lambda case: (V12_CLASS_ORDER.index(case["class"]), case["id"]),
    )
    with tempfile.TemporaryDirectory(prefix="t023-scheduler-v12-") as temporary:
        root = Path(temporary)
        agreeing = _agreeing_scenario(inputs, root, ordered)
        conditional = _conditional_scenario(inputs, root, ordered)
        critical = _critical_scenario(inputs, root, ordered)
        full_count = _full_reference_scenario(inputs, root, ordered)
    return {
        "status": "PASS",
        "execution_epoch": inputs.oracle["execution_epoch"],
        "provider_model_calls_issued": 0,
        "tested_module_sha256": _tested_module_hashes(),
        "scenarios": {
            "agreeing_pair_forward_progress": {"status": "PASS", "scheduled": agreeing},
            "conditional_third_forward_progress": {
                "status": "PASS",
                "scheduled": conditional,
            },
            "no_fourth_repetition": {"status": "PASS"},
            "critical_terminal": {"status": "PASS", "scheduled": critical},
            "full_reference_adaptive_dry_run": {
                "status": "PASS",
                "scheduled_observations": full_count,
            },
        },
    }
