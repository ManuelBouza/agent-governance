# MG1-v8 Windows Sandbox Root-Cause Analysis

## Scope

This research closes the Specify re-entry opened by `docs/reviews/T023-R7.md` after MG1-v8 stopped `BLOCKED / HOST_CAPABILITY_PREFLIGHT` before any acceptance prompt.

The question is narrow: why did Codex CLI 0.149.0 reject every model-generated read of the synthetic `.agents/skills/mx-canary/SKILL.md` under both logical `read-only` and `workspace-write` modes even though local Skills are a supported Codex capability?

This document is method research only. It does not rescore v8, change candidate semantics, or authorize a live T023 restart by itself.

## Evidence from MG1-v8

The submitted v8 branch recorded:

- one `read-only` canary attempt and one `workspace-write` fallback attempt;
- every required `Get-Content`, `cmd /c type`, or equivalent Skill-body read rejected as `blocked by policy`;
- no successful host-observed Skill-body read/use;
- no exact body nonce returned;
- zero acceptance prompts and zero scored observations;
- deterministic regressions green.

Because the preflight required 2/2 successful repetitions under one concrete profile, the first failure under each profile was already terminal. The harness correctly stopped before exposing `MG1-T023-CORPUS-v4`.

## Codex Skill loading model

Current Codex source confirms two distinct paths that must not be conflated.

### Explicit Skill selection

`codex-rs/core/src/session/turn.rs` collects explicit Skill mentions and calls `skills_snapshot.load_skill_prompts(...)` before sampling.

`codex-rs/ext/skills/src/host_prompt.rs` states that `load_skill_prompts` reads selected host Skills and builds model-visible prompt fragments. It calls `read_skill_text` and injects the resulting `SKILL.md` contents.

Therefore an explicitly selected `$skill` can be host-read and injected without requiring a model-generated shell command.

This does not solve T023. MG1 evaluates implicit activation/routing from ordinary user turns. Substituting explicit `$skill` invocation would change the property under test.

### Implicit activation

Codex Skill invocation logic recognizes a model command that reads a Skill document as an implicit Skill access. On Windows, PowerShell command parsing participates in that classification.

Therefore the v8 requirement for successful host-observable candidate-body read/use is consistent with the implicit route being evaluated. The problem is not that v8 expected a nonexistent Skill mechanism; the problem is that the command required to reach that mechanism was rejected before execution.

## Root cause

The decisive interaction is between `codex exec`, `--ignore-user-config`, and the native Windows sandbox backend.

### 1. `codex exec` is non-interactive and defaults approvals to Never

In the exact Codex 0.149.0 source (`rust-v0.149.0`, `codex-rs/exec/src/lib.rs`), headless exec sets:

```text
approval_policy = AskForApproval::Never
```

This is deliberate: a headless eval cannot stop for interactive approval.

### 2. The Windows sandbox implementation is a separate configuration axis

In the exact 0.149.0 protocol source (`codex-rs/protocol/src/config_types.rs`), `WindowsSandboxLevel` is:

```text
Disabled
RestrictedToken
Elevated
```

with `Disabled` as the default enum value.

The logical permission mode selected by `--sandbox read-only` or `--sandbox workspace-write` is not itself proof that a native Windows sandbox backend is active.

### 3. V8 intentionally ignored user config but did not restore the Windows backend inline

V8 used `--ignore-user-config` to prevent personal Codex configuration from contaminating the experiment. That was correct for isolation, but the harness then supplied only the logical sandbox mode and did not explicitly restore an equivalent `windows.sandbox` backend selection through the hermetic command/config overrides.

Consequently the eval could resolve the Windows backend as disabled while still carrying a logical read-only/workspace permission profile.

### 4. Codex 0.149.0 tests reproduce exactly this policy outcome

The exact 0.149.0 test file `codex-rs/core/src/exec_policy_windows_tests.rs` establishes:

- an unmatched PowerShell read requires approval when there is no active Windows sandbox backend;
- with `AskForApproval::Never`, a logical read-only profile and `WindowsSandboxLevel::Disabled` cause an unmatched command to be forbidden;
- the same applies to a writable/workspace permission profile when the Windows backend is disabled;
- when the Windows backend is `RestrictedToken` or `Elevated`, unmatched commands under a read-only profile are allowed to execute inside the sandbox even with approval policy Never.

