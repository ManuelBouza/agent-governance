from __future__ import annotations

import json
import shutil
import sys
import zipfile
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from chatgpt_skill_package import (  # noqa: E402
    SKILL_SOURCES,
    SkillPackageError,
    build_packages,
    validate_source_topology,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCE_REVISION = "1" * 40
EXPECTED_SKILLS = {
    "source-maintainer",
    "repository-change-control",
    "upstream-version-revalidation",
    "research-evidence-traceability",
    "durable-work-checkpoint",
    "executor-launch-handoff",
}


def copy_skill_sources(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for source_directory in SKILL_SOURCES.values():
        shutil.copytree(ROOT / source_directory, root / source_directory)
    return root


def manifest_by_name(manifest: dict[str, object]) -> dict[str, dict[str, object]]:
    skills = manifest["skills"]
    assert isinstance(skills, list)
    return {str(item["name"]): item for item in skills}


def test_d082_topology_is_exactly_six_top_level_skills() -> None:
    topology = validate_source_topology(ROOT)
    assert set(topology) == EXPECTED_SKILLS
    assert set(topology) == set(SKILL_SOURCES)
    assert "workspace-isolation" not in topology
    assert len(topology) == 6


def test_builds_six_source_identical_skill_archives_and_manifest(tmp_path: Path) -> None:
    output = tmp_path / "out"
    manifest = build_packages(ROOT, output, SOURCE_REVISION)
    skills = manifest_by_name(manifest)

    assert manifest["schema"] == "agent-governance-chatgpt-skill-packages/v1"
    assert manifest["source_revision"] == SOURCE_REVISION
    assert manifest["bundle_count"] == 6
    assert set(skills) == EXPECTED_SKILLS
    assert {path.name for path in output.glob("*.zip")} == {
        f"{name}.zip" for name in EXPECTED_SKILLS
    }
    assert not (output / "workspace-isolation.zip").exists()
    assert json.loads((output / "manifest.json").read_text(encoding="utf-8")) == manifest

    for skill_name, item in skills.items():
        source_dir = ROOT / str(item["source_directory"])
        archive_path = output / str(item["archive"])
        file_records = item["files"]
        assert isinstance(file_records, list)
        expected_members = {str(record["path"]) for record in file_records}
        assert "SKILL.md" in expected_members

        with zipfile.ZipFile(archive_path) as archive:
            assert set(archive.namelist()) == expected_members
            assert all(
                not member.startswith(f"{source_dir.name}/") for member in archive.namelist()
            )
            for member in archive.namelist():
                assert archive.read(member) == (source_dir / member).read_bytes()

        assert skill_name == archive_path.stem


def test_maintainer_and_executor_resources_are_preserved(tmp_path: Path) -> None:
    output = tmp_path / "out"
    build_packages(ROOT, output, SOURCE_REVISION)

    with zipfile.ZipFile(output / "source-maintainer.zip") as archive:
        members = set(archive.namelist())
        assert "references/orchestrator-route.md" in members
        assert "references/executor-route.md" in members
        assert "references/TASK-CONTRACT-TEMPLATE-USAGE.md" in members
        assert "references/TASK-CONTRACT-V4-TEMPLATE.md" in members

    with zipfile.ZipFile(output / "executor-launch-handoff.zip") as archive:
        assert "references/workspace-isolation.md" in set(archive.namelist())


def test_repeated_build_is_byte_stable_for_same_inputs(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first_manifest = build_packages(ROOT, first, SOURCE_REVISION)
    second_manifest = build_packages(ROOT, second, SOURCE_REVISION)

    assert first_manifest == second_manifest
    assert (first / "manifest.json").read_bytes() == (second / "manifest.json").read_bytes()
    for name in EXPECTED_SKILLS:
        assert (first / f"{name}.zip").read_bytes() == (second / f"{name}.zip").read_bytes()


def test_wrong_front_matter_name_fails_closed(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    skill_md = root / "repository-change-control-skill" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8").replace(
            "name: repository-change-control", "name: wrong-name", 1
        ),
        encoding="utf-8",
    )

    with pytest.raises(SkillPackageError, match="Skill name mismatch"):
        validate_source_topology(root)


def test_missing_skill_local_reference_fails_closed(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    missing = root / "executor-launch-handoff-skill" / "references" / "workspace-isolation.md"
    missing.unlink()

    with pytest.raises(SkillPackageError, match="missing Skill-local reference"):
        validate_source_topology(root)


def test_forbidden_local_state_inside_skill_fails_closed(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    cache = root / "maintainer-skill" / "__pycache__"
    cache.mkdir()
    (cache / "leak.pyc").write_bytes(b"not-package-content")

    with pytest.raises(SkillPackageError, match="forbidden local/generated Skill path"):
        validate_source_topology(root)


def test_output_directory_contamination_is_preserved_and_blocks(tmp_path: Path) -> None:
    output = tmp_path / "out"
    output.mkdir()
    unrelated = output / "unrelated.zip"
    unrelated.write_bytes(b"do-not-delete")

    with pytest.raises(SkillPackageError, match="unrelated entries"):
        build_packages(ROOT, output, SOURCE_REVISION)
    assert unrelated.read_bytes() == b"do-not-delete"


def test_source_revision_is_required(tmp_path: Path) -> None:
    with pytest.raises(SkillPackageError, match="source revision is required"):
        build_packages(ROOT, tmp_path / "out", "   ")


def test_output_cannot_be_inside_skill_source(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    output = root / "maintainer-skill" / "generated"

    with pytest.raises(SkillPackageError, match="must not be inside"):
        build_packages(root, output, SOURCE_REVISION)
