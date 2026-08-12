# OP002 — Retire T008-R1 planning branch

Operation ID: OP002  
Status: READY  
Type: post-integration branch cleanup  
Base branch: `develop`

## Objective

Retire the source branch of PR #62 after that PR is merged, without modifying repository content or affecting the active T008 implementation branch.

## Durable target

- PR #62 — `docs: persist T008 R1 and protocol baseline correction`.

The executor MUST derive the source branch name, reviewed `head_sha`, merged state, current remote head, and deletion safety from Git/GitHub records for PR #62.

## Controlling references

- `AGENTS.md`
- `docs/OPERATION-CONTRACTS.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`
- PR #62 merged Git/GitHub record

## Authorized operations

The Agente de IA Ejecutor may fetch/prune and inspect the canonical remote, verify PR #62 is merged and its surviving source branch still equals the reviewed PR head, delete that verified remote branch, remove the corresponding safe local branch and stale tracking ref in accessible controlled checkouts, and report inaccessible checkouts as unverified.

## Explicit exclusions

The executor MUST NOT:

- modify/create/commit/push repository content;
- delete `main`, `develop`, `test/egll-deterministic-learning-detectors`, or any branch not derived from PR #62;
- infer deletion safety from naming or ancestry alone;
- discard uncommitted/unique work;
- alter tags, releases, settings, rulesets, or history;
- start T009 or resume T008 as part of this operation;
- use chat-provided branch names, SHAs, or deletion decisions as authority.

## Safety invariant

```text
PR #62 merged
+ current source-branch HEAD == reviewed PR #62 head_sha
+ no later unique work
=> eligible for retirement
```

Any head drift, unrepresented work, local worktree ambiguity, dirty state, missing PR evidence, or permission/tool failure becomes `REVIEW` and the affected deletion stops.

## Verification requirements

Before returning, re-fetch and report the final remote and accessible-local branch inventories, confirm `main`/`develop` remain, confirm the active T008 branch remains untouched, and confirm no repository content commit/push was created.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP002
REMOTE_REMAINING: <branches>
LOCAL_REMAINING: <branches>
```
