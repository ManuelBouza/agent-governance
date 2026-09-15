# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O335  
Date: 2026-09-15  
Canonical-Branch: `develop`  
Current-Work-Unit: `T068 / ChatGPT Skill host materialization and qualification`  
State: T068_E5_KNOWN_GOOD_SHAPE_PROBE_AUTHORIZED  
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
T068-ChatGPT-Install-State: VERIFIED_INSTALLED_SIX_OF_SIX  
T068-ChatGPT-Qualification-State: BLOCKED_FAIL_CLOSED_DIAGNOSTIC_ACTIVE  
T068-Immediate-Unit: `E5 known-good-shape host packaging probe`  
Active-Executor: none  
T067-State: ACCEPTED_INTEGRATED_OPERATIONALLY_CLOSED  
T066-Stage5-State: NOT_STARTED  
ChatGPT-Empirical-Parity: NOT_ESTABLISHED  
Experimental-Human-Readability-Rule: ACTIVE_TRIAL_CHATGPT_ONLY  
Next-ChatGPT-Effort: MEDIUM  
Next-Execution-Shape: SINGLE_EXECUTION  
Next-Action: Generate one disposable `repository-change-control` host probe whose ZIP shape matches the known-good ChatGPT Skill control: a top-level `<skill-name>/` directory containing `SKILL.md` plus `agents/openai.yaml`. Change only the temporary Skill `name:` in SKILL.md; preserve all remaining canonical semantic text. Do not add `policy.allow_implicit_invocation`, icon metadata, products, or any runtime-enriched fields manually. Keep the probe untracked and outside canonical Skill directories. Human uploads the probe and records whether the host exposes it for explicit selection and/or natural-intent runtime activation. Do not advance to E6 or modify T066.  
Next-Chat-Minimum-Load: `docs/tasks/T068-chatgpt-skill-host-materialization-and-qualification.md`; `evals/t068_chatgpt_skill_host/qualification-result-2026-09-15.json`; this checkpoint; `tools/chatgpt_skill_package.py`; R031 only if a consequential OpenAI host claim needs refresh  
Do-Not-Load-Or-Do: Do not reopen T067; do not start/modify T066; do not relaunch E3; do not advance to E6; do not modify canonical Skill semantics/topology; do not relabel ChatGPT/Codex parity.

## Experimental Human-readable identifier rule

This remains an experimental ChatGPT Human-facing presentation rule only. ChatGPT should gloss opaque governance identifiers on first meaningful use in Human-visible prose. Do not propagate the gloss requirement to Codex, Executor prompts, machine-readable evidence, Task Contracts, handoffs, commands, branches, SHAs, filenames, or internal reasoning.

## Accepted evidence retained

E3 / Stage 6 remains accepted. E4 remains COMPLETE/VERIFIED from Human-visible ChatGPT Skills UI evidence showing the six canonical T068 Skills installed and no top-level `workspace-isolation` Skill.

E5 remains fail-closed. The durable result records 22 preserved scenarios, 0 PASS, 0 semantic FAIL, 6 `BLOCKED_UNAVAILABLE`, and 16 `NOT_RUN_INCONCLUSIVE`. This is host-surface evidence only and does not establish a semantic defect in the Skill packages.

## Comparative known-good evidence

Human supplied a forensic report from a similar project with a ChatGPT Skill known to auto-trigger by natural intent and to be runtime-enumerable. The known-good package pattern differs from the current T068 packager in two material ways:

1. the ZIP contains a top-level `<skill-name>/` directory rather than placing `SKILL.md` directly at archive root;
2. the source Skill includes `agents/openai.yaml` with only `interface.display_name` and `interface.short_description`.

The known-good runtime later exposes enriched metadata such as icons, product policy and `allow_implicit_invocation: true`, but those fields are not present in the canonical Git source. Therefore this diagnostic MUST NOT synthesize runtime-enriched policy fields manually.

The current T068 packager already normalizes regular files to mode `0644`, so unreadable `0600` ZIP entries are not the leading hypothesis.

The previous renamed-name probe remains disposable evidence but is diagnostically deprioritized because it retained the flat ZIP shape and omitted `agents/openai.yaml`; it could not isolate the now-observed packaging/registration differences.

## Authorized known-good-shape probe

Human `go` on 2026-09-15 authorizes exactly one reversible probe before any Stage 5 re-entry.

Source: `repository-change-control-skill/SKILL.md`.

Temporary probe identity:

`repository-change-control-t068-shape-probe-20260915`

Disposable source tree MUST be exactly:

```text
repository-change-control-t068-shape-probe-20260915/
├── SKILL.md
└── agents/
    └── openai.yaml
```

`SKILL.md` requirements:

- copy canonical `repository-change-control-skill/SKILL.md`;
- change only frontmatter `name: repository-change-control` to `name: repository-change-control-t068-shape-probe-20260915`;
- all other bytes/content remain identical.

`agents/openai.yaml` contents MUST be exactly:

```yaml
interface:
  display_name: "Repository Change Control T068 Shape Probe"
  short_description: "Resuelve rutas autorizadas de mutación de repositorios y falla cerrado ante estado ambiguo."
```

ZIP requirements:

- archive name: `repository-change-control-t068-shape-probe-20260915.zip`;
- archive entries exactly:
  - `repository-change-control-t068-shape-probe-20260915/SKILL.md`;
  - `repository-change-control-t068-shape-probe-20260915/agents/openai.yaml`;
- regular-file mode equivalent to `0644`;
- deterministic timestamps/order/compression are preferred;
- no extra files or directories need explicit ZIP directory entries;
- no canonical/tracked file modification;
- no commit or push.

Required mechanical evidence before Human upload:

- exact remote branch HEAD matches this checkpoint commit;
- canonical source file unchanged;
- SKILL.md delta is name-only;
- exact two-entry ZIP inventory;
- readable file modes;
- ZIP SHA-256;
- Git tracked state clean after generation.

## Host observation after upload

After Human upload, use a fresh ChatGPT chat and record independently:

1. whether the probe appears installed;
2. whether it appears/is selectable through the explicit Skill surface when typing `@`;
3. whether a natural repository-mutation request without naming the Skill causes observably Skill-specific behavior or runtime Skill exposure, if the host provides such exposure.

Do not infer hidden routing. A working shape probe supports narrow Stage 5 re-entry for host adapter/packaging; it does not itself qualify the six canonical Skills or alter D082 topology.

## Ordered remaining geometry

1. **E5 known-good-shape probe** — AUTHORIZED, reversible, disposable.
2. **Potential narrow Stage 5 host-adapter re-entry** — only if probe evidence supports it and Human/Orchestrator explicitly authorizes.
3. **E5 qualification retry** — blocked until a valid observable runtime path exists.
4. **E6** — blocked until E5 produces scorable evidence.

## Preserved boundaries

- D082 topology remains one Maintainer Skill with Orchestrator/Executor internal routes plus exactly five transverse Skills.
- `workspace-isolation` remains subordinate, never a seventh top-level Skill.
- Git remains canonical authority.
- Canonical Skill source bytes and semantics remain unchanged by this probe.
- T066 remains separate and unstarted.
- ChatGPT/Codex empirical parity remains `NOT_ESTABLISHED`.
