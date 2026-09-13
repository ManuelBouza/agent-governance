# R029-S4 — `repository-change-control` Candidate Evaluation

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S4 — repository-change-control candidate`  
Baseline-Develop: `808f2fa601c7f141139dde23279ef2c4811d1466`  
Inputs: `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`, `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md`, `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md`, `docs/BRANCHING.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `KEEP_CANDIDATE`

## Purpose

Evaluate whether `repository-change-control` has a reusable, non-overlapping semantic intent strong enough to remain a transverse Skill candidate. This is an analytical disposition only. It does not authorize Skill creation, packaging, root `AGENTS.md` changes, or adoption of this architecture.

S4 intentionally does not decide the final placement of workspace isolation. S9 owns that question.

## Reusable semantic intent

The reusable intent is:

> Prepare and carry out a repository mutation through an authorized change path while preserving protected-target safety, reviewability, durable provenance, and repository-local policy.

This intent survives removal of Agent Governance-specific branch names, SDD stages, Task Contract vocabulary, decision IDs, toolchain choices, and release semantics.

The capability is not “use Git” or “create a branch.” It is repository change control: resolve the repository's authoritative mutation policy, establish the correct base and target relationship, use a bounded reviewable change path, and verify the resulting durable state without granting new authority.

## Positive triggers

The candidate should be considered when a task requires one or more of the following:

- create or modify tracked repository content under a branch/PR policy;
- determine the permitted mutation base, topic/change branch and integration target;
- avoid direct writes to protected or long-lived branches;
- verify that the active change branch is based on the authorized current base before mutation;
- preserve one coherent, reviewable change unit and return it through the repository's accepted review mechanism;
- verify durable remote state after the mutation or review transition;
- enforce repository-local naming/target/protection rules while remaining host-neutral.

The trigger is semantic change-path control, not the presence of Git commands.

## Negative / anti-triggers

Do not activate this candidate merely for:

- read-only repository inspection;
- ordinary code editing when a safe change path is already established and no repository-control decision remains;
- generic Git syntax questions, commit message wording, diff viewing, or history browsing;
- release planning whose distinguishing intent is product release/stabilization rather than ordinary repository mutation;
- workspace/worktree collision management as an independent intent before S9 resolves its placement;
- task authority, scope, acceptance, test ownership, SDD stage ownership, or Executor launch/handoff decisions;
- consumer-project governance lifecycle work that happens to use Git;
- local scratch work that is explicitly outside tracked repository change control.

## Input contract

A host invoking the candidate needs, at minimum:

- repository identity;
- current authorized repository policy or policy pointer;
- requested change intent/scope;
- current durable repository state sufficient to identify base/target/branch relationship;
- caller authority envelope and any protected-target restrictions.

Repository-specific policy remains authoritative. The candidate must fail closed when the required base/target/permission relationship is unknown or conflicting.

## Output / postcondition contract

A successful invocation should produce or establish:

1. the resolved authorized base and integration target;
2. the permitted change-path class (for example topic branch + review, hotfix path, or repository-specific equivalent);
3. a change branch/reference identity that does not encode agent identity unless repository policy explicitly requires it;
4. confirmation that protected/direct-write restrictions are respected;
5. a bounded, reviewable mutation state or a precise blocked state if policy cannot be satisfied;
6. durable provenance sufficient to reconstruct what branch/ref was used and where the change is intended to integrate;
7. verification of the relevant remote/durable postcondition after creation/update/integration actions that the caller is authorized to perform.

The capability must not claim semantic acceptance merely because repository mechanics succeeded.

## Authority boundary

`repository-change-control` is procedural and policy-resolving, not an authority source.

It may:

- read and apply repository-local branching/change policy;
- select among already-authorized change-path mechanics;
- verify base/head/target relationships and protected-target constraints;
- surface conflicts and stop conditions.

It must not:

- invent permission to mutate a repository;
- redefine repository branch/release policy;
- change task scope, specification, design, acceptance, ownership, or release authority;
- weaken branch protection or bypass required review;
- convert a host/product identity into repository authority;
- treat a generic reusable default as stronger than repository-local policy.

For Agent Governance specifically, D053/D068 stage ownership, Markdown/file ownership, Task Contracts, L007, D061/D062, release semantics, and Human/Orchestrator/Executor authority remain in the Maintainer/domain adapter.

## Agent Governance adapter boundary

The candidate's generic semantics can cover:

