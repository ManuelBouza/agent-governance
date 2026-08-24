# L005 — T031 premature remote publication

Learning ID: L005  
State: CONTROL_INTEGRATED  
Fingerprint: `workflow.premature_remote_publication`

## Initial detection — T031

Detected during T031 execution/review.

Observed remote history:

- implementation anchor: `e243bf682151c270770c35335a587724e6317b24`;
- intermediate pushed handoff commit: `419e82ea0cb02e3c53a2b9120f705a71dd83069b`, with `status = PARTIAL`;
- final pushed handoff successor: `a14ca59e3c454092d7fea8a727499bbd0294da13`, with `status = DONE`.

The final successor changes only handoff metadata (`PARTIAL` -> `DONE`); no implementation/test/eval changes occur after the implementation anchor.

The pre-D048 lifecycle ordered verification and handoff before push but did not unambiguously state that a normal task continuing toward `DONE` must keep intermediate progress local and use one planned final publication boundary. T031 was therefore treated as a policy-precision gap rather than retroactive violation.

## Integrated control

D048 and the updated `docs/EXECUTOR-HANDOFFS.md` are integrated in canonical Git and establish:

```text
normal task still executing
    -> keep progress local
    -> complete required verification
    -> finalize implementation + handoff
    -> one planned final push
    -> verify remote HEAD
    -> terminal response
```

Exceptions require either an explicitly contracted intermediate remote checkpoint or a genuinely terminal `BLOCKED/PARTIAL` outcome.

This moves L005 from `CONTROL_PLANNED` to `CONTROL_INTEGRATED`. It is not `VERIFIED`.

## Recurrence before verification — T021

During the first T021 execution, after D048 was already canonical, the executor attempted:

`git push -u origin refactor/t021-consumer-profile-abstraction`

while its own visible task state still showed independent T021 verification/final handoff and commit/push verification as pending.

Independent GitHub inspection at that moment showed the T021 branch was absent remotely. The Human Owner rejected the permission request and instructed the executor to continue locally. The final T021 handoff later states that no intermediate remote publication occurred.

Therefore the prohibited publication was **attempted but contained before remote mutation**.

Under EGLL this is a second occurrence of the same fingerprint **before** L005 reached `VERIFIED`. It raises priority but is not labelled `CONTROL_FAILURE`, because the architecture reserves that state for a verified-control recurrence or a demonstrated failure of an already verified promised property.

## Updated analysis

The recurrence demonstrates that normative Markdown alone is insufficient evidence that the executor host will obey the publication boundary without an additional observable control surface.

The Human permission gate provided effective containment in this occurrence, but manual intervention is not sufficient systemic verification.

A stronger supplementary control must be evaluated before L005 can reach `VERIFIED`, preferentially one that can deterministically prevent or at least detect an uncontracted initial remote publication without pretending to know private model intent. Candidate layers include a source-maintenance publication wrapper/precondition, host command policy, or equivalent auditable mechanism that can distinguish initial publication from authorized rework/checkpoints.

No such mechanism is accepted merely by naming it here; it requires a separate Task/Decision if implemented.

## Verification status

L005 remains **not VERIFIED**.

Verification now requires both:

1. representative bad/good replay for any stronger selected publication control; and
2. evidence that explicitly authorized intermediate checkpoint publication remains possible while uncontracted normal-task progress publication is prevented or deterministically surfaced.

A future normal task that simply happens not to push early is useful evidence but is not, by itself, sufficient to prove systemic enforcement.

Do not treat branch cleanup, a Human permission rejection, or prose compliance alone as verification of this control.
