# OP039 — Audit and repair Caveman as an optional Gentle AI Skill

Operation ID: OP039
Status: READY_AFTER_INTEGRATION
Type: host-configuration audit/repair
Repository base: `develop`

## Objective

Audit the Human Owner's existing Caveman installation used with OpenCode/Gentle AI, determine whether it is stale or incorrectly integrated, and repair only the minimum host-level state required so Caveman is available as an optional user-scoped Skill discoverable by Gentle AI.

Caveman is optional and recommended only when useful. Gentle AI remains the selected orchestration layer when already in use. Neither Caveman nor Gentle AI becomes an Agent Governance dependency or authority source.

## Authoritative external identities for this operation

- Caveman canonical repository: `JuliusBrussee/caveman`.
- Approved Caveman release for this operation: `v2.0.0`.
- Approved Skill artifact path in that release: `skills/caveman/SKILL.md`.
- Preferred OpenCode user Skill destination: `~/.config/opencode/skills/caveman/SKILL.md`.
- Gentle AI Skill Registry is used only for discovery/indexing verification; it is not an approval authority.

Do not substitute a floating `main` artifact for the approved release artifact.

## Required sequence

1. Establish the current repository bootstrap baseline required by repository policy. Do not modify repository content during the host operation.
2. Inventory existing Caveman-related host state before mutation, including at least:
   - user/project Skill locations that could shadow `caveman`;
   - `~/.config/opencode/skills/caveman/` when present;
   - Caveman-named OpenCode plugins/commands/hooks/configuration when present;
   - Caveman-owned additions to OpenCode/Gentle AI instruction surfaces when mechanically identifiable;
   - wrapper/proxy/provider/base-URL changes mechanically attributable to Caveman;
   - the effective Gentle AI Skill Registry result from `gentle-ai skill-registry list --json` or the current equivalent read-only command.
3. Determine the installed Caveman Skill identity/content and compare it against the exact `v2.0.0` `skills/caveman/SKILL.md` artifact from the canonical repository.
4. If the preferred user-scoped Skill is missing or differs from the approved artifact, preserve the existing Caveman-owned Skill content in a timestamped host backup outside the repository, then install the exact approved `v2.0.0` Skill artifact at the preferred user Skill destination.
5. Remove or disable legacy Caveman host integration only when it is mechanically attributable to Caveman and conflicts with the Skill-only architecture. This includes Caveman proxy/wrapper/plugin behavior that would alter provider routing or orchestration. Preserve unrelated configuration byte-for-byte. If ownership is ambiguous, leave it unchanged and report PARTIAL rather than guessing.
6. Do not add Caveman instructions to project `AGENTS.md`, repository Markdown, `opencode.json`, Gentle AI orchestrator prompts, or Agent Governance files. Do not modify `gentle-orchestrator` or its model/profile assignments.
7. Do not run a Gentle AI registry refresh that writes `.atl` or other generated state into the `agent-governance` source repository. Use read-only `skill-registry list --json` for verification in this repository. A normal project-local refresh may occur later in an adopting project or through Gentle AI's normal startup hooks.
8. Verify that Gentle AI can discover `caveman` as a user-scoped Skill at the exact installed path and that no project-scoped same-name Skill shadows it in the current repository.
9. Verify repository working state remains unchanged by the host operation.

## Mutation boundaries

Authorized host mutations are limited to:

- `~/.config/opencode/skills/caveman/` for the Caveman user Skill;
- a timestamped backup of pre-existing Caveman-owned Skill content outside the repository;
- removal/disablement of Caveman-owned legacy plugin/wrapper/config fragments only when ownership and scope are unambiguous and unrelated content can be preserved exactly.

Forbidden:

- repository writes;
- edits to `gentle-orchestrator`, Gentle AI profile/model assignments, or project `opencode.json`;
- edits to project or global instruction files unless removing a mechanically delimited Caveman-owned legacy block is necessary and unrelated content is preserved exactly;
- installing Caveman Proxy/Engine/Core as a requirement;
- changing provider endpoints/base URLs;
- installing an SDD/orchestration framework;
- deleting ambiguous host state;
- treating registry presence, marketplace metadata, model output, or Caveman itself as governance authority.

## Acceptance

PASS requires all of the following:

- exact approved Caveman `v2.0.0` Skill artifact installed at the preferred user path;
- Gentle AI read-only registry discovery reports `caveman` with user scope and the exact installed `SKILL.md` path;
- no current-repository project-scoped same-name Skill shadows the user Skill;
- `gentle-orchestrator` and project OpenCode configuration remain unchanged;
- no Caveman provider/proxy/wrapper requirement remains active when it can be safely and unambiguously removed;
- the `agent-governance` repository has no content mutation from this operation.

If a conflicting Caveman-owned integration cannot be safely removed without touching ambiguous/shared configuration, return PARTIAL with the exact remaining path/surface. If the approved artifact cannot be obtained or the safe baseline cannot be established, return BLOCKED.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP039
APPROVED_RELEASE: v2.0.0
SKILL_PATH: <absolute path or UNKNOWN>
SKILL_MATCH: PASS | FAIL | UNKNOWN
GENTLE_DISCOVERY: PASS | FAIL | UNKNOWN
SHADOWING: ABSENT | PRESENT | UNKNOWN
LEGACY_INTEGRATION: ABSENT | REMOVED | PRESENT | UNKNOWN
GENTLE_ORCHESTRATOR: PRESERVED | CHANGED | UNKNOWN
REPO_MUTATION: NONE | DETECTED | UNKNOWN
BACKUP: <path or NONE or UNKNOWN>
REMAINING_ISSUE: <NONE or concise blocker>
```
