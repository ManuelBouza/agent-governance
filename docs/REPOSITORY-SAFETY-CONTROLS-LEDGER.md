# Repository Safety Controls Ledger

Status: CURRENT  
Owner: Human Owner / ChatGPT Orchestrator  
Controlling decision: `docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md`  
Runbook: `docs/LONG-LIVED-BRANCH-PROTECTION-RUNBOOK.md`

## Purpose

Record effective repository-level safety controls that materially constrain agentic writes and that cannot be reconstructed reliably from task/chat history alone.

This ledger records provider-effective controls and their verification state. It does not replace provider configuration, branching policy, Task Contracts, or project-native security authority.

## State model

`Control-State`:

- `ACTIVE` — effective and verified;
- `DEGRADED` — expected control exists but a required property is missing/unverified;
- `RETIRED` — intentionally superseded or no longer applicable.

A ledger entry MUST distinguish desired policy from verified effective state.

## Required fields

Each material control entry records at least:

```text
Control-ID
Control-State
Repository
Provider
Verified-At
Control-Type
Provider-Control-ID
Provider-Control-Name
Targets
Required-Semantics
Bypass-State
Verification-Surface
Decision-Ref
Runbook-Ref
Notes / disposition
```

## RSC001 — long-lived branch protection

```text
Control-ID: RSC001
Control-State: ACTIVE
Repository: ManuelBouza/agent-governance
Provider: GitHub
Verified-At: 2026-09-05
Control-Type: long-lived branch protection / PR-only transport baseline
Provider-Control-ID: 22339910
Provider-Control-Name: Protect long-lived branches
Targets:
  - refs/heads/main
  - refs/heads/develop
Required-Semantics:
  pull/merge request required: true
  required approving reviews: 0
  deletion restriction: true
  force/non-fast-forward block: true
  enforcement active: true
Bypass-State:
  bypass actors: none
  connected actor can bypass: never
Allowed-Merge-Methods:
  - merge
  - squash
  - rebase
Verification-Surface:
  - GitHub repository rulesets collection
  - GitHub repository ruleset 22339910
  - branch endpoint corroboration (`protected: true` for develop)
Decision-Ref:
  - docs/decisions/D061-orchestrator-branch-target-write-guard.md
  - docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md
Runbook-Ref:
  - docs/LONG-LIVED-BRANCH-PROTECTION-RUNBOOK.md
Disposition:
  hard server-side guard now rejects routine direct long-lived-branch updates by normal connected actors; D061 remains independently required as the Orchestrator-side pre-write guard.
```

## Incident lineage motivating RSC001

The following source-product Orchestrator authoring incidents demonstrated that a prose-only prohibition was insufficient while `develop` accepted direct API writes:

```text
2a2f34baa5e90724c46555c876aabe68309a8b99  R012 placeholder
59c44d88e202c24928fd4908470bd91099703023  R013 placeholder
7a116b92c706801c9259ce152096609adb465563  D061 placeholder
```

These commits remain in history. They are not rewritten away. D061 corrected the process-layer targeting rule; RSC001 records the independent provider-side enforcement established afterward.

## Verification evidence — 2026-09-05

Effective GitHub state was read back after Human configuration and showed:

```text
ruleset name: Protect long-lived branches
enforcement: active
include:
  refs/heads/main
  refs/heads/develop
rules:
  deletion
  non_fast_forward
  pull_request
pull_request.required_approving_review_count: 0
pull_request.require_extra_approval_for_unattributed_changes: false
pull_request.allowed_merge_methods:
  merge
  squash
  rebase
bypass_actors: []
current_user_can_bypass: never
```

The repository `develop` branch subsequently reports `protected: true`, corroborating that an active ruleset applies. Detailed rule semantics remain sourced from the ruleset resource, not the branch boolean.

## Revalidation triggers

RSC001 must be revalidated when:

- ruleset 22339910 is changed, disabled, deleted or replaced;
- `main`/`develop` topology changes;
- repository ownership/provider changes;
- the connected agent/app/connector identity or permissions change;
- bypass actors change;
- an unexpected direct long-lived-branch mutation succeeds;
- D062/runbook minimum semantics change.

## Consumer-project ledger rule

Future adopting repositories must keep an equivalent durable receipt for the protection actually used there.

Agent Governance MUST prefer an existing compatible project-native security/operations/governance ledger rather than introducing a competing record solely to match this filename. The Consumer Governance Skill bootstrap must surface the requirement and fail closed on unverified writable readiness according to D062.

The provider-specific control identifier, targets and verification evidence belong to the adopting repository; this source-product ledger MUST NOT be copied as if RSC001 described another project.
