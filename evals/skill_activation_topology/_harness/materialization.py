"""Extracted MG1 topology harness implementation."""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import platform
import shutil
import subprocess
import uuid
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from .models import REPO_ROOT, WORKSPACE_FACTORY_ID, FrozenInputs, HarnessError


def materialize_fixture(
    inputs: FrozenInputs, case: dict[str, Any], destination: Path
) -> dict[str, Any]:
    role = case["fixture_role"]
    fixture = inputs.envelope["fixtures"][role]
    records: list[dict[str, Any]] = []
    for relative in fixture.get("directories", []):
        target = destination / relative
        target.mkdir(parents=True, exist_ok=False)
        records.append({"path": Path(relative).as_posix(), "kind": "directory"})
    for file_spec in fixture.get("files", []):
        target = destination / file_spec["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(file_spec["json"], indent=2, sort_keys=True) + "\n"
        target.write_text(payload, encoding="utf-8", newline="\n")
        records.append(
            {
                "path": Path(file_spec["path"]).as_posix(),
                "kind": "file",
                "bytes": len(payload.encode("utf-8")),
                "sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
                "json": file_spec["json"],
            }
        )
    return {"fixture_role": role, "records": records}


def _copy_record(source: Path, target: Path, destination: Path) -> dict[str, Any]:
    source_bytes = source.read_bytes()
    target_bytes = target.read_bytes()
    if target_bytes != source_bytes:
        raise HarnessError(f"byte-copy verification failed for {source}")
    return {
        "source": source.relative_to(REPO_ROOT).as_posix(),
        "target": target.relative_to(destination).as_posix(),
        "bytes": len(source_bytes),
        "sha256": hashlib.sha256(source_bytes).hexdigest(),
    }


def _validate_workspace_root(inputs: FrozenInputs, root: Path) -> dict[str, Any]:
    resolved = root.resolve(strict=True)
    canonical = REPO_ROOT.resolve(strict=True)
    policy = inputs.envelope["workspace_root_policy"]
    folded = str(resolved).casefold()
    matches = [term for term in policy["forbidden_root_substrings_casefold"] if term in folded]
    if matches:
        raise HarnessError(f"workspace root contains forbidden substring: {matches[0]}")
    if _is_relative_to(resolved, canonical) or _is_relative_to(canonical, resolved):
        raise HarnessError("workspace root overlaps the canonical repository")
    if any(
        (root / marker).exists()
        for marker in (".git", "agent-governance-source.json", ".agent-governance")
    ):
        raise HarnessError("fresh workspace unexpectedly contains role or Git state")
    if any(resolved.iterdir()):
        raise HarnessError("fresh workspace root is not empty")
    components = [resolved, *resolved.parents]
    linked_components = [
        str(path)
        for path in components
        if path.is_symlink() or (hasattr(os.path, "isjunction") and os.path.isjunction(path))
    ]
    if linked_components:
        raise HarnessError("workspace root traverses a symlink or junction")
    return {
        "absolute_root": str(resolved),
        "canonical_repository": str(canonical),
        "outside_canonical_repository": True,
        "forbidden_root_substring_matches": [],
        "linked_components": [],
        "canonical_git_metadata_present": False,
        "initially_empty": True,
    }


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _acl_diagnostic(root: Path) -> dict[str, Any]:
    if platform.system() != "Windows":
        return {"available": False, "reason": "non-Windows host"}
    try:
        process = subprocess.Popen(
            ["icacls", str(root)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        raw, _ = process.communicate(timeout=15)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}
    output = raw.decode("utf-8", errors="replace")
    return {
        "available": process.returncode == 0,
        "returncode": process.returncode,
        "stdout": output,
        "stderr": "",
    }


@contextlib.contextmanager
def _inherited_acl_workspace(
    workspace_parent: Path, *, prefix: str
) -> Iterator[tuple[Path, dict[str, Any]]]:
    """Create an atomic disposable root with ordinary inherited Windows ACLs."""
    if platform.system() != "Windows":
        raise HarnessError("the v11 workspace factory requires native Windows")
    parent = workspace_parent.resolve(strict=True)
    root: Path | None = None
    for _ in range(32):
        candidate = parent / f"{prefix}{uuid.uuid4().hex}"
        try:
            candidate.mkdir()
        except FileExistsError:
            continue
        root = candidate
        break
    if root is None:
        raise HarnessError("cannot allocate a unique v11 disposable workspace")
    diagnostic: dict[str, Any] = {
        "absolute_workspace_root": str(root),
        "workspace_creation_method": WORKSPACE_FACTORY_ID,
        "workspace_acl_profile_identity": WORKSPACE_FACTORY_ID,
        "python_runtime": platform.python_version(),
        "private_temp_creation_avoided": True,
        "acl_diagnostic": _acl_diagnostic(root),
        "cleanup_result": "PENDING",
    }
    try:
        yield root, diagnostic
    finally:
        try:
            shutil.rmtree(root)
        except OSError as exc:
            diagnostic["cleanup_result"] = "FAILED"
            diagnostic["cleanup_error"] = str(exc)
        else:
            diagnostic["cleanup_result"] = "REMOVED"


def materialize_candidate(
    inputs: FrozenInputs, candidate_id: str, destination: Path
) -> dict[str, Any]:
    if candidate_id not in inputs.oracle["candidate_ids"]:
        raise HarnessError(f"unknown candidate: {candidate_id}")
    candidate = inputs.manifest["candidates"][candidate_id]
    skill_root = destination / ".agents" / "skills"
    copied: list[dict[str, Any]] = []

    for entrypoint, entrypoint_data in candidate["entrypoints"].items():
        target_dir = skill_root / entrypoint
        target_dir.mkdir(parents=True, exist_ok=False)
        source = REPO_ROOT / entrypoint_data["skill_source"]
        target = target_dir / "SKILL.md"
        shutil.copyfile(source, target)
        copied.append(_copy_record(source, target, destination))

        references_dir = target_dir / "references"
        references_dir.mkdir()
        for capability in candidate["load_order"]:
            if capability not in entrypoint_data["capabilities"]:
                continue
            reference_source = REPO_ROOT / inputs.manifest["shared_references"][capability]
            reference_target = references_dir / f"{capability}.md"
            shutil.copyfile(reference_source, reference_target)
            copied.append(_copy_record(reference_source, reference_target, destination))

    return {
        "candidate_id": candidate_id,
        "presentation_revision": inputs.oracle["presentation_revision"],
        "capability_source_epoch": inputs.oracle["capability_source_epoch"],
        "construction": "byte-copy",
        "files": copied,
    }


def _validate_fixture_evidence(
    inputs: FrozenInputs, case: dict[str, Any], evidence: dict[str, Any]
) -> None:
    role = case["fixture_role"]
    fixture = inputs.envelope["fixtures"][role]
    expected_directories = {Path(value).as_posix() for value in fixture.get("directories", [])}
    actual_directories = {
        record.get("path")
        for record in evidence.get("records", [])
        if record.get("kind") == "directory"
    }
    expected_files = {item["path"]: item["json"] for item in fixture.get("files", [])}
    actual_files = {
        record.get("path"): record
        for record in evidence.get("records", [])
        if record.get("kind") == "file"
    }
    if (
        evidence.get("fixture_role") != role
        or actual_directories != expected_directories
        or set(actual_files) != set(expected_files)
    ):
        raise HarnessError(f"{case['id']}: fixture evidence differs from the frozen role")
    for path, value in expected_files.items():
        payload = json.dumps(value, indent=2, sort_keys=True) + "\n"
        record = actual_files[path]
        if (
            record.get("json") != value
            or record.get("bytes") != len(payload.encode("utf-8"))
            or record.get("sha256") != hashlib.sha256(payload.encode("utf-8")).hexdigest()
        ):
            raise HarnessError(f"{case['id']}: frozen fixture file evidence mismatch")
