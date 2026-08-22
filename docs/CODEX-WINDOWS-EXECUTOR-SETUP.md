# Codex Windows Executor Setup

Status: ACTIVE HOST ADAPTATION  
Research baseline: 2026-08-22

## Purpose

Define the recommended workstation and Codex configuration for using the ChatGPT desktop app / Codex natively on Windows as the Agent Governance source-product **Agente de IA Ejecutor**.

This is a host adaptation only. Codex does not become a governance role, repository authority, acceptance authority, or product dependency. `AGENTS.md`, persisted Task Contracts, review/rework records, Git state, and the normal source-maintenance workflow remain authoritative.

This document is deliberately stricter for the first Codex execution because the current migration from OpenCode + Gentle-IA/WSL is also an **executor-independence test**: Codex should be able to reconstruct and execute the task from canonical Git state without inheriting project semantics from the previous host.

## Target operating profile

For the current workstation and independence test, the preferred baseline is:

```text
Host OS              = Windows 11
Codex agent           = Windows native
Repository filesystem = native Windows/NTFS
Agent shell           = PowerShell
Codex sandbox         = elevated
Execution sandbox     = workspace-write
Approval policy       = on-request, Human reviewer
Command network       = off by default; escalate only when needed
Project instructions  = repository AGENTS.md
Local Codex memories  = off for independence baseline
Gentle-IA             = not loaded
Project-aware MCP     = not loaded
Project-aware Skills  = not loaded from user/global state
Project-aware hooks   = not loaded from user/global state
Initial T021 mode     = Local checkout, not Codex-managed detached worktree
```

Windows native is preferred here specifically to exercise the new host boundary. Do not silently fall back to the previous WSL/Gentle-IA execution environment merely because it already works.

## 1. Windows and repository placement

Use a fully updated Windows 11 workstation. OpenAI documents Windows 11 as the recommended native Windows baseline and provides a stronger `elevated` native sandbox plus an `unelevated` fallback.

When the Codex agent runs natively on Windows, keep the repository on the native Windows filesystem. OpenAI recommends this layout over opening a repository from `\\wsl$` when retaining the Windows-native agent.

Preferred shape:

```text
C:\...\agent-governance
```

Avoid using the old WSL checkout as the Codex execution checkout for the independence run. The WSL checkout may remain on disk, but it is not execution authority and must not be used as hidden state.

## 2. Required workstation tools

The repository's canonical source-maintenance requirements remain those in `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`:

- Git;
- uv compatible with `tool.uv.required-version` in `pyproject.toml`;
- a working GitHub fetch/push path;
- the selected executor host.

For Codex on Windows, additionally install native Git so the desktop app's Git/review functionality works correctly. GitHub CLI (`gh`) is recommended for authentication and diagnostics but is not an Agent Governance correctness dependency.

OpenAI also recommends common local developer tools such as Node.js and Python for general Codex use. For this repository, however, do **not** make Node.js or a separately installed global Python an acceptance requirement merely because Codex can use them. `uv` remains the canonical Python/runtime/environment manager for this source product.

### Windows tool check

Run from native PowerShell:

```powershell
git --version
uv --version
gh --version
gh auth status
```

If `uv` is absent, the upstream Windows standalone installer is:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, open a new terminal if required and verify `uv --version`.

Authentication readiness is satisfied by either a working Git SSH/HTTPS credential path or GitHub CLI-backed credentials as appropriate to the workstation. Do not store GitHub tokens, SSH private keys, or other credentials in this repository or Codex project instructions.

## 3. Codex home and configuration boundary

On native Windows, the ChatGPT desktop app uses:

```text
%USERPROFILE%\.codex
```

as the Codex home directory.

Codex configuration precedence places project `.codex/config.toml` above user config, but project-scoped `.codex` layers load only for trusted projects. The repository currently does not require a committed Codex configuration file.

For the independence baseline, keep **host safety configuration** in the user-level file:

```text
%USERPROFILE%\.codex\config.toml
```

and keep **project semantics** in canonical repository files, primarily root `AGENTS.md` and the persisted task/review documents.

Do not create a global `%USERPROFILE%\.codex\AGENTS.md` or `AGENTS.override.md` containing Agent Governance task semantics, decisions, branch state, or previous-chat summaries. Such content would weaken the independence test by injecting non-repository authority into every Codex session.

## 4. Recommended `config.toml` baseline

Recommended user-level baseline for this repository:

```toml
approval_policy = "on-request"
approvals_reviewer = "user"
sandbox_mode = "workspace-write"

# Optional hardening. Keep only if it does not break required local tooling.
allow_login_shell = false

[windows]
sandbox = "elevated"
sandbox_private_desktop = true

[sandbox_workspace_write]
network_access = false
```

