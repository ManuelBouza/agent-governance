# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O063  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is integrated and operationally closed. Protocol `1.13.0` is active, `ASSURANCE.md` is ACTIVE/routed, and L001 `verification.regression.protocol_version_drift` is `VERIFIED`.

OP018 completed the D040/T011 cleanup. Canonical remote branch inventory after independent verification was exactly:

```text
develop
main
```

L002 remains `ANALYZED`, separate and non-blocking.

## CodeGraph activation sequence

CodeGraph is the active next capability scope.

Repository inspection shows root `.gitignore` currently contains local AI runtime state for `.atl/` but does not yet ignore `.codegraph/`.

The activation is intentionally split:

```text
T012
  -> canonically ignore .codegraph/
  -> prove generated state stays outside Git
  -> accept / integrate / clean
        ↓
local activation operation
  -> initialize CodeGraph in the canonical local checkout
  -> verify usable
  -> verify Git remains clean
```

This avoids treating an index created inside a disposable implementation worktree as durable activation for the checkout used by future executor sessions.

## T012

Task Contract:

`docs/tasks/T012-codegraph-local-state-ignore.md`

Status: `READY` after this planning change is integrated.

Tracked implementation scope is limited to root `.gitignore` plus the required executor handoff. CodeGraph remains optional executor-local capability, not Governance authority, product/runtime state or correctness dependency.

Required verification includes Git ignore evidence plus full pytest/Ruff gates.

## OP020 — planning cleanup

Operational Contract:

`docs/operations/OP020-retire-t012-planning-branch.md`

OP020 remains `DRAFT` until the planning PR identity is recorded and merged.

## OpenCode preflight

When the selected executor host is OpenCode and the delegated execution may use repository-external worktrees, surface `docs/OPENCODE-WORKTREE-PREFLIGHT.md` before the executor bootstrap prompt.

Current workstation convention:

```text
~/projects/agent-governance-worktrees/**
```

Use the narrow OpenCode `permission.external_directory` allowlist for that trusted root only. Host configuration remains workstation state and is not part of task semantics.

## Executor bootstrap policy

D041 remains:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D042 requires canonical remote freshness before persisted contract load.

D043 normal launches omit explicit `AGENTS.md` reload unless the immediately governing integrated change modified `AGENTS.md`. This planning change does not modify `AGENTS.md`.

## Next Action

1. Open/review the T012 planning PR from `docs/t012-codegraph-ignore-readiness`.
2. Record the actual PR identity in OP020, mark OP020 `READY`, merge the planning PR and freeze its source branch.
3. If OpenCode will execute OP020, apply the OpenCode worktree preflight before launch.
4. Execute OP020 and independently verify planning-branch cleanup.
5. If OpenCode will execute T012, apply the same preflight before launch.
6. Launch T012 from current `develop` containing the exact Task Contract.
7. Review remote handoff/diff/evidence; accept/integrate/clean T012 under normal workflow.
8. Only after `.codegraph/` ignore is canonical and T012 is closed, persist the separate local CodeGraph initialization operation.
9. Context7 remains optional host documentation capability and requires no repository change.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. while T012 planning is pending, load T012 + OP020 + current `.gitignore` + D041;
2. for T012 review, load exact handoff/diff + T012;
3. after T012 closure, load current `.gitignore`, `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md` and the new local CodeGraph activation operation;
4. load L002 only on a concrete identity conflict or explicit separate work.

## Do Not

- Do not initialize durable CodeGraph state in a disposable task worktree and call that canonical activation.
- Do not commit `.codegraph/` content.
- Do not make CodeGraph a product/runtime/correctness dependency.
- Do not prescribe CodeGraph as the executor's mandatory internal navigation method.
- Do not put OpenCode workstation configuration into repository correctness semantics.
- Do not use blanket OpenCode external-directory permission.
- Do not write directly to `develop` or `main`.
- Do not add an unconditional `read AGENTS.md` directive to normal executor launch prompts.
