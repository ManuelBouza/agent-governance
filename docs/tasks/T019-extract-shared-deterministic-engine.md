# T019 — Extract Shared Deterministic Engine

## Identity

- Task ID: `T019`
- Status: `BLOCKED`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t019-shared-governance-engine`
- Expected executor handoff: `handoffs/T019-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T018 is ACCEPTED and ChatGPT freezes its characterization baseline.

## Objective

Extract the deterministic Consumer Governance implementation from the monolithic Skill launcher into a reusable engine while preserving all T018-characterized Consumer v1 behavior. `governance-skill/scripts/governance.py` must become a thin compatibility launcher/shim rather than a second implementation.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/REFACTORING-WORKFLOW.md`
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
