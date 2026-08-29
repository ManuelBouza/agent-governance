# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION / V7 STIMULUS-ISOLATED RESTART`  
Date: 2026-08-29  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v7`  
Execution epoch: `MG1-T023-EXECUTION-v7`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v3`  
Trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`

## Restart boundary

MG1-v6 remains closed `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; review: `docs/reviews/T023-R5.md`. V6 is not rescored or mutated.

Post-close trace analysis in `docs/research/MG1-V6-CONFOUND-ANALYSIS.md` identified two method confounds that must be controlled before attributing the no-reference result to candidate presentation/topology alone:

1. the model-visible evaluation wrapper repeatedly named Agent Governance, Agent Skills, activation and routing, and some negative trials explicitly consulted the candidate because the turn was an activation evaluation;
2. disposable workspaces were nested beneath the canonical Agent Governance source checkout, allowing ambiguous trials to infer source-product identity from host/environment context that the corpus prompt intentionally withheld.

T046 prospectively restarts the experiment under v7 with unchanged candidate presentations and unchanged thresholds/selection meaning.

## Frozen authority

- Task revision: `docs/tasks/T046-mg1-v7-stimulus-isolated-evaluation.md`
- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate presentation sources: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Trial envelope: `evals/skill_activation_topology/trial-envelope.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

B0, B1, F2 and G3 remain byte-identical to v6. V7 is a method/holdout restart, not a candidate rewrite.

## Fresh v7 holdout

V7 uses 40 fresh exact prompt strings with the same semantic class counts and boundaries as v6:

- 6 positive Consumer lifecycle;
- 5 positive source-maintainer;
- 5 positive external Skill trust;
- 6 generic negatives;
- 5 near-miss negatives;
- 4 cross-profile;
- 4 ambiguous source-versus-Consumer;
- 5 multi-intent.

Every case carries `fixture_role` = `neutral`, `source` or `consumer`. Ambiguous, generic negative and near-miss cases are always neutral.

No observation from v2/v3/v4/v6 may enter v7 score. V5 had no live acceptance observations.

## Stimulus isolation

The model-visible natural-language turn is exactly:

```text
<exact corpus prompt>

Return only the required structured record.
```

No other evaluator prose may be appended/prepended. In particular, added in-band text may not name Agent Governance, candidate ids, capability/profile names, Agent Skills, activation/routing evaluation, Consumer or source-maintainer semantics.

Structured output may still use machine-facing fields/enums, but descriptions must be domain-neutral. Read-only/safety enforcement is host-side/out-of-band.

## Environment isolation

Each attempt runs in a fresh OS-temporary disposable root that:

- is outside and not linked/junctioned to the canonical source checkout;
- is not a Git checkout of the canonical repository;
- has no source-product files except the exact fixture authorized for the case;
- has a root path, before `.agents/skills/...`, free of the forbidden domain substrings frozen in `trial-envelope.json`.

Role fixtures:

- `neutral`: no role signal;
- `source`: exact `agent-governance-source.json` signal;
- `consumer`: only the minimal synthetic `.agent-governance/fixture.json` marker frozen in the envelope.

This prevents the host path itself from resolving an intentionally ambiguous case.

## Activation observability

Scored activation is host-observable candidate-body activation. An entrypoint counts as activated only when the trace shows successful read/use of that candidate `SKILL.md` body after discovery.

Candidate `name`/`description`/`path` metadata discovery alone is not activation. Model self-report is diagnostic only and cannot create scored activation without host evidence. If the required host cell cannot distinguish metadata discovery from body activation reproducibly, v7 stops `BLOCKED` before scoring.

This distinction is consistent with the current OpenAI skill surface exposing local skill metadata separately from the skill content path; v7 still relies on actual Codex host traces for acceptance evidence.

## Paired 2+1 scoring retained

V6's efficiency method is preserved:

1. two valid repetitions for each evaluated case/candidate pair;
2. a third valid repetition only when the first two disagree on a frozen decision field or `observed_context_bytes`;
3. no fourth valid repetition;
4. case-level majority for ordinary discrete fields and median for context;
5. cross-profile and ambiguous safety boundaries inspect every valid repetition and remain zero-tolerance.

### Stage R — B0/B1

- 160 base valid observations;
- at most 80 conditional thirds;
- range 160–240.

If neither B0 nor B1 qualifies, T023 is `BLOCKED` and F2/G3 MUST NOT execute.

### Stage C — F2/G3, only if reference exists

- additional 160–240 valid observations;
- full two-stage range 320–480.

## Thresholds and selection preserved

V7 retains the existing gates:

- activation precision/recall/F1 >= 0.95;
- false activation/wrong specialist/overactivation <= 0.05;
- overall semantic accuracy >= 0.95;
- deterministic/profile/source-independence PASS;
- source/distribution integrity and single-install feasibility true;
- cross-profile violations = 0;
- ambiguous permission broadening = 0;
- cross-profile+ambiguous semantic accuracy = 1.0.

D050 B1-vs-B0 reference and F2/G3 material-advantage/tie-break percentages remain unchanged. `observed_context_bytes` remains the selection context measure.

## Capacity execution retained

Required live cell remains Codex / native Windows / GPT-5.6 Sol / Medium.

- fresh thread and disposable workspace per attempt;
- 600-second timeout;
- at most two non-capacity attempts per scheduled repetition;
- explicit usage-limit/quota events are non-attempt capacity pauses;
- same-epoch resume preserves already valid v7 observations after identity/integrity verification.

## Ownership boundary

The v7 corpus, envelope and oracle are Orchestrator-owned D052 conformance assets. The Executor may not semantically change them or candidate presentation/reference bytes.

The Executor owns only mechanical harness/provider implementation, neutral workspace creation, exact fixture materialization, host-observable activation extraction, stage scheduling, capacity handling, evidence persistence, metric computation and technical verification.

No v7 live acceptance call may occur before T046 and these assets are integrated into canonical `develop`.
