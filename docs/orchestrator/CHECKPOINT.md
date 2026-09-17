# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O339  
Date: 2026-09-17  
Canonical-Branch: `develop`  
Current-Work-Unit: `R032 / Codex model-effort selection classifier`  
State: R032_COMPLETE_D083_PROPOSED_TRACEABILITY_GATE_OPEN  
Chat-Closure: KEEP_CURRENT_CHAT  
Human-Objective: Define a proportionate Codex model/reasoning selection policy from execution determinism, technical branching, verification strength and concrete risk rather than defaulting mechanically to Sol/Medium  
R032-Research: `docs/research/R032-CODEX-MODEL-EFFORT-SELECTION.md`  
R032-Research-State: COMPLETE  
R032-Decision-State: EVALUATING  
R032-Branch: `docs/r032-codex-model-effort-selection`  
R032-Research-Commit: `ebcb7e07035e0bf7b65a77712d8b0f119dad13c7`  
D083-Proposal: `docs/decisions/D083-codex-model-effort-selection-classifier.md`  
D083-State: PROPOSED_NOT_ACCEPTED  
D083-Proposal-Commit: `d0e6a06862eabbe2163e3894e9cde056c4db961a`  
Active-Executor: none  
T069-State: PAUSED_BEFORE_STAGE6_FOR_R032_POLICY_REVIEW  
T069-Branch: `feat/t069-git-backed-skill-loading@24d5a4fc0fd5a307ba0b7eb4b1428fa82de53337`  
T068-State: DEFERRED_UNTIL_PERSONAL_PLUS_NATIVE_SKILLS_AVAILABLE  
T068-Branch: `feat/t068-chatgpt-skill-host-activation@d9ead79ce06ee693b8ed315d1a209370f0270779`  
T066-Stage5-State: NOT_STARTED  
Next-ChatGPT-Effort: MEDIUM  
Next-Action: Complete the D057 traceability gate by adding R032 to `docs/RESEARCH-TRACEABILITY.md`. Then present D083 for explicit Human acceptance. Do not modify `docs/EXECUTOR-LAUNCH-PROFILES.md`, relabel R032 as DECIDED, or resume T069 Stage 6 until that acceptance gate is satisfied.  
Next-Chat-Minimum-Load: this checkpoint; `docs/research/R032-CODEX-MODEL-EFFORT-SELECTION.md`; `docs/decisions/D083-codex-model-effort-selection-classifier.md`; `docs/RESEARCH-TRACEABILITY.md`; D055 only if resolving a concrete conflict  
Do-Not-Load-Or-Do: Do not resume T068; do not start/modify T066; do not launch T069 Stage 6; do not treat T063 as qualification of the proposed root-routing policy; do not adopt Astra as default; do not use higher model/effort to cross an authority boundary.

## Research conclusion

R032 is complete analytical evidence. It confirms D055's minimum-sufficient-compute principle and proposes a more explicit classifier with four steps after the authority gate:

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

This mapping is a proposal, not controlling policy, until D083 is accepted.

## D057 traceability gate

R032 currently exists durably in Git with required metadata, and D083 exists only as a proposed decision. The remaining gate is representation in the canonical research registry. Until that is complete:

- R032 remains `COMPLETE / EVALUATING`;
- D083 remains `PROPOSED`;
- D055 and the existing `docs/EXECUTOR-LAUNCH-PROFILES.md` remain controlling unchanged;
- no active Executor launch may rely on D083.

## T069 interaction

T069 Stage 6 remains paused before Human launch. If D083 is later accepted, T069 must be revalidated against its then-current remote branch/authority before applying the new classifier. The current research hypothesis is that T069 fits `Terra / Low`, with escalation to `Terra / Medium` only for non-trivial in-contract diagnosis; semantic or authority conflict remains an Orchestrator re-entry condition rather than a compute-escalation problem.
