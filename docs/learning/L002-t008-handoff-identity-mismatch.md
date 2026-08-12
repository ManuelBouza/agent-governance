# L002 — T008 handoff identity mismatch

Learning ID: L002  
State: ANALYZED  
Fingerprint: `task.handoff.identity_mismatch`

## Detection

Detected during Orchestrator review of T008 executor HEAD `b67d9894e6f979d04f17ed5e512cf92a6601d228`.

The persisted handoff declared base SHA `2be1ad9329e0b7901b784cff542aca50a8516927`, which GitHub cannot resolve. The authoritative `develop` revision actually incorporated for that successful rerun was `2be1ad97fefb43e7116d534eecfd420a3c4f9923`.

## Immediate containment

T008 was not accepted despite green verification gates. T008-R2 authorized correction of the handoff identity only and explicitly froze detector semantics.

The corrected executor handoff at HEAD `79df001b6a20a6f363e34e61093c63fc639479fe` records exact incorporated base `develop@472bc4fc2c283a3cd649c2efc4c80733dd02428b`; GitHub comparison confirms that base is the merge base and the T008 executable artifacts remain unchanged from the previously reviewed implementation anchor.

## Causal/systemic analysis

Observed fact: durable executor evidence contained a non-resolvable `base_sha` while implementation behavior and test gates were otherwise correct.

Immediate recovery: block acceptance, persist R2, correct only handoff identity, rerun verification, and re-review the exact remote HEAD.

Contributing condition: the current T008 `task.handoff.identity_mismatch` detector checks expected task ID, branch, and handoff path, but does not validate base/head commit resolvability or ancestry.

Systemic gap: green execution evidence can still contain invalid repository identity metadata unless the reviewer independently resolves and compares the referenced commits. The detector's current identity surface is narrower than the full D029/D021 audit surface exercised during review.

This is repository-level evidence integrity, not individual or agent-product blame.

## Control decision boundary

Do not expand T008 retroactively. Its accepted Task Contract did not require base-SHA resolvability/ancestry validation, and R2 explicitly prohibited detector-semantic changes.

A future separately contracted control SHOULD evaluate whether deterministic handoff identity validation should cover at least:

- referenced base/head commit resolvability;
- expected base branch identity;
- merge-base/ancestry consistency where applicable;
- returned HEAD versus persisted handoff HEAD consistency.

That control is not required to close T008 and MUST NOT be folded into T006/D035/D036. Control selection/scheduling remains pending after the current T008 integration frontier so it can be prioritized without scope smuggling.

## Verification evidence

T008-R3 accepts corrected HEAD `79df001b6a20a6f363e34e61093c63fc639479fe` with exact auditable base identity and unchanged detector/test blobs.

L002 remains `ANALYZED`, not `VERIFIED`: the immediate evidence defect is corrected, but the broader automatic-prevention control identified above is not yet selected/integrated.
