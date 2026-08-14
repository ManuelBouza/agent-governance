"""Deterministic mechanical validator for Consumer Governance trigger corpus."""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

ROOT_KEYS = {"schema_version", "authority_policy", "cases"}
CASE_KEYS = {
    "id",
    "partition",
    "category",
    "expected_activation",
    "surface_tags",
    "synthetic",
    "source_independent",
    "prompt",
    "coexistence",
}
COEXISTENCE_KEYS = {
    "shape",
    "existing_capabilities",
    "managed_surfaces",
    "governance_overlap",
    "expected_behaviors",
}
PARTITIONS = {"train", "validation"}
CATEGORIES = {"positive", "negative", "near_miss"}
EXPECTED_CASES_PER_SLOT = 6
SHAPES = {"gentle_ai_like", "spec_kit_like", "openspec_like", "custom_sdd", "no_sdd"}
BEHAVIORS = {
    "reuse_existing_capabilities",
    "adapt_existing_capabilities",
    "preserve_managed_surfaces",
    "refuse_unsolicited_sdd",
    "fail_closed_conflict",
}
POSITIVE_OPERATION_TAGS = {
    "bootstrap_install",
    "validate_reconstruct",
    "mission_state_event_handoff",
    "coexistence_inspection",
    "governance_skill_discovery_audit",
    "sequential_disclosure_readiness",
}
NEGATIVE_OPERATION_TAGS = {
    "generic_planning",
    "generic_coding",
    "generic_testing",
    "generic_refactoring",
    "generic_release",
    "generic_sdd",
    "generic_skill_install_search",
    "source_product_maintenance",
    "ordinary_application_implementation",
}
NEAR_MISS_TAGS = {
    "generic_spec_plan_tasks",
    "governed_repo_feature_test",
    "generic_skill_install",
    "maintainer_only",
    "existing_sdd_continuation",
    "equivalent_governance_overlap",
    "generic_registry_lookup",
}
CROSS_CUTTING_TAGS = {
    "consumer_vs_maintainer",
    "source_independence",
}
COEXISTENCE_TAGS = SHAPES | {
    "managed_preservation",
    "managed_conflict",
    "no_unsolicited_sdd",
}
ALLOWED_TAGS = (
    POSITIVE_OPERATION_TAGS
    | NEGATIVE_OPERATION_TAGS
    | NEAR_MISS_TAGS
    | CROSS_CUTTING_TAGS
    | COEXISTENCE_TAGS
)
ALLOWED_TAGS_BY_CATEGORY = {
    "positive": POSITIVE_OPERATION_TAGS | {"source_independence"} | COEXISTENCE_TAGS,
    "negative": NEGATIVE_OPERATION_TAGS | {"consumer_vs_maintainer"},
    "near_miss": NEAR_MISS_TAGS | {"consumer_vs_maintainer"} | COEXISTENCE_TAGS,
}
REQUIRED_TAG_PLACEMENTS = {
    "consumer_vs_maintainer": {
        ("validation", "negative"),
        ("train", "near_miss"),
        ("validation", "near_miss"),
    },
    "source_independence": {("train", "positive"), ("validation", "positive")},
}
ID_PATTERN = re.compile(r"cg-(?:pos|neg|near)-(?:train|validation)-\d{3}")
SOURCE_COUPLING_PATTERN = re.compile(
    r"(?:/home/|/Users/|(?:^|[\s'\"`])\.\.?[/\\]|"
    r"(?:^|[\s'\"`/\\])(?:governance-core|governance-skill|maintainer-skill)(?:[\s'\"`/\\.]|$)|"
    r"(?:^|[\s'\"`/\\])docs[/\\]tasks(?:[\s'\"`/\\.]|$))",
    re.IGNORECASE,
)


class CorpusError(ValueError):
    """Corpus violates one or more deterministic integrity rules."""


def _exact_keys(value: dict[str, Any], expected: set[str], location: str) -> list[str]:
    errors = []
    if missing := expected - value.keys():
        errors.append(f"{location}: missing keys {sorted(missing)}")
    if unknown := value.keys() - expected:
        errors.append(f"{location}: unknown keys {sorted(unknown)}")
    return errors


