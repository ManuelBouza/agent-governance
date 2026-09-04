"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from .models import REPO_ROOT, V12_CLASS_ORDER, FrozenInputs, HarnessError, TrialSpec


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
        key=lambda case: (V12_CLASS_ORDER.index(case["class"]), case["id"]),
    )
    for case_index, case in enumerate(ordered_cases):
        for repetition in repetitions:
            offset = (case_index + repetition - 1) % len(candidates)
            rotated = candidates[offset:] + candidates[:offset]
            schedule.extend(TrialSpec(case, candidate, repetition) for candidate in rotated)
    return schedule


def expected_load_path(inputs: FrozenInputs, spec: TrialSpec) -> tuple[list[str], int]:
    expected = set(spec.case["expected_capabilities"])
    load_order = inputs.manifest["candidates"][spec.candidate_id]["load_order"]
    paths = [inputs.manifest["shared_references"][cap] for cap in load_order if cap in expected]
    return paths, sum((REPO_ROOT / path).stat().st_size for path in paths)


def scheduled_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    """Return the V12 full-completion two-repetition ceiling for all candidates.

    Conditional third repetitions are deliberately absent.  They are derived only
    after both valid paired observations exist for a case/candidate identity.
    """
    candidates = inputs.oracle["candidate_ids"]
    repetitions = inputs.oracle["trial_method"]["base_valid_repetitions_per_case_candidate"]
    return _schedule(inputs, candidates, range(1, repetitions + 1))


def all_possible_trials(inputs: FrozenInputs) -> list[TrialSpec]:
    """Return all V12 identities, including conditional repetition three."""
    maximum = inputs.oracle["trial_method"]["max_valid_repetitions_per_case_candidate"]
    return _schedule(inputs, inputs.oracle["candidate_ids"], range(1, maximum + 1))


def validate_repetition(inputs: FrozenInputs, spec: TrialSpec) -> None:
    maximum = inputs.oracle["trial_method"]["max_valid_repetitions_per_case_candidate"]
    if spec.repetition < 1 or spec.repetition > maximum:
        raise HarnessError(f"{spec.key}: repetition is outside the frozen identity set")


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
