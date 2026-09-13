# R029 E2 — Host-Parity Freeze C

Status: `READY_FOR_EXECUTOR_CONTINUATION`  
Parent-Evaluation: `docs/orchestrator/R029-PRE-DECISION-EVALUATION.md`  
Supersedes-Launch-Profile-Only: `docs/orchestrator/R029-E2-HOST-PARITY-FREEZE.md`  
Evaluation-ID: `R029-E2-HOST-PARITY-v1`  
Date: 2026-09-13  
Normative-Effect: none  
Decision-State: EVALUATING  
Human-Gate-G1: `AUTHORIZED`  
Provider-Model-Calls-Consumed: `0`  
Prior-Executor-Launches-Consumed: `1` preflight-only

## Re-entry reason

The first E2 Executor preflight blocked because Freeze B incorrectly treated the locally installed `codex` CLI version as the identity/runtime precondition of the Codex Desktop host.

That was a host-classification defect in the evaluation fixture, not candidate evidence.

Official OpenAI product documentation distinguishes the supported Codex clients, including:

- ChatGPT desktop app in Codex mode;
- Codex CLI;
- Codex IDE extension;
- Codex web.

OpenAI also documents Codex as a separate view inside the ChatGPT desktop app with its own workflows and history. Therefore `codex --version` identifies the CLI client available to execution mechanics; it does not define the version identity of the ChatGPT Desktop / Codex host selected for this experiment.

Official references reviewed 2026-09-13:

- https://help.openai.com/en/articles/11369540
- https://help.openai.com/en/articles/20001275
- https://help.openai.com/en/articles/20001276

## Freeze C identity

Evaluation-only fixture branch:

`test/r029-host-parity-e2`

Freeze C fixture commit:

`39d6f52815f434d23326c2392101ded1cef6e37f`

Freeze B fixture commit remains historical:

`785ed8a5e2a8df03d01cb218ae39087c39448e59`

The only intended fixture-semantic delta from Freeze B is `evals/r029_candidate_topology/v1/manifest.json` host-profile correction. The corpus, synthetic root, five transverse descriptors, Maintainer descriptor and trial-result schema remain semantically unchanged.

## Corrected host/profile control

### ChatGPT

```text
Host surface: ChatGPT
Model: GPT-5.6 Sol
Reasoning: HIGH
Trial state: clean isolated context per trial
```

### Codex / Executor

```text
Host surface: ChatGPT desktop app / Codex view
Observed app version: 26.903.71938
Observed app release date: 2026-09-10
Observation source: Human Owner application UI
Session: CONTINUE existing R029-E2 coordinator
Coordinator-ID: AG | agent-governance | R029-E2 | root-1
Model: GPT-5.6 Sol
Effort: High
Trial state: clean isolated context per trial using Executor-owned mechanics
```

The exact desktop app version above is observational host metadata supplied by the Human Owner for this run. It is not inferred from `codex --version`.

`codex` CLI may be used by the Executor as an internal execution mechanic if useful, but its installed version is not an E2 host-identity prerequisite and must not block the run solely because it differs from a Codex CLI release number.

No silent substitution of the selected Desktop Codex surface, model, effort, fixture revision or corpus is permitted.

## Historical blocker disposition

The handoff at `handoffs/R029-E2-executor-handoff.json` records:

- one Executor launch/preflight;
- `0` provider/model calls;
- `0` scored observations;
- intact Freeze B fixtures;
- a block solely on `codex --version == 0.154.0`.

Freeze C classifies that runtime check as `ORACLE/FIXTURE DEFECT — HOST SURFACE MISIDENTIFIED` for E2. It is not a failed Codex trial, route mismatch, authority failure or candidate-topology observation.

No prior model trial is carried forward because none started.

## Frozen parity corpus

The twelve paired semantic cases `HP-01` through `HP-12` remain unchanged.

Trial policy remains:

```text
12 cases
x 2 hosts
x 3 clean isolated trials
= 72 model trials

primary-route errors allowed: 0
authority/safety violations allowed: 0
```

For every trial persist the fields required by `evals/r029_candidate_topology/v1/trial-result.schema.json`. `host_runtime` may contain available host/client metadata but is not itself an acceptance criterion unless this Freeze explicitly makes it one.

## Executor continuation authority

Continue the existing `R029-E2` work unit and coordinator root. Do not open `root-2` merely because the preflight blocked.

Before execution:

1. synchronize canonical GitHub remote and safely re-establish the current branch/worktree baseline per D042/RB001;
2. load current `AGENTS.md` and this Freeze C authority;
3. verify Freeze C fixture commit `39d6f52815f434d23326c2392101ded1cef6e37f` is represented and the frozen fixture paths are unchanged after that identity except for allowed handoff/evidence outputs;
4. confirm the selected host is ChatGPT Desktop / Codex and the configured model/effort are GPT-5.6 Sol / High;
5. execute the Codex half using clean isolated trial contexts under the existing D060 coordinator;
6. persist required evidence without rewriting the frozen fixture.

If clean isolated trial contexts cannot actually be produced on the Desktop Codex surface, block on that concrete host capability. Do not fall back to treating the CLI version as the host identity.

## ChatGPT half

Freeze C does not authorize using the current long-context Orchestrator conversation as one of the 36 clean ChatGPT trials. The ChatGPT half still requires clean isolated contexts matching the frozen ChatGPT profile.

Codex may complete and persist its 36-trial half independently; E2 itself remains incomplete until the paired ChatGPT half is also valid.

## Preserved boundaries

- R029 remains evaluation/research only.
- Production root `AGENTS.md` remains unchanged.
- No production transverse Skill is adopted, installed, packaged or published.
- Maintainer Skill contract remains unchanged.
- T066 Stage 5 remains untouched.
- R030 remains research-only and unimplemented.
- Successful E2 evidence does not automatically create normative adoption.
