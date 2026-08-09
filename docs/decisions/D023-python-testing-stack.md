# D023 — Python testing stack

Status: ACCEPTED
Authority: Human Owner

## Decision

Repository-owned test and evaluation harness code for `agent-governance` SHALL use **Python** as the primary programming language.

The baseline testing stack is:

- **Python >= 3.13** as the minimum supported test runtime;
- **pytest 9.x** as the canonical deterministic test runner/framework;
- **Hypothesis 6.x** as the approved property/state-machine testing engine when D019 Layer 2 requires generated/stateful coverage;
- Python standard-library modules such as `pathlib`, `json`, `tempfile`, `subprocess`, `hashlib`, `dataclasses`, and related built-ins for ordinary repository/protocol checks before adding third-party dependencies;
- `python -m pytest` as the canonical framework-level invocation form.

The implementation SHOULD remain compatible with the current latest stable Python feature series in addition to the minimum runtime. At the time of this decision, Python 3.13 and 3.14 are both in bugfix support, while Python 3.12 is security-fixes-only.

## Dependency minimization

`pytest` is the only third-party dependency required by the first deterministic harness increment unless a later accepted task requires more.

Hypothesis is approved for property/state-machine work but MUST NOT be added to a simple deterministic task merely because it is part of the project testing stack. It becomes required only for task scope that actually exercises generated properties/state transitions where it adds material coverage.

Other libraries, including JSON Schema validators, coverage tools, hosted eval SDKs, security scanners, or model-provider SDKs, are NOT implicitly approved by this decision. They require a concrete need and the applicable later toolchain/task decision.

## Configuration direction

Python test configuration and development-only dependency declarations SHOULD converge on repository-root `pyproject.toml` using standardized/tool-native sections where supported:

- pytest native TOML configuration under `[tool.pytest]` for pytest 9.x;
- PEP 735 dependency groups for development-only test dependencies rather than making test dependencies runtime product dependencies.

The exact local environment manager/installer CLI and lock strategy are intentionally NOT decided here; those belong to the local development-toolchain decision.

## Why Python

The repository currently contains no implementation-language code and GitHub reports no detected language, so there is no existing application-language constraint to preserve.

Python fits the Governance verification surface particularly well:

1. the product is heavily filesystem/protocol oriented (`*.md`, JSON, JSONL, TOML, paths, digests, subprocess/tool traces), all of which are directly supported by the standard library;
2. pytest provides concise assertion reporting, test discovery, fixtures, parametrization, and per-test temporary paths useful for disposable synthetic repositories;
3. Hypothesis provides rule-based state machines that generate sequences of operations and check invariants after evolving state, directly matching lifecycle/STATE/EXCHANGE testing required by D019;
4. one language can cover deterministic tests, property/state-machine tests, fixture manipulation, CLI/subprocess verification, and later repository-owned eval orchestration without requiring a polyglot harness by default;
5. Python 3.13 provides a modern maintained baseline while retaining current ecosystem compatibility; Python 3.14 compatibility remains an expected target.

## Alternatives considered

### Node.js / TypeScript

Node has a stable built-in test runner and is a viable general testing platform. It is not selected as the primary stack because this repository has no JavaScript/TypeScript runtime surface requiring it, while adopting it would add a second ecosystem without improving the state-machine/property-testing fit that motivates Hypothesis.

### Go

Go has an excellent integrated `go test` toolchain and native fuzzing. It is not selected because the Governance product is not a Go binary/library and the current verification surface is file/protocol/state-model heavy; introducing compilation and a separate Go module would add machinery without a product-language benefit.

### Python `unittest` as primary runner

The standard library remains usable for isolated cases, and pytest can run unittest-style tests, but pytest is the canonical runner because its fixtures, parametrization, temporary-path support, and assertion introspection reduce harness boilerplate for synthetic repository testing.

## Version policy

- Do not pin to a single Python patch release in source contracts.
- Minimum language contract: `>=3.13`.
- Normal development/release verification SHOULD include the minimum supported series and the current latest stable series when the toolchain/CI implementation is defined.
- pytest compatibility line: `>=9,<10` until a deliberate major-version review changes it.
- Hypothesis compatibility line: `>=6,<7` until a deliberate major-version review changes it.
- Dependency resolution/lock files may pin concrete transitive versions for reproducibility once the local toolchain policy is defined.

## Canonical test style

- deterministic tests use pytest functions and plain `assert` by default;
- reusable setup uses fixtures rather than ad-hoc global mutable state;
- disposable repositories/files use `tmp_path`/`tmp_path_factory` and `pathlib.Path`;
- data-driven policy cases use pytest parametrization;
- stateful protocol models use `hypothesis.stateful.RuleBasedStateMachine` only where the state-space warrants it;
- fixtures that are fundamentally protocol data SHOULD remain data files (for example JSON/JSONL) rather than being encoded unnecessarily as Python source;
- subprocess/tool behavior is verified using controlled local subprocess execution and observable exit/output/filesystem results;
- network access remains excluded unless a specific later task explicitly authorizes it.

## Evaluation harness consequence

Repository-owned agent-eval harness code SHOULD also be Python unless a target adapter can only be exercised through unavoidable language-specific glue. Provider/model SDK selection is not part of this decision.

## External technical basis

Primary references used for this decision:

- Python active releases: https://www.python.org/downloads/
  - Python 3.13 and 3.14 are in bugfix support; 3.12 is security-fixes-only at decision time.
- pytest documentation: https://docs.pytest.org/en/stable/
  - assertion introspection, auto-discovery, fixtures, and Python 3.10+ support.
- pytest temporary paths: https://docs.pytest.org/en/stable/how-to/tmp_path.html
  - `tmp_path` provides a unique `pathlib.Path` temporary directory per test.
- pytest parametrization: https://docs.pytest.org/en/stable/how-to/parametrize.html
  - built-in parameterized test/fixture support.
- pytest configuration: https://docs.pytest.org/en/stable/reference/customize.html
  - pytest 9 supports native TOML configuration under `[tool.pytest]` in `pyproject.toml`.
- pytest invocation: https://docs.pytest.org/en/stable/how-to/usage.html
  - supports `python -m pytest` as an official invocation mode.
- Hypothesis stateful testing: https://hypothesis.readthedocs.io/en/latest/stateful.html
  - generates sequences of primitive actions and supports rule-based state machines/invariants.
- Hypothesis compatibility: https://hypothesis.readthedocs.io/en/latest/compatibility.html
  - current supported CPython/PyPy series and compatibility policy.
- Python Packaging dependency groups (PEP 735): https://packaging.python.org/en/latest/specifications/dependency-groups/
  - standardized development-only dependency groups suitable for testing.
- Python `pathlib`: https://docs.python.org/3.13/library/pathlib.html
- Python `json`: https://docs.python.org/3.13/library/json.html
- Python `subprocess`: https://docs.python.org/3.13/library/subprocess.html

## Consequences

- D019's generic reference to "standard Python test tooling" is now concretized by this decision.
- T001 may assume Python >=3.13 and pytest 9.x once its remaining readiness blockers are resolved.
- T001 SHOULD NOT add Hypothesis unless its actual first-increment scope expands to genuine stateful/property testing through an approved Task Contract revision.
- The next foundation decisions remain separate: required Skills/capabilities, local CLI/development toolchain, and SDD/Skill coexistence.
