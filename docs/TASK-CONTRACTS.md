# Source Product Task Contracts

Status: ACTIVE

## Purpose

Define the persistent handoff format used when ChatGPT Orchestrator delegates executable work in the canonical `agent-governance` source repository.

Task Contracts are auditable source-product maintenance records. They are intentionally separate from consumer-project `.agent-coordination/` tasks.

Under accepted D053, Task Contracts are also the normal source-product `Plan & Trace` carrier for executable work unless a dedicated specification/design artifact is materially justified. They reference rather than duplicate adequate current specification carriers.

## Authority

- ChatGPT Orchestrator authors and revises Task Contract Markdown.
- ChatGPT owns native SDD Explore/Frame, Specify, Design, Plan & Trace, and Converge/Accept/Evolve semantics.
- Under D052-designated `orchestrator-conformance` or `mixed` work, ChatGPT may also author the narrowly scoped non-Markdown conformance/oracle assets that directly encode approved acceptance semantics.
- The Agente de IA Ejecutor reads Task Contracts as authoritative execution scope and MUST NOT edit them.
- The Agente de IA Ejecutor owns only the technical `Implement` and `Code Review & Verify` stages for authorized executor-owned work.
- The Human Owner retains final authority.

A chat/terminal prompt is only a pointer to a Task Contract. It is not the canonical task specification.

## D053 native SDD contract invariant

Every new or materially revised executable Task Contract receives proportionate SDD coverage using `COMPACT`, `STANDARD`, or `ASSURED`.

The Task Contract must make the applicable chain durable enough to reconstruct from Git:

```text
Human/product intent
    -> current specification carrier + requirement/spec delta
    -> Orchestrator Design
    -> Plan & Trace / Task Contract
    -> Executor implementation
    -> Executor Code Review & Verify evidence
    -> Orchestrator Converge / Accept / Evolve
```

Material requirement deltas use `ADDED / MODIFIED / REMOVED / PRESERVED`. `PRESERVED` is the normal way to make non-regression/zero-drift behavior first-class for refactors, fixes, migrations and security hardening.

A separate spec/design/trace file is not required merely for ceremony. Existing normative Markdown, Decision Records, Task Contract sections or other accepted artifacts may carry the current specification/Design when they do so unambiguously.

The contract is not READY if the executor would need to invent missing normative behavior, material architecture/Design, acceptance meaning or task decomposition.

## Executor process autonomy invariant

Task Contracts define **what must be delivered, the complete controlling Design/Plan boundary, and what evidence must exist**. They do not normally define **how the executor must organize its private implementation/review process**.

Under D041 as refined by D053, the Agente de IA Ejecutor may independently choose and compose any compatible executor-native methods and capabilities needed inside native SDD stages 5-6, including direct work, private/internal planning, private SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers, or other mechanisms.

```text
Task Contract = specification + Design + Plan/Trace + scope + acceptance + evidence
Executor       = local implementation process + technical Code Review & Verify process
```

Executor-private planning/SDD state is not a second authoritative Design or Plan. If an executor-side choice would materially change approved requirements, architecture/interfaces/state/data flow/trust boundaries, compatibility/migration, failure behavior, acceptance meaning or task decomposition, the executor stops and reports a re-entry condition rather than silently deciding it.

D052 adds a material ownership boundary, not an executor methodology: when the Task Contract selects `orchestrator-conformance` or `mixed`, the approved conformance oracle is pre-authored by ChatGPT and the executor must execute rather than semantically redefine it. The executor remains free to choose its implementation/testing/review process and to add supplementary technical coverage.

ChatGPT MUST NOT prescribe executor-specific agent types, delegation topology, private SDD routing, internal planning structure, or tool selection unless the method itself is material to an accepted safety/security/reproducibility/ownership requirement or to the requested product behavior.

Likewise, review MUST NOT require the executor's private orchestration trace unless a particular process artifact was explicitly part of the persisted deliverable/evidence contract. Governance evaluates remote Git state, persisted handoff, Code Review & Verify evidence and required verification results.

Executor-native workflows remain subordinate implementation mechanisms: they may not redefine Task Contract semantics, acquire Governance acceptance authority, or introduce tracked/generated repository state outside authorized scope.

