# D062 — Repository Long-Lived Branch Protection Bootstrap

Status: ACCEPTED  
Date: 2026-09-05  
Owner: Human Owner / ChatGPT Orchestrator  
Related: `docs/decisions/D061-orchestrator-branch-target-write-guard.md`

## Decision

Agent Governance adopts server-side protection of long-lived repository branches as a bootstrap safety invariant for governed repositories that support branch/ruleset protection.

The invariant is provider-neutral:

```text
identify long-lived branches
-> inspect existing server-side protection
-> preserve stronger compatible project-native controls
-> establish missing minimum protection through authorized repository administration
-> verify the effective provider-side state
-> record a durable safety-control receipt
-> only then permit normal agentic writable operation
```

A written branching policy is not sufficient when the repository provider can technically reject unsafe direct writes.

## Minimum effective control

For every long-lived branch that is a normal integration/stable target, the server-side control MUST provide the semantic equivalent of:

- changes reach the branch through a pull/merge request rather than routine direct update;
- branch deletion is restricted;
- force/non-fast-forward updates are blocked;
- the agent/app/connector used for normal automated repository writes has no routine bypass;
- the control is active/enforced, not merely drafted or evaluation-only.

Required review counts, status checks, code-owner review, signed commits, deployment gates, linear history and similar stronger controls remain project-specific. Agent Governance does not weaken an existing stronger compatible policy.

A zero-review baseline is acceptable when the safety objective is specifically to force PR/MR transport rather than to establish independent Human approval. Projects may require stronger review policy separately.

`Restrict updates`-style rules that would block normal PR/MR merges are not part of the portable baseline unless the project intentionally supplies a compatible bypass/merge architecture.

## Bootstrap gate

The Consumer Governance bootstrap must inspect the repository's branch/PR capability surface before normal writable automation.

Read-only discovery and coexistence inspection may occur before protection exists. However, Agent Governance MUST NOT treat a repository as writable-ready for normal automated development until the protection invariant is verified or an explicit Human risk disposition authorizes an alternative because the provider lacks an equivalent control.

When the current agent/connector cannot administer repository rules:

1. report `REQUIRE_HUMAN` with the exact missing protection;
2. provide the applicable runbook/provider steps;
3. wait for the Human/repository administrator to apply the control;
4. verify the resulting effective state through a supported read surface;
5. only then clear the writable-ready gate.

The inability of an agent to configure the rule is not permission to continue unprotected.

## Existing repositories

Bootstrap MUST detect and classify existing project-native branch controls before adding anything.

- compatible stronger protection -> `REUSE`;
- compatible protection needing a bounded adjustment -> `ADAPT`;
- missing protection -> require the minimum control;
- conflicting/bypass-heavy protection that does not satisfy the invariant -> `CONFLICT`/Human resolution;
- provider with no equivalent technical mechanism -> explicit alternative-control/risk decision before writable automation.

Do not overwrite or weaken repository-native protection merely to match the example GitHub configuration.

## Long-lived branch discovery

Do not assume every repository uses `main` + `develop`.

Identify from repository/provider truth:

- default/stable branch;
- integration/development branch when one exists;
- authorized release/hotfix long-lived branches when the project's workflow treats them as protected targets.

Topic branches are normally excluded from this baseline because they must remain writable by their owning work unit.

## Durable safety receipt

The effective protection MUST be reconstructible without chat history.

The durable receipt/ledger entry should contain at least:

```text
control_id
repository
provider
state
verified_at
long_lived_targets
provider_control_id/name
required_pr_or_mr_transport
restrict_deletions
block_force_or_non_fast_forward
routine_agent_bypass
stronger_project_specific_rules
verification_surface
owner/disposition
```

This source repository uses `docs/REPOSITORY-SAFETY-CONTROLS-LEDGER.md` as its canonical ledger. Consumer projects may reuse an existing project-native security/operations ledger; Agent Governance must not invent a competing authority path merely for naming consistency.

## Verification rule

Configuration screenshots or operator statements are useful setup evidence but do not by themselves close the gate when a supported provider read surface can show the effective configuration.

Prefer effective-state verification from the repository provider/API and confirm:

- enforcement is active;
- exact branch targets are covered;
- required rules are present;
- bypass actors do not include the normal agentic write identity.

Do not perform a destructive direct-write test against `main`, `develop`, or another protected long-lived branch merely to prove rejection when configuration state is directly observable.

## Revalidation triggers

Revalidate the control when any of the following changes materially:

- repository provider or organization ownership;
- default/integration branch topology;
- ruleset/branch-protection configuration;
- agent app/connector identity or permissions;
- bypass list;
- repository administration model;
- a direct-write incident or unexpected long-lived-branch movement.

## Relationship to D061

D061 protects ChatGPT Orchestrator authoring in this source repository through a fail-closed topic-branch target gate.

D062 adds the independent server-side layer and generalizes the requirement to future governed repositories:

```text
process guard prevents the unsafe request
+
provider guard rejects the unsafe request if process guard fails
```

Neither layer substitutes for the other when both are available.

## Provider adapter

`docs/LONG-LIVED-BRANCH-PROTECTION-RUNBOOK.md` carries the current GitHub procedure and the semantic mapping required for other providers.

Provider-specific UI labels, API schemas and commands are operational adapter details, not Governance Core semantics.

## Effective rule

```text
provider supports enforceable long-lived-branch protection
AND normal agentic writable work is planned
AND protection is missing/unverified
=> writable readiness is BLOCKED / REQUIRE_HUMAN as applicable.
```
