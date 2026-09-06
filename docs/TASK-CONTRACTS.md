# Source Product Task Contracts

Status: ACTIVE

## Purpose

Define the persistent handoff format used when ChatGPT Orchestrator delegates executable work in the canonical `agent-governance` source repository.

Task Contracts are auditable source-product maintenance records. They are intentionally separate from consumer-project `.agent-coordination/` tasks.

Under accepted D053, Task Contracts are also the normal source-product `Plan & Trace` carrier for executable work unless a dedicated specification/design artifact is materially justified. They reference rather than duplicate adequate current specification carriers.

## Authority

- ChatGPT Orchestrator authors and revises Task Contract Markdown.
- ChatGPT owns native SDD Explore/Frame, Specify, Design, Plan & Trace, and Converge/Accept/Evolve semantics.
- For D068-mode source maintenance, ChatGPT also owns Stage 5 complete candidate materialization.
- Under D052-designated `orchestrator-conformance` or `mixed` work, ChatGPT owns the semantic conformance/oracle assets that directly encode approved acceptance semantics.
- The Agente de IA Ejecutor reads Task Contracts as authoritative execution scope and MUST NOT edit them.
- For D068-mode work, the Agente de IA Ejecutor owns Stage 6 execution, diagnosis, bounded technical repair, Code Review & Verify, and verification evidence for the published candidate.
- The Human Owner retains final authority.

A chat/terminal prompt is only a pointer to a Task Contract. It is not the canonical task specification.

### D068 prospective source-maintenance normalization

For new D068-mode source-maintenance work, this document uses the following effective chain:

```text
Human/product intent
    -> current specification carrier + requirement/spec delta
    -> Orchestrator Design
    -> Plan & Trace / Task Contract
    -> Orchestrator complete Stage 5 candidate
    -> coherent candidate + authority published on verified topic branch
    -> Executor Stage 6 execution / diagnosis / bounded repair / verification
    -> Orchestrator Converge / Accept / Integrate / Evolve
```

A coherent published topic-branch checkpoint containing the controlling Task Contract/Plan, applicable D052 semantic oracle assets, and complete candidate is sufficient authority for Executor verification. D068-mode work does **not** require a separate planning/candidate merge into `develop` first.

Any later unqualified wording in this document that says the Executor owns D068 Stage 5 first-pass implementation, that a Task Contract/oracle must first be merged into `develop`, or that an Executor topic branch can exist only after such a merge retains only explicit historical/grandfathered or non-D068 scope. Historical executed Task Contracts, handoffs, reviews, and evidence are not rewritten retroactively.

D052 semantic-oracle ownership, D054 execution-mechanics ownership, D060 coordinator continuity, D061/D062 branch protection and freshness, D065 delegation obligations, and the explicit D066 gaps remain intact. D068 does not change Governance Core or consumer-project SDD semantics.

## D053 native SDD contract invariant

Every new or materially revised executable Task Contract receives proportionate SDD coverage using `COMPACT`, `STANDARD`, or `ASSURED`.

The Task Contract must make the applicable authority and evidence chain durable enough to reconstruct from Git. For D068-mode work the chain is the normalized sequence above; explicit grandfathered/non-D068 contracts retain their original persisted execution topology.

Material requirement deltas use `ADDED / MODIFIED / REMOVED / PRESERVED`. `PRESERVED` is the normal way to make non-regression/zero-drift behavior first-class for refactors, fixes, migrations and security hardening.

A separate spec/design/trace file is not required merely for ceremony. Existing normative Markdown, Decision Records, Task Contract sections or other accepted artifacts may carry the current specification/Design when they do so unambiguously.

The contract is not READY if the executor would need to invent missing normative behavior, material architecture/Design, acceptance meaning or task decomposition.

## Executor process autonomy invariant

Task Contracts define **what must be delivered, the complete controlling Design/Plan boundary, the candidate to be verified when D068 applies, and what evidence must exist**. They do not normally define **how the executor must organize its private Stage 6 process**.

Under D041/D054 as refined by D068 for source maintenance, the Agente de IA Ejecutor may independently choose and compose compatible executor-native methods and capabilities needed inside its authorized execution/diagnosis/repair/verification work, including direct work, private/internal planning, private SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other mechanisms.

```text
Task Contract = specification + Design + Plan/Trace + scope + acceptance + evidence
D068 candidate = complete Orchestrator-materialized Stage 5 repository state
Executor       = Stage 6 execution + diagnosis + bounded repair + technical review/verification process
```

