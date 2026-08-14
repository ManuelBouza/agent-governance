# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O078
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014-T017 Consumer Governance v1 implementation/eval sequence is accepted, integrated and cleaned up. Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R2` is ACCEPTED / RELEASE-APPROVED. Consumer Governance Skill v1 is release-approved.

Optional ecosystem guidance is integrated. Gentle AI and Caveman are optional/recommended only, never dependencies or authority sources. Caveman is preferred as a discovered Skill when Gentle AI is already the selected orchestration layer.

OP039 established the approved Caveman `v2.0.0` user Skill, Gentle discovery PASS, no same-name shadowing, preserved `gentle-orchestrator`, and no repository mutation. OP041 then confirmed that only two legacy Caveman host fragments remain: the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json` and the delimited Caveman block in `/home/manuel/.config/opencode/AGENTS.md`.

OP043 attempted the same bounded cleanup with a process-local permission override and returned BLOCKED with `EPHEMERAL_PERMISSION: DENIED_BY_MANAGED_POLICY`. No partial mutation occurred. This establishes a higher-priority managed/admin edit policy as the only remaining blocker.

OP044 is the read-only successor. It must identify the exact effective policy provenance/rule denying edits to those two files, classify control as USER_CONTROLLED / ADMIN_CONTROLLED / UNKNOWN_CONTROL, and report the minimum legitimate authority action without changing policy or host state. OP045 retires the OP044 contract branch after integration.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate OP044/OP045 and this checkpoint into `develop`.
2. Execute OP045 and independently verify the remote returns to `develop`, `main`.
3. Execute OP044 through OpenCode and review the exact read-only policy-provenance response.
4. If `POLICY_CONTROL: USER_CONTROLLED`, request only the exact Human authority decision needed to alter that policy, then persist a bounded successor operation before mutation.
5. If `POLICY_CONTROL: ADMIN_CONTROLLED`, stop automated cleanup and report the exact administrator-controlled blocker; do not attempt bypasses.
6. If `UNKNOWN_CONTROL`, resolve only policy provenance; do not broaden Caveman/product/repository scope.

## Next Chat Minimum Load

After normal bootstrap:
- while OP044 integration/cleanup is pending, load `docs/operations/OP044-audit-opencode-managed-edit-policy.md` and `docs/operations/OP045-retire-op044-contract-branch.md`;
- for OP044 completion review, load only OP044 plus the returned host-policy evidence;
- load release/status records only for a concrete release/promotion question.

## Do Not

Do not bypass managed/admin policy, make Gentle AI or Caveman mandatory, modify `gentle-orchestrator` for Caveman, install Caveman Proxy/Engine/Core as a requirement, change provider endpoints, mutate host policy during OP044, mutate the source repository during host audit, expose secrets, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
