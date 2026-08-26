"""Preserve an incomplete T023 run without retrying or scoring its holdout."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

import harness


def finalize(output: Path, failed_key: str, session_log: Path) -> None:
    inputs = harness.load_frozen_inputs()
    metadata = harness._load_json(output / "run-metadata.json")
    if metadata["runner_sha256"] != harness._sha256(Path(harness.__file__)):
        raise harness.HarnessError("executed runner changed before evidence preservation")
    for relative, expected_digest in metadata["frozen_asset_sha256"].items():
        if harness._sha256(harness.REPO_ROOT / relative) != expected_digest:
            raise harness.HarnessError(f"frozen asset changed: {relative}")

    schedule = harness.scheduled_trials(inputs)
    specs = {spec.key: spec for spec in schedule}
    if failed_key not in specs:
        raise harness.HarnessError("failed trial is outside the frozen schedule")
    completed = {}
    for journal in sorted((output / ".partial").glob("*.json")):
        if journal.stem not in specs:
            raise harness.HarnessError(f"unexpected journal: {journal.name}")
        spec = specs[journal.stem]
        structured, raw = harness._read_partial(journal)
        harness._validate_partial(
            inputs, spec, structured, raw, model=metadata["model"], effort=metadata["effort"]
        )
        if raw["prompt"] != harness._trial_prompt(spec.case) or raw["returncode"] != 0:
            raise harness.HarnessError(f"invalid completed journal: {journal.name}")
        completed[spec.key] = (structured, raw)
    if failed_key in completed or len(completed) >= len(schedule):
        raise harness.HarnessError("incomplete-run identity contradicts completed evidence")

    records = [json.loads(line) for line in session_log.read_text(encoding="utf-8").splitlines()]
    session = records[0]["payload"]
    if f"t023-{failed_key}-" not in session["cwd"] or session.get("parent_thread_id"):
        raise harness.HarnessError("timeout session does not identify the primary failed trial")
    visible = [
        record
        for record in records
        if record["type"] == "response_item"
        and (
            record["payload"]["type"]
            in {
                "custom_tool_call",
                "custom_tool_call_output",
                "function_call",
                "function_call_output",
            }
            or (
                record["payload"]["type"] == "message"
                and record["payload"].get("role") == "assistant"
                and record["payload"].get("channel") in {"commentary", "final"}
            )
        )
    ]
    if any(record["payload"].get("channel") == "final" for record in visible):
        raise harness.HarnessError("session contains a final response; diagnose before finalizing")

    missing = [spec.key for spec in schedule if spec.key not in completed]
    harness._jsonl_dump(
        output / "trials.jsonl",
        (completed[spec.key][0] for spec in schedule if spec.key in completed),
    )
    harness._jsonl_dump(
        output / "raw-trials.jsonl",
        (completed[spec.key][1] for spec in schedule if spec.key in completed),
    )
    harness._json_dump(
        output / "deterministic-evidence.json", harness.build_deterministic_evidence(inputs)
    )
    harness._json_dump(
        output / "failure-evidence.json",
        {
            "status": "BLOCKED",
            "type": "LIVE_TRIAL_TIMEOUT_UNCLASSIFIED",
            "trial_key": failed_key,
            "timeout_seconds": metadata["timeout_seconds"],
            "runner_error": f"{failed_key}: Codex exceeded the {metadata['timeout_seconds']}-second trial timeout",
            "session_id": session["id"],
            "session_started_at": session["timestamp"],
            "last_recorded_event_at": records[-1]["timestamp"],
            "source_session_log_sha256": harness._sha256(session_log),
            "session_log_projection": "Only visible assistant commentary/final and tool calls/results; no base instructions, private reasoning, authentication or unrelated sessions.",
            "observable_session_events": visible,
            "structured_final_response_available": False,
            "provider_or_network_root_cause_established": False,
            "retry_performed": False,
            "selection_performed": False,
            "disposition": "Required live cell is incomplete. Do not infer a routing failure, replace the missing observation, or score a partial acceptance matrix. Persisted Orchestrator recovery/re-entry authority is required.",
        },
    )
    harness._json_dump(
        output / "completeness.json",
        {
            "oracle_id": inputs.oracle["oracle_id"],
            "required_trials": len(schedule),
            "completed_trials": len(completed),
            "failed_trials": [failed_key],
            "missing_trial_keys": missing,
            "not_started_trial_keys": [key for key in missing if key != failed_key],
            "acceptance_matrix_complete": False,
            "scored": False,
        },
    )
    harness._json_dump(
        output / "selection.json",
        {
            "status": "BLOCKED",
            "selected_candidate": None,
            "reason": "incomplete live matrix; unclassified timeout; frozen selection rule not applied",
            "oracle_id": inputs.oracle["oracle_id"],
            "required_trials": len(schedule),
            "completed_trials": len(completed),
            "scored": False,
        },
    )
    metadata.update(
        {
            "status": "BLOCKED",
            "completed_trials": len(completed),
            "failed_trials": 1,
            "attempted_trials": len(completed) + 1,
            "not_started_trials": len(missing) - 1,
            "acceptance_matrix_complete": False,
            "evidence_preserved_at": datetime.now(UTC).isoformat(),
        }
    )
    harness._json_dump(output / "run-metadata.json", metadata)
    print(
        json.dumps(
            {"status": "BLOCKED", "completed_trials": len(completed), "failed_key": failed_key}
        )
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--failed-key", required=True)
    parser.add_argument("--session-log", type=Path, required=True)
    args = parser.parse_args()
    finalize(args.output.resolve(), args.failed_key, args.session_log.resolve())
