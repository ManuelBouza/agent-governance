# MG1-v9 Windows Temporary-Workspace ACL Analysis

Date: 2026-09-01  
Owner: ChatGPT Orchestrator  
Applies to: `T023` / successor method after `MG1-T023-EXECUTION-v9`

## Question

Why did the v9 synthetic Skill canary fail under both logical `read-only` and `workspace-write` even after Codex 0.149.0 successfully initialized the permitted native Windows `unelevated` backend?

## Evidence from v9

The accepted terminal evidence is in:

- `evals/skill_activation_topology/evidence/mg1-v9-codex-windows-gpt-5.6-sol-medium/backend-resolution.json`;
- `.../canary/unelevated-read-only-r1.json`;
- `.../canary/unelevated-workspace-write-r1.json`;
- `.../host-preflight.json`;
- `handoffs/T023-executor-handoff.json`.

The backend probe established:

- `elevated`: initialization timeout, no provider/model call;
- `unelevated`: initialized and executed the exact provider-free nonce command;
- user config remained isolated;
- dangerous bypass was not used.

The canary traces then show a broader filesystem failure than a `.agents`-specific block. Inside each disposable workspace, the sandboxed process failed to:

- read `.agents/skills/mx-canary/SKILL.md`;
- enumerate the current directory;
- enumerate `.agents`;
- use alternative ordinary file-enumeration/read commands against the same workspace.

The error is consistently Windows `Access is denied` / `Acceso denegado`.

The harness created these roots with Python `tempfile.TemporaryDirectory()` and `run-metadata` reports Python `3.13.14`.

## Python 3.13 Windows ACL change

CPython documents a security change in Python 3.13: on Windows, `os.mkdir()` / `os.makedirs()` with mode `0o700` applies access control that restricts the new directory to the current user and administrators. CPython notes that this affects `tempfile.mkdtemp` when its default private mode is used.

Relevant upstream sources:

- CPython `Doc/whatsnew/3.13.rst` / associated security change for Windows `0o700` directory ACLs;
- CPython news entry for the `tempfile.mkdtemp` security fix (CVE-2024-4030);
- CPython `Lib/tempfile.py`, where `mkdtemp` creates candidate directories with mode `0o700`.

This is materially relevant because the Codex `unelevated` backend executes commands with a restricted token/capability-SID ACL model. A directory whose DACL grants traversal/read only to the real interactive user/Administrators can therefore be inaccessible to the sandbox token even when that directory is selected as the command CWD.

## Independent Codex evidence

OpenAI Codex issue `#19791`, titled **Windows sandbox blocks pytest-xdist temp dirs created with Python 3.14/pytest 0o700 permissions**, documents the same failure mode on native Windows: `PermissionError: [WinError 5] Access is denied` for private temporary directories created with `0o700`, including temp roots moved inside the workspace.

Issue: `https://github.com/openai/codex/issues/19791`

The report specifically identifies the interaction between Python private temp-directory ACLs and Codex's restricted-token/ACL sandbox model. Although the report used Codex 0.125.0 / Python 3.14, the relevant Python ACL behavior is already present in Python 3.13, which is the exact v9 runtime.

## Exact Codex 0.149.0 source checks

### Normal Windows sandbox workspace

`codex-rs/windows-sandbox-rs/sandbox_smoketests.py` defines its workspace under the user's profile (`%USERPROFILE%/sbx_ws_tests`) and verifies expected read/write behavior there. It does not construct the command CWD through Python `TemporaryDirectory()`.

### `.agents` protection

`codex-rs/windows-sandbox-rs/src/workspace_acl.rs` protects `.agents` with `add_deny_write_ace`. This is a write-protection mechanism for protected workspace metadata, not a blanket read denial.

### Unelevated ACL model

`codex-rs/windows-sandbox-rs/src/unified_exec/backends/legacy.rs`, `spawn_prep.rs`, `allow.rs`, and `sandboxing/src/windows.rs` show that the restricted-token backend derives workspace allow/write roots and applies capability/ACL rules before spawning the process. The backend assumes the underlying Windows filesystem ACLs permit the sandbox token to traverse/read paths that its policy otherwise allows.

## Root-cause conclusion

The most specific supported explanation of the v9 observations is:

> The harness created each outer disposable workspace with Python 3.13 `TemporaryDirectory`, which uses private `0o700`-style Windows ACL semantics. The Codex unelevated restricted token therefore could not traverse/read the workspace root. The canary consequently failed before the experiment could test Skill-body accessibility.

This is an **Execution Adapter workspace-creation confound**.

It is not evidence that:

- `.agents` is inherently unreadable under Codex 0.149.0;
- the unelevated backend cannot support local Skills;
- any topology candidate failed activation semantics.

## Prospective correction boundary

A successor experiment may retain an OS-temporary disposable workspace while changing how its **outer root** is created.

The outer root must:

- be unique and fresh per attempt;
- remain under a neutral OS-temporary parent or another pre-authorized disposable Windows location;
- remain outside/not linked to the canonical repository;
- have no canonical `.git` metadata;
- inherit ordinary Windows ACLs compatible with the selected Codex sandbox rather than Python's private `0o700` temp-directory ACL;
- receive no broad manual `Everyone` grant and cause no parent-directory ACL mutation;
- be cleaned up host-side after evidence preservation.

The exact atomic Windows creation/cleanup command or API is an Execution Adapter detail owned by the Executor under D054.

## New provider-free workspace-access gate

Before a synthetic Skill canary, the successor must create a neutral file in the workspace and invoke the selected Codex native Windows sandbox **without provider/model access** to prove the sandbox can:

1. start in the exact workspace root;
2. enumerate/read the root;
3. read the neutral probe file exactly.

The gate must persist:

- workspace path;
- creation method identity;
- relevant ACL/DACL diagnostic output when available;
- requested/resolved native backend;
- logical sandbox identity;
- exact provider-free command/result;
- proof that no provider/model call occurred.

If the gate fails, stop `BLOCKED / WINDOWS_WORKSPACE_ACL_UNAVAILABLE` with zero synthetic model calls and zero acceptance calls.

Only after this gate passes may the unchanged mx-canary be issued.

## Isolation of variables

The first successor should continue to freeze:

- Codex CLI 0.149.0;
- native Windows;
- elevated-first / unelevated fallback policy;
- GPT-5.6 Sol / Medium live cell;
- candidate/reference bytes;
- corpus v4;
- trial envelope v2;
- thresholds and D050 selection;
- paired 2+1 and cost-bounded futility rules.

That isolates the workspace-ACL correction instead of combining it with a CLI upgrade or semantic experiment change.