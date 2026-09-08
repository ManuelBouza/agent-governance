# R017 Appendix — ChatGPT Library cross-chat fork race qualification

Research-ID: R017 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-07  
Last-Reviewed: 2026-09-07  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-ONLY-DOCUMENT-GOVERNANCE-AND-CODEX-BRIDGE-RESEARCH.md`  
Decision-Ref: none

## Purpose

Qualify the remaining Library-only concurrency question after the explicit version-control PoC: when two independent ChatGPT chats start from the same promoted parent revision and both attempt to promote distinct children using the same requested promotion pathname with `overwrite=false`, does Library provide create-if-absent exclusion or preserve both writes?

## Fixture

Library root:

```text
/r017-library-vc-race-20260907
```

Canonical parent:

```text
revision_id: control@race-base
content_sha256: c44c9d6337fdced520ebf1238919e30f218aaf42a41f15b7538e130d848185cb
```

The parent object, receipt and initial promotion were created before either competitor entered its write phase.

## Competitors

Chat A:

```text
owner: race-chat-a
revision_id: control@race-A
content_sha256: 378d6d06f384c5690e63d2552a849feadb8c57cb3f4e2112538ba0dcc91ba65c
parent_revision_id: control@race-base
```

Chat B:

```text
owner: race-chat-b
revision_id: control@race-B
content_sha256: 2e6c56d0e1bedc985f9fab44ce2daeca76a1738e2ec9b60bd54c6f57d15b6bd7
parent_revision_id: control@race-base
```

Both chats passed a preflight that observed no competing child promotion before receiving `GO`.

## Contended promotion pathname

Both competitors were instructed to create, with `overwrite=false`, exactly:

```text
/r017-library-vc-race-20260907/promotions/promote-from-race-base.json
```

No retry and no manual rename were allowed.

## Observed results

Chat A:

```text
R017_LIBRARY_RACE_RESULT: SUCCESS
PROMOTION_FINAL_PATH: /r017-library-vc-race-20260907/promotions/promote-from-race-base.json
PROMOTION_WRITE_RESULT: SUCCESS
```

Chat B:

```text
R017_LIBRARY_RACE_RESULT: SUCCESS
PROMOTION_FINAL_PATH: /r017-library-vc-race-20260907/promotions/promote-from-race-base(1).json
PROMOTION_WRITE_RESULT: SUCCESS
```

Library therefore resolved the same-path collision by assigning a duplicate-safe filename to the second persisted write instead of rejecting it.

## Independent verification

The Orchestrator re-listed the Library namespace after both chats completed and observed:

```text
objects/control-race-A.txt
objects/control-race-B.txt
receipts/control-race-A.receipt.json
receipts/control-race-B.receipt.json
promotions/promote-from-race-base.json
promotions/promote-from-race-base(1).json
```

The two child objects were rematerialized from Library and their SHA-256 values independently recomputed:

```text
control-race-A.txt
378d6d06f384c5690e63d2552a849feadb8c57cb3f4e2112538ba0dcc91ba65c
MATCH receipt

control-race-B.txt
2e6c56d0e1bedc985f9fab44ce2daeca76a1738e2ec9b60bd54c6f57d15b6bd7
MATCH receipt
```

The promotion records independently read from Library were:

```text
promote-from-race-base.json
parent_revision_id: control@race-base
child_revision_id: control@race-A
owner: race-chat-a

promote-from-race-base(1).json
parent_revision_id: control@race-base
child_revision_id: control@race-B
owner: race-chat-b
```

## Graph reconstruction

The promotion graph is therefore:

```text
              control@race-A
             /
control@race-base
             \
              control@race-B
```

There are two children of the same parent and two reachable heads.

Classification:

```text
FORK_DETECTED
```

No automatic winner is justified by pathname order, creation time, duplicate suffix, file_id, owner, or content hash.

## Qualification result

`PASS`

The race empirically qualifies the following claims for the tested ChatGPT Library surface on 2026-09-07:

1. `overwrite=false` on an occupied Library pathname is **not** create-if-absent semantics.
2. Duplicate-safe rename permits both contending writes to survive.
3. A shared promotion pathname cannot serve as a Library-only mutex.
4. Two independent chats can successfully promote distinct children from the same parent revision.
5. Append-only parent/child promotion records allow deterministic post-write fork detection.
6. Pure Library fork prevention / atomic compare-and-set remains unqualified.

## Operational consequence

The qualified multi-writer Library-only model is:

```text
isolated immutable candidates
+ immutable receipts
+ append-only promotions
+ parent revision checks
+ reconstruct all heads
+ if exactly one head: continue
+ if multiple heads: FORK_DETECTED and fail closed
```

It is **not**:

```text
same pathname + overwrite=false = lock
```

or:

```text
first final filename wins
```

The duplicate-safe suffix is storage collision handling, not concurrency authority.

## Bounded conclusion

Application-level Library version control is now empirically qualified for history, exact-byte restore and fork detection, including a real cross-chat race. Strict multi-chat serializability is not provided by the tested Library primitives. Projects requiring prevention rather than detection need either single-writer discipline or a separately approved coordination authority with atomic compare-and-set semantics.
