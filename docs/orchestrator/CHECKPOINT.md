# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O336  
Date: 2026-09-15  
Canonical-Branch: `develop`  
Current-Work-Unit: `T068 / ChatGPT Skill host materialization and qualification`  
State: T068_E5_SHAPE_PROBE_INSTALLED_BUT_NOT_RUNTIME_EXPOSED  
Chat-Closure: KEEP_CURRENT_CHAT  
Human-Objective: Materialize the adopted R029/D082 Skills in ChatGPT and qualify real host activation/routing  
T068-Task-Contract: `docs/tasks/T068-chatgpt-skill-host-materialization-and-qualification.md`  
T068-Research: `docs/research/R031-CHATGPT-SKILL-HOST-MATERIALIZATION.md`  
T068-Topic-Branch: `feat/t068-chatgpt-skill-host-activation`  
T068-Base: `develop@5bed8b952a3c552e3af0abfdbe07895864319696`  
T068-Candidate-Content-Anchor: `9707b41a1e0ac7f64c776318ca557bd3ceca263f`  
T068-Stage6-Implementation-Head: `b25a5a3e7ac91137a302cde4849c4b1262393b2d`  
T068-Stage6-Handoff-Head: `48852fff2dd0272836c9c814f65335bdc98fd035`  
T068-E5-Blocked-Head: `3ec70dcb1e92a09a7136e63a22e8dcaba036183f`  
T068-E5-Result: `evals/t068_chatgpt_skill_host/qualification-result-2026-09-15.json`  
T068-Execution-Shape: MULTI_EXECUTION  
T068-E4-State: VERIFIED_BY_HUMAN_VISIBLE_CHATGPT_SKILLS_UI  
T068-ChatGPT-Install-State: VERIFIED_INSTALLED_SIX_OF_SIX_PLUS_DISPOSABLE_PROBE  
T068-ChatGPT-Qualification-State: BLOCKED_FAIL_CLOSED_DIAGNOSTIC_ACTIVE  
T068-Immediate-Unit: `E5 native-creation-path diagnostic`  
Active-Executor: none  
T067-State: ACCEPTED_INTEGRATED_OPERATIONALLY_CLOSED  
T066-Stage5-State: NOT_STARTED  
ChatGPT-Empirical-Parity: NOT_ESTABLISHED  
Experimental-Human-Readability-Rule: ACTIVE_TRIAL_CHATGPT_ONLY  
Next-ChatGPT-Effort: MEDIUM  
Next-Execution-Shape: SINGLE_EXECUTION  
Next-Action: Do not change canonical Skills yet. The known-good-shape ZIP probe was accepted by ChatGPT and is visibly installed, but remained absent from the observable runtime Skill resource catalog and its resources were unreadable. Therefore top-level `<skill-name>/` ZIP shape plus source `agents/openai.yaml` is insufficient by itself. Run one controlled ChatGPT-native creation-path diagnostic using the platform `skill-creator` / `Create with chat` flow to create an equivalent temporary `repository-change-control` probe from the same semantic instructions. Observe whether the natively created probe becomes runtime-enumerable/loadable in a fresh chat. Preserve fail-closed scoring, do not advance to E6, and do not modify T066.  
Next-Chat-Minimum-Load: `docs/tasks/T068-chatgpt-skill-host-materialization-and-qualification.md`; `evals/t068_chatgpt_skill_host/qualification-result-2026-09-15.json`; this checkpoint; R031 only if a consequential host claim needs refresh  
Do-Not-Load-Or-Do: Do not reopen T067; do not start/modify T066; do not relaunch E3; do not advance to E6; do not modify canonical Skill semantics/topology; do not relabel ChatGPT/Codex parity.

## Experimental Human-readable identifier rule

This remains an experimental ChatGPT Human-facing presentation rule only. ChatGPT should gloss opaque governance identifiers on first meaningful use in Human-visible prose. Do not propagate the gloss requirement to Codex, Executor prompts, machine-readable evidence, Task Contracts, handoffs, commands, branches, SHAs, filenames, or internal reasoning.

## Accepted evidence retained

