# Refactoring Workflow

Status: ACTIVE

## Purpose

Define the repository-specific workflow for restructuring `agent-governance` without changing externally observable behavior or governance semantics.

A change that intentionally changes behavior, protocol semantics, authority, compatibility, or acceptance outcomes is NOT a refactor and must use `docs/DEVELOPMENT-WORKFLOW.md` as a behavior-changing product change.

D022 and `docs/DEVELOPMENT-WORKFLOW.md` provide the common contract/branch/handoff rules. This document adds the stricter characterization-baseline requirements needed for refactoring. D052 controls authorship when the characterization baseline itself is a semantic conformance oracle.

## Why this workflow

Safe refactoring depends on small behavior-preserving transformations and a known-good verification baseline. Martin Fowler describes refactoring as a sequence of small behavior-preserving transformations; Google Engineering Practices similarly recommends separating refactorings from feature/bug changes and establishing tests before refactoring when coverage is missing.

D052 changes **who may author part of the baseline**, not the requirement that the baseline be independently executable and accepted before structural mutation.

## Refactor contract precondition

Executable refactoring MUST NOT begin until ChatGPT has:
1. classified the work as behavior-preserving;
2. defined the invariants that must remain true;
3. persisted the refactor Task Contract under `docs/tasks/`;
4. selected the D052 `Test-Authorship-Mode` when characterization ownership is material;
5. persisted/reviewed any required Orchestrator-owned characterization/conformance assets under `orchestrator-conformance` or `mixed`;
6. integrated that contract/controlling decisions/required oracle assets into `develop`;
7. launched the executor from a `develop` revision containing the contract and required frozen baseline assets.

The executor then creates the required `refactor/<slug>` topic branch from that revision.

Markdown-only refactors are performed by ChatGPT on a topic branch, but executable characterization/verification may still be delegated through a Task Contract. D052-designated non-Markdown conformance assets remain a narrow ChatGPT exception to normal non-Markdown Executor ownership.

D052 is prospective. Existing T032/T021 work is grandfathered and T022 may complete under its existing contract as stated by D052.

## RF0 — Classify and define invariants

ChatGPT determines that the work is genuinely behavior-preserving and records the invariants before structural mutation.

Examples:
- public protocol meaning unchanged;
- CLI/API behavior unchanged;
- installed footprint semantics unchanged;
- file/reference routing still resolves;
- Skill activation/operation semantics unchanged;
- no new permissions, dependencies, external effects, or compatibility requirements.

If changed behavior is desired or discovered as necessary, stop RF and use normal PD flow.

## RF1 — Characterization baseline checkpoint

Before structural mutation, the accepted behavior must be represented by a remotely auditable characterization baseline.

### `executor-implementation`

When the Task Contract assigns characterization authorship to the Executor, the Agente de IA Ejecutor MUST:
1. identify existing tests/evals that characterize the behavior;
2. add focused characterization tests/evals when material behavior is insufficiently covered;
3. execute the relevant suite against the pre-refactor state;
4. establish a green or explicitly isolated baseline;
5. persist the baseline evidence at the Task Contract-specified path, normally `handoffs/TNNN-rf1-baseline.json` when a separate checkpoint is required;
6. commit and push the baseline checkpoint to the remote refactor branch;
7. return only a minimal `PARTIAL` pointer to ChatGPT.

### `orchestrator-conformance` / `mixed`

When the refactor preserves semantics primarily defined by ChatGPT-owned normative content, ChatGPT owns the required semantic characterization/oracle assets designated by D052 and `docs/CONFORMANCE-ORACLE-CONTRACT.md`.

Preferred sequence:

```text
ChatGPT invariant contract
    -> required characterization/oracle assets
    -> review/integrate into develop
    -> Executor refactor branch from that exact baseline
    -> Executor supplementary technical characterization as useful
    -> Executor executes complete pre-refactor baseline
    -> persisted RF1 evidence
    -> ChatGPT baseline acceptance
```

The Executor remains responsible for execution, harness/environment mechanics, measurements/evidence and useful supplementary implementation/property/fuzz/edge-case characterization. It MUST NOT silently redefine expected outcomes, remove semantic negative controls, or change accepted baseline meaning.

A suspected semantic oracle defect uses the D052 `ORACLE_DEFECT` boundary. Purely mechanical correction is allowed only when the Task Contract/durable Orchestrator revision explicitly authorizes that correction class.

### Common RF1 evidence

Regardless of authorship mode, the baseline artifact must identify the task/refactor unit, branch, pushed HEAD/base, commands, results, relevant tests/evals/oracle identity, and any isolated pre-existing failures.

If the existing baseline is already complete and no Executor-owned test/eval files need to change, the Task Contract may allow the same refactor branch to persist only the baseline execution evidence before RF3.

