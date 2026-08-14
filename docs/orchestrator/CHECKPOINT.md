# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O077
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014-T017 Consumer Governance v1 implementation/eval sequence is accepted, integrated and cleaned up. Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R2` is ACCEPTED / RELEASE-APPROVED. Consumer Governance Skill v1 is release-approved.

Optional ecosystem guidance is integrated. Gentle AI and Caveman are optional/recommended only, never dependencies or authority sources. Caveman is preferred as a discovered Skill when Gentle AI is already the selected orchestration layer.

OP039 host audit returned PARTIAL. Verified host state: exact Caveman `v2.0.0` Skill at `/home/manuel/.config/opencode/skills/caveman/SKILL.md`; Gentle AI discovery PASS; same-name shadowing absent; `gentle-orchestrator` preserved; repository mutation none. Backup: `/home/manuel/.config/opencode/backups/op039-caveman-20260814T185334Z`.

The only remaining OP039 issue is legacy Caveman integration in two mechanically identified host surfaces: a Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json` and a delimited Caveman-owned block in `/home/manuel/.config/opencode/AGENTS.md`. OP039 could not remove them because host policy denied those edits.

OP041 is the bounded successor explicitly authorizing removal of only those two legacy Caveman fragments while preserving unrelated configuration, the approved Skill, Gentle AI behavior, and `gentle-orchestrator`. OP042 retires the OP041 contract branch after integration.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate OP041/OP042 and this checkpoint into `develop`.
2. Execute OP042 and independently verify remote branches return to `develop`, `main`.
3. Execute OP041 through OpenCode and review the exact completion response.
4. If OP041 is DONE, Caveman host configuration is closed: optional `v2.0.0` user Skill, Gentle-discoverable, no legacy plugin/AGENTS integration.
5. If OP041 remains PARTIAL/BLOCKED, resolve only the exact reported host-policy conflict; do not broaden product/repository scope.

## Next Chat Minimum Load

After normal bootstrap:
- while OP041 integration/cleanup is pending, load `docs/operations/OP041-remove-legacy-caveman-host-integration.md` and `docs/operations/OP042-retire-op041-contract-branch.md`;
- for OP041 completion review, load only OP041 plus the returned host evidence;
- load release/status records only for a concrete release/promotion question.

## Do Not

Do not make Gentle AI or Caveman mandatory, modify `gentle-orchestrator` for Caveman, install Caveman Proxy/Engine/Core as a requirement, change provider endpoints, mutate the source repository during host repair, delete ambiguous host state, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
