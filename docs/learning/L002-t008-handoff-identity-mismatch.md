# L002 — T008 handoff identity mismatch

Learning ID: L002  
State: DETECTED  
Fingerprint: `task.handoff.identity_mismatch`

## Detection

Detected during Orchestrator review of T008 executor HEAD `b67d9894e6f979d04f17ed5e512cf92a6601d228`.

The persisted handoff declared base SHA `2be1ad9329e0b7901b784cff542aca50a8516927`, which GitHub cannot resolve. The authoritative `develop` revision actually incorporated for the successful rerun is `2be1ad97fefb43e7116d534eecfd420a3c4f9923`.

## Immediate containment

T008 is not accepted despite green verification gates. T008-R2 requires correction of the handoff identity only; detector semantics remain frozen.

## Learning significance

This is direct dogfooding evidence for the newly implemented `task.handoff.identity_mismatch` fingerprint: a task may have correct implementation and green tests while still being non-acceptable because its durable evidence identity is invalid.

Automatic detection remains evidence only; remediation authority comes from persisted Orchestrator review.

## Next state

Advance only after the corrected handoff is remotely auditable and T008 is accepted. A later control decision may determine whether handoff identity validation should become an automatic pre-return gate.