Executor-private planning/SDD state is not a second authoritative Design or Plan. If an executor-side choice would materially change approved requirements, architecture/interfaces/state/data flow/trust boundaries, compatibility/migration, failure behavior, acceptance meaning or task decomposition, the executor stops and reports a re-entry condition rather than silently deciding it.

D052 adds a material semantic-ownership boundary, not an executor methodology: when the Task Contract selects `orchestrator-conformance` or `mixed`, the approved conformance oracle is owned by ChatGPT and the executor must execute rather than semantically redefine it. D068 permits ChatGPT to materialize candidate implementation/regression/integration tests during Stage 5; the executor may add/correct technical coverage during Stage 6 only inside approved semantics/Design.

ChatGPT MUST NOT prescribe executor-specific agent types, delegation topology, private SDD routing, internal planning structure, or tool selection unless the method itself is material to an accepted safety/security/reproducibility/ownership requirement or to the requested product behavior. D065 still requires materially separable Stage 6 work to be delegated when its positive triggers hold and no anti-trigger dominates.

Likewise, review MUST NOT require the executor's private orchestration trace unless a particular process artifact was explicitly part of the persisted deliverable/evidence contract. Governance evaluates remote Git state, persisted handoff, Code Review & Verify evidence and required verification results.

Executor-native workflows remain subordinate implementation mechanisms: they may not redefine Task Contract semantics, acquire Governance acceptance authority, or introduce tracked/generated repository state outside authorized scope.

## Test authorship mode

D052 defines three semantic/test-ownership modes when ownership is material:

- `orchestrator-conformance` — ChatGPT owns the required acceptance/conformance oracle; executor owns execution plus authorized technical supplementary testing/repair during Stage 6.
- `executor-implementation` — outside D068 Stage 5 candidate authorship, the executor may own technical test/eval implementation under the controlling contract; in D068 mode ChatGPT may materialize the candidate tests and the executor may technically repair/strengthen them inside authority.
- `mixed` — ChatGPT owns semantic conformance meaning; executor owns authorized technical execution/repair/supplementary coverage.

New or materially revised Task Contracts SHOULD declare `Test-Authorship-Mode` when semantic test ownership affects scope. Ordinary consumer/application implementation defaults conceptually to `executor-implementation`; Agent Skill/governance/policy/documentation-managed semantic products should normally use `orchestrator-conformance` or `mixed` when ChatGPT owns the correctness semantics.

The mode does not transfer semantic-oracle ownership or assurance-plane selection. D019/D046 still determine whether the required evidence is deterministic, property/state-machine, routing/eval, behavioral, security, portability or package/provenance evidence.

### Conformance asset rule

When `orchestrator-conformance` or `mixed` applies, the Task Contract SHOULD identify the exact conformance assets needed for acceptance. In D068 mode those assets may be published with the coherent topic-branch candidate rather than first merged separately to `develop`. They may include approved assertions, corpora, expected outcomes, semantic negative controls, thresholds, golden fixtures or graders.

A conformance asset is an executable projection of the controlling Core/Decision/Task Contract. It is not independent authority.

The executor MAY diagnose a defect or make a purely mechanical correction only when durable task/review authority explicitly permits that correction class without changing semantics. Any expected-result, classification, threshold, security expectation, negative-control meaning, or frozen-baseline change requires persisted ChatGPT authority before execution continues.

If the executor believes an Orchestrator-owned oracle is semantically defective, it reports the affected claim as blocked/`ORACLE_DEFECT`-equivalent with evidence rather than silently weakening the oracle.

## Remote baseline freshness and repository-instruction loading

Under D042/D061/D062, the executor MUST load the Task Contract and candidate from an auditable remote state with a current protected-base relationship.

For D068-mode work the authoritative verification target is the coherent published topic-branch checkpoint. A stale local branch merely named `develop`, an arbitrary older topic branch, or local-only candidate state is not sufficient authority.

Under D043, compatible executor hosts are expected to load applicable repository-level instructions such as `AGENTS.md` through their native session/repository bootstrap. Agent Governance therefore does not repeat an unconditional `read AGENTS.md` directive in every launch prompt.

