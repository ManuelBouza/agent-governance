# Orchestrator Checkpoint

Checkpoint-ID: O259  
Date: 2026-09-09  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_EXTERNAL_REVALIDATION_COMPLETE_READY_FOR_EXPLICIT_HUMAN_LAUNCH  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

Canonical `develop` before this revalidation change set:

`bd3e0473525c064c23bef9bff5bf542fd82a7f50`

After O258, the Human asked whether a **fresh external OpenAI/Codex revalidation** had actually been performed. It had not. The Human then said `adelante` specifically to perform that research/revalidation.

That instruction authorized the research and necessary prelaunch classification correction only. It did **not** launch T063 and did not resume T062.

Fresh research is persisted as:

`docs/research/R018-CODEX-SUBAGENT-RUNTIME-REVALIDATION.md`

Prelaunch T063 correction is persisted as:

`docs/reviews/T063-R1.md`

## Fresh official Codex revalidation

R018 revalidated current official OpenAI documentation and exact stable Codex source on 2026-09-09.

Current stable release at review time:

```text
codex-cli 0.153.4
release tag: rust-v0.153.4
```

Official `0.154.0-alpha.*` releases are pre-releases and are not preferred for the scored T063 run merely because they are newer.

The stable `0.153.4` source and current Subagents documentation confirm:

- subagents are intended for concrete bounded work, especially independent/parallel exploration, testing, analysis and other noisy context;
- subagents add their own model/tool/token work, so unconditional delegation is not free;
- stable runtime guidance distinguishes immediate critical-path/tightly coupled local work from bounded independent sidecars suitable for delegation;
- current Codex supports child model/reasoning inheritance and override/configuration paths;
- Multi-Agent V2 model/reasoning override exposure exists in stable source but remains runtime/configuration dependent;
- subagents inherit parent permission/sandbox posture, subject to supported custom/runtime configuration;
- current model guidance supports GPT-5.6 for demanding work, Terra for lighter/read-heavy supporting work and Luna for narrow/repeatable work, with Medium as normal balanced effort and High for review/complex logic.

Therefore D075 remains supported without normative change and T063 must retain fail-closed live capability/profile/permission measurement gates.

## T063 topology correction

T063 originally described all scored probes as `DELEGATED` under D075/D065.

T063-R1 corrects the exact Stage-A label:

```text
execution_target: CONTRACT_FIXED
underlying_delegation_eligibility: DELEGATED
```

Reason:

- the selected probe units are deliberately material/read-heavy enough to independently satisfy D065/D075 delegation eligibility;
- but the exact CONTROL/ADAPTIVE child topology, ordering, context, permissions and receipts are material experimental authority fixed by T063 itself;
- D075 therefore classifies the actual scored topology as `CONTRACT_FIXED`.

This is a governance-label correction only. Probe semantics, arm order, scoring, quality gates and child-compute hypotheses are unchanged.

Terminal T063 evidence must record both concepts or semantic equivalents.

## T063 prelaunch profile recommendation — not yet frozen

R018 supports the following **prelaunch hypothesis**:

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | T063 | root-1
preferred stable runtime: Codex 0.153.4
root / CONTROL: GPT-5.6 Sol / Medium
P1 ADAPTIVE:     GPT-5.6 Luna / Medium
P2 ADAPTIVE:     GPT-5.6 Terra / Medium
P3 ADAPTIVE:     GPT-5.6 Terra / High
```

Rationale for retaining Sol/Medium as the pilot root rather than relying on the 0.153.4 default:

- T054 used Sol/Medium as the CONTROL baseline;
- R010 still defers global Astra adoption;
- Codex 0.153.4 can default to Astra when no model is explicitly configured;
- explicitly pinning Sol avoids introducing an unplanned root-model-family change into the corrected successor experiment.

These values are not frozen launch authority yet. After an explicit Human `launch T063`, ChatGPT must immediately revalidate the concrete host/account/runtime surface and persist the exact launch matrix before rendering the Codex transport prompt.

## T063 Task Contract state

Controlling task:

`docs/tasks/T063-adaptive-worker-routing-requalification.md`

Controlling prelaunch correction:

`docs/reviews/T063-R1.md`

Current state:

```text
Task: T063
Status: READY / NOT_AUTHORIZED_PENDING_EXPLICIT_HUMAN_LAUNCH
Type: read-only matched-arm Executor/subagent evaluation
SDD profile: ASSURED
Expected evidence branch: test/t063-adaptive-worker-routing-requalification
Executor: none
Provider/model calls: 0
Scored topology: CONTRACT_FIXED
Underlying probe delegation eligibility: DELEGATED
Adaptive Stage-B policy: EVALUATING / NOT DECIDED
```

D063 exact-child read-only/profile/usage/duration/reroute measurement remains mandatory. Live failure of that surface is `BLOCKED_MEASUREMENT_SURFACE`; requested/resolved profile mismatch is `BLOCKED_PROFILE_RESOLUTION`.

## Research traceability

`docs/RESEARCH-TRACEABILITY.md` now records:

```text
R017: COMPLETE / DECIDED -> D075
       fresh external revalidation supplied later by R018