Rationale:

- `workspace-write` lets Codex read, edit, and run commands inside the repository without forcing an approval for every normal local operation;
- `on-request` preserves explicit Human approval for operations that require escalation, including network or out-of-workspace access;
- `approvals_reviewer = "user"` keeps the Human Owner as the approval endpoint during the independence baseline rather than delegating approvals to Auto-review;
- `elevated` is OpenAI's preferred stronger native Windows sandbox;
- the private desktop is the stronger default UI-isolation mode;
- command network stays disabled by default, matching this repository's separation between provisioning/Git network and deterministic test-runtime behavior.

Do not use `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, or permanent full-access mode for ordinary Agent Governance execution.

### Network handling

Ordinary deterministic tests do not need network access. Network may legitimately be required for:

- `git fetch` / final authorized `git push`;
- `uv sync --locked` when the new workstation needs Python or locked dependencies;
- other provisioning explicitly allowed by the Task Contract/toolchain policy.

Keep network off by default and approve an escalation when it is genuinely needed. Do not enable broad permanent network access merely to remove prompts.

If a future workflow requires persistent command network, Codex supports enabling it under `[sandbox_workspace_write]`, and can additionally constrain traffic through its network proxy/domain policy. That is not required for the current T021 independence run.

## 5. Repository trust

Mark only the intended `agent-governance` checkout as trusted in Codex after verifying:

```powershell
git rev-parse --show-toplevel
git remote -v
git status --short --branch
```

The reported root must be the newly created native-Windows project, and `origin` must identify the canonical Agent Governance repository.

Trust is material because Codex skips project-local `.codex` configuration, hooks, and rules for untrusted projects. Trust does **not** enlarge the Agent Governance Task Contract or repository write authority.

## 6. Instructions: use the existing `AGENTS.md`

Codex natively discovers `AGENTS.md`. From the Git/project root it walks toward the current working directory and merges applicable instruction files, with nearer instructions taking precedence. It also supports a global Codex-home instruction file.

Agent Governance already has the correct root instruction surface: `AGENTS.md`. Do not create a duplicate `CODEX.md`, project-level global prompt, or pasted replica of `AGENTS.md` merely to make Codex work.

For the first independence run:

- root `AGENTS.md` is the project-level instruction authority;
- no Codex-home `AGENTS.override.md` may inject Agent Governance semantics;
- any Codex-home `AGENTS.md` should be absent or limited to generic personal/workstation conventions that cannot alter project authority;
- no nested `AGENTS.override.md` should be added merely for Codex unless the repository later has a genuine scoped-instruction need.

Codex's default combined project-instruction budget is 32 KiB. Do not raise that budget preemptively; first preserve the repository's progressive-loading design.

### Instruction-source verification

Before T021 execution, start a **fresh Codex chat** in the repository and ask, without authorizing mutation:

```text
Summarize the active repository instructions and identify the instruction files/sources you loaded. Do not modify files.
```

If Codex CLI is installed, the upstream diagnostic form is:

```powershell
codex --ask-for-approval never "Summarize the current instructions."
```

and `codex status` can be used to verify the workspace root.

Unexpected global instructions or an unexpected workspace root are a preflight failure; correct them before delegating T021.

## 7. Memories: keep them off for the independence baseline

Local Codex memories are a separate local state layer under the Codex home directory. OpenAI currently documents local memories as **off by default** and explicitly recommends keeping required team guidance in `AGENTS.md` or checked-in documentation rather than relying on memory.

For the first Agent Governance Codex run:

```text
use existing local memories      = off
create future memory from T021   = off
```

Use `/memories` in the Codex chat to verify the chat cannot consume old local memories and will not generate future project memory during this baseline.

This is an independence-test constraint, not a permanent rejection of Codex memory. After host independence is demonstrated, local memory may be evaluated separately as an optional productivity layer, but it must never become required authority or the only location of task semantics.

## 8. Model and reasoning setting

As of the research baseline date, OpenAI recommends GPT-5.6 Sol for difficult, open-ended coding and research, with medium as the default reasoning level and higher reasoning levels for more complex work.

For T021-R1:

```text
Model     = GPT-5.6 Sol
Reasoning = High initially
Ultra     = off for the first independence run
```

High reasoning is appropriate because T021 requires safe Git reconciliation, preservation of an accepted refactor baseline, a narrowly scoped fail-closed correction, and complete verification.

Do not hard-code a model name into repository state merely for this run. Model availability changes faster than the governance contract. Select the current recommended capable model in the Codex UI/session and record host/model information only when the normal handoff schema calls for relevant execution evidence.

Ultra/subagents are not prohibited by Agent Governance—D041 leaves implementation process to the executor—but keeping Ultra off for the first run makes the host-independence observation easier to interpret. It can be evaluated separately later.

## 9. MCP, Skills, plugins and Gentle-IA

Codex can use MCP servers, Skills/plugins and other extension surfaces. They are **not required** for a cold Agent Governance source-product executor bootstrap.

For the first independence run, do not load:

- Gentle-IA or a compatibility bridge to it;
- an MCP server that carries prior Agent Governance project/chat state;
- a user/global Skill containing Agent Governance task history or hidden workflow semantics;
- an extension whose required output substitutes for the persisted Task Contract or handoff.

This does not prohibit ordinary built-in Codex capabilities. It isolates the experiment: the executor should succeed from Git + repository instructions + the Task Contract rather than from previous-host context.

After independence is demonstrated, MCP/Skills may be evaluated under the repository's existing capability/supply-chain/coexistence policies. Codex Skills use progressive disclosure, which is architecturally compatible with Agent Governance, but an installed Skill remains tooling rather than authority.

## 10. Hooks and Rules

Codex provides host-native Rules for commands outside the sandbox and hooks around tool execution. These can be useful hardening mechanisms, but they should **not** be introduced silently before the first independence baseline.

Reasons:

- Codex Rules are currently documented as experimental;
- hidden user/global Rules or hooks could alter execution independently of the repository;
- hooks are useful guardrails but are not a complete enforcement boundary;
- Agent Governance already has explicit ownership, scope, branch and publication policy that must remain the semantic authority.

Therefore, baseline policy is:

```text
custom project-aware user rules = none
custom project-aware user hooks = none
```

After the first successful Codex run, a separate hardening task may evaluate narrow Rules/hooks for defense in depth—for example, protecting destructive Git operations or host-specific forbidden writes—without redefining Agent Governance semantics. Any Rules file should be tested with `codex execpolicy check` before relying on it operationally.

## 11. Worktrees and T021

Codex has strong managed-worktree support, but managed worktrees start in detached `HEAD` state under `$CODEX_HOME/worktrees` by default.

That behavior is useful for parallel greenfield tasks, but **T021-R1 is a special re-entry case**:

- a remote T021 topic branch already exists;
- its represented history must be preserved;
- current `develop` must be reconciled into that existing work without discarding/recreating history;
- force-pushing rewritten history is not authorized;
- D048 permits only the planned terminal publication boundary.

For this first run, use **Local** mode against the native-Windows repository checkout rather than asking Codex to create an automatic detached worktree. Let the executor inspect Git state and choose a history-preserving reconciliation mechanism inside the existing T021 contract/checkpoint boundary.

This is T021-specific. Future tasks can use Codex-managed worktrees after their branch/publication lifecycle is confirmed compatible with the governing Task Contract.

## 12. Fresh-checkout reproducibility preflight

Before giving Codex T021 implementation authority, prove that the Windows checkout can bootstrap from repository state alone.

From native PowerShell at the project root:

```powershell
git status --short --branch
git fetch --prune origin
git rev-parse origin/develop
git ls-remote origin refs/heads/refactor/t021-consumer-profile-abstraction
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

