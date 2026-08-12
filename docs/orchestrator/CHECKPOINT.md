# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O035  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003 and T005 are `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

T006 remains `READY` and unchanged. It resumes immediately after T007 closes.

T007 is in focused R1 rework after remote review of executor HEAD `656c71e22f60ae8b235304179dc1d8fee4ec4031`.

## T007 — R1 REWORK

Task Contract:

`docs/tasks/T007-branch-hygiene-cleanup.md`

Active review directive:

`docs/reviews/T007-R1.md`

Reviewed evidence accepted so far:

- executor branch is exactly one commit ahead of T007 base `c30017ccfd6ab912321f10fe0baa9b5181787609`;
- only committed change is `handoffs/T007-executor-handoff.json`;
- 50 historical `DELETE` branches are absent remotely;
- `main` and `develop` were not moved;
- executor-controlled local cleanup evidence is present.

Remaining branch:

`eval/d032-agent-capability@eb20dc0fed2674190a82ef40aa0e02436c02ced4`

It has no PR, but comparison against `develop` shows only cancelled T004 implementation artifacts. Because T004 is terminal `CANCELLED_BY_HUMAN`, R1 resolves that branch as intentionally abandoned work and authorizes exact-SHA remote/local deletion.

The initial executor pass deleted this branch before fully resolving its missing PR association, then restored it at the exact original SHA. Final state was recovered safely, but the classify-before-delete procedural nonconformance MUST remain recorded in the final handoff.

## T006 — READY / PAUSED FOR T007

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

T006 semantics, D035 Core state and verification requirements remain unchanged. Do not start T006 until T007 is accepted/closed.

D036 remains after T006.

## Next Action

1. Re-launch/continue the Agente de IA Ejecutor on T007 using the canonical minimal prompt and the same Task Contract pointer.
2. Executor follows `docs/reviews/T007-R1.md`, deletes only the exact resolved T004 branch remotely and locally, prunes/verifies state, updates the handoff including the procedural nonconformance, commits/pushes, and returns status/path/branch/HEAD only.
3. ChatGPT reviews the new remote handoff and final branch state.
4. If accepted, integrate/close T007 and resume T006 unchanged.
5. Do not start D036 until T006 is accepted/integrated.

Canonical T007 launch prompt:

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Start from current develop and read AGENTS.md first.

Then load and execute the authoritative Task Contract:
docs/tasks/T007-branch-hygiene-cleanup.md

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T007-branch-hygiene-cleanup.md` and `docs/reviews/T007-R1.md` while T007 is active;
2. load `docs/BRANCHING.md` and `docs/BRANCH-CLEANUP.md` as needed;
3. inspect current remote branch state and the latest T007 handoff;
4. after T007 closes, return to the T006 contract and its D035/security verification context only;
5. do not reload T001–T005 implementation details absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not delete a branch at a SHA different from the persisted resolved-review SHA.
- Do not hide the T007 classify-before-delete procedural nonconformance.
- Do not modify product/Core/test semantics during T007.
- Do not start T006 implementation until T007 closes.
- Do not implement D036 inside T006 or T007.
- Do not add model-based verification gates.
- Do not declare the source product stable/release-ready.
