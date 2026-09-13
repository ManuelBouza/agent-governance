# T067 — R029 / D082 Materialization and Post-Materialization Qualification

## Identity

- Task ID: `T067`
- Status: `READY`
- Type: `refactor`
- SDD profile: `ASSURED`
- Base branch: `develop`
- Base SHA: `758b92cf38af9bc06e4717b1206dafb8e5d82e9e`
- Topic branch: `refactor/r029-d082-materialization`
- Expected Executor handoff: `handoffs/T067-executor-handoff.json`
- Test-Authorship-Mode: `mixed`
- Owner: `ChatGPT Orchestrator (Stages 1-5/7 and semantic oracle) / Agente de IA Ejecutor (Stage 6) / Human Owner (final authority)`
- Execution Shape: `MULTI_EXECUTION`
- ChatGPT Effort: `HIGH`

## Objective

Materialize and post-materialization-qualify the R029 architecture adopted by D082 without weakening any preserved authority, ownership, safety, cold-start, fail-closed, routing, or residual condition.

Normative topology:

```text
lean always-loaded root AGENTS.md
  + one Agent Governance Maintainer top-level domain Skill
       -> Orchestrator internal route
       -> Executor internal route
  + exactly five transverse top-level Skills
       -> repository-change-control
       -> upstream-version-revalidation
       -> research-evidence-traceability
       -> durable-work-checkpoint
       -> executor-launch-handoff
            -> workspace-isolation internal route/reference
  + host-specific mechanics only as narrow adapters/references
  + deterministic scripts/CI/references for mechanical enforcement
```

T066 is out of scope and must remain untouched.

## Controlling authority

Load only the smallest set needed for the active stage:

- `AGENTS.md`
- D082, D068, D061, D067, D080
- `docs/orchestrator/R029-S1-ROOT-PRESERVATION-MAP.md`
- `docs/orchestrator/R029-S2-LEAN-ROOT-RESPONSIBILITY-CONTRACT.md`
- `docs/orchestrator/R029-S3-MAINTAINER-DOMAIN-BOUNDARY.md`
- R029 S4-S9 candidate/placement artifacts and S10 evaluation plan when their exact trigger/qualification semantics are material
- `docs/orchestrator/R029-E3-CONVERGENCE.md`
- `docs/MAINTAINER-SKILL-CONTRACT.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md`
- `maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md`

D082 is the normative architecture authority. R029 scientific artifacts are preservation/evaluation evidence.

## Requirement delta

### ADDED

- `T067-A1` Preserve all 79 S1 units with `ROOT=39`, `ROOT+ROUTE=20`, `ROUTE=20`, uncovered `0`.
- `T067-A2` Materialize one top-level Maintainer domain Skill with internal Orchestrator/Executor routes.
- `T067-A3` Materialize exactly the five D082 transverse top-level Skills.
- `T067-A4` Keep workspace isolation subordinate to `executor-launch-handoff`, consuming repository/local change-control policy for repository semantics.
- `T067-A5` Publish deterministic Stage 5 qualification assets for preservation, topology, descriptors, activation oracle, cold-start/no-Skill checks, context-burden measurement, normative ownership, and reference-hop depth.
- `T067-A6` Measure actual root bytes, catalog metadata bytes, representative conditional loads, normative duplication, and reference-hop depth during Stage 6.
- `T067-A7` Qualify production Maintainer activation/anti-trigger behavior; historical `21/36` remains informational/unscored.
- `T067-A8` Preserve ChatGPT/Codex empirical parity as `NOT_ESTABLISHED`.
- `T067-A9` Reuse historical Codex `36/36` transverse evidence unless production semantics/descriptions materially changed.

### PRESERVED

- `T067-P1` Human / Orchestrator / Executor authority stays unchanged except the already-adopted D068 Stage 5/6/7 refinement.
- `T067-P2` Pre-routing authority, ownership, safety, fail-closed behavior, durable authority, and cold-start correctness do not depend on Skill activation.
- `T067-P3` Skills are routing/tooling aids, not governance authority; deterministic verification works with Skills absent/disabled.
- `T067-P4` Source-maintenance and consumer-governance activation domains remain separate.
- `T067-P5` Agent Governance D052/D053/D054/D055/D058/D060/D061/D062/D065/D068/D076/D077/D080 semantics remain domain-side.
- `T067-P6` Historical/grandfathered persisted authority retains its original meaning.
- `T067-P7` Progressive disclosure reduces duplicated always-on procedure without duplicating normative ownership.
- `T067-P8` T066 remains not started and unchanged.

## Controlling Design

### Lean root