R018: COMPLETE / NOT_REQUIRED
       fresh current official Codex runtime/documentation revalidation

R007: COMPLETE / EVALUATING -> T063
       no global adaptive worker-routing policy yet
```

R018 explicitly records the provenance correction: R017/D075 were integrated before a genuinely fresh external revalidation was performed. R018 closes that gap rather than rewriting history.

## T062 held frontier

T023-R33 remains controlling. T062 has not been resumed.

```text
scientific branch:               test/t023-skill-activation-topology-evals-v15
terminal Stage 5 HEAD:           3e0d0b71cf382db502e186622f40a23bcd915390
Candidate Freeze E:              5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Holdout/oracle Freeze F:         5b8ac55980ecdbb6a2bf3784812b933647f2f13d
blocked Stage 6 evidence HEAD:   b9034e450f04fbc9736543425e531159d4b79d49
blocked handoff:                 handoffs/T062-executor-handoff.json
provider/model calls:            0
R32 continuation authority:      valid but unconsumed
R32 transport:                   PAUSED by T023-R33
```

Do not paste/execute the R32 T062 continuation prompt while R33 controls.

## D061 / D062 state

This research/correction change set uses verified short-lived topic branch:

`docs/t063-official-codex-revalidation`

Authoring base:

`develop@bd3e0473525c064c23bef9bff5bf542fd82a7f50`

GitHub ruleset `22339910` was revalidated active over `main`/`develop`, requiring PR transport, blocking deletion/non-fast-forward updates and exposing no routine bypass.

No direct content write to `develop` or `main` is authorized.

## Other durable constraints

- T024 remains unauthorized until T023 has an accepted topology selection from valid Stage 6 evidence.
- T058 remains frozen by explicit Human decision; do not resume, integrate, clean or copy it without new explicit Human authorization.
- D066 intentional gaps remain unchanged.
- D071/D072/D073 remain controlling for future Codex Human-mediated transport/title handling.
- Historical scientific branches/freezes/evidence boundaries remain immutable.

## Next Chat Minimum Load

At the start of the next source-maintenance chat, after reading current `develop`, `AGENTS.md` and this checkpoint:

1. for T063, load `docs/tasks/T063-adaptive-worker-routing-requalification.md` and `docs/reviews/T063-R1.md`;
2. load R018 and D075;
3. load R007, D063 and T054-R1 when preparing launch/evaluation details;
4. load R010 only if the root-model choice is questioned or Astra is proposed;
5. load D065/D060/D055 only when a concrete routing/launch conflict requires their full text;
6. for T062 resumption, instead load T023-R31/R32/R33 plus the current scientific branch/handoff;
7. do not reconstruct either frontier from prior chats or Project Memory.

## Next Action

STOP. Fresh external revalidation is complete, but T063 is **not launched**.

The Human may explicitly select:

```text
launch T063
```

Then ChatGPT must revalidate the live host/account/runtime capabilities, persist the exact T063 launch matrix/profile and render a NEW Codex handoff for `AG | agent-governance | T063 | root-1`.

Or the Human may explicitly select:

```text
resume T062
```

Then ChatGPT must revalidate R31/R32/R33 and the held scientific branch before removing the Human Hold.

A generic `go` remains insufficient while these two separate work units are available.
