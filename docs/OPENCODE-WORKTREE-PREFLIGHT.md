# OpenCode Worktree Permission Preflight

Status: ACTIVE HOST ADAPTATION

## Purpose

Avoid repeated OpenCode `external_directory` approval prompts when an Agent Governance executor operation uses Git worktrees outside the directory from which the OpenCode session was started.

This is a host/workstation adaptation only. It does not make OpenCode a repository dependency, does not authorize creation or use of a worktree by itself, and does not change Task/Operational Contract scope or D041 executor-process autonomy.

## When this applies

Apply this preflight only when all of the following are true:

- the selected Agente de IA Ejecutor host is OpenCode;
- the delegated work may use a Git worktree outside the OpenCode session working directory;
- the intended worktree root is already a trusted repository-specific local path.

If another executor host is selected, this document creates no requirement.

## Required pre-launch check

Before launching the delegated Task/Operational Contract, determine whether the trusted Agent Governance worktree root is already durably allowed by the effective OpenCode configuration.

On the current workstation convention, the expected repository-specific root is:

```text
~/projects/agent-governance-worktrees/**
```

If the workstation uses a different root, use that exact trusted repository-specific root instead. Do not broaden the rule merely to avoid prompts.

For the current OpenCode permission model, the intended configuration is equivalent to:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "external_directory": {
      "~/projects/agent-governance-worktrees/**": "allow"
    }
  }
}
```

OpenCode expands `~`/`$HOME` in permission patterns. `external_directory` is the permission used when tools touch paths outside the working directory where OpenCode started.

## Safety boundary

Use a narrow trusted-path allowlist.

```text
repo-specific trusted worktree root -> allow
unrelated external paths            -> retain normal OpenCode policy
```

Do not solve this by setting a blanket `external_directory: allow` rule or an equivalent global allow for arbitrary external directories.

The allowlist only prevents the extra external-directory prompt. The delegated contract, repository ownership rules, Git state, tool-specific permissions and any applicable execution authorization still control what the executor may do inside the allowed path.

## If the allowlist is not configured

Surface the missing preflight to the Human Owner **before** delegated execution begins.

The Human Owner may configure the narrow durable allowlist or approve the worktree path manually for the current OpenCode session. Session-only `Allow once` / `Allow always` approval is an operational fallback, not the preferred durable workstation setup.

Do not encode a Human home-directory absolute path, token, credential or machine secret in repository state.

## Repository-state boundary

OpenCode host configuration is workstation state, not Agent Governance product state, unless a later explicit adapter decision says otherwise.

This repository documents the required safety outcome; it does not version the Human Owner's global OpenCode configuration.

## Orchestrator launch rule

When the next delegated execution will use OpenCode, ChatGPT must surface this preflight before presenting the executor bootstrap prompt whenever repository-external worktrees may be used.

The Task/Operational launch prompt itself remains transport-only under D041/D042/D043. Do not duplicate this host configuration inside every persisted contract or task prompt.
