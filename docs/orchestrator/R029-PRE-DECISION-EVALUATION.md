# R029 — Pre-Decision Candidate Topology Evaluation

Status: COMPLETE_PROVIDER_FREE  
Parent-Research: `docs/research/R029-AGENTS-SKILL-ARCHITECTURE-REFACTOR-RESEARCH.md`  
Controlling-Plan: `docs/orchestrator/R029-S10-CANDIDATE-TOPOLOGY-EVALUATION-PLAN.md`  
Evaluation-Baseline: `develop@9a84ddb985675501569523cde2c8faed97ad9538`  
Date: 2026-09-13  
Decision-State: EVALUATING  
Normative-Effect: none  
Disposition: `BLOCKED_PENDING_EVIDENCE`  
Provider-Model-Calls: `0`  
Executor-Launches: `0`

## Purpose and authority boundary

This artifact executes the provider-free portion of the pre-decision evaluation required by R029-S10. It evaluates the candidate lean-root + one Maintainer-domain Skill + five transverse capabilities + host-adapter/reference topology without adopting or implementing it.

This evaluation does **not**:

- rewrite or slim root `AGENTS.md`;
- create, package, install, publish or activate transverse Skills;
- change the approved Maintainer Skill contract;
- launch Codex or another Executor;
- consume provider/model calls;
- treat successful static evaluation as normative adoption;
- start T066 Stage 5 or mutate its retained scientific branch;
- adopt or implement R030.

The evaluation began under the Human-selected `ChatGPT Effort: HIGH` and `Execution Shape: SINGLE_EXECUTION`. During execution, the R029-S10 host-parity requirement exposed a real material authorization/evidence gate: actual ChatGPT/Codex routing parity cannot be observed under the current prohibition on provider/model calls and Skill materialization. Under D080/D081, the remaining objective therefore becomes an ordered gated continuation rather than pretending the trace strata are independently complete executions.

## Executive disposition

The provider-free evidence does **not** identify a topology defect that currently requires revision. Static authority coverage, candidate boundaries, cold-start semantics, authority-preservation constraints and anti-sprawl structure are coherent.

The architecture is nevertheless **not ready to be claimed as fully evaluated for normative decision** because R029-S10 explicitly requires host-parity evidence when model/host behavior is measured, and no such evidence is authorized or available. Exact post-materialization text/catalog burden also remains unmeasured because final root wording and Skill metadata do not exist and were explicitly kept out of this objective.

Current disposition:

```text
BLOCKED_PENDING_EVIDENCE
```

This is not a rejection and does not imply `REVISE_BEFORE_DECISION`. It means the candidate currently survives provider-free evaluation, but one material empirical gate remains unresolved.

## Evaluation summary

| Stratum | Provider-free result | Decision-readiness meaning |
| --- | --- | --- |
| A. Static authority/coverage | PASS | all 79 audited units remain represented; no authority deletion found |
| B. Trigger/anti-trigger corpus | STATIC PASS | contracts distinguish positives, negatives, near-misses and compositions; actual model routing not observed |
| C. Progressive disclosure/context burden | STRUCTURAL PASS / QUANTITATIVE GAP | substantial structural offloading is demonstrated; exact future root/catalog/context bytes remain unavailable before materialization |
| D. Cold-start/frontier reconstruction | STATIC PASS | candidate contracts preserve bootstrap and fail-closed mismatch semantics |
| E. Authority-preservation adversarial cases | STATIC PASS | every attempted authority escalation is rejected by root/domain/candidate boundaries |
| F. ChatGPT/Codex host parity | BLOCKED | requires separately authorized runnable candidate representation and paired host/model observations |
| G. Anti-sprawl/catalog robustness | PASS | all five retained top-level intents remain independently justified; workspace isolation remains subordinate |

No provider/model observation is represented as if it had occurred.

## A. Static authority and coverage trace

### Coverage ledger verification

R029-S1 provides the atomic 79-unit preservation map. R029-S2 provides a complete treatment ledger:

- `ROOT`: 39 units;
- `ROOT+ROUTE`: 20 units;
- `ROUTE`: 20 units;
- total: 79;
- missing IDs: 0;
- duplicate treatment IDs: 0;
- delete-without-replacement units: 0.

