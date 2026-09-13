#!/usr/bin/env python3
"""Deterministic qualification checks for T067 / R029 D082 materialization."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing YAML frontmatter")
    _, frontmatter, _ = text.split("---", 2)
    values: dict[str, str] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def add_check(checks: list[dict[str, Any]], name: str, ok: bool, detail: Any) -> None:
    checks.append({"name": name, "ok": bool(ok), "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.root.resolve()

    eval_dir = repo / "evals" / "r029_materialization"
    ledger = load_json(eval_dir / "preservation-ledger.json")
    corpus = load_json(eval_dir / "activation-corpus.json")
    profile = load_json(eval_dir / "qualification-profile.json")
    normative = load_json(eval_dir / "normative-rule-index.json")
    equivalence = load_json(eval_dir / "descriptor-equivalence.json")

    checks: list[dict[str, Any]] = []

    treatments = ledger["treatments"]
    expected = ledger["expected_counts"]
    flat_ids = treatments["ROOT"] + treatments["ROOT+ROUTE"] + treatments["ROUTE"]
    expected_ids = [f"S1-{number:03d}" for number in range(1, 80)]
    add_check(
        checks,
        "preservation-counts",
        len(treatments["ROOT"]) == expected["ROOT"]
        and len(treatments["ROOT+ROUTE"]) == expected["ROOT+ROUTE"]
        and len(treatments["ROUTE"]) == expected["ROUTE"]
        and len(flat_ids) == expected["TOTAL"],
        {key: len(value) for key, value in treatments.items()},
    )
    add_check(
        checks,
        "preservation-ids",
        sorted(flat_ids) == expected_ids and len(set(flat_ids)) == 79,
        sorted(flat_ids),
    )

    rooted_ids = set(treatments["ROOT"]) | set(treatments["ROOT+ROUTE"])
    family_ids = {item for values in ledger["root_families"].values() for item in values}
    add_check(
        checks,
        "root-family-coverage",
        rooted_ids <= family_ids,
        sorted(rooted_ids - family_ids),
    )

    routed_ids = set(treatments["ROOT+ROUTE"]) | set(treatments["ROUTE"])
    route_keys = set(ledger["route_destinations"])
    add_check(
        checks,
        "route-destination-coverage",
        routed_ids == route_keys,
        {
            "missing": sorted(routed_ids - route_keys),
            "unexpected": sorted(route_keys - routed_ids),
        },
    )
    missing_destinations: list[str] = []
    for item_id, destinations in ledger["route_destinations"].items():
        for relative in destinations:
            if not (repo / relative).exists():
                missing_destinations.append(f"{item_id}:{relative}")
    add_check(
        checks, "preservation-destinations-exist", not missing_destinations, missing_destinations
    )

    root_path = repo / profile["root_path"]
    root_text = root_path.read_text(encoding="utf-8")
    missing_markers = [
        marker for marker in profile["root_markers"] if f"({marker})" not in root_text
    ]
    add_check(checks, "root-family-markers", not missing_markers, missing_markers)
    missing_cold_start = [
        snippet for snippet in profile["cold_start_required_snippets"] if snippet not in root_text
    ]
    add_check(checks, "cold-start-root-contract", not missing_cold_start, missing_cold_start)

    maintainer = profile["maintainer"]
    maintainer_meta = parse_frontmatter(repo / maintainer["skill"])
    add_check(
        checks,
        "maintainer-top-level-name",
        maintainer_meta.get("name") == maintainer["name"],
        maintainer_meta,
    )
    missing_routes = [path for path in maintainer["routes"] if not (repo / path).is_file()]
    add_check(checks, "maintainer-internal-routes", not missing_routes, missing_routes)

    transverse_names: list[str] = []
    catalog_metadata_bytes: dict[str, int] = {}
    descriptor_failures: dict[str, list[str]] = {}
    all_skill_paths = [maintainer["skill"]]
    for skill in profile["transverse"]:
        all_skill_paths.append(skill["skill"])
        meta = parse_frontmatter(repo / skill["skill"])
        transverse_names.append(meta.get("name", ""))
    expected_transverse = [skill["name"] for skill in profile["transverse"]]
    add_check(
        checks,
        "exact-five-transverse",
        transverse_names == expected_transverse and len(transverse_names) == 5,
        transverse_names,
    )

    discovered_names: dict[str, str] = {}
    for path in repo.glob("*-skill/SKILL.md"):
        meta = parse_frontmatter(path)
        discovered_names[meta.get("name", "")] = path.relative_to(repo).as_posix()
    forbidden = profile["workspace_isolation"]["top_level_forbidden_name"]
    add_check(
        checks,
        "workspace-isolation-not-top-level",
        forbidden not in discovered_names,
        discovered_names.get(forbidden),
    )
    workspace_ref = repo / profile["workspace_isolation"]["reference"]
    add_check(checks, "workspace-isolation-reference", workspace_ref.is_file(), str(workspace_ref))

    for relative in all_skill_paths:
        meta = parse_frontmatter(repo / relative)
        name = meta.get("name", "")
        description = meta.get("description", "")
        raw = f"name:{name}\ndescription:{description}\n".encode()
        catalog_metadata_bytes[name] = len(raw)
        required_terms = profile["descriptor_required_terms"].get(name, [])
        missing = [term for term in required_terms if term not in description]
        if missing:
            descriptor_failures[name] = missing
    add_check(checks, "descriptor-contract", not descriptor_failures, descriptor_failures)

    allowed_routes = set(expected_transverse) | {"source-maintainer", "consumer-governance", None}
    corpus_errors: list[str] = []
    for case in corpus["cases"]:
        if case.get("expected_domain") not in allowed_routes:
            corpus_errors.append(f"{case['id']}:unexpected-domain")
        if case.get("expected_primary") not in allowed_routes:
            corpus_errors.append(f"{case['id']}:unexpected-primary")
        if case.get("expected_secondary") not in allowed_routes:
            corpus_errors.append(f"{case['id']}:unexpected-secondary")
        if case.get("expected_internal") not in {None, "workspace-isolation"}:
            corpus_errors.append(f"{case['id']}:unexpected-internal")
    add_check(checks, "activation-corpus-integrity", not corpus_errors, corpus_errors)

    rule_ids: list[str] = []
    missing_normative_paths: list[str] = []
    for rule in normative["rule_families"]:
        rule_ids.append(rule["id"])
        for relative in [rule["owner_path"], *rule.get("references", [])]:
            if not (repo / relative).exists():
                missing_normative_paths.append(f"{rule['id']}:{relative}")
    duplicate_rule_ids = sorted({item for item in rule_ids if rule_ids.count(item) > 1})
    add_check(checks, "normative-single-owner-index", not duplicate_rule_ids, duplicate_rule_ids)
    add_check(checks, "normative-index-paths", not missing_normative_paths, missing_normative_paths)

    add_check(
        checks,
        "descriptor-equivalence-disposition",
        equivalence["overall_disposition"] == "MATERIALLY_EQUIVALENT"
        and equivalence["fresh_36_codex_trials_required"] is False
        and equivalence["preserved_residuals"]["chatgpt_codex_empirical_parity"]
        == "NOT_ESTABLISHED",
        {
            "overall_disposition": equivalence["overall_disposition"],
            "fresh_36_codex_trials_required": equivalence["fresh_36_codex_trials_required"],
            "parity": equivalence["preserved_residuals"]["chatgpt_codex_empirical_parity"],
        },
    )

    conditional_loads: list[dict[str, Any]] = []
    missing_load_paths: list[str] = []
    for case in profile["representative_loads"]:
        total = 0
        for relative in case["paths"]:
            path = repo / relative
            if not path.is_file():
                missing_load_paths.append(f"{case['id']}:{relative}")
                continue
            total += len(path.read_bytes())
        conditional_loads.append(
            {
                "id": case["id"],
                "bytes": total,
                "reference_hops": case["reference_hops"],
                "paths": case["paths"],
            }
        )
    add_check(checks, "representative-load-paths", not missing_load_paths, missing_load_paths)

    root_bytes = len(root_path.read_bytes())
    result = {
        "schema_version": "1.0.0",
        "task": "T067",
        "status": "PASS" if all(check["ok"] for check in checks) else "FAIL",
        "checks": checks,
        "measurements": {
            "root_bytes": root_bytes,
            "baseline_root_bytes": profile["baseline_root_bytes"],
            "root_byte_delta": root_bytes - profile["baseline_root_bytes"],
            "catalog_metadata_bytes_by_skill": catalog_metadata_bytes,
            "initial_catalog_bytes": sum(catalog_metadata_bytes.values()),
            "representative_conditional_loads": conditional_loads,
            "reference_hop_depth_max": max(item["reference_hops"] for item in conditional_loads),
            "normative_rule_families": len(normative["rule_families"]),
            "normative_duplicate_owner_ids": duplicate_rule_ids,
        },
        "residuals": equivalence["preserved_residuals"],
        "provider_evidence": equivalence["evidence_reuse"],
    }

    serialized = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        output = args.output if args.output.is_absolute() else repo / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
