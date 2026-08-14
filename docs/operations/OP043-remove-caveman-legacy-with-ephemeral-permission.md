# OP043 — Remove Caveman legacy integration with ephemeral OpenCode permission

Operation ID: OP043
Status: READY_AFTER_INTEGRATION
Type: host-configuration repair
Repository base: `develop`

## Context

OP039 established the correct optional Caveman Skill architecture and OP041 confirmed the remaining legacy state is limited to two mechanically identified fragments:

- the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json`;
- the mechanically delimited Caveman-owned block in `/home/manuel/.config/opencode/AGENTS.md`.

OP041 returned BLOCKED because the active OpenCode host permission policy denied both edits before any mutation. The approved Caveman `v2.0.0` Skill remains exact, Gentle AI discovery passes, same-name shadowing is absent, `gentle-orchestrator` is preserved and the source repository is unchanged.

## Objective

Complete the exact OP041 cleanup by launching this operation with a process-local OpenCode permission override that authorizes only the minimum external-directory/edit access required for the two already-approved host files. Do not weaken or rewrite persistent OpenCode permission policy.

## Permission model

OpenCode process-local inline configuration may override ordinary global/project permission configuration for the running process. This operation authorizes use of `OPENCODE_CONFIG_CONTENT` only as an ephemeral bootstrap transport for the following effective permissions:

- external-directory access to `/home/manuel/.config/opencode/**` only as required to reach the two target files and existing Caveman Skill/backup paths;
- edit permission only for `/home/manuel/.config/opencode/opencode.json` and `/home/manuel/.config/opencode/AGENTS.md`;
- normal repository permissions remain unchanged.

The override MUST NOT grant blanket edit permission to unrelated external paths. It MUST NOT be persisted into `opencode.json`, agent profiles, `AGENTS.md`, shell startup files, environment files or repository state.

If a higher-priority managed/admin policy still denies either required edit, stop and report BLOCKED. Do not attempt to bypass managed policy.

## Authorized mutations

Exactly the same two mutations authorized by OP041:

1. `/home/manuel/.config/opencode/opencode.json`: remove only the Caveman plugin entry identified by OP039/OP041, preserving valid syntax and all unrelated settings.
2. `/home/manuel/.config/opencode/AGENTS.md`: remove only the mechanically delimited Caveman-owned block identified by OP039/OP041, preserving all unrelated instructions.

No other host mutation is authorized.

## Required sequence

1. Establish current `develop` bootstrap baseline. Do not modify repository content.
2. Confirm the approved Caveman `v2.0.0` Skill remains exact at `/home/manuel/.config/opencode/skills/caveman/SKILL.md`.
3. Confirm Gentle AI read-only discovery still reports `caveman` with user scope and no current-repository same-name shadowing.
4. Confirm both target legacy fragments are still present and mechanically attributable to Caveman.
5. Confirm a usable backup exists; create a new timestamped backup of both target files outside the repository if needed.
6. Remove only the Caveman plugin entry from global `opencode.json`.
7. Remove only the delimited Caveman-owned block from global `AGENTS.md`.
8. Re-read both files and verify unrelated configuration/instructions remain preserved and syntax is valid.
9. Verify Caveman Skill remains exact `v2.0.0`, Gentle discovery remains PASS, no same-name shadowing exists and no Caveman plugin/global-instruction integration remains from these two surfaces.
10. Verify `gentle-orchestrator` remains unchanged.
11. Verify the `agent-governance` repository has no content mutation.
12. Verify the process-local permission override was not persisted anywhere.

## Forbidden

Do not:

- persist broader OpenCode permission changes;
- use `--auto` as a substitute for explicit-deny handling;
- bypass a managed/admin deny;
- modify the Caveman Skill artifact;
- install Caveman Proxy/Engine/Core;
- change provider/base URL settings;
- alter `gentle-orchestrator` or Gentle AI profile/model assignments;
- edit any other host or repository file;
- make Caveman or Gentle AI mandatory or authoritative.

## Acceptance

PASS requires:

- exact Caveman `v2.0.0` Skill remains installed and Gentle-discoverable with user scope;
- same-name project shadowing remains absent;
- Caveman plugin entry is absent from `/home/manuel/.config/opencode/opencode.json`;
- Caveman-owned legacy block is absent from `/home/manuel/.config/opencode/AGENTS.md`;
- unrelated host configuration is preserved;
- `gentle-orchestrator` is preserved;
- repository mutation is NONE;
- ephemeral permission override is not persisted.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP043
SKILL_MATCH: PASS | FAIL | UNKNOWN
GENTLE_DISCOVERY: PASS | FAIL | UNKNOWN
SHADOWING: ABSENT | PRESENT | UNKNOWN
PLUGIN_ENTRY: ABSENT | PRESENT | UNKNOWN
AGENTS_BLOCK: ABSENT | PRESENT | UNKNOWN
GENTLE_ORCHESTRATOR: PRESERVED | CHANGED | UNKNOWN
REPO_MUTATION: NONE | DETECTED | UNKNOWN
EPHEMERAL_PERMISSION: USED_NOT_PERSISTED | DENIED_BY_MANAGED_POLICY | UNKNOWN
BACKUP: <path or UNKNOWN>
REMAINING_ISSUE: <NONE or concise blocker>
```
