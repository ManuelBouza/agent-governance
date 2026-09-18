# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O345  
Date: 2026-09-18  
Canonical-Branch: `develop`  
Current-Work-Unit: `T066 / R027-R028 ChatGPT + Codex efficiency screening`  
State: T066_STAGE5_FREEZE_A_COMPLETE_AWAITING_HUMAN_LAUNCH  
Chat-Closure: HUMAN_GATE  
Human-Objective: Materialize T066 Stage 5 provider-free Freeze A from current `develop`  
T066-Task-Contract: `docs/tasks/T066-r027-chatgpt-codex-efficiency-evaluation.md`  
T066-Stage5-State: COMPLETE  
Freeze-A-State: PUBLISHED_PROVIDER_FREE_VERIFIED  
Scientific-Branch: `test/r027-chatgpt-codex-efficiency-v2`  
Scientific-Branch-Head: `e00acd9bbee6ca8e260fdd3d96bbd26452d0ef48`  
Scientific-Branch-Base: `develop@6b7d2aa8f2f8682a39afb84ee99aa0b4383f4acc`  
Abandoned-Branch: `test/r027-chatgpt-codex-efficiency-v1@dc8fd229bf403fbc2085ee906740f0cad63cbd43`  
Abandoned-Branch-Disposition: HUMAN_DISCARD_DO_NOT_CONSUM  
D077-T066-Disposition: MATERIAL_UPSTREAM_CHANGE_REVALIDATED_FOR_FREEZE_A  
Provider-Free-Verification: PASS  
Provider-Model-Calls-T066: 0  
Scored-Observations-T066: 0  
Executor-Authorization: NOT_AUTHORIZED_PENDING_SEPARATE_HUMAN_LAUNCH  
Active-Executor: none  
T068-State: DEFERRED_UNTIL_PERSONAL_PLUS_NATIVE_SKILLS_AVAILABLE  
ChatGPT-Empirical-Parity: NOT_ESTABLISHED  
Next-ChatGPT-Effort: HIGH  
Next-Action: Await a separate explicit Human launch authorization for T066. If authorized, perform live-host measurement/instruction/model/rate-card preflight and begin Phase 1 only if every preflight condition passes. Do not consume a scored arm while any required identity or measurement is ambiguous.  
Next-Chat-Minimum-Load: current `develop`; `AGENTS.md`; this checkpoint; T066 Task Contract; `evals/r027_efficiency/freeze_a.json` from the exact frozen scientific HEAD  
Do-Not-Load-Or-Do: Do not consume the abandoned v1 branch; do not mutate the frozen v2 scientific branch; do not launch Codex/Executor or consume provider/model calls without separate Human authorization; do not resume T068 unless separately selected; do not claim empirical parity or production-policy adoption from T066 screening.

## Stage 5 closure

The Human Owner selected T066 Stage 5 and explicitly chose to discard the pre-existing divergent v1 scientific branch.

A fresh scientific branch was created from the canonical baseline:

```text
develop@6b7d2aa8f2f8682a39afb84ee99aa0b4383f4acc
-> test/r027-chatgpt-codex-efficiency-v2
-> Freeze A e00acd9bbee6ca8e260fdd3d96bbd26452d0ef48
```

Freeze A freezes:

- 9 matched pairs / 18 opaque arms across Phases 1-3 and archetypes A/B/C;
- deterministic D052 acceptance oracles and repository-realistic fixture generation;
- counterbalanced scheduler seed/order and fail-closed phase gates;
- contamination/isolation controls;
- common progressive verification contract;
- scoring and credit normalization;
- terminal result schema;
- current D077, rate-card, runtime, instruction-loading and model-identity receipts;
- provider-free integrity/conformance tests.

Provider-free verification evidence:

```text
exact reconstructed Git blob SHA match: PASS
python3 evals/r027_efficiency/integrity.py: PASS
python3 -m pytest -q tests/test_r027_efficiency_freeze.py: 5 passed
provider/model calls consumed: 0
scored observations: 0
```

The frozen branch is now immutable experimental authority for Stage 6 launch preparation. Do not append further Stage 5 work to it.

## D077 / live preflight boundary

Stage 5 found material drift relative to historical R027/R028 inputs:

- current root `AGENTS.md` is 12,095 bytes, below the documented default 32 KiB project-instruction budget;
- current official purchased-credit rates differ from the historical R028 rate assumptions;
- current stable Codex CLI observed upstream is 0.155.0.

Those observations are evidence, not a production-policy change.

Before the first scored arm, the live host must still prove:

- actual client/runtime identity;
- applicable signed-in account / pricing regime;
- exact per-arm token attribution;
- requested/resolved model identity where observable;
- required `MEDIUM` reasoning and `STANDARD` speed;
- complete active instruction loading without truncation.

Failure or ambiguity in any required measurement/configuration remains a fail-closed stop condition.

## Preserved frontier

- D055/D068 and other production ownership/model policies are unchanged.
- T068 remains deferred.
- T066 remains screening-only; no result can self-promote into policy.
- ChatGPT/Codex empirical parity remains `NOT_ESTABLISHED`.
