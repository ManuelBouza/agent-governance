# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O045  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T009 is `ACCEPTED`, integrated, and post-integration-cleaned. D039 is `ACCEPTED`.

T008 rerun reached green focused/full/Ruff gates, but T008-R2 is `REWORK_REQUIRED` because `handoffs/T008-executor-handoff.json` at executor HEAD `b67d9894e6f979d04f17ed5e512cf92a6601d228` records non-existent base SHA `2be1ad9329e0b7901b784cff542aca50a8516927` instead of authoritative incorporated `develop` `2be1ad97fefb43e7116d534eecfd420a3c4f9923`.

This is deterministic dogfooding evidence for fingerprint `task.handoff.identity_mismatch`. L002 is `DETECTED` at `docs/learning/L002-t008-handoff-identity-mismatch.md`.

L001 remains `CONTROL_INTEGRATED`, not `VERIFIED`, until T008 closes with valid auditable identity.

T006 remains `READY` after T008. D036 remains after T006.

## Persisted executor-instruction invariant

`prompt = bootstrap transport only`; persisted Task/Operational Contract plus referenced Git policy is the complete instruction. Concrete rework authority is persisted in review records, never supplied only by chat.

## T008 — REWORK_REQUIRED

Task Contract: `docs/tasks/T008-egll-deterministic-learning-detectors.md`  
R1: `docs/reviews/T008-R1.md`  
R2: `docs/reviews/T008-R2.md`  
Active branch: `test/egll-deterministic-learning-detectors`

R2 authorizes only correction of the non-Markdown handoff identity and rerun of original gates. Detector implementation/fixtures/tests must remain unchanged.

## Learning state

L001 — `verification.regression.protocol_version_drift` — `CONTROL_INTEGRATED`; T009 corrected the baseline and T008 rerun is green, but L001 waits for T008 accepted closure.

L002 — `task.handoff.identity_mismatch` — `DETECTED`; invalid handoff base identity blocked acceptance despite green tests. Future control planning may add automatic handoff identity validation before executor return.

## Procedural audit

Preserve all prior audit history. Additionally, during T008-R2 preparation the Orchestrator accidentally wrote placeholder `docs/reviews/T008-R2.md` directly to `develop` in commit `643abb6eb91ea928d9f3f933f6ee8dfa6bf7e839`. History must remain visible; this branch replaces the placeholder through normal reviewed Markdown flow.

## Next Action

1. Integrate the Markdown change containing T008-R2, L002, OP004 and this checkpoint; freeze its source branch.
2. Execute OP004 to retire that planning branch only, preserving active T008.
3. Resume T008 using its existing Task Contract; executor must consume persisted R2 and correct only handoff identity plus rerun gates.
4. Re-review T008. If accepted, integrate and clean it; then mark L001 `VERIFIED` and advance L002 according to evidence/control decision.
5. Resume T006 unchanged. D036 remains after T006.

## Do Not

- Do not accept T008 with unresolved handoff identity.
- Do not modify T008 detector semantics under R2.
- Do not hide the `643abb6e…` direct-write incident.
- Do not delete `main`, `develop`, or active T008 during planning cleanup.
- Do not place concrete executor semantics only in chat.
