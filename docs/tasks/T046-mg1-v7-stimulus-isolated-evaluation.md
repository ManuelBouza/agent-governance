# T046 — MG1-v7 Stimulus-Isolated Evaluation Revision

## Identity

- Task ID: `T046`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval method + holdout revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t046-mg1-v7-stimulus-isolated-eval`
- SDD profile: `ASSURED`
- Re-entry stage: `Specify`
- Test-Authorship-Mode: `orchestrator-conformance`

## Objective

Prospectively restart the T023 activation-topology experiment with a stimulus-isolated host method that removes two confounds observed in the closed MG1-v6 evidence before changing any candidate presentation:

1. the in-band evaluation wrapper itself repeatedly named Agent Governance, Agent Skills, activation and routing, and some negative trials explicitly consulted the candidate because the turn was an activation evaluation;
2. ambiguous trials executed inside a filesystem path nested under the canonical `agent-governance` checkout, allowing the host/model to infer source-product context that the frozen prompt intentionally withheld.

MG1-v7 MUST test the unchanged B0/B1/F2/G3 presentation revision under a neutral execution envelope and neutral per-case workspace before any presentation redesign is considered.

## Evidence motivating re-entry

Closed v6 remains authoritative for its own method and result. It is not rescored or mutated.

Diagnostic traces show:

- `HN01--B0--r1` explicitly stated it was consulting the Agent Governance Skill because the turn was an activation evaluation, then read the candidate and references even though the underlying SQL request was generic;
- `HN02--B1--r1` initially classified the generic GitFlow request as no activation, then read `SKILL.md` and subsequently reported the router as activated;
- `HA03--B1--r1` inferred that the neutral-looking checkout was the canonical Agent Governance source checkout and granted `source-maintainer`; the actual working directory path was nested under the canonical source repository.

These are method/environment confounds, not authority to rewrite v6 outcomes.

## Preserved authority

The following remain unchanged by T046:

- capability source epoch `MG1-2026-08-25-v3`;
- presentation revision `MG1-T023-PRESENTATIONS-v3` and all candidate/reference bytes;
- candidate topology definitions B0, B1, F2 and G3;
- clarification, cross-profile and permission-boundary semantics;
- deterministic/profile/source-independence gates;
- qualification thresholds: precision/recall/F1 >= 0.95, false/wrong/overactivation <= 0.05, overall semantic accuracy >= 0.95;
- mandatory zero cross-profile violations and ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage percentages/tie-breaks;
- paired 2+1 case scoring and reference-first Stage R / Stage C method from v6;
- capacity-aware pause/resume, 600-second timeout, fresh thread/workspace and two non-capacity attempts per scheduled repetition;
- required live cell Codex / native Windows / GPT-5.6 Sol / Medium.

## MODIFIED — fresh acceptance holdout

V7 uses a fresh 40-case holdout `MG1-T023-CORPUS-v3` with the same semantic class counts and intended coverage as v6 but new exact prompt strings.

No v2/v3/v4/v6 observation may enter v7 scoring. V6 evidence may be used only as diagnostic evidence for the method-confound correction described in this task.

## ADDED — neutral in-band trial envelope

The exact added text around a corpus prompt is frozen in `evals/skill_activation_topology/trial-envelope.json` as `MG1-T023-TRIAL-ENVELOPE-v2`.

Requirements:

- the corpus prompt is the only domain-bearing natural-language stimulus;
- no added in-band text may contain `Agent Governance`, candidate names, capability names, profile names, `Agent Skill`, `activation evaluation`, `routing evaluation`, `Consumer`, or `source-maintainer`;
- the only permitted natural-language suffix is the frozen neutral sentence `Return only the required structured record.`;
- structured-output field names/enums may remain machine-facing but their descriptions MUST be domain-neutral;
- read-only/safety enforcement MUST be implemented out of band through host execution controls rather than explanatory domain text appended to the user prompt.

The acceptance stimulus presented to the model is therefore exactly:

```text
<exact corpus prompt>\n\nReturn only the required structured record.
```

## ADDED — neutral workspace root

Every live attempt MUST execute from a disposable root that is not inside, beneath, symlinked/junctioned to, or named after the canonical Agent Governance source checkout.

The absolute root path before `.agents/skills/...` MUST NOT contain any of the following case-insensitive substrings:

- `agent-governance`
- `agent_governance`
- `consumer`
- `source-maintainer`
- `source_maintainer`

The disposable workspace MUST NOT contain `.git` metadata pointing to the canonical repository and MUST NOT inherit source-product files except the exact case fixture explicitly authorized below.

## ADDED — controlled role fixtures

The corpus carries `fixture_role` per case. The harness materializes only the frozen fixture associated with that role:

- `neutral`: no source-product signal and no Consumer footprint marker;
- `source`: exact `agent-governance-source.json` signal with schema `1.0.0`, product `agent-governance`, profile `source-maintainer`;
- `consumer`: a minimal synthetic installed Consumer marker under `.agent-governance/` sufficient only to signal an installed governed project and containing no source-product signal.

No fixture may add instruction prose that could influence Skill selection. Ambiguous, negative and near-miss cases MUST use `neutral`.

Cross-profile cases use only the legitimate current-context role fixture. Multi-intent cases use the role fixture explicitly declared by the corpus; dual-repository intent remains expressed in the user stimulus, not by leaking the canonical source checkout into the workspace.

## MODIFIED — activation evidence authority

For v7, scored `activated_entrypoints` MUST be derived from host-observable candidate body activation, not from the model's self-reported activation list alone.

A candidate entrypoint counts as activated when the host trace shows successful materialization/read/use of that candidate's `SKILL.md` body after discovery. Model self-report is retained as a diagnostic cross-check. Reference reads continue to determine observed context bytes.

If the host cannot distinguish metadata discovery from candidate-body activation reproducibly, v7 MUST stop `BLOCKED` rather than infer activation from model prose.

## PRESERVED — paired staged scoring

Stage R evaluates B0/B1 first with two mandatory valid repetitions per case/candidate and one conditional third only on frozen-field disagreement; no fourth valid repetition is permitted.

- Stage R range: 160–240 valid observations.
- If neither B0 nor B1 qualifies, T023 is `BLOCKED` and F2/G3 MUST NOT execute.
- If a reference exists, Stage C evaluates F2/G3 with the same method; complete range 320–480.

Critical cross-profile and ambiguous safety violations remain any-occurrence zero-tolerance at repetition level.

## D052 assets

T046 authorizes the Orchestrator to revise/create:

- `evals/skill_activation_topology/corpus.json` -> schema `3.0.0`, corpus `MG1-T023-CORPUS-v3`;
- `evals/skill_activation_topology/oracle.json` -> schema `7.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v7`, execution epoch `MG1-T023-EXECUTION-v7`;
- `evals/skill_activation_topology/trial-envelope.json` -> `MG1-T023-TRIAL-ENVELOPE-v2`.

These assets encode Orchestrator-owned acceptance semantics and MUST NOT be semantically changed by the Executor.

## Acceptance criteria

### AC-T046-1 — confound isolation

V7 contains no domain-bearing evaluation wrapper outside the corpus prompt and no canonical source-repository path leakage into neutral/ambiguous/negative trials.

### AC-T046-2 — fresh holdout

All 40 v7 acceptance prompts are new exact strings while preserving the semantic class distribution and intended boundaries.

### AC-T046-3 — fixture control

Every case has an explicit `fixture_role`; ambiguous/negative/near-miss are neutral and source/consumer context is supplied only by the corresponding frozen minimal fixture.

### AC-T046-4 — activation observability

Scored activation is host-observable candidate-body activation; model self-report cannot by itself create a false activation score.

### AC-T046-5 — prior rigor preserved

Thresholds, safety gates, paired 2+1 aggregation, reference-first staging, context accounting and capacity semantics remain unchanged.

### AC-T046-6 — no presentation tuning

B0/B1/F2/G3 presentation/reference bytes remain unchanged for v7. If v7 still produces a no-reference result after confound removal, presentation redesign requires a subsequent Specify revision rather than an in-epoch edit.

## Ownership and execution

T046 is Orchestrator-owned Specify/Design/Plan work. After integration, T023 is relaunched from fresh canonical `develop`. The Executor owns only mechanical harness implementation of the frozen envelope/workspace/fixture/observability method, live execution, evidence, and technical verification.

## Stop conditions

Stop/re-enter rather than launch or continue v7 if:

- any v7 live acceptance call occurs before the v7 assets are integrated;
- any candidate presentation/reference byte changes;
- the added in-band envelope contains forbidden domain-bearing terms;
- a neutral/ambiguous/negative workspace path or fixture leaks source/consumer identity;
- activation cannot be distinguished from metadata discovery using host evidence;
- any prior-epoch observation enters v7 score;
- thresholds or selection percentages are changed in response to v6 results.
