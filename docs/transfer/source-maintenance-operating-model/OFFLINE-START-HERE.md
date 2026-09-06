# Offline Transfer Bundle — Start Here

Status: PORTABLE DELIVERY ENTRYPOINT

This package is designed for a target project that has **no access** to `ManuelBouza/agent-governance`.

The Human Owner may copy the complete exported package into the target project, attach it to the target-adoption chat, or otherwise make all package files locally available. The target must not need network access to, or credentials for, the source repository.

## Read order

1. `PORTABLE-OPERATING-MODEL.md`
2. `PORTABILITY-MANIFEST.md`
3. `UNRESOLVED-GAPS.md`
4. `TARGET-ADOPTION-CHECKLIST.md`
5. `EVIDENCE-APPENDIX.md`
6. `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md`
7. `OFFLINE-EXPORT-MANIFEST.md`
8. `source-reference/` only when provenance/audit detail is needed.

## Authority boundary

The portable operating model is a **candidate for target-native adoption**, not automatic target authority.

The `source-reference/` material is included only so the target-adoption chat can inspect original source wording without reaching the source repository. It must not be copied wholesale into target governance or treated as already accepted target decisions.

The target must inspect its existing governance first and classify each overlapping capability as:

`REUSE | ADAPT | COEXIST | MISSING | CONFLICT`

Preserve stronger compatible target-native controls.

## No source-repository dependency

The target bootstrap must use only:

- the files physically included in this exported package; and
- the target repository's own canonical state.

Source repository access is optional provenance revalidation only and is never a prerequisite for target adoption.

## Frozen implementation exclusion

T058 remains `BLOCKED / FROZEN_BY_HUMAN` and `DO_NOT_COPY`. Its unaccepted helper/code/tests are not part of the portable implementation package.

## Integrity

A generated offline archive should include an `EXPORT-RECEIPT.txt` and `SHA256SUMS.txt` binding the exported file set to the source commit used to produce the archive. Any missing or mismatched file is a fail-closed bootstrap condition.
