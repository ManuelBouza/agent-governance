#!/usr/bin/env python3
"""Deterministically materialize one frozen T066 benchmark variant.

This module is provider-free. It creates only the scheduled starter fixture; it never
creates a solution candidate or invokes a model/provider.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_pairs() -> list[dict[str, Any]]:
    index = _load_json(ROOT / "pairs.json")
    pairs: list[dict[str, Any]] = []
    for relative in index["pair_files"]:
        pairs.extend(_load_json(ROOT / relative)["pairs"])
    return pairs


def load_variant(variant_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    pairs = _load_pairs()
    oracles = _load_json(ROOT / "oracles.json")["variants"]
    for pair in pairs:
        for variant in pair["variants"]:
            if variant["variant_id"] == variant_id:
                return variant, oracles[variant_id]
    raise KeyError(f"unknown frozen variant: {variant_id}")


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _common_files(dest: Path) -> None:
    _write(dest / "src/benchpkg/__init__.py", '"""Synthetic T066 benchmark package."""\n')
    _write(
        dest / "pyproject.toml",
        """[project]\nname = \"t066-benchmark-fixture\"\nversion = \"0.0.0\"\nrequires-python = \">=3.13\"\n\n[tool.pytest.ini_options]\naddopts = [\"-q\", \"--strict-config\"]\ntestpaths = [\"tests\"]\npythonpath = [\"src\"]\n""",
    )


def _materialize_a(dest: Path, variant: dict[str, Any], oracle: dict[str, Any]) -> None:
    p = variant["parameters"]
    module = p["module"]
    function = p["function"]
    _write(
        dest / f"src/benchpkg/{module}.py",
        f'''"""Capacity helper for the {p["slug"]} fixture."""\n\n\ndef {function}(limit: int, used: int, reserved: int) -> int:\n    """Return available headroom while rejecting negative inputs."""\n    if min(limit, used, reserved) < 0:\n        raise ValueError("capacity inputs must be non-negative")\n    # Frozen starter defect: reserved capacity is not yet subtracted.\n    return max(limit - used, 0)\n''',
    )
    cases = {case["id"]: case for case in oracle["cases"]}
    normal = cases["normal"]
    clamp = cases["clamp"]
    negative = cases["negative"]
    _write(
        dest / "tests/test_acceptance.py",
        f'''import pytest\n\nfrom benchpkg.{module} import {function}\n\n\ndef test_normal_headroom() -> None:\n    assert {function}(*{normal["args"]!r}) == {normal["expected"]!r}\n\n\ndef test_clamps_at_zero() -> None:\n    assert {function}(*{clamp["args"]!r}) == {clamp["expected"]!r}\n\n\ndef test_negative_input_is_rejected() -> None:\n    with pytest.raises(ValueError):\n        {function}(*{negative["args"]!r})\n''',
    )


def _materialize_b(dest: Path, variant: dict[str, Any], oracle: dict[str, Any]) -> None:
    p = variant["parameters"]
    old_key = p["old_key"]
    new_key = p["new_key"]
    value = p["value"]
    module = p["module"]
    accessor = p["accessor"]
    validator = p["validator"]
    _write(dest / "config/defaults.json", json.dumps({old_key: value}, indent=2, sort_keys=True) + "\n")
    _write(
        dest / f"src/benchpkg/{module}.py",
        f'''"""Settings helper for the {p["slug"]} fixture."""\n\nfrom typing import Any\n\n\ndef {accessor}(config: dict[str, Any]) -> int:\n    return int(config["{old_key}"])\n\n\ndef {validator}(config: dict[str, Any]) -> None:\n    if "{old_key}" not in config:\n        raise ValueError("missing {old_key}")\n    if not isinstance(config["{old_key}"], int):\n        raise ValueError("{old_key} must be an integer")\n''',
    )
    _write(
        dest / "src/benchpkg/render.py",
        '''"""Public rendering preserved by archetype B."""\n\n\ndef render_ceiling(value: int) -> str:\n    return f"ceiling={value}"\n''',
    )
    cases = {case["id"]: case for case in oracle["cases"]}
    _write(
        dest / "tests/test_acceptance.py",
        f'''import json\nfrom pathlib import Path\n\nimport pytest\n\nfrom benchpkg.{module} import {accessor}, {validator}\nfrom benchpkg.render import render_ceiling\n\nROOT = Path(__file__).resolve().parents[1]\n\n\ndef test_frozen_default_uses_new_key() -> None:\n    config = json.loads((ROOT / "config/defaults.json").read_text(encoding="utf-8"))\n    assert config == {{{new_key!r}: {value!r}}}\n\n\ndef test_accessor_reads_new_key() -> None:\n    config = {cases["new-key"]["config"]!r}\n    {validator}(config)\n    assert {accessor}(config) == {cases["new-key"]["expected"]!r}\n\n\ndef test_legacy_key_is_rejected() -> None:\n    with pytest.raises(ValueError):\n        {validator}({cases["legacy-rejected"]["config"]!r})\n\n\ndef test_public_rendering_is_preserved() -> None:\n    config = {cases["render"]["config"]!r}\n    assert render_ceiling({accessor}(config)) == {cases["render"]["expected"]!r}\n''',
    )


