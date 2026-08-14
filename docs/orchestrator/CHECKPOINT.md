# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O070
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014 Consumer Governance deterministic package/tooling foundation is accepted, integrated and cleaned up.

T015 Consumer Governance trigger/eval corpus is accepted, integrated and cleaned up. The accepted deterministic corpus contains 36 fixed cases with balanced train/validation positive/negative/near-miss partitions, Consumer-vs-Maintainer separation, synthetic coexistence coverage, source independence and fail-closed grading. Runtime model activation accuracy is not claimed.

The Consumer Governance Skill remains `DESIGN-APPROVED / NOT YET RELEASED`. The release gate now permits ChatGPT-owned final `governance-skill/SKILL.md` authoring, but the accepted T015 test suite still contains a sequencing assertion that the final file must not exist. That assertion was valid before T015 acceptance and is now transitional rather than a permanent product invariant.

T016 is the narrow executable test-maintenance transition that removes only that obsolete pre-authoring absence assertion while preserving permanent source-checkout isolation for `.agent-governance/` and `.agent-coordination/`. T016 does not authorize final Skill content, runtime changes, corpus changes or release.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required. Do not ask the Human to perform operational Git/PR/cleanup steps that can be delegated.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate T016 planning Markdown and retire its planning branch through a persisted cleanup operation.
2. Launch T016 from current `develop` and independently review its exact test-only diff/handoff.
3. Accept and integrate T016 only if it removes the obsolete `SKILL.md` absence guard without weakening permanent source-footprint isolation or other T015 guarantees.
4. Author final `governance-skill/SKILL.md` on a fresh ChatGPT-owned Markdown branch using the accepted package/tooling, functional contract and fixed trigger corpus.
5. Perform a focused Consumer Governance Skill v1 release review. That review must fail closed on any mismatch between final Skill routing, actually implemented CLI/runtime surfaces, accepted trigger boundaries and release contracts; model/provider output is never release authority.

## Next Chat Minimum Load

After normal bootstrap:
- while T016 is pending, load T016 and its exact executor handoff/diff;
- before final Skill authoring, load `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`, `docs/GOVERNANCE-SKILL-CONTRACT.md`, `docs/GOVERNANCE-SKILL-PACKAGE.md`, accepted T014/T015 review records and the fixed T015 corpus;
- during release review, inspect the final `governance-skill/SKILL.md`, actual `governance-skill/scripts/governance.py` command surface and focused deterministic tests/evals;
- load Maintainer Skill material only on a concrete Consumer-vs-Maintainer conflict.

## Do Not

Do not weaken executor Markdown ownership, ask the Human to perform delegable operational steps, treat T015 corpus integrity as runtime model accuracy, integrate a final Skill that routes to nonexistent mandatory runtime capabilities without recording the release blocker, create live consumer runtime footprints in this source checkout, install live external SDD/Skills for evals, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
