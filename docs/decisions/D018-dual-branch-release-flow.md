# D018 — Dual-branch release flow

Status: ACCEPTED
Authority: Human Owner

## Decision

The canonical repository uses a simplified dual-branch release flow:

- `main` is the primary/default stable branch and represents the latest accepted, potentially releasable product state.
- `develop` is the long-lived integration branch for the next unreleased product state.
- normal work MUST occur on short-lived topic branches created from `develop` and merged back by pull request.
- direct development writes to `main` or `develop` are prohibited in normal operation.

Topic prefixes:
- `feat/`
- `fix/`
- `refactor/`
- `test/`
- `docs/`
- `chore/`

`release/<semver>` is optional and used only when release stabilization must proceed while `develop` continues advancing.

`hotfix/<semver>` is exceptional, starts from `main`, returns to `main` through PR, and its effective fix MUST also be propagated to `develop`.

## Merge policy

- topic branch -> `develop`: prefer squash merge for one coherent change per PR.
- `develop` -> `main`: prefer merge commit so the two long-lived branches preserve ancestry.
- `release/*` -> `main`: merge commit.
- `hotfix/*` -> `main`: merge according to release-maintenance needs; propagate the fix to `develop` immediately.

## Stable releases

Tags/releases are cut from `main` only. Published `v*` tags are immutable release identities.

Consumers SHOULD pin an immutable release/tag/commit rather than `main` or `develop`.

## Protection intent

Repository rules SHOULD enforce, where available:
- pull requests required for `main` and `develop`;
- required verification checks;
- no force pushes;
- no branch deletion;
- resolved review conversations where practical;
- only `develop`, `release/*`, or `hotfix/*` may target `main` under normal policy.

`main` remains the default branch so public visitors and clones see the latest stable state. Contribution instructions MUST tell contributors to target `develop` for normal changes.

## Rationale

The project publishes versioned governance artifacts and needs a stable public branch without imposing the full overhead of classic GitFlow. A stable `main`, integration `develop`, and short-lived topic branches preserve release clarity, reviewability, rollback safety, and public trust while keeping the workflow lightweight.

## Consequences

- `docs/BRANCHING.md` is the normative operational branch policy.
- `docs/RELEASES.md`, `README.md`, `AGENTS.md`, and `CONTRIBUTING.md` must align with this model.
- ChatGPT Orchestrator and the Agente de IA Ejecutor follow the same branch policy; agent identity never appears in branch naming semantics.
