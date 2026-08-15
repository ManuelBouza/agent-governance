# T029 — Unified Governance Release Readiness And Rollback Gate

## Identity

- Task ID: `T029`
- Status: `BLOCKED`
- Type: `release`
- Base branch: `develop`
- Expected topic branch: `test/t029-unified-governance-release-gate`
- Expected executor handoff: `handoffs/T029-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T024, T027, T028, MG3, and the accepted T026 decision outcome are complete.

## Objective

Execute the final non-Markdown release-readiness verification for the unified Governance Skill architecture and produce auditable evidence for ChatGPT release review. This task does not itself promote, tag, merge to `main`, or grant release approval.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/RELEASES.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`

## Authorized scope

- Non-Markdown release verification harness/fixtures/evidence needed to exercise the accepted architecture.
- Artifact build and isolated test outputs in appropriate non-authoritative locations.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Release promotion/tag creation/`main` mutation.
- Changing acceptance criteria in order to turn failures into passes.
- Deleting the pre-refactor Consumer v1 rollback evidence.

## Invariants / constraints

- All controlling Markdown gates through MG3 are integrated before final review.
- The outcome of the T025/T026 persistence decision is treated as authoritative: accepted migration is verified, or cancelled migration is not fabricated as a release requirement.
- The previous release-approved Consumer v1 identity remains available as rollback reference.
- Built artifact verification is first-class release evidence.

## Acceptance criteria

- Full deterministic regression passes at 100% per current policy.
- Profile activation/eval thresholds pass for the selected dispatcher/entrypoint packaging outcome.
- Artifact-only install/bootstrap/validate/normal operation and explicit upgrade/migration tests pass.
- Supported adapter/platform verification satisfies current release policy.
- Security/supply-chain/source-state-exclusion checks pass.
- Build identity/digests trace the candidate to its exact source revision.
- Rollback evidence identifies the immutable pre-refactor Consumer v1 baseline and demonstrates the new migration strategy does not destroy that recovery path.

## Verification requirements

- Run all required deterministic, property, profile/isolation, artifact, migration, and agent-facing eval suites.
- Persist structured test/eval evidence and exact source/artifact identities.
- Report failures individually; do not collapse agent-facing repeated trials into a single opaque result.

## Stop / escalation conditions

- Any controlling task or Markdown gate is not accepted/integrated.
- Any release criterion is ambiguous or would require a new product decision.
- The built artifact depends on source checkout/state or cannot be traced reproducibly.
- Rollback identity/evidence is missing.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T029-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
