from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

SKILL_SOURCES: dict[str, str] = {
    "source-maintainer": "maintainer-skill",
    "repository-change-control": "repository-change-control-skill",
    "upstream-version-revalidation": "upstream-version-revalidation-skill",
    "research-evidence-traceability": "research-evidence-traceability-skill",
    "durable-work-checkpoint": "durable-work-checkpoint-skill",
    "executor-launch-handoff": "executor-launch-handoff-skill",
}

FORBIDDEN_TOP_LEVEL_SKILLS = {"workspace-isolation"}
FORBIDDEN_TOP_LEVEL_SOURCE_DIRECTORIES = {"workspace-isolation", "workspace-isolation-skill"}
FORBIDDEN_PATH_PARTS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    ".DS_Store",
}
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
SKILL_NAME_RE = re.compile(r"^name:\s*([A-Za-z0-9][A-Za-z0-9_-]*)\s*$")
REFERENCE_RE = re.compile(r"(?<![A-Za-z0-9_.-])(references/[A-Za-z0-9_./-]+\.md)")


class SkillPackageError(ValueError):
    """Raised when canonical Skill source cannot be packaged safely."""


@dataclass(frozen=True)
class SourceFile:
    relative_path: str
    sha256: str
    size: int


@dataclass(frozen=True)
class SkillBundle:
    name: str
    source_directory: str
    archive: str
    archive_sha256: str
    files: tuple[SourceFile, ...]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parse_skill_name(skill_md: Path) -> str:
    try:
        lines = skill_md.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        raise SkillPackageError(f"cannot read UTF-8 Skill file: {skill_md}") from exc

    if not lines or lines[0].strip() != "---":
        raise SkillPackageError(f"missing YAML front matter in {skill_md}")

    name: str | None = None
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        match = SKILL_NAME_RE.match(line.strip())
        if match:
            if name is not None:
                raise SkillPackageError(f"duplicate name field in {skill_md}")
            name = match.group(1)

    if not closed:
        raise SkillPackageError(f"unterminated YAML front matter in {skill_md}")
    if name is None:
        raise SkillPackageError(f"missing Skill name in {skill_md}")
    return name


def _validate_relative_path(relative: Path) -> str:
    if relative.is_absolute() or ".." in relative.parts:
        raise SkillPackageError(f"unsafe Skill path: {relative}")
    if any(part in FORBIDDEN_PATH_PARTS for part in relative.parts):
        raise SkillPackageError(f"forbidden local/generated Skill path: {relative}")
    return PurePosixPath(*relative.parts).as_posix()


