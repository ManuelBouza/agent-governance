# D082 — R029 Lean-Root and Transverse Skill Architecture

Status: ACCEPTED  
Date: 2026-09-13  
Authority: Human Owner / ChatGPT Orchestrator  
Research: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Evaluation: `docs/orchestrator/R029-PRE-DECISION-EVALUATION.md`; `docs/orchestrator/R029-E2-HOST-PARITY-FREEZE-D.md`; `docs/orchestrator/R029-E2-EMPIRICAL-DISPOSITION.md`; `docs/orchestrator/R029-E3-CONVERGENCE.md`  
Disposition: `ADOPT_WITH_CONDITIONS`  
Architecture-State: `ADOPTED`  
Materialization-State: `NOT_STARTED`  
Qualification-State: `POST_MATERIALIZATION_CONDITIONS_OPEN`

## Problem

R029 evaluated whether the current overloaded root `AGENTS.md` should be decomposed so that always-on authority and safety remain visible before routing, while Agent-Governance-specific workflows and genuinely reusable cross-project capabilities use progressive disclosure without creating Skill sprawl or host-specific semantic forks.

The completed pre-decision evidence establishes that the candidate preserves all audited root authority/safety semantics, retains distinct transverse intent boundaries, preserves cold-start and fail-closed behavior, and survives the complete scored Codex transverse-routing corpus without an authority/safety failure. The evidence also leaves three explicit uncertainties that concern later materialization and qualification rather than a demonstrated family-level topology defect.

A normative decision is therefore required to distinguish architecture adoption from later implementation and qualification.

## Decision

Agent Governance adopts the R029 candidate architecture **with explicit materialization and qualification conditions**.

The normative architecture is:

```text
lean always-loaded root AGENTS.md
  + one Agent Governance Maintainer top-level domain Skill
       -> Orchestrator internal route
       -> Executor internal route
  + five top-level transverse capabilities
       -> repository-change-control
       -> upstream-version-revalidation
       -> research-evidence-traceability
       -> durable-work-checkpoint
       -> executor-launch-handoff
            -> workspace-isolation internal route/reference
  + host-specific adapters/references only where mechanics differ
  + deterministic scripts/CI/references for mechanical enforcement
```

This adoption is at the **architecture/family level**. R029 E3 found no evidence requiring a family addition, removal, split, or merge before adoption. Accordingly, D082 does not introduce a topology revision relative to the E3 recommendation.

`ADOPT_WITH_CONDITIONS` means the architecture is now normative design authority, while claims about its actual production behavior, routing quality, context reduction, or cross-host equivalence remain bounded by the conditions and residuals below.

## Always-loaded root boundary

The future root `AGENTS.md` SHALL be lean, not empty and not a pointer-only file.

It SHALL preserve pre-routing representation for the authority/safety responsibility families established by R029, including repository identity, role/ownership, write authority, SDD and stop/re-entry safety, semantic-vs-mechanics separation, Human gates, durable authority, cold-start/bootstrap anchors, mutation and branch safety, handoff/evidence safety, Skill independence, and instruction-architecture guardrails.

The complete 79-unit R029 preservation ledger remains a materialization invariant:

```text
ROOT:       39
ROOT+ROUTE: 20
ROUTE:      20
TOTAL:      79
UNRESOLVED:  0
```

No materialization may delete an audited semantic obligation without an independently accepted normative change. Authority, ownership, safety, cold-start and fail-closed behavior MUST NOT depend on successful Skill activation.

## Maintainer domain boundary

Agent Governance SHALL retain **one** top-level Maintainer domain Skill for source-product maintenance, with internal Orchestrator and Executor routes.

Host identity and governance role are not equivalent routing dimensions. The Maintainer Skill SHALL NOT be split into top-level ChatGPT/Codex or Orchestrator/Executor Skills solely because the hosts or roles differ.

Agent-Governance-specific policy, accepted decision semantics, Task Contract/checkpoint/handoff vocabulary, stage ownership, write ownership, release/testing policy and repository-specific adapters remain domain authority. A transverse capability may structure a reusable workflow but cannot create or supersede that authority.

## Transverse capability boundary

The adopted top-level transverse capability families are exactly:

1. `repository-change-control`;
2. `upstream-version-revalidation`;
3. `research-evidence-traceability`;
4. `durable-work-checkpoint`;
5. `executor-launch-handoff`.

`workspace-isolation` remains an internal route/reference under `executor-launch-handoff`; for repository-backed work it consumes `repository-change-control` or repository-local policy for branch/base/integration/retirement constraints. It is not a sixth top-level capability.

No additional top-level transverse Skill is authorized merely because a workflow appears reusable. A later addition requires distinct intent, trigger/anti-trigger separation, a concrete postcondition, non-overlap, measurable routing/context/error-reduction value, and an explicit normative decision when it changes this architecture.

Generic coding, testing, pytest/TDD, Git-command, branching, Markdown-editing, SDD-stage, role-named, worktree-only and host-product top-level Skills remain outside this adopted topology absent new evidence and authority.

## Host-adapter and deterministic-mechanics boundary

The same reusable intent, semantic outcome and authority boundary SHALL use the same transverse capability across compatible hosts by default.

