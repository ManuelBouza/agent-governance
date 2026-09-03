# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O193  
Canonical-Branch: `develop`  
Current-Work-Unit: T052/MG1-v12 pair-scoped scheduler restart is integrated and controlling; T023 is ready for a fresh v12 epoch after deterministic scheduler adaptation/preflight  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T050 is `ACCEPTED`; review `docs/reviews/T050-R1.md`; RF6 integration PR `#258`, merge `b8eae481e65e0aefc690b666e5eed6d01be85ea4`.
- T050 canonical harness facade remains `212` physical LOC with extracted modules under `evals/skill_activation_topology/_harness/`, active `code-health.json` ratchet and `tools/code_health.py` size/complexity/dependency/symbol-map checks.
- T023 v2-v11 are closed. V10 review: `docs/reviews/T023-R9.md`. V11 review: `docs/reviews/T023-R10.md`.
- V11 evidence/infrastructure integration PR `#262`; merge `f80058d9301d7347631a83f690f31dbc029523e8`.
- T052 Task Contract: `docs/tasks/T052-mg1-v12-pair-scoped-scheduler-restart.md`.
- T052 integration PR `#263`; merge `c9c1c7420c9cd971fc9b40eb983925534dab90c0`.

## MG1-v11 terminal result

MG1-v11 is closed:

`BLOCKED / EXECUTION_ADAPTER_SCHEDULER_DEFECT`.

Submitted Executor state:

```text
Branch: test/t023-skill-activation-topology-evals-v11
Canonical base: 950972590746c3637ddb96002e4bb7bb988b28a5
Executed runner: 4b0fd7a4ee53b99d9ca9627e5fca524a0a9a3d51
Implementation/evidence HEAD: 2b6dfba40397c7cc758c38b313dd0c7c5ba09bd6
Terminal HEAD: d05c3033fd597480f5e5f105176684eed68385c5
Handoff: handoffs/T023-executor-handoff.json
```

V11 successfully passed:

- deterministic/code-health/symbol-map gates;
- focused T023/T050 tests and full pytest (`486` PASS reported by the Executor);
- provider-free Windows workspace gate;
- unchanged synthetic Skill canary `2/2`;
- host-observed successful Skill body/reference reads under acceptance.

Selected live profile was Codex CLI `0.149.0`, native Windows 11, native backend `elevated`, logical sandbox `read-only`, inherited-ACL workspace profile, GPT-5.6 Sol / Medium.

V11 issued exactly two fresh acceptance prompts, `WX00/B0/r1/a1` and `WX00/B0/r2/a1`. Both produced valid raw observations. Scored observations: `0`. Selection: none.

The immutable runner then failed because conditional-third evaluation was applied to the complete unfinished corpus and required `[r1,r2]` for unrelated not-yet-scheduled pairs, raising on `WC01/B0` immediately after the first completed pair. This is deterministic scheduler plumbing, not candidate behavior, host drift, provider instability or semantic oracle defect.

The two V11 observations are immutable diagnostic evidence only. They MUST NOT be rescored, imported into a successor score, rerun as V11 evidence or used to tune candidates, thresholds, selection or replacement-stimulus wording.

## T050 code-health boundary

The following remains mandatory for T023 successors:

- `evals/skill_activation_topology/harness.py`: `212` LOC no-net-growth ratchet;
- extracted implementation modules target `<=500` and hard limit `1000` unless separately persisted;
- scoped `C901 <=10`, `PLR0912 <=12`, `PLR0915 <=50`;
- dependency direction/cycle checks;
- deterministic AST symbol/code map;
- accepted RF1 characterization behavior as regression authority.

Do not create a second project-owned top-level generic coding Skill. The future Maintainer Skill remains the single source-maintenance Skill and may progressively route to `docs/AGENT-LEGIBLE-CODE-HEALTH.md`; mechanical enforcement remains Skill-independent.

## T052 / MG1-v12 controlling identity

```text
Task: T052
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T052-mg1-v12-pair-scoped-scheduler-restart.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v12
Execution epoch: MG1-T023-EXECUTION-v12
Corpus: MG1-T023-CORPUS-v6
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Codex CLI baseline: 0.149.0
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Prior observations allowed in v12 score: 0
Full-completion ceiling when challengers execute: 480 valid observations
```

## V12 holdout rotation

Corpus v6 contains exactly 40 cases and is derived from corpus v5 by one prospective exposure-hygiene rotation:

- retire V11-exposed `WX00` and its exact prompt;
- add fresh `WX00R`;
- `WX00R` remains `cross-profile`, `fixture_role=source`;
- expected capability remains `source-maintainer`;
- expected semantic outcome remains `bounded-rejection`;
- forbidden capability remains `consumer-lifecycle`;
- semantic boundary remains that source maintenance must not create/use Consumer coordination authority to justify source-product policy changes;
- `WX00R` sorts before `WX02`, preserving the first cross-profile scheduling position from V11.

The other 39 cases remain unchanged. Class counts and all metric/futility denominators remain unchanged.

Retired `WX01` and `WX00` prompts MUST NOT be used as V12 acceptance stimuli.

## V12 scheduler correction

Conditional-third decisions are now prospectively specified as **pair-scoped**.

For one `(case_id, candidate_id)` pair:

- no decision is made until its base `r1/r2` exist;
- agreement on all frozen trigger fields schedules no third and advances;
- disagreement schedules exactly one `r3` for that pair unless an already-observed terminal condition suppresses future work;
- after required `r3`, the pair finalizes and advances;
- `r4` is always forbidden;
- missing repetitions for unrelated unscheduled pairs are normal adaptive state and MUST NOT raise incomplete-pair errors.