### Baseline acceptance gate

ChatGPT reviews the pushed RF1 checkpoint through GitHub together with the controlling invariant contract and any D052 oracle identity.

RF3 MUST NOT begin until ChatGPT accepts the characterization baseline. Once accepted, the baseline meaning is frozen for that refactor unit.

ChatGPT may persist an explicit baseline-acceptance/review note or Task Contract/oracle lifecycle metadata. The executor cannot weaken, remove, or reinterpret the accepted baseline after RF3 starts unless ChatGPT explicitly authorizes a correction.

If baseline verification is failing:
- resolve the failure as separate work; or
- explicitly isolate a known unrelated failure before RF3.

Never hide a defect inside the refactor.

## RF2 — Atomic refactor contract

The persisted Task Contract decomposes the refactor into the smallest coherent, independently reviewable units practical.

Each unit states:
- target structure/code smell;
- behavior/invariants that remain unchanged;
- affected surface;
- explicit exclusions;
- accepted RF1 baseline/reference;
- D052 authorship/oracle identity when material;
- verification required after mutation.

Do not mix feature work, bug fixes, protocol behavior changes, dependency upgrades, or unrelated cleanup into the same refactor unit.

If decomposition changes materially after execution starts, ChatGPT persists an explicit Task Contract revision before work continues.

## RF3 — Apply refactor

### Executable/configuration/test infrastructure refactor

The Agente de IA Ejecutor performs the authorized non-Markdown refactor after RF1 acceptance, except that it does not semantically modify ChatGPT-owned D052 oracle assets without persisted authorization.

### Markdown/instruction refactor

ChatGPT performs the committed Markdown refactor. The Agente de IA Ejecutor may execute the frozen deterministic/eval verification when delegated.

No named executor product has special authority.

## RF4 — Verify and persist final handoff

After each atomic refactor unit, the executor runs:
- the frozen RF1 characterization/regression baseline, including any Orchestrator-owned D052 conformance assets;
- any additional non-contract-changing checks required by the Task Contract;
- useful Executor-owned supplementary technical checks added during implementation when applicable.

Required result: the same behavior contract remains satisfied.

Failure routing:
- implementation regression -> executor fixes within the frozen contract;
- genuine baseline/test/oracle defect -> stop and return to ChatGPT before changing baseline meaning;
- ambiguity over intended behavior -> stop and return to ChatGPT;
- discovered need for changed behavior -> terminate RF and return to PD0.

After verification, the executor persists the final `handoffs/TNNN-executor-handoff.json`, commits its authorized implementation/technical-test/handoff changes, and pushes the final refactor branch according to `docs/EXECUTOR-HANDOFFS.md`.

Never change the baseline merely because the new implementation prefers different behavior.

For higher-risk refactors ChatGPT MAY request rerun by a fresh executor session or a second compatible executor product. This remains the same logical executor role.

## RF5 — Orchestrator remote structural review

ChatGPT reviews the pushed branch, accepted baseline/oracle, final executor handoff, and actual diff.

Check at minimum:
- behavior remained stable;
- accepted RF1 baseline meaning remained intact;
- architecture/progressive-context boundaries remain coherent;
- duplication/indirection did not merely move;
- public compatibility did not change accidentally;
- complexity/coupling improved or stayed controlled;
- Markdown/D052-oracle/Executor write boundaries were respected;
- verification is green or all exceptions are explicitly understood;
- branch/PR target complies with `docs/BRANCHING.md`.

Green tests alone are not acceptance authority.

## RF6 — PR and integrate

Only after RF5 acceptance does ChatGPT normally create/review the PR from `refactor/<slug>` to `develop`.

Prefer squash merge for one coherent refactor unit. Each accepted unit must leave the repository working and reversible.

Promotion to `main` remains a separate release action.

## Special rule: Core Markdown refactoring

Because much of Governance Core is Markdown, structural wording moves can alter semantics even without code changes.

For Core Markdown:
- ChatGPT owns every wording/structure edit;
- semantic invariants are explicit before editing;
- under D052, ChatGPT also owns designated semantic conformance/characterization cases when those cases encode the accepted meaning being preserved;
- deterministic reference/layout checks and focused agent evals are used where appropriate;
- the Executor independently executes delegated executable verification and may add supplementary technical/adversarial coverage;
- moving normative rules must preserve authority, routing, direct references, and progressive-loading behavior;
- if wording changes interpretation, classify it as a protocol change rather than refactor.

## Core invariant

Refactor safety comes from a ChatGPT-owned invariant contract plus a remotely auditable pre-change characterization baseline whose semantic meaning cannot be silently moved after structural mutation begins. D052 determines authorship of the semantic oracle; the Executor remains responsible for independent execution and technical exploration.
