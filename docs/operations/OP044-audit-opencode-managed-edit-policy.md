# OP044 — Audit OpenCode managed edit policy

Operation ID: OP044
Status: READY_AFTER_INTEGRATION
Type: host-policy audit
Repository base: `develop`

## Context

OP043 returned BLOCKED after a process-local permission override still could not edit the two authorized legacy Caveman host surfaces. The returned state was:

- Caveman `v2.0.0` Skill exact: PASS;
- Gentle AI discovery: PASS;
- same-name shadowing: ABSENT;
- Caveman plugin entry: PRESENT;
- Caveman global AGENTS block: PRESENT;
- `gentle-orchestrator`: PRESERVED;
- repository mutation: NONE;
- ephemeral override: DENIED_BY_MANAGED_POLICY.

This establishes that the remaining blocker is a higher-priority managed OpenCode policy, not Caveman artifact identity, Gentle AI discovery, shadowing, repository state, or ordinary process-local permission configuration.

## Objective

Identify, read-only, the exact effective managed/admin policy source that denies edits to:

- `/home/manuel/.config/opencode/opencode.json`;
- `/home/manuel/.config/opencode/AGENTS.md`.

Determine whether that policy is user-controlled, organization/administrator-controlled, or otherwise externally managed, and report the minimum legitimate authority/action required to permit the already-authorized OP041 cleanup.

This operation does not authorize changing, disabling, bypassing, replacing, or persisting any permission policy.

## Required sequence

1. Establish the current `develop` bootstrap baseline required by repository policy. Do not modify repository content.
2. Confirm the OP043 returned state remains materially unchanged: approved Caveman Skill exact, Gentle discovery PASS, no same-name shadowing, both legacy fragments still present, `gentle-orchestrator` preserved.
3. Inspect OpenCode's effective configuration/policy provenance using read-only mechanisms available on the host. Prefer OpenCode-native diagnostic/config inspection when available.
4. Identify the rule that resolves the `edit` action for each of the two target host files to `deny`.
5. Identify the policy source with as much deterministic precision as the host exposes, including file/path/source/tier/profile/managed provider or equivalent provenance.
6. Classify control of the blocking policy as exactly one of:
   - `USER_CONTROLLED` — the Human Owner can legitimately change the policy in their own host configuration;
   - `ADMIN_CONTROLLED` — an organization/system administrator or managed policy authority controls it;
   - `UNKNOWN_CONTROL` — provenance/control cannot be established safely.
7. Determine the minimum legitimate next action needed to allow the two already-authorized edits. Do not execute that action.
8. Verify no host or repository file was modified by this audit.

## Boundaries

Read-only only. Do not:

- edit any OpenCode configuration or policy file;
- change managed/admin policy;
- launch another bypass/override attempt;
- use `--auto` to defeat explicit deny;
- edit the Caveman Skill, `opencode.json`, global `AGENTS.md`, Gentle AI profiles, or `gentle-orchestrator`;
- install or remove plugins;
- mutate repository content;
- expose secrets or credentials in the completion response.

If the policy provenance cannot be safely determined without mutation or privileged access, return BLOCKED with `POLICY_CONTROL: UNKNOWN_CONTROL`.

## Acceptance

PASS requires:

- blocking policy provenance is identified deterministically enough to explain both denied edits;
- policy control is classified;
- minimum legitimate next action is identified without executing it;
- Caveman/Gentle/repository state remains unchanged;
- no host mutation occurs.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP044
POLICY_CONTROL: USER_CONTROLLED | ADMIN_CONTROLLED | UNKNOWN_CONTROL
POLICY_SOURCE: <concise non-secret source/path/tier or UNKNOWN>
TARGET_RULE: <concise rule identity/effect or UNKNOWN>
SKILL_MATCH: PASS | FAIL | UNKNOWN
GENTLE_DISCOVERY: PASS | FAIL | UNKNOWN
PLUGIN_ENTRY: PRESENT | ABSENT | UNKNOWN
AGENTS_BLOCK: PRESENT | ABSENT | UNKNOWN
GENTLE_ORCHESTRATOR: PRESERVED | CHANGED | UNKNOWN
HOST_MUTATION: NONE | DETECTED | UNKNOWN
REPO_MUTATION: NONE | DETECTED | UNKNOWN
NEXT_AUTHORITY_ACTION: <concise legitimate action or UNKNOWN>
REMAINING_ISSUE: <NONE or concise blocker>
```
