"""Tracked-file measurement reports and canonical report identity."""

from __future__ import annotations

import hashlib
import posixpath
import re
import tempfile
from pathlib import Path, PurePosixPath

from .common import MeasurementError, canonical_json, relative_output
from .tracked_files import git, read_tracked_file, tracked_paths

SCHEMA_VERSION = "1.0.0"
DEFAULT_BASELINE = "baselines/repository-context-source-v1.json"
BOOTSTRAP_PATHS = ("AGENTS.md", "docs/orchestrator/CHECKPOINT.md")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
MARKDOWN_CODE_PATH = re.compile(r"`([^`\n]+)`")
MARKDOWN_HEADING = re.compile(r"^#{1,6}(?:[ \t]+|$)", re.MULTILINE)
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")

TRACKED_CONTENT_DIGEST_KEY = "tracked_content_digest"
VOLATILE_EXECUTION_METADATA_KEY = "volatile_execution_metadata"


def category(path: str, is_text: bool) -> str:
    if not is_text:
        return "binary"
    suffix = PurePosixPath(path).suffix.lower()
    categories = {
        ".json": "json",
        ".jsonl": "jsonl",
        ".md": "markdown",
        ".py": "python",
        ".sh": "shell",
        ".toml": "toml",
        ".yaml": "yaml",
        ".yml": "yaml",
    }
    return categories.get(suffix, "text")


def line_count(text: str) -> int:
    return len(text.splitlines())


def local_markdown_target(source: str, raw_target: str, tracked: set[str]) -> str | None:
    target = raw_target.strip("<>").split("#", 1)[0]
    if not target or target.startswith(("#", "//")) or URI_SCHEME.match(target):
        return None
    if target in tracked:
        return target
    if target.startswith("/"):
        candidate = posixpath.normpath(target.lstrip("/"))
    else:
        candidate = posixpath.normpath(posixpath.join(posixpath.dirname(source), target))
    if candidate.startswith("../") or candidate == ".." or candidate not in tracked:
        return None
    return candidate


def file_record(path: str, data: bytes) -> tuple[dict[str, object], str | None]:
    is_text = b"\0" not in data
    text = None
    if is_text:
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            is_text = False
    suffix = PurePosixPath(path).suffix.lower() or None
    record: dict[str, object] = {
        "byte_size": len(data),
        "category": category(path, is_text),
        "character_count": len(text) if text is not None else None,
        "extension": suffix,
        "line_count": line_count(text) if text is not None else None,
        "markdown_heading_count": (
            len(MARKDOWN_HEADING.findall(text)) if text is not None and suffix == ".md" else None
        ),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "text_encoding": "utf-8" if text is not None else None,
    }
    return record, text


def metric_totals(records: list[dict[str, object]]) -> dict[str, object]:
    return {
        "byte_size": sum(int(record["byte_size"]) for record in records),
        "character_count": sum(int(record["character_count"] or 0) for record in records),
        "file_count": len(records),
        "line_count": sum(int(record["line_count"] or 0) for record in records),
        "markdown_heading_count": sum(
            int(record["markdown_heading_count"] or 0) for record in records
        ),
        "text_file_count": sum(record["text_encoding"] == "utf-8" for record in records),
    }