## Test authorship mode

D052 defines three test-authorship modes when ownership is material:

- `orchestrator-conformance` — ChatGPT owns the required acceptance/conformance oracle; executor owns execution plus supplementary implementation/exploratory testing.
- `executor-implementation` — executor owns technical test/eval implementation and execution within the ChatGPT-owned specification/Design/acceptance contract.
- `mixed` — ChatGPT owns the semantic conformance oracle and executor owns implementation/exploratory tests and execution.

New or materially revised Task Contracts SHOULD declare `Test-Authorship-Mode` when test ownership affects scope. Ordinary consumer/application implementation defaults conceptually to `executor-implementation`; Agent Skill/governance/policy/documentation-managed semantic products should normally use `orchestrator-conformance` or `mixed` when ChatGPT owns the correctness semantics.

The mode does not change native SDD stage ownership or assurance-plane selection. D019/D046 still determine whether the required evidence is deterministic, property/state-machine, routing/eval, behavioral, security, portability or package/provenance evidence.

### Conformance asset rule

When `orchestrator-conformance` or `mixed` applies, the Task Contract or its integrated prerequisite gate SHOULD identify the exact pre-authored conformance assets needed for acceptance. Those assets may include approved assertions, corpora, expected outcomes, semantic negative controls, thresholds, golden fixtures or graders.

A conformance asset is an executable projection of the controlling Core/Decision/Task Contract. It is not independent authority.

The executor MAY diagnose a defect or make a purely mechanical correction only when durable task/review authority explicitly permits that correction class without changing semantics. Any expected-result, classification, threshold, security expectation, negative-control meaning, or frozen-baseline change requires persisted ChatGPT authority before execution continues.

If the executor believes an Orchestrator-owned oracle is semantically defective, it reports the affected claim as blocked/`ORACLE_DEFECT`-equivalent with evidence rather than silently weakening the oracle.

## Remote baseline freshness and repository-instruction loading

Under D042, the executor MUST load the Task Contract from a local baseline that is current with the canonical remote base branch.

Under D043, compatible executor hosts are expected to load applicable repository-level instructions such as `AGENTS.md` through their native session/repository bootstrap. Agent Governance therefore does not repeat an unconditional `read AGENTS.md` directive in every launch prompt.

```text
normal launch:
synchronize canonical remote
    -> verify safe local base == current origin/<base-branch>
    -> read Task Contract
    -> execute

launch after governing AGENTS.md change:
synchronize canonical remote
    -> verify safe local base == current origin/<base-branch>
    -> reload current AGENTS.md
    -> read Task Contract
    -> execute
```

A currently checked-out older topic branch, or a stale local branch merely named `develop`, is not sufficient evidence of `current develop`.

The executor chooses the concrete compatible Git workflow for synchronization. It MUST preserve local/uncommitted work and MUST stop/escalate rather than destructively overwrite, discard or guess if the current remote baseline cannot be established safely.

The conditional `AGENTS.md` reload is determined by canonical Git history. ChatGPT includes it only when the integrated change governing the delegated execution modified `AGENTS.md` and a running executor session may hold a pre-change instruction snapshot.

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

When D052 applies, the Task Contract SHOULD point to the exact integrated conformance/oracle assets or prerequisite gate rather than requiring the executor to reconstruct their semantics from unrelated history.

### Requirement / specification delta
Represent the material affected semantics with the applicable subset:

- `ADDED`
- `MODIFIED`
- `REMOVED`
- `PRESERVED`

Requirements SHOULD use stable IDs when independent traceability is materially useful. For no-behavior-delta work, `PRESERVED` plus explicitly authorized structural/objective changes is sufficient; do not invent fake feature behavior.

### Controlling Design
Persist or directly reference the complete implementation-relevant Design and material architecture/quality/security/privacy/reliability/compatibility decisions.

The Design must be complete enough that the executor does not need to invent missing material architecture or acceptance semantics. Local code details that cannot change the approved Design remain implementation choices.

### Authorized scope
Artifacts and behavior the executor is allowed to modify or create.

