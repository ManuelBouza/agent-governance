# Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O308  
Date: 2026-09-13  
Canonical-Branch: `develop`  
Predecessor-Work-Unit: R029 — incremental Skill-architecture evaluation  
Predecessor-Objective-Status: OBJECTIVE_COMPLETE  
State: HANDOFF_READY  
Chat-Closure: HANDOFF_READY  
Human-Selected-Next-Objective: Formalize and apply execution-flow refinement so trace/decomposition subtasks are not automatically execution units, related subtasks are grouped into one execution when no material gate requires separation, and Human-requested in-cycle changes may be applied locally as explicitly experimental adaptations without breaking the active task flow; at cycle close, experimental adaptations are evaluated against the objective/acceptance evidence and only successful ones may be promoted through an explicit normative decision and later materialization.  
Bootstrap-Anchor-HEAD: `00a51d551356c59738097c36b19d11377f9ff719`  
Bootstrap-Expected-HEAD-Semantics: the exact expected canonical `develop` HEAD is supplied by the predecessor transport prompt after the HANDOFF_READY checkpoint is integrated; do not compare the successor against this checkpoint's own pre-integration anchor as though it were the final canonical HEAD.  
Next-Chat-Minimum-Load: `AGENTS.md`; `docs/orchestrator/CHECKPOINT.md`; `docs/decisions/D067-objective-scoped-orchestrator-chat-lifecycle.md`; `docs/decisions/D080-orchestrator-execution-shape-control.md`; load R029 artifacts only if a concrete conflict requires them  
Next-ChatGPT-Effort: HIGH  
Next-Execution-Shape: SINGLE_EXECUTION  
Active-Executor: none  
Executor-Launch-State: NOT_AUTHORIZED  
Prior-Unselected-T066-Scientific-Branch: `test/r027-chatgpt-codex-efficiency-v1`  
Prior-Unselected-T066-Scientific-Branch-State: PREEXISTING_DIVERGED_UNCONSUMED_CONFLICT

## Completed predecessor objective

R029 is complete. The Human Owner accepted its candidate topology only as the basis for a possible later normative architecture decision. R029 remains `Decision-State: EVALUATING`; no root `AGENTS.md` rewrite, transverse Skill implementation, Executor/provider/model call, scored observation or T066 mutation was authorized.

## Successor objective semantics

The successor must distinguish three levels that must not be conflated:

```text
subtask / trace unit
    != execution unit
    != normative decision
```

### 1. Execution grouping

Multiple consecutive subtasks SHOULD normally remain inside one execution when they share the same authority, context and invariants and no earlier result must become a controlling prerequisite through a material freeze, verification, revalidation, Human acceptance, distinct failure-domain boundary or durable-resumption gate.

Do not manufacture execution boundaries merely because trace IDs or analytical subtasks exist. A materially small task may still require multiple executions when a real gate exists; a task spanning many files/subtasks may remain one execution when it is one coherent bounded unit.

### 2. In-cycle experimental adaptation

If the Human Owner requests a change while an authorized execution/cycle is in progress, do not automatically terminate the objective, create a new chat, or promote the change into policy.

When the requested change is compatible with the active objective and authority envelope, it may be applied locally as an explicit `EXPERIMENTAL_IN_CYCLE` adaptation. The adaptation must be durably traceable enough to identify:

- what changed and why;
- which execution/cycle it affected;
- which prior assumption/rule remained unchanged versus locally varied;
- what evidence will determine whether the adaptation helped, harmed or remained inconclusive;
- that the adaptation is not yet normative authority.

A change that materially alters the Human objective, authority/ownership, accepted specification/Design, safety envelope, or controlling acceptance meaning remains a stop/re-entry/new-objective boundary; `EXPERIMENTAL_IN_CYCLE` must not be used to bypass those gates.

### 3. End-of-cycle promotion gate

At the end of the relevant cycle, evaluate each experimental adaptation against the controlling objective, acceptance criteria and observed evidence.

```text
experimental adaptation
    -> evidence at cycle close
    -> retain / revise / reject / recommend promotion
    -> explicit Human/normative decision if promotion is desired
    -> materialize only after that decision authorizes it
```

Successful local experimentation does not automatically become product policy. Normative promotion must remain explicit and durable under the applicable research/decision traceability rules.

## Successor bootstrap verification

Before material work, the successor MUST:

1. fetch current `develop` HEAD from GitHub;
2. read current `AGENTS.md` from that `develop`;
3. read current `docs/orchestrator/CHECKPOINT.md`;
4. compare observed `develop` HEAD and checkpoint sequence with the exact expected values carried by the predecessor successor-bootstrap prompt;
5. verify that this checkpoint remains `HANDOFF_READY` for the same Human-selected objective;
6. read D067 and D080;
7. load no additional history unless the checkpoint or a concrete conflict requires it;
8. if a material mismatch exists, stop as `BOOTSTRAP_MISMATCH` rather than silently reconciling it.

## Authorized successor scope

The successor may formalize the execution-grouping and in-cycle experimental-adaptation rule and integrate the smallest coherent documentation/decision changes needed to make it durable.

It must preserve the distinction between execution geometry and ChatGPT reasoning effort. It must not introduce minute/token/time budgets.

It may apply the resulting rule prospectively to future planned work, including T066 Stage 5 geometry, but MUST NOT start T066 Stage 5 materialization, create its scientific branch, launch Executor/Codex, consume provider/model calls or mutate the preexisting unselected T066 branch unless separately authorized.

## Do Not Do In This Predecessor Chat

- Do not execute the successor objective here.
- Do not modify D080 or other normative policy here beyond this successor bootstrap.
- Do not start T066 work.
- Do not launch an Executor or consume provider/model calls.
- Do not treat `EXPERIMENTAL_IN_CYCLE` as authority to bypass specification, ownership, safety, Human or acceptance gates.
