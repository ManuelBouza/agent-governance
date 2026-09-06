"""CLI for deterministic ChatGPT portable-workspace validation and classification."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from _chatgpt_workspace import (
    Decision,
    Identity,
    LockObservation,
    Status,
    build_publication_plan,
    classify_acquisition,
    classify_gc,
    classify_release,
    classify_write_entry,
    validate_snapshot,
    verify_release,
)


def _input(path: str) -> Mapping[str, Any]:
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    value = json.loads(text)
    if not isinstance(value, Mapping):
        raise ValueError("input must be a JSON object")
    return value


def _decision(value: Mapping[str, Any]) -> Decision:
    details = value.get("details", {})
    if not isinstance(details, dict):
        raise ValueError("decision details must be an object")
    return Decision(Status(value["status"]), str(value.get("reason", "")), details)


def _optional_bool(value: Mapping[str, Any], field: str, default: bool) -> bool:
    candidate = value.get(field, default)
    if type(candidate) is not bool:
        raise ValueError(f"{field} must be a boolean")
    return candidate


def _classify(command: str, value: Mapping[str, Any]) -> Decision:
    if command == "classify-lock":
        return classify_acquisition(LockObservation.from_mapping(value))
    if command == "validate-snapshot":
        return validate_snapshot(
            Path(value["archive"]),
            Path(value["destination"]),
            expected_archive_sha256=value["expected_archive_sha256"],
            expected_identity=Identity.from_mapping(value["expected_identity"]),
            expected_remote_head=value["expected_remote_head"],
            expected_remote_tree=value["expected_remote_tree"],
            expected_target_branch=value.get("expected_target_branch", "develop"),
            require_clean=_optional_bool(value, "require_clean", True),
            require_remote_tree_equivalence=_optional_bool(
                value, "require_remote_tree_equivalence", False
            ),
        )
    if command == "write-gate":
        return classify_write_entry(
            _decision(value["snapshot"]),
            expected_identity=Identity.from_mapping(value["expected_identity"]),
            lock_observation=LockObservation.from_mapping(value["lock_observation"]),
            observed_remote_head=value.get("observed_remote_head"),
            observed_remote_tree=value.get("observed_remote_tree"),
            require_tree_equivalence=_optional_bool(value, "require_tree_equivalence", False),
            expected_target_branch=value.get("expected_target_branch", "develop"),
        )
    if command == "release":
        return classify_release(
            LockObservation.from_mapping(value["lock_observation"]),
            Identity.from_mapping(value["expected_identity"]),
            value["expected_sentinel_blob_sha"],
        )
    if command == "verify-release":
        return verify_release(LockObservation.from_mapping(value["lock_observation"]))
    if command == "gc":
        fields = (
            "merged",
            "closed",
            "integration_verified",
            "target_snapshot_validated",
            "target_snapshot_promoted",
            "target_snapshot_revalidated",
        )
        return classify_gc(**{field: value.get(field) for field in fields})
    if command == "publish-plan":
        return build_publication_plan(
            Path(value["repository_path"]),
            repository=value["repository"],
            work_unit=value["work_unit"],
            topic_branch=value["topic_branch"],
            expected_remote_head=value["expected_remote_head"],
            changed_paths=value["changed_paths"],
        )
    raise ValueError(f"unsupported command: {command}")


_ALLOWED = {
    Status.SNAPSHOT_VALID,
    Status.ACQUIRE_ALLOWED,
    Status.WRITE_ALLOWED,
    Status.RELEASE_ALLOWED,
    Status.RELEASED,
    Status.GC_ELIGIBLE,
    Status.PUBLICATION_PLAN_READY,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=(
            "classify-lock",
            "validate-snapshot",
            "write-gate",
            "release",
            "verify-release",
            "gc",
            "publish-plan",
        ),
    )
    parser.add_argument("--input", required=True, help="JSON file path, or - for stdin")
    args = parser.parse_args(argv)
    try:
        result = _classify(args.command, _input(args.input))
    except (KeyError, OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        result = Decision(Status.INVALID_INPUT, str(error))
    print(json.dumps(result.as_dict(), sort_keys=True, separators=(",", ":")))
    return 0 if result.status in _ALLOWED else 2


if __name__ == "__main__":
    raise SystemExit(main())
