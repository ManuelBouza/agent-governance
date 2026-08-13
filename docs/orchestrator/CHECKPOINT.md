# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O062  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is integrated.

Exact successful activation evidence:

- OP017 verified candidate HEAD `43a783ff5e8f810eaa8cf62aedca482feedc71d3`;
- `MARKDOWN_ONLY: YES`;
- focused pytest: PASS;
- full pytest: PASS;
- Ruff check: PASS;
- Ruff format-check: PASS;
- `REPO_MUTATION: NONE`;
- PR #87 merged exactly that tested candidate into `develop` as `85ccfac49e2e4a635f66c43fbedf95d54f7a6d29`.

Canonical Core is now:

```text
Protocol-Version: 1.13.0
ASSURANCE.md: ACTIVE
ASSURANCE routed in GOVERNANCE Source Map / Context Router
```

The original candidate PR #81 is closed/unmerged historical blocked evidence. PR #85, the attempted mechanical refresh of the old candidate, was closed without merge after GitHub reported it non-mergeable. The clean v2 path superseded both.

## T011

T011 — Assurance active-routing deterministic verification — is `ACCEPTED` and integrated.

- reviewed executor HEAD: `c231eec0cf5e96b676df9932402a3166fa4589c2`;
- acceptance PR #83 merged;
- implementation PR #84 merged;
- T011 proved both staged and active assurance routing without creating a second mutable current-protocol authority.

## Learning state

L001 — `verification.regression.protocol_version_drift` — returns to `VERIFIED` in the current Markdown recovery change.

Recovery basis:

```text
D040 single authority
+ T010 parser/validator readiness
+ T011 active-routing readiness
+ exact v2 OP017 PASS without mutation
+ exact tested PR #87 integration
= systemic control verified end-to-end
```

L002 — `task.handoff.identity_mismatch` — remains `ANALYZED`, separate and non-blocking.

## OpenCode worktree preflight

New host-specific preflight:

`docs/OPENCODE-WORKTREE-PREFLIGHT.md`

When the selected executor host is OpenCode and delegated work may use Git worktrees outside the OpenCode session working directory, ChatGPT must surface this preflight **before** the executor bootstrap prompt.

On the current workstation convention, the trusted repository-specific root is:

```text
~/projects/agent-governance-worktrees/**
```

The intended OpenCode behavior is a narrow `permission.external_directory` allow for that trusted root only. Do not use blanket external-directory allowance. OpenCode host configuration remains workstation state, not product/correctness authority.

This host adaptation does not prescribe use of OpenCode or worktrees; D041 executor-process autonomy remains unchanged.

## OP018 — completion-branch cleanup

Operational Contract:

`docs/operations/OP018-retire-d040-t011-completion-branches.md`

Status: `DRAFT` until the PR integrating this checkpoint, L001 recovery, OpenCode preflight and OP018 is opened/recorded/merged.

OP018 is a bounded cleanup for:

- merged T011 acceptance/implementation branches;
- merged D040 v2 control/activation branches;
- the branch integrating this recovery/preflight change;
- closed superseded PR #81 branch only if exact no-later-work/supersession conditions are proven;
- abandoned temporary `docs/d040-candidate-refresh-operation` only if Git proves it has no unique commits.

Ambiguous branches remain `REVIEW`; cleanup returns `PARTIAL` rather than guessing.

## CodeGraph next

After OP018 closes the D040/T011 branch backlog, CodeGraph project initialization is the next separate capability operation.

Required outcome for that later scope:

```text
CodeGraph initialized locally for agent-governance
.codegraph/ remains generated local state
canonical .gitignore excludes .codegraph/
Git remains clean after initialization
CodeGraph is executor capability, not Governance authority/correctness dependency
```

Context7 remains an optional executor-host external documentation capability and requires no repository state when already supplied by the host.

## Executor bootstrap policy

D041:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D042 requires canonical remote freshness before persisted contract load.

D043 normal launches omit explicit `AGENTS.md` reload unless the immediately governing integrated change modified `AGENTS.md`.

This recovery/preflight change does **not** modify `AGENTS.md`, so the next executor launch uses the normal D043 form. The OpenCode worktree permission step is Human/Orchestrator preflight outside the transport-only executor prompt.

## Next Action

1. Open/review/merge the Markdown recovery/preflight PR from `docs/opencode-worktree-bootstrap-and-l001-recovery`.
2. Record that merged PR identity in OP018 and mark OP018 `READY` before execution.
3. If the selected executor host for OP018 is OpenCode, surface `docs/OPENCODE-WORKTREE-PREFLIGHT.md` and ensure the narrow trusted worktree-root permission is configured/approved before presenting the OP018 bootstrap prompt.
4. Execute OP018 and independently verify final remote branch state.
5. Then persist and execute the separate CodeGraph initialization / `.gitignore` scope.
6. Do not start real-system assurance adapters/providers unless a later explicit decision/Task Contract authorizes them.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. while this Markdown recovery/preflight PR is pending, load L001 + OP018 + `docs/OPENCODE-WORKTREE-PREFLIGHT.md`;
2. for OP018 execution/result review, load OP018 + branch-cleanup policy + canonical PR/branch metadata;
3. for CodeGraph activation, load current `.gitignore`, D041, `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` and the new persisted CodeGraph contract;
4. load L002 only on a concrete identity conflict or explicit separate control-selection work.

## Do Not

- Do not reopen or merge historical blocked PR #81.
- Do not mark L001 CONTROL_FAILURE after the verified recovery unless the fingerprint recurs or new evidence invalidates the control.
- Do not delete ambiguous/superseded branches without exact Git evidence.
- Do not use blanket OpenCode `external_directory` allowance to suppress worktree prompts.
- Do not put workstation OpenCode configuration into product correctness semantics.
- Do not initialize CodeGraph inside OP018.
- Do not write directly to `develop` or `main`.
- Do not prescribe executor-internal methodology/tool routing.
- Do not add an unconditional `read AGENTS.md` directive to normal executor launch prompts.
- Preserve prior procedural audit history.
