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

## Recurrence before control verification — T030 stale rework bootstrap

After T030-R1 was integrated through PR #130, a T030 rework invocation returned `STATUS: DONE` with the exact previously rejected HEAD `1322e8fbf936604c17a4120beb0092df884ad0dc`.

Remote verification established that:

- `develop` had advanced to the T030-R1 integration commit while the T030 topic branch had not moved;
- the topic branch remained diverged from current `develop`, two commits ahead and one commit behind, with merge-base at the pre-review T030 launch baseline;
- the persisted handoff was unchanged and still contained the same AC-CTX-1 evidence already rejected by T030-R1; and
- no corrected implementation commit, finalization-aware regression, refreshed baseline, or refreshed handoff existed remotely.

The controlling policy was already explicit: an executor must establish a safe local baseline equal to current remote `develop` containing the controlling Task Contract before using the implementation branch, and rework repeats on the same branch using durable review/revision instructions. The recurrence is therefore not treated as missing Task Contract semantics and does not justify chat-carried rework instructions.

Under D039 this is a recurrence of `workflow.procedural_nonconformance` before L004 reaches `VERIFIED`, so it is a priority/escalation signal rather than `CONTROL_FAILURE`.

The recurrence refines the selected control boundary:

```text
durable review present in Git
    != durable review consumed by rework executor

valid rework transition
    = current canonical base established
    + controlling Task Contract/review loaded from that base
    + implementation branch reconciled without losing work
    + only then correction execution
```

Immediate containment for T030 uses the existing D045 chained-transition mechanism so the continuation re-bootstraps from current canonical `develop`, verifies the required review is reachable there, and only then resumes the implementation branch. This is stronger transport/orchestration containment, not proof that the systemic fail-closed control is complete.

## Selected systemic control

D046/ICAE selects the prospective control direction:

- review/rework records should carry machine-readable enough identity/disposition to bind exact task + reviewed HEAD + `REWORK_REQUIRED` state;
- a rework transition must be mechanically detectable as invalid when its required durable authority is absent;
- the transition control must also prove the rework executor consumed authority from the current canonical base rather than a stale topic-branch copy;
- the control should reference Git authority rather than duplicate rework instructions in prompts;
- EGLL integration should emit procedural-nonconformance evidence when the transition invariant is violated and `task.done_requires_rework` evidence when applicable;
- automation is enforcement/evidence support only and cannot acquire review, architecture or acceptance authority.

The existing D045 chain mechanism does not waive this requirement: any Stage-B rework authority must already be integrated in Git before continuation is eligible. D045 may provide bounded immediate containment where its deterministic re-bootstrap preconditions are explicit, but it is not by itself the final L004 systemic control.

## Verification / recurrence status

L004 is `CONTROL_PLANNED`, not `VERIFIED`.

Verification requires an implemented fail-closed/replayable control demonstrating both:

1. a bad transition without durable/currently-consumed review authority is detected/rejected; and
2. a compliant transition from current canonical authority is accepted without false positive.

A recurrence after that control reaches `VERIFIED` must be evaluated as potential `CONTROL_FAILURE` under D039.
