# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O082
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B remains closed. Protocol `1.13.0` is active and L001 remains `VERIFIED`.

T014-T017 Consumer Governance v1 implementation/eval sequence remains accepted, integrated and cleaned up. Focused review `CONSUMER-GOVERNANCE-SKILL-V1-R2` remains ACCEPTED / RELEASE-APPROVED. The current Consumer Governance Skill v1 is the behavioral and rollback baseline for the new architecture program.

The Caveman/Gentle host configuration line remains closed under the accepted host-state decision. Remote branch cleanup has already returned the canonical remote to `develop`, `main`. Do not reopen that line absent concrete host-conflict evidence.

The Human Owner selected unified Governance Skill architecture/refactor planning as the next product-maintenance priority after reviewing two Deep Research studies. Git state and repository policy were re-read before planning; external research is supporting evidence only.

D044 establishes the target architecture:

- `governance-core/` remains the single normative authority;
- one shared deterministic engine becomes the single runtime implementation;
- one canonical Governance Skill source uses mutually exclusive `consumer` and `source-maintainer` profiles;
- distribution artifacts are generated and self-contained;
- platform wrappers or thin multiple entrypoints may be generated when packaging or measured activation quality requires them, without creating a second maintained product;
- source-maintainer initially uses adapters over existing source-maintenance state/policy;
- full source persistence convergence is separately gated and is not required for Skill/engine/package unification.

`docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` defines the staged program. Executor Task Contracts T018-T029 are persisted. T018 is the first executable task and freezes the Consumer v1 characterization/package baseline before structural mutation.

T019-T029 remain prerequisite-gated. T026 is intentionally `BLOCKED` pending T025 semantic-equivalence evidence and a separate accepted decision on source persistence/Markdown ownership. Cancellation of T026 in favor of a source-specific persistence adapter is an explicitly valid outcome.

The refactor program contains ChatGPT-owned Markdown gates MG0-MG3. Executors MUST NOT edit committed Markdown to bypass those gates.

L002 remains separate and non-blocking.

## Delegation rule

All delegated executor work is initiated through an integrated Task Contract and the canonical minimal launch prompt in `docs/TASK-CONTRACTS.md`.

The planning/refactor sequence MUST preserve the split between ChatGPT Markdown ownership and executor non-Markdown ownership. A task is not executable from a planning branch; its controlling contract must be present in current `develop` and its prerequisites satisfied.

## Next Action

1. Treat this checkpoint, D044, the unified refactor plan, and T018-T029 as the integrated MG0 planning frontier.
2. Launch T018 only from a safe current `origin/develop` baseline containing its exact Task Contract.
3. Review T018 evidence and freeze the RF1 characterization baseline before changing T019 to execution-active.
4. Execute subsequent tasks only in dependency order defined by `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`; independent work may overlap only where the plan explicitly allows it.
5. Perform MG1, MG2, and MG3 as ChatGPT-owned Markdown changes at their defined gates; do not delegate those Markdown edits.
6. Do not launch T026 unless T025 is ACCEPTED and a later accepted decision explicitly authorizes live source persistence convergence and resolves Markdown ownership/write semantics.
7. After T029 ACCEPTED, perform a separate Orchestrator release review before any Human-authorized promotion/tag/release action.

## Next Chat Minimum Load

After normal bootstrap, load:

- `docs/decisions/D044-unified-governance-skill-architecture.md`;
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`;
- the currently active Task Contract only;
- additional controlling files only when that Task Contract or a concrete conflict requires them.

Do not reload Caveman/Gentle host history unless a concrete host conflict or ecosystem integration question requires it.

## Do Not

Do not treat the architecture program as one monolithic refactor, bypass RF1 characterization before behavior-preserving structural changes, turn generated distribution snapshots into editable authority, maintain a second independent Governance runtime/Skill product, silently migrate governed repositories on Skill/plugin update, require live source `.agent-coordination/` before the T025/T026 decision gate, delegate committed Markdown edits, retry closed Caveman/Gentle permission work absent new evidence, change provider endpoints, expose secrets, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
