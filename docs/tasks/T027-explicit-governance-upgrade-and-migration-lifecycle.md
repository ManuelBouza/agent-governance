# T027 — Explicit Governance Upgrade And Migration Lifecycle

## Identity

- Task ID: `T027`
- Status: `BLOCKED`
- Type: `feature`
- Base branch: `develop`
- Expected topic branch: `feat/t027-governance-upgrade-lifecycle`
- Expected executor handoff: `handoffs/T027-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T020 and T023 are ACCEPTED and MG2 is integrated into `develop`.

## Objective

Implement an explicit, transactional governed-repository upgrade/migration lifecycle that separates distribution updates from installed Governance protocol/footprint changes. The implementation must follow the ChatGPT-owned MG2 contract revision and must never silently migrate a governed repository.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/RELEASES.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`
- `governance-skill/SKILL.md`
- `docs/MIGRATION.md`

## Authorized scope

- Non-Markdown deterministic upgrade planning/apply/validation/rollback runtime.
- Non-authoritative installed-version/digest metadata in a non-Markdown format.
- Non-Markdown migration fixtures/tests covering supported prior footprint(s).
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Changing the CLI contract before MG2 is integrated.
- Automatic mutation of `.agent-governance/` or `.agent-coordination/` merely because the installed Skill/wrapper version changed.
- Unbounded migration support for undocumented historical versions.

## Invariants / constraints

- Distribution version, protocol version, and installed-footprint version remain separate concepts.
- Upgrade application requires explicit authorization after a deterministic plan.
- Migration must be transactional or provide equivalent rollback safety.
- Governance acceptance authority remains unchanged.

## Acceptance criteria

- The MG2-defined upgrade interface can report current/target versions, affected footprint, migration path, compatibility risks, and rollback plan before mutation.
- Apply performs only an explicitly planned/authorized migration and validates post-state.
- Rollback or recovery behavior is tested for interrupted/failed migration.
- Installing/updating the Skill/wrapper alone does not change governed repository state.

## Verification requirements

- Run focused upgrade plan/apply/rollback tests.
- Run migration fixtures from each version/footprint declared supported by MG2.
- Run consumer regression, artifact-isolation, and full deterministic suites.

## Stop / escalation conditions

- MG2 is not integrated.
- The migration path requires silent destructive overwrite of human/project state.
- A prior footprint cannot be migrated safely without a new product decision.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T027-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
