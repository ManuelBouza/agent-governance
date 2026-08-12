# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O034  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003 and T005 are `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

T006 remains `READY` and unchanged. Its D035 Security Core/Task Contract are already integrated and it resumes immediately after the branch-hygiene maintenance interruption closes.

T007 is the current maintenance task: repository-wide branch hygiene cleanup covering both canonical remote branches and the Agente de IA Ejecutor's accessible local checkout.

Current deterministic verification policy remains:

```text
probabilistic implementation assistant != verification authority
source-product acceptance = deterministic evidence + authorized Human/Orchestrator judgment
```

## T007 — READY FOR EXECUTOR

Task Contract:

`docs/tasks/T007-branch-hygiene-cleanup.md`

Controlling policy:

- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- GitHub issue #50

Expected executor branch:

`chore/branch-hygiene-cleanup`

Expected handoff:

`handoffs/T007-executor-handoff.json`

T007 is operational repository maintenance only. It may inspect/classify/delete safe stale Git branches and prune/delete safe local branches in the executor-controlled checkout. It MUST NOT change product code, Core, tests, decisions, Task Contracts, Markdown, tags, release state, `main`, or `develop`.

The executor must classify every non-long-lived remote branch as `DELETE | REVIEW | RETAIN`. Only `DELETE` may be removed. Exact merged-PR/head identity is required because normal PRs use squash merge; ancestry alone is not deletion authority.

Local cleanup is part of T007 acceptance. The executor must inspect local branches/worktrees, switch away from stale branches, prune remote-tracking refs and remove verified stale local topic branches. It must explicitly report any Human/other-agent checkout it cannot access instead of claiming it clean.

## T006 — READY / PAUSED FOR T007

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Planning/Core integration PR #45:

`d2730f2054a5a0639db28eae4564a47bf6051714`

Expected executor branch:

`test/security-verification-contract`

Expected handoff:

`handoffs/T006-executor-handoff.json`

T006 semantics, D035 Core state and its verification requirements are unchanged. Do not start T006 inside T007. After T007 acceptance/closure, the next action returns directly to the canonical T006 executor launch.

D036 remains after T006; do not implement it during either T007 or T006.

## Canonical executor launch-prompt invariant

`docs/TASK-CONTRACTS.md` defines the mandatory normal executor launch structure:

```text
role
+ repository/base
+ AGENTS.md bootstrap
+ exactly one authoritative Task Contract pointer
+ completion/return contract
```

Do not duplicate objective, acceptance criteria, scope, exclusions, branch/handoff details, tests or safety rules in the launch prompt when Git already controls them.

## Provider / verification invariants preserved

Portable Governance Core remains provider-neutral. D037 remains controlling: no live LLM/model reviewer is a required verification/release gate.

For T006, security and execution control remain independent planes:

```text
security evaluation may narrow/block
but cannot expand execution authority

execution authorization/procedure success
cannot manufacture security PASS
```

D038/D030 remain relevant only if a concrete provider/coexistence conflict appears.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.

## Next Action

1. Launch the Agente de IA Ejecutor for T007 using the canonical minimal launch prompt and exactly one Task Contract pointer.
2. Executor performs the complete remote + accessible-local branch hygiene task, persists/pushes the D029-compliant handoff and returns status/path/branch/HEAD only.
3. ChatGPT reviews the remote T007 handoff plus final GitHub branch state and accepts/reworks the cleanup.
4. After T007 closes, resume T006 exactly as already contracted.
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

1. while T007 is active, load `docs/tasks/T007-branch-hygiene-cleanup.md`, `docs/BRANCHING.md`, and `docs/BRANCH-CLEANUP.md`;
2. inspect GitHub issue #50 and current remote branch/PR state as needed for T007 review;
3. do not load D035/D036/provider history merely for branch cleanup;
4. after T007 closes, load the T006 contract plus D035/`governance-core/SECURITY.md` and only its controlling verification context;
5. do not reload T001–T005 implementation details absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not automatically delete `REVIEW` or `RETAIN` branches.
- Do not treat squash-merge ancestry as deletion authority.
- Do not claim inaccessible local checkouts are clean.
- Do not modify product/Core/test semantics during T007.
- Do not start T006 implementation until T007 closes.
- Do not implement D036 inside T006 or T007.
- Do not add model-based verification gates.
- Do not declare the source product stable/release-ready.
