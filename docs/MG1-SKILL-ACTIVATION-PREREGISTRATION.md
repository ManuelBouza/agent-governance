# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION`  
Date: 2026-08-26  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v4`  
Execution epoch: `MG1-T023-EXECUTION-v4`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v2`

## Restart boundary

MG1-v2 is closed `BLOCKED`; no topology was selected. MG1-v3 is closed `EXECUTION-INCOMPLETE`: it attempted 75 sessions, retained 74 complete observations and stopped on one unclassified timeout. Review: `docs/reviews/T023-R2.md`.

Neither v2 nor the 74 completed v3 observations may enter the v4 acceptance score. They remain diagnostic evidence only.

V4 is a prospective execution-method restart under `docs/tasks/T043-mg1-v4-uniform-execution-recovery.md`. It does not change candidate semantics, holdout membership/expectations, thresholds or selection meaning.

## Frozen authority

- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- V3 presentation sources retained for v4: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

Required candidates remain exactly B0, B1, F2 and G3. All are projections of one Agent Governance product, one Core, one shared engine and one capability-source epoch. Portable Skill-to-Skill invocation remains forbidden.

## Candidate presentation semantics

B0 is the unified dispatcher baseline and deliberately loads all three capability references after activation.

B1 is a thin neutral router. It classifies first, loads only required capability references, and may activate without loading a reference when explicit Agent Governance context is source-versus-Consumer ambiguous and clarification is required.

F2 exposes Consumer Governance and Source Maintainer peers. G3 exposes Consumer Lifecycle, Source Maintainer and External Skill Trust peers. Profile-specific peers do not activate for unresolved source-versus-Consumer ambiguity.

All files are exact Orchestrator-owned D052 assets and may only be byte-copied by the Executor.

## Holdout and uniform v4 execution method

The acceptance holdout contains 40 exact prompts spanning positive Consumer, source-maintainer, external trust, negative, near-miss, cross-profile, ambiguous and multi-intent classes.

Required live cell:

- Host: Codex
- Platform: native Windows
- Model: GPT-5.6 Sol
- Effort: Medium

The v4 acceptance run starts from zero and requires exactly 40 x 4 x 3 = **480 logical scored observations**. Candidate order rotates deterministically.

Each logical observation permits at most two attempts. Every attempt uses a fresh Codex thread and disposable workspace, the same frozen prompt/candidate/repetition/materialization, and a uniform 600-second timeout. Failed attempts are retained as diagnostic evidence and never scored. The first valid structured result is the sole scored observation. A logical observation with two failed attempts blocks the entire acceptance run; partial metrics or topology selection are forbidden.

Retry counts/failure classes are reported per candidate as diagnostics. Mechanical smoke and prior-experiment regression cases do not enter acceptance scores.

## Clarification and cross-profile semantics

For `clarify-context`, no profile/capability permission may be granted and no governed mutation may occur. Neutral B0/B1 activation solely to ask for missing context is permitted and is not permission broadening. Their expected ambiguous entrypoint is frozen in `topologies.json`; F2/G3 have none.

For `bounded-rejection`, activation of the legitimate current-context capability is permitted. A violation exists when a forbidden capability/profile is granted/performed or the required bounded rejection is not returned.

## Context/load accounting

Selection uses `observed_context_bytes`: the UTF-8 byte sum of unique successfully host-read materialized candidate `SKILL.md` files plus unique successfully host-read candidate references in that trial. Only host-observed successful reads count; model self-report does not.

`activation_surface_bytes` and `loaded_reference_bytes` remain separately reported diagnostics. Byte measures are not exact token counts.

## Mandatory boundaries and thresholds

Every qualifying candidate must preserve deterministic/profile/source-independence PASS, one-product/source/install integrity, zero forbidden capability grants/operations, zero ambiguous permission broadening, and 100% correct semantic outcome for cross-profile/ambiguous cases.

Routing thresholds remain: precision/recall/F1 >= 0.95; false activation/wrong-specialist/overactivation <= 0.05; overall semantic-outcome accuracy >= 0.95.

Selection remains D050-consistent: B1 replaces B0 only with routing non-regression and >=20% median observed-context reduction. F2/G3 count as material challengers only with >=0.03 absolute F1 advantage, >=15% median observed-context reduction, no worse false activation, and <=0.01 wrong-specialist/overactivation regression versus the single-family reference.

If neither B0 nor B1 qualifies, the result is `BLOCKED`; thresholds may not be weakened after results are seen.

## Ownership boundary

The frozen semantic assets above are Orchestrator-owned under D052. Executor owns harness/provider mechanics, trial isolation/recovery plumbing, byte-copy materialization, observed-trace extraction, metric computation, result evidence, supplementary diagnostics and ordinary technical tests.

If a semantic defect is suspected, stop the affected claim and report it. Do not mutate corpus membership, expected outcomes, presentation wording, thresholds, execution-recovery meaning or selection meaning.
