# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O081
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014-T017 Consumer Governance v1 implementation/eval sequence is accepted, integrated and cleaned up. Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R2` is ACCEPTED / RELEASE-APPROVED. Consumer Governance Skill v1 is release-approved.

Optional ecosystem guidance is integrated. Gentle AI and Caveman are optional/recommended only, never dependencies or authority sources. Caveman is preferred as a discovered Skill when Gentle AI is already the selected orchestration layer.

OP039 established the approved Caveman `v2.0.0` user Skill, Gentle discovery PASS, no same-name shadowing, preserved `gentle-orchestrator`, and no repository mutation. OP041/OP043 established that two legacy Caveman host fragments remain: the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json` and the delimited Caveman block in `/home/manuel/.config/opencode/AGENTS.md`.

OP044 completed read-only policy provenance and classified the blocking edit policy as `USER_CONTROLLED`. The Human Owner authorized a narrow ephemeral cleanup attempt through OP046. OP046 returned BLOCKED because OpenCode denied both exact process-local edit exceptions. The returned state still showed Caveman Skill match PASS, Gentle discovery PASS, no shadowing, `gentle-orchestrator` preserved, persistent policy preserved, repository mutation NONE, and both legacy fragments still present.

The Human Owner then explicitly accepted retaining those two legacy fragments rather than continuing permission work solely to remove them. `docs/CAVEMAN-HOST-STATE.md` records the resulting accepted host state. OP046 is therefore closed as BLOCKED / NOT REQUIRED FOR CURRENT ACCEPTANCE and must not be retried absent concrete evidence of a real host conflict.

Operational Contract completion responses now include the required short `DESCRIPTION` field defined by `docs/OPERATIONAL-CONTRACTS.md`. OP048 is completed and independently verified; remote branches returned to exactly `develop`, `main`.

OP049 retires the Markdown branch that records the accepted Caveman host state after integration.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required.

Operational Contract completion responses MUST follow `docs/OPERATIONAL-CONTRACTS.md`, including a concise human-readable `DESCRIPTION` field.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate `docs/CAVEMAN-HOST-STATE.md`, OP049, and this checkpoint into `develop`.
2. Execute OP049 and independently verify remote branches return to exactly `develop`, `main`.
3. Treat the Caveman/Gentle host configuration line as closed. Do not retry OP046 or alter permissions solely to remove the retained legacy fragments.
4. Reopen this line only if concrete evidence shows duplicate Caveman activation, unintended runtime/provider routing, Gentle interference, `gentle-orchestrator` modification, or another material host conflict caused by a retained fragment.
5. Continue from the next product-maintenance priority selected by the Human Owner or the durable repository frontier.

## Next Chat Minimum Load

After normal bootstrap:
- while the host-state Markdown integration/cleanup is pending, load `docs/CAVEMAN-HOST-STATE.md` and `docs/operations/OP049-retire-caveman-host-state-branch.md`;
- after OP049 is complete, no Caveman/Gentle host history needs to be loaded unless a concrete host conflict or ecosystem integration question requires it;
- load release/status records only for a concrete release/promotion question.

## Do Not

Do not retry OP046 absent new material host-conflict evidence, broaden or persist host edit permissions merely to remove accepted legacy fragments, omit the Operational Contract `DESCRIPTION` field in newly authored completion shapes, make Gentle AI or Caveman mandatory, modify `gentle-orchestrator` for Caveman, install Caveman Proxy/Engine/Core as a requirement, change provider endpoints, expose secrets, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
