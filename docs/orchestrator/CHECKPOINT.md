# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O148  
Canonical-Branch: `develop`  
Current-Work-Unit: D055 Executor launch-profile policy; explicit Human stop before any subsequent implementation task  
Chat-Closure: KEEP_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- T034 native SDD executable materialization is `ACCEPTED` and integrated.
- T035 remains separately gated and is not started.
- T021/T022 remain paused.
- D055 introduces a mandatory Human-facing **Executor Launch Profile** before every Executor prompt.
- The current provider mapping is maintained in `docs/EXECUTOR-LAUNCH-PROFILES.md`; it is operating guidance, not Task Contract authority or repository correctness semantics.
- The active concrete Executor adapter is currently Codex in the ChatGPT desktop app on the native-Windows source-maintenance workstation.
- No post-T034-integration canonical native-Windows baseline has been rerun merely to advance the queue.

## D055 launch invariant

Before every future prompt intended for the Agente de IA Ejecutor, ChatGPT Orchestrator must first show the Human Owner:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Model: <exact recommended current model>
Effort: <exact recommended current effort>
Rationale: <one concise sentence>
```

Then the Executor prompt is shown separately and remains minimal transport to canonical repository/branch state plus persisted execution authority.

Session policy:

- `NEW` is the default for the first launch of a new Task Contract/work unit;
- `CONTINUE` is the default for clean same-task/same-branch follow-up or persisted rework;
- use `NEW` for cold-start/independence evidence, executor/host/checkout changes, stale or contaminated context, unrelated prior work, or inability to reload newly controlling repository instructions safely;
- a newly governing `AGENTS.md` change may use the D043 conditional reload rather than forcing `NEW` when the host can refresh the instruction snapshot reliably.

Compute policy:

- `LOW`: mechanically bounded/read-only/repetitive work with strong deterministic guidance;
- `MEDIUM`: normal Agent Governance implementation/review center of gravity;
- `HIGH`: selective use for concrete substantial technical reasoning risk;
- highest host modes: exceptional only with a concrete justification.

Reasoning effort must not substitute for incomplete Orchestrator-owned specification, Design, Plan/Trace or acceptance authority.

## Current Codex mapping

Current research baseline: 2026-08-23.

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

Fallbacks and re-evaluation rules are defined in `docs/EXECUTOR-LAUNCH-PROFILES.md`. Model names remain provider-specific operating choices, never Governance authority.

## T034 accepted state

```text
T034 status                        = ACCEPTED
T034 R2 acceptance                 = docs/reviews/T034-R2.md
T034 implementation PR             = #193 — MERGED
T034 integrated implementation     = af3b29acb2ad5317a4db23b8399d1bd25f008029
T034 acceptance PR                 = #194 — MERGED
T034 acceptance commit             = 43930c606c37150b8751595250feefcb08db8604
T034 final executor HEAD           = a277e24a957b1a8ffc66f7efc8758cc5933bf451
T034 implementation anchor         = 7dd13b61ae3c710b8b36a58ba21329b169a35005
T034 oracle revision               = T034-A2-v1 — FROZEN / unchanged
```

Accepted branch evidence remains: focused T034/R1 `159 passed`, Ruff lint/format PASS, full deterministic suite `340 passed`, `git diff --check` PASS, no implementation Markdown drift, no skip/xfail/deletion/weakening, and no unresolved Executor Code Review & Verify findings.

## Current remote state

Before integration of this D055 Markdown change:

```text
last verified develop              = 558ef4bcda1689614ba3e24f739105bfbb2a8e11
D055 decision                      = docs/decisions/D055-executor-launch-session-and-compute-profile.md
Executor launch guidance           = docs/EXECUTOR-LAUNCH-PROFILES.md
Active Executor                    = Codex
T035                               = BLOCKED / NOT STARTED
T021/T022                          = PAUSED
```

Reverify canonical `develop` after the D055 Markdown PR is merged and update this identity only through a later durable frontier change when required.

## Stop boundary

Do not automatically:

- author/freeze the T035 oracle;
- launch T035;
- run a next-task/post-integration baseline merely to advance the queue;
- resume T021 or T022;
- create a new executable Task Contract solely because D055 is integrated.

The current work is only the Orchestrator/Executor interaction policy requested by the Human Owner.

## Next action

1. Integrate D055, `docs/EXECUTOR-LAUNCH-PROFILES.md`, the minimal `AGENTS.md` wiring and this O148 checkpoint through the current Markdown-only PR.
2. Reverify canonical `develop` after merge.
3. Report the research result and integrated interaction policy to the Human Owner; stop before any implementation-task queue advancement.
4. For every later Executor prompt, resolve the active Executor and emit the D055 launch card before the prompt.

## Next chat minimum load

Until the Human explicitly authorizes a subsequent work unit, load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint.

Load D055 and `docs/EXECUTOR-LAUNCH-PROFILES.md` when preparing or revising an Executor launch profile. Load task-specific artifacts only after a future explicit direction makes that work unit relevant.

## Do not

Do not advance T035/T021/T022 without Human direction; do not claim a post-integration Windows baseline that has not been rerun; do not infer model/session settings without knowing the concrete active Executor; do not put provider-specific model identity into Task Contract correctness semantics; do not use higher reasoning to compensate for missing specification authority; do not hand routine CLI/API/shell commands to the Human; and do not write directly to `main`/`develop`.