def _string_list(value: Any, location: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or (not value and not allow_empty):
        return [f"{location}: expected {'possibly empty ' if allow_empty else 'non-empty '}list"]
    if any(not isinstance(item, str) or not item.strip() for item in value):
        return [f"{location}: entries must be non-empty strings"]
    if len(value) != len(set(value)):
        return [f"{location}: duplicate entries"]
    return []


def _normalize_text(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", normalized))


def _content_fingerprint(case: dict[str, Any]) -> str:
    content = {
        "prompt": _normalize_text(case["prompt"]),
        "surface_tags": sorted(case["surface_tags"]),
        "coexistence": case["coexistence"],
    }
    return json.dumps(content, sort_keys=True, separators=(",", ":"))


def _validate_coexistence(value: Any, location: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, dict):
        return [f"{location}: expected object or null"]
    errors = _exact_keys(value, COEXISTENCE_KEYS, location)
    if errors:
        return errors
    if not isinstance(value["shape"], str) or value["shape"] not in SHAPES:
        errors.append(f"{location}.shape: invalid value")
    errors.extend(
        _string_list(
            value["existing_capabilities"], f"{location}.existing_capabilities", allow_empty=True
        )
    )
    errors.extend(
        _string_list(value["managed_surfaces"], f"{location}.managed_surfaces", allow_empty=True)
    )
    errors.extend(_string_list(value["expected_behaviors"], f"{location}.expected_behaviors"))
    expected_behaviors = value["expected_behaviors"]
    managed_surfaces = value["managed_surfaces"]
    behaviors_valid = isinstance(expected_behaviors, list) and all(
        isinstance(behavior, str) for behavior in expected_behaviors
    )
    if behaviors_valid and any(
        not isinstance(behavior, str) or behavior not in BEHAVIORS
        for behavior in expected_behaviors
    ):
        errors.append(f"{location}.expected_behaviors: invalid value")
    if type(value["governance_overlap"]) is not bool:
        errors.append(f"{location}.governance_overlap: expected boolean")
    elif (
        value["governance_overlap"]
        and behaviors_valid
        and "fail_closed_conflict" not in expected_behaviors
    ):
        errors.append(f"{location}: overlap must fail closed")
    if (
        isinstance(managed_surfaces, list)
        and managed_surfaces
        and behaviors_valid
        and "preserve_managed_surfaces" not in expected_behaviors
    ):
        errors.append(f"{location}: managed surfaces must be preserved")
    if value["shape"] == "no_sdd" and expected_behaviors != ["refuse_unsolicited_sdd"]:
        errors.append(f"{location}: no_sdd must refuse unsolicited SDD only")
    return errors


def validate_corpus(data: Any) -> dict[str, Any]:
    """Validate exact corpus schema and return deterministic counts."""
    if not isinstance(data, dict):
        raise CorpusError("root: expected object")
    errors = _exact_keys(data, ROOT_KEYS, "root")
    if errors:
        raise CorpusError("\n".join(errors))
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        errors.append("root.schema_version: expected integer 1")
    if data["authority_policy"] != "observed_project_facts_only":
        errors.append("root.authority_policy: vendor defaults cannot be authority")
    cases = data["cases"]
    if not isinstance(cases, list) or not cases:
        errors.append("root.cases: expected non-empty list")
        raise CorpusError("\n".join(errors))

    ids: set[str] = set()
    prompts: set[str] = set()
    contents: set[str] = set()
    tags: set[str] = set()
    tag_placements: dict[str, set[tuple[str, str]]] = {tag: set() for tag in CROSS_CUTTING_TAGS}
    shapes: set[str] = set()
    behaviors: set[str] = set()
    counts: Counter[tuple[str, str]] = Counter()

    for index, case in enumerate(cases):
        location = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{location}: expected object")
            continue
        case_key_errors = _exact_keys(case, CASE_KEYS, location)
        errors.extend(case_key_errors)
        if case_key_errors:
            continue
        case_id = case["id"]
        if not isinstance(case_id, str) or ID_PATTERN.fullmatch(case_id) is None:
            errors.append(f"{location}.id: invalid stable ID")
        elif case_id in ids:
            errors.append(f"{location}.id: duplicate {case_id}")
        else:
            ids.add(case_id)
        partition = case["partition"]
        category = case["category"]
        partition_valid = isinstance(partition, str) and partition in PARTITIONS
        category_valid = isinstance(category, str) and category in CATEGORIES
        if not partition_valid:
            errors.append(f"{location}.partition: invalid value")
        if not category_valid:
            errors.append(f"{location}.category: invalid value")
        if partition_valid and category_valid:
            counts[(partition, category)] += 1
            id_parts = case_id.split("-") if isinstance(case_id, str) else []
            expected_id_parts = (
                "pos" if category == "positive" else "near" if category == "near_miss" else "neg",
                partition,
            )
            if len(id_parts) >= 4 and tuple(id_parts[1:3]) != expected_id_parts:
                errors.append(f"{location}.id: category/partition mismatch")
        expected = category == "positive"
        if type(case["expected_activation"]) is not bool or case["expected_activation"] != expected:
            errors.append(f"{location}.expected_activation: must be {expected}")
        case_tags = case["surface_tags"]
        errors.extend(_string_list(case_tags, f"{location}.surface_tags"))
        tags_valid = isinstance(case_tags, list) and all(isinstance(tag, str) for tag in case_tags)
        if tags_valid:
            tags.update(case_tags)
            if unknown_tags := set(case_tags) - ALLOWED_TAGS:
                errors.append(f"{location}.surface_tags: unknown tags {sorted(unknown_tags)}")
            if category_valid:
                if misplaced_tags := set(case_tags) - ALLOWED_TAGS_BY_CATEGORY[category]:
                    errors.append(
                        f"{location}.surface_tags: tags misplaced for {category} {sorted(misplaced_tags)}"
                    )
                category_tags = {
                    "positive": POSITIVE_OPERATION_TAGS,
                    "negative": NEGATIVE_OPERATION_TAGS,
                    "near_miss": NEAR_MISS_TAGS,
                }[category]
                if not set(case_tags) & category_tags:
                    errors.append(f"{location}.surface_tags: missing {category} operation tag")
            if partition_valid and category_valid:
                for tag in CROSS_CUTTING_TAGS & set(case_tags):
                    tag_placements[tag].add((partition, category))
        if case["synthetic"] is not True or case["source_independent"] is not True:
            errors.append(f"{location}: synthetic and source_independent must be true")
        prompt = case["prompt"]
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"{location}.prompt: expected non-empty string")
        else:
            normalized_prompt = _normalize_text(prompt)
            if normalized_prompt in prompts:
                errors.append(f"{location}.prompt: duplicate normalized prompt")
            prompts.add(normalized_prompt)
        errors.extend(_validate_coexistence(case["coexistence"], f"{location}.coexistence"))
        if isinstance(case["coexistence"], dict):
            shape = case["coexistence"].get("shape")
            expected_behaviors = case["coexistence"].get("expected_behaviors")
            if isinstance(shape, str):
                shapes.add(shape)
            if isinstance(expected_behaviors, list):
                behaviors.update(
                    behavior for behavior in expected_behaviors if isinstance(behavior, str)
                )
            if tags_valid and isinstance(shape, str) and shape not in case_tags:
                errors.append(
                    f"{location}.surface_tags: coexistence shape {shape} must be explicit"
                )
            behavior_tags = {
                "preserve_managed_surfaces": "managed_preservation",
                "fail_closed_conflict": "managed_conflict",
                "refuse_unsolicited_sdd": "no_unsolicited_sdd",
            }
            if tags_valid and isinstance(expected_behaviors, list):
                required_behavior_tags = {
                    tag for behavior, tag in behavior_tags.items() if behavior in expected_behaviors
                }
                present_behavior_tags = set(case_tags) & set(behavior_tags.values())
                if present_behavior_tags != required_behavior_tags:
                    errors.append(
                        f"{location}.surface_tags: coexistence behaviors must map explicitly"
                    )
        elif tags_valid and set(case_tags) & COEXISTENCE_TAGS:
            errors.append(f"{location}.surface_tags: coexistence tags require coexistence case")
        if isinstance(prompt, str) and tags_valid:
            fingerprint = _content_fingerprint(case)
            if fingerprint in contents:
                errors.append(f"{location}: duplicate normalized content")
            contents.add(fingerprint)
        serialized = json.dumps(case, sort_keys=True)
        if SOURCE_COUPLING_PATTERN.search(serialized):
            errors.append(f"{location}: source checkout path dependency forbidden")

    for partition in PARTITIONS:
        for category in CATEGORIES:
            if counts[(partition, category)] != EXPECTED_CASES_PER_SLOT:
                errors.append(
                    f"coverage: expected {EXPECTED_CASES_PER_SLOT} cases for "
                    f"{partition}/{category}, got {counts[(partition, category)]}"
                )
    if missing_tags := ALLOWED_TAGS - tags:
        errors.append(f"coverage: missing surface tags {sorted(missing_tags)}")
    for tag, required in REQUIRED_TAG_PLACEMENTS.items():
        if tag_placements[tag] != required:
            errors.append(
                f"coverage: {tag} placements must be {sorted(required)}, "
                f"got {sorted(tag_placements[tag])}"
            )
    if missing_shapes := SHAPES - shapes:
        errors.append(f"coverage: missing coexistence shapes {sorted(missing_shapes)}")
    if missing_behaviors := BEHAVIORS - behaviors:
        errors.append(f"coverage: missing coexistence behaviors {sorted(missing_behaviors)}")
    if errors:
        raise CorpusError("\n".join(errors))

    return {
        "status": "pass",
        "schema_version": 1,
        "total_cases": len(cases),
        "counts": {
            partition: {category: counts[(partition, category)] for category in sorted(CATEGORIES)}
            for partition in sorted(PARTITIONS)
        },
    }


def load_and_validate(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise CorpusError(f"unable to load corpus: {exc}") from exc
    return validate_corpus(data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corpus", type=Path, default=Path(__file__).with_name("corpus.json"))
    args = parser.parse_args(argv)
    try:
        report = load_and_validate(args.corpus)
    except CorpusError as exc:
        print(json.dumps({"status": "fail", "errors": str(exc).splitlines()}, sort_keys=True))
        return 1
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