Authorized scope constrains externally visible repository mutation/result, not the executor's private internal organization or compatible local tooling unless the contract explicitly states otherwise for a material reason.

For D052 modes, authorized scope MUST distinguish Orchestrator-owned conformance assets from executor-owned implementation/harness/supplementary-test scope.

### Explicit exclusions
Things the executor must not change or expand into.

Exclusions should protect product scope, specification/Design/Plan authority, safety, reproducibility or repository state. Avoid using exclusions to ban an executor-internal methodology/tool merely because the current host provides it.

When D052 applies, semantic changes to the conformance oracle are excluded from executor authority unless a durable revision explicitly transfers a bounded correction.

### Invariants / constraints
Architecture, compatibility, safety, ownership, or behavioral properties that must remain true. Material non-regression behavior should normally be represented as `PRESERVED` in the requirement delta as well.

### Acceptance criteria
Objective conditions ChatGPT will use during `Converge / Accept / Evolve` to accept or reject the implementation.

### Verification and trace requirements
Define tests/evals/inspection/analysis/demonstration that must be created or executed and the minimum evidence expected.

Material requirements must have enough mapping to answer which implementation/evidence satisfies them. A separate matrix is optional unless risk/complexity justifies it.

Verification requirements define required evidence/results. They should not dictate private execution topology unless that topology is itself part of the behavior or assurance property being verified.

For D052 `orchestrator-conformance`/`mixed`, verification requirements SHOULD separate:

- required execution of the pre-authored conformance oracle;
- executor-owned supplementary implementation/exploratory verification;
- evidence required to prove both classes ran against the submitted implementation.

### Code Review & Verify obligations
The Task Contract SHOULD make clear any task-specific technical review obligations beyond the repository baseline. Regardless of whether a dedicated section exists, the executor must perform the D053 Code Review & Verify stage before `DONE` and provide evidence sufficient for `docs/EXECUTOR-HANDOFFS.md`.

### Stop / escalation / SDD re-entry conditions
Conditions requiring the executor to stop instead of guessing or expanding scope.

These include suspected material defects/ambiguity/infeasibility in the requirement/spec delta, controlling Design, Plan/Trace or acceptance meaning. The executor reports evidence and the earliest affected SDD stage; ChatGPT persists the revision before work resumes.

When D052 applies, suspected semantic oracle defects are stop/escalation conditions for the affected acceptance claim.

### Expected handoff
The executor MUST persist its result according to `docs/EXECUTOR-HANDOFFS.md` at the task's expected handoff path before claiming `DONE`, `BLOCKED`, or `PARTIAL`.

## Contract and conformance integration gate

An executable Task Contract is not ready for execution merely because it exists on a planning branch.

Before launching an executor:
1. ChatGPT completes the applicable Explore/Specify/Design/Plan & Trace stages and creates/updates the Task Contract on a policy-compliant planning/topic branch;
2. when D052 `orchestrator-conformance` or `mixed` requires a pre-authored oracle, ChatGPT creates/updates the designated conformance assets on that preimplementation gate and records their role in the Task Contract/gate;
3. ChatGPT reviews the Task Contract, controlling Markdown/Decision/specification/Design artifacts, trace, and any Orchestrator-owned conformance assets;
4. the planning/conformance change is merged into `develop`;
5. the task status is `READY` only when all known prerequisite decisions are resolved and the executor will not need to invent upstream authority;
6. the executor synchronizes the canonical remote and establishes a safe local baseline equal to the current remote base branch containing that exact contract and required conformance assets;
7. if the governing integrated change modified `AGENTS.md`, ChatGPT includes the D043 reload line and the executor reloads current `AGENTS.md` from that baseline;
8. only then may the executor create/use the implementation topic branch from that current baseline.

This creates durable specification/Design/Plan/oracle before implementation history:

```text
specification + Design + Task Contract/trace + applicable conformance history
        -> implementation + Code Review & Verify history
        -> Orchestrator convergence/acceptance history
```

The executor MUST NOT begin executable work from a branch/revision that predates the controlling Task Contract or required pre-authored oracle, or from a stale local base that has not been reconciled with the canonical remote.

## Freeze and revision semantics

