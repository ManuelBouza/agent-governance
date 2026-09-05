# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O203  
Canonical-Branch: `develop`  
Current-Work-Unit: T055 child-observability qualification is accepted/integrated with formal outcome `PARTIAL_OBSERVABILITY`; R008 is `DEFERRED`; R007 remains `DEFERRED`; no routing successor is authorized  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: none

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling. Core protocol remains `1.15.0`.
- D057 research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md`.
- Canonical research ledger: `docs/RESEARCH-TRACEABILITY.md`.
- T050 remains `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- D055 remains unchanged as the global Human-facing Executor launch-profile policy.
- T054 remains accepted as an execution with frozen pilot outcome `NOT_QUALIFIED`; do not rerun it unchanged.

## T055 final state

T055 is **ACCEPTED as an execution** with frozen qualification decision **`PARTIAL_OBSERVABILITY`**.

Authoritative records:

- Task Contract: `docs/tasks/T055-codex-child-observability-qualification.md`;
- final review: `docs/reviews/T055-R1.md`;
- executor handoff: `handoffs/T055-executor-handoff.json`;
- telemetry: `handoffs/T055-child-observability-telemetry.json`;
- submitted Executor HEAD: `71cd53d4a83a300d6f741aade627a7ee2cc99a67`;
- evidence PR: `#280`;
- integrated evidence commit: `55758864fa68a953637e0203d52a6d994ed8e045`.

### Installed host

```text
Codex CLI:      0.149.0
App Server:     0.149.0
Transport:      stdio / JSON-RPC 2.0
Authentication: chatgpt category
Python SDK:     not used
```

The installed host was older than R008's 0.153.4 reference. T055 did not globally upgrade it. Native generated 0.149.0 schemas/help exposed the fields used by the qualification.

### T055 positive observability evidence

One real multi-agent child was spawned and uniquely correlated to its instrumented parent.

Requested child profile:

```text
model:            gpt-5.6-terra
reasoning effort: low
fork_turns:       none
```

Supported child thread state, read without model/reasoning overrides, reported:

```text
model provider:   openai
model:            gpt-5.6-terra
reasoning effort: low
```

Therefore requested-vs-resolved profile observation passed. This remains configured/persisted thread state, not provider-served per-turn identity.

Stable `sourceKinds` enumeration did not return the matching direct child. Deterministic parent/child correlation required the documented experimental `thread/list parentThreadId` filter. This experimental dependency is acceptable only as an explicitly version-pinned qualification dependency; it is not the reason T055 remained partial.

Supported `thread/tokenUsage/updated` telemetry was attributable to the exact child thread and turn:

```text
total tokens:            22577
input tokens:            22562
cached input tokens:     0
cache-write tokens:      0
output tokens:           15
reasoning output tokens: 0
model context window:    258400
estimated:               false
```

Supported child-turn duration was `3743 ms`.

The installed schema exposed `model/rerouted`; no reroute was observed. No authoritative backend-served model/reasoning receipt was exposed, and T055 correctly left that identity unverified.

### T055 blocker — child sandbox receipt

The instrumented parent had a supported `readOnly` sandbox receipt.

The real child had the supported receipt:

```text
workspaceWrite
writableRoots: []
networkAccess: false
excludeTmpdirEnvVar: false
excludeSlashTmp: false
```

Direct per-spawn sandbox override was not supported by the exercised spawn surface.

AC-T055-6 therefore failed. Empty writable roots are not sufficient to infer the contract's required non-write envelope because the supported receipt remains `workspaceWrite` and temporary write surfaces are not excluded.

This single missing mandatory measurement/safety gate forces `PARTIAL_OBSERVABILITY` under the frozen Task Contract.

### Acceptance-criteria result

```text
AC-T055-1   PASS
AC-T055-2   PASS
AC-T055-3   PASS_WITH_EXPERIMENTAL_DISCOVERY
AC-T055-4   PASS
AC-T055-5   PASS
AC-T055-6   FAIL
AC-T055-7   PASS
AC-T055-8   PASS
AC-T055-9   PASS
AC-T055-10  PASS
AC-T055-11  PASS
```

The Executor branch changed only the two authorized non-Markdown evidence files. No product code, Markdown, repository dependency, Governance Core, D055, routing policy, global Codex configuration or persistent agent catalog changed.

## Research dispositions

### R006 — persistent Executor coordinator

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Decision-Ref: none
```

No global D055 persistence-session change is adopted.

### R007 — adaptive subagent compute routing

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Evaluation: T054 accepted / NOT_QUALIFIED
Decision-Ref: none
```

T055 does not reactivate R007. A corrected routing pilot remains unauthorized because the measurement/safety substrate did not fully qualify.

### R008 — Codex child observability surface

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Evaluation: T055 accepted / PARTIAL_OBSERVABILITY
Decision-Ref: none
```

T055 confirmed that supported child profile state, child/turn token usage and duration are materially better than T054's parent-facing surface. However, the required non-write child sandbox receipt was not available on the exercised installed 0.149.0 host.

Reconsider R008 only when a supported installed Codex surface can demonstrate an unambiguous non-write sandbox receipt for a real spawned child without private persistence, product dependency changes or global configuration mutation. Experimental relationship discovery may remain acceptable if explicit and version-pinned and all other gates pass.

## Next action

1. Do not rerun T055 unchanged on the same installed Codex 0.149.0 surface.
2. Do not reactivate R007 and do not specify a corrected routing pilot yet.
3. If adaptive-routing work is to continue, ChatGPT Orchestrator should open a new D057-tracked research item (`R009`) focused narrowly on **current Codex child sandbox inheritance/override semantics**.
4. R009 should use current official OpenAI documentation and the official `openai/codex` repository to determine whether a materially newer supported stable/current surface than the exercised 0.149.0 host can:
   - cause a real collaboration child to retain/receive an unambiguous non-write/read-only sandbox;
   - expose that child sandbox through a supported receipt;
   - support direct per-spawn sandbox control or a documented safe inheritance mechanism;
   - do so without global configuration mutation or private persistence scraping.
5. Only if R009 finds a materially changed supported surface should the Orchestrator specify a narrow successor observability qualification (new Task Contract, not a T055 rerun) pinned to that surface.
6. Only after that qualification passes may R007 return to `EVALUATING` and a corrected adaptive-routing Task Contract be specified.
7. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then follow `Next action`. Load `docs/reviews/T055-R1.md` and R008 only if exact predecessor evidence is needed. Load no additional project history unless a concrete conflict requires it.

## Do not

Do not treat T055 `PARTIAL_OBSERVABILITY` as a failed execution; the execution is accepted and the qualification result is partial. Do not infer `readOnly` from empty `writableRoots`. Do not claim configured `Thread.model` / `reasoningEffort` prove backend-served identity. Do not estimate child tokens. Do not use private SQLite/JSONL to upgrade the result. Do not globally upgrade Codex merely to make the experiment pass. Do not change D055, persistence policy, consumer policy or global child-routing policy. Do not reactivate R007 without a persisted D057 transition after a passing measurement qualification. Do not rerun MG1-v12 or launch V13.