# T020 — Self Contained Build Artifact And Identity

## Identity

- Task ID: `T020`
- Status: `ACCEPTED`
- Type: `infrastructure`
- Base branch: `develop`
- Expected topic branch: `feat/t020-self-contained-governance-artifact`
- Expected executor handoff: `handoffs/T020-executor-handoff.json`
- Lifecycle note: T020 was remotely reviewed through T020-R1/T020-R2 and ACCEPTED at exact executor HEAD `0aad8ce78b52a4bd2a4851663d675048215a539c`. Integration is controlled by PR #127; any source-branch advancement before integration requires re-review. The post-T020 ICAE methodology gate remains mandatory before T021 becomes READY.

## Objective

Introduce a reproducible build/package boundary that produces a self-contained Governance Skill payload from canonical source. The built artifact must contain the Core snapshot, runtime, assets, and generated identity metadata needed for consumer bootstrap without reading the source repository.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/GOVERNANCE-SKILL-PACKAGE.md`
- `docs/RELEASES.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`
- `docs/tasks/T019-extract-shared-deterministic-engine.md`
- `handoffs/T019-executor-handoff.json`
- `src/agent_governance/engine.py`
- `tests/test_consumer_v1_characterization.py`
- `tests/test_shared_governance_engine.py`

## Authorized scope

- Non-Markdown build/packaging code and configuration.
- Generated-artifact manifest/identity schema or JSON metadata.
- Non-Markdown artifact-isolation tests and temporary-fixture helpers.
- Build-time copying of canonical `governance-core/` content into the artifact as generated output.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Hand-maintained duplicate Core source inside `governance-skill/`.
- Consumer profile semantic changes.
- Platform-specific public release promotion.
- Silent migration of an already-governed repository.

## Invariants / constraints

- Every runtime dependency required by the built Skill is inside the built artifact boundary.
- Generated Core content is traceable to the canonical source revision and is never a second editable authority.
- Generated metadata distinguishes product/Skill version, protocol version, installed-footprint version, source commit, build schema, and content digests where applicable.
- The existing consumer installed footprint remains semantically unchanged.
- The accepted T018/T019 behavior baseline remains unchanged while source-checkout lookup is replaced by artifact-local runtime resolution.

## Acceptance criteria

- A clean artifact can bootstrap and validate a clean unrelated repository when the Agent Governance source checkout is unavailable to execution.
- Normal Consumer v1 deterministic operations used by the current release gate work from the artifact-only environment.
- No runtime path traverses from the artifact to a source-tree sibling dependency.
- Repeated builds from the same source are reproducible at the defined identity level.

## Verification requirements

- Run focused packaging/build tests.
- Run artifact-only bootstrap/validate/operation tests with the source tree unavailable.
- Run all T018 characterization and consumer regression tests.
- Run the T019 shared-engine structural test.
- Verify generated metadata/digests against the source/build inputs.

## Stop / escalation conditions

- Self-containment would require copying source-only policy/state/history into the consumer artifact.
- Build identity cannot be made deterministic enough to support release evidence.
- Fixing packaging requires consumer behavior or protocol changes not authorized here.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T020-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
