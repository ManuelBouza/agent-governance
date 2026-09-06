# Refactoring Workflow

Status: ACTIVE

## Purpose

Define the repository-specific workflow for restructuring `agent-governance` without changing externally observable behavior or governance semantics.

A change that intentionally changes behavior, protocol semantics, authority, compatibility, or acceptance outcomes is NOT a refactor and must use `docs/DEVELOPMENT-WORKFLOW.md` as a behavior-changing product change.

D022 and `docs/DEVELOPMENT-WORKFLOW.md` provide the common contract/branch/handoff rules. This document adds the stricter characterization-baseline requirements needed for refactoring. D052 controls semantic-oracle ownership. D068 prospectively controls Stage 5/6 ownership and publication sequencing for refactors operating in D068 mode.

## D068 refactor normalization

For a new D068-mode refactor:

```text
RF0 / invariant authority / Plan & Trace
    -> ChatGPT Orchestrator
accepted preserved-behavior/oracle meaning
    -> ChatGPT Orchestrator
Stage 5 complete refactor candidate materialization
    -> ChatGPT Orchestrator
publish coherent candidate + authority on verified topic branch
    -> GitHub topic branch
Stage 6 execute frozen baseline / diagnose / bounded repair / verify
    -> Agente de IA Ejecutor
Stage 7 converge / accept / integrate / evolve
    -> ChatGPT Orchestrator
```

A coherent published topic-branch candidate is sufficient authority for D068 Stage 6; no separate planning/candidate merge into `develop` is required first. D052 semantic-oracle ownership and D054 execution mechanics remain intact.

A new D068-mode refactor does not launch an Executor merely to create the Stage 5 candidate. If a pre-mutation Executor characterization checkpoint is indispensable to a particular persisted task topology, that work must be explicitly grandfathered/non-D068 or otherwise governed by already accepted authority; this document does not invent a new exception to D068.

Any later unqualified wording in this document that assigns first-pass RF3 source mutation to the Executor or requires planning/oracle integration into `develop` before candidate materialization retains only historical/grandfathered or explicitly non-D068 scope. Historical executed Task Contracts, baselines, handoffs, reviews, and evidence are not rewritten retroactively.

## Why this workflow

Safe refactoring depends on small behavior-preserving transformations and a known-good verification baseline. Martin Fowler describes refactoring as a sequence of small behavior-preserving transformations; Google Engineering Practices similarly recommends separating refactorings from feature/bug changes and establishing tests before refactoring when coverage is missing.

D052 changes **who owns semantic baseline meaning**, not the requirement that the baseline be independently executable and accepted before structural mutation where the controlling refactor contract requires that gate. D068 changes who materializes the candidate and when the Executor enters for new D068-mode work.

## Refactor contract precondition

For D068-mode executable refactoring, ChatGPT MUST before Stage 6:
1. classify the work as behavior-preserving;
2. define the invariants that must remain true;
3. persist the refactor Task Contract under `docs/tasks/`;
4. select the D052 `Test-Authorship-Mode` when characterization ownership is material;
5. persist/review any required Orchestrator-owned characterization/conformance assets under `orchestrator-conformance` or `mixed`;
6. establish the accepted preserved-behavior meaning needed before mutation;
7. materialize the complete Stage 5 refactor candidate on a verified short-lived topic branch;
8. publish that coherent authority/candidate checkpoint to GitHub.

The Executor then uses that exact published topic branch for Stage 6 execution, diagnosis, bounded technical repair, and verification. D061/D062 freshness/protection rules remain mandatory.

Explicit grandfathered/non-D068 refactors retain any persisted preimplementation `develop` integration gate they already require.

Markdown-only refactors are performed by ChatGPT on a topic branch. D068 does not require an Executor merely for Markdown-only verification ceremony; executable verification is delegated only when it is genuinely applicable.

D052 and D068 are prospective. Existing historical work retains its original contract meaning.

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

## RF1 — Characterization baseline authority

Before structural mutation, the accepted behavior must be represented by an auditable characterization baseline or equivalent preserved-behavior authority sufficient for the selected SDD/refactor profile.

### D068 mode

ChatGPT owns the preserved-behavior meaning and any D052 semantic characterization/oracle assets. The baseline authority is frozen before Stage 5 candidate mutation. Existing trustworthy remote test/eval evidence may be referenced when the Task Contract makes that sufficient; a new Executor pre-mutation run is not invented merely to preserve the old topology.

If the Task Contract genuinely requires new pre-mutation execution evidence that only the Executor can produce before a safe candidate can be materialized, classify and persist the required non-D068/grandfathered topology explicitly rather than silently violating D068.

### Explicit grandfathered/non-D068 `executor-implementation`

When persisted authority assigns pre-refactor characterization authorship/execution to the Executor, the Agente de IA Ejecutor MUST follow that contract, including identifying/adding focused characterization coverage, executing the pre-refactor suite, persisting the baseline artifact, and publishing the required checkpoint before structural mutation.

### `orchestrator-conformance` / `mixed`

When the refactor preserves semantics primarily defined by ChatGPT-owned normative content, ChatGPT owns the required semantic characterization/oracle assets designated by D052 and `docs/CONFORMANCE-ORACLE-CONTRACT.md`.

For D068 mode the normalized sequence is:

```text
ChatGPT invariant contract + semantic oracle meaning
    -> freeze accepted preserved-behavior authority
    -> ChatGPT Stage 5 refactor candidate
    -> publish coherent candidate checkpoint
    -> Executor Stage 6 executes frozen baseline + supplementary technical checks
    -> persisted verification/repair evidence
    -> ChatGPT convergence acceptance
```

