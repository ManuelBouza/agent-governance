# OP038 — Retire optional ecosystem guidance branch

Operation ID: OP038
Status: READY_AFTER_GUIDANCE_MERGE
Type: branch-cleanup
Base branch: `develop`

## Objective

Retire the merged ChatGPT-owned Markdown branch used to formalize optional/recommended Gentle AI and Caveman ecosystem guidance.

## Preconditions

- the guidance PR from `docs/optional-ecosystem-integrations` is merged into `develop`;
- current canonical remote state is synchronized;
- deleting the merged topic branch will not discard unmerged work.

## Authorized operation

Delete only the merged topic branch:

- remote `docs/optional-ecosystem-integrations`;
- corresponding local branch/worktree if present and safe to remove.

Do not delete or rewrite `develop`, `main`, unrelated branches, tags, commits or working state.

Preserve local/uncommitted work. If safe cleanup cannot be established, stop and report `BLOCKED`.

## Verification

After cleanup, remote branches must be exactly:

```text
develop
main
```

Local branches relevant to this repository should likewise retain only `develop`, `main` unless unrelated pre-existing local state makes that impossible; in that case report it without deleting unrelated work.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP038
REMOTE_REMAINING: <comma-separated branches>
LOCAL_REMAINING: <comma-separated branches>
```
