# Branching Policy

Status: ACTIVE

## Purpose

Keep `main` stable and public-facing while allowing continuous product development in `develop` through short-lived reviewable branches.

This is a simplified dual-branch release flow. It deliberately avoids mandatory classic-GitFlow release branches unless parallel stabilization is actually needed.

## Long-lived branches

### `main`

`main` is the primary/default stable branch.

It MUST represent the latest accepted product state and SHOULD be releasable at any commit. Normal feature, fix, refactor, test, documentation, or chore work does not begin directly on `main`.

Tags and public releases are created from `main` only.

### `develop`

`develop` is the integration branch for the next unreleased state.

It MAY be ahead of the latest release, but it SHOULD remain coherent and verification-green. Normal work does not begin by editing `develop` directly; create a topic branch first.

## Topic branches

Normal work starts from the current `develop` head using one of:

- `feat/<slug>`
- `fix/<slug>`
- `refactor/<slug>`
- `test/<slug>`
- `docs/<slug>`
- `chore/<slug>`

Use product/task meaning, never agent-product names, in branch names.

Topic branches are short-lived and merge back into `develop` through pull request. Prefer squash merge so one accepted PR becomes one coherent integration unit.

A topic branch lifecycle is not complete merely because its PR was merged. Successful integration includes post-merge branch cleanup according to `docs/BRANCH-CLEANUP.md`.

## Post-merge branch cleanup

After a topic PR is successfully merged into its authorized target, the corresponding topic branch MUST be retired rather than left indefinitely on the canonical remote.

For normal `feat/*`, `fix/*`, `refactor/*`, `test/*`, `docs/*`, and `chore/*` work:

1. verify that the PR is actually merged into the authorized target;
2. verify the exact reviewed PR head identity;
3. if the remote topic branch still exists, verify that its current HEAD has not advanced beyond the reviewed PR head;
4. delete the remote topic branch;
5. verify that the remote branch is absent;
6. prune/delete corresponding local topic branches in every maintainer/executor checkout that still carries them, after verifying that no unrepresented local work would be discarded.

Remote branch deletion is part of normal integration closure and SHOULD happen immediately after merge. Local cleanup MUST happen immediately when the merge operator controls that checkout; otherwise it MUST happen before that checkout begins its next repository task.

Because normal topic PRs are commonly squash-merged, Git ancestry alone is not sufficient evidence that a topic branch is safe to delete: the original topic commits may not appear as ancestors of `develop`. The safe deletion decision MUST use the merged PR record and its exact reviewed `head_sha`, plus confirmation that the branch has not received post-review/post-merge commits.

If the branch HEAD differs from the merged PR head, the branch has no merged PR, the PR was closed without merge, or the state is otherwise ambiguous, do not delete it automatically. Classify it for explicit review under `docs/BRANCH-CLEANUP.md`.

Repository hosting settings SHOULD automatically delete merged PR head branches when the platform supports that control. Automatic deletion is defense in depth, not a substitute for the post-merge verification above.

`main` and `develop` are long-lived and MUST NOT be deleted by this procedure. `release/*` and `hotfix/*` branches follow their specialized lifecycle and may be deleted only after their required propagation/integration is complete.

## Promotion to stable

When ChatGPT Orchestrator determines `develop` satisfies the applicable release/readiness contract:

1. run the required release verification;
2. open a PR from `develop` to `main`;
3. review public compatibility, security/supply-chain impact, migration needs, and verification evidence;
4. merge with a merge commit so ancestry between the long-lived branches remains explicit;
5. create any intended SemVer tag/release from the resulting `main` commit.

Normal topic branches MUST NOT target `main`.

## Optional release branches

Create `release/<semver>` only when a version requires stabilization while `develop` must continue toward later work.

A release branch is cut from the intended `develop` baseline and accepts stabilization-only changes. Do not use it as a general feature branch.

After release, ensure any stabilization fixes are also represented in `develop`.

Once a `release/*` branch has been fully integrated/propagated and no longer carries unique stabilization work, retire it using the same evidence-preserving cleanup principles in `docs/BRANCH-CLEANUP.md`.

## Hotfixes

Use `hotfix/<semver>` only for urgent corrections to the current stable line.

A hotfix:
1. starts from `main`;
2. contains the smallest required correction plus verification;
3. returns to `main` by PR;
4. may produce a patch release;
5. MUST be propagated to `develop` so the defect does not reappear in the next version.

Hotfix is not a shortcut around normal `develop` integration.

After required propagation to both stable and integration lines is complete and no unique hotfix work remains, retire the `hotfix/*` branch using `docs/BRANCH-CLEANUP.md`.

## Pull-request targets

Normal allowed targets:

- topic branch -> `develop`
- `develop` -> `main`
- `release/*` -> `main`
- `hotfix/*` -> `main`

A normal `feat/*`, `fix/*`, `refactor/*`, `test/*`, `docs/*`, or `chore/*` PR targeting `main` is a policy violation.

## Repository protection

Where repository controls support it, protect both `main` and `develop` with:

- pull requests required;
- applicable status checks required;
- force pushes disabled;
- deletion disabled;
- conversation resolution required where practical.

Protect published `v*` tags from mutation/deletion where GitHub rulesets are available.

Human approval requirements may evolve with the maintainer team; do not require self-approval from a sole maintainer.

## Agent invariant

The Human Owner, ChatGPT Orchestrator, and every Agente de IA Ejecutor use the same branch policy.

Neither ChatGPT nor an executor obtains permission to bypass protected long-lived branches because of agent identity. Agent/product names are adapter details and MUST NOT enter branch semantics.