- use a non-protected review branch when repository policy requires it;
- start from the authorized current base;
- avoid direct protected-target writes;
- return through the authorized review/integration path;
- preserve durable branch/ref provenance.

The Agent Governance adapter must continue to supply:

- `develop` as the normal maintenance base/integration target and `main` as stable release branch;
- exact `feat/*`, `fix/*`, `refactor/*`, `test/*`, `docs/*`, `chore/*`, `release/*`, and `hotfix/*` rules;
- D061/D062 freshness/protected-base requirements;
- D068 candidate publication semantics;
- L007 fail-closed branch targeting;
- source-product release propagation and cleanup rules;
- current role/write-ownership restrictions.

The generic candidate therefore cannot replace `docs/BRANCHING.md` or the Maintainer Skill domain route.

## ChatGPT / Codex host-adapter boundary

The semantic contract should remain host-neutral. Host adapters differ only in execution surfaces.

### ChatGPT adapter

For ChatGPT, the candidate may use connected repository operations to inspect refs/policy, create or update a topic branch, persist authorized Markdown/source changes, open/review PRs, and verify remote state. ChatGPT-specific tool names and UI flows remain adapter mechanics, not candidate semantics.

### Codex / Executor adapter

For Codex or another coding Executor, the same candidate semantics apply through local Git/provider tooling inside the Executor's already-authorized task envelope. Exact CLI/API/SDK syntax remains D054/executor-owned mechanics in Agent Governance.

Neither adapter changes who is permitted to author a given file or stage. Same intent and postcondition support one host-neutral candidate with host-specific mechanics references rather than separate ChatGPT/Codex Skills.

## Non-overlap analysis

The candidate is distinct from:

- **Maintainer Skill**: Maintainer answers “maintain Agent Governance”; this candidate answers “control the repository mutation path” and can apply outside Agent Governance.
- **executor-launch-handoff**: launch/handoff concerns preparing/returning delegated work; repository change control concerns the durable mutation path itself.
- **durable-work-checkpoint**: checkpointing preserves resumable work frontier; repository change control governs tracked repository mutation/integration.
- **upstream-version-revalidation**: version revalidation decides whether relied-on external behavior changed; it does not control repository mutation topology.
- **research-evidence-traceability**: research provenance is evidence/decision lifecycle, not branch/PR mutation control.

Workspace isolation overlaps partially through collision prevention, but S4 does not resolve whether that should be an internal sub-route/reference or a distinct capability. S9 owns that disposition.

## Candidate risks and guardrails

Primary risks:

- becoming a broad generic “Git Skill” with noisy routing;
- duplicating repository-local branch policy instead of reading it;
- silently importing Agent Governance's `main/develop` assumptions into other repositories;
- expanding into workspace hygiene, release management, or generic coding without distinct triggers;
- allowing successful mechanics to masquerade as semantic acceptance.

Required guardrails for any later design:

- narrow description around repository mutation/change-path control;
- explicit anti-triggers for generic Git help/read-only inspection;
- repository-local policy wins over candidate defaults;
- fail closed on ambiguous authority/base/target;
- no authority creation;
- workspace-isolation placement deferred to S9;
- host-specific commands kept in adapters/references.

## Analytical disposition

`KEEP_CANDIDATE`

Rationale:

- the intent is reusable across repositories and hosts;
- it has a distinct trigger boundary centered on controlled tracked mutation, not generic Git usage;
- it yields a concrete postcondition (authorized base/target/change path + durable reviewable state);
- it can reduce repeated always-on branch/PR procedure while preserving repository-local authority;
- it does not require splitting by ChatGPT/Codex host;
- it remains separable from Agent Governance's domain-specific branch/release/stage semantics.

This disposition means “retain for candidate-topology synthesis/evaluation,” not “adopt or implement a Skill.”

## Completion assessment

S4 completion gate is satisfied:

- reusable intent is explicit;
- positive and negative trigger boundaries are explicit;
- output/postcondition contract is explicit;
- authority and Agent Governance adapter boundaries are explicit;
- ChatGPT/Codex mechanics are separated from host-neutral semantics;
- non-overlap with adjacent candidates is documented;
- disposition is `KEEP_CANDIDATE`;
- workspace-isolation final placement remains deferred to S9;
- no normative decision, root rewrite, Skill implementation, Executor launch, provider/model call, or T066 mutation occurred.

R029-S4 is complete analytically and awaits Human review/acceptance before R029-S5 may be selected.