This is the closest available executable specification for the exact failure observed in v8.

## Why `.agents` protection is not the root cause

Codex treats `.agents`, `.codex`, and `.git` as protected workspace metadata. That protection matters primarily to write semantics inside writable roots.

Current Windows sandbox code explicitly models protected metadata through read-only/write-deny carveouts and distinguishes those from deny-read restrictions. The restricted-token backend cannot enforce arbitrary deny-read restrictions and the elevated backend handles them separately.

Therefore the presence of `.agents` under the workspace does not, by itself, explain why simple read commands were rejected before execution. The disabled native backend plus headless `AskForApproval::Never` does.

## Supported corrective direction

Official Codex Windows documentation exposes a native Windows sandbox selection with a preferred elevated implementation and an unelevated/restricted-token fallback. Codex CLI also supports per-invocation configuration overrides.

The next acceptance method should therefore remain hermetic while explicitly binding the concrete Windows backend instead of relying on ignored user configuration.

The required effective state is:

1. continue ignoring user config and project/user execpolicy rules;
2. explicitly select the native Windows sandbox backend through the invocation's configuration override;
3. prefer the elevated backend;
4. use the unelevated/restricted-token backend only as a preregistered fallback when elevated cannot initialize or cannot pass the unchanged canary;
5. retain logical `read-only` first and `workspace-write` only as the existing least-permissive fallback;
6. require the unchanged synthetic Skill canary to pass 2/2 under the complete concrete profile before any acceptance prompt;
7. bind acceptance to the exact backend + logical sandbox profile that passed;
8. stop on any backend/profile drift.

Exact version-specific CLI/config syntax remains Executor-owned under D054. The experiment freezes the required effective state, not a chat-authored shell spelling.

## What must not be used as a shortcut

The following would change the claim or weaken the experiment and are rejected:

- `--dangerously-bypass-approvals-and-sandbox` / `--yolo`;
- explicit `$skill` invocation in place of implicit activation;
- pre-reading candidate bodies into the user prompt;
- adding an acceptance-specific read grant solely to bypass the native sandbox profile without proving it is part of the normal supported host route;
- enabling interactive approvals inside the acceptance cell;
- importing v8 observations into a successor score;
- changing candidate bytes, expected outcomes, thresholds, D050 percentages, or safety gates because of the v8 blocker.

## CLI-version boundary

V8 executed Codex CLI 0.149.0. A newer stable Codex release exists, but upgrading the CLI and changing the Windows sandbox binding in the same acceptance restart would confound two execution variables.

The narrow successor should keep Codex 0.149.0 for the first corrected canary/acceptance epoch unless that exact version cannot realize the required explicit backend binding. If it cannot, the run stops before acceptance and a separate prospective host-version revision is required.

## Conclusion

MG1-v8 exposed an **Execution Adapter configuration defect**, not evidence that Codex local Skills or the candidate topologies are intrinsically unusable.

The causal chain is:

```text
codex exec headless
  + approval policy Never
  + --ignore-user-config
  + no explicit native Windows sandbox backend restoration
  -> Windows sandbox backend can resolve Disabled
  -> unmatched Skill-body read requires approval
  -> approval cannot be surfaced
  -> command rejected as blocked by policy
```

A narrow v9 restart is justified prospectively. V9 should preserve v8 semantics and the unexposed v4 holdout while adding one immutable execution identity requirement: an explicitly selected native Windows sandbox backend that passes the unchanged canary twice before acceptance.

## Primary sources

- OpenAI Codex source, exact installed release `rust-v0.149.0`:
  - `codex-rs/exec/src/lib.rs`
  - `codex-rs/protocol/src/config_types.rs`
  - `codex-rs/core/src/exec_policy_windows_tests.rs`
- OpenAI Codex current source used to clarify Skill and Windows-sandbox architecture:
  - `codex-rs/core/src/session/turn.rs`
  - `codex-rs/ext/skills/src/host_prompt.rs`
  - `codex-rs/skills/src/invocation.rs`
  - `codex-rs/protocol/src/permissions.rs`
  - `codex-rs/sandboxing/src/windows.rs`
- Official Codex documentation:
  - Skills / progressive disclosure and explicit versus implicit activation
  - Windows sandbox configuration
  - CLI `--config` and `--ignore-user-config` / `--ignore-rules` behavior