`AGENTS.md` must preserve the twelve R029 S2 pre-routing responsibility families: repository/contamination boundary; authority/host neutrality; write ownership; SDD/re-entry safety; semantic-vs-mechanics/Human gate; durable authority; bootstrap/routing anchors; mutation/branch safety; durable handoff; research/freshness; Skill independence/coexistence; instruction/change-discipline guardrail.

Every ROOT/ROOT+ROUTE obligation remains represented before optional routing.

### Maintainer domain

Production package:

```text
maintainer-skill/SKILL.md
maintainer-skill/references/orchestrator-route.md
maintainer-skill/references/executor-route.md
maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md
maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md
```

There is one top-level source-maintenance domain Skill. Internal routes select context only and never create roles or authority.

### Transverse packages

```text
repository-change-control-skill/SKILL.md
upstream-version-revalidation-skill/SKILL.md
research-evidence-traceability-skill/SKILL.md
durable-work-checkpoint-skill/SKILL.md
executor-launch-handoff-skill/SKILL.md
executor-launch-handoff-skill/references/workspace-isolation.md
```

Each `SKILL.md` carries a narrow positive trigger, explicit anti-triggers, bounded postcondition, and authority boundary consistent with R029 S4-S8. Host identity cannot split a semantic capability.

### Stage 5 semantic/conformance assets

Orchestrator-owned frozen inputs:

```text
evals/r029_materialization/preservation-ledger.json
evals/r029_materialization/activation-corpus.json
evals/r029_materialization/qualification-profile.json
evals/r029_materialization/normative-rule-index.json
evals/r029_materialization/descriptor-equivalence.json
tests/test_r029_materialization.py
tools/r029_materialization_qualify.py
```

The Executor may execute and technically diagnose these assets but must not weaken their semantic expectations.

### Measurement method

`tools/r029_materialization_qualify.py` records at least:

- `root_bytes` against pre-materialization baseline `34567`;
- `initial_catalog_bytes` for Maintainer + five transverse name/description metadata;
- representative conditional-context bytes with exact loaded paths;
- stable normative rule-family ownership / duplicate-owner findings;
- representative and maximum reference-hop depth.

No numeric optimization threshold is invented. Context reduction cannot compensate for lost authority/safety.

### Provider-evidence reuse

`evals/r029_materialization/descriptor-equivalence.json` freezes the Stage 5 disposition:

```text
overall_disposition: MATERIALLY_EQUIVALENT
historical Codex transverse evidence: REUSE_AS_REGRESSION_EVIDENCE
fresh 36-trial rerun required: false
ChatGPT/Codex empirical parity: NOT_ESTABLISHED
Maintainer 21/36 history: informational/unscored
```

If Stage 6 finds a material descriptor/semantic mismatch that invalidates this disposition, stop for Orchestrator re-entry rather than launching fresh provider/model trials autonomously.

## Plan & Trace / D080 units

| Unit | Owner | Durable boundary | Gate |
| --- | --- | --- | --- |
| `E1` | ChatGPT | this contract + verified topic branch | complete |
| `E2` | ChatGPT | complete D082 candidate + semantic/conformance assets + published Stage 5 checkpoint | complete |
| `E3` | Executor | execution/diagnosis/bounded repair/Code Review & Verify + handoff/evidence | DONE permits E4; BLOCKED/PARTIAL re-enters earliest affected stage |
| `E4` | ChatGPT | convergence, qualification disposition, PR/integration, checkpoint | objective closure or explicit re-entry |

Later units must not begin before the previous gate is satisfied.

## Stage ownership

```text
Stages 1-4 -> ChatGPT Orchestrator
Stage 5    -> ChatGPT Orchestrator
Stage 6    -> Agente de IA Ejecutor
Stage 7    -> ChatGPT Orchestrator
```

The Executor must not reconstruct or first-pass materialize this architecture.

## Published Stage 5 candidate freeze

```text
candidate_branch:                 refactor/r029-d082-materialization
candidate_materialization_anchor: c59dfe3ed2ee69d2fbfb9100f6927dbd10051017
candidate_checkpoint_head:        c6da4445862f0166192283479d3ae77c27d07f78
candidate_base:                   758b92cf38af9bc06e4717b1206dafb8e5d82e9e
```

`candidate_materialization_anchor` introduced the complete Stage 5 product/eval candidate. `candidate_checkpoint_head` additionally persists O322, the durable E2 -> E3 frontier. This Task Contract freeze is necessarily a metadata-only successor because a file cannot contain the SHA of the commit that contains itself.

Before Stage 6 launch, ChatGPT supplies the exact current remote branch HEAD in thin transport. The Executor must verify:

