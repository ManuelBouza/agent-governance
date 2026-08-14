# OP047 — Retire OP046 contract branch

Operation ID: OP047
Status: READY_AFTER_INTEGRATION
Type: branch cleanup
Repository base: `develop`

## Objective

After OP046 and this contract are integrated into `develop`, retire exactly the merged remote branch `docs/op046-authorized-caveman-cleanup` and preserve `develop` and `main`.

## Preconditions

- local bootstrap baseline is current with `origin/develop`;
- OP046, OP047, and the current checkpoint are reachable from `develop`;
- `docs/op046-authorized-caveman-cleanup` is merged/reachable from `develop`;
- local/uncommitted work is preserved; BLOCK if safe cleanup cannot be established.

## Authorized mutation

Delete exactly the remote branch `docs/op046-authorized-caveman-cleanup`. Remove a matching local branch only when safe and already merged.

No repository file edits, tag/release changes, or other branch mutations are authorized.

## Verification

PASS requires remote branches exactly `develop`, `main`; local remaining branches reported; `develop` and `main` unchanged by cleanup; no repository files modified.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED
OPERATION: OP047
REMOTE_REMAINING: <comma-separated branches>
LOCAL_REMAINING: <comma-separated branches>
```