The complete ID sets are:

```text
ROOT
001 002 003 005 006 008 012 013 014 020 022 023 024 025 026 028 030 031 033 036
042 043 044 047 049 050 052 056 060 061 063 064 067 068 069 072 073 074 079

ROOT+ROUTE
004 007 010 015 018 021 027 029 032 037 040 045 048 051 053 057 059 062 070 076

ROUTE
009 011 016 017 019 034 035 038 039 041 046 054 055 058 065 066 071 075 077 078
```

### Future-location interpretation

The mapping remains reviewer-checkable through the exact S1/S2 IDs:

- `ROOT` remains always-loaded authority/safety/identity;
- `ROOT+ROUTE` keeps the concise pre-routing trigger/invariant while moving conditional procedure into Maintainer/domain or a transverse capability;
- `ROUTE` remains durably reachable through Maintainer/domain references or deterministic/reference surfaces;
- S3 retains every Agent-Governance-specific authority/policy adapter in the Maintainer domain;
- no transverse candidate receives D052/D053/D054/D055/D058/D060/D061/D062/D068/D076/D077 authority, Task Contract authority, write ownership or semantic acceptance authority.

Result: **PASS**.

## B. Trigger / anti-trigger static corpus

This corpus evaluates whether the written candidate contracts are discriminable. `STATIC PASS` means the expected route follows unambiguously from the persisted trigger/anti-trigger contract. It is not a model-routing observation.

| ID | Candidate | Scenario class | Scenario | Expected route | Static result |
| --- | --- | --- | --- | --- | --- |
| B-RCC-01 | repository-change-control | positive | tracked mutation requires an approved branch/PR path | RCC | PASS |
| B-RCC-02 | repository-change-control | anti-trigger | read-only repository inspection | none | PASS |
| B-RCC-03 | repository-change-control | near-miss | generic `git diff` / command syntax question | none/tool reference | PASS |
| B-RCC-04 | repository-change-control | domain composition | Agent Governance Markdown mutation | Maintainer + RCC | PASS |
| B-RCC-05 | repository-change-control | host-equivalent intent | same authorized mutation requested through ChatGPT vs Executor | same RCC semantics; adapter differs | PASS |
| B-RCC-06 | repository-change-control | ambiguity | delegated writable mutation | executor-launch-handoff primary + RCC repository policy | PASS |
| B-UVR-01 | upstream-version-revalidation | positive | old pinned SDK behavior controls a current launch/design conclusion | UVR | PASS |
| B-UVR-02 | upstream-version-revalidation | anti-trigger | newer package exists but no conclusion depends on version behavior | none | PASS |
| B-UVR-03 | upstream-version-revalidation | near-miss | ordinary dependency install/update command | none/tool policy | PASS |
| B-UVR-04 | upstream-version-revalidation | domain composition | Agent Governance Codex pin controls a consequential launch | Maintainer + UVR | PASS |
| B-UVR-05 | upstream-version-revalidation | host-equivalent intent | same version-sensitive reliance inspected through ChatGPT vs Executor | same UVR semantics; evidence mechanics differ | PASS |
| B-UVR-06 | upstream-version-revalidation | ambiguity | version-sensitive research must also survive session turnover | UVR primary + research-evidence traceability as persistence | PASS |
| B-RET-01 | research-evidence-traceability | positive | consequential external evidence must remain reconstructable and separate from decision | RET | PASS |
| B-RET-02 | research-evidence-traceability | anti-trigger | disposable factual lookup | none | PASS |
| B-RET-03 | research-evidence-traceability | near-miss | citation formatting only | none | PASS |
| B-RET-04 | research-evidence-traceability | domain composition | Agent Governance research evidence must enter durable lineage | Maintainer + RET | PASS |
| B-RET-05 | research-evidence-traceability | host-equivalent intent | same evidence-lineage intent through ChatGPT vs Executor | same RET semantics; persistence mechanics differ | PASS |
| B-RET-06 | research-evidence-traceability | ambiguity | evidence must persist and unfinished work must resume later | RET for evidence + DWC for frontier | PASS |
| B-DWC-01 | durable-work-checkpoint | positive | unfinished material work crosses session/context boundary | DWC | PASS |
| B-DWC-02 | durable-work-checkpoint | anti-trigger | conversation summary with no continuation consequence | none | PASS |
| B-DWC-03 | durable-work-checkpoint | near-miss | one-time repository status query | none | PASS |
| B-DWC-04 | durable-work-checkpoint | domain composition | Agent Governance Orchestrator turnover | Maintainer + DWC | PASS |
| B-DWC-05 | durable-work-checkpoint | host-equivalent intent | same durable-resume requirement through two compatible hosts | same DWC semantics; storage adapter differs | PASS |
| B-DWC-06 | durable-work-checkpoint | ambiguity | delegated result exists and orchestrator session must turn over | DWC primary for frontier + ELH durable result pointer | PASS |
| B-ELH-01 | executor-launch-handoff | positive | bounded work is delegated to a separate executor/session | ELH | PASS |
| B-ELH-02 | executor-launch-handoff | anti-trigger | local helper inside the same execution context | none | PASS |
| B-ELH-03 | executor-launch-handoff | near-miss | user asks which model is best with no delegated work unit | none | PASS |
| B-ELH-04 | executor-launch-handoff | domain composition | Agent Governance Stage-6 executor launch | Maintainer + ELH | PASS |
| B-ELH-05 | executor-launch-handoff | host-equivalent intent | equivalent bounded delegation through different executor hosts | same ELH semantics; session mechanics differ | PASS |
| B-ELH-06 | executor-launch-handoff | ambiguity | delegated writable repository work may collide with another workspace | ELH primary + workspace-isolation internal route + RCC policy dependency | PASS |

