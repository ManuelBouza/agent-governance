# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT
Checkpoint-Sequence: O084
Canonical-Branch: `develop`
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

D040 Phase B remains closed. Protocol `1.13.0` is active and L001 remains `VERIFIED`.

T014-T018 remain ACCEPTED. Consumer Governance Skill v1 and the T018 characterization suite remain the behavioral/rollback baseline for the unified architecture program.

D044 and `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` define the active T018-T029 program. `governance-core/` remains the single normative authority. The architecture continues toward one shared deterministic engine, one canonical Governance Skill source with isolated `consumer` / `source-maintainer` profiles, and generated self-contained distribution artifacts. Full source-persistence convergence remains separately gated.

OP050 completed before T019 execution. The executor reported all three MG0/T018 lifecycle branches retired with no exceptions, and ChatGPT independently verified the canonical remote exposed exactly `develop`, `main` while `develop` remained unchanged at `9148be3c11c85d2bc7e0c43e3e8e86f110b2682f`. This lifecycle gate now records OP050 as DONE.

T019 is ACCEPTED and integrated. ChatGPT remotely reviewed executor branch `refactor/t019-shared-governance-engine` at submitted HEAD `fd71070f4b3ed08826fdde99ad34d81916bec21e`, implementation commit `f5032c30fe4f97b09e566deb3ef12af9e78e9e4f`, base `9148be3c11c85d2bc7e0c43e3e8e86f110b2682f`, and handoff `handoffs/T019-executor-handoff.json`.

The accepted T019 structure moves deterministic Consumer Governance implementation into `src/agent_governance/engine.py`. `governance-skill/scripts/governance.py` is now a thin compatibility launcher containing only shared-engine source resolution, package-path adaptation, frozen-test compatibility forwarding, and `main` delegation. Focused structural coverage confirms command implementation functions do not remain in the launcher.

T019 preserved the frozen T018 baseline unchanged. Accepted evidence reported 1 shared-engine structural test, 2 T018 characterization tests, 77 frozen Consumer v1 baseline tests, 78 combined affected tests, and 262 full deterministic tests, with Ruff/format/py_compile/diff checks PASS and no network/dependency/configuration/Markdown/protocol/CLI/footprint drift. An initial post-extraction run exposed three direct launcher-internal seams; compatibility was restored through thin forwarding without weakening or rewriting the frozen baseline. PR #122 integrated the refactor through squash commit `e2525c54f4de5703b1614bc303346cb044e24a60`.

The source-checkout lookup used by the thin launcher is an accepted temporary T019 boundary, not the final distribution design. T020 is `READY` after this lifecycle gate is integrated. T020 must replace source-tree runtime dependency with a reproducible self-contained build artifact containing the generated Core snapshot, shared engine/runtime, assets, and deterministic identity metadata while preserving the existing Consumer v1 footprint and behavior.

OP051 is `READY` and is the required post-integration cleanup operation for PRs #122 and #123. It retires exactly `refactor/t019-shared-governance-engine` and `docs/t019-accept-t020-ready` after PR #123 merges, using authoritative reviewed-head checks and local-work preservation. T020 should not begin in the executor checkout until OP051 is completed or a concrete cleanup exception is durably resolved.

T021-T029 remain dependency-gated. T026 remains intentionally BLOCKED pending T025 semantic-equivalence evidence and a later accepted persistence/Markdown-ownership decision. MG1, MG2, and MG3 remain ChatGPT-owned Markdown gates at their defined points.

The Caveman/Gentle host configuration line remains closed. L002 remains separate and non-blocking.

## Delegation rule

All delegated executor work is initiated through an integrated Task Contract or Operational Contract and the canonical minimal launch prompt defined by repository policy.

Committed Markdown remains ChatGPT-owned. Executors MUST NOT edit committed Markdown to bypass lifecycle gates, accepted characterization baselines, MG1-MG3, or cleanup authority.

## Next Action

1. Integrate PR #123 into `develop`; this persists T019=`ACCEPTED`, T020=`READY`, OP050=`DONE`, OP051=`READY`, and O084.
2. Launch and complete `docs/operations/OP051-retire-t019-and-lifecycle-branches.md` from a safe current `origin/develop` baseline.
3. Independently verify the canonical remote returns to exactly `develop`, `main`; treat any OP051 exception according to its contract rather than broadening cleanup.
4. Launch T020 only after the cleanup gate is satisfied and from a safe current `origin/develop` baseline containing the exact READY T020 Task Contract and accepted T019 references.
5. Review T020 handoff, built-artifact isolation evidence, reproducibility/identity evidence, remote diff, and full regression before accepting or integrating T020.
6. Continue subsequent tasks only in dependency order defined by `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`; perform MG1, MG2, and MG3 as ChatGPT-owned Markdown gates.
7. Do not launch T026 unless T025 is ACCEPTED and a separate accepted decision authorizes live source persistence convergence and resolves Markdown ownership/write semantics.

## Next Chat Minimum Load

After normal bootstrap, load:

- `docs/decisions/D044-unified-governance-skill-architecture.md`;
- `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md`;
- `docs/tasks/T020-self-contained-build-artifact-and-identity.md`;
- while cleanup is pending, `docs/operations/OP051-retire-t019-and-lifecycle-branches.md`;
- additional controlling files only when T020, OP051, or a concrete conflict requires them.

After OP051 completes, do not reload T019 branch-cleanup history unless a concrete branch, packaging, or accepted-baseline dispute requires it.

## Do Not

Do not weaken or reinterpret the accepted T018/T019 behavior baseline to make packaging easier, treat source-tree lookup as acceptable final distribution behavior, create a hand-maintained duplicate Core authority inside the Skill, copy source-only policy/history/state into consumer artifacts, begin T020 before its READY lifecycle is canonical and cleanup is satisfied, leave the executor checkout on a stale merged topic branch, delete branches outside OP051 scope, maintain a second independent Governance runtime/Skill product, silently migrate governed repositories on Skill/plugin update, require live source `.agent-coordination/` before the T025/T026 decision gate, delegate committed Markdown edits, retry closed Caveman/Gentle permission work absent new evidence, change provider endpoints, expose secrets, make model/provider output a correctness authority, track `.codegraph/`, or write directly to `develop`/`main`.
