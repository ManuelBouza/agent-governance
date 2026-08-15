# T021 — Consumer Profile Abstraction Zero Drift

## Identity

- Task ID: `T021`
- Status: `IN_PROGRESS`
- Type: `refactor`
- Base branch: `develop`
- Expected topic branch: `refactor/t021-consumer-profile-abstraction`
- Expected executor handoff: `handoffs/T021-executor-handoff.json`
- Readiness note: T020 is ACCEPTED/integrated and OP055 is DONE. D046/ICAE is the prospective assurance gate for T021+.
- Assurance-Class: `deterministic`
- Baseline: `T018 Consumer v1 characterization + accepted T020 artifact-isolation baseline`
- Verification-Planes: `static, deterministic, package`
- Release-Impact: `compatibility`
- Context-Impact: `none`

## Objective

Introduce an explicit runtime profile abstraction with `consumer` as the only active profile, without changing Consumer v1 behavior. This creates the profile boundary required for later source-maintainer support while remaining a behavior-preserving refactor.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
- `docs/AGENT-CAPABILITY-ENGINEERING.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- `docs/REFACTORING-WORKFLOW.md`
- `docs/GOVERNANCE-SKILL-CONTRACT.md`
- `docs/tasks/T018-consumer-v1-characterization-and-package-baseline.md`
- `docs/tasks/T020-self-contained-build-artifact-and-identity.md`

## Authorized scope

- Non-Markdown profile/runtime modules and routing code.
- Non-Markdown tests proving `consumer` profile behavior and isolation defaults.
- The thin launcher/build plumbing necessary to pass an explicit or resolved consumer profile.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Unrelated provider/model routing, host configuration, permissions, Gentle AI/Caveman integration, or release promotion.
- Direct writes to `develop` or `main`.
- Source-maintainer profile implementation.
- Changes to Skill Markdown activation/description.
- Changes to consumer CLI commands or repository footprint.
- RCAB repository-context tooling, document splitting, or context-budget enforcement.

## Invariants / constraints

- The T018 Consumer v1 characterization remains the behavioral baseline.
- The accepted T020 self-contained artifact boundary remains intact.
- `consumer` is an implementation profile, not a new normative authority.
- No profile default may grant source-maintenance permissions.
- The built artifact remains self-contained.
- This task changes no model-mediated Skill description/activation surface. Under ICAE, model evals are therefore not required for acceptance. If implementation requires changing such a surface, stop/escalate rather than expanding scope.

## Acceptance criteria

### AC-T021-1 — zero Consumer drift
Consumer behavior is identical with the profile abstraction enabled against the frozen T018 baseline.

### AC-T021-2 — fail-closed profile routing
Unsupported or ambiguous profile values are rejected rather than routed with broader permissions.

### AC-T021-3 — artifact compatibility
The accepted T020 artifact remains self-contained and all Consumer v1/artifact regression behavior passes.

## Verification requirements

- Run T018 characterization unchanged.
- Run focused profile routing/isolation tests, including negative controls for unsupported/ambiguous profile values.
- Run T020 artifact-isolation tests.
- Run the full deterministic suite.
- Run applicable static/Ruff/compile checks.

The handoff MUST map `AC-T021-1` through `AC-T021-3` to the exact verifier/test evidence that proves each criterion; green-suite summaries alone are not sufficient traceability.

## Stop / escalation conditions

- Profile abstraction requires changing the Consumer Skill contract or activation semantics.
- An ambiguous context would be routed with broader permissions rather than fail closed.
- The refactor requires weakening/changing T018 or T020 accepted baselines.
- Model-mediated behavior would need to change to complete the task.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T021-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized non-Markdown work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.

## Review / rework lifecycle

### T021-R1 — REWORK_REQUIRED

`docs/reviews/T021-R1.md` reviewed submitted executor HEAD `969e2130ca9abb27c6ae5ad830923582f45b8a2f` and found `AC-T021-2` incomplete.

The submitted `engine.main()` accepts directly constructed unsupported `Profile` instances because it validates only object type plus `grants_source_maintenance`, while the current `Profile` implementation returns `False` for that property regardless of unsupported `name`.

Rework authority is exclusively the unchanged Task Contract plus `docs/reviews/T021-R1.md`.

T021 rework is temporarily sequenced behind T032 because the canonical full deterministic suite is already red on clean `develop` due the unrelated RCAB generated-snapshot/live-currentness coupling recorded as L006. T021 MUST NOT absorb that RCAB repair into its scope.

After T032 is accepted/integrated and canonical full deterministic regression is green, T021 rework must re-bootstrap current `develop`, safely reconcile the existing T021 topic branch, implement only the T021-R1 fail-closed correction, rerun the complete verification matrix, finalize the handoff, and follow D048's publication boundary.
