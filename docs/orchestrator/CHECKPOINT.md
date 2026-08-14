# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O079
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014-T017 Consumer Governance v1 implementation/eval sequence is accepted, integrated and cleaned up. Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R2` is ACCEPTED / RELEASE-APPROVED. Consumer Governance Skill v1 is release-approved.

Optional ecosystem guidance is integrated. Gentle AI and Caveman are optional/recommended only, never dependencies or authority sources. Caveman is preferred as a discovered Skill when Gentle AI is already the selected orchestration layer.

OP039 established the approved Caveman `v2.0.0` user Skill, Gentle discovery PASS, no same-name shadowing, preserved `gentle-orchestrator`, and no repository mutation. OP041/OP043 established that only two legacy Caveman host fragments remain: the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json` and the delimited Caveman block in `/home/manuel/.config/opencode/AGENTS.md`.

OP044 completed read-only policy provenance. The blocking policy is `USER_CONTROLLED`, sourced from project `/home/manuel/projects/agent-governance/opencode.json` `permission.edit`, with deny rules affecting `opencode.json` and Markdown files. The Human Owner explicitly authorized the narrow ephemeral permission exception needed to complete only the two previously authorized host edits.

OP046 persists that Human authorization and completes the bounded Caveman legacy cleanup without changing persistent project/global permission policy. OP047 retires the OP046 contract branch after integration.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate OP046/OP047 and this checkpoint into `develop`.
2. Execute OP047 and independently verify remote branches return to `develop`, `main`.
3. Execute OP046 through OpenCode using only the Human-authorized narrow process-local permission exception.
4. If OP046 is DONE, close Caveman host configuration as optional v2.0.0 user Skill, Gentle-discoverable, with no legacy plugin/global-AGENTS integration and unchanged persistent policy.
5. If OP046 remains BLOCKED/PARTIAL, resolve only the exact reported permission/configuration conflict; do not broaden permissions, product dependencies, or repository scope.

## Next Chat Minimum Load

After normal bootstrap:
- while OP046 integration/cleanup is pending, load `docs/operations/OP046-complete-caveman-cleanup.md` and `docs/operations/OP047-retire-op046-contract-branch.md`;
- for OP046 completion review, load only OP046 plus the returned host evidence;
- load release/status records only for a concrete release/promotion question.

## Do Not

Do not persist the temporary permission exception, broaden host edit permissions, make Gentle AI or Caveman mandatory, modify `gentle-orchestrator` for Caveman, install Caveman Proxy/Engine/Core as a requirement, change provider endpoints, mutate repository content during host repair, expose secrets, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