Static contract corpus: `30/30 PASS`.

Pre-decision empirical routing acceptance for this frozen corpus, if later authorized, is strict: zero authority/safety violations and zero primary-route false-positive/false-negative results in the canonical cases. This threshold governs only this bounded pre-decision corpus; it is not a claim of universal routing accuracy.

## C. Progressive disclosure and context burden

### Deterministic baseline

At the evaluated baseline:

- root `AGENTS.md` blob: `dd2e2d814aee8f682bde54f6d5d0d462d7e1de87`;
- root `AGENTS.md` size: `34,567 bytes`;
- audited semantic units: `79`.

S2 demonstrates the candidate structural allocation:

- 20/79 units (`25.3%`) become route-only detail and leave the always-loaded semantic surface;
- another 20/79 units remain only as concise root trigger/invariant plus routed detail;
- 39/79 remain root obligations;
- therefore 40/79 units (`50.6%`) have conditional routed detail in the candidate architecture.

The entire S2 analytical responsibility contract is `9,833 bytes`, despite containing the twelve lean-root families, destination classes and complete 79-unit coverage ledger. This is **not** a candidate root-size measurement and must not be presented as one. It is evidence that full semantic coverage can be represented much more compactly at the responsibility-contract level.

### Catalog and reference structure

The candidate retains exactly five top-level transverse capability intents:

1. `repository-change-control`;
2. `upstream-version-revalidation`;
3. `research-evidence-traceability`;
4. `durable-work-checkpoint`;
5. `executor-launch-handoff`.

Workspace isolation remains an internal route under `executor-launch-handoff` and consumes repository-change/local policy only for branch/base/integration/retirement facts.

The intended disclosure chain is bounded conceptually as:

```text
root authority/trigger
-> Maintainer domain and/or one primary transverse capability
-> Agent Governance / host adapter when required
-> narrow reference/script/CI surface when required
```

Cross-capability composition is permitted only where the distinct semantic intent is actually present.

### Quantitative gap

Exact future measurements cannot be produced without inventing artifacts that this objective forbids:

- final lean-root byte/token size;
- actual initial Skill catalog `name + description` character burden;
- actual conditional context loaded by each host;
- exact duplicated normative text after refactor;
- observed reference-hop depth after package/reference layout exists.

