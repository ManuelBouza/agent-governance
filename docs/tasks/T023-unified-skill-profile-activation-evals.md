# T023 — Unified Skill Profile Activation Evals

## Identity

- Task ID: `T023`
- Status: `BLOCKED`
- Type: `test/eval`
- Base branch: `develop`
- Expected topic branch: `test/t023-unified-skill-profile-evals`
- Expected executor handoff: `handoffs/T023-executor-handoff.json`
- Readiness note: Remains `BLOCKED` until T022 is ACCEPTED and MG1 is integrated into `develop`.

## Objective

Measure whether the ChatGPT-owned unified Skill dispatcher and profile references introduced by MG1 activate and route `consumer` versus `source-maintainer` reliably enough to replace the two-maintained-Skill design. Produce the evidence for either one dispatcher or the D044 thin-generated-entrypoint fallback.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `governance-skill/SKILL.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/MAINTAINER-SKILL-CONTRACT.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`

## Authorized scope

- Non-Markdown activation/eval corpora, fixtures, harnesses, and result evidence.
- Non-Markdown profile isolation tests and routing support if required by the already-integrated MG1 contract.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Editing `SKILL.md` or profile Markdown; MG1 is ChatGPT-owned.
- Creating a second independently maintained Skill source.
- Changing acceptance thresholds after observing results merely to force a preferred architecture.

## Invariants / constraints

- The eval design includes positive, negative, near-miss, and cross-profile cases.
- Consumer prompts must not acquire source-maintainer context or permissions.
- Source-maintainer prompts must not initialize consumer state or bypass source policy.
- A routing failure results in evidence/fallback selection, not ad hoc widening of permissions.

## Acceptance criteria

- Unified-dispatcher activation and profile selection meet the predeclared repository acceptance threshold, OR the evidence objectively triggers D044 fallback to thin generated entrypoints.
- Repeated trials are isolated and reported separately where agent-facing eval methodology requires repetition.
- Deterministic profile-isolation tests remain green.
- No second normative or runtime source is introduced in either outcome.

## Verification requirements

- Run the full new activation/profile eval corpus according to current agent-facing evaluation policy.
- Run deterministic profile-isolation and consumer regression tests.
- Persist raw/structured non-Markdown evidence required by the current eval policy.

## Stop / escalation conditions

- MG1 is not integrated into current `develop`.
- The eval harness cannot distinguish dispatcher quality from unrelated provider/network instability.
- A proposed fix would broaden source-maintainer authorization or duplicate canonical sources.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T023-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
