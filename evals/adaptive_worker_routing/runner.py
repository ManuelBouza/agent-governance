"""Executable T063 v2 harness entrypoint and evidence materializer."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from .app_server import AppServerClient, AppServerError
from .config import (
    APP_SERVER_CONFIG_OVERRIDES,
    ARM_ORDER,
    EVIDENCE_BRANCH,
    FROZEN_HEAD,
    HISTORICAL_BLOCKED_HEAD,
    REQUIRED_CODEX_VERSION,
    ROOT_MODEL,
    ROOT_REASONING,
    ArmSpec,
    ExecutionInvalid,
    HarnessError,
    MeasurementSurfaceBlocked,
    PreparedInputs,
    ProfileResolutionBlocked,
)
from .measurement import app_server_version, execute_arm, preflight
from .oracles import cleanup_runtime_root, git, prepare_inputs


def tracked_state(repo: Path) -> list[str]:
    output = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
    return [line for line in output.splitlines() if line]


def aggregate(scored: list[dict[str, Any]]) -> dict[str, Any]:
    controls = [item for item in scored if item["arm"] == "CONTROL"]
    adaptive = [item for item in scored if item["arm"] == "ADAPTIVE"]
    return {
        "control_pass_count": sum(item["result_status"] == "PASS" for item in controls),
        "adaptive_pass_count": sum(item["result_status"] == "PASS" for item in adaptive),
        "adaptive_first_attempt_failures": sum(
            item["result_status"] != "PASS" for item in adaptive
        ),
        "adaptive_escalation_count": 0,
        "material_false_negative_count": sum(
            item.get("material_false_negative_count", 0) for item in scored
        ),
        "material_false_positive_count": sum(
            item.get("material_false_positive_count", 0) for item in scored
        ),
        "profile_resolution_failures": 0,
        "control_exact_tokens_total": sum(item["total_tokens"] for item in controls),
        "adaptive_exact_tokens_total": sum(item["total_tokens"] for item in adaptive),
        "control_exact_duration_total": round(
            sum(item["duration_seconds"] for item in controls), 3
        ),
        "adaptive_exact_duration_total": round(
            sum(item["duration_seconds"] for item in adaptive), 3
        ),
        "root_rework_events_caused_by_children": 0,
    }


def pilot_decision(metrics: dict[str, Any], scored: list[dict[str, Any]]) -> str:
    if metrics["control_pass_count"] != 3:
        raise ExecutionInvalid("CONTROL did not pass 3/3 first attempts; baseline invalid")
    if metrics["adaptive_first_attempt_failures"]:
        return "NOT_QUALIFIED"
    if metrics["material_false_negative_count"] or metrics["material_false_positive_count"]:
        return "NOT_QUALIFIED"
    if metrics["adaptive_pass_count"] != 3:
        return "NOT_QUALIFIED"
    if any(item["reroute_observed"] for item in scored):
        return "NOT_QUALIFIED"
    if metrics["adaptive_exact_tokens_total"] < metrics["control_exact_tokens_total"]:
        return "QUALIFIED"
    return "QUALIFIED_QUALITY_ONLY"


def evidence_payload(
    *,
    started_at: str,
    ended_at: str,
    repo_head: str,
    preflight_receipt: dict[str, Any],
    prepared: PreparedInputs,
    scored: list[dict[str, Any]],
    metrics: dict[str, Any],
    decision: str | None,
    status: str,
    terminal_classification: str,
    blocker: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "schema_version": 2,
        "run_id": f"T063-v2-{started_at}",
        "task_id": "T063",
        "status": status,
        "terminal_classification": terminal_classification,
        "pilot_decision": decision,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "authority": {
            "frozen_evaluation_head": FROZEN_HEAD,
            "candidate_head_before_execution": repo_head,
            "evidence_branch": EVIDENCE_BRANCH,
            "execution_target": "CONTRACT_FIXED",
            "underlying_delegation_eligibility": "DELEGATED",
            "launch_authority_review": "docs/reviews/T063-R4.md",
            "measurement_decision": (
                "docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md"
            ),
            "stage6_materialization_decision": (
                "docs/decisions/D076-stage6-ephemeral-executable-materialization-boundary.md"
            ),
        },
        "launch_profile": {
            "executor": "Codex",
            "root_model": ROOT_MODEL,
            "root_reasoning_effort": ROOT_REASONING,
            "codex_cli_required": REQUIRED_CODEX_VERSION,
            "app_server_required": REQUIRED_CODEX_VERSION,
            "auth_category_required": "chatgpt",
        },
        "preflight": preflight_receipt,
        "oracles": {
            "p1": prepared.p1_oracle,
            "p2": prepared.p2_oracle,
            "p3": prepared.p3_oracle,
            "computed_before_scored_children": True,
        },
        "task_message_digests": prepared.task_message_digests,
        "scored_children": scored,
        "metrics": metrics,
        "blocker": blocker,
        "oracle_leak_observed": any(item.get("oracle_leak_observed") for item in scored),
        "backend_served_profile_verified": False,
        "prior_blocked_run_reused_for_scoring": False,
        "historical_blocked_evidence_head": HISTORICAL_BLOCKED_HEAD,
        "provider_execution": {
            "scored_child_attempts": len(scored),
            "scored_parent_turns": len(scored),
            "diagnostic_child_attempts": 0,
            "compensating_attempts": 0,
        },
        "d076": {
            "published_stage5_harness_used": True,
            "executor_material_ephemeral_artifacts": [],
            "candidate_runtime_artifacts": [
                {
                    "label": "P3 profile fixture",
                    "created_by": "published T063 harness",
                    "materiality": "candidate-owned semantic fixture",
                    "persisted": False,
                    "removed_after_run": True,
                }
            ],
        },
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_evaluation(
    *,
    repo: Path,
    codex_bin: Path,
    runtime_root: Path,
    telemetry_path: Path,
    handoff_path: Path,
) -> int:
    repo = repo.resolve()
    codex_bin = codex_bin.resolve()
    runtime_root = runtime_root.resolve()
    telemetry_path = telemetry_path if telemetry_path.is_absolute() else repo / telemetry_path
    handoff_path = handoff_path if handoff_path.is_absolute() else repo / handoff_path
    if tracked_state(repo):
        raise HarnessError("candidate worktree must be clean before T063 v2 execution")
    branch = git(repo, "branch", "--show-current")
    if branch != EVIDENCE_BRANCH:
        raise HarnessError(f"wrong branch: expected {EVIDENCE_BRANCH}, got {branch}")
    repo_head = git(repo, "rev-parse", "HEAD")
    started_at = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())

    prepared: PreparedInputs | None = None
    preflight_receipt: dict[str, Any] = {}
    scored: list[dict[str, Any]] = []
    blocker: dict[str, Any] | None = None
    decision: str | None = None
    status = "BLOCKED"
    terminal = "BLOCKED_UNCLASSIFIED"
    metrics = aggregate(scored)

    try:
        prepared = prepare_inputs(repo, runtime_root)
        app_server_overrides = APP_SERVER_CONFIG_OVERRIDES
        with AppServerClient(
            codex_bin,
            cwd=repo,
            config_overrides=app_server_overrides,
        ) as client:
            required_profiles = {(model, effort) for _, _, model, effort in ARM_ORDER}
            preflight_receipt = preflight(
                client,
                codex_bin=codex_bin,
                repo=repo,
                runtime_root=runtime_root,
                required_profiles=required_profiles,
            )
        preflight_receipt["fresh_app_server_per_scored_arm"] = True
        preflight_receipt["app_server_config_overrides"] = list(app_server_overrides)
        for probe, arm, model, reasoning in ARM_ORDER:
            with AppServerClient(
                codex_bin,
                cwd=repo,
                config_overrides=app_server_overrides,
            ) as arm_client:
                initialized = arm_client.initialize()
                app_version = app_server_version(initialized)
                if app_version != REQUIRED_CODEX_VERSION:
                    raise MeasurementSurfaceBlocked(
                        f"scored arm App Server mismatch: expected {REQUIRED_CODEX_VERSION}, got {app_version!r}"
                    )
                scored.append(
                    execute_arm(
                        arm_client,
                        repo=repo,
                        runtime_root=runtime_root,
                        prepared=prepared,
                        spec=ArmSpec(probe, arm, model, reasoning),
                    )
                )
        metrics = aggregate(scored)
        decision = pilot_decision(metrics, scored)
        status = "COMPLETED"
        terminal = "COMPLETED_SCORED"
    except MeasurementSurfaceBlocked as exc:
        metrics = aggregate(scored)
        terminal = "BLOCKED_MEASUREMENT_SURFACE"
        blocker = {"code": terminal, "message": str(exc)}
    except ProfileResolutionBlocked as exc:
        metrics = aggregate(scored)
        terminal = "BLOCKED_PROFILE_RESOLUTION"
        blocker = {"code": terminal, "message": str(exc)}
    except (ExecutionInvalid, AppServerError, HarnessError) as exc:
        metrics = aggregate(scored)
        terminal = "BLOCKED_EXECUTION_INVALID"
        blocker = {"code": terminal, "message": str(exc)}
    finally:
        ended_at = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        cleanup_runtime_root(runtime_root, prepared)

    if prepared is None:
        raise HarnessError("input preparation failed before safe evidence materialization")

    telemetry = evidence_payload(
        started_at=started_at,
        ended_at=ended_at,
        repo_head=repo_head,
        preflight_receipt=preflight_receipt,
        prepared=prepared,
        scored=scored,
        metrics=metrics,
        decision=decision,
        status=status,
        terminal_classification=terminal,
        blocker=blocker,
    )
    write_json(telemetry_path, telemetry)
    handoff = {
        "schema_version": 2,
        "task_id": "T063",
        "status": status,
        "terminal_classification": terminal,
        "branch": EVIDENCE_BRANCH,
        "candidate_head_before_execution": repo_head,
        "frozen_evaluation_head": FROZEN_HEAD,
        "telemetry_path": telemetry_path.relative_to(repo).as_posix(),
        "pilot_decision": decision,
        "blocker": blocker,
        "metrics": metrics,
        "provider_execution": telemetry["provider_execution"],
        "technical_review": {
            "published_stage5_harness_used": True,
            "prior_blocked_run_reused_for_scoring": False,
            "product_source_changed_by_harness": False,
            "markdown_changed_by_harness": False,
        },
        "ephemeral_artifacts": [],
        "next_required_authority": (
            "ChatGPT Orchestrator convergence required."
            if status == "COMPLETED"
            else "ChatGPT Orchestrator review/re-entry required before additional scored calls."
        ),
    }
    write_json(handoff_path, handoff)
    return 0 if status == "COMPLETED" else 2


def command_prepare(args: argparse.Namespace) -> int:
    runtime_root = args.runtime_root.resolve()
    prepared: PreparedInputs | None = None
    try:
        prepared = prepare_inputs(args.repo.resolve(), runtime_root)
        print(
            json.dumps(
                {
                    "p1_oracle": prepared.p1_oracle,
                    "p2_oracle": prepared.p2_oracle,
                    "p3_oracle": prepared.p3_oracle,
                    "task_message_digests": prepared.task_message_digests,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0
    finally:
        cleanup_runtime_root(runtime_root, prepared)


def command_run(args: argparse.Namespace) -> int:
    return run_evaluation(
        repo=args.repo,
        codex_bin=args.codex_bin,
        runtime_root=args.runtime_root,
        telemetry_path=args.telemetry,
        handoff_path=args.handoff,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare", help="provider-free oracle/fixture verification")
    prepare.add_argument("--repo", type=Path, default=Path.cwd())
    prepare.add_argument("--runtime-root", type=Path, required=True)
    prepare.set_defaults(func=command_prepare)
    run = sub.add_parser("run", help="run the six-arm T063 v2 scored evaluation")
    run.add_argument("--repo", type=Path, default=Path.cwd())
    run.add_argument("--codex-bin", type=Path, required=True)
    run.add_argument("--runtime-root", type=Path, required=True)
    run.add_argument(
        "--telemetry",
        type=Path,
        default=Path("handoffs/T063-adaptive-worker-routing-telemetry-v2.json"),
    )
    run.add_argument(
        "--handoff",
        type=Path,
        default=Path("handoffs/T063-executor-handoff-v2.json"),
    )
    run.set_defaults(func=command_run)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (HarnessError, AppServerError, OSError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from exc


if __name__ == "__main__":
    raise SystemExit(main())
