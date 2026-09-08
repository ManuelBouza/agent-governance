# R017 Appendix — Explicit version control over ChatGPT Library

Research-ID: R017 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-07  
Last-Reviewed: 2026-09-07  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-ONLY-DOCUMENT-GOVERNANCE-AND-CODEX-BRIDGE-RESEARCH.md`  
Decision-Ref: none

## Purpose

Qualify an application-level version-control scheme that uses ChatGPT Library only as persistent object storage and does not depend on Library's internal `version_id`, GitHub, or a native Library restore/CAS API.

## Tested Library namespaces

Initial exploratory schema:

`/r017-library-vc-poc-20260907`

Corrected schema:

`/r017-library-vc-poc2-20260907`

The corrected namespace contains independent immutable objects, receipts and append-only promotion records.

## Initial schema finding

The first pass used `content_sha256` itself as the graph node identity. That is insufficient for a real restore: if a later revision restores the exact bytes of an earlier revision, both revisions necessarily have the same SHA-256 and cannot be distinguished historically by content hash alone.

This was treated as a design defect, not accepted as qualification evidence.

## Corrected identity model

The corrected schema separates:

- `revision_id`: unique historical revision identity;
- `content_sha256`: integrity/content identity;
- `parent_revision_id`: graph ancestry;
- `restored_from_revision_id`: explicit restore provenance.

Example:

```json
{
  "schema": "library-document-governance/v2",
  "project_id": "r017-library-vc-poc2-20260907",
  "document_id": "control",
  "revision_id": "control@v0004",
  "file": "objects/control-v0004-restore-v0001.txt",
  "content_sha256": "a5ccec54d5758688e6591efbcb6b1846732950acb2ec63bcea154cc569449cb0",
  "parent_revision_id": "control@v0003",
  "restored_from_revision_id": "control@v0001",
  "state": "PROMOTED"
}
```

## Linear revisions

The Library-only sequence was:

```text
control@v0001  alpha
    -> control@v0002  beta
    -> control@v0003  gamma
    -> control@v0004  exact-byte restore of v0001
```

Round-trip identities:

| Revision | Size | SHA-256 |
| --- | ---: | --- |
| `control@v0001` | 26 | `a5ccec54d5758688e6591efbcb6b1846732950acb2ec63bcea154cc569449cb0` |
| `control@v0002` | 25 | `31a3c59ccc97619d2d06a5e244b2c47882983b96446c125d99f60410f9ddbd93` |
| `control@v0003` | 26 | `12328b89d6380303522346bf78bf1370bdf3d00e0fa691152be7517e72d28380` |
| `control@v0004` | 26 | `a5ccec54d5758688e6591efbcb6b1846732950acb2ec63bcea154cc569449cb0` |

All five tested objects, including the fork object below, were rematerialized from Library and recomputed SHA-256/size matched their receipts exactly.

### Restore property

`control@v0004` contains exactly the same bytes as `control@v0001`.

Therefore:

```text
content_sha256(v0004) == content_sha256(v0001)
```

while:

```text
revision_id(v0004) != revision_id(v0001)
```

and its receipt records:

```text
parent_revision_id = control@v0003
restored_from_revision_id = control@v0001
```

Result: restore can preserve exact historical content without losing historical revision identity.

## Fork qualification

A competing immutable revision was created from the already-used parent `control@v0002`:

```text
control@f001
content SHA-256:
ec665f3fb44704cdfb66323cdef8f5544ee91a227458739820dcc7a642ef77a3
parent_revision_id:
control@v0002
```

The promotion graph reconstructed only from persisted promotion records was:

```text
control@v0001
      |
control@v0002
     / \
control@v0003   control@f001
      |
control@v0004
```

Computed heads:

```text
control@v0004
control@f001
```

Computed fork parent:

```text
control@v0002
```

Classification:

`FORK_DETECTED`

No automatic winner was selected.

## Qualified read/reconstruction protocol

```text
1. enumerate immutable receipts/promotions
2. verify every referenced content object exists
3. rematerialize object
4. recompute SHA-256
5. require exact receipt match
6. build graph by revision_id / parent_revision_id
7. calculate heads
8. exactly one head -> healthy canonical lineage
9. more than one head -> FORK_DETECTED / fail closed
```

## Qualified restore protocol

A restore is not an overwrite and not movement of a mutable pointer.

```text
1. select historical source revision R_old
2. retrieve and hash-verify R_old bytes
3. create a new unique revision R_new with those exact bytes
4. parent_revision_id = current healthy head
5. restored_from_revision_id = R_old
6. create immutable receipt
7. create append-only promotion
8. reconstruct graph and require one head
```

This preserves both content fidelity and audit history.

## Capability result

| Capability | Result |
| --- | --- |
| independent Library object per revision | VERIFIED |
| exact round-trip integrity via SHA-256 | VERIFIED |
| application-level linear history | VERIFIED |
| restore exact old bytes as new revision | VERIFIED |
| distinguish identical-content historical revisions | VERIFIED via `revision_id` |
| append-only ancestry reconstruction | VERIFIED |
| competing promotion from same parent | VERIFIED |
| deterministic fork detection | VERIFIED |
| silent winner selection | PROHIBITED / NOT USED |
| dependence on Library internal `version_id` | NOT REQUIRED |
| dependence on GitHub for payload/history | NOT REQUIRED |
| atomic prevention of concurrent promotions | NOT QUALIFIED |

## Bounded conclusion

An auditable Library-only documentary history is empirically feasible without relying on Library's internal version semantics when the control plane uses:

```text
immutable content objects
+ unique revision_id
+ SHA-256 content integrity
+ immutable receipts
+ append-only promotions
+ parent_revision_id graph
+ explicit restored_from_revision_id
+ fork detection
```

`content_sha256` must not be used as the sole revision identity because restored or deduplicated content may legitimately repeat the same bytes at different historical points.

The scheme detects concurrent/divergent promotion but does not establish an atomic multi-chat mutex. Strict single-writer enforcement or a separately qualified coordination authority remains necessary if fork prevention rather than fork detection is required.

## Disposition

R017 remains `COMPLETE / NOT_REQUIRED` as research. This appendix qualifies the application-level version-history, restore and fork-detection mechanics only; it does not adopt a normative Library-only adapter.