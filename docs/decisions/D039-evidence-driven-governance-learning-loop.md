# D039 — Evidence-driven governance learning loop

Status: ACCEPTED  
Decision owner: Human Owner  
Applies to: Agent Governance source-product maintenance learning, incident recurrence prevention, deterministic workflow verification

## Context

Agent Governance already records durable tasks, reviews, handoffs, decisions and checkpoints, but the conversion of failures/near misses into preventive controls was not a first-class lifecycle.

Recent T007 work exposed both executor and Orchestrator workflow failures that were recovered and then converted into policy manually. The recovery was successful, but the learning path depended on someone noticing the systemic gap, reasoning about it, editing policy, and later remembering to verify the new invariant.

External engineering practice supports a stronger closed loop:

- Google SRE postmortems/CAPA: define incident triggers, analyze contributing causes, create preventive actions, and aggregate structured incident metadata to detect recurring themes;
- NIST SSDF: address root causes to prevent recurrence rather than treating symptom repair as sufficient;
- policy-as-code systems such as OPA: keep policy explicit/versioned and separate policy decisions, enforcement and decision telemetry;
- GitHub rulesets/status checks: mechanically enforce repository invariants where the platform exposes the required state;
- LLM reflection research such as Reflexion/Self-Refine: linguistic feedback can improve subsequent reasoning, but it is not an acceptable source-product verification authority under D037.

The detailed research and architecture are in `docs/ARCHITECTURE-GOVERNANCE-LEARNING-LOOP.md`.

## Decision

Agent Governance SHALL adopt an **Evidence-Driven Governance Learning Loop (EGLL)** for source maintenance before considering any consumer-product version.

The loop is:

```text
detect -> capture evidence -> triage/fingerprint -> causal analysis
       -> select control -> controlled implementation
       -> regression/replay proof -> recurrence monitoring
```

A material failure is not considered learned merely because it was fixed or documented.

```text
failure observed != learning completed
written lesson != preventive control
control integrated != control effective
```

A learning case reaches `VERIFIED` only when the selected preventive/detective control is integrated and evidence shows that the original failure class is caught/prevented, unless D037 requires an explicit limitation because deterministic reduction would change the requirement's meaning.

## Learning states

- `DETECTED`
- `TRIAGED`
- `ANALYZED`
- `CONTROL_PLANNED`
- `CONTROL_INTEGRATED`
- `VERIFIED`
- `CLOSED_NO_ACTION`
- `CONTROL_FAILURE`
- `SUPERSEDED`

Recurrence of the same stable fingerprint after `VERIFIED` becomes `CONTROL_FAILURE` and requires re-analysis.

## Automatic detection boundary

Automatically detectable source-maintenance signals SHOULD initially include:

- deterministic verification regressions;
- explicit persisted procedural nonconformance;
- merged-branch advancement after PR merge;
- stale eligible merged branches not retired;
- Task Contract / branch / handoff identity mismatch;
- formal rework after executor `DONE` as a learning candidate;
- deterministically observable long-lived-branch direct-write/protection bypass;
- D035/D037 security known-bad recurrence;
- repeated explicit exception fingerprints.

Human corrections and qualitative architecture failures remain valid learning triggers, but they MUST be persisted as Human/Orchestrator evidence instead of pretending they were automatically detected.

## Stable fingerprint invariant

Learning cases use agent-neutral stable fingerprints for recurrence/trend detection, for example:

- `git.branch.post_merge_advance`
- `git.branch.delete_before_review_resolution`
- `task.handoff.identity_mismatch`
- `task.done_requires_rework`
- `workflow.direct_write.long_lived_branch`
- `verification.regression.security_known_bad`

A fingerprint describes the failure/control class, never a person or agent product.

## Authority boundary

Automatic components MAY detect, fingerprint, annotate/fail already-authorized checks, aggregate recurrence, and replay deterministic regressions.

Automatic components MUST NOT create new Governance authority, alter architecture/policy/Task Contracts, weaken acceptance, approve their own remediation, infer Human intent, or use an LLM judgment as a PASS/FAIL gate.

Role ownership remains D016-compatible:

- ChatGPT Orchestrator owns causal/systemic analysis, control selection, committed Markdown learning records/Decisions, and acceptance;
- Agente de IA Ejecutor owns authorized non-Markdown detectors, fixtures, tests, CI/check implementation and verification evidence;
- Human Owner owns final material architecture/risk decisions and exceptions.

## Persistence boundary

Git remains authoritative.

Material source-maintainer learning cases SHALL follow `docs/GOVERNANCE-LEARNING.md`. Orchestrator-owned Markdown learning records live under `docs/learning/`. Detector logs/check artifacts are evidence transport, not authority. The checkpoint contains only unresolved current learning/control state.

The source repository MUST NOT create a live consumer `.agent-governance/` or `.agent-coordination/` footprint to implement EGLL.

## Verification boundary

D037 remains controlling:

```text
model reflection = candidate analysis aid
model reflection != learning authority
model reflection != verification gate
```

The source-product EGLL core path MUST remain deterministic/code-first and must not require model/provider availability.

## Staged adoption

1. **Phase A — learning contract:** accepted by this decision and `docs/GOVERNANCE-LEARNING.md`.
2. **Phase B — deterministic MVP:** T008 implements fingerprint schema, replay fixtures and local detectors for the highest-value source workflow failures, including T007 regression cases.
3. **Phase C — GitHub-aware detector:** later bounded remote-state checks for facts unavailable in a local fixture, such as merged-branch advancement/retirement.
4. **Phase D — trend aggregation:** later mechanically aggregate fingerprints and escalate recurrence/control failure.
5. **Phase E — consumer decision:** only after source-maintainer evidence demonstrates value, decide separately whether EGLL belongs in Governance Core for consumer projects.

## Sequencing decision

T008 SHALL execute after the outstanding post-integration branch cleanup and before T006.

Rationale: T008 strengthens the source-maintenance process under which later tasks execute. It is deliberately a narrow deterministic infrastructure MVP and MUST NOT absorb T006, D035, D036, Governance Core changes, live GitHub enforcement, or consumer-product behavior.

After T008 is accepted, integrated, and post-integration-cleaned, resume T006 exactly as already contracted. D036 remains after T006.

## Consequences

1. source maintenance treats recurrence prevention as a first-class lifecycle;
2. automatic detection may create evidence/learning candidates but never new authority;
3. material learning closes only with verified control or explicit justified no-action;
4. recurrence after verified control is a control failure;
5. D037 deterministic verification remains authoritative;
6. source/consumer boundaries remain intact;
7. consumer EGLL remains a later explicit decision, not an implicit consequence of source-maintainer adoption;
8. executable EGLL work requires a dedicated Task Contract and normal source-change procedure.
