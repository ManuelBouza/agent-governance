# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O154  
Canonical-Branch: `develop`  
Current-Work-Unit: T036 D054 Phase-B oracle transition planning/conformance gate integrated; independent Executor Code Review & Verify is the next required action before D040 Phase-B may resume  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: Codex  
Active-Executor-Surface: ChatGPT desktop / Codex / native Windows

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- D042 requires canonical GitHub remote synchronization/freshness before the Executor loads `AGENTS.md` or persisted execution authority.
- D055 requires a Human-facing Executor Launch Profile before every Executor prompt; `docs/EXECUTOR-LAUNCH-PROFILES.md` carries the current Codex mapping and pointer-only prompt shape.
- D056 requires concise Human-visible progress notes around meaningful GitHub/remote operation phases.
- T034 is `ACCEPTED` and integrated.
- T035 is `ACCEPTED`; its implementation-time oracle revision `T035-D054-v1` remains the frozen historical baseline and T035 accepted evidence remains unchanged.
- During D040 Phase-B preparation, Orchestrator discovered that the T035 preserved-surface test projected T035's historical `Protocol-Version == 1.14.0` requirement as a live current-version assertion, which would make the separately authorized Phase-B protocol bump knowingly red.
- D040 forbids a knowingly red protocol-transition baseline; D052 requires persisted Orchestrator correction when an Orchestrator-owned oracle conflicts with controlling normative semantics.
- T036 `docs/tasks/T036-d054-phase-b-oracle-transition.md` was therefore created with Test-Authorship-Mode `orchestrator-conformance` and integrated through PR #204 at `cc4cb59b3979f6260890e94588f3cb071c9b9488`.
- T036 Oracle revision `T036-D054-ACTIVATION-TRANSITION-v1` changes only the temporal binding of the T035 preserved-protocol assertion: it now verifies the accepted T035 contract recorded `1.14.0` preservation during T035 instead of pinning the repository's future current protocol version. All other T035 oracle semantics and the CLI v1 exact-set assertion remain unchanged.
- T036 has **not** been accepted yet. Its next required gate is independent Executor Code Review & Verify plus persisted handoff evidence from current canonical `develop`.
- D040 Phase-B D054 routed-Core activation is BLOCKED pending T036 acceptance. The prior uncommitted activation preparation MUST NOT be treated as repository authority or reused from stale branch state; restart Phase-B from fresh canonical `develop` after T036 acceptance.
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
Oracle: T035-D054-v1 — FROZEN historical implementation-time baseline
Acceptance PR: #202
Accepted develop anchor: 218e279bc7be6efdffe9b30b183a05e888d3f99a
```

## T036 current identity

```text
Task: T036
Status: PLANNED / CONFORMANCE GATE INTEGRATED / VERIFICATION REQUIRED
Task Contract: docs/tasks/T036-d054-phase-b-oracle-transition.md
Test-Authorship-Mode: orchestrator-conformance
Oracle transition: T036-D054-ACTIVATION-TRANSITION-v1
Planning/oracle PR: #204
Integrated planning/oracle anchor: cc4cb59b3979f6260890e94588f3cb071c9b9488
Expected Executor verification branch: verify/t036-d054-phase-b-oracle-transition
Expected handoff: handoffs/T036-executor-handoff.json
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

1. Show the D055 launch profile for active Executor Codex.
2. Launch a `NEW` Executor session for T036 because this is a new Task Contract/work unit.
3. Use current canonical `develop` containing `cc4cb59b3979f6260890e94588f3cb071c9b9488` and send only the pointer-only prompt to `docs/tasks/T036-d054-phase-b-oracle-transition.md`, including D042 remote freshness.
4. Executor performs only T036-authorized independent Code Review & Verify and persists/pushes `handoffs/T036-executor-handoff.json` on `verify/t036-d054-phase-b-oracle-transition`.
5. ChatGPT Orchestrator then reviews the remote handoff/branch/evidence and performs T036 Converge/Accept.
6. Only after T036 acceptance may D040 Phase-B D054 routed-Core activation restart from a fresh branch based on then-current canonical `develop`.
7. Do not resume T021/T022 automatically.

## Next chat minimum load

Load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint.

Then follow `Next action`. Do not reconstruct the frontier from prior chat history or Project Memory.

## Do not

Do not omit D042 remote freshness from an Executor prompt; do not duplicate task semantics into the prompt; do not give routine CLI/API/shell commands to the Human; do not edit any T035 oracle semantics outside the exact T036-authorized temporal-binding transition; do not activate D054 routed Core semantics before T036 acceptance; do not reuse the stale pre-T036 activation branch as authority; do not use the polluted represented T035 Executor branch tip as accepted T035 identity; do not resume T021/T022 automatically; do not expose private chain-of-thought instead of D056 progress notes; and do not write directly to `main`/`develop`.
