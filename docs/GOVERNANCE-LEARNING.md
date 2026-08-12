# Governance Learning Procedure

Status: ACTIVE

## Purpose

Define the source-maintenance Evidence-Driven Governance Learning Loop (EGLL) accepted by D039. This procedure converts material failures and near misses into auditable recurrence-prevention controls without granting automatic components authority to change Governance policy.

## Core invariant

```text
failure observed != learning completed
written lesson != preventive control
control integrated != control effective

verified learning = evidence
                  + causal analysis
                  + selected control
                  + integrated control
                  + regression/replay proof
```

Git is authoritative. Private chat/model memory is never learning authority.

## Learning states

A material learning record uses exactly one current state:

- `DETECTED`
- `TRIAGED`
- `ANALYZED`
- `CONTROL_PLANNED`
- `CONTROL_INTEGRATED`
- `VERIFIED`
- `CLOSED_NO_ACTION`
- `CONTROL_FAILURE`
- `SUPERSEDED`

`VERIFIED` requires proof that the accepted control catches/prevents the represented failure class, unless an explicit D037 limitation explains why deterministic representation would change the requirement meaning.

`CLOSED_NO_ACTION` requires a persisted rationale that no systemic preventive/detective control is warranted.

## Trigger sources

Learning candidates MAY originate from deterministic detectors or persisted Human/Orchestrator evidence.

Initial deterministic trigger classes include:

- verification regression;
- persisted procedural nonconformance;
- merged-branch post-merge advancement;
- stale eligible merged branch retirement;
- Task Contract / branch / handoff identity mismatch;
- formal rework after executor `DONE`;
- deterministically observable protected-flow/direct-write violation;
- security known-bad recurrence;
- repeated explicit exception fingerprint.

A trigger creates a candidate. It does not establish root cause, blame, architecture, or remediation authority.

## Stable fingerprints

Every material case has an agent-neutral fingerprint identifying a failure/control class, for example:

- `git.branch.post_merge_advance`
- `git.branch.delete_before_review_resolution`
- `task.handoff.identity_mismatch`
- `task.done_requires_rework`
- `workflow.direct_write.long_lived_branch`
- `verification.regression.security_known_bad`

Fingerprint semantics MUST be stable enough for deterministic recurrence comparison. They MUST NOT encode agent-product identity or individual blame.

If the same fingerprint recurs after a prior case reached `VERIFIED`, the new occurrence enters `CONTROL_FAILURE` unless evidence proves it is materially a different condition.

## Material learning records

Material records live under `docs/learning/LNNN-<slug>.md` and are authored by ChatGPT Orchestrator.

Each record MUST separate facts, analysis, and authority and contain at least:

- Learning ID;
- current state;
- stable fingerprint;
- detection source/revision/time where available;
- affected task/PR/decision/control;
- factual evidence references;
- immediate recovery/containment;
- contributing/systemic-cause analysis;
- systemic-gap determination;
- selected control and owner, or no-action rationale;
- implementation Task/PR references where applicable;
- regression/replay acceptance evidence;
- recurrence/control-failure links;
- closure/supersession rationale.

Do not create a heavyweight record for every ordinary transient test failure. A record is warranted when the evidence suggests a reusable failure class, material process/architecture gap, recurrence, control failure, or Human/Orchestrator-directed learning case.

## Causal analysis

Analysis is Human/Orchestrator-owned. It MUST distinguish:

1. observed fact;
2. immediate recovery;
3. contributing conditions;
4. systemic control gap;
5. proposed preventive/detective control.

Do not use blame or agent-product identity as a root cause.

A model may help generate hypotheses but its reflection is advisory only:

```text
model reflection = candidate analysis aid
model reflection != incident fact
model reflection != policy authority
model reflection != verification gate
```

## Control promotion

Promote a learning result to the strongest honest control layer that preserves requirement meaning:

- mechanically invalid repository state -> deterministic detector/status check/ruleset;
- protocol/state transition failure -> deterministic contract/state-machine regression test;
- ambiguous task/handoff identity -> schema/policy plus deterministic validator;
- recurring workflow misuse -> workflow invariant plus automated precondition/check where possible;
- security known-bad recurrence -> security fixture/scanner/config verifier;
- qualitative architecture mistake -> Decision/policy plus deterministic proxies only when they preserve actual meaning.

Do not create a fake deterministic proxy merely to claim automation.

## Implementation ownership

ChatGPT Orchestrator owns committed Markdown learning records, causal analysis, architecture/policy selection, Task Contracts, and acceptance.

Agente de IA Ejecutor owns authorized non-Markdown detector implementation, schemas/fixtures/tests, CI/check code, machine-readable telemetry, and verification evidence.

Human Owner retains final material architecture/risk authority and exceptions.

Any executable control change follows D022 and requires an integrated Task Contract before implementation.

## Verification and replay

For an automatically detectable class, learning SHOULD NOT reach `VERIFIED` until a deterministic fixture/replay demonstrates both:

1. the original bad state produces the expected fingerprint/failure; and
2. a corresponding compliant state does not produce that fingerprint.

Regression tests MUST be model-independent under D037.

Live remote-state checks may be introduced only through a separately authorized bounded integration phase; local/core verification must not silently gain network/provider dependencies.

## Recurrence monitoring

Machine-readable detector output SHOULD allow aggregation by stable fingerprint.

Semantics:

- first occurrence -> normal triage;
- recurrence before control verification -> priority/escalation signal, not automatic same-root-cause proof;
- recurrence after `VERIFIED` -> `CONTROL_FAILURE`;
- several fingerprints sharing one control surface -> architecture-level trend candidate.

## Checkpoint behavior

`docs/orchestrator/CHECKPOINT.md` contains only unresolved/current learning frontier needed for cold start. Historical learning detail remains in `docs/learning/`, decisions, tasks, reviews, handoffs, PRs and Git history.

## Source/consumer boundary

This procedure governs Agent Governance source maintenance only.

It MUST NOT create a live consumer `.agent-governance/` or `.agent-coordination/` footprint in this repository. Consumer-product EGLL requires a later explicit architecture decision after source-maintainer evidence demonstrates value.
