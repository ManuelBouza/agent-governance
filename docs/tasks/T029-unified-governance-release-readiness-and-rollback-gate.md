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

Execute the final non-Markdown release-readiness verification for the accepted Agent Governance product architecture and T023-selected Skill activation topology, producing auditable evidence for ChatGPT release review.

The selected distribution may expose one or multiple generated Skill entrypoints, but it must remain one Agent Governance product/version over one canonical capability source, one Governance Core and one shared deterministic engine.

The final release candidate must also satisfy D051 end to end: **install Agent Governance once -> self-bootstrap a clean Consumer repository -> validate its durable project footprint -> perform applicable normal operations without source-checkout or manually installed supplemental Agent Governance payload**.

This task does not itself promote, tag, merge to `main`, or grant release approval.

## Controlling references

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/decisions/D044-unified-governance-skill-architecture.md`
- `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`
- `docs/decisions/D051-single-install-self-bootstrap-and-durable-project-footprint.md`
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`
- accepted T023 topology review/evidence
- accepted T024 projection/distribution review/evidence
- `docs/RELEASES.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`

## Authorized scope

- Non-Markdown release verification harness/fixtures/evidence needed to exercise the accepted architecture and selected topology.
- Artifact build and isolated test outputs in appropriate non-authoritative locations.
- Non-Markdown distribution/entrypoint identity and provenance verification evidence.
- Non-Markdown clean-install/self-bootstrap/upgrade fixtures and evidence required by D051.
- The executor handoff JSON.

## Explicit exclusions

- Committed Markdown (`*.md`) authoring, editing, deletion, or regeneration.
- Changes to `governance-core/` protocol semantics unless this Task Contract explicitly authorizes them.
- Changing the T023-selected topology or T024-accepted projection merely to make release checks pass.
- Introducing independently maintained Governance Skill sources/products or independent per-entrypoint versions.
- Making portable release correctness depend on Skill-to-Skill invocation or unapproved multi-agent architecture.
- Requiring users to manually install/copy a second Agent Governance Core/runtime/template/schema/Skill support payload after installing the release distribution.
- Requiring source-repository checkout access for normal Consumer bootstrap/operation from an already-installed release.
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
- If multiple Skill entrypoints are emitted, they share one Agent Governance distribution version and the same canonical capability-source/Core/engine provenance.
- Generated entrypoints remain routing/distribution projections, never independent normative authorities.
- Each supported Consumer release-target platform provides one Agent Governance installation unit/bundle for the complete selected topology.
- Bootstrap materializes durable project-owned Governance/state; that project footprint is not treated as an extra package installation.
- Source-maintainer overlays/history/state do not leak into an ordinary Consumer project footprint.

## Acceptance criteria

### AC-T029-1 — complete regression
Full deterministic regression passes at 100% per current policy, together with all required property/state-machine, profile/isolation and migration tests.

### AC-T029-2 — selected topology activation quality
The exact T023-selected dispatcher/entrypoint topology continues to meet its accepted activation/routing/isolation thresholds under final release-candidate evidence.

### AC-T029-3 — artifact operation and source independence
Artifact-only install/bootstrap/validate/normal operation and explicit upgrade/migration tests pass; Consumer-capable operation does not require the source checkout.

### AC-T029-4 — atomic one-product identity
For every emitted Skill entrypoint/wrapper, evidence proves the same:

- Agent Governance distribution version/identity;
- canonical capability-source epoch/identity;
- Governance Core identity;
- deterministic engine identity;
- exact source revision/build schema as required by current package policy.

No entrypoint is independently versioned or independently authoritative.

### AC-T029-5 — selected-topology package integrity
The release candidate contains exactly the accepted T023/T024 topology, with no missing/extra entrypoints, unreviewed capability repartition or wrapper-specific semantic fork.

### AC-T029-6 — adapter/platform and security assurance
Supported adapter/platform verification satisfies current release policy, and required security/supply-chain/source-state-exclusion checks pass.

### AC-T029-7 — rollback preserved
Rollback evidence identifies the immutable pre-refactor Consumer v1 baseline and demonstrates that the selected topology plus migration strategy do not destroy that recovery path.

### AC-T029-8 — D051 single-install self-bootstrap journey
For each supported Consumer release-target packaging path, clean-environment evidence proves:

1. one supported Agent Governance distribution installation action/bundle;
2. no manual second Agent Governance Core/runtime/template/schema/Skill support installation;
3. clean unrelated repository bootstrap with Agent Governance source checkout unavailable;
4. required reusable Agent Governance payload resolved from the installed distribution;
5. valid durable `.agent-governance/` / `.agent-coordination/` project footprint;
6. applicable normal Consumer operations succeed from installed distribution + project footprint;
7. source-maintainer overlays/history/state are absent from the ordinary Consumer footprint.

### AC-T029-9 — distribution update / project migration separation
Updating the installed Agent Governance distribution alone does not silently migrate an existing governed repository. Any project-footprint migration follows the accepted MG2/T027 explicit transactional lifecycle.

## Verification requirements

- Run all required deterministic, property, profile/isolation, selected-topology activation, artifact, migration and agent-facing eval suites.
- Rebuild the complete selected distribution topology from canonical source and verify deterministic identity/provenance.
- Verify all emitted entrypoints/wrappers share one distribution/Core/engine/capability identity set.
- Verify there is no independently editable normative/runtime source inside an emitted entrypoint.
- Execute the D051 clean single-install -> self-bootstrap -> durable-operation journey for every supported Consumer release-target packaging path.
- Verify no out-of-band Agent Governance support payload or source checkout is required after the distribution has been installed.
- Verify ordinary Consumer project footprint excludes source-maintenance overlays/history/state.
- Verify distribution-only update does not silently mutate governed project footprint; then exercise accepted explicit migration/rollback behavior separately.
- Persist structured test/eval evidence and exact source/artifact/entrypoint identities.
- Report failures individually; do not collapse agent-facing repeated trials or host/model cells into one opaque result.
- Map every acceptance criterion to exact evidence in the handoff.

## Stop / escalation conditions

- Any controlling task or Markdown gate is not accepted/integrated.
- Any release criterion is ambiguous or would require a new product decision.
- The built artifact depends on source checkout/state or cannot be traced reproducibly.
- Multiple emitted entrypoints cannot be proven to share one atomic product/version/provenance identity.
- Final built topology differs from T023/T024 acceptance evidence.
- A supported release-target platform requires manual installation of multiple independent Agent Governance components or missing product-owned support files contrary to D051.
- Distribution update and project-footprint migration cannot be kept semantically separate.
- Rollback identity/evidence is missing.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist `handoffs/T029-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, follow D048's normal-task publication boundary, commit/push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