def _materialize_c(dest: Path, variant: dict[str, Any], oracle: dict[str, Any]) -> None:
    p = variant["parameters"]
    formatter = p["formatter"]
    module = p["module"]
    option = p["option"]
    _write(
        dest / "src/benchpkg/service.py",
        f'''"""Rendering service for the {p["slug"]} fixture."""\n\n\ndef {formatter}(items: list[str]) -> str:\n    return ",".join(items)\n''',
    )
    _write(
        dest / f"src/benchpkg/{module}.py",
        f'''"""CLI for the {p["slug"]} fixture."""\n\nimport sys\n\nfrom benchpkg.service import {formatter}\n\n\ndef main(argv: list[str] | None = None) -> int:\n    args = list(sys.argv[1:] if argv is None else argv)\n    print({formatter}(args))\n    return 0\n\n\nif __name__ == "__main__":\n    raise SystemExit(main())\n''',
    )
    cases = {case["id"]: case for case in oracle["cases"]}
    sample = p["sample"]
    _write(
        dest / "tests/test_acceptance.py",
        f'''import os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom benchpkg.service import {formatter}\n\nROOT = Path(__file__).resolve().parents[1]\n\n\ndef _env() -> dict[str, str]:\n    env = os.environ.copy()\n    previous = env.get("PYTHONPATH", "")\n    env["PYTHONPATH"] = str(ROOT / "src") + (os.pathsep + previous if previous else "")\n    return env\n\n\ndef test_service_preserves_default_behavior() -> None:\n    assert {formatter}({sample!r}) == {cases["no-option"]["stdout"]!r}\n\n\ndef test_service_accepts_prefix() -> None:\n    assert {formatter}({sample!r}, {p["prefix"]!r}) == {cases["prefix"]["stdout"]!r}\n\n\ndef test_cli_prefix_option() -> None:\n    proc = subprocess.run(\n        [sys.executable, "-m", "benchpkg.{module}", {option!r}, {p["prefix"]!r}, *{sample!r}],\n        check=False,\n        capture_output=True,\n        text=True,\n        cwd=ROOT,\n        env=_env(),\n    )\n    assert proc.returncode == 0\n    assert proc.stdout.strip() == {cases["prefix"]["stdout"]!r}\n\n\ndef test_missing_option_value_is_usage_error_without_traceback() -> None:\n    proc = subprocess.run(\n        [sys.executable, "-m", "benchpkg.{module}", {option!r}],\n        check=False,\n        capture_output=True,\n        text=True,\n        cwd=ROOT,\n        env=_env(),\n    )\n    assert proc.returncode == {cases["missing-value"]["exit_code"]!r}\n    assert "Traceback" not in proc.stderr\n''',
    )


def materialize(variant_id: str, destination: Path, *, replace: bool = False) -> Path:
    variant, oracle = load_variant(variant_id)
    if destination.exists():
        if not replace:
            raise FileExistsError(f"destination already exists: {destination}")
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    _common_files(destination)
    archetype = oracle["archetype"]
    if archetype == "A":
        _materialize_a(destination, variant, oracle)
    elif archetype == "B":
        _materialize_b(destination, variant, oracle)
    elif archetype == "C":
        _materialize_c(destination, variant, oracle)
    else:
        raise ValueError(f"unsupported archetype: {archetype}")
    _write(destination / ".t066-variant.json", json.dumps(variant, indent=2, sort_keys=True) + "\n")
    _write(destination / ".t066-oracle.json", json.dumps(oracle, indent=2, sort_keys=True) + "\n")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("variant_id")
    parser.add_argument("destination", type=Path)
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    materialize(args.variant_id, args.destination, replace=args.replace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