```text
D068 normal launch:
synchronize canonical remote
    -> verify protected-base/topic relationship and exact published candidate HEAD
    -> checkout/use authorized topic branch
    -> read Task Contract from that represented state
    -> execute/diagnose/repair/verify

launch after governing AGENTS.md change:
synchronize canonical remote
    -> verify authorized base/topic/candidate identity
    -> reload current governing AGENTS.md
    -> read Task Contract
    -> execute/diagnose/repair/verify
```

The executor chooses the concrete compatible Git workflow for synchronization under D054. It MUST preserve local/uncommitted work and MUST stop/escalate rather than destructively overwrite, discard or guess if the current remote identity cannot be established safely.

The conditional `AGENTS.md` reload is determined by canonical Git history. ChatGPT includes it only when the governing change modified `AGENTS.md` and a running executor session may hold a pre-change instruction snapshot.

If an executor host does not natively load repository instructions, its adapter/session bootstrap must provide equivalent loading before it is treated as a compatible Agente de IA Ejecutor. Repeating `read AGENTS.md` in every Task prompt is not the fallback mechanism.

## Location and naming

Active and completed source-maintenance Task Contracts live under:

`docs/tasks/`

Recommended naming:

`TNNN-<short-slug>.md`

Task IDs are stable once assigned.

Each executable task SHOULD identify its expected persisted executor handoff path under `handoffs/`, normally:

`handoffs/TNNN-executor-handoff.json`

## Required fields

Each new or materially revised executable task should contain the following, proportionate to its selected SDD profile.

### Identity
- Task ID
- Status: `DRAFT`, `BLOCKED`, `READY`, `IN_PROGRESS`, `DONE`, `ACCEPTED`, `CANCELLED`
- Type: feature, fix, refactor, test/eval, release, infrastructure, or mixed
- Base branch
- Expected topic branch
- Expected executor handoff path
- `SDD-Profile`: `COMPACT`, `STANDARD`, or `ASSURED`
- `Test-Authorship-Mode` when D052 ownership classification is material

### Objective
A concise description of the observable result required.

### Current specification carrier / controlling references
Identify the accepted current specification carrier when one exists and only the repository files/decisions needed to interpret the task correctly.

The carrier may be an existing normative artifact, dedicated spec, Decision Record, protocol/Skill artifact or project-native SDD artifact. Do not duplicate the full carrier into the Task Contract merely for convenience.

`AGENTS.md` remains controlling repository policy even when its load is supplied natively by the executor host rather than repeated in the launch prompt.

When D052 applies, the Task Contract SHOULD point to the exact conformance/oracle assets or candidate gate rather than requiring the executor to reconstruct their semantics from unrelated history.

### Requirement / specification delta
Represent the material affected semantics with the applicable subset:

- `ADDED`
- `MODIFIED`
- `REMOVED`
- `PRESERVED`

Requirements SHOULD use stable IDs when independent traceability is materially useful. For no-behavior-delta work, `PRESERVED` plus explicitly authorized structural/objective changes is sufficient; do not invent fake feature behavior.

### Controlling Design
Persist or directly reference the complete implementation-relevant Design and material architecture/quality/security/privacy/reliability/compatibility decisions.

The Design must be complete enough that the executor does not need to invent missing material architecture or acceptance semantics. Local code details that cannot change the approved Design remain technical repair/verification choices only when they stay inside the approved Design.

### Authorized scope
Artifacts and behavior the executor is allowed to modify or create during its authorized stage.

For D068-mode work, the Task Contract distinguishes the complete Orchestrator-materialized Stage 5 candidate from the Executor's bounded Stage 6 repair/test/evidence authority. Authorized scope constrains externally visible repository mutation/result, not the executor's private internal organization or compatible local tooling unless the contract explicitly states otherwise for a material reason.

For D052 modes, authorized scope MUST distinguish Orchestrator-owned semantic conformance assets from executor-authorized technical repair/harness/supplementary-test scope.

### Explicit exclusions
Things the executor must not change or expand into.

Exclusions should protect product scope, specification/Design/Plan authority, safety, reproducibility or repository state. Avoid using exclusions to ban an executor-internal methodology/tool merely because the current host provides it.

When D052 applies, semantic changes to the conformance oracle are excluded from executor authority unless a durable revision explicitly transfers a bounded correction.

### Invariants / constraints
Architecture, compatibility, safety, ownership, or behavioral properties that must remain true. Material non-regression behavior should normally be represented as `PRESERVED` in the requirement delta as well.

### Acceptance criteria
Objective conditions ChatGPT will use during `Converge / Accept / Evolve` to accept or reject the final candidate.

