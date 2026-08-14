# OP046 — Complete Caveman cleanup

Operation ID: OP046
Status: READY_AFTER_INTEGRATION
Type: host-configuration repair
Repository base: `develop`

## Context

OP044 established that the remaining edit denial is USER_CONTROLLED and originates from the project OpenCode configuration. The Human Owner explicitly approved a narrow, process-local permission exception for this cleanup only.

The approved Caveman v2.0.0 Skill is already correct and Gentle AI discovery passes. Two legacy Caveman host fragments remain:

- the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json`;
- the mechanically delimited Caveman block in `/home/manuel/.config/opencode/AGENTS.md`.

## Objective

Remove only those two legacy fragments while preserving the Caveman Skill, Gentle AI, `gentle-orchestrator`, all unrelated host configuration, persistent OpenCode permission policy, and repository state.

## Authorization

The Human Owner authorizes a temporary process-local OpenCode permission exception limited to the two target host files above. The exception must not be written to project/global configuration or persisted after the process ends.

No other host mutation is authorized.

## Required result

- Caveman v2.0.0 Skill remains exact and Gentle-discoverable with user scope.
- No same-name project Skill shadows it.
- Caveman plugin entry is absent from global `opencode.json`.
- Caveman-owned block is absent from global `AGENTS.md`.
- `gentle-orchestrator` is preserved.
- persistent project/global permission policy is unchanged.
- repository mutation is NONE.
- temporary permission exception is not persisted.

If the narrow temporary permission cannot authorize both exact edits, return BLOCKED without broadening permissions.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP046
SKILL_MATCH: PASS | FAIL | UNKNOWN
GENTLE_DISCOVERY: PASS | FAIL | UNKNOWN
SHADOWING: ABSENT | PRESENT | UNKNOWN
PLUGIN_ENTRY: ABSENT | PRESENT | UNKNOWN
AGENTS_BLOCK: ABSENT | PRESENT | UNKNOWN
GENTLE_ORCHESTRATOR: PRESERVED | CHANGED | UNKNOWN
PERSISTENT_POLICY: PRESERVED | CHANGED | UNKNOWN
REPO_MUTATION: NONE | DETECTED | UNKNOWN
EPHEMERAL_PERMISSION: USED_NOT_PERSISTED | DENIED | UNKNOWN
BACKUP: <path or UNKNOWN>
REMAINING_ISSUE: <NONE or concise blocker>
```
