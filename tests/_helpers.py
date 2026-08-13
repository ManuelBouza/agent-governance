"""Reusable helpers for agent-governance deterministic tests.

These helpers intentionally operate on repository-relative structure
only. They do not interpret prose meaning or strategic content; they
expose mechanical checks for layout, reference resolution, and
separation between source-product artifacts and consumer
`.agent-coordination/` footprints.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT_MARKERS: tuple[str, ...] = (
    "AGENTS.md",
    "governance-core",
    "docs",
    "tests",
    "evals",
    "pyproject.toml",
)

CONSUMER_FOOTPRINT_DIR: str = ".agent-coordination"
CONSUMER_FOOTPRINT_ALIAS_DIR: str = ".agent-governance"

CORE_REQUIRED_MODULES: tuple[str, ...] = (
    "ADAPTERS.md",
    "COEXISTENCE.md",
    "CONTEXT.md",
    "EXECUTION.md",
    "EXECUTION-CONTROL.md",
    "GOVERNANCE.md",
    "HANDOFF.md",
    "INTERACTION.md",
    "LIFECYCLE.md",
    "PROTOCOL.md",
    "QUALITY.md",
    "SECURITY.md",
    "SKILL-DISCOVERY.md",
    "SKILL-SUPPLY-CHAIN.md",
    "SKILLS.md",
)

ASSURANCE_ROUTE: str = ".agent-governance/ASSURANCE.md"

SOURCE_MAINTENANCE_PATHS: tuple[str, ...] = (
    "docs/ORCHESTRATOR-CHECKPOINTS.md",
    "docs/orchestrator/CHECKPOINT.md",
    "docs/BRANCHING.md",
    "docs/DEVELOPMENT-WORKFLOW.md",
    "docs/EXECUTOR-HANDOFFS.md",
    "docs/TASK-CONTRACTS.md",
    "docs/TESTING-AND-EVALUATION.md",
    "docs/TESTING-SKILL-CAPABILITIES.md",
    "docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md",
    "docs/REFACTORING-WORKFLOW.md",
    "docs/RELEASES.md",
    "AGENTS.md",
)

CONSUMER_SKILL_DIR: str = "governance-skill"
MAINTAINER_SKILL_DIR: str = "maintainer-skill"

URL_SCHEMES: tuple[str, ...] = ("http://", "https://", "mailto:")

MARKDOWN_LINK_RE = re.compile(r"\[(?:[^\]]*)\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(r"`([^`\n]+)`")


@dataclass(frozen=True)
class Reference:
    """A single internal path reference extracted from a Markdown file."""

    source: Path
    line_no: int
    raw: str
    target: str

    @property
    def target_path(self) -> str:
        cleaned = self.target
        for prefix in URL_SCHEMES:
            if cleaned.startswith(prefix):
                return cleaned
        if "#" in cleaned:
            cleaned = cleaned.split("#", 1)[0]
        if "?" in cleaned:
            cleaned = cleaned.split("?", 1)[0]
        return cleaned


def find_repo_root(start: Path) -> Path:
    """Walk upward from `start` until a directory containing all
    `REPO_ROOT_MARKERS` is found. Falls back to `start` if no such
    directory exists.
    """

    candidate = start.resolve()
    for parent in (candidate, *candidate.parents):
        if all((parent / marker).exists() for marker in REPO_ROOT_MARKERS):
            return parent
    return start.resolve()


def extract_internal_references(markdown_path: Path) -> list[Reference]:
    """Return mechanical path references found in `markdown_path`.

    Recognises:
    - Markdown links `[text](path)`;
    - backtick-quoted paths (e.g. `` `docs/ORCHESTRATOR-CHECKPOINTS.md` ``).

    External/URL-style references and references that look like
    identifiers (e.g. `D019`, `T001`) are ignored. The caller decides
    what counts as "internal".
    """

    references: list[Reference] = []
    text = markdown_path.read_text(encoding="utf-8")

    for line_no, line in enumerate(text.splitlines(), start=1):
        for match in MARKDOWN_LINK_RE.finditer(line):
            references.append(
                Reference(
                    source=markdown_path,
                    line_no=line_no,
                    raw=match.group(1),
                    target=match.group(1),
                )
            )
        for match in BACKTICK_PATH_RE.finditer(line):
            references.append(
                Reference(
                    source=markdown_path,
                    line_no=line_no,
                    raw=match.group(1),
                    target=match.group(1),
                )
            )

    return references


def iter_markdown_files(root: Path) -> Iterable[Path]:
    """Yield all `.md` files under `root` recursively, sorted
    deterministically.
    """

    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            yield path


def protocol_version_from(core_governance: Path) -> str | None:
    """Return the single valid SemVer `Protocol-Version` declaration."""

    if not core_governance.exists():
        return None
    declarations = [
        line.split(":", 1)[1].strip()
        for line in core_governance.read_text(encoding="utf-8").splitlines()
        if line.startswith("Protocol-Version:")
    ]
    if len(declarations) != 1:
        return None
    version = declarations[0]
    if re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", version):
        return version
    return None


def required_core_modules_from(core_governance: Path) -> tuple[str, ...]:
    """Return required Core modules, including state-derived routing."""

    if not core_governance.exists():
        return CORE_REQUIRED_MODULES
    governance_text = core_governance.read_text(encoding="utf-8")
    if ASSURANCE_ROUTE in governance_text:
        return (*CORE_REQUIRED_MODULES, "ASSURANCE.md")
    return CORE_REQUIRED_MODULES


def looks_like_path(token: str) -> bool:
    """Heuristic: does `token` look like a repository path? Filters
    out identifiers like `D019` or `T001` that do not correspond to
    on-disk files.
    """

    if not token:
        return False
    if token.startswith(URL_SCHEMES):
        return False
    if "://" in token:
        return False
    if token.startswith("#"):
        return False
    if token[0] in "./":
        return True
    if "/" not in token and "\\" not in token:
        return False
    return not re.fullmatch(r"[A-Za-z0-9._-]+", token)