### Verification and trace requirements
Define tests/evals/inspection/analysis/demonstration that must be created or executed and the minimum evidence expected.

Material requirements must have enough mapping to answer which candidate implementation/evidence satisfies them. A separate matrix is optional unless risk/complexity justifies it.

Verification requirements define required evidence/results. They should not dictate private execution topology unless that topology is itself part of the behavior or assurance property being verified.

For D052 `orchestrator-conformance`/`mixed`, verification requirements SHOULD separate:

- required execution of the Orchestrator-owned conformance oracle;
- executor-authorized supplementary technical verification/repair;
- evidence required to prove both classes ran against the submitted candidate.

### Code Review & Verify obligations
The Task Contract SHOULD make clear any task-specific technical review obligations beyond the repository baseline. Regardless of whether a dedicated section exists, the executor must perform the Stage 6 Code Review & Verify work before `DONE` and provide evidence sufficient for `docs/EXECUTOR-HANDOFFS.md`.

### Stop / escalation / SDD re-entry conditions
Conditions requiring the executor to stop instead of guessing or expanding scope.

These include suspected material defects/ambiguity/infeasibility in the requirement/spec delta, controlling Design, Plan/Trace or acceptance meaning. The executor reports evidence and the earliest affected SDD stage; ChatGPT persists the revision before work resumes.

When D052 applies, suspected semantic oracle defects are stop/escalation conditions for the affected acceptance claim.

### Expected handoff
The executor MUST persist its result according to `docs/EXECUTOR-HANDOFFS.md` at the task's expected handoff path before claiming `DONE`, `BLOCKED`, or `PARTIAL`.

## Contract, candidate, and conformance publication gate

A D068 executable Task Contract is not ready for Stage 6 merely because it exists only in chat, Library, or an unpublished local branch.

Before launching an Executor for D068-mode work:
1. ChatGPT completes Explore/Specify/Design/Plan & Trace and creates/updates the Task Contract on the verified topic branch;
2. when D052 `orchestrator-conformance` or `mixed` requires a semantic oracle, ChatGPT creates/updates the designated conformance assets and records their role;
3. ChatGPT completes Stage 5 materialization of the candidate on that topic branch;
4. ChatGPT reviews the Task Contract, controlling Markdown/Decision/specification/Design artifacts, trace, applicable semantic oracle assets, and candidate coherence;
5. ChatGPT publishes one coherent topic-branch checkpoint containing the authority and candidate;
6. task readiness requires all known prerequisite decisions to be resolved and the Executor not to need to invent upstream authority;
7. the Executor synchronizes the canonical remote and verifies the exact published topic branch/HEAD plus its protected-base freshness relationship;
8. if the governing published change modified `AGENTS.md`, ChatGPT includes the D043 reload line and the Executor reloads the governing current `AGENTS.md` before Stage 6;
9. only then may the Executor execute, diagnose, make bounded technical repairs, and verify that published candidate.

D068 sequence:

```text
current protected develop base
    -> verified topic branch
    -> specification + Design + Task Contract/trace + applicable conformance + complete candidate
    -> coherent published candidate checkpoint
    -> Executor Stage 6 evidence/repairs
    -> Orchestrator convergence/acceptance/integration
```

A separate planning/candidate PR to `develop` before Stage 6 is not required in D068 mode.

For explicit grandfathered/non-D068 work whose persisted authority requires the earlier topology, preserve that historical sequence exactly rather than rewriting it:

```text
planning/conformance -> develop -> Executor first-pass implementation -> verification
```

The executor MUST NOT begin executable work from a branch/revision that predates the controlling Task Contract or required semantic oracle, from an unpublished D068 candidate, or from a stale branch whose protected-base relationship has not been established safely.

## Freeze and revision semantics

The original objective, current-spec binding, requirement/spec delta, controlling Design, scope, exclusions, invariants, Plan/Trace, acceptance criteria, verification meaning, and any D052 semantic conformance oracle are the durable request.

After Stage 6 begins:
- the executor cannot edit the Task Contract;
- ChatGPT must not silently rewrite original semantics to match implementation;
- an executor cannot silently change an Orchestrator-owned expected result/threshold/classification or material Design assumption to match implementation;
- a material change requires explicit SDD re-entry and a persisted revision before execution continues;
- lifecycle metadata and explicit review/revision/acceptance notes may be updated/appended by ChatGPT as long as the original request remains auditable.