1. `candidate_checkpoint_head` is an ancestor of that launch HEAD;
2. the diff from `candidate_checkpoint_head` to launch HEAD contains only this T067 freeze/finalization metadata;
3. no candidate product/test/eval/checkpoint artifact changed after `candidate_checkpoint_head`;
4. `candidate_materialization_anchor` is an ancestor of `candidate_checkpoint_head`;
5. the protected base remains the exact `candidate_base`.

Any other pre-Stage-6 branch movement requires Orchestrator re-entry.

## Authorized Stage 6 scope

The Executor may:

- establish exact branch/base/candidate identities;
- execute the already-published deterministic tests/evals/measurement tooling;
- inspect root/Skill/reference topology and perform Code Review & Verify;
- diagnose technical failures inside D082 and this Design;
- make bounded **non-Markdown** technical repairs that do not change topology, triggers/anti-triggers, authority, acceptance meaning, or Orchestrator-owned semantic oracle meaning;
- add small supplementary technical verification inside approved semantics;
- persist `handoffs/T067-executor-handoff.json` and authorized non-Markdown evidence.

The Executor must not edit committed Markdown; add/remove/split/merge top-level Skills; change workspace-isolation placement; change the 79-unit mapping; weaken activation expected classifications; relabel parity; autonomously rerun/waive provider evidence; touch T066; or first-pass-create substantial missing harness/controller/script/fixture/oracle material.

D076 applies to all Stage 6 executable aids.

## Acceptance criteria

- `AC-T067-1` Preservation: 79/79 with `39/20/20`, zero unresolved, and no pre-routing obligation dependent on Skill activation.
- `AC-T067-2` Topology: one Maintainer/two internal routes; exactly five transverse Skills; workspace isolation internal.
- `AC-T067-3` Activation: production Maintainer and transverse positive/anti-trigger/composition cases preserve the frozen semantic boundaries.
- `AC-T067-4` Cold start: cold Orchestrator/authorized Executor bootstrap is reconstructable from canonical Git without chat or Skill activation; mismatches fail closed.
- `AC-T067-5` Progressive disclosure: actual burden metrics and reference hops are measured/reviewable with no semantic loss.
- `AC-T067-6` Deterministic qualification: repository-owned qualification assets execute without model-driven Skill activation.
- `AC-T067-7` Residual integrity: parity remains `NOT_ESTABLISHED`; Maintainer historical `21/36` remains unscored history.
- `AC-T067-8` Evidence economy: no ceremonial repeat of 36 Codex trials.
- `AC-T067-9` Stage boundary: E2 materializes, E3 executes/verifies/repairs only, E4 accepts/integrates.
- `AC-T067-10` Isolation: T066 unchanged/not started.

## Stage 6 required evidence

At minimum execute/review:

- deterministic 79-unit preservation/topology checks;
- syntax/structure of production Skill packages/references;
- frozen activation/anti-trigger corpus against production descriptions/routing behavior at the strongest available non-authority-changing surface;
- cold-start/no-Skill structural checks;
- burden measurement tool with persisted non-Markdown results;
- absence of a sixth workspace-isolation Skill;
- normative ownership/reference-hop outputs;
- descriptor-equivalence disposition;
- normal affected repository test/lint/conformance suite.

Executor Code Review & Verify must inspect requirement/Design/PRESERVED fidelity, missing/duplicated authority, false trigger risks, hidden Skill dependency, stale/unreachable references, measurement reproducibility, unauthorized scope, and D076 compliance.

## Stop / re-entry

Stop rather than guess if branch/base/candidate identity is unsafe; any S1 unit lacks an unambiguous destination; root slimming makes safety/authority conditional on Skills; Maintainer/consumer routing is materially ambiguous; workspace isolation appears to require a sixth Skill; production routing contradicts D082 evidence; descriptor equivalence is materially false and fresh provider evidence would be required; a semantic oracle is defective; substantial Stage 5 qualification material is missing; a repair would change D082/Design/acceptance semantics; or T066 would need modification.

## Expected handoff

Stage 6 must persist:

```text
handoffs/T067-executor-handoff.json
```

It must satisfy `docs/EXECUTOR-HANDOFFS.md`, including SDD profile, implementation/review SHA anchors, requirement trace, verification results/runtime, findings, re-entry fields, and D076 `ephemeral_artifacts`.

Terminal response:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T067-executor-handoff.json
BRANCH: refactor/r029-d082-materialization
HEAD: <actual pushed remote branch HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

ChatGPT must present the D055 concrete Executor/session/model/effort profile and the exact launch HEAD before the Human starts Stage 6.

## Thin transport invariant

The Human-visible Executor prompt contains only the canonical repository, session/coordinator identity when required, this Task Contract path, and exact authorized branch@launch-HEAD. Design, tests, commands, repair rules, evidence schema, and stop conditions remain in canonical Git authority.