Interpretation:

- Git identity/read access must work;
- the current remote `develop` and remote T021 branch must be visible;
- `uv sync --locked` must reproduce the repository environment without ad-hoc dependency edits;
- the canonical deterministic baseline must be green before T021 mutation, otherwise the executor stops/escalates per the checkpoint rather than absorbing unrelated repairs.

The full T021 verification matrix remains governed by the T021 Task Contract and review record. This preflight does not replace it.

## 13. Git write/publication readiness

Before launch, verify read-only remote access and authentication diagnostics. Do **not** perform a test push to the T021 branch just to prove credentials: D048 deliberately constrains intermediate publication.

At terminal T021 completion, the executor must follow the persisted T021/D048 sequence and perform the single planned final push of the complete authorized branch state, then verify remote HEAD.

Codex permissions are not authorization to bypass branch policy. A Codex approval prompt for Git/network access is only a host-security approval; the Task Contract still decides whether that Git operation is permitted.

## 14. T021 independence-test launch conditions

Do not launch T021 until all of these are true:

- [ ] Windows 11 is current enough for the native Codex sandbox.
- [ ] The Agent environment is explicitly **Windows native**.
- [ ] The repository lives on a native Windows filesystem.
- [ ] Native Git works and points to the canonical repository.
- [ ] `uv` works and satisfies repository requirements.
- [ ] GitHub read/authentication diagnostics succeed.
- [ ] Codex sandbox is `elevated` (or a Human-approved documented fallback is required).
- [ ] Session mode is `workspace-write` + `on-request`, with Human approval review.
- [ ] Command network is off by default.
- [ ] Project is intentionally trusted after repository identity verification.
- [ ] Root `AGENTS.md` is detected as project instruction authority.
- [ ] No project-semantic Codex-home `AGENTS.md` / `AGENTS.override.md` contaminates the run.
- [ ] Local Codex memories are disabled for the baseline chat.
- [ ] Gentle-IA is not connected to the baseline run.
- [ ] No project-aware MCP/Skill/hook/rule supplies hidden prior Agent Governance state.
- [ ] A fresh Codex chat is used.
- [ ] The clean `uv sync --locked` bootstrap succeeds.
- [ ] The canonical deterministic suite is green before T021 mutation.
- [ ] The remote T021 branch still matches the Orchestrator checkpoint when execution starts.