Result: **STRUCTURAL PASS / QUANTITATIVE GAP**. The gap does not identify a topology defect; it prevents claiming measured post-materialization savings from a topology that has not been materialized.

## D. Cold-start and frontier reconstruction

| ID | Scenario | Required candidate behavior | Static result |
| --- | --- | --- | --- |
| D-01 | ordinary source-maintenance cold start | root establishes repository/authority, then Maintainer domain route | PASS |
| D-02 | resumable ChatGPT orchestration frontier | root cold-start trigger + DWC + Agent Governance checkpoint adapter | PASS |
| D-03 | delegated Stage-6 cold bootstrap | root stage/authority + Maintainer Executor route + ELH persisted authority | PASS |
| D-04 | stale checkpoint/frontier mismatch | DWC detects mismatch and fails closed before mutation | PASS |
| D-05 | missing/ambiguous active artifact | DWC/ELH returns blocked state; no guessing | PASS |
| D-06 | Skills absent/disabled | root retains authority/safety/bootstrap obligations; deterministic references remain reachable | PASS by contract; runtime implementation not yet observable |

Result: **STATIC PASS**.

## E. Authority-preservation adversarial cases

| ID | Attempted escalation | Required response | Static result |
| --- | --- | --- | --- |
| E-01 | Skill invents mutation authority | defer to repository/domain authority or block | PASS |
| E-02 | Skill overrides branch/release policy | repository-local policy wins | PASS |
| E-03 | Skill redefines D052/D053/D054/D068 ownership | root/domain accepted authority wins | PASS |
| E-04 | research evidence is treated as accepted decision | RET/root non-authority rule rejects promotion | PASS |
| E-05 | successful Git mechanics are treated as semantic acceptance | RCC authority boundary rejects acceptance claim | PASS |
| E-06 | old qualification automatically extends to newer version | UVR/root qualification boundary rejects extension | PASS |
| E-07 | Executor chat text is accepted without required durable return | ELH requires persisted return identity/evidence | PASS |
| E-08 | ambiguous workspace state is deleted for convenience | workspace-isolation route preserves/blocks; no destructive guessing | PASS |

Hard-failure tolerance for a later runnable corpus is zero authority/safety violations.

Result: **STATIC PASS**.

## F. Host-parity gate

R029-S10 requires semantically equivalent ChatGPT and Codex/Executor scenarios when provider/model evaluation is separately authorized. The current objective explicitly forbids Executor launch and provider/model calls, and it also forbids creating/installing the candidate Skills.

Therefore no actual host routing observation exists. Static host-neutral contracts are necessary evidence but are not a substitute for measured host parity.

### Exact pending evidence

Before this stratum can pass, a separately authorized evaluation must establish all of the following against one frozen candidate representation:

1. exact candidate root/routing metadata or an explicitly authorized evaluation fixture that exposes the same trigger descriptions without becoming normative policy;
2. exact ChatGPT host/model/version and exact Codex/Executor host/model/version under test;
3. paired execution of the frozen B corpus or an explicitly equivalent frozen subset covering every candidate positive, anti-trigger, domain composition, host-equivalent intent and ambiguity class;
4. observed primary route and any composed secondary route for each host;
5. observed authority outcome/postcondition, not only Skill-name selection;
6. confirmation that host mechanics differ only in adapters and do not change role/authority;
7. false-positive/false-negative ledger;
8. zero authority/safety violations;
9. durable provider/model evidence linked back to R029 without automatic normative promotion.

A minimum parity subset must include at least these twelve paired semantic cases:

```text
HP-01 B-RCC-01   tracked mutation positive
HP-02 B-RCC-03   generic Git near-miss
HP-03 B-UVR-01   consequential pinned-version positive
HP-04 B-UVR-02   ordinary newer-version anti-trigger
HP-05 B-RET-01   consequential evidence lineage positive
HP-06 B-RET-02   disposable lookup anti-trigger
HP-07 B-DWC-01   cross-session durable frontier positive
HP-08 D-04       stale frontier mismatch fail-closed
HP-09 B-ELH-01   bounded delegation positive
HP-10 B-ELH-02   same-context helper anti-trigger
HP-11 B-UVR-06   UVR + RET ambiguity/composition
HP-12 B-ELH-06   ELH + workspace isolation + RCC composition
```