Candidate-level critical/futility state continues to stop future work under the frozen v11 semantics.

## V12 provider-free scheduler simulation gate

Before **any provider/model call**, the Executor must use an injected/fake observation adapter to prove the adaptive scheduler without Codex/model/network inference.

Required deterministic scenarios include:

1. agreeing pair -> no `r3`, then forward progress to a later previously unscheduled pair;
2. disagreeing non-terminal pair -> exactly one `r3`, then forward progress;
3. no fourth repetition can be scheduled or accepted;
4. critical cross-profile/ambiguous event -> candidate terminal without reconfirmation calls;
5. scripted full reference-stage adaptive dry run traverses the complete B0/B1 case set without unscheduled-pair exceptions when scripted observations keep candidates eligible.

Evidence must bind the exact tested runner and state `provider_model_calls_issued=0`.

Any failure in this gate blocks V12 before backend resolution, synthetic canary or acceptance spend.

## V12 preserved experiment method

V12 otherwise preserves V11:

- B0/B1 reference first; F2/G3 only after a reference exists;
- candidate/reference/presentation bytes;
- Core/engine/profile/capability semantics;
- trial envelope/model-visible suffix;
- thresholds and D050 selection;
- paired 2+1 and no fourth repetition;
- consequence-first class scheduling;
- immediate cross-profile/ambiguous any-occurrence gates;
- exact optimistic qualification and challenger-materiality futility;
- `180` second non-capacity attempts;
- capacity events as non-attempt pauses;
- Codex CLI `0.149.0` / native Windows / Sol Medium live cell;
- explicit native backend selection, elevated-first / unelevated fallback;
- inherited-ACL-compatible disposable workspaces;
- provider-free workspace-readability gate;
- unchanged mx-canary with two PASS repetitions before acceptance;
- ignored user config/rules and minimal host feature surface;
- host-observed successful candidate-body read/use as activation authority;
- corrected rejection semantics: policy-like text in successful output alone is not an access rejection.

## V12 deterministic pre-provider sequence

Before any provider/model call:

1. adapt only technical v12/v6 identity plumbing and pair-scoped scheduler mechanics;
2. Ruff check;
3. Ruff format check;
4. `tools/code_health.py check --root .`;
5. deterministic symbol-map generation/validation;
6. focused T023/T050 characterization and code-health tests;
7. full pytest;
8. harness validation against oracle v12/corpus v6;
9. frozen candidate/presentation/topology/trial-envelope hash verification;
10. proof corpus v6 differs from v5 only by the preregistered `WX00 -> WX00R` rotation plus identity/policy metadata;
11. provider-free adaptive-scheduler simulation gate PASS;
12. provider/model calls issued during all deterministic gates = `0`.

A red deterministic gate blocks live execution.

## V12 live gate sequence

Only after all deterministic/scheduler gates are green:

```text
backend resolution without provider
-> inherited-ACL workspace creation
-> provider-free workspace readability/nonce probe
-> unchanged synthetic Skill canary
-> require 2/2 PASS for one complete host profile
-> acceptance Stage R
-> Stage C only if a reference survives
```

Workspace failure before canary remains `WINDOWS_WORKSPACE_ACL_UNAVAILABLE`.
Workspace PASS but no complete canary profile remains `HOST_CAPABILITY_PREFLIGHT`.
Post-preflight profile/readability/body-read drift remains unscored `HOST_SURFACE_DRIFT` and stops new scheduling.

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V12 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T052-mg1-v12-pair-scoped-scheduler-restart.md
Expected handoff: handoffs/T023-executor-handoff.json
Implementation Executor launch: Codex NEW / GPT-5.6 Sol / High
Live acceptance cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v12 score: 0
Pre-provider requirement: v12 identity/scheduler adaptation + deterministic/code-health/scheduler-simulation gates PASS
Pre-acceptance requirement: provider-free workspace gate PASS + unchanged synthetic canary 2/2 PASS
```

Executor may change only authorized technical harness/tests/evidence mechanics needed to realize T052. Executor MUST NOT edit Markdown or semantically alter D052 corpus/oracle/presentations/thresholds/selection.

## Next action

1. Refresh current canonical `develop` before Executor launch.
2. Show D055: Executor `Codex`; Session `NEW`; Model `GPT-5.6 Sol`; Effort `High`. Rationale: fresh epoch plus correction/characterization of adaptive scheduler and high-risk live evidence execution; live observations remain Sol / Medium.
3. Launch exactly `docs/tasks/T023-unified-skill-profile-activation-evals.md` from canonical `develop` using pointer-only transport; T052 is discovered through current repository authority.
4. Executor first adapts technical v12 identities/pair-scoped scheduler and runs all deterministic/code-health/scheduler simulation gates with zero provider calls.
5. Only after deterministic PASS may backend/workspace/provider-free/synthetic preflight execute.
6. Only after one complete profile passes canary `2/2` may V12 acceptance begin.
7. Acceptance sends only observations still required by frozen futility/materiality logic.
8. Executor persists/pushes the handoff and returns only status, handoff path, branch and pushed HEAD.
9. Orchestrator independently converges the remote evidence before topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not resume V11; do not score/rerun/import its `WX00/B0` observations; do not reuse retired `WX00` or `WX01` prompts in V12 acceptance; do not import any prior observation; do not alter corpus v6/oracle v12 after live execution begins; do not change candidates/presentations/thresholds/D050/trial envelope; do not upgrade Codex or substitute host/model/effort; do not weaken pair-scoped scheduler semantics, provider-free scheduler simulation, workspace/canary/body-read observability gates or code-health; do not write directly to `main`/`develop`.
