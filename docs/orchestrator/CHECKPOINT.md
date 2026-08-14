# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O075
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014 Consumer Governance deterministic package/tooling foundation is accepted, integrated and cleaned up.

T015 Consumer Governance trigger/eval corpus is accepted, integrated and cleaned up. The accepted deterministic corpus contains 36 fixed cases with balanced train/validation positive/negative/near-miss partitions, Consumer-vs-Maintainer separation, synthetic coexistence coverage, source independence and fail-closed grading. Runtime model activation accuracy is not claimed.

T016 Consumer Skill final-authoring test transition is accepted, integrated and cleaned up. Permanent source-checkout isolation for `.agent-governance/` and `.agent-coordination/` remains enforced.

T017 Consumer Governance remaining CLI v1 surfaces is accepted, integrated and cleaned up. The stable deterministic runtime surface is exactly `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, and `archive`.

Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R2` is ACCEPTED / RELEASE-APPROVED. Consumer Governance Skill v1 is release-approved. Release approval remains bounded to deterministic evidence and does not claim runtime model activation accuracy.

OP037 is completed and independently verified; remote branches returned to exactly `develop`, `main`.

Optional ecosystem guidance is authored in `docs/OPTIONAL-ECOSYSTEM-INTEGRATIONS.md`. Gentle AI and Caveman are explicitly optional and recommended when useful, never dependencies or authority sources. Gentle AI may remain the selected orchestration layer in projects that already use it. When Caveman is used with Gentle AI, prefer Caveman as an optional discovered Skill rather than a required proxy/runtime layer. Agent Governance correctness, bootstrap, validation, execution, verification and release acceptance remain independent of both.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required. Do not ask the Human to perform operational Git/PR/cleanup steps that can be delegated.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate the ChatGPT-owned optional ecosystem guidance Markdown branch into `develop`.
2. Execute OP038 and independently verify remote branches return to `develop`, `main`.
3. Keep Gentle AI and Caveman recommendations explicitly optional; do not add runtime/package dependencies or authority semantics for either.
4. After ecosystem-guidance cleanup, select the next product frontier from current repository state; do not promote `develop` to `main` or publish/tag a release without the repository's authorized release workflow.

## Next Chat Minimum Load

After normal bootstrap:
- while ecosystem-guidance integration/cleanup is pending, load `docs/OPTIONAL-ECOSYSTEM-INTEGRATIONS.md` and `docs/operations/OP038-retire-optional-ecosystem-guidance-branch.md`;
- load current release/status records only if a concrete release/promotion question arises;
- load Maintainer Skill material only on a concrete Consumer-vs-Maintainer conflict.

## Do Not

Do not weaken executor Markdown ownership, ask the Human to perform delegable operational steps, treat deterministic corpus integrity as runtime model accuracy, create live consumer runtime footprints in this source checkout, install live external SDD/Skills for evals, make Gentle AI or Caveman mandatory, route correctness authority through Caveman, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