A reviewer must be able to distinguish the original task/oracle/specification/Design from later authorized revisions.

## Lifecycle

For D068-mode work:
1. ChatGPT performs Explore/Frame and Specify.
2. ChatGPT completes controlling Design and Plan & Trace, creates the Task Contract, and selects D052 authorship mode when material.
3. ChatGPT authors any required semantic conformance oracle and completes Stage 5 candidate materialization.
4. ChatGPT publishes the coherent Task Contract/authority/oracle/candidate checkpoint to the verified topic branch.
5. ChatGPT launches the Executor with the canonical minimal launch prompt defined below.
6. The Executor synchronizes the canonical remote and verifies the exact authorized topic branch/HEAD and protected-base relationship.
7. If the governing published change modified `AGENTS.md`, the Executor reloads the governing `AGENTS.md` when explicitly instructed by D043.
8. The Executor performs Stage 6 execution, diagnosis, bounded technical repair, technical Code Review & Verify, and required verification.
9. If Stage 6 discovers an upstream semantic/Design/Plan defect, the Executor stops and reports it; material changes require persisted Orchestrator SDD re-entry before execution continues.
10. The Executor persists its non-Markdown handoff under `handoffs/`, commits and pushes any authorized Stage 6 repair/test/handoff changes under D048 publication rules.
11. The Executor returns only status, handoff path, branch, and pushed HEAD.
12. ChatGPT reads the Task Contract, specification/Design/trace, conformance baseline where applicable, handoff, and remote Git diff/evidence.
13. ChatGPT performs Converge/Accept; rework/re-entry repeats on the same represented task branch using durable review/revision instructions.
14. After ChatGPT acceptance, the candidate proceeds through PR to `develop`.
15. ChatGPT evolves the accepted current specification carrier where applicable and may update lifecycle/acceptance metadata without rewriting original execution semantics.
16. After accepted task content/handoff and acceptance records are integrated, any delegated post-integration branch retirement MUST be governed by an integrated Operational Contract under `docs/OPERATION-CONTRACTS.md` and launched only through `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`.
17. Operational task closure is complete only after required remote/local branch cleanup is verified.

Explicit grandfathered/non-D068 Task Contracts retain the lifecycle they already record. This section does not retroactively migrate historical executed contracts, reviews, handoffs, or evidence.

## Canonical minimal executor launch prompt

Every normal source-product Executor launch MUST use the same structural contract. The launch prompt is transport/bootstrap only; it MUST NOT become a second task specification.

For D068 mode the prompt contains these semantic parts:

1. **Role** — identify the abstract `Agente de IA Ejecutor` role and canonical repository.
2. **Repository freshness/candidate identity** — require synchronization of the canonical remote and verification of the exact authorized topic-branch candidate plus protected-base relationship.
3. **Conditional repository-instruction reload** — include an explicit `AGENTS.md` reload only when the governing published change modified it; omit it otherwise.
4. **Authoritative task pointer** — provide exactly one controlling Task Contract path and state that the Task Contract, published candidate, and referenced repository policies are the complete Stage 6 execution specification.
5. **Completion contract** — require contract-defined execution/diagnosis/bounded repair/Code Review & Verify evidence/handoff, commit and push, then require only the minimal status/handoff/branch/HEAD response.

Normal D068 template:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and establish the exact published topic-branch candidate authorized by the Task Contract, including its protected-base/freshness relationship. Preserve local/uncommitted work; if the authoritative candidate cannot be established safely, stop and report BLOCKED rather than using stale repository state.

Then load and execute the authoritative Task Contract from that represented candidate state:
<task-contract-path>

Treat that Task Contract, the published candidate, and their referenced repository policies as the complete Stage 6 execution specification. Do not recreate the candidate from scratch or infer/expand task scope from this prompt.

Complete the required execution, diagnosis, bounded technical repair, Code Review & Verify, verification and executor handoff, commit and push all authorized Stage 6 work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

If and only if the governing published change modified `AGENTS.md`, insert this line after the remote-freshness paragraph and before the Task Contract pointer:

```text
AGENTS.md changed in the governing published change; reload the governing current AGENTS.md before loading the Task Contract.
```

For normal launches, substitute only repository identity and Task Contract path; the concrete branch/HEAD/handoff identity is resolved from persisted authority and verified Git state. The output placeholders remain the generic completion schema. The Executor chooses concrete safe Git/command mechanics under D054.

### Launch-prompt non-duplication invariant

