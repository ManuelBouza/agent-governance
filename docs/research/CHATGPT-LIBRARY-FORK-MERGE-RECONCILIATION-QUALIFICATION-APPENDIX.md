# R017 Appendix — ChatGPT Library fork merge reconciliation qualification

Status: COMPLETE  
Research-ID: R017  
Date: 2026-09-07

## Objective

Qualify whether a real Library-only fork can be reconciled without deleting either branch by creating a new merge revision with two explicit parents, preserving append-only history, and reconstructing a single canonical head from Library artifacts alone.

## Input fork

Library root:

`/r017-library-vc-race-20260907`

Previously qualified fork:

```text
              control@race-A
             /
control@race-base
             \
              control@race-B
```

Both branch objects and receipts were independently verified after the cross-chat race.

## Merge revision

A new immutable object was created:

`objects/control-race-merge.txt`

Exact content:

```text
revision: race-merge
content-A: child-from-chat-A
content-B: child-from-chat-B
```

Size: `79` bytes  
SHA-256: `537463e3f1d3ceb489c5b6e8aeac8eb2d837a06329119bc16b87cde64def2e26`

The object was rematerialized from Library and the 79-byte size and SHA-256 matched exactly.

## Merge receipt schema

Normal revisions in the earlier PoC used a single `parent_revision_id`. A merge revision requires multiple parents, so this qualification introduces schema `library-document-governance/v3` with:

```json
{
  "revision_id": "control@race-merge",
  "content_sha256": "537463e3f1d3ceb489c5b6e8aeac8eb2d837a06329119bc16b87cde64def2e26",
  "parent_revision_ids": [
    "control@race-A",
    "control@race-B"
  ],
  "merge_strategy": "deterministic-union"
}
```

Receipt path:

`receipts/control-race-merge.receipt.json`

## Merge promotion schema

A new append-only promotion was created:

`promotions/promote-race-A-race-B-to-merge.json`

It uses schema `library-document-governance-promotion/v2` and records both parents:

```json
{
  "parent_revision_ids": [
    "control@race-A",
    "control@race-B"
  ],
  "child_revision_id": "control@race-merge",
  "state": "PROMOTED"
}
```

No branch object, receipt, or earlier promotion was overwritten or deleted.

## DAG reconstruction

Using only persisted Library promotion records:

```text
control@race-base
       /       \
control@race-A  control@race-B
       \       /
      control@race-merge
```

Before merge:

```text
heads = [control@race-A, control@race-B]
classification = FORK_DETECTED
```

After merge:

```text
heads = [control@race-merge]
classification = ONE_HEAD
```

The merge therefore consumes both previous heads as parents and restores a single canonical head without erasing either divergent branch.

## Reconciliation receipt

An append-only reconciliation record was persisted at:

`reconciliations/reconcile-race-fork-001.json`

It records:

```text
heads_before = [control@race-A, control@race-B]
merge_revision_id = control@race-merge
merge_parent_revision_ids = [control@race-A, control@race-B]
heads_after = [control@race-merge]
classification_before = FORK_DETECTED
classification_after = ONE_HEAD
resolution = MERGED
state = RECONCILED
```

## Result

`PASS`

Empirically qualified on the tested ChatGPT Library surface:

- a forked history can be reconciled through a new immutable merge revision;
- merge revisions can carry multiple explicit parents at the application layer;
- no existing branch needs to be deleted or overwritten;
- DAG reconstruction returns from multiple heads to exactly one head;
- the full pre-merge history remains reconstructible;
- reconciliation itself can be represented by an append-only audit receipt.

## Bounded conclusion

Pure Library multi-writer behavior remains optimistic rather than serialized. The tested model is now:

```text
immutable revisions
+ unique revision_id
+ content_sha256
+ single-parent or multi-parent ancestry
+ immutable receipts
+ append-only promotions
+ deterministic fork detection
+ explicit merge reconciliation
+ append-only reconciliation receipt
```

This qualifies detection **and recovery** from a concurrent fork. It does not qualify atomic fork prevention or a Library-only mutex/CAS primitive.