def build_report(
    root: Path,
    *,
    excluded_paths: set[str] | None = None,
    source_git_revision: str | None = None,
) -> dict[str, object]:
    """Build canonical measurement data from files selected by the Git index."""
    root = root.resolve()
    excluded = {PurePosixPath(DEFAULT_BASELINE).as_posix()}
    excluded.update(PurePosixPath(path).as_posix() for path in (excluded_paths or set()))
    paths = tracked_paths(root, excluded)
    tracked = set(paths)
    records: list[dict[str, object]] = []
    markdown_text: dict[str, str] = {}
    for path in paths:
        record, text = file_record(path, read_tracked_file(root, path))
        records.append(record)
        if text is not None and record["extension"] == ".md":
            markdown_text[path] = text

    edge_counts: dict[tuple[str, str], int] = {}
    reference_counts = {path: 0 for path in markdown_text}
    for source, text in markdown_text.items():
        raw_targets = [match.group(1) for match in MARKDOWN_LINK.finditer(text)]
        raw_targets.extend(match.group(1) for match in MARKDOWN_CODE_PATH.finditer(text))
        for raw_target in raw_targets:
            target = local_markdown_target(source, raw_target, tracked)
            if target is None:
                continue
            edge = (source, target)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
            reference_counts[source] += 1
    for record in records:
        record["structural_markdown_reference_count"] = reference_counts.get(str(record["path"]))

    by_category: dict[str, dict[str, object]] = {}
    for record_category in sorted({str(record["category"]) for record in records}):
        by_category[record_category] = metric_totals(
            [record for record in records if record["category"] == record_category]
        )

    bootstrap = [record for record in records if record["path"] in BOOTSTRAP_PATHS]
    missing_bootstrap = sorted(set(BOOTSTRAP_PATHS) - {str(item["path"]) for item in bootstrap})
    if missing_bootstrap:
        raise MeasurementError(f"missing tracked bootstrap files: {', '.join(missing_bootstrap)}")

    text_records = [record for record in records if record["text_encoding"] == "utf-8"]
    largest = sorted(text_records, key=lambda item: (-int(item["byte_size"]), str(item["path"])))
    content_identity = [{"path": record["path"], "sha256": record["sha256"]} for record in records]
    if source_git_revision is None:
        source_git_revision = git(root, "rev-parse", "HEAD").decode("ascii").strip()
    return {
        "bootstrap_physical_footprint": {
            "description": "Physical UTF-8 footprint of source cold-start router files; no token or observed-load claim.",
            "files": bootstrap,
            "totals": metric_totals(bootstrap),
        },
        "excluded_paths": sorted(excluded),
        "files": records,
        "largest_context_relevant_files": {
            "description": "Largest UTF-8 text files by physical byte size; not runtime context fan-out.",
            "limit": 20,
            "files": [
                {
                    "byte_size": record["byte_size"],
                    "category": record["category"],
                    "path": record["path"],
                }
                for record in largest[:20]
            ],
        },
        "measurement_scope": {
            "canonical_size_metric": "raw file bytes; UTF-8 character metrics only for decodable text",
            "inventory": "paths returned by git ls-files --cached, measured from worktree bytes",
            "observed_runtime_context_metrics": False,
        },
        "report_schema_version": SCHEMA_VERSION,
        "structural_markdown_references": {
            "description": "Static resolvable local Markdown links and code-span paths to tracked files; not observed RFO, TMC, CAR, or runtime loads.",
            "edge_count": len(edge_counts),
            "edges": [
                {"occurrences": count, "source": source, "target": target}
                for (source, target), count in sorted(edge_counts.items())
            ],
            "reference_count": sum(edge_counts.values()),
        },
        "totals": {"by_category": by_category, "repository": metric_totals(records)},
        TRACKED_CONTENT_DIGEST_KEY: hashlib.sha256(canonical_json(content_identity)).hexdigest(),
        VOLATILE_EXECUTION_METADATA_KEY: {
            "description": (
                "Per-execution provenance; NOT part of canonical baseline identity "
                "and MAY legitimately differ across runs even when canonical "
                "baseline identity is identical."
            ),
            "source_git_revision": source_git_revision,
        },
    }


def canonical_payload(report: dict[str, object]) -> dict[str, object]:
    """Return the canonical baseline portion of a report."""
    return {key: value for key, value in report.items() if key != VOLATILE_EXECUTION_METADATA_KEY}


def canonical_identity_digest(report: dict[str, object]) -> str:
    """Return the SHA-256 of :func:`canonical_payload`."""
    return hashlib.sha256(canonical_json(canonical_payload(report))).hexdigest()


def validate_canonical_identity(*reports: dict[str, object]) -> None:
    """Assert that every supplied report shares the same canonical identity."""
    if not reports:
        raise MeasurementError("validate_canonical_identity requires at least one report")
    reference = canonical_identity_digest(reports[0])
    for index, report in enumerate(reports[1:], start=1):
        current = canonical_identity_digest(report)
        if current != reference:
            raise MeasurementError(
                f"canonical identity mismatch at report index {index}: {reference} != {current}"
            )


def write_report(root: Path, output: Path) -> dict[str, object]:
    """Build a report and atomically write its canonical JSON bytes."""
    excluded = {_relative} if (_relative := relative_output(root, output)) else set()
    report = build_report(root, excluded_paths=excluded)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_json(report))
    temporary.replace(output)
    return report
