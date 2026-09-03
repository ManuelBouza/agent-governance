"""Execution scheduling and evidence state for the MG1 topology harness."""

from __future__ import annotations

import concurrent.futures
from collections import Counter
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .aggregation import (
    conditional_third_specs,
    materiality_futility_certificate,
    qualification_futility_certificate,
)
from .frozen_inputs import _load_json
from .models import (
    V10_CLASS_ORDER,
    CapacityPause,
    FrozenInputs,
    HarnessError,
    HostSurfaceDrift,
    TrialSpec,
)
from .scheduling import all_possible_trials
from .storage import _json_dump, _jsonl_dump

Observation = tuple[dict[str, Any], dict[str, Any]]
ExecuteObservation = Callable[..., Observation | None]


@dataclass
class RunContext:
    inputs: FrozenInputs
    args: Any
    output: Path
    workspace_parent: Path
    metadata: dict[str, Any]
    execute_observation: ExecuteObservation

    def execute(self, spec: TrialSpec) -> Observation | None:
        return self.execute_observation(
            self.inputs,
            spec,
            output=self.output,
            codex_command=self.args.codex_command,
            model=self.args.model,
            effort=self.args.effort,
            timeout_seconds=self.args.timeout_seconds,
            workspace_parent=self.workspace_parent,
            backend=self.metadata.get("selected_backend", "elevated"),
            sandbox=self.metadata.get("selected_sandbox", "read-only"),
        )

    def persisted_results(self) -> dict[str, Observation]:
        values: dict[str, Observation] = {}
        for path in sorted((self.output / "attempts").glob("*.json")):
            item = _load_json(path)
            if item["status"] != "VALID":
                continue
            if item["trial_key"] in values:
                raise HarnessError(f"{item['trial_key']}: duplicate valid attempt")
            values[item["trial_key"]] = (item["structured"], item["raw"])
        return values

    def trials(self) -> list[dict[str, Any]]:
        return [value[0] for value in self.persisted_results().values()]

    def export_evidence(
        self, stage_state: str, status: str, blocked: list[str] | None = None
    ) -> None:
        results = self.persisted_results()
        specs = {spec.key: spec for spec in all_possible_trials(self.inputs)}
        ordered = [key for key in specs if key in results]
        _jsonl_dump(self.output / "trials.jsonl", (results[key][0] for key in ordered))
        _jsonl_dump(self.output / "raw-trials.jsonl", (results[key][1] for key in ordered))
        attempts = [_load_json(path) for path in sorted((self.output / "attempts").glob("*.json"))]
        capacity = [
            _load_json(path) for path in sorted((self.output / "capacity-events").glob("*.json"))
        ]
        _jsonl_dump(self.output / "attempts.jsonl", attempts)
        _jsonl_dump(
            self.output / "failed-attempts.jsonl",
            [item for item in attempts if item["status"] == "FAILED"],
        )
        _jsonl_dump(self.output / "capacity-events.jsonl", capacity)
        self._write_completion(stage_state, status, blocked, attempts, capacity, len(results))

    def _write_completion(
        self,
        stage_state: str,
        status: str,
        blocked: list[str] | None,
        attempts: list[dict[str, Any]],
        capacity: list[dict[str, Any]],
        completed: int,
    ) -> None:
        self.metadata.update(
            status=status,
            stage_state=stage_state,
            completed_valid_observations=completed,
            capacity_event_count=len(capacity),
            updated_at=datetime.now(UTC).isoformat(),
        )
        _json_dump(self.output / "run-metadata.json", self.metadata)
        _json_dump(
            self.output / "completeness.json",
            {
                "execution_epoch": self.inputs.oracle["execution_epoch"],
                "stage_state": stage_state,
                "completed_valid_observations": completed,
                "exhausted_observations": blocked or [],
                "capacity_event_count": len(capacity),
                "acceptance_complete": status in {"COMPLETE", "BLOCKED_NO_REFERENCE"},
                "partial_scoring_permitted": False,
            },
        )
        _json_dump(
            self.output / "retry-diagnostics.json",
            {
                candidate: self._retry_diagnostic(candidate, attempts, capacity)
                for candidate in self.inputs.oracle["candidate_ids"]
            },
        )

    @staticmethod
    def _retry_diagnostic(
        candidate: str, attempts: list[dict[str, Any]], capacity: list[dict[str, Any]]
    ) -> dict[str, Any]:
        return {
            "model_attempts": sum(item["candidate_id"] == candidate for item in attempts),
            "non_capacity_failures": sum(
                item["candidate_id"] == candidate and item["status"] == "FAILED"
                for item in attempts
            ),
            "capacity_events": sum(item["candidate_id"] == candidate for item in capacity),
            "failure_classes": dict(
                Counter(
                    item["failure_class"]
                    for item in attempts
                    if item["candidate_id"] == candidate and item["status"] == "FAILED"
                )
            ),
        }

    def _submit_available(
        self,
        executor: concurrent.futures.ThreadPoolExecutor,
        futures: dict[concurrent.futures.Future, TrialSpec],
        pending: Iterator[TrialSpec],
    ) -> None:
        for _ in range(self.args.workers - len(futures)):
            spec = next(pending, None)
            if spec is not None:
                futures[executor.submit(self.execute, spec)] = spec

    @staticmethod
    def _record_future(
        future: concurrent.futures.Future,
        spec: TrialSpec,
        completed: set[str],
        blocked: list[str],
        host_drift: list[str],
    ) -> bool:
        try:
            result = future.result()
        except CapacityPause:
            return True
        except HostSurfaceDrift:
            host_drift.append(spec.key)
        else:
            if result is None:
                blocked.append(spec.key)
            else:
                completed.add(spec.key)
                print(f"completed {len(completed)} {spec.key}", flush=True)
        return False

    def execute_schedule(self, schedule: list[TrialSpec]) -> tuple[list[str], bool, list[str]]:
        completed = set(self.persisted_results())
        pending = iter([spec for spec in schedule if spec.key not in completed])
        blocked: list[str] = []
        host_drift: list[str] = []
        capacity_pause = False
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.args.workers) as executor:
            futures: dict[concurrent.futures.Future, TrialSpec] = {}
            self._submit_available(executor, futures, pending)
            while futures:
                done, _ = concurrent.futures.wait(
                    futures, return_when=concurrent.futures.FIRST_COMPLETED
                )
                for future in done:
                    spec = futures.pop(future)
                    capacity_pause |= self._record_future(
                        future, spec, completed, blocked, host_drift
                    )
                if not blocked and not capacity_pause and not host_drift:
                    self._submit_available(executor, futures, pending)
        return blocked, capacity_pause, host_drift

    def stop_for_execution_state(
        self, blocked: list[str], capacity: bool, host_drift: list[str], state: str
    ) -> int | None:
        if host_drift:
            self.export_evidence("HOST_SURFACE_DRIFT", "BLOCKED", host_drift)
            self._write_selection("BLOCKED", "HOST_SURFACE_DRIFT")
            return 1
        if capacity:
            self.export_evidence(state, "PAUSED_EXTERNAL_CAPACITY", blocked)
            self._write_selection("PAUSED_EXTERNAL_CAPACITY")
            return 2
        if blocked:
            self.export_evidence(state, "BLOCKED", blocked)
            self._write_selection(
                "BLOCKED", "scheduled observation exhausted two non-capacity model attempts"
            )
            return 1
        return None

    def _write_selection(self, status: str, reason: str | None = None) -> None:
        value = {"status": status, "selected_candidate": None, "scored": False}
        if reason is not None:
            value["reason"] = reason
        _json_dump(self.output / "selection.json", value)

    def _store_certificate(self, candidate: str, certificate: dict[str, Any]) -> None:
        self.terminal_candidates[candidate] = certificate
        _json_dump(self.output / "futility-certificates" / f"{candidate}.json", certificate)

    terminal_candidates: dict[str, dict[str, Any]] | None = None

    def _base_pair(self, stage: str, case: dict[str, Any], candidate: str) -> int | None:
        for repetition in (1, 2):
            spec = TrialSpec(case, candidate, repetition)
            stopped = self.stop_for_execution_state(
                *self.execute_schedule([spec]),
                f"{stage}_{case['id']}_{candidate}_INCOMPLETE",
            )
            if stopped is not None:
                return stopped
            certificate = qualification_futility_certificate(self.inputs, candidate, self.trials())
            if certificate["terminal"]:
                self._store_certificate(candidate, certificate)
                break
        return None

    def _conditional_third(self, stage: str, case: dict[str, Any], candidate: str) -> int | None:
        thirds = [
            spec
            for spec in conditional_third_specs(self.inputs, [candidate], self.trials())
            if spec.case["id"] == case["id"]
        ]
        if not thirds:
            return None
        return self.stop_for_execution_state(
            *self.execute_schedule(thirds),
            f"{stage}_{case['id']}_{candidate}_THIRD_INCOMPLETE",
        )

    def _finalize_candidate(self, candidate: str, reference_metrics: dict[str, Any] | None) -> None:
        certificate = qualification_futility_certificate(self.inputs, candidate, self.trials())
        if not certificate["terminal"] and reference_metrics is not None:
            certificate = materiality_futility_certificate(
                self.inputs, candidate, self.trials(), reference_metrics
            )
        if certificate["terminal"]:
            self._store_certificate(candidate, certificate)

    def _candidate_case(
        self,
        stage: str,
        case: dict[str, Any],
        candidate: str,
        reference_metrics: dict[str, Any] | None,
    ) -> int | None:
        if candidate in self.terminal_candidates:
            return None
        stopped = self._base_pair(stage, case, candidate)
        if stopped is not None or candidate in self.terminal_candidates:
            return stopped
        stopped = self._conditional_third(stage, case, candidate)
        if stopped is not None:
            return stopped
        self._finalize_candidate(candidate, reference_metrics)
        return None

    def adaptive_stage(
        self, stage: str, candidates: list[str], reference_metrics: dict[str, Any] | None = None
    ) -> int | None:
        ordered_cases = sorted(
            self.inputs.corpus["cases"],
            key=lambda case: (V10_CLASS_ORDER.index(case["class"]), case["id"]),
        )
        for case_index, case in enumerate(ordered_cases):
            offset = case_index % len(candidates)
            for candidate in candidates[offset:] + candidates[:offset]:
                stopped = self._candidate_case(stage, case, candidate, reference_metrics)
                if stopped is not None:
                    return stopped
        return None

    def __post_init__(self) -> None:
        if self.terminal_candidates is None:
            self.terminal_candidates = {}
