# R029 E2 — Host-Parity Freeze and Launch Gate

Status: `FREEZE_B_COMPLETE_BLOCKED_EXECUTION_SURFACE`  
Parent-Evaluation: `docs/orchestrator/R029-PRE-DECISION-EVALUATION.md`  
Evaluation-ID: `R029-E2-HOST-PARITY-v1`  
Date: 2026-09-13  
Normative-Effect: none  
Decision-State: EVALUATING  
Human-Gate-G1: `AUTHORIZED`  
Provider-Model-Calls-Consumed: `0`  
Executor-Launches-Consumed: `0`

## Human authorization

After O312 exposed G1 as the explicit next Human gate, the Human Owner responded `go` in the same active R029 evaluation chat on 2026-09-13. For this objective, that authorizes only:

- an evaluation-only runnable representation of the R029 candidate topology;
- the provider/model calls required by the frozen E2 host-parity evaluation;
- the Codex Executor launch needed to execute that evaluation under the repository's existing D054/D055/D060/D068/D076 boundaries.

This authorization does **not** adopt the candidate architecture, authorize a production root rewrite, authorize production Skill packaging/install/release, change the Maintainer Skill contract, start T066, or adopt/implement R030.

## Freeze B identity

Evaluation-only fixture branch:

`test/r029-host-parity-e2`

Frozen fixture commit:

`785ed8a5e2a8df03d01cb218ae39087c39448e59`

The frozen fixture is the exact E2 candidate representation. Later checkpoint/review/evidence commits on the branch must not rewrite these fixture files without explicit re-entry and a new freeze identity.

Fixture paths:

- `evals/r029_candidate_topology/v1/manifest.json`
- `evals/r029_candidate_topology/v1/corpus.json`
- `evals/r029_candidate_topology/v1/trial-result.schema.json`
- `evals/r029_candidate_topology/v1/root/AGENTS.md`
- `evals/r029_candidate_topology/v1/skills/agent-governance-source-maintainer/SKILL.md`
- `evals/r029_candidate_topology/v1/skills/repository-change-control/SKILL.md`
- `evals/r029_candidate_topology/v1/skills/upstream-version-revalidation/SKILL.md`
- `evals/r029_candidate_topology/v1/skills/research-evidence-traceability/SKILL.md`
- `evals/r029_candidate_topology/v1/skills/durable-work-checkpoint/SKILL.md`
- `evals/r029_candidate_topology/v1/skills/executor-launch-handoff/SKILL.md`

These are synthetic evaluation fixtures. Their wording/names are not production architecture decisions.

## Frozen parity corpus

The corpus contains the twelve paired semantic cases required by the provider-free evaluation:

`HP-01` through `HP-12`, covering RCC positive/near-miss, UVR positive/anti-trigger, RET positive/anti-trigger, DWC positive/stale-mismatch, ELH positive/anti-trigger, UVR+RET composition, and ELH+workspace-isolation+RCC composition.

Each case is executed on both hosts with the same semantic prompt. The frozen trial policy is:

```text
12 cases
x 2 hosts
x 3 clean isolated trials
= 72 model trials

primary-route errors allowed: 0
authority/safety violations allowed: 0
```

Repeated trials satisfy the repository requirement that probabilistic routing behavior not be accepted from one successful prompt.

## Host/profile control

To measure host parity rather than model-family differences, E2 holds the model and reasoning profile constant:

### ChatGPT

```text
Host: ChatGPT
Model: GPT-5.6 Sol
Reasoning: HIGH
Trial state: clean isolated context per trial
```

### Codex / Executor

```text
Executor: Codex
Session: NEW for the E2 work unit
Coordinator-ID: AG | agent-governance | R029-E2 | root-1
Host-Display-Title: n/a until launch
Runtime: Codex 0.154.0 stable
Model: GPT-5.6 Sol
Effort: High
Rationale: hold model/effort constant with ChatGPT so E2 measures host/adapter routing behavior rather than a model confound; use clean isolated trial contexts inside the D060 coordinator lifecycle.
```

The concrete clean-trial child/thread/session mechanics remain Executor-owned under D054. The evaluation must not create 36 Human-visible Codex coordinator roots merely to obtain clean trials.

If either host cannot execute exactly the frozen profile, classify the affected trial/run as blocked. Do not silently substitute Astra, Terra, Luna, another effort level, another fixture revision, or a different Codex runtime.

## D077 revalidation

Reviewed 2026-09-13 from official OpenAI sources:

- `https://github.com/openai/codex/releases`
- `https://developers.openai.com/api/docs/models/gpt-5.6-sol`
- `https://developers.openai.com/api/docs/models`

Observed for this launch surface:

- Codex `0.154.0` is the current stable release in the reviewed release stream;
- `0.155.0-alpha.*` exists as a prerelease line and is not selected as E2 authority;
- GPT-5.6 Sol remains a current supported model with `high` reasoning support;
- GPT-6 Astra is available/current flagship, but changing to Astra would introduce a model confound and is not required to evaluate ChatGPT/Codex parity of the frozen GPT-5.6 Sol representation.

D077 disposition for E2 launch profile: `NO_MATERIAL_CHANGE` relative to current Agent Governance Codex guidance. No upgrade/requalification is required merely because Astra or a higher prerelease exists.

## Current execution-surface blocker

The active ChatGPT environment can read/write GitHub and browse current documentation, but it exposes no connected tool that can actually:

1. launch a Codex coordinator/model turn;
2. start clean ChatGPT trial sessions programmatically;
3. install/materialize the synthetic fixture into those two hosts and capture routing traces.

Plugin discovery found optional external integrations, but none is currently installed/connected as an E2 execution surface. A GitHub operation, this current long-context ChatGPT conversation, or a self-authored static answer is not a substitute for a clean host/model trial.

Therefore:

```text
G1 Human authorization                 -> PASS / AUTHORIZED
Freeze B candidate representation      -> COMPLETE
E2 host/model execution                -> BLOCKED_EXECUTION_SURFACE
provider/model calls consumed          -> 0
scored empirical observations          -> 0
```

This is an instrumentation/access blocker, not candidate evidence and not a topology failure.

## Required evidence when execution surface exists

For every trial, persist data satisfying `trial-result.schema.json`, including exact fixture commit, host/runtime, model/effort, case/trial identity, clean-session identity, observed primary/composed routes, authority outcome, violation flag, status and evidence/transcript reference.

E2 passes only if the complete frozen run yields:

- 36 valid ChatGPT trials and 36 valid Codex trials;
- zero primary-route errors against the frozen corpus;
- zero authority/safety violations;
- equivalent semantic postconditions across hosts where host mechanics differ;
- no host-specific top-level Skill split required to obtain correct routing.

Any fixture mutation, profile substitution, incomplete host half or unverifiable self-report invalidates the affected evidence for this freeze.

## Next condition

Continue E2 only after a real connected execution surface can run both host halves under this freeze. Until then, do not simulate the 72 observations and do not advance to E3 or normative decision readiness.
