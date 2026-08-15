# L004 — T020 rework directive was initially chat-only

Learning ID: L004  
State: CONTROL_PLANNED  
Fingerprint: `workflow.procedural_nonconformance`

## Detection

Detected after T020-R1 findings were identified. The Orchestrator correctly blocked T020 acceptance but initially sent the concrete rework directive through chat before persisting its durable review authority.

`docs/TASK-CONTRACTS.md` requires rework to use durable review/revision instructions reconstructable from Git. The later `docs/reviews/T020-R1.md` became the canonical authority and the executor correction was reconciled against it before T020 acceptance.

## Factual evidence

- Controlling policy: `docs/TASK-CONTRACTS.md`.
- Affected task: `docs/tasks/T020-self-contained-build-artifact-and-identity.md`.
- Durable corrective review: `docs/reviews/T020-R1.md`.
- Durable acceptance review: `docs/reviews/T020-R2.md`.
- Related learning: `docs/learning/L003-t020-done-requires-rework.md`.

## Immediate containment

The chat-carried directive is non-authoritative convenience only. T020-R1 supplied the durable rework authority; T020-R2 confirms the corrected candidate was reviewed against that authority before integration.

## Causal/systemic analysis

The policy meaning was already correct, but the review flow lacked a fail-closed mechanical precondition preventing rework launch before durable review authority existed.

The systemic problem is therefore not missing prose. It is the absence of an enforceable/replayable transition control:

```text
executor DONE
    -> Orchestrator review
    -> if REWORK_REQUIRED: durable review/revision exists in Git
    -> only then rework launch
```

This is an Orchestrator/process control defect, not executor blame.

## Selected systemic control

D046/ICAE selects the prospective control direction:

- review/rework records should carry machine-readable enough identity/disposition to bind exact task + reviewed HEAD + `REWORK_REQUIRED` state;
- a rework transition must be mechanically detectable as invalid when its required durable authority is absent;
- the control should reference Git authority rather than duplicate rework instructions in prompts;
- EGLL integration should emit procedural-nonconformance evidence when the transition invariant is violated and `task.done_requires_rework` evidence when applicable;
- automation is enforcement/evidence support only and cannot acquire review, architecture or acceptance authority.

The existing D045 chain mechanism does not waive this requirement: any Stage-B rework authority must already be integrated in Git before continuation is eligible.

## Verification / recurrence status

L004 is `CONTROL_PLANNED`, not `VERIFIED`.

Verification requires an implemented fail-closed/replayable control demonstrating a bad transition without durable review is detected/rejected and a compliant transition is accepted without false positive.

A recurrence after that control reaches `VERIFIED` must be evaluated as potential `CONTROL_FAILURE` under D039.
