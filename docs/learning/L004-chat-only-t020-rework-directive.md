# L004 — T020 rework directive was initially chat-only

Learning ID: L004  
State: ANALYZED  
Fingerprint: `workflow.procedural_nonconformance`

## Detection

Detected during follow-up discussion after T020-R1 findings were identified.

The Orchestrator sent a concrete T020 rework directive through chat before persisting the corresponding review/revision instruction in Git.

`docs/TASK-CONTRACTS.md` requires rework to repeat on the same task branch using durable review/revision instructions and requires a reviewer to reconstruct from Git alone any explicit review directive. Therefore the chat-carried directive was not valid canonical authority even though its content matched the later persisted T020-R1 review.

## Factual evidence

- Controlling policy: `docs/TASK-CONTRACTS.md`.
- Affected task: `docs/tasks/T020-self-contained-build-artifact-and-identity.md`.
- Durable corrective review: `docs/reviews/T020-R1.md`.
- Related learning case: `docs/learning/L003-t020-done-requires-rework.md`.

## Immediate containment

The chat directive is treated as non-authoritative convenience only.

T020-R1 is the canonical rework authority. T020 must not be accepted on the basis of work performed solely from the chat-carried directive.

Before final T020 acceptance, the executor state must be reconciled with current canonical `develop` containing T020-R1, the durable review must be consumed as the rework instruction, and the required verification/handoff must be rerun or reaffirmed from that canonical instruction state. Any mismatch between the already-produced correction and T020-R1 remains rework, not implied authorization.

## Causal/systemic analysis

### Observed fact

The Orchestrator correctly blocked acceptance but moved directly from review findings to an executor-facing correction prompt instead of first persisting the review directive.

### Contributing conditions

- The current Orchestrator review flow has a strong policy rule but no mechanical precondition that prevents a chat rework launch before a review record exists in Git.
- The EGLL detector MVP includes `task.done_requires_rework` and generic procedural-nonconformance fingerprints, but it is not connected to live review orchestration.
- The prior T008-R2 workflow had demonstrated the correct durable-review pattern, but that pattern is not mechanically enforced.

### Systemic gap

A governance invariant that exists only as procedure can still be bypassed by the Orchestrator during a fast review/rework cycle. The repository lacks a fail-closed review-to-rework transition control.

This is an Orchestrator/process control defect, not executor blame.

## Control decision boundary

The policy meaning is already correct; do not add duplicate prose merely to restate it.

The future preventive control should instead enforce or mechanically expose the transition:

```text
executor DONE
    -> Orchestrator review
    -> if REWORK_REQUIRED: durable review/revision exists in Git
    -> only then rework launch
```

A separately contracted executable control should evaluate whether source-maintenance tooling can verify, before a rework launch or acceptance review, that:

- a durable review record exists for the exact task/review sequence;
- its disposition is machine-readable enough to distinguish `REWORK_REQUIRED` from acceptance;
- the reviewed executor HEAD is recorded;
- rework instructions are referenced from Git rather than carried only in chat;
- EGLL automatically emits `task.done_requires_rework` / procedural-nonconformance evidence when the transition is violated or when rework follows `DONE`.

The control must remain evidence/enforcement support only; it cannot acquire architecture or acceptance authority.

This should be designed with the post-T020 ICAE/assurance update so the same structured review/evidence model closes both L003 and L004 without creating a parallel methodology layer.

## Verification / recurrence status

L004 is `ANALYZED`, not `VERIFIED`.

The immediate containment is the persisted T020-R1 review. The systemic fail-closed review-to-rework control has not yet been implemented or replay-verified.

A recurrence after that future control reaches `VERIFIED` must be treated as potential `CONTROL_FAILURE` under D039.