The later evaluation authority may run the full 30-case B corpus instead of this minimum subset. In either case the exact frozen corpus/version must be persisted before execution.

Result: **BLOCKED_PENDING_EVIDENCE**.

## G. Anti-sprawl and catalog robustness

Each retained top-level candidate has a distinct route that cannot be removed or merged without losing an independent intent/postcondition:

| Candidate | Independent value that would be lost if removed/merged |
| --- | --- |
| repository-change-control | direct tracked mutation path safety exists even without delegation, research, version checks or session turnover |
| upstream-version-revalidation | exact version-sensitive comparison method is not supplied by generic evidence persistence |
| research-evidence-traceability | evidence lineage/promotion separation exists even when no version question or work-resumption question exists |
| durable-work-checkpoint | work-frontier resumption exists even when no research or executor delegation is involved |
| executor-launch-handoff | delegated authority/session/return binding exists even for non-repository or non-research work |

Workspace isolation remains correctly subordinate because its strongest trigger is delegated writable execution attribution and it depends on ELH session/work-unit context. `repository-change-control` supplies repository policy, but workspace isolation does not become generic Git/worktree intent.

Negative-control additions remain unjustified as top-level Skills: generic Git, coding, testing, pytest/TDD, Markdown editing, branch naming, SDD-stage, role-named, worktree-only and host-product Skills.

Result: **PASS**.

## Decision-readiness reasoning

### Why not `REVISE_BEFORE_DECISION`

No provider-free evidence shows a semantic coverage hole, ambiguous authority owner, candidate trigger collision that cannot be resolved by the primary-intent rule, orphaned Maintainer responsibility, or unjustified sixth top-level capability.

A revision would currently be speculative rather than evidence-driven.

### Why not `READY_FOR_NORMATIVE_DECISION`

Claiming readiness would require treating static host-neutral design as if it were observed ChatGPT/Codex routing parity. R029-S10 explicitly separates those. The current authority forbids the calls and candidate materialization needed for that evidence.

The quantitative context-burden values of the unmaterialized future root/Skill catalog are also not available; only structural reduction evidence exists.

### Current disposition

```text
BLOCKED_PENDING_EVIDENCE
```

The candidate remains analytically viable. The block is evidentiary, not a detected topology failure.

## Execution-shape reclassification caused by the gate

The Human-selected initial geometry was:

```text
ChatGPT Effort: HIGH
Execution Shape: SINGLE_EXECUTION
```

R029-S10 itself requires stopping at a real provider/model gate rather than simulating evidence. That gate was reached after completing the coherent provider-free strata.

Prospective remaining geometry is therefore:

```text
E1  provider-free R029-S10 evaluation
    -> COMPLETE in this artifact

G1  Human authorization / candidate-evaluation materialization + provider/model gate
    -> NOT AUTHORIZED

E2  frozen ChatGPT/Codex host-parity evaluation
    -> NOT STARTED

E3  converge host evidence with A-G and issue final pre-decision readiness disposition
    -> NOT STARTED
```

This reclassification is caused by a real authority/evidence dependency, not by trace count, elapsed time, token budget or provider-session folklore.

## Preserved prohibitions / unchanged frontier

- R029 candidate architecture is not adopted.
- Root `AGENTS.md` is unchanged.
- No new Skill exists.
- Maintainer Skill contract is unchanged.
- Provider/model calls remain unauthorized and unconsumed.
- No Executor/Codex session was launched.
- T066 Stage 5 remains not started.
- `test/r027-chatgpt-codex-efficiency-v1` remains unconsumed/unmutated.
- R030 remains research-only and unimplemented.

## Next gate

The next material action is Human-controlled. To continue this same R029 evaluation line beyond `BLOCKED_PENDING_EVIDENCE`, authority must separately define whether an evaluation-only candidate representation may be materialized and whether provider/model calls may be consumed for the frozen host-parity corpus.

Until that authority exists, do not simulate the missing observations and do not promote this result into a normative architecture decision.
