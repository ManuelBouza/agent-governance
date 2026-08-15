# Agent Capability Engineering (ICAE)

Status: ACTIVE
Controlling decision: `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`

## Purpose

ICAE is the risk-routed engineering/assurance method for capabilities consumed by agents in Agent Governance.

> **ICAE treats an agent-consumed capability as a composed software artifact: specify authority and contracts, deterministically enforce hard invariants, demonstrate model-mediated behavior with repeated evaluations, and release only reproducible, traceable, Governance-accepted artifacts.**

ICAE extends the existing source-development workflow; it does not create a parallel task lifecycle.

## Assurance routing

Choose verification from the property being claimed, not from a fixed checklist.

| Property | Minimum honest assurance |
|---|---|
| machine-decidable hard invariant | deterministic validator/test/control |
| protocol/state transition space | property/state-machine tests |
| Skill/profile activation or routing | repeated positive/negative/near-miss evals |
| semantic/model-mediated behavior | behavioral eval + objective assertions where possible |
| security boundary | deterministic permissions/isolation + adversarial verification |
| host/model-dependent compatibility | supported host/model matrix |
| architecture/authority/risk | Human/Orchestrator review |
| distribution/package | isolation, reproducibility, identity/provenance evidence |

A deterministic-only refactor does not acquire model eval requirements merely because agents use the repository. Conversely, a Skill description/routing change cannot use deterministic tests alone to claim activation quality.

## Task Contract application

When material to the task, Task Contracts MAY declare:

```text
Assurance-Class: deterministic | model-mediated | mixed
Baseline: <accepted characterization / prior artifact / no-skill / none>
Verification-Planes: <static, deterministic, property, routing, behavioral, security, portability, package>
Release-Impact: none | compatibility | behavior | security | distribution
Context-Impact: none | bootstrap | routing | focused | distribution
Context-Baseline: <accepted context baseline when applicable>
```

Do not add fields that do not affect task assurance. These fields classify an existing Task Contract; they do not authorize scope.

## Acceptance criterion -> evidence traceability

Material acceptance criteria SHOULD have stable identifiers when several evidence planes or rework cycles make ambiguity plausible.

Each material criterion must be reviewable against evidence that directly supports the property claimed. Evidence should state its type where confusion is possible.

Examples:

```text
AC-PKG-1 -> package/isolation -> artifact bootstrap with source absent
AC-CLI-1 -> executed-successfully -> direct command execution
AC-NEG-1 -> negative-control -> unsupported profile rejected
AC-REP-1 -> reproducibility -> repeated build identity equality
```

`listed`, `importable`, `surface-present`, `--help-visible`, or analogous evidence MUST NOT be treated as successful execution when the criterion requires execution.

Green tests are evidence, not acceptance authority.

## Lifecycle integration

Use the existing D022 workflow:

```text
intent/research
  -> decision / Task Contract where needed
  -> baseline + assurance classification
  -> design / author / implement
  -> static validation
  -> required deterministic/property/eval/security/package planes
  -> Orchestrator acceptance
  -> reproducible integration/package/release evidence
  -> observation
  -> regression capture / EGLL when warranted
```

Stages that do not apply are omitted deliberately; they are not performed as ceremony.

## Evaluator discipline

Prefer code assertions for objective properties. Use model graders only where semantic judgment is genuinely required, and pair them with objective evidence/human review when material.

LLM-as-judge output MAY support a decision. It MUST NOT independently become Governance acceptance, architecture or release authority.

## Repository context architecture

`docs/CONTEXT-ARCHITECTURE.md` defines the RCAB assurance dimension for source-repository information architecture.

Context efficiency is a quality property, not a justification for deleting required safety/authority information. Optimize retrieval/load paths while preserving one canonical authority and auditable Git history.

## EGLL

Failures and near misses that reveal reusable assurance gaps feed `docs/GOVERNANCE-LEARNING.md`.

A learning is not `VERIFIED` because ICAE names a control. Verification still requires integrated control plus bad-case/good-case replay evidence where the class is deterministically representable.