def iter_skill_files(skill_dir: Path) -> tuple[Path, ...]:
    if not skill_dir.is_dir():
        raise SkillPackageError(f"missing Skill directory: {skill_dir}")
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        raise SkillPackageError(f"missing root SKILL.md: {skill_dir}")

    files: list[Path] = []
    for path in sorted(skill_dir.rglob("*"), key=lambda item: item.as_posix()):
        relative = path.relative_to(skill_dir)
        _validate_relative_path(relative)
        if path.is_symlink():
            raise SkillPackageError(f"symlinks are not allowed in Skill packages: {relative}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise SkillPackageError(f"unsupported Skill filesystem entry: {relative}")
        files.append(path)
    return tuple(files)


def validate_skill_local_references(skill_dir: Path, files: Iterable[Path]) -> None:
    for path in files:
        if path.suffix.lower() != ".md":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise SkillPackageError(f"cannot read Markdown Skill resource: {path}") from exc
        for reference in sorted(set(REFERENCE_RE.findall(text))):
            relative_reference = PurePosixPath(reference)
            if ".." in relative_reference.parts:
                raise SkillPackageError(f"Skill reference escapes package: {reference}")
            target = skill_dir.joinpath(*relative_reference.parts)
            if not target.is_file():
                relative_source = path.relative_to(skill_dir).as_posix()
                raise SkillPackageError(
                    f"missing Skill-local reference {reference!r} from {relative_source}"
                )


def validate_source_topology(root: Path) -> dict[str, tuple[Path, tuple[Path, ...]]]:
    if set(SKILL_SOURCES) & FORBIDDEN_TOP_LEVEL_SKILLS:
        raise SkillPackageError("forbidden top-level Skill configured")
    if len(set(SKILL_SOURCES.values())) != len(SKILL_SOURCES):
        raise SkillPackageError("duplicate Skill source directory configured")
    forbidden_sources = sorted(
        directory
        for directory in FORBIDDEN_TOP_LEVEL_SOURCE_DIRECTORIES
        if (root / directory).exists()
    )
    if forbidden_sources:
        raise SkillPackageError(
            "workspace-isolation cannot be promoted to a top-level Skill source: "
            + ", ".join(forbidden_sources)
        )

    validated: dict[str, tuple[Path, tuple[Path, ...]]] = {}
    seen_names: set[str] = set()
    for expected_name, source_directory in SKILL_SOURCES.items():
        skill_dir = root / source_directory
        files = iter_skill_files(skill_dir)
        actual_name = parse_skill_name(skill_dir / "SKILL.md")
        if actual_name != expected_name:
            raise SkillPackageError(
                f"Skill name mismatch for {source_directory}: expected {expected_name!r}, "
                f"found {actual_name!r}"
            )
        if actual_name in seen_names:
            raise SkillPackageError(f"duplicate Skill name: {actual_name}")
        seen_names.add(actual_name)
        validate_skill_local_references(skill_dir, files)
        validated[actual_name] = (skill_dir, files)

    if set(validated) != set(SKILL_SOURCES):
        raise SkillPackageError("canonical top-level Skill set does not match D082 topology")
    if set(validated) & FORBIDDEN_TOP_LEVEL_SKILLS:
        raise SkillPackageError("workspace-isolation cannot be a top-level Skill")
    return validated


def _zip_info(relative_path: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(relative_path, date_time=FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (stat.S_IFREG | 0o644) << 16
    info.flag_bits |= 0x800
    return info


def _source_file(skill_dir: Path, path: Path) -> SourceFile:
    data = path.read_bytes()
    return SourceFile(
        relative_path=path.relative_to(skill_dir).as_posix(),
        sha256=sha256_bytes(data),
        size=len(data),
    )


def build_bundle(
    *,
    name: str,
    skill_dir: Path,
    files: tuple[Path, ...],
    output_dir: Path,
) -> SkillBundle:
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"{name}.zip"
    with zipfile.ZipFile(
        archive_path,
        mode="w",
        compression=zipfile.ZIP_DEFLATED,
        compresslevel=9,
        strict_timestamps=True,
    ) as archive:
        for path in files:
            relative_path = _validate_relative_path(path.relative_to(skill_dir))
            archive.writestr(
                _zip_info(relative_path),
                path.read_bytes(),
                compress_type=zipfile.ZIP_DEFLATED,
                compresslevel=9,
            )

    source_files = tuple(_source_file(skill_dir, path) for path in files)
    return SkillBundle(
        name=name,
        source_directory=skill_dir.name,
        archive=archive_path.name,
        archive_sha256=sha256_bytes(archive_path.read_bytes()),
        files=source_files,
    )


def build_packages(root: Path, output_dir: Path, source_revision: str) -> dict[str, object]:
    if not source_revision.strip():
        raise SkillPackageError("source revision is required")
    resolved_root = root.resolve()
    resolved_output = output_dir.resolve()
    for source_directory in SKILL_SOURCES.values():
        skill_dir = (resolved_root / source_directory).resolve()
        if resolved_output == skill_dir or skill_dir in resolved_output.parents:
            raise SkillPackageError("output directory must not be inside a canonical Skill source")

    topology = validate_source_topology(resolved_root)
    resolved_output.mkdir(parents=True, exist_ok=True)

    expected_outputs = {f"{name}.zip" for name in SKILL_SOURCES} | {"manifest.json"}
    unexpected_outputs = sorted(
        path.name for path in resolved_output.iterdir() if path.name not in expected_outputs
    )
    if unexpected_outputs:
        raise SkillPackageError(
            "output directory contains unrelated entries: " + ", ".join(unexpected_outputs)
        )

    bundles: list[SkillBundle] = []
    for name in SKILL_SOURCES:
        skill_dir, files = topology[name]
        bundles.append(
            build_bundle(name=name, skill_dir=skill_dir, files=files, output_dir=resolved_output)
        )

    manifest: dict[str, object] = {
        "schema": "agent-governance-chatgpt-skill-packages/v1",
        "source_revision": source_revision.strip(),
        "bundle_count": len(bundles),
        "skills": [
            {
                "name": bundle.name,
                "source_directory": bundle.source_directory,
                "archive": bundle.archive,
                "archive_sha256": bundle.archive_sha256,
                "files": [
                    {
                        "path": source_file.relative_path,
                        "sha256": source_file.sha256,
                        "size": source_file.size,
                    }
                    for source_file in bundle.files
                ],
            }
            for bundle in bundles
        ],
    }
    manifest_path = resolved_output / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest


def validate_packages(root: Path) -> None:
    validate_source_topology(root.resolve())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate and deterministically package the six D082 Agent Governance Skills."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-revision")
    parser.add_argument("--validate-only", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.validate_only:
        validate_packages(args.root)
        return 0
    if args.output is None:
        raise SystemExit("--output is required unless --validate-only is used")
    if not args.source_revision:
        raise SystemExit("--source-revision is required when building packages")
    manifest = build_packages(args.root, args.output, args.source_revision)
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
