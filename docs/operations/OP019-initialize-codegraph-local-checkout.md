# OP019 — Initialize CodeGraph in canonical local checkout

Operation ID: OP019  
Status: READY_AFTER_T012_CLEANUP  
Type: local capability activation  
Base branch: `develop`

## Objective

Initialize CodeGraph for the canonical local `agent-governance` checkout used by future executor sessions, verify that it is usable, and prove that its generated `.codegraph/` state remains ignored/untracked under the canonical `.gitignore` policy integrated by T012.

## Preconditions

- T012 implementation PR #91 is merged into `develop`;
- T012 acceptance/implementation/planning branches are operationally cleaned;
- local checkout can be safely reconciled to current `origin/develop` without discarding work;
- CodeGraph is already available on the workstation as an external executor capability.

If any precondition cannot be established safely, return `BLOCKED`.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D041-executor-process-autonomy.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/OPENCODE-WORKTREE-PREFLIGHT.md`
- `.gitignore`

## Authorized operations

The executor may synchronize the canonical remote; establish the canonical local `develop` checkout; initialize/update CodeGraph local project state in that checkout using the installed CodeGraph version's supported project-initialization workflow; inspect CodeGraph status/health; and inspect Git status/ignore behavior.

The executor chooses the exact compatible CodeGraph commands for the installed version.

## Required boundaries

- `.codegraph/` is generated local state and MUST remain ignored/untracked;
- no repository content may be committed or pushed;
- no dependency, runtime, test, Governance Core, host configuration, or Markdown file may be changed;
- CodeGraph does not become Governance authority, Task Contract authority, acceptance authority, or a correctness dependency;
- initialization must occur in the canonical local checkout intended for subsequent executor work, not only in a disposable task worktree.

## Verification

Before returning, establish all of the following:

1. CodeGraph reports the repository as initialized/usable under the installed version's supported status/health mechanism;
2. `.codegraph/` exists only as local generated state as applicable to that version;
3. Git confirms `.codegraph/` is ignored;
4. no `.codegraph/` path is tracked;
5. repository tracked state remains clean after initialization;
6. no repository commit/push occurred.

## Stop / escalation

Return `BLOCKED` instead of guessing if CodeGraph is unavailable, initialization would require tracked repository state, the checkout is unsafe/dirty in a way that cannot be preserved, or the installed version's behavior conflicts with these boundaries.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP019
CODEGRAPH: READY | NOT_READY
GIT_CLEAN: YES | NO
TRACKED_CODEGRAPH: NONE | <paths>
REPO_MUTATION: NONE | <description>
```
