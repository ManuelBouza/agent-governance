# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O073
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B is closed. Protocol `1.13.0` is active and L001 is `VERIFIED`.

T014 Consumer Governance deterministic package/tooling foundation is accepted, integrated and cleaned up.

T015 Consumer Governance trigger/eval corpus is accepted, integrated and cleaned up. The accepted deterministic corpus contains 36 fixed cases with balanced train/validation positive/negative/near-miss partitions, Consumer-vs-Maintainer separation, synthetic coexistence coverage, source independence and fail-closed grading. Runtime model activation accuracy is not claimed.

T016 Consumer Skill final-authoring test transition is accepted, integrated and cleaned up. The obsolete pre-authoring assertion that `governance-skill/SKILL.md` must be absent is retired while permanent source-checkout isolation for `.agent-governance/` and `.agent-coordination/` remains enforced.

Final `governance-skill/SKILL.md` is integrated. Focused release review `CONSUMER-GOVERNANCE-SKILL-V1-R1` remains the last recorded release decision and is BLOCKED on the missing deterministic CLI v1 surfaces.

T017 is independently reviewed and ACCEPTED in `docs/reviews/T017-R1.md`. Remote evidence shows exact base `ddaa256d1bcdc1c101c446e731cafb400b5a99b6`, implementation anchor `ee540cf842d11b74ccfea7873a0f51a5347dffa4`, final executor head `6a6343a78ebce5fb585722840b6d728d9d1fab93`, authorized runtime/test/handoff paths only, and the complete stable seven-command surface: `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, `archive`.

T017 acceptance is not release approval. The implementation and acceptance records must be integrated and OP036 must retire both branches before rerunning the focused Consumer Governance Skill v1 release review against the actual integrated runtime.

Gentle AI and Caveman are ecosystem integrations only: optional and recommended when useful, never dependencies for Agent Governance correctness, bootstrap, validation, execution, verification or release acceptance. Caveman should be treated as an optional Skill when used with Gentle AI rather than as a required proxy/runtime layer.

L002 remains separate and non-blocking.

## OpenCode delegation rule

All delegated OpenCode actions are initiated by the Orchestrator through a persisted Task/Operational Contract and an exact bootstrap prompt. The Human acts only as transport for the prompt/response unless a genuine Human decision or approval is required. Do not ask the Human to perform operational Git/PR/cleanup steps that can be delegated.

The existing narrow external-worktree permission is treated as stable workstation configuration; do not repeat its preflight unless evidence shows it changed or blocks execution.

## Next Action

1. Integrate T017-R1, OP036 and this checkpoint into `develop`.
2. Integrate the exact accepted T017 executor head `6a6343a78ebce5fb585722840b6d728d9d1fab93` into `develop` without rewriting the executor branch.
3. Execute OP036 and independently verify remote branches return to `develop`, `main`.
4. Rerun the focused Consumer Governance Skill v1 release review against the final Skill, accepted trigger corpus, package/functional/release contracts, T014-T017 accepted reviews and the actual integrated seven-command runtime.
5. Transition release status only if every deterministic v1 release-gate invariant closes without unresolved blockers.
6. After the Consumer release decision, formalize Gentle AI and Caveman as optional/recommended ecosystem coexistence guidance without introducing either as a required dependency.

## Next Chat Minimum Load

After normal bootstrap:
- while T017 integration/cleanup is pending, load `docs/reviews/T017-R1.md`, `handoffs/T017-executor-handoff.json` and `docs/operations/OP036-retire-t017-integration-branches.md`;
- for final release review, load `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`, `docs/GOVERNANCE-SKILL-CONTRACT.md`, `docs/GOVERNANCE-SKILL-PACKAGE.md`, accepted T014/T015/T016/T017 reviews, fixed trigger corpus, final `governance-skill/SKILL.md`, current Consumer status and actual `governance-skill/scripts/governance.py` runtime surface;
- for ecosystem guidance, load only the concrete Gentle AI/Caveman coexistence sources needed to document optional/recommended integration; do not make either a product dependency;
- load Maintainer Skill material only on a concrete Consumer-vs-Maintainer conflict.

## Do Not

Do not weaken executor Markdown ownership, ask the Human to perform delegable operational steps, treat deterministic corpus integrity as runtime model accuracy, claim T017 acceptance or final Skill presence alone equals release readiness, create live consumer runtime footprints in this source checkout, install live external SDD/Skills for evals, make Gentle AI or Caveman mandatory, route correctness authority through Caveman, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
