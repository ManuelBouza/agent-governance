# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O153  
Canonical-Branch: `develop`  
Current-Work-Unit: chat closed after T035 acceptance; D054 Phase-B routed-Core activation is the next eligible Orchestrator work unit if the Human continues  
Chat-Closure: NEW_CHAT_RECOMMENDED  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- D042 requires canonical GitHub remote synchronization/freshness before the Executor loads `AGENTS.md` or persisted execution authority.
- D055 requires a Human-facing Executor Launch Profile before every Executor prompt; `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current Codex mapping and pointer-only prompt shape.
- D056 requires concise Human-visible progress notes around meaningful GitHub/remote operation phases.
- T034 is `ACCEPTED` and integrated.
- T035 oracle `T035-D054-v1` is integrated/frozen on canonical `develop` through commit `3df2b4a91c94c99c160477ed031a37132070b228`.
- T035 Executor result was submitted as `DONE` at `7c90ba89644d6d4d25d92ba30a96bfd25a6253d5` with handoff `handoffs/T035-executor-handoff.json`.
- T035 implementation was independently reviewed by ChatGPT Orchestrator, integrated through PR #201 at `29bc0aacb80bc8adb19072a5634d4fed715e3779`, and accepted in `docs/reviews/T035-R1.md`.
- T035 is `ACCEPTED`; accepted evidence includes focused suite `59 passed`, full native-Windows deterministic suite `355 passed in 50.88s`, Ruff check/format PASS, `git diff --check` PASS, no Markdown/oracle drift and no unresolved Executor Code Review & Verify findings.
- T035 acceptance Markdown was integrated through PR #202 at `218e279bc7be6efdffe9b30b183a05e888d3f99a`.
- D040 Phase-B D054 routed-Core activation is eligible as a separate Orchestrator-owned Markdown work unit. It has **not** started.
- T021/T022 remain paused and MUST NOT auto-resume.

## Mandatory Executor prompt transport invariant

Every prompt sent to the active Executor remains pointer-only and includes D042 freshness.

Canonical shape:

```text
Operate as the Agente de IA Ejecutor for <repository>.

Synchronize with GitHub and establish a safe current local baseline from the canonical remote state before loading repository instructions or execution authority, per D042/RB001. Do not discard unrepresented local work.

Use <canonical/base or represented topic branch as applicable>.

Load current repository instructions, then execute exactly:
<persisted authority path>

Return only the output required by that persisted authority.
```

Do not carry task requirements, acceptance criteria, implementation instructions, copied contract text, or routine Git/CLI/uv/PowerShell commands in the prompt. Exact adapter mechanics belong to the Executor under D054. `CONTINUE` preserves chat context only; it never exempts D042 remote synchronization/freshness.

## D055 launch invariant

Before every Executor prompt, ChatGPT Orchestrator shows:

```text
Executor: <active concrete executor>
Session: NEW | CONTINUE
Model: <exact recommended current model>
Effort: <exact recommended current effort>
Rationale: <one concise sentence>
```

Current Codex mapping:

```text
read-only/repetitive observation -> GPT-5.6 Luna / Low
narrow mechanical implementation -> GPT-5.6 Terra / Low
standard AG implementation/rework -> GPT-5.6 Sol / Medium
complex/high-risk technical work  -> GPT-5.6 Sol / High
exceptional long-horizon work     -> GPT-5.6 Sol / highest mode only when justified
```

## T035 accepted identity

```text
Task: T035
Status: ACCEPTED
Submitted Executor HEAD: 7c90ba89644d6d4d25d92ba30a96bfd25a6253d5
Implementation anchor: 05130a1993c04e489ff69d4c60c8de5ad5f09685
Implementation PR: #201
Integrated implementation: 29bc0aacb80bc8adb19072a5634d4fed715e3779
Handoff: handoffs/T035-executor-handoff.json
Acceptance review: docs/reviews/T035-R1.md
Oracle: T035-D054-v1 — FROZEN / unchanged
Acceptance PR: #202
Accepted develop anchor: 218e279bc7be6efdffe9b30b183a05e888d3f99a
```

## Orchestrator branch-mutation containment

During T035 convergence, ChatGPT Orchestrator mistakenly created `docs/reviews/T035-R1.md` on the represented Executor branch after the submitted Executor HEAD. This was an Orchestrator ownership/workflow error, not an Executor defect.

Containment:

- no direct write to `develop`/`main` occurred;
- the submitted Executor HEAD `7c90ba89644d6d4d25d92ba30a96bfd25a6253d5` remained intact as an immutable commit;
- PR #201 integrated only an integration branch created exactly from that submitted HEAD;
- the accidental post-submission Markdown commit on `feat/t035-runbook-operation-resolution-readiness` was excluded from acceptance/integration;
- history was not rewritten or force-pushed;
- durable acceptance Markdown was integrated separately through PR #202.

Do not use the current tip of the represented Executor branch as T035 accepted identity. Use the submitted Executor HEAD and integrated commits recorded above.

## Next action

On the next Human-authorized chat:

1. bootstrap from current GitHub `develop`;
2. read current `AGENTS.md` and this checkpoint before loading deeper history;
3. because the next eligible work unit is D040 Phase-B D054 routed-Core activation, load only D040, D054 and the routed Core modules required by their own sequencing/ownership rules;
4. perform the Orchestrator-owned Explore/Specify/Design/Plan/Trace and Markdown-only activation workflow from a fresh topic branch;
5. do not launch an Executor merely for Markdown-only activation unless a new executable requirement emerges;
6. do not resume T021/T022 automatically.

## Next chat minimum load

Load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint.

Then follow `Next action`. Do not reconstruct the frontier from prior chat history or Project Memory.

## Do not

Do not omit D042 remote freshness from an Executor prompt; do not duplicate task semantics into the prompt; do not give routine CLI/API/shell commands to the Human; do not edit or weaken frozen `T035-D054-v1`; do not use the polluted represented Executor branch tip as accepted T035 identity; do not activate D054 routed Core semantics without a separate Orchestrator work unit; do not resume T021/T022 automatically; do not expose private chain-of-thought instead of D056 progress notes; and do not write directly to `main`/`develop`.
