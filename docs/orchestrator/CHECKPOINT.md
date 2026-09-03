# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O192  
Canonical-Branch: `develop`  
Current-Work-Unit: T051/MG1-v11 holdout-rotation restart is integrated and controlling; T023 is ready for a fresh v11 epoch after deterministic identity adaptation and preflight  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2-v10 remain closed according to reviews `T023-R1.md` through `T023-R9.md`; v10 is `BLOCKED / EXECUTION_ADAPTER_TRACE_CLASSIFICATION_DEFECT`.
- V10 evidence/infrastructure integration PR `#254`; merge `c0c29cd7f338b3395b7b7f06955265018e030b5b`.
- T050 is `ACCEPTED`; acceptance review `docs/reviews/T050-R1.md`; RF6 integration PR `#258`, merge `b8eae481e65e0aefc690b666e5eed6d01be85ea4`.
- T050 canonical harness facade is `212` physical LOC with extracted modules under `evals/skill_activation_topology/_harness/`, active `code-health.json` ratchet and `tools/code_health.py` size/complexity/dependency/symbol-map checks.
- T051 Task Contract: `docs/tasks/T051-mg1-v11-post-v10-holdout-rotation-restart.md`.
- T051 integration PR `#260`; merge `a15c63df0bf2e252c02d4dc5a3ce4f58a6e6df0a`.

## V10 terminal evidence carried forward

MG1-v10 successfully proved the host path that earlier epochs could not:

- provider-free Windows workspace readability PASS under the selected `unelevated/read-only` profile;
- unchanged synthetic Skill canary PASS `2/2` with successful host-observed `SKILL.md` reads.

V10 then exposed exactly one acceptance prompt: `WX01/B0/r1/a1`.

That attempt was left unscored because immutable runner `cd0f97b0022176efdabe34e7d7142ff3344fa841` falsely classified successful body/reference reads as `HOST_SURFACE_DRIFT / REQUIRED_SKILL_BODY_READ_REJECTED` by matching policy-like text inside successful command output. The technical classifier correction was made only after the attempt, so v10 was correctly closed rather than resumed under a changed runner identity.

V10 acceptance prompts issued: `1`. V10 scored observations: `0`. Selection: none.

The exposed v10 observation remains immutable and diagnostic only. It MUST NOT be rescored, rerun as v10, imported into v11 score or used to tune candidates/thresholds/selection.

## T050 accepted code-health boundary

T050 remains controlling for agent-legible code health:

- `evals/skill_activation_topology/harness.py`: `212` LOC no-net-growth ratchet;
- extracted implementation modules target `<=500` and hard limit `1000` unless separately persisted;
- scoped `C901 <=10`, `PLR0912 <=12`, `PLR0915 <=50`;
- dependency direction/cycle checks;
- deterministic AST symbol/code map;
- accepted RF1 characterization behavior remains regression authority.

A T023 successor MUST run the deterministic code-health gate before provider/model use and MUST NOT re-grow the facade or replace it with another monolith.

Do not create a second project-owned top-level generic coding Skill. The future Maintainer Skill remains the one top-level source-maintenance Skill and may progressively route to `docs/AGENT-LEGIBLE-CODE-HEALTH.md`; mechanical checks remain Skill-independent.

## T051 / MG1-v11 controlling identity

```text
Task: T051
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T051-mg1-v11-post-v10-holdout-rotation-restart.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v11
Execution epoch: MG1-T023-EXECUTION-v11
Corpus: MG1-T023-CORPUS-v5
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
Codex CLI baseline: 0.149.0
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Prior observations allowed in v11 score: 0
Full-completion ceiling when challengers execute: 480 valid observations
```

## V11 holdout rotation

Corpus v5 contains exactly 40 cases and is derived from corpus v4 by one prospective rotation only:

- retired exposed v4/v10 case `WX01` and its exact prompt;
- added fresh case `WX00`;
- `WX00` remains `cross-profile` with `fixture_role=source`;
- expected capabilities remain `source-maintainer`;
- expected semantic outcome remains `bounded-rejection`;
- forbidden capability remains `consumer-lifecycle`;
- the boundary under test remains: canonical source maintenance must not create/use Consumer coordination authority as the basis for a source-product policy decision.

The other 39 cases remain unchanged. Class counts, 29 activation-expected cases, 11 negative/near-miss cases, four cross-profile cases, four ambiguous cases and all final denominators remain unchanged.

Corpus v5 and oracle v11 were frozen in `develop` before any v11 acceptance execution.

## V11 preserved method

V11 preserves from v10:

- B0/B1 reference first; F2/G3 only after a reference exists;
- candidate/reference/presentation bytes;
- Core/engine/profile/capability semantics;
- trial envelope and exact model-visible prompt suffix;
- thresholds and D050 selection;
- paired 2+1 aggregation and no fourth repetition;
- consequence-first class scheduling;
- immediate cross-profile/ambiguous any-occurrence gates;
- exact optimistic qualification futility and challenger materiality futility;
- 180-second non-capacity attempts;
- explicit capacity events as non-attempt pauses;
- Codex 0.149.0 / native Windows / Sol Medium live cell;
- explicit native backend resolution, elevated-first / unelevated fallback;
- inherited-ACL-compatible disposable workspaces;
- provider-free workspace-readability gate;
- unchanged mx-canary with two PASS repetitions before acceptance;
- ignored user config/rules and minimal host feature surface;
- host-observed successful candidate-body read/use as activation authority.

Corrected rejection semantics are now explicit: rejection-like text inside a successful relevant command output does not itself establish Skill-body access rejection. Required-body rejection must come from a relevant failed/denied host event or equivalent unambiguous first-party evidence.

## V11 deterministic pre-provider gate

Before any provider/model call, Executor must adapt only technical identity plumbing required by oracle v11/corpus v5 and run/persist at minimum:

1. Ruff check;
2. Ruff format check;
3. `tools/code_health.py check --root .`;
4. deterministic symbol-map validation;
5. full pytest;
6. focused T023/T050 harness characterization/code-health tests;
7. deterministic harness validation against oracle v11/corpus v5;
8. frozen candidate/presentation/topology/trial-envelope hash verification;
9. proof corpus v5 differs from v4 only by preregistered `WX01 -> WX00` rotation;
10. provider/model calls issued = zero during the deterministic gate.

A red deterministic gate blocks live execution.

## V11 live gate sequence

Only after deterministic gates are green:

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
Status: READY / FRESH V11 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T051-mg1-v11-post-v10-holdout-rotation-restart.md
Expected handoff: handoffs/T023-executor-handoff.json
Implementation Executor launch: Codex NEW / GPT-5.6 Sol / High
Live acceptance cell: Codex / native Windows / GPT-5.6 Sol / Medium
Codex CLI baseline: 0.149.0
Prior observations allowed in v11 score: 0
Pre-provider requirement: v11 identity adaptation + deterministic/code-health gates PASS
Pre-acceptance requirement: provider-free workspace gate PASS + unchanged synthetic canary 2/2 PASS
```

Executor may mechanically update technical oracle/corpus identity validation, deterministic tests, evidence/run metadata identity and resume checks. Executor MUST NOT edit Markdown or semantically alter D052 corpus/oracle/presentations/thresholds/selection.

## Operational integrity note

During this Orchestrator turn an API probe was accidentally written to `main` as `docs/tasks/__probe.txt` in commit `10cd97896b5d95aeae58e833841bed0c2919611d` and immediately removed in commit `fa23a9cc53e6e191d1cdd9c2fe89fe2f00e581de`.

This was not T051 work and did not touch `develop`. The post-removal `main` tree SHA is `a0253eac9fd4aed59aca022fa7522178a9bfd310`, exactly equal to the pre-probe parent `9cfb62c3107b0fd36d3360c7b694d5c9afd95e80` tree SHA, so no repository content delta remains on `main`. The two commits are procedural history only and carry no release/task authority.

## Next action

1. Refresh current canonical `develop` before Executor launch.
2. Show D055: Executor `Codex`; Session `NEW`; Model `GPT-5.6 Sol`; Effort `High`. Rationale: fresh acceptance epoch plus mechanical v11 identity adaptation and high-risk live host/evidence execution; live observations remain Sol / Medium.
3. Launch exactly `docs/tasks/T023-unified-skill-profile-activation-evals.md` from current canonical `develop` using only D042 freshness plus the persisted task pointer; T051 is discovered through current repository authority.
4. Executor first adapts only technical v11 identity plumbing and runs all deterministic/code-health gates with zero provider calls.
5. Only after deterministic PASS may backend/workspace/provider-free/synthetic preflight execute.
6. Only after one complete profile passes canary 2/2 may v11 acceptance begin.
7. Acceptance sends only observations still required by frozen futility/materiality logic.
8. Orchestrator independently converges the successor handoff/evidence before topology acceptance.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not resume v10; do not score/rerun/import `WX01/B0/r1/a1`; do not use the retired `WX01` prompt in v11 acceptance; do not import any prior observation; do not alter corpus v5/oracle v11 after live execution begins; do not change candidates/presentations/thresholds/D050/trial envelope; do not upgrade Codex or substitute host/model/effort; do not weaken provider-free/canary/body-read observability gates; do not bypass code-health; do not write directly to `main`/`develop`.
