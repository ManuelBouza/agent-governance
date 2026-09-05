# Long-Lived Branch Protection Runbook

Status: ACTIVE  
Controlling decision: `docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md`  
Source-product write guard: `docs/decisions/D061-orchestrator-branch-target-write-guard.md`

## Purpose

Provide a repeatable provider-adapter procedure for establishing and verifying server-side protection of long-lived branches before normal agentic writable work.

This runbook implements a provider-neutral invariant. UI labels and API fields may change; verify the current provider surface instead of relying on memory when they do.

## Required semantic outcome

For each repository long-lived integration/stable branch:

```text
normal changes require PR/MR transport
branch deletion restricted
force/non-fast-forward updates blocked
normal agent/app/connector has no routine bypass
control is active/enforced
```

Project-native stronger controls remain in force.

## Preflight

Before changing repository settings:

1. identify the repository provider and administrative owner;
2. identify the default/stable branch from provider truth;
3. identify any normal integration/development branch;
4. inspect existing branch/ruleset/protected-branch controls;
5. inspect existing bypass/exception actors;
6. classify the current state as `REUSE`, `ADAPT`, `MISSING`, or `CONFLICT`;
7. do not weaken existing stronger compatible rules.

Do not assume the branch names are `main` and `develop`.

## GitHub adapter

### Create the ruleset

Repository UI:

```text
Settings
-> Rules
-> Rulesets
-> New ruleset
-> New branch ruleset
```

Recommended baseline name:

```text
Protect long-lived branches
```

Set:

```text
Enforcement status: Active
```

### Bypass list

The baseline safety posture is:

```text
Bypass list: empty for normal agentic writers
```

Do not grant routine bypass to the app/connector/user used by ChatGPT, Codex, another Executor, CI mutation bot, or ordinary automated repository writer merely for convenience.

A narrowly scoped recovery/administration actor may exist only when the repository owner intentionally requires it and the risk is documented. It must not become the normal agentic write identity.

### Target branches

Add the actual long-lived branches discovered in preflight.

For this source repository the targets are:

```text
main
develop
```

Do not target all topic branches unless the repository intentionally needs a stronger workflow; Agent Governance normally expects task/topic branches to remain writable by their owning work unit.

### Baseline rules

Enable the semantic equivalents of:

```text
[x] Restrict deletions
[x] Require a pull request before merging
[x] Block force pushes
```

For the PR rule, a baseline of:

```text
Required approvals: 0
```

is sufficient for the specific invariant of forcing PR transport. Independent review requirements are a separate project policy and may be stronger.

Do not enable `Restrict updates` as a generic baseline unless the project has deliberately designed the corresponding bypass/merge architecture; it can prevent ordinary PR merges.

Optional controls such as required status checks, signed commits, code-owner reviews, last-push approval, deployment gates, linear history, security scans or coverage thresholds are project-specific. Preserve them when already required.

Allowed merge methods are project policy. Agent Governance does not require changing them merely to establish this safety control.

### Save

Create/save the ruleset and confirm it remains `Active`.

## GitHub verification

Prefer effective provider state over screenshots alone.

Verify the repository ruleset read surface and confirm:

```text
enforcement == active
ref targets include the intended long-lived branches
rules include pull_request
rules include deletion restriction
rules include non_fast_forward / force-push block
bypass actors do not include the normal agentic writer
```

For GitHub REST the relevant effective-state surfaces are the repository rulesets collection and the selected repository ruleset resource.

A branch endpoint may report `protected: true` when a ruleset applies even though the legacy branch-protection payload is not the controlling mechanism. Verify the ruleset itself rather than inferring detailed semantics from the branch boolean.

### Do not prove by damaging the branch

Do not intentionally issue a direct content mutation, force push or branch delete against a protected long-lived branch merely to show rejection when the provider exposes the effective configuration directly.

Configuration-state verification is the preferred non-destructive proof.

## Current source-product verified configuration

The canonical source repository currently uses:

```text
Repository: ManuelBouza/agent-governance
Provider: GitHub
Ruleset ID: 22339910
Ruleset name: Protect long-lived branches
Enforcement: active
Targets: refs/heads/main, refs/heads/develop
Bypass actors: none
Current connected actor bypass: never
Rules:
  deletion restriction
  non-fast-forward / force-push block
  pull request required
Required approvals: 0
Allowed merge methods: merge, squash, rebase
Verified: 2026-09-05
```

The canonical durable record is `docs/REPOSITORY-SAFETY-CONTROLS-LEDGER.md`.

## Consumer-project bootstrap procedure

For a new Agent Governance adopting repository:

```text
read-only repository/coexistence inspection
-> discover provider + long-lived branches + existing protection
-> if minimum control already satisfied: verify and REUSE
-> if missing and agent can administer safely: apply provider-equivalent control
-> if missing and agent cannot administer: REQUIRE_HUMAN with provider steps
-> verify effective provider-side state
-> record durable receipt in the project's existing security/operations/governance record surface
-> mark repository writable-ready
-> proceed with normal governed writable work through topic branches + PR/MR
```

Do not invent a new project-local ledger file if the project already has a compatible security/operations control ledger. Reuse/adapt under coexistence rules.

If no durable project-native receipt surface exists, Strategy should establish a minimal auditable record as part of governance bootstrap rather than relying on chat history. The exact installed path remains a packaging/design concern until the Consumer distribution defines it canonically.

## Other provider mapping

For GitLab, Bitbucket, Azure DevOps or another provider, map the invariant semantically rather than copying GitHub labels.

Required mapping questions:

```text
What server-side mechanism protects the default/integration branches?
Does it require merge-request/pull-request flow?
Can direct/force updates still occur?
Can the branch be deleted?
Which users/apps/tokens can bypass it?
Can effective configuration be read back after setup?
```

If the provider cannot satisfy an equivalent control, stop normal writable readiness and obtain an explicit Human alternative-control/risk disposition.

## Revalidation

Re-run verification when:

- default/integration branch names change;
- ruleset/protection configuration changes;
- repository transfers organizations/providers;
- the normal agent app/connector identity changes;
- bypass actors change;
- an unexpected direct update occurs;
- repository administration policy changes.

## Failure handling

Return fail-closed when any required fact is unresolved:

```text
BLOCKED / REQUIRE_HUMAN
reason: <missing or conflicting protection fact>
provider: <provider>
targets: <known long-lived branches>
required_action: <bounded provider/admin action>
verification_needed: <effective-state read>
```

Do not convert repository-admin friction into permission to work unprotected.
