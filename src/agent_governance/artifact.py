"""Build a self-contained Governance Skill artifact from canonical source."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

BUILD_SCHEMA_VERSION = "1.0.0"
IDENTITY_FILENAME = "artifact-identity.json"
SCHEMA_SOURCE = Path("schemas/governance-artifact-identity.schema.json")
SEMVER = re.compile(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)")
COMMIT = re.compile(r"[0-9a-f]{40,64}")


class ArtifactBuildError(Exception):
    """Expected fail-closed artifact build error."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _copy_file(source: Path, destination: Path) -> None:
    if source.is_symlink() or not source.is_file():
        raise ArtifactBuildError(f"missing or unsafe build input: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _copy_tree_files(source: Path, destination: Path, pattern: str = "*") -> None:
    if source.is_symlink() or not source.is_dir():
        raise ArtifactBuildError(f"missing or unsafe build input directory: {source}")
    files = sorted(path for path in source.rglob(pattern) if path.is_file())
    if not files:
        raise ArtifactBuildError(f"build input directory is empty: {source}")
    for path in files:
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        _copy_file(path, destination / path.relative_to(source))


def _protocol_version(governance: Path) -> str:
    if governance.is_symlink() or not governance.is_file():
        raise ArtifactBuildError(f"missing or unsafe protocol authority: {governance}")
    declarations = [
        line.split(":", 1)[1].strip()
        for line in governance.read_text(encoding="utf-8").splitlines()
        if line.startswith("Protocol-Version:")
    ]
    if len(declarations) != 1 or SEMVER.fullmatch(declarations[0]) is None:
        raise ArtifactBuildError("canonical GOVERNANCE.md has invalid Protocol-Version")
    return declarations[0]


def _source_commit(source_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=source_root,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    commit = result.stdout.strip()
    if result.returncode != 0 or COMMIT.fullmatch(commit) is None:
        raise ArtifactBuildError("cannot derive full source commit; pass --source-commit")
    return commit


def _inventory(artifact: Path) -> list[dict[str, object]]:
    files = []
    for path in sorted(candidate for candidate in artifact.rglob("*") if candidate.is_file()):
        relative = path.relative_to(artifact).as_posix()
        if relative == IDENTITY_FILENAME:
            continue
        files.append({"path": relative, "sha256": _sha256(path), "size": path.stat().st_size})
    return files


def build_artifact(
    source_root: Path,
    output: Path,
    *,
    skill_version: str,
    installed_footprint_version: str,
    source_commit: str | None = None,
) -> dict[str, object]:
    """Build artifact at an absent output path and return generated identity."""
    source_root = source_root.resolve()
    output = output.absolute()
    if output.exists() or output.is_symlink():
        raise ArtifactBuildError(f"output already exists: {output}")
    for field, value in (
        ("skill version", skill_version),
        ("installed-footprint version", installed_footprint_version),
    ):
        if SEMVER.fullmatch(value) is None:
            raise ArtifactBuildError(f"{field} must be strict SemVer")
    commit = source_commit or _source_commit(source_root)
    if COMMIT.fullmatch(commit) is None:
        raise ArtifactBuildError("source commit must be 40-64 lowercase hexadecimal characters")

    skill_source = source_root / "governance-skill"
    core_source = source_root / "governance-core"
    runtime_source = source_root / "src" / "agent_governance"
    schema_source = source_root / SCHEMA_SOURCE
    protocol_version = _protocol_version(core_source / "GOVERNANCE.md")
    output.parent.mkdir(parents=True, exist_ok=True)

    temporary = Path(tempfile.mkdtemp(prefix=f".{output.name}-", dir=output.parent))
    try:
        _copy_tree_files(skill_source, temporary)
        _copy_tree_files(core_source, temporary / "core", "*.md")
        _copy_tree_files(runtime_source, temporary / "runtime" / "agent_governance", "*.py")
        _copy_file(schema_source, temporary / SCHEMA_SOURCE.name)

        identity: dict[str, object] = {
            "build_schema_version": BUILD_SCHEMA_VERSION,
            "skill_version": skill_version,
            "protocol_version": protocol_version,
            "installed_footprint_version": installed_footprint_version,
            "source_commit": commit,
            "files": _inventory(temporary),
        }
        identity["payload_digest"] = hashlib.sha256(_canonical_json(identity["files"])).hexdigest()
        identity["identity_digest"] = hashlib.sha256(_canonical_json(identity)).hexdigest()
        (temporary / IDENTITY_FILENAME).write_bytes(_canonical_json(identity))
        temporary.rename(output)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return identity


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--skill-version", required=True)
    parser.add_argument("--installed-footprint-version", required=True)
    parser.add_argument("--source-commit")
    args = parser.parse_args(argv)
    try:
        identity = build_artifact(
            args.source_root,
            args.output,
            skill_version=args.skill_version,
            installed_footprint_version=args.installed_footprint_version,
            source_commit=args.source_commit,
        )
    except (ArtifactBuildError, OSError, UnicodeError) as error:
        parser.exit(1, f"error: {error}\n")
    print(json.dumps(identity, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
