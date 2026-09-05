# Repository Branch Protection Bootstrap

Purpose: portable Consumer Governance bootstrap guidance for making long-lived repository branches server-side protected before normal agentic writable work.

This asset is operational guidance. Project-native repository/security policy remains authoritative when it is compatible or stronger.

## Writable-readiness invariant

Before normal governed writable automation:

1. discover the repository provider;
2. identify the actual default/stable and integration branches;
3. inspect existing provider-side branch protections/rulesets;
4. preserve stronger compatible project controls;
5. establish any missing minimum protection through an authorized repository administrator;
6. verify the effective provider-side state;
7. record a durable project receipt;
8. only then mark the repository writable-ready.

Minimum semantics:

```text
PR/MR required for normal long-lived-branch changes
deletions restricted
force/non-fast-forward updates blocked
normal agent/app/connector has no routine bypass
protection active/enforced
```

Read-only discovery may occur before this gate closes. Missing administration capability is `REQUIRE_HUMAN`, not permission to continue unprotected.

## GitHub baseline

UI path:

```text
Repository Settings
-> Rules
-> Rulesets
-> New ruleset
-> New branch ruleset
```

Recommended baseline:

```text
Name: Protect long-lived branches
Enforcement: Active
Bypass list: no normal agentic writer
Targets: actual long-lived branches
Rules:
  Restrict deletions
  Require a pull request before merging
    Required approvals: 0  # minimum transport guard; project may require more
  Block force pushes
```

Do not enable `Restrict updates` as a generic baseline unless the repository intentionally has a compatible merge/bypass architecture.

Do not weaken existing required status checks, reviews, signatures, scans, deployments or other stronger project-native controls.

## GitHub verification

Read back the effective ruleset and verify:

```text
enforcement == active
intended refs are included
pull_request rule present
deletion rule present
non_fast_forward rule present
normal agentic writer absent from bypass actors
```

Do not deliberately mutate/delete/force-push a protected long-lived branch just to demonstrate rejection when effective configuration is directly observable.

## Other providers

Map semantics rather than GitHub labels. For GitLab, Bitbucket, Azure DevOps or another provider, determine:

```text
which server-side protected-branch mechanism applies
whether normal changes require MR/PR flow
whether force/direct updates remain possible
whether deletion is restricted
which users/apps/tokens can bypass
how effective configuration is verified
```

If equivalent protection is unavailable, stop writable readiness and require an explicit Human alternative-control/risk decision.

## Durable receipt

Reuse an existing compatible project security/operations/governance ledger where possible. Record at least:

```text
repository
provider
verified_at
long-lived targets
provider control id/name
enforcement state
PR/MR requirement
deletion restriction
force/non-fast-forward block
agent bypass state
verification surface
owner/disposition
```

Do not copy the source product's control IDs or GitHub ruleset ID into another project.

## Revalidate when

- provider/organization changes;
- default or integration branch changes;
- protection/ruleset changes;
- agent/app/connector identity changes;
- bypass lists change;
- an unexpected direct update succeeds.
