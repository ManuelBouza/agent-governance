"""Measure deterministic physical context properties of a tracked Git tree."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import tempfile
from pathlib import Path, PurePosixPath

SCHEMA_VERSION = "1.0.0"
DEFAULT_BASELINE = "baselines/repository-context-source-v1.json"
BOOTSTRAP_PATHS = ("AGENTS.md", "docs/orchestrator/CHECKPOINT.md")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
MARKDOWN_CODE_PATH = re.compile(r"`([^`\n]+)`")
MARKDOWN_HEADING = re.compile(r"^#{1,6}(?:[ \t]+|$)", re.MULTILINE)
URI_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


class MeasurementError(Exception):
    """Raised when a repository cannot be measured deterministically."""


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _git(root: Path, *arguments: str) -> bytes:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        capture_output=True,
        timeout=30,
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise MeasurementError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout


def _tracked_paths(root: Path, excluded: set[str]) -> list[str]:
    raw = _git(root, "ls-files", "--cached", "-z")
    paths = [os.fsdecode(path) for path in raw.split(b"\0") if path]
    return sorted(path for path in paths if PurePosixPath(path).as_posix() not in excluded)


def _read_tracked_file(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink():
        return os.fsencode(os.readlink(path))
    try:
        return path.read_bytes()
    except OSError as error:
        raise MeasurementError(f"cannot read tracked file {relative}: {error}") from error


def _category(path: str, is_text: bool) -> str:
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


def _line_count(text: str) -> int:
    return len(text.splitlines())


def _local_markdown_target(source: str, raw_target: str, tracked: set[str]) -> str | None:
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


def _file_record(path: str, data: bytes) -> tuple[dict[str, object], str | None]:
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
        "category": _category(path, is_text),
        "character_count": len(text) if text is not None else None,
        "extension": suffix,
        "line_count": _line_count(text) if text is not None else None,
        "markdown_heading_count": (
            len(MARKDOWN_HEADING.findall(text)) if text is not None and suffix == ".md" else None
        ),
        "path": path,
        "sha256": hashlib.sha256(data).hexdigest(),
        "text_encoding": "utf-8" if text is not None else None,
    }
    return record, text


def _metric_totals(records: list[dict[str, object]]) -> dict[str, object]:
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


def build_report(root: Path, *, excluded_paths: set[str] | None = None) -> dict[str, object]:
    """Build canonical measurement data from files selected by the Git index."""
    root = root.resolve()
    excluded = {PurePosixPath(DEFAULT_BASELINE).as_posix()}
    excluded.update(PurePosixPath(path).as_posix() for path in (excluded_paths or set()))
    paths = _tracked_paths(root, excluded)
    tracked = set(paths)
    records: list[dict[str, object]] = []
    markdown_text: dict[str, str] = {}
    for path in paths:
        record, text = _file_record(path, _read_tracked_file(root, path))
        records.append(record)
        if text is not None and record["extension"] == ".md":
            markdown_text[path] = text

    edge_counts: dict[tuple[str, str], int] = {}
    reference_counts = {path: 0 for path in markdown_text}
    for source, text in markdown_text.items():
        raw_targets = [match.group(1) for match in MARKDOWN_LINK.finditer(text)]
        raw_targets.extend(match.group(1) for match in MARKDOWN_CODE_PATH.finditer(text))
        for raw_target in raw_targets:
            target = _local_markdown_target(source, raw_target, tracked)
            if target is None:
                continue
            edge = (source, target)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1
            reference_counts[source] += 1
    for record in records:
        record["structural_markdown_reference_count"] = reference_counts.get(str(record["path"]))

    by_category: dict[str, dict[str, object]] = {}
    for category in sorted({str(record["category"]) for record in records}):
        by_category[category] = _metric_totals(
            [record for record in records if record["category"] == category]
        )

    bootstrap = [record for record in records if record["path"] in BOOTSTRAP_PATHS]
    missing_bootstrap = sorted(set(BOOTSTRAP_PATHS) - {str(item["path"]) for item in bootstrap})
    if missing_bootstrap:
        raise MeasurementError(f"missing tracked bootstrap files: {', '.join(missing_bootstrap)}")

    text_records = [record for record in records if record["text_encoding"] == "utf-8"]
    largest = sorted(text_records, key=lambda item: (-int(item["byte_size"]), str(item["path"])))
    content_identity = [{"path": record["path"], "sha256": record["sha256"]} for record in records]
    revision = _git(root, "rev-parse", "HEAD").decode("ascii").strip()
    return {
        "bootstrap_physical_footprint": {
            "description": "Physical UTF-8 footprint of source cold-start router files; no token or observed-load claim.",
            "files": bootstrap,
            "totals": _metric_totals(bootstrap),
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
        "source_git_revision": revision,
        "structural_markdown_references": {
            "description": "Static resolvable local Markdown links and code-span paths to tracked files; not observed RFO, TMC, CAR, or runtime loads.",
            "edge_count": len(edge_counts),
            "edges": [
                {"occurrences": count, "source": source, "target": target}
                for (source, target), count in sorted(edge_counts.items())
            ],
            "reference_count": sum(edge_counts.values()),
        },
        "totals": {"by_category": by_category, "repository": _metric_totals(records)},
        "tracked_content_digest": hashlib.sha256(canonical_json(content_identity)).hexdigest(),
    }


def _relative_output(root: Path, output: Path) -> str | None:
    try:
        return output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def write_report(root: Path, output: Path) -> dict[str, object]:
    excluded = {_relative} if (_relative := _relative_output(root, output)) else set()
    report = build_report(root, excluded_paths=excluded)
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(canonical_json(report))
    temporary.replace(output)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = (
            write_report(args.source_root, args.output)
            if args.output is not None
            else build_report(args.source_root)
        )
    except (MeasurementError, OSError, UnicodeError) as error:
        parser.exit(1, f"error: {error}\n")
    if args.output is None:
        print(canonical_json(report).decode("utf-8"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