The Executor remains responsible for Stage 6 execution, harness/environment mechanics, measurements/evidence and useful supplementary technical characterization. It MUST NOT silently redefine expected outcomes, remove semantic negative controls, or change accepted baseline meaning.

A suspected semantic oracle defect uses the D052 `ORACLE_DEFECT` boundary. Purely mechanical correction is allowed only when the Task Contract/durable Orchestrator revision explicitly authorizes that correction class.

### Common RF1 evidence

When the controlling contract requires a persisted RF1 evidence artifact, it identifies the task/refactor unit, branch, pushed HEAD/base, commands, results, relevant tests/evals/oracle identity, and any isolated pre-existing failures.

### Baseline acceptance gate

ChatGPT accepts/fixes the preserved-behavior meaning before Stage 5 structural mutation. Once accepted, the baseline meaning is frozen for that refactor unit.

The Executor cannot weaken, remove, or reinterpret the accepted baseline during Stage 6 unless ChatGPT explicitly authorizes a semantic correction through re-entry.

If baseline semantics are ambiguous or known failing behavior cannot be isolated safely, resolve that as separate work or classify the objective outside D068/refactor mode rather than hiding a defect inside the refactor.

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

## RF3 — Apply refactor candidate

### D068 executable/configuration/test-infrastructure refactor

ChatGPT Orchestrator materializes the complete authorized non-Markdown refactor candidate during Stage 5, including source/config/test changes required by the approved refactor Design/Plan. D052 semantic-oracle meaning remains separately protected.

The Executor does not recreate that candidate. During Stage 6 it may make bounded technical repairs only when they preserve the approved refactor semantics/Design and frozen behavior baseline.

### Explicit grandfathered/non-D068 executable refactor

Where a historical or persisted contract explicitly assigns first-pass source mutation to the Executor, preserve that authority for that work only. Do not generalize it to new D068-mode tasks.

### Markdown/instruction refactor

ChatGPT performs the committed Markdown refactor. The Agente de IA Ejecutor may execute frozen deterministic/eval verification when genuinely delegated as Stage 6 work.

No named executor product has special authority.

## RF4 — Verify and persist final handoff

For D068-mode executable refactors, the Executor runs against the published Stage 5 candidate:
- the frozen RF1 characterization/regression baseline, including any Orchestrator-owned D052 conformance assets;
- any additional non-contract-changing checks required by the Task Contract;
- useful supplementary technical checks;
- affected verification again after any bounded technical repair.

Required result: the same behavior contract remains satisfied.

Failure routing:
- technical implementation regression -> Executor may repair within the frozen contract and rerun affected verification;
- genuine baseline/test/oracle semantic defect -> stop and return to ChatGPT before changing baseline meaning;
- ambiguity over intended behavior -> stop and return to ChatGPT;
- discovered need for changed behavior -> terminate RF and return to PD0.

After verification, the Executor persists the final `handoffs/TNNN-executor-handoff.json`, commits its authorized Stage 6 repair/test/handoff changes, and pushes the final refactor branch according to `docs/EXECUTOR-HANDOFFS.md`.

Never change the baseline merely because the new implementation prefers different behavior.

For higher-risk refactors ChatGPT MAY request rerun by a fresh Executor session or a second compatible Executor product. This remains the same logical Executor role.

## RF5 — Orchestrator remote structural review

ChatGPT reviews the pushed branch, accepted baseline/oracle, final Executor handoff, and actual diff.

Check at minimum:
- behavior remained stable;
- accepted RF1 baseline meaning remained intact;
- architecture/progressive-context boundaries remain coherent;
- duplication/indirection did not merely move;
- public compatibility did not change accidentally;
- complexity/coupling improved or stayed controlled;
- D068/D052/Markdown/Executor ownership boundaries were respected;
- verification is green or all exceptions are explicitly understood;
- branch/PR target complies with `docs/BRANCHING.md`.

Green tests alone are not acceptance authority.

## RF6 — PR and integrate

Only after RF5 acceptance does ChatGPT normally create/review the PR from the refactor topic branch to `develop`.

Prefer squash merge for one coherent refactor unit. Each accepted unit must leave the repository working and reversible.

Promotion to `main` remains a separate release action.

## Special rule: Core Markdown refactoring

Because much of Governance Core is Markdown, structural wording moves can alter semantics even without code changes.

For Core Markdown:
- ChatGPT owns every wording/structure edit;
- semantic invariants are explicit before editing;
- under D052, ChatGPT also owns designated semantic conformance/characterization meaning when those cases encode the accepted meaning being preserved;
- deterministic reference/layout checks and focused agent evals are used where appropriate;
- the Executor independently executes delegated executable verification and may add supplementary technical/adversarial coverage inside Stage 6 authority;
- moving normative rules must preserve authority, routing, direct references, and progressive-loading behavior;
- if wording changes interpretation, classify it as a protocol change rather than refactor.

D068 does not change Governance Core or consumer-project SDD semantics merely because the source repository uses this maintenance workflow.

## Core invariant

Refactor safety comes from a ChatGPT-owned invariant contract plus an auditable frozen preserved-behavior baseline whose semantic meaning cannot be silently moved after structural mutation begins. In D068 mode ChatGPT materializes the complete candidate, the Executor independently executes/diagnoses/bounded-repairs/verifies it, and ChatGPT retains final convergence/acceptance/integration authority.
