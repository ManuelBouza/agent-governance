from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from chatgpt_skill_package import (  # noqa: E402
    SKILL_SOURCES,
    SkillPackageError,
    validate_source_topology,
)

ROOT = Path(__file__).resolve().parents[1]


def copy_skill_sources(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    for source_directory in SKILL_SOURCES.values():
        shutil.copytree(ROOT / source_directory, root / source_directory)
    return root


def test_workspace_isolation_top_level_source_is_rejected(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    promoted = root / "workspace-isolation-skill"
    promoted.mkdir()
    (promoted / "SKILL.md").write_text(
        "---\nname: workspace-isolation\ndescription: forbidden promotion\n---\n",
        encoding="utf-8",
    )

    with pytest.raises(SkillPackageError, match="cannot be promoted"):
        validate_source_topology(root)


def test_skill_local_reference_cannot_escape_package(tmp_path: Path) -> None:
    root = copy_skill_sources(tmp_path)
    skill_md = root / "executor-launch-handoff-skill" / "SKILL.md"
    skill_md.write_text(
        skill_md.read_text(encoding="utf-8")
        + "\nUnsafe synthetic fixture: references/../outside.md\n",
        encoding="utf-8",
    )
    (root / "outside.md").write_text("outside\n", encoding="utf-8")

    with pytest.raises(SkillPackageError, match="escapes package"):
        validate_source_topology(root)
