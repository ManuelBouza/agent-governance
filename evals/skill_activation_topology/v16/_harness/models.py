"""Core models and frozen paths for T023 v16 selective routing."""
from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
V16_ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_PATH = V16_ROOT / "analysis-plan.json"
ROUTING_PATH = V16_ROOT / "capability-routing.json"
CANDIDATE_HASHES_PATH = V16_ROOT / "candidate-hashes.json"
TOPOLOGIES_PATH = V16_ROOT / "topologies.json"
PRESENTATION_MANIFEST_PATH = V16_ROOT / "presentation-manifest.json"
DEVELOPMENT_PATH = V16_ROOT / "development.json"
CORPUS_PATH = V16_ROOT / "corpus.json"
ORACLE_PATH = V16_ROOT / "oracle.json"
ENVELOPE_PATH = V16_ROOT / "trial-envelope.json"
CAPABILITIES = ("consumer-lifecycle", "source-maintainer", "external-skill-trust")
CANDIDATES = ("B2", "F2", "G3")
DISPOSITIONS = ("ROUTE", "NONE", "ABSTAIN")

class HarnessError(RuntimeError):
    """Fail-closed v16 harness error."""

def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise HarnessError(f"{path} must contain a JSON object")
    return value

@dataclass(frozen=True)
class RoutingTruth:
    case_id: str
    disposition: str
    capabilities: frozenset[str] | None
    admissible_capability_sets: tuple[frozenset[str], ...] = ()
    critical_permission_boundary: bool = False
    expected_semantic_outcome: str | None = None

@dataclass(frozen=True)
class RoutingObservation:
    case_id: str
    candidate_id: str
    repetition: str
    observed_disposition: str
    observed_activation_set: frozenset[str]
    observed_capability_set: frozenset[str]
    clarification_requested: bool
    critical_permission_violation: bool
    context_bytes: int
    latency_seconds: float
    provider_usage: dict[str, Any]
    technical_valid: bool
    phase: str = "routing"
    task_success: bool | None = None
    semantic_outcome: str | None = None
