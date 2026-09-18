# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O341  
Date: 2026-09-18  
Canonical-Branch: `develop`  
Current-Work-Unit: `R032 / Codex model-effort selection classifier`  
State: R032_DECIDED_D083_ACCEPTED_T069_REVALIDATION_NEXT  
Chat-Closure: KEEP_CURRENT_CHAT  
Human-Objective: Define a proportionate Codex model/reasoning selection policy from execution determinism, technical branching, verification strength and concrete risk rather than defaulting mechanically to Sol/Medium  
R032-Research: `docs/research/R032-CODEX-MODEL-EFFORT-SELECTION.md`  
R032-Research-State: COMPLETE  
R032-Decision-State: DECIDED  
R032-Branch: `docs/r032-codex-model-effort-selection`  
R032-Research-Commit: `ebcb7e07035e0bf7b65a77712d8b0f119dad13c7`  
R032-Traceability-Commit: `3bcf5b1b4b0ea9de27b74c227839ccc4edbe9dd7`  
D083-Proposal: `docs/decisions/D083-codex-model-effort-selection-classifier.md`  
D083-State: ACCEPTED  
D083-Proposal-Commit: `d0e6a06862eabbe2163e3894e9cde056c4db961a`  
Active-Executor: none  
T069-State: PAUSED_BEFORE_STAGE6_PENDING_POST_D083_REVALIDATION  
T069-Branch: `feat/t069-git-backed-skill-loading@24d5a4fc0fd5a307ba0b7eb4b1428fa82de53337`  
T068-State: DEFERRED_UNTIL_PERSONAL_PLUS_NATIVE_SKILLS_AVAILABLE  
T068-Branch: `feat/t068-chatgpt-skill-host-activation@d9ead79ce06ee693b8ed315d1a209370f0270779`  
T066-Stage5-State: NOT_STARTED  
Next-ChatGPT-Effort: MEDIUM  
Next-Action: Revalidate current T069 remote branch, Task Contract, Stage 5 candidate/anchor and launch authority against current Git state. If still valid, classify the Stage 6 launch under accepted D083 and present the Human launch card/prompt. Do not launch automatically.  
Next-Chat-Minimum-Load: this checkpoint; `docs/decisions/D083-codex-model-effort-selection-classifier.md`; `docs/EXECUTOR-LAUNCH-PROFILES.md`; T069 Task Contract and current T069 branch/checkpoint only for revalidation  
Do-Not-Load-Or-Do: Do not resume T068; do not start/modify T066; do not launch T069 Stage 6 automatically; do not treat T063 as qualification of root routing; do not adopt Astra as default; do not use higher model/effort to cross an authority boundary.  

## Research conclusion

R032 is complete analytical evidence and is now represented in the canonical research registry. It confirms D055's minimum-sufficient-compute principle and proposes a more explicit classifier with four steps after the authority gate:

```text
authority complete?
    -> execution determinism
    -> technical branching
    -> verification strength
    -> concrete risk modifiers
    -> choose model capability
    -> choose reasoning effort independently
    -> verify and escalate only the deficient axis
```

The proposed conservative Codex mapping is:

- Luna/Low for read-only or repetitive high-determinism work with strong postconditions;
- Terra/Low for narrow tracked mutation with high determinism, low branching and strong deterministic verification;
- Terra/Medium for bounded local implementation/refactor with low-to-medium branching;
- Sol/Medium for ordinary multi-file implementation/rework when the task is not clearly eligible for downshift;
- Sol/High for high branching, weak verification, non-local diagnosis or serious concrete risk modifiers;
- Astra or stronger current tier only for concrete capability insufficiency, not as a default.

This mapping is accepted by D083 and now controls Codex root launch classification together with D055.

## D057 traceability status

R032 is now `COMPLETE / DECIDED` and D083 is the accepted decision authority. The research registry and Codex adapter guidance have been updated consistently.

## T069 interaction

T069 Stage 6 remains paused until a fresh Git revalidation is completed. D083 suggests `Terra / Low` if the current Task Contract still presents high determinism, low technical branching, strong deterministic verification, bounded repair authority and fail-closed semantic re-entry. Revalidation, not this remembered classification, controls the actual launch card.
