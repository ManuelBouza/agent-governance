"""Frozen v16 observation scheduling and attempt accounting."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .models import CANDIDATES, HarnessError

@dataclass(frozen=True)
class ScheduledObservation:
    phase: str
    case_id: str
    candidate_id: str
    repetition: str
    @property
    def key(self) -> str:
        return f"{self.phase}:{self.case_id}:{self.candidate_id}:{self.repetition}"

def routing_first_schedule(corpus: dict[str, Any]) -> list[ScheduledObservation]:
    return [ScheduledObservation("routing", case["id"], candidate, "r1") for case in corpus["routing_cases"] for candidate in CANDIDATES]

def reliability_schedule(corpus: dict[str, Any], oracle: dict[str, Any]) -> list[ScheduledObservation]:
    allowed = {case["id"] for case in corpus["routing_cases"]}
    subset = oracle["reliability_subset_case_ids"]
    if len(subset) != 30 or len(set(subset)) != 30 or not set(subset) <= allowed:
        raise HarnessError("invalid frozen reliability subset")
    return [ScheduledObservation("reliability", case_id, candidate, "r2") for case_id in subset for candidate in CANDIDATES]

def e2e_schedule(corpus: dict[str, Any], finalists: list[str]) -> list[ScheduledObservation]:
    if not 1 <= len(finalists) <= 2 or len(set(finalists)) != len(finalists):
        raise HarnessError("end-to-end requires one or two unique finalists")
    if set(finalists) - set(CANDIDATES):
        raise HarnessError("unknown finalist")
    return [ScheduledObservation("e2e", case["id"], candidate, "r1") for case in corpus["e2e_reserve"] for candidate in finalists]

class AttemptBudget:
    def __init__(self, plan: dict[str, Any], already_used: int = 0):
        self.spec = plan["attempt_budget"]
        self.used = already_used
    @property
    def ceiling(self) -> int:
        return int(self.spec["absolute_stage6_provider_model_attempt_ceiling"])
    def consume(self, count: int = 1) -> None:
        if count < 0 or self.used + count > self.ceiling:
            raise HarnessError("absolute provider/model attempt ceiling would be exceeded")
        self.used += count
    def max_attempts_for(self, phase: str) -> int:
        if phase in {"routing", "reliability", "e2e"}:
            return int(self.spec["max_attempts_per_scientific_observation"])
        if phase == "preflight":
            return int(self.spec["behavioral_preflight_max_attempts"])
        if phase == "canary":
            return int(self.spec["synthetic_canary_max_attempts"])
        raise HarnessError(f"unknown attempt phase: {phase}")
