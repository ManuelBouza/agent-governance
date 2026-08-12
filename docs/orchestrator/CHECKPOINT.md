# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O040  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

D039 — Evidence-Driven Governance Learning Loop (EGLL) — is `ACCEPTED`. Its source-maintainer lifecycle is controlled by:

- `docs/decisions/D039-evidence-driven-governance-learning-loop.md`
- `docs/ARCHITECTURE-GOVERNANCE-LEARNING-LOOP.md`
- `docs/GOVERNANCE-LEARNING.md`

T008 — `docs/tasks/T008-egll-deterministic-learning-detectors.md` — is `READY` and is the next executable task after outstanding post-integration branch cleanup.

T006 remains `READY` and unchanged, but is sequenced after T008. T008 MUST NOT absorb T006/D035/D036 work. After T008 is accepted, integrated and post-integration-cleaned, resume T006 exactly as already contracted. D036 remains after T006.

## D039 — ACCEPTED

D039 makes recurrence prevention a first-class source-maintenance lifecycle:

```text
detect -> evidence -> fingerprint/triage -> causal analysis
       -> control selection -> controlled implementation
       -> regression/replay proof -> recurrence monitoring
```

Controlling invariants:

```text
failure observed != learning completed
written lesson != preventive control
control integrated != control effective
model reflection != learning authority
```

Automatic components MAY detect/fingerprint evidence and enforce already-accepted deterministic invariants. They MUST NOT create new Governance authority, mutate policy/architecture/Task Contracts, approve their own remediation, infer Human intent, or use LLM judgment as a verification gate.

Recurrence of the same stable fingerprint after a control reaches `VERIFIED` becomes `CONTROL_FAILURE` unless evidence establishes a materially different condition.

Consumer-product EGLL remains out of scope until a later explicit architecture decision based on source-maintainer evidence.

## T008 — READY

Task Contract:

`docs/tasks/T008-egll-deterministic-learning-detectors.md`

Expected executor branch:

`test/egll-deterministic-learning-detectors`

Expected handoff:

`handoffs/T008-executor-handoff.json`

T008 is a deterministic source-maintainer MVP. Required initial fingerprints:

- `git.branch.post_merge_advance`
- `git.branch.delete_before_review_resolution`
- `task.handoff.identity_mismatch`
- `task.done_requires_rework`
- structured procedural-nonconformance learning candidate

T008 uses synthetic replay fixtures, including T007-derived cases. It has no live GitHub/network/model/provider/ruleset/Actions dependency and changes no Governance Core consumer semantics.

## T006 — READY AFTER T008

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Expected executor branch:

`test/security-verification-contract`

Expected handoff:

`handoffs/T006-executor-handoff.json`

T006 semantics, D035 Core state and deterministic verification requirements remain unchanged. D036 MUST NOT be folded into T006.

## Branch lifecycle hardening

PR #58 introduced the explicit merged-branch freeze invariant in `docs/BRANCHING.md` and `docs/BRANCH-CLEANUP.md`:

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

Once a topic PR is merged, its source branch MUST receive no additional commits. Any post-merge branch advancement is a workflow nonconformance and becomes `REVIEW`; follow-up work must be recovered/persisted through a fresh branch from the current authorized base before the original merged branch can be retired.

Canonical delegated branch retirement is defined by `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` and `docs/BRANCH-CLEANUP.md`. The cleanup prompt accepts exactly one durable target: `TASK <task-id>` or `PR <number>`. Do not send branch lists or deletion decisions in chat.

## T007 closure state

T007 implementation is accepted/integrated and the historical backlog was resolved. The remaining operational work is post-integration retirement of temporary T007 and follow-up Markdown branches that still exist remotely/local to accessible checkouts.

Preserve the T007 procedural audit: the initial executor pass deleted `eval/d032-agent-capability` before fully resolving its missing PR association, restored it at the exact original SHA, and the persisted R1 disposition later authorized final exact-SHA deletion as cancelled T004 work.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.
- T007-R1 review preparation: accidental temporary non-Markdown `noop` file on `docs/t007-r1-branch-cleanup`; removed before PR integration and never merged to `develop`.
- T007 post-integration prompt work: new Markdown commits were mistakenly appended to already-merged `docs/t007-post-integration` after PR #55; recovered through fresh branch/PR #56. This incident is a seed regression case for D039/T008 and the basis for the merged-branch freeze invariant.

## Next Action

1. Integrate the D039 acceptance / learning lifecycle / T008 planning PR if its diff remains limited to authorized Markdown, then freeze its source branch.
2. Complete canonical post-integration cleanup for outstanding integrated targets whose branches remain, including the D039/T008 planning PR after integration. Verify remote and accessible-local inventories.
3. Launch the Agente de IA Ejecutor for T008 using the canonical minimal Task Contract launch prompt and exactly one pointer to `docs/tasks/T008-egll-deterministic-learning-detectors.md`.
4. ChatGPT remotely reviews T008 handoff/diff/evidence. Rework must be persisted/auditable.
5. After T008 acceptance/integration and post-integration cleanup, launch T006 unchanged.
6. Do not start D036 until T006 is accepted/integrated.

Canonical T008 launch prompt:

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Start from current develop and read AGENTS.md first.

Then load and execute the authoritative Task Contract:
docs/tasks/T008-egll-deterministic-learning-detectors.md

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

Canonical T006 launch prompt remains controlled by its existing Task Contract and `docs/TASK-CONTRACTS.md`.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. verify required post-integration branch retirement under `docs/BRANCHING.md`, `docs/BRANCH-CLEANUP.md`, and `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` if not already complete;
2. for T008 load `docs/tasks/T008-egll-deterministic-learning-detectors.md`, D039 and `docs/GOVERNANCE-LEARNING.md`;
3. load D037 and existing deterministic test/helper conventions only as needed for T008 review;
4. after T008 closes, for T006 load `docs/tasks/T006-d035-deterministic-security-verification-contract.md`, D035 and `governance-core/SECURITY.md`;
5. load D033/D034 only for explicit security-vs-execution composition cases;
6. load D038/D030 only for a concrete provider conflict;
7. load D036 only after T006 closes or for a concrete boundary conflict;
8. do not reload older implementation history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not append commits to a topic branch after its PR has merged.
- Do not let automatic learning components mutate Governance authority.
- Do not use model-based verification gates.
- Do not implement live GitHub enforcement, trend aggregation, or consumer EGLL inside T008.
- Do not fold T008 into T006 or D036.
- Do not hide the T007 procedural nonconformance or Orchestrator direct-write audit history.
- Do not declare the source product stable/release-ready.
