"""Technical runner and scorer for the frozen MG1 T023 topology oracle.

The semantic corpus, candidate presentations, metric definitions, and thresholds
remain owned by the checked-in JSON/Markdown oracle assets. This facade delegates
materialization, host execution, evidence, and scoring to cohesive implementation
modules.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

# Direct script execution exposes this directory, while importlib-based compatibility
# loading does not. Implementation imports therefore intentionally follow the bootstrap.
# Re-exported names are the legacy facade surface consumed by deterministic tests/tools.
# ruff: noqa: E402, F401
_FACADE_DIR = Path(__file__).resolve().parent
if str(_FACADE_DIR) not in sys.path:
    sys.path.insert(0, str(_FACADE_DIR))

from _harness import cli as _cli
from _harness import evidence as _evidence
from _harness import host_preflight as _host_preflight
from _harness import runner as _runner
from _harness.aggregation import (
    _critical_violation,
    _decision_signature,
    _majority_scalar,
    _majority_set,
    _p95,
    _safe_ratio,
    aggregate_candidate_trials,
    candidate_has_critical_violation,
    conditional_third_specs,
    disagreement_fields,
    finalized_candidate_aggregates,
    materiality_futility_certificate,
    qualification_futility_certificate,
)
from _harness.codex_adapter import (
    _backend_probe,
    _codex_version,
    _host_command,
    _is_explicit_capacity_event,
)
from _harness.evidence import _validate_partial, build_deterministic_evidence
from _harness.frozen_inputs import _load_json, _sha256, load_frozen_inputs, validate_frozen_inputs
from _harness.host_preflight import _workspace_access_probe, run_canary
from _harness.materialization import (
    _acl_diagnostic,
    _copy_record,
    _inherited_acl_workspace,
    _is_relative_to,
    _validate_fixture_evidence,
    _validate_workspace_root,
    materialize_candidate,
    materialize_fixture,
)
from _harness.models import (
    ACTIVATION_RELEVANT_CLASSES,
    ALLOWED_OUTCOMES,
    BACKEND_PROBE_NONCE,
    CANARY_NONCE,
    CANARY_SCHEMA,
    CORPUS_PATH,
    ENVELOPE_PATH,
    HERE,
    MANIFEST_PATH,
    MINIMAL_DISABLED_FEATURES,
    NEGATIVE_CLASSES,
    ORACLE_PATH,
    REPO_ROOT,
    REQUIRED_CODEX_VERSION,
    TOPOLOGIES_PATH,
    TRIAL_SCHEMA,
    V10_CLASS_ORDER,
    WINDOWS_BACKEND_ORDER,
    WORKSPACE_FACTORY_ID,
    WORKSPACE_PROBE_FILENAME,
    WORKSPACE_PROBE_NONCE,
    AttemptFailure,
    CapacityPause,
    FrozenInputs,
    HarnessError,
    HostSurfaceDrift,
    TrialSpec,
)
from _harness.observability import (
    _observed_skill_reads,
    _successful_body_read,
    _surface_drift,
    _trace_telemetry,
    _validate_model_result,
)
from _harness.provenance import (
    _validate_executed_runner_provenance,
    load_trials,
    score_matrix,
    validate_complete_evidence,
    verify_deterministic,
)
from _harness.scheduling import (
    _schedule,
    _trial_prompt,
    all_possible_trials,
    expected_entrypoints,
    expected_load_path,
    scheduled_trials,
    stage_schedule,
)
from _harness.scoring import (
    apply_selection_rule,
    candidate_qualifies,
    compute_candidate_metrics,
    select_from_cost_bounded_metrics,
    select_single_family_reference,
)
from _harness.storage import _json_dump, _jsonl_dump, _read_partial
from _harness.trial_execution import run_trial


def execute_logical_observation(
    inputs: FrozenInputs, spec: TrialSpec, *, output: Path, **kwargs: Any
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    _evidence.run_trial = globals()["run_trial"]
    return _evidence.execute_logical_observation(inputs, spec, output=output, **kwargs)


def run_host_preflight(
    inputs: FrozenInputs, args: Any, output: Path, workspace_parent: Path
) -> dict[str, Any]:
    _host_preflight._backend_probe = globals()["_backend_probe"]
    _host_preflight._workspace_access_probe = globals()["_workspace_access_probe"]
    _host_preflight.run_canary = globals()["run_canary"]
    _host_preflight._codex_version = globals()["_codex_version"]
    return _host_preflight.run_host_preflight(inputs, args, output, workspace_parent)


def run_matrix(args: Any) -> int:
    _runner._codex_version = globals()["_codex_version"]
    _runner.run_host_preflight = globals()["run_host_preflight"]
    _runner.build_deterministic_evidence = globals()["build_deterministic_evidence"]
    _runner.verify_deterministic = globals()["verify_deterministic"]
    _runner.execute_logical_observation = globals()["execute_logical_observation"]
    return _runner.run_matrix(args)


def validate_execution_config(inputs: FrozenInputs, args: argparse.Namespace) -> None:
    _runner._codex_version = globals()["_codex_version"]
    _runner.validate_execution_config(inputs, args)


def command_validate(args: Any) -> int:
    original = _cli.load_frozen_inputs
    try:
        _cli.load_frozen_inputs = globals()["load_frozen_inputs"]
        return _cli.command_validate(args)
    finally:
        _cli.load_frozen_inputs = original


def command_materialize(args: Any) -> int:
    original_load = _cli.load_frozen_inputs
    original_materialize = _cli.materialize_candidate
    try:
        _cli.load_frozen_inputs = globals()["load_frozen_inputs"]
        _cli.materialize_candidate = globals()["materialize_candidate"]
        return _cli.command_materialize(args)
    finally:
        _cli.load_frozen_inputs = original_load
        _cli.materialize_candidate = original_materialize


def build_parser() -> argparse.ArgumentParser:
    parser = _cli.build_parser()
    parser.description = __doc__
    subparsers = next(
        action for action in parser._actions if isinstance(action, argparse._SubParsersAction)
    )
    functions = {
        "validate": command_validate,
        "materialize": command_materialize,
        "run": run_matrix,
        "score": score_matrix,
        "verify": verify_deterministic,
    }
    for command, function in functions.items():
        subparsers.choices[command].set_defaults(func=function)
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
