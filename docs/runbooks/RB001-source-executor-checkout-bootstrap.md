# RB001 — Source Executor Checkout Bootstrap

Runbook-ID: `source.executor.checkout-bootstrap`  
Status: `ACTIVE`  
Revision: `D054-v1`  
Owner: `strategy`

## Purpose

Establish a safe, current source-repository checkout and locked local development environment for an authorized Executor task without making the Human Owner the routine terminal operator and without relying on remembered command syntax.

This runbook defines procedure semantics. Exact Git, GitHub, uv, PowerShell, Bash or equivalent syntax is resolved by the Executor under D054.

## Applicability and exclusions

Applies when:

- a source Task Contract requires a fresh/rematerialized or reconciled local checkout;
- the Executor must prove a local base equals the canonical remote branch before implementation;
- a locked repository toolchain/environment must be prepared before verification.

Excludes:

- destructive cleanup of an existing path with unrepresented work;
- production/system administration unrelated to the source checkout;
- global workstation Git/toolchain policy changes as an acceptance mechanism;
- privilege elevation unless separately authorized;
- release/deployment/credential-rotation operations.

## Authorization binding

- Required effect classes: `OBSERVE`, `NETWORK_CONNECT`, `MUTATE_SCOPED`, `EXECUTE_LOCAL`; `INSTALL_CONFIGURE` only for the project-local locked environment when the Task Contract/toolchain permits it.
- Target constraints: the canonical Agent Governance remote and a specifically resolved local source checkout path.
- Privilege ceiling: current non-elevated user unless a separate D033 gate authorizes otherwise.
- Credential class: existing approved Git/GitHub authentication and package-registry access; never persist secret values.
- Network scope: canonical Git remote plus repository-declared package sources required by the locked toolchain.
- Approval mode: normally `ALLOW_TASK`/`ALLOW_EXPLICIT` when already covered by the active Task Contract; any boundary crossing follows D033.

This runbook does not grant those permissions.

## Inputs

- canonical repository identity;
- canonical base branch, normally `develop`;
- intended local checkout path;
- current Task Contract requiring the bootstrap;
- repository-native toolchain contract (`docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`);
- any task-specific host/platform requirement.

## Preconditions

- the Executor has loaded current repository instructions and the active Task Contract according to source bootstrap policy;
- the actual local target path is resolved before mutation;
- an existing path is inspected before any delete/reset/overwrite action;
- unrepresented local work is preserved; ambiguity blocks destructive recovery;
- required network/credential use fits the current D033 envelope;
- installed adapter/tool versions can be identified.

## Semantic steps

### Step `resolve-target` — bind local and remote identity

- Required effect: `OBSERVE`.
- Determine canonical repository/remote identity, intended local path and base branch.
- If the local path already exists, inspect ownership/repository/status before mutation.
- Postcondition: the Executor can prove whether a safe existing checkout may be reused/reconciled or a new checkout path is required.
- Failure route: `BLOCKED` on ambiguous ownership/unrepresented work.

### Step `resolve-git-operation` — obtain a safe Git adapter realization

- Required effects: `OBSERVE`; documentation network lookup may require `NETWORK_CONNECT`.
- Check for a current compatible verified operation recipe when native recipe persistence exists.
- If absent/stale, use installed Git help/version plus official Git documentation under D054 before constructing the candidate operation.
- Do not use a chat snippet/model memory as sole syntax authority.
- Postcondition: Git operation is bound to the intended remote/base/path without destructive overwrite semantics.

### Step `materialize-or-reconcile` — establish current checkout

- Required effects: `NETWORK_CONNECT`, `MUTATE_SCOPED`, `EXECUTE_LOCAL`.
- Obtain/reconcile repository state using the resolved Git adapter operation.
- Preserve local/uncommitted work. Do not force-reset, clean, overwrite or delete ambiguous existing state to make the operation convenient.
- Postcondition: local base branch is current with the canonical remote base and the worktree is in the task-required safe state.
- Evidence: remote identity, branch identity, local HEAD, canonical remote HEAD, concise worktree status.

### Step `resolve-toolchain-operation` — obtain locked environment adapter realization

- Required effects: `OBSERVE`; package access may require `NETWORK_CONNECT`.
- Inspect repository-native toolchain authority and installed tool/version.
- Check for a compatible verified recipe when available; otherwise use installed/version-specific help and official tool documentation.
- Do not mutate global workstation configuration to satisfy a repository-local contract unless separately authorized.

### Step `prepare-locked-environment` — materialize repository-local dependencies

- Required effects: `EXECUTE_LOCAL`, `MUTATE_SCOPED`, and when applicable bounded `INSTALL_CONFIGURE`/`NETWORK_CONNECT`.
- Use the repository's locked dependency state and project-local environment semantics.
- Postcondition: the repository-local environment is consistent with committed dependency/lock authority.
- Evidence: tool/version identity and sanitized success/failure result.

### Step `handoff-ready` — prove bootstrap result

- Required effect: `OBSERVE`.
- Reconfirm remote/base/worktree identity after environment preparation.
- Do not infer that product tests are green merely because bootstrap succeeded; task-specific verification remains controlled by the Task Contract.
- Postcondition: the Executor has a current safe baseline from which the authorized implementation/review may start.

## Checkpoints and Human gates

Stop before continuing when:

- the intended local path contains unrepresented work that would be overwritten/discarded;
- remote/repository/branch identity differs from the Task Contract/canonical source;
- credentials resolve to an unexpected account/principal;
- required network/privilege falls outside the current envelope;
- official/version-specific documentation cannot resolve an unknown operation safely;
- a tool proposes an interactive/destructive action outside the pre-authorized effect boundary.

Normal low-risk command choice does not require the Human to copy/paste each command.

## Postconditions

- canonical remote identity verified;
- local base equals current authorized remote base;
- no unintended local work was discarded;
- locked project-local environment prepared according to repository authority;
- adapter/tool versions and relevant execution evidence are available for the task handoff;
- no global workstation policy change was used as a hidden correctness prerequisite.

## Recovery

If a newly created checkout/environment fails before becoming task state, cleanup may remove only artifacts proven to have been created by that failed invocation and only when doing so cannot discard unrelated work.

If safe ownership cannot be proven, leave the state intact and report `BLOCKED` with the smallest useful evidence.

Do not repair bootstrap failure by force-push, hidden history rewrite, global Git setting changes, disabling certificate/host verification, broad credential changes or privilege escalation without explicit current authority.

## Evidence

Capture the applicable sanitized subset:

- runbook ID/revision;
- adapter/tool identities and versions;
- authoritative documentation provenance for newly resolved operations;
- local target path class and remote identity;
- base/local/remote Git identities and concise status;
- project-local environment/bootstrap result;
- any blocked gate/deviation;
- provisional resolved-operation evidence during the pre-T035 bootstrap period.

After T035 native recipe persistence is active, eligible successful adapter operations may be promoted into verified recipes only through D054's provenance/postcondition/staleness contract.