# T066 Freeze A — R027/R028 Lean Executor screening

State: `PROVIDER_FREE_FREEZE_A`  
Task: `T066`  
Scope: `SCREENING_ONLY`  
Frozen base: `develop@6d4a698832cf08bded0351b0046fe5b2bf38b1c0`  
Scientific branch: `test/r027-chatgpt-codex-efficiency-v1`  
Scored provider/model calls in Freeze A: `0`

This directory is the provider-free Stage 5 control package required by T066 v2 and D079. It freezes nine matched pairs, eighteen maximum scored arms, D052 acceptance oracles, deterministic order/isolation, the common L0→L4 verification contract, scoring, exact-use accounting requirements, and the live-preflight blockers that must be cleared before any scored arm.

Freeze A does **not** authorize a Codex launch. D068 remains the production ownership policy. A scored launch requires separate Human authorization plus the live host/account preflight represented in `launch-envelope.json` and `receipts/`.

## Frozen benchmark geometry

`pairs.json` indexes three phase-scoped immutable pair files. The nine pairs cover three phases and three ordinary source-maintenance archetypes per phase: localized Python behavior fix, bounded multi-file configuration synchronization preserving public behavior, and small CLI/service behavior addition preserving no-option behavior. Every pair has two isomorphic variants differing only in identifiers, data, and constants while preserving step depth, file-count class, verification geometry, and acceptance meaning. Markdown is excluded from scored subject work.

`fixture_generator.py` creates only a starter fixture for one requested frozen variant. It never creates a solution. Control-arm solution materialization remains deferred to the frozen scored schedule as required by T066.

## Execution control

`schedule.json` freezes seed `6602807917` and the full counterbalanced arm order. `scheduler.py` is fail-closed: later phases require an explicit prior `PASSED` gate, earlier arms cannot be skipped, and each launch must use one exclusive writable workspace plus one allowed fixture/result namespace. All scored work is root-local with `children_used = 0` and `agents.enabled = false` required at live preflight.

The instruction envelope freezes `project_doc_max_bytes = 65536` as the experiment control because the current root `AGENTS.md` is 34,567 bytes, above the documented default 32 KiB combined project-document budget. Live execution must still prove that the effective setting and complete instruction chain were actually loaded identically across matched arms.

## Measurement and economics

Exact per-arm token attribution is mandatory. Credits use this priority: exact direct per-arm credit receipt; otherwise deterministic derivation from per-model usage segments and one official rate card selected prospectively for the actual account. Freeze A intentionally does not select between the two observed official credit surfaces because their Sol rows differ. `receipts/rate-card.json` therefore keeps `derivation_authorized = false`. Unresolved account applicability is `BLOCKED_MEASUREMENT`, not permission to estimate.

`terminal-result.schema.json` keeps token classes, credits, latency, rework, verification, protocol quality, Orchestrator materialization load, and final Git state separate. `scoring.py` implements only screening gates; it cannot turn screening output into production policy.

## Provider-free verification

Run `python evals/r027_efficiency/integrity.py` and `pytest tests/test_r027_efficiency_freeze.py`. `manifest.json` binds the Freeze A payload using a SHA-256 digest over the canonical path-to-Git-blob map, with Git blob IDs binding file bytes.

## Live stop boundary

Before the first scored arm, stop unless all live items are proven: exact Codex/client/runtime version and D077 relevance, exact per-arm usage attribution, account credit regime or direct credits, complete instruction loading, `agents.enabled=false`, no child creation, and an exclusive clean worktree/ref for the arm. A later material model/rate/runtime/accounting regime change stops the experiment; do not mix regimes or replace known scored observations.