The original objective, current-spec binding, requirement/spec delta, controlling Design, scope, exclusions, invariants, Plan/Trace, acceptance criteria, verification meaning, and any D052 semantic conformance oracle are the durable request.

After implementation begins:
- the executor cannot edit the Task Contract;
- ChatGPT must not silently rewrite original semantics to match implementation;
- an executor cannot silently change an Orchestrator-owned expected result/threshold/classification or material Design assumption to match implementation;
- a material change requires explicit SDD re-entry and a persisted revision before execution continues;
- lifecycle metadata and explicit review/revision/acceptance notes may be updated/appended by ChatGPT as long as the original request remains auditable.

A reviewer must be able to distinguish the original task/oracle/specification/Design from later authorized revisions.

## Lifecycle

1. ChatGPT performs Explore/Frame and Specify for the change.
2. ChatGPT completes controlling Design and Plan & Trace, creates the Task Contract, and selects D052 authorship mode when material.
3. For `orchestrator-conformance`/`mixed`, ChatGPT authors the required conformance oracle before implementation when appropriate.
4. The Task Contract and applicable conformance gate are reviewed and integrated into `develop`.
5. ChatGPT launches the executor with the canonical minimal launch prompt defined below.
6. The executor synchronizes the canonical remote and verifies a safe current base baseline.
7. If the governing integrated change modified `AGENTS.md`, the executor reloads current `AGENTS.md` when explicitly instructed by the conditional D043 line.
8. The executor creates/uses the authorized implementation topic branch.
9. The executor chooses its private implementation process and performs only authorized non-Markdown work, respecting the approved specification/Design/Plan and any D052 conformance ownership boundary.
10. If implementation discovers an upstream semantic/Design/Plan defect, the executor stops and reports it; material changes require persisted Orchestrator SDD re-entry before execution continues.
11. The executor performs technical Code Review & Verify, runs required conformance plus supplementary verification, resolves in-authority defects, and persists its non-Markdown handoff under `handoffs/`.
12. The executor commits and pushes the implementation branch, including the current handoff artifact, under D048 publication rules.
13. The executor returns only status, handoff path, branch, and pushed HEAD.
14. ChatGPT reads the Task Contract, specification/Design/trace, conformance baseline where applicable, handoff, and remote Git diff/evidence.
15. ChatGPT performs Converge/Accept; rework/re-entry repeats on the same represented task branch using durable review/revision instructions.
16. After ChatGPT acceptance, the implementation proceeds through PR to `develop`.
17. ChatGPT evolves the accepted current specification carrier where applicable and may update lifecycle/acceptance metadata without rewriting original execution semantics.
18. After accepted task content/handoff and acceptance records are integrated, any delegated post-integration branch retirement MUST be governed by an integrated Operational Contract under `docs/OPERATION-CONTRACTS.md` and launched only through `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`.
19. Operational task closure is complete only after required remote/local branch cleanup is verified.

## Canonical minimal executor launch prompt

Every normal source-product executor launch MUST use the same structural contract. The launch prompt is transport/bootstrap only; it MUST NOT become a second task specification.

The prompt contains these semantic parts:

1. **Role** — identify the abstract `Agente de IA Ejecutor` role and canonical repository.
2. **Repository freshness/baseline** — require synchronization of the canonical remote and a safe local baseline current with the Task Contract base branch, normally `origin/develop`.
3. **Conditional repository-instruction reload** — include an explicit `AGENTS.md` reload only when the governing integrated change modified `AGENTS.md`; omit it otherwise.
4. **Authoritative task pointer** — provide exactly one controlling Task Contract path and state that the Task Contract plus its referenced repository policies are the complete execution specification.
5. **Completion contract** — require the contract-defined Implement + Code Review & Verify evidence/handoff, commit and push, then require only the minimal status/handoff/branch/HEAD response.

Normal canonical template:

```text
Operate as the Agente de IA Ejecutor for <owner>/<repository>.

Synchronize the canonical remote and ensure the local <base-branch> baseline used for bootstrap is current with origin/<base-branch>. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

Then load and execute the authoritative Task Contract:
<task-contract-path>

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required implementation, Code Review & Verify, verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```
