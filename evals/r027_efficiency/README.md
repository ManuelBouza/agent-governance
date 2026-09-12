# T066 Freeze A — R027/R028 Lean Executor screening

State: `PROVIDER_FREE_FREEZE_A`  
Task: `T066`  
Scope: `SCREENING_ONLY`  
Frozen base: `develop@6d4a698832cf08bded0351b0046fe5b2bf38b1c0`  
Scientific branch: `test/r027-chatgpt-codex-efficiency-v1`  
Scored provider/model calls in Freeze A: `0`

This directory is the provider-free Stage 5 control package required by T066 v2 and D079. It freezes nine matched pairs, eighteen maximum scored arms, D052 acceptance oracles, deterministic order/isolation, the common L0→L4 verification contract, scoring, exact-use accounting requirements, and the live-preflight blockers that must be cleared before any scored arm.

Freeze A does **not** authorize a Codex launch. D068 remains the production ownership policy. A scored launch requires separate Human authorization plus the live host/account preflight represented in `launch-envelope.json` and `receipts/`.
