# OP041 — Remove legacy Caveman host integration

Operation ID: OP041
Status: READY_AFTER_INTEGRATION
Type: host-configuration repair
Repository base: `develop`

## Context

OP039 verified the approved Caveman `v2.0.0` Skill at `/home/manuel/.config/opencode/skills/caveman/SKILL.md`, Gentle AI discovery PASS, no same-name shadowing, `gentle-orchestrator` preserved, and no repository mutation. OP039 returned PARTIAL only because host policy denied mutation of two already-identified legacy Caveman surfaces:

- a Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json`;
- a mechanically delimited Caveman-owned block in `/home/manuel/.config/opencode/AGENTS.md`.

The OP039 backup is `/home/manuel/.config/opencode/backups/op039-caveman-20260814T185334Z`.

## Objective

Remove only those two legacy Caveman integration surfaces so Caveman remains available solely as the optional user-scoped Skill discovered by Gentle AI, while preserving all unrelated OpenCode/Gentle AI configuration and `gentle-orchestrator` behavior.

## Authorization

This Operational Contract explicitly authorizes host-level edits to the following existing files only:

- `/home/manuel/.config/opencode/opencode.json`: remove only the Caveman plugin entry identified by OP039;
- `/home/manuel/.config/opencode/AGENTS.md`: remove only the mechanically delimited Caveman-owned block identified by OP039.

No other host mutation is authorized.

Before mutation, independently confirm that each target fragment is mechanically attributable to Caveman and that removal can preserve all unrelated bytes/semantics. If either fragment is not unambiguous at execution time, do not guess; return PARTIAL with the exact unresolved surface.

## Required sequence

1. Establish the current `develop` bootstrap baseline required by repository policy. Do not modify repository content.
2. Confirm the OP039-approved Skill remains present and exact at `/home/manuel/.config/opencode/skills/caveman/SKILL.md`.
3. Inspect the two authorized legacy surfaces and confirm they match the OP039 findings.
4. Preserve the current versions of both host files in a timestamped backup outside the repository before editing, unless the OP039 backup already contains byte-identical pre-edit copies; in either case report the backup path used.
5. Remove only the Caveman plugin entry from `/home/manuel/.config/opencode/opencode.json`, preserving valid syntax and every unrelated setting.
6. Remove only the mechanically delimited Caveman-owned block from `/home/manuel/.config/opencode/AGENTS.md`, preserving every unrelated instruction byte-for-byte where practical.
7. Verify no Caveman proxy/wrapper/plugin/provider-routing requirement remains active from these two surfaces.
8. Verify Gentle AI read-only discovery still reports `caveman` as a user-scoped Skill at `/home/manuel/.config/opencode/skills/caveman/SKILL.md` and no project-scoped same-name Skill shadows it.
9. Verify `gentle-orchestrator` remains unchanged and effective OpenCode/Gentle AI configuration remains usable.
10. Verify the `agent-governance` repository has no content mutation from this operation.

## Forbidden

Do not:

- modify the Caveman Skill artifact itself;
- install Caveman Proxy/Engine/Core;
- change provider endpoints/base URLs;
- alter `gentle-orchestrator`, its model/profile assignments, or Gentle AI orchestration semantics;
- change unrelated OpenCode plugins/settings/instructions;
- edit any repository file;
- remove ambiguous host state;
- make Caveman or Gentle AI mandatory or authoritative.

## Acceptance

PASS requires:

- Caveman Skill remains exact `v2.0.0` and Gentle-discoverable with user scope;
- no same-name project shadowing;
- the identified Caveman plugin entry is absent from `opencode.json`;
- the identified Caveman-owned block is absent from global `AGENTS.md`;
- unrelated host configuration is preserved;
- `gentle-orchestrator` remains preserved;
- no repository mutation occurs.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP041
SKILL_MATCH: PASS | FAIL | UNKNOWN
GENTLE_DISCOVERY: PASS | FAIL | UNKNOWN
SHADOWING: ABSENT | PRESENT | UNKNOWN
PLUGIN_ENTRY: ABSENT | PRESENT | UNKNOWN
AGENTS_BLOCK: ABSENT | PRESENT | UNKNOWN
GENTLE_ORCHESTRATOR: PRESERVED | CHANGED | UNKNOWN
REPO_MUTATION: NONE | DETECTED | UNKNOWN
BACKUP: <path or UNKNOWN>
REMAINING_ISSUE: <NONE or concise blocker>
```
