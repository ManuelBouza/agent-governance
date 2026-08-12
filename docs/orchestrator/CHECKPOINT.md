# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O038  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

T007 branch-hygiene implementation was accepted by `docs/reviews/T007-R2.md` and integrated through PR #54. The historical branch backlog is resolved. Post-integration retirement of the temporary T007 and follow-up policy branches remains the only closure work before T006 resumes.

T006 remains `READY` and unchanged. After post-integration branch retirement is verified, resume T006 exactly as already contracted.

## Branch lifecycle hardening

PR #58 introduces the explicit merged-branch freeze invariant in `docs/BRANCHING.md` and `docs/BRANCH-CLEANUP.md`.

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

Once a topic PR is merged, its source branch MUST receive no additional commits. Any post-merge branch advancement is a workflow nonconformance and becomes `REVIEW`; follow-up work must be recovered/persisted through a fresh branch from the current authorized base before the original merged branch can be retired.

This policy closes the failure mode exposed during T007 closure, when `docs/t007-post-integration` received new Markdown commits after PR #55 had already merged. Those commits were later recovered through a fresh branch/PR (#56). Do not reuse a merged branch again, including for closely related follow-up Markdown or checkpoint work.

## T006 — READY

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Expected executor branch:

`test/security-verification-contract`

Expected handoff:

`handoffs/T006-executor-handoff.json`

T006 semantics, D035 Core state and deterministic verification requirements remain unchanged. D036 remains after T006 and MUST NOT be folded into it.

## T007 closure state

Accepted review:

`docs/reviews/T007-R2.md`

Integrated handoff:

`handoffs/T007-executor-handoff.json`

Canonical delegated branch retirement is defined by `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` and `docs/BRANCH-CLEANUP.md`.

The cleanup prompt accepts exactly one durable target:

- `TASK <task-id>` for Task-Contract-governed work;
- `PR <number>` for integrated changes without a Task ID.

Do not send branch lists or deletion decisions in chat. The executor derives candidates and deletion safety from current Git/GitHub state and merged PR evidence.

Preserve the T007 procedural audit: the initial pass deleted `eval/d032-agent-capability` before fully resolving its missing PR association, restored it at the exact original SHA, and the persisted R1 disposition later authorized final exact-SHA deletion as cancelled T004 work.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.
- T007-R1 review preparation: accidental temporary non-Markdown `noop` file on `docs/t007-r1-branch-cleanup`; removed before PR integration and never merged to `develop`.
- T007 post-integration prompt work: new Markdown commits were mistakenly appended to already-merged `docs/t007-post-integration` after PR #55; recovered through fresh branch/PR #56. This incident is the basis for the merged-branch freeze invariant introduced by PR #58.

## Next Action

1. After PR #58 is integrated, perform canonical post-integration cleanup using one durable target per invocation: first `TASK T007`, then the follow-up Markdown policy PR targets `PR 56`, `PR 57`, and `PR 58` as applicable to branches still present.
2. ChatGPT verifies the executor's returned remote/local inventories against current GitHub state. No eligible merged topic branch may remain remotely; inaccessible local checkouts must remain explicitly unverified rather than assumed clean.
3. Then launch the Agente de IA Ejecutor for T006 using the canonical minimal launch prompt and exactly one Task Contract pointer.
4. ChatGPT remotely reviews T006 handoff/diff/evidence before acceptance.
5. Do not start D036 until T006 is accepted/integrated.

Canonical post-integration cleanup prompt template is controlled by:

`docs/POST-INTEGRATION-CLEANUP-PROMPT.md`

For T007, substitute only the repository identity and target `TASK T007`. For each Markdown follow-up, substitute only its durable `PR <number>` target. Do not add branch names, SHAs, commands, or deletion decisions to the prompt.

Canonical T006 launch prompt:

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Start from current develop and read AGENTS.md first.

Then load and execute the authoritative Task Contract:
docs/tasks/T006-d035-deterministic-security-verification-contract.md

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. verify post-integration branch retirement under `docs/BRANCHING.md`, `docs/BRANCH-CLEANUP.md`, and `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` if not already complete;
2. for T006 load `docs/tasks/T006-d035-deterministic-security-verification-contract.md`;
3. load D035 and `governance-core/SECURITY.md` as normative security semantics;
4. load `governance-core/GOVERNANCE.md`, D037 and deterministic helpers only as needed;
5. load D033/D034 only for explicit security-vs-execution composition cases;
6. load D038/D030 only for a concrete provider conflict;
7. load D036 only after T006 closes or for a concrete boundary conflict;
8. do not reload T001–T005/T007 implementation history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not append commits to a topic branch after its PR has merged.
- Do not hide the T007 procedural nonconformance or Orchestrator direct-write audit history.
- Do not reopen T001–T005/T007 absent regression/audit need.
- Do not add model-based verification gates.
- Do not implement D036 inside T006.
- Do not declare the source product stable/release-ready.
