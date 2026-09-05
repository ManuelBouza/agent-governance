# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O206  
Canonical-Branch: `develop`  
Current-Work-Unit: D058 coordinator-session/worktree hygiene accepted; OP067 local hygiene must converge before T057 may launch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: Codex 0.153.4 native Windows when OP067 is launched

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056, D057 and D058 control the current source-maintenance workflow.
- Core protocol remains `1.15.0`.
- T054 remains accepted with pilot outcome `NOT_QUALIFIED`.
- T055 remains accepted with `PARTIAL_OBSERVABILITY` on Codex 0.149.0.
- T056 remains accepted as an execution with `PARTIAL_OBSERVABILITY` on Codex 0.153.4; its sole causal blocker was the temporary controller `thread/loaded/list` parsing / parent-residency defect documented in `docs/reviews/T056-R1.md`.
- T057 is specified as the bounded successor in `docs/tasks/T057-codex-read-only-child-requalification-v2.md`, but it is **not yet authorized to launch** until OP067 returns `DONE`.
- R009 remains `COMPLETE / EVALUATING` under T057.
- R010 remains `COMPLETE / DEFERRED`; no global GPT-6 Astra migration is adopted and T057 remains Sol / Medium.
- R011 is `COMPLETE / DECIDED` through D058.

## D058 — coordinator identity and worktree hygiene

Authoritative decision:

`docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md`

Operating procedure:

`docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`

Research:

`docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` (`R011`)

### Coordinator naming

For named-session-capable Executors, every `NEW` Human-visible coordinator gets a deterministic name.

Current Codex convention:

```text
AG | <repo> | <work-unit> | root-<n>
```

Same-work-unit `CONTINUE` keeps the same coordinator identity. A required fresh root for the same work unit increments the ordinal.

The name is navigation metadata only. Git, persisted contracts, branches, handoffs, reviews and checkpoints remain authority.

### Worktree isolation

Each concurrently writable work unit uses an exclusive topic branch and writable worktree. Two writable coordinators may not share either surface.

Post-integration closure now includes safe retirement of obsolete task worktrees/local branches plus primary-checkout convergence.

Normal Agent Governance primary-checkout terminal state:

```text
branch        = develop
HEAD          = current origin/develop
tracked state = clean
```

Ambiguous/unique local state is preserved and blocks destructive cleanup.

## OP067 — mandatory pre-T057 local hygiene gate

Contract:

`docs/operations/OP067-normalize-local-worktrees-and-primary-checkout.md`

Receipt anchor:

GitHub issue `#286`.

Purpose:

- audit the accessible primary checkout, registered worktrees and relevant local/remote topic branches;
- classify non-primary state as `ACTIVE`, `RETAIN`, `REVIEW`, or `DELETE`;
- retire only evidence-safe `DELETE` state;
- preserve ambiguous/unrepresented state;
- prune stale worktree administrative records;
- leave the primary checkout clean at current `origin/develop`;
- establish `T057_WORKSPACE_READY=true` before T057 launch.

OP067 does not modify tracked product files.

### OP067 launch profile

```text
Executor: Codex
Session: NEW
Coordinator-Chat: AG | agent-governance | OP067 | root-1
Model: GPT-5.6 Sol
Effort: High
```

Rationale: the operation is bounded but can delete worktrees/refs and must distinguish represented history from unique local work; D055 reserves High for this class of repository-history/fail-closed risk.

## T057 launch after OP067

Only after OP067 returns `DONE` with `T057_WORKSPACE_READY=true`:

```text
Executor: Codex
Session: NEW
Coordinator-Chat: AG | agent-governance | T057 | root-1
Model: GPT-5.6 Sol
Effort: Medium
Expected branch: test/t057-codex-read-only-child-requalification-v2
```

T057 must use an exclusive writable worktree. Its scientific controls remain unchanged from the already integrated Task Contract.

## Research dispositions

```text
R006 COMPLETE / DEFERRED
R007 COMPLETE / DEFERRED
R008 COMPLETE / DEFERRED
R009 COMPLETE / EVALUATING
R010 COMPLETE / DEFERRED
R011 COMPLETE / DECIDED -> D058
```

No D055 persistence policy, child-routing policy, global Astra policy, or consumer policy is changed by D058.

## Operational incident during D058 authoring

During this Orchestrator session, a GitHub file-create call was accidentally issued without the intended topic branch and therefore targeted default `main`. It created a one-character research-path artifact, which was immediately removed by a second direct `main` commit after detection.

```text
accidental create commit: da8b819e3cf24e05fd0abcc6b6f5af11af940ba1
corrective delete commit: 9cacc956749ed6b7d5dc2faa1e9319df4571f9ed
net tracked content change on main: none
```

Do **not** rewrite/force-reset `main` to erase this history. The incident is durably acknowledged here; D058 authoring itself continues only on `docs/d058-coordinator-worktree-hygiene` from the canonical `develop` base.

## Next action

1. Complete/review/integrate the D058/R011/OP067 Markdown branch into `develop` through PR.
2. Revalidate the resulting `develop` and current `AGENTS.md`/checkpoint.
3. Human starts a NEW Codex coordinator for OP067 named exactly `AG | agent-governance | OP067 | root-1`, using GPT-5.6 Sol / High.
4. Send pointer-only transport to `docs/operations/OP067-normalize-local-worktrees-and-primary-checkout.md`.
5. Executor performs the local hygiene operation, posts the durable receipt to issue #286, and returns only the terminal fields required by OP067.
6. Orchestrator reads issue #286 and verifies OP067 outcome.
7. If OP067 is `DONE` and `T057_WORKSPACE_READY=true`, launch T057 in a separate NEW coordinator named `AG | agent-governance | T057 | root-1`, Sol / Medium, with its own exclusive worktree.
8. If OP067 is blocked, do not launch T057; resolve only the named preserved blocker through durable authority.
9. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then:

- if OP067 has not run, load D058 plus `docs/operations/OP067-normalize-local-worktrees-and-primary-checkout.md`;
- if OP067 returned terminal status, read issue #286 before any T057 launch;
- load T057 only after OP067 qualifies the local workspace.

## Do not

Do not launch T057 before OP067 `DONE`. Do not delete ambiguous worktrees/branches. Do not force-reset/clean the primary checkout to manufacture a clean state. Do not let two writable coordinators share a worktree or branch. Do not infer coordinator authority from chat title. Do not change T057's frozen model/effort/scientific variables because GPT-6 Astra exists. Do not rewrite `main` history to hide the acknowledged authoring incident.