The launch prompt MUST NOT duplicate task semantics that belong in Git, including:

- objective/result;
- requirement/specification delta or current specification carrier;
- acceptance criteria;
- authorized filenames/scope;
- exclusions;
- architecture/controlling Design constraints;
- Plan/Trace decomposition;
- test commands or fixture families;
- D052 conformance corpus/expected outcomes/thresholds or oracle semantics;
- expected implementation branch/handoff path when the Task Contract already defines them;
- provider/product-specific implementation instructions;
- task-specific safety/security restrictions;
- protocol/module versions;
- executor-internal methodology, sub-agent topology, private SDD mode, Skill routing, or tool choice;
- routine repository-instruction reads already supplied by the compatible host.

Standing repository rules such as Markdown ownership remain in `AGENTS.md`/referenced policy and SHOULD NOT be re-stated task-by-task in the launch prompt.

The generic remote-freshness/candidate-identity requirement is allowed because it determines which persisted repository state is being loaded; it is not task-specific semantics. The D043 reload line is also allowed when required because it refreshes changed repository instructions rather than adding task semantics.

If any task-specific fact is necessary to execute safely or correctly, persist it in the Task Contract, its controlling specification/Design/Plan artifacts, its D052 conformance assets, or its controlling repository policy before launch rather than extending the chat/terminal prompt.

### Launch-prompt authority invariant

The prompt does not supersede or supplement missing Task Contract semantics.

```text
normal D068 launch prompt = role + repository + remote candidate freshness + task pointer + completion contract
conditional delta          = AGENTS.md reload only after governing AGENTS.md change
Task Contract + published candidate + referenced Git policy/specification/Design + designated D052 conformance assets = Stage 6 execution specification
```

If the Task Contract is missing, not ready, materially incomplete, absent from the coherent published candidate, or missing a required D052 semantic oracle, do not compensate by adding instructions to the launch prompt. Repair/persist/publish the appropriate Orchestrator-owned stage first.

If the Executor cannot find the Task Contract, candidate, or required conformance assets after synchronizing and verifying the authorized remote state, it MUST stop/escalate; it MUST NOT fall back to a stale branch or chat-carried semantics.

If a launch prompt conflicts with the persisted Task Contract, D052 conformance oracle, published candidate authority, or repository policy, the Executor MUST stop/escalate rather than choosing the chat-only instruction as a new task scope. Human/ChatGPT changes to specification/Design/Plan/objective/scope/acceptance/verification/oracle semantics must be persisted through the normal SDD re-entry/Task Contract revision flow.

## Canonical post-integration cleanup delegation

Post-integration branch retirement is not another implementation launch and MUST NOT be expressed as an ad hoc executor instruction or as a chat-carried `TASK`/`PR` cleanup target.

Before delegating cleanup, ChatGPT MUST persist the complete concrete operation in an integrated `docs/operations/OPNNN-*.md` Operational Contract governed by `docs/OPERATION-CONTRACTS.md`.

The cleanup bootstrap prompt then contains only repository/base/remote-freshness context plus exactly one Operational Contract path, with the same conditional D043 `AGENTS.md` reload rule. All concrete targets, resolved-review exceptions, safety semantics, and required evidence live in Git.

```text
normal task launch -> Task Contract pointer
post-integration cleanup -> Operational Contract pointer
prompt-specific operation semantics -> prohibited
```

If cleanup safety cannot be derived from the persisted Operational Contract and its referenced authoritative Git/GitHub state, the executor returns `BLOCKED` or `PARTIAL`; ChatGPT MUST NOT compensate with chat-only instructions.

## Minimal executor response pattern

After persisting/committing/pushing the required implementation handoff, the executor should return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-commit-sha>`

Operational Contract completion schemas are defined by each integrated Operational Contract and are referenced through `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` for branch retirement.

## Audit invariant

A reviewer must be able to reconstruct from Git alone:
- what was requested before Stage 6, including applicable specification/Design/Plan/Trace;
- the exact published D068 candidate checkpoint when D068 applies;
- which D052 test-authorship mode/oracle applied when material;
- any explicit SDD re-entry revisions/review directives;
- what the Executor reported it executed/repaired/technically reviewed;
- what actually changed;
- what the Orchestrator later accepted/rejected through convergence.

Chat history and private Executor orchestration traces must not be required for this reconstruction unless a persisted contract explicitly makes a process artifact part of the deliverable/evidence.
