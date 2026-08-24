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

Preserve D051: Agent Governance remains one installed product/distribution even when the selected topology exposes multiple generated Skill entrypoints. Updating that distribution must not turn into independent per-entrypoint updates or require manual supplemental Agent Governance payload installation.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D051-single-install-self-bootstrap-and-durable-project-footprint.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/RELEASES.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`
- `governance-skill/SKILL.md`
- `docs/MIGRATION.md`

## Authorized scope

- Non-Markdown deterministic upgrade planning/apply/validation/rollback runtime.
- Non-authoritative installed-version/digest metadata in a non-Markdown format.
- Non-Markdown migration fixtures/tests covering supported prior footprint(s).
- Non-Markdown distribution-update compatibility checks needed to preserve D051 one-product identity.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Changing the CLI contract before MG2 is integrated.
- Automatic mutation of `.agent-governance/` or `.agent-coordination/` merely because the installed Skill/wrapper/distribution version changed.
- Unbounded migration support for undocumented historical versions.
- Independent upgrade/version lifecycles for generated Agent Governance entrypoints.
- A migration flow that requires users to manually fetch/copy/install a second Agent Governance Core/runtime/template/schema/support payload outside the installed distribution.

## Invariants / constraints

- Distribution version, protocol version, and installed-footprint version remain separate concepts.
- The selected topology is upgraded as one Agent Governance distribution/product identity.
- Distribution replacement/update may change the installed reusable product package, but it does not silently mutate governed repository state.
- Project-footprint migration requires explicit authorization after a deterministic plan.
- Migration must be transactional or provide equivalent rollback safety.
- All Agent-Governance-owned reusable migration/runtime/template assets needed for a supported migration path are available through the installed target distribution; normal migration does not depend on a floating source checkout.
- Governance acceptance authority remains unchanged.

## Acceptance criteria

### AC-T027-1 — deterministic migration plan
The MG2-defined upgrade interface can report current/target versions, affected footprint, migration path, compatibility risks and rollback plan before mutation.

### AC-T027-2 — explicit transactional apply
Apply performs only an explicitly planned/authorized migration and validates post-state.

### AC-T027-3 — recovery/rollback
Rollback or recovery behavior is tested for interrupted/failed migration.

### AC-T027-4 — distribution update does not silently migrate project state
Installing/updating the Agent Governance distribution alone does not change `.agent-governance/` or `.agent-coordination/` state.

### AC-T027-5 — one-product upgrade identity
If the selected topology contains multiple generated entrypoints, they update under one Agent Governance distribution identity/version; the upgrade path does not independently version or partially update those product entrypoints.

### AC-T027-6 — no supplemental product install
Supported upgrade/migration can execute from the installed target Agent Governance distribution plus the governed project's durable state without requiring manual installation of out-of-band Agent Governance support files or source-repository access.

## Verification requirements

- Run focused upgrade plan/apply/rollback tests.
- Run migration fixtures from each version/footprint declared supported by MG2.
- Verify distribution-only update leaves governed project footprint unchanged until explicit migration authorization.
- Verify multi-entrypoint topology, if selected, remains one distribution/version through update.
- Verify supported migration fixtures do not require separately installed Agent Governance support payload or source checkout.
- Run consumer regression, artifact-isolation, and full deterministic suites.
- Map every acceptance criterion to exact evidence in the handoff.

## Stop / escalation conditions

- MG2 is not integrated.
- The migration path requires silent destructive overwrite of human/project state.
- A prior footprint cannot be migrated safely without a new product decision.
- The selected topology cannot be updated atomically as one Agent Governance product identity.
- A supported migration intrinsically requires a separately distributed/manual Agent Governance support component contrary to D051.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist `handoffs/T027-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