Host-specific adapters/references MAY differ for mechanical surfaces such as repository access, web/document access, session lifecycle, CLI/API/SDK invocation, workspace representation, persistence mechanics and user-visible navigation. Such mechanical differences do not create governance authority and do not justify divergent semantic Skills by themselves.

Deterministic behavior SHALL remain script/CI/reference-first where mechanical enforcement is appropriate. Skill activation is not a prerequisite for deterministic safety or correctness checks that can be enforced without model routing.

## Conditions for materialization and qualification

A later materialization/qualification objective SHALL preserve all of the following conditions:

1. Preserve the complete 79-unit R029 responsibility ledger with no authority deletion.
2. Keep pre-routing authority, ownership, safety, cold-start and fail-closed obligations independent of Skill activation.
3. Keep one Maintainer top-level domain Skill with internal Orchestrator/Executor routing unless new evidence independently justifies a later topology decision.
4. Keep the five adopted top-level transverse families and subordinate workspace-isolation relationship unless a later accepted decision changes them.
5. Validate actual Maintainer-domain activation and anti-trigger behavior on the materialized candidate; the historical `21/36` observation is not a qualification result.
6. Measure the actual materialized lean-root size, initial Skill catalog burden, representative conditional context load, duplicated normative text and reference-hop depth.
7. Preserve the frozen five-candidate transverse routing corpus and a zero authority/safety-failure expectation as regression evidence.
8. Do not repeat the existing 36 Codex trials merely for ceremony. Repetition is warranted only if materialized semantics/descriptions change materially or a later qualification authority explicitly requires fresh evidence.
9. Preserve the explicit limitation that paired ChatGPT/Codex empirical parity was not established by R029 E2.
10. Fail closed if materialization reveals an authority gap, routing ambiguity, topology conflict, or qualification result that materially contradicts the adopted design; such a finding requires normal re-entry rather than silent policy invention.

These are implementation and qualification conditions. They do not imply that E3 found a pre-adoption topology defect.

## Explicit unresolved residuals

D082 carries forward, without reinterpreting, these residuals:

```text
ChatGPT/Codex paired empirical parity:
  NOT_ESTABLISHED
  ChatGPT half = WAIVED_BY_HUMAN
  ChatGPT empirical trials = 0/36

Maintainer domain-route behavior:
  21/36 observed in Codex Freeze D evidence
  informational / unscored
  not qualified

Exact post-materialization root/catalog/context burden:
  NOT_MEASURED
```

These residuals prohibit stronger qualification claims than the evidence supports. They do **not** by themselves reopen the adopted family-level topology.

## Evidence basis and rejected alternatives

R029 provider-free evaluation preserved all 79 audited semantic units, produced a `30/30` static trigger/anti-trigger pass, preserved cold-start/fail-closed and adversarial authority boundaries, and found the five-family topology anti-sprawl coherent. Progressive disclosure passed structurally while exact quantitative burden remained unavailable before materialization.

Freeze D rescored 36 Codex transverse attempts as `36/36 PASS` with zero route mismatch, invalid trial, authority failure, or authority/safety violation. The subsequent Human disposition waived rather than passed the unexecuted ChatGPT half, so paired empirical parity remains unproven.

E3 explicitly found no semantic coverage hole, surviving transverse trigger collision, authority/safety failure, evidence for a sixth top-level capability, or evidence requiring Maintainer role/host splitting. Therefore:

- `REJECT` is not supported by the converged evidence;
- `REVISE_BEFORE_ADOPTION` is not supported by a demonstrated topology defect;
- unconditional/full-qualification adoption would overclaim the unresolved residuals;
- `ADOPT_WITH_CONDITIONS` is the evidence-consistent disposition.

## Relationship to existing authority

D082 adopts instruction/context architecture; it does not redefine source-maintenance role or execution ownership.

In particular, D082 preserves D052, D053, D054, D055, D057, D061, D067, D068, D076, D077, D080 and D081 unless a later accepted decision explicitly changes those rules. Current Markdown ownership and D068 Stage 5/6/7 ownership remain unchanged.

D082 is also independent of the R027/R028 Lean Executor production-adoption question controlled by D079/T066. It does not start T066, qualify Lean Executor, or modify D068 ownership policy.

## Materialization boundary

This decision does **not** itself:

- rewrite or slim production `AGENTS.md`;
- create, rename, package, install, publish or activate any production Skill;
- modify the current Maintainer Skill contract or package;
- integrate the R029 scientific evaluation branch into production;
- launch an Executor/Codex session;
- authorize or consume a provider/model call;
- start T066 Stage 5;
- adopt R030 or any other unrelated research line.

Productive materialization is a separate Human-selected objective under D067 and must follow the then-current source-maintenance, branching, SDD, qualification and re-entry rules.

## Effective rule

```text
R029 family-level architecture
  -> ADOPTED_WITH_CONDITIONS

production materialization
  -> NOT_STARTED

qualification claims
  -> limited to evidence actually established

R029 residuals
  -> explicit and carried forward
  -> not silently converted to PASS

future contradictory material evidence
  -> fail closed
  -> normal re-entry / later normative change if needed
```
