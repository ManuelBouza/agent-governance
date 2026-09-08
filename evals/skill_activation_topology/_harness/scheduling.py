"""Deterministic RIQ-NBC scheduling for the T023 v15 epoch."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .models import REPO_ROOT, FrozenInputs, HarnessError, TrialSpec


def ordered_cases(inputs: FrozenInputs) -> list[dict[str, Any]]:
    order = inputs.oracle["scheduling"]["case_group_order"]
    return sorted(inputs.corpus["cases"], key=lambda case: (order.index(case["class"]), case["id"]))


def _schedule(
    inputs: FrozenInputs,
    candidates: Iterable[str],
    repetitions: Iterable[int],
) -> list[TrialSpec]:
    candidates = list(candidates)
    repetitions = list(repetitions)
    expected_order = inputs.oracle["scheduling"]["candidate_round_robin_order"]
    if candidates != expected_order:
        raise HarnessError("v15 base scheduling requires exact B2/F2/G3 order")
    schedule: list[TrialSpec] = []
    for repetition in repetitions:
        for case in ordered_cases(inputs):
            schedule.extend(TrialSpec(case, candidate, repetition) for candidate in candidates)
    return schedule


def stage_schedule(inputs: FrozenInputs, stage: str) -> list[TrialSpec]:
    """Compatibility entrypoint for the single v15 acceptance base stage."""
    if stage not in {"A", "BASE"}:
        raise HarnessError("v15 has one independent acceptance stage; R/C stages are obsolete")
    return scheduled_trials(inputs)


def expected_load_path(inputs: FrozenInputs, spec: TrialSpec) -> tuple[list[str], int]:
    expected = set(spec.case["expected_capabilities"])
    load_order = inputs.manifest["candidates"][spec.candidate_id]["load_order"]
    paths = [inputs.manifest["shared_references"][cap] for cap in load_order if cap in expected]
    return paths, sum((REPO_ROOT / path).stat().st_size for path in paths)


def scheduled_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    """Return the 420 mandatory v15 base observations: all r1, then all r2."""
    method = inputs.oracle["trial_method"]
    repetitions = range(1, method["base_valid_repetitions_per_case_candidate"] + 1)
    return _schedule(inputs, inputs.oracle["candidate_ids"], repetitions)


def all_possible_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    """Return the complete v15 identity set including pair-scoped r3 observations."""
    maximum = inputs.oracle["trial_method"]["max_valid_repetitions_per_case_candidate"]
    return _schedule(inputs, inputs.oracle["candidate_ids"], range(1, maximum + 1))


def validate_repetition(inputs: FrozenInputs, spec: TrialSpec) -> None:
    maximum = inputs.oracle["trial_method"]["max_valid_repetitions_per_case_candidate"]
    if spec.repetition < 1 or spec.repetition > maximum:
        raise HarnessError(f"{spec.key}: repetition is outside the frozen v15 identity set")


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


def _trial_prompt(inputs: FrozenInputs, case: dict[str, Any]) -> str:
    return f"{case['prompt']}\n\n{inputs.envelope['user_suffix']}"
