# L006 — RCAB committed manifest live-freshness coupling

Learning ID: L006  
State: CONTROL_PLANNED  
Fingerprint: `verification.generated_snapshot_live_coupling`

## Detection

Detected during T021 verification/review.

The T021 handoff reports that the full deterministic suite fails on:

`tests/test_repository_context.py::test_manifest_cli_check_on_real_repository`

with the same failure reproduced on clean canonical `develop@53b9c39c1111f4b871ef73b7447510195f672ea2` after removing T021 changes.

## Factual evidence

T031 generated and accepted `baselines/repository-context-manifest-v1.json` from the RCAB registry and then-current registered source files.

Subsequent accepted Markdown-only governance changes legitimately modified registered files:

- PR #136 changed `docs/EXECUTOR-HANDOFFS.md` and `docs/orchestrator/CHECKPOINT.md` while introducing D048/T031 acceptance metadata;
- PR #137 changed the checkpoint again while correcting publication-policy wording.

The committed manifest on clean `develop@53b9c39...` still contains the earlier T031 snapshot values/content identities for those registered paths. The ordinary full deterministic suite therefore treats accepted repository evolution as a stale-manifest failure.

No T021 executable change is required to reproduce the failure.

## Analysis

The generated manifest had two distinct roles conflated:

1. durable deterministic **snapshot evidence** of a particular RCAB registry/content epoch; and
2. a continuously **live currentness cache** expected to equal every later repository state.

Those roles are incompatible with normal role-separated source maintenance when registered Markdown such as the checkpoint changes frequently and the generated manifest is executor-owned non-Markdown state.

The result is a red canonical deterministic baseline between otherwise valid changes and unrelated tasks inheriting failures outside their scope.

```text
historical snapshot age != corrupted evidence
live state must come from live authority
```

## Selected systemic control

D049 selects explicit snapshot/live separation:

- committed RCAB manifest = historical epoch snapshot evidence;
- live ratchet/currentness = compute directly from current map + registered files;
- stale/current comparison remains an explicit deterministic operation when currentness is intentionally required;
- ordinary full deterministic regression no longer requires a historical snapshot to equal mutable current repository state.

T032 implements D049, updates deterministic tests/tooling, refreshes the snapshot epoch, and restores a green canonical full deterministic baseline.

## Verification requirements

L006 cannot reach `VERIFIED` until T032 is accepted/integrated and replay proves all of the following:

1. a valid committed snapshot remains acceptable after a registered source file legitimately advances;
2. explicit currentness comparison still detects that the snapshot differs from current content;
3. live RCAB warning/current metrics are computed from current source rather than trusted from the snapshot;
4. the ordinary full deterministic suite remains green on that legitimate drift case;
5. stale/tampered detection fixtures still fail when explicit currentness/integrity checks are invoked.

## Boundary

This learning does not authorize weakening RCAB registry integrity, bootstrap warning policy, source/distribution isolation, or tamper detection. It changes only the lifecycle assumption that a committed generated evidence snapshot must continuously equal mutable live source state.
