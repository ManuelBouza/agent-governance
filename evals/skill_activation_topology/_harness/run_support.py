"""Execution state and sequential schedule support for the T023 v15 harness."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .frozen_inputs import _load_json
from .models import CapacityPause, FrozenInputs, HarnessError, HostSurfaceDrift, TrialSpec
from .scheduling import all_possible_trials, validate_repetition
from .storage import _json_dump, _jsonl_dump

Observation = tuple[dict[str, Any], dict[str, Any]]


@dataclass
class RunContext:
    inputs: FrozenInputs
    args: Any
    output: Path
    workspace_parent: Path
    metadata: dict[str, Any]
    execute_observation: Any

    def execute(self, spec: TrialSpec) -> Observation | None:
        validate_repetition(self.inputs, spec)
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
        method = self.inputs.oracle["trial_method"]
        self.metadata.update(
            status=status,
            stage_state=stage_state,
            completed_valid_observations=completed,
            acceptance_model_attempts=len(attempts),
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
                "acceptance_model_attempts": len(attempts),
                "acceptance_model_attempt_ceiling": method["maximum_acceptance_model_attempts"],
                "capacity_event_count": len(capacity),
                "acceptance_complete": status == "COMPLETE",
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

    def execute_schedule(self, schedule: list[TrialSpec]) -> tuple[list[str], bool, list[str]]:
        """Execute in exact frozen order; full acceptance is intentionally single-threaded."""
        completed = set(self.persisted_results())
        blocked: list[str] = []
        host_drift: list[str] = []
        capacity_pause = False
        for spec in schedule:
            if spec.key in completed:
                continue
            try:
                result = self.execute(spec)
            except CapacityPause:
                capacity_pause = True
                break
            except HostSurfaceDrift:
                host_drift.append(spec.key)
                break
            if result is None:
                blocked.append(spec.key)
                break
            completed.add(spec.key)
            print(f"completed {len(completed)} {spec.key}", flush=True)
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