E3 / Stage 6 remains accepted. E4 remains COMPLETE/VERIFIED from Human-visible ChatGPT Skills UI evidence showing the six canonical T068 Skills installed and no top-level `workspace-isolation` Skill.

E5 remains fail-closed. The durable result records 22 preserved scenarios, 0 PASS, 0 semantic FAIL, 6 `BLOCKED_UNAVAILABLE`, and 16 `NOT_RUN_INCONCLUSIVE`. This is host-surface evidence only and does not establish a semantic defect in the Skill packages.

## Known-good-shape probe generation evidence

Disposable probe:

`repository-change-control-t068-shape-probe-20260915`

Codex returned:

- `STATUS: COMPLETED`;
- ZIP SHA-256 `5536f77f4644edae3266f4daae1adf33c103abd991c1f92737e76183882673af`;
- `SKILL_CONTENT_DELTA: NAME_ONLY`;
- `ZIP_INVENTORY: EXACT_TWO_ENTRIES`;
- `FILE_MODES: READABLE_0644_EQUIVALENT`;
- `GIT_TRACKED_STATE: CLEAN`.

The ZIP contained exactly:

- `repository-change-control-t068-shape-probe-20260915/SKILL.md`;
- `repository-change-control-t068-shape-probe-20260915/agents/openai.yaml`.

No canonical/tracked repository file was changed by probe generation.

## Human-visible installation evidence

On 2026-09-15 the Human supplied a ChatGPT Skills UI screenshot. The probe is visibly present under both `Instaladas` and `Creadas por mí` with the expected display metadata. The same screenshot also shows the canonical Agent Governance Skills still installed.

This proves the host accepted and indexed enough of the package metadata to render the probe in the Skills management UI. It does not prove runtime availability.

## Runtime observation for shape probe

A fresh ChatGPT execution reported:

- `RUNTIME_SKILL_VISIBLE: NO`;
- `EXPLICIT_AT_VISIBLE: UNKNOWN`;
- `EXPLICIT_AT_SELECTABLE: UNKNOWN`;
- `SKILL_RESOURCES_READABLE: NO`;
- `NATURAL_INTENT_TEST_RUN: NO`.

The observable runtime Skill/plugin resource catalog exposed 36 resources but did not expose `repository-change-control-t068-shape-probe-20260915`. An explicit search in the available plugin-management surface also did not return the probe as a runtime resource. The execution did not infer hidden routing.

Therefore the following hypothesis is now rejected as sufficient:

`top-level <skill-name>/ ZIP directory + agents/openai.yaml + readable 0644 files => runtime Skill availability`

Those properties may still be necessary, but they are not sufficient in this observed ChatGPT host state.

## Updated diagnostic hypothesis

Current evidence separates three planes:

1. **UI installation/metadata plane:** working for both canonical Skills and the shape probe.
2. **Package mechanical plane:** accepted for the shape probe and previously verified for canonical packages.
3. **Runtime registration/loading plane:** not established for Agent Governance Skills or the shape probe.

The remaining high-value variable is the ChatGPT-native creation/promotion path itself. Current OpenAI documentation states that eligible accounts include the `skill-creator` Skill and that asking ChatGPT to create or modify a Skill automatically uses it; Skills can also be created through `Create with chat`, the editor, or upload. A native-creation control can therefore test whether host-side creation performs registration/enrichment not reproduced by direct ZIP upload.

## Ordered remaining geometry

1. **E5 native-creation-path diagnostic** — next, one temporary probe only.
2. **Potential narrow Stage 5 host-adapter re-entry** — only if diagnostic evidence identifies a reproducible repository-side representation/promotion requirement.
3. **E5 qualification retry** — blocked until a valid observable runtime path exists.
4. **E6** — blocked until E5 produces scorable evidence.

## Preserved boundaries

- D082 topology remains one Maintainer Skill with Orchestrator/Executor internal routes plus exactly five transverse Skills.
- `workspace-isolation` remains subordinate, never a seventh top-level Skill.
- Git remains canonical authority.
- Canonical Skill source bytes and semantics remain unchanged by diagnostics.
- T066 remains separate and unstarted.
- ChatGPT/Codex empirical parity remains `NOT_ESTABLISHED`.