A failure of a workstation item is a host-preflight issue, not authority to change T021 scope.

## 15. Recommended T021 launch transport

Once the checklist above is satisfied, the launch message should remain intentionally small:

```text
Repository: https://github.com/ManuelBouza/agent-governance
Use current remote develop and the current repository instructions.
Execute T021-R1 only.
Task Contract: docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
Follow docs/reviews/T021-R1.md and docs/orchestrator/CHECKPOINT.md.
```

Do not paste old OpenCode/Gentle-IA plans, prior executor reasoning, stale local diffs, or a chat-derived implementation recipe. The point of the test is that Codex reconstructs execution from canonical Git authority.

## 16. Post-baseline enhancements to evaluate separately

After one clean Codex/Windows task succeeds, useful follow-up experiments include:

1. **Codex-managed worktrees** for independent parallel tasks whose contracts allow their branch lifecycle.
2. **Narrow Rules** for defense-in-depth around dangerous out-of-sandbox commands.
3. **Hooks** for observable workstation policy checks, while retaining repository policy as authority.
4. **MCP** for approved external services where it reduces operational friction without importing hidden project authority.
5. **Skills** for reusable executor techniques after supply-chain/coexistence review.
6. **Auto-review** for selected host-level permission requests after the Human-reviewed baseline is understood.
7. **Local memories** as a non-authoritative productivity layer, tested separately from cold-start correctness.
8. **Ultra/subagents** for tasks that genuinely benefit from parallel decomposition.
9. A committed `.codex/config.toml` adapter only if a dedicated repository change establishes that portable project-level Codex configuration is worth owning. Such a file is non-Markdown and must follow normal Agent Governance ownership/Task Contract rules; it must not be smuggled into T021.

## Repository-state boundary

User-level Codex configuration, credentials, local memories, sandbox state, and app settings are workstation state. They are not canonical Agent Governance product state.

This repository documents the desired host outcome and the independence-test controls. It does not version personal credentials, user-global Codex configuration, or local Codex memory.

## Orchestrator launch rule

When Codex/Windows is selected as executor host, the Orchestrator should surface this preflight before executor launch when the workstation has not already been validated for the current environment.

For the first migration run from OpenCode/Gentle-IA, the Human Owner should explicitly confirm the launch-condition checklist before T021 is delegated. After a stable Codex baseline is established, later tasks may use a shorter host check when no relevant workstation configuration changed.

## Upstream references

Research checked on 2026-08-22 against:

- OpenAI Codex/ChatGPT Windows app: https://developers.openai.com/codex/app/windows/
- OpenAI native Windows sandbox: https://developers.openai.com/codex/windows/
- OpenAI Codex configuration basics: https://developers.openai.com/codex/config-basic/
- OpenAI `AGENTS.md` discovery: https://developers.openai.com/codex/guides/agents-md/
- OpenAI agent approvals and security: https://developers.openai.com/codex/agent-approvals-security/
- OpenAI Codex models: https://developers.openai.com/codex/models/
- OpenAI Codex memories: https://developers.openai.com/codex/memories/
- OpenAI Codex Rules: https://developers.openai.com/codex/rules/
- OpenAI Codex worktrees: https://developers.openai.com/codex/app/worktrees/
- OpenAI Codex hooks: https://developers.openai.com/codex/hooks/
- OpenAI Codex Skills: https://developers.openai.com/codex/skills/
- OpenAI Codex MCP: https://developers.openai.com/codex/mcp/
- Astral uv installation: https://docs.astral.sh/uv/getting-started/installation/

Re-check upstream behavior before changing durable host configuration when Codex changes sandbox, configuration, instruction-discovery, memory, or worktree semantics materially.
