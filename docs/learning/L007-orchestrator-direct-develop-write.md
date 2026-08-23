# L007 — Orchestrator direct write to `develop`

Learning ID: L007  
State: CONTROL_PLANNED  
Fingerprint: `workflow.direct_protected_branch_write`

## Detection

On 2026-08-17, while preparing `docs/CAPABILITY-SOURCE-CONTRACT.md`, ChatGPT Orchestrator intended to create the file on a fresh Markdown topic branch but issued a GitHub contents write with `branch: develop` after repeated failed attempts against a not-yet-created branch.

GitHub accepted that request and created commit:

`dffe9cc18696ae04e57b9fef9a4b5b833f0c3435`

containing a placeholder version of `docs/CAPABILITY-SOURCE-CONTRACT.md` directly on `develop`.

This violates the repository branch invariant even though the content was Markdown and Orchestrator-owned.

### 2026-08-23 recurrence

While preparing D054/T035, the Orchestrator again intended to create a topic branch first but accidentally invoked the GitHub contents `create_file` action against `develop` instead of the branch-creation action. A second mistaken contents invocation followed during attempted recovery.

The two direct commits were:

- `a09e1d8cc84e0591ca2cd0401b30cd69844914ba` — added root file `noop`;
- `87319e9167c60d64a2f16f0a79367000c048bfb9` — added root file `noop2`.

The repository tree was restored without rewriting history through PR #188, which removed only those two unintended files and squash-integrated the containment as `3694cd7ec562f2baa127965f4269a609957f4783`.

Because L007 had never reached `VERIFIED`, this is not classified as a post-verification `CONTROL_FAILURE`; it is stronger evidence that the planned attention-based control was not yet an effective mechanical prevention control.

## Controlling policy

- `AGENTS.md` — normal Markdown work occurs on a short-lived topic branch from `develop` and returns through PR.
- `docs/BRANCHING.md` — normal direct development writes to `develop`/`main` are prohibited.

Role ownership does not waive branch discipline.

## Immediate containment

For both occurrences the Orchestrator did **not** reset, force-update, rewrite or hide canonical history.

Containment preserves the accidental commits as auditable evidence and restores the intended tree through a policy-compliant topic branch/PR.

For the 2026-08-23 recurrence specifically:

1. stop further D054 repository mutation;
2. read current `develop` and preserve both accidental commits;
3. create `fix/remove-accidental-noop-files` from the resulting canonical head;
4. delete only `noop` and `noop2` on that fix branch;
5. verify the branch diff contained only those removals;
6. merge PR #188 to `develop`;
7. re-read canonical `develop` before resuming D054 on a separately created topic branch.

The correction restores valid repository content but does not claim that the direct-write procedure was conforming.

## Causal analysis

The repository policy was explicit. The original failure occurred because branch existence and target-branch identity were not treated as a mandatory fail-closed precondition immediately before the write.

The first failed sequence was effectively:

```text
intend topic-branch write
    -> target branch does not yet exist
    -> repeated write attempts fail
    -> fallback write targets develop
    -> GitHub accepts direct mutation
```

The 2026-08-23 recurrence removes ambiguity about the weakness of the prior control. The topic branch had not yet been created, and the Orchestrator selected the wrong GitHub mutation action. The first accidental direct write was then compounded by another wrong contents action during recovery.

The systemic defect is therefore broader than remembering a branch name:

```text
correct ownership + intended branch name
    != mechanically verified safe mutation target
```

The unsafe tool surface permits a contents mutation to a long-lived branch whenever the caller supplies that branch. A reasoning-only reminder did not prevent a tool-selection/argument error.

A safe write requires all of:

```text
correct file ownership
+ topic branch created
+ topic branch ref verified
+ mutation action explicitly bound to that verified ref
+ long-lived branch target rejected before invocation
```

## Selected systemic control direction

The earlier control remains necessary but is strengthened.

For future Orchestrator repository writes:

1. resolve current canonical `develop` SHA;
2. create the intended topic branch using the dedicated branch-creation action before any content mutation;
3. read/search the branch ref back and prove the branch exists at the captured authorized base;
4. only after that proof may create/update/delete actions be invoked;
5. every create/update/delete request must name that exact verified topic branch;
6. a create/update/delete request whose target is `develop` or `main` is invalid unless a separately accepted emergency procedure explicitly authorizes that exact mutation;
7. after writes, compare the topic branch to the captured canonical base before PR creation;
8. unexpected canonical-branch movement caused by Orchestrator tooling is a procedural incident and must be persisted rather than repaired by history rewrite.

The desired end state is a mechanically fail-closed mutation preflight or wrapper that makes long-lived-branch contents mutation unavailable to normal Orchestrator flows. Until that control exists, branch creation + ref verification is a mandatory explicit gate, not a conversational reminder.

D054's runbook/verified-operation-recipe design is relevant to this class of problem, but it does not by itself close L007: Orchestrator-owned GitHub repository mutation needs its own enforceable source-maintainer control because D054 assigns executor command/API mechanics only for delegated implementation work.

## Verification status

L007 remains `CONTROL_PLANNED`, not `VERIFIED`.

The 2026-08-23 recurrence demonstrates that the prior non-mechanical control had not closed the failure class.

Verification now requires representative future Orchestrator write flows showing that:

- a nonexistent topic branch cannot lead to fallback mutation of `develop`/`main`;
- normal content mutation cannot be invoked until the topic branch ref is mechanically verified;
- a create/update/delete request targeting a long-lived branch is rejected before GitHub mutation in the normal flow;
- a normal Markdown write succeeds only through the verified topic branch and reviewed PR;
- canonical `develop` moves only through the reviewed PR integration path in that flow.

A later recurrence after this strengthened control is actually `VERIFIED` must be evaluated as `CONTROL_FAILURE` under D039.