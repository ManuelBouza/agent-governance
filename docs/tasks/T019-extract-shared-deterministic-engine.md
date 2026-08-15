# T019 — Extract Shared Deterministic Engine

## Identity

- Task ID: `T019`
- Status: `ACCEPTED`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t019-shared-governance-engine`
- Expected executor handoff: `handoffs/T019-executor-handoff.json`
- Lifecycle note: T018 RF1 remained frozen throughout execution. T019 was remotely reviewed and accepted after RF5, then integrated through PR #122 at `e2525c54f4de5703b1614bc303346cb044e24a60`.

## Acceptance / lifecycle

- Submitted executor HEAD: `fd71070f4b3ed08826fdde99ad34d81916bec21e`.
- Implementation commit before handoff finalization: `f5032c30fe4f97b09e566deb3ef12af9e78e9e4f`.
- Execution base: `9148be3c11c85d2bc7e0c43e3e8e86f110b2682f`.
- Integration: PR #122, squash commit `e2525c54f4de5703b1614bc303346cb044e24a60`.
- Scope reviewed: `governance-skill/scripts/governance.py`, `src/agent_governance/__init__.py`, `src/agent_governance/engine.py`, `tests/test_shared_governance_engine.py`, and `handoffs/T019-executor-handoff.json` only.
- Structural result: the launcher is a thin compatibility shim; deterministic command implementations live in `src/agent_governance/engine.py` as the single editable engine implementation.
- Frozen baseline result: T018 characterization `2 passed`; Consumer v1 frozen baseline `77 passed`; combined affected suite `78 passed`; full deterministic suite `262 passed`; Ruff/format/py_compile/diff checks PASS; no network, dependency, configuration, Markdown, protocol, footprint, or CLI-surface drift.
- Diagnostic note: the first post-extraction RF1 run exposed three direct launcher-internal seams. The executor did not weaken or rewrite the frozen tests; thin forwarding restored compatibility and the unchanged RF1 suite passed completely.
- Deferred boundary: self-contained distribution and removal of source-checkout engine lookup are intentionally T020 scope, not a T019 defect.

## Objective

Extract the deterministic Consumer Governance implementation from the monolithic Skill launcher into a reusable engine while preserving all T018-characterized Consumer v1 behavior. `governance-skill/scripts/governance.py` must become a thin compatibility launcher/shim rather than a second implementation.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/tasks/T018-consumer-v1-characterization-and-package-baseline.md`
- `handoffs/T018-executor-handoff.json`
- `tests/test_consumer_v1_characterization.py`
- `governance-skill/scripts/governance.py`
- `pyproject.toml`

## Authorized scope

- Non-Markdown runtime modules under an appropriate source package such as `src/agent_governance/`.
- `governance-skill/scripts/governance.py` only as needed to become a thin launcher/shim.
- Non-Markdown tests/import plumbing required for behavior-preserving extraction.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Profile selection semantics.
- Self-contained distribution packaging or Core relocation.
- Changes to the seven-command CLI surface, output contract, installed footprint, or protocol version.

## Invariants / constraints

- T018 characterization is the RF1 frozen baseline.
- Accepted RF1 identity: T018 submitted HEAD `fe66bda778147648c30e3ed3c7c11c11f547ca00`, integrated through PR #120 at `85bdb75537eab98bf8b1bd1f603809a33ab23603`.
- The accepted baseline comprises the unchanged existing Consumer v1 CLI tests plus `tests/test_consumer_v1_characterization.py`; it must not be weakened, removed, or reinterpreted during T019 without explicit ChatGPT authorization.
- No duplicate editable implementation of the deterministic engine is introduced.
- The launcher remains usable from the current source/package layout.
- Consumer v1 observable behavior and exit semantics remain unchanged.

## Acceptance criteria

- Deterministic engine logic is imported/invoked from the shared source package rather than remaining duplicated in the launcher.
- All T018 characterization tests pass unchanged.
- Existing consumer CLI and full regression suites pass.
- No consumer footprint or protocol semantic drift is observed.

## Verification requirements

- Run T018 characterization unchanged.
- Run focused engine/CLI tests added or affected by extraction.
- Run the full deterministic regression suite.
- Include diff/evidence showing the launcher is thin and the shared engine is the single implementation.

## Stop / escalation conditions

- Any T018 observable behavior cannot be preserved without a product decision.
- The extraction requires editing normative Core Markdown or changing the stable CLI contract.
- Import/package mechanics would make current supported execution paths unusable.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T019-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
