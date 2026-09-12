"""Candidate and synthetic-fixture materialization for v16."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any
from .models import REPO_ROOT, HarnessError

def _copy_verified(source: Path, target: Path) -> dict[str, Any]:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    before = source.read_bytes()
    after = target.read_bytes()
    if before != after:
        raise HarnessError(f"copy verification failed: {source}")
    return {"source": source.relative_to(REPO_ROOT).as_posix(), "target": target.as_posix(), "bytes": len(before), "sha256": hashlib.sha256(before).hexdigest()}

def materialize_candidate(manifest: dict[str, Any], candidate_id: str, workspace: Path) -> dict[str, Any]:
    candidate = manifest["candidates"].get(candidate_id)
    if not candidate:
        raise HarnessError(f"unknown candidate: {candidate_id}")
    skill_root = workspace / ".agents" / "skills"
    records = []
    for entrypoint, data in candidate["entrypoints"].items():
        root = skill_root / entrypoint
        records.append(_copy_verified(REPO_ROOT / data["skill_source"], root / "SKILL.md"))
        for capability in candidate["load_order"]:
            if capability in data["capabilities"]:
                records.append(_copy_verified(REPO_ROOT / manifest["shared_references"][capability], root / "references" / f"{capability}.md"))
    return {"candidate_id": candidate_id, "records": records}

def materialize_fixture(envelope: dict[str, Any], fixture_role: str, workspace: Path) -> dict[str, Any]:
    fixture = envelope["fixtures"].get(fixture_role)
    if fixture is None:
        raise HarnessError(f"unknown fixture role: {fixture_role}")
    records = []
    for rel in fixture.get("directories", []):
        (workspace / rel).mkdir(parents=True, exist_ok=True)
        records.append({"path": rel, "kind": "directory"})
    for spec in fixture.get("files", []):
        target = workspace / spec["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if "json" in spec:
            payload = json.dumps(spec["json"], indent=2, sort_keys=True) + "\n"
        else:
            payload = str(spec.get("text", ""))
        target.write_text(payload, encoding="utf-8", newline="\n")
        records.append({"path": spec["path"], "kind": "file", "sha256": hashlib.sha256(payload.encode()).hexdigest()})
    return {"fixture_role": fixture_role, "records": records}
