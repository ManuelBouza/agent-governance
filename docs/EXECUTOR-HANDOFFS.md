# Executor Handoffs

Status: ACTIVE

## Purpose

Define how an `Agente de IA Ejecutor` returns Stage 6 execution, diagnosis, bounded technical repair, and native SDD `Code Review & Verify` evidence to ChatGPT Orchestrator in a durable, auditable form.

The executor's chat/terminal response is transport only. The authoritative execution result MUST be persisted in Git and pushed to the canonical remote before the executor reports completion, blocking, or partial progress.

D029 defines the non-self-referential Git identity model used by this contract. D048 defines normal-task remote-publication timing. D053 defines single-owner SDD authority, and D068 prospectively refines new D068-mode source maintenance so ChatGPT owns Stage 5 complete candidate materialization while the Executor owns Stage 6 execution/diagnosis/bounded repair/verification. ChatGPT Orchestrator retains Stage 7 `Converge / Accept / Integrate / Evolve` authority.

For D068-mode work, the coherent candidate and its controlling authority published on the verified topic branch are sufficient authority for Executor verification. A separate planning/candidate merge into `develop` is not required before Stage 6. Historical executed contracts/handoffs retain their original meaning and are not rewritten retroactively.

D052 semantic-oracle ownership, D054 execution-mechanics ownership, D060 coordinator continuity, D061/D062 protections/freshness, and D065 delegation obligations remain intact.

## Canonical location

Executor handoffs live under:

`handoffs/`

Recommended naming:

`TNNN-executor-handoff.json`

The handoff MUST be non-Markdown so the Agente de IA Ejecutor can own and persist it under D016/D068 Stage 6 authority.

For refactor baseline checkpoints, a Task Contract MAY require an additional artifact such as:

`handoffs/TNNN-rf1-baseline.json`

## Required fields

Each final handoff MUST record at least:
- `task_id`
- `status`: `DONE`, `BLOCKED`, or `PARTIAL`
- `task_contract_path`
- `branch`
- `implementation_head_sha`
- `base_branch`
- `base_sha`
- `files_changed`
- `implementation_summary`
- `verification.commands`
- `verification.results`
- `verification.runtime`
- `verification.network_required`
- `dependencies_or_config_changes`
- `git_status`
- `unresolved_issues`
- `recommended_next_task`
- `chatgpt_read_path`

For new or materially revised D053/D068-governed tasks, the handoff MUST additionally make the applicable Code Review & Verify evidence determinable, either through explicit fields below or an equivalent Task-Contract-defined structure:

- `sdd_profile`
- `code_review.reviewed_head_sha` — the final candidate/repair state technically reviewed; normally equal to `implementation_head_sha`
- `code_review.summary`
- `code_review.findings` — material findings or an explicit empty result
- `code_review.resolved_findings` — in-authority technical defects corrected before terminal status, when any
- `code_review.upstream_reentry_required` — boolean
- `code_review.upstream_reentry_stage` — `null`, `Specify`, `Design`, or `Plan & Trace` as applicable
- `requirement_trace` — mapping/evidence pointers for material requirement/spec-delta items, including `PRESERVED` invariants where applicable

A `COMPACT` task MAY represent these through concise equivalent fields rather than verbose nested objects, provided ChatGPT can reconstruct the same claims unambiguously from the handoff plus referenced evidence. A Task Contract may require stronger `STANDARD`/`ASSURED` trace detail.

The handoff MUST NOT create a second specification, Design or acceptance authority. It reports Stage 6 execution/review evidence against the Task Contract and published candidate; it does not redefine the requirement delta or approved Design.

`implementation_head_sha` identifies the committed final candidate/technical-repair/test/eval state described by the evidence. It MUST be reachable as an ancestor of the final pushed topic-branch HEAD reported after handoff finalization.

The handoff JSON MUST NOT be required to contain the SHA of the commit that contains that same JSON. Such a requirement is self-referential and impossible to satisfy.

For backward compatibility, an existing `head_sha` field MAY be interpreted as the implementation/review anchor when the handoff explicitly states that meaning.

## Code Review & Verify invariant

Before a normal D068 task may report `DONE`, the executor SHALL review the published/final repaired candidate against the approved specification/Design/Plan and applicable Task Contract obligations for:

- requirement/spec-delta fidelity, including material `PRESERVED` behavior;
- controlling Design and authorized-scope fidelity;
- correctness, edge cases and failure behavior;
- maintainability/unnecessary complexity;
- represented security/privacy/reliability/compatibility constraints;
- required deterministic/property/integration/eval/conformance evidence;
- material unauthorized scope additions.

The executor MAY correct findings that are technical implementation/test defects inside the D068 repair envelope and then rerun affected verification. If a material finding indicates a defective/ambiguous/infeasible upstream specification, Design, Plan or acceptance meaning, the executor MUST NOT redesign/reinterpret it in the handoff. It reports `upstream_reentry_required`, persists the evidence, and returns `BLOCKED` or `PARTIAL` as appropriate to the Task Contract.

D052 semantic oracle meaning remains Orchestrator-owned. An Executor may not weaken or reinterpret an Orchestrator-owned oracle merely to make the candidate pass.

Executor technical review completion is not ChatGPT acceptance.

## Lifecycle

For D068-mode work:

1. ChatGPT persists the SDD-anchored Task Contract, applicable D052 semantic oracle assets, and complete Stage 5 candidate on the verified topic branch.
2. ChatGPT publishes one coherent topic-branch checkpoint containing that authority/candidate; no separate pre-verification merge to `develop` is required.
3. The executor synchronizes the canonical remote, verifies the exact topic-branch candidate HEAD and protected-base/freshness relationship, and uses that candidate as the Stage 6 starting state.
4. The executor executes the candidate, diagnoses failures, performs only bounded technical repairs inside approved semantics/Design, and performs Code Review & Verify plus required verification.
5. If an upstream SDD defect is found, the executor persists a terminal blocker/re-entry handoff rather than redefining the contract.
6. For a `DONE` path, the executor commits the final candidate/repair/test/eval state that the review/verification evidence describes.
7. The executor records that commit as `implementation_head_sha` and `code_review.reviewed_head_sha` in the task handoff artifact under `handoffs/`.
8. The executor records material requirement-to-evidence trace and review findings/results.
9. The executor commits the handoff artifact; this may create a handoff-only successor commit.
10. For a normal task, after Stage 6 terminal state and handoff are coherent, the executor performs the planned publication of the complete topic-branch state to the canonical remote under D048.
11. The executor verifies that the remote topic branch resolves to the pushed final HEAD.
12. The executor's visible response contains only status, handoff path, branch, and the actual pushed branch HEAD.
13. ChatGPT fetches the remote branch at that visible HEAD, reads the handoff there, verifies that `implementation_head_sha` is an ancestor, and performs Stage 7 Converge/Accept review of the candidate, Stage 6 evidence and trace.

Explicit grandfathered/non-D068 work retains the lifecycle recorded by its persisted authority, including any earlier planning-only `develop` integration requirement. This document does not retroactively migrate historical executed handoffs.

If implementation changes after the handoff was generated, the executor MUST rerun affected technical review/verification as required, create a new implementation commit, update `implementation_head_sha`/review anchor, and regenerate the handoff. A handoff-only metadata/finalization commit does not require a new implementation anchor.

## Remote publication timing invariant

D068 requires the Orchestrator's complete candidate checkpoint to be published before Executor Stage 6. D048 continues to control Executor publication timing after that handoff boundary.

For a normal Stage 6 invocation that is still executing toward its intended terminal result, intermediate Executor repair progress SHOULD remain local unless the controlling Task Contract/workflow requires a remote checkpoint or the invocation terminates `BLOCKED`/`PARTIAL` with auditable state.

The normal D068 sequence is:

`published Orchestrator candidate -> local Stage 6 execution/diagnosis/repair -> Code Review & Verify -> repair/final implementation commit when needed -> final handoff -> handoff/finalization commit -> planned Executor push -> remote HEAD verification -> terminal response`

A pre-completion Executor remote push is allowed when:

- the controlling Task Contract or referenced workflow explicitly requires an intermediate remote checkpoint, such as an RF1 baseline awaiting Orchestrator approval; or
- the executor is actually terminating the invocation with `BLOCKED` or `PARTIAL` and can safely publish a remotely auditable terminal handoff before returning that status.

Writing `status = PARTIAL` into an intermediate handoff does not create checkpoint authority when the same invocation is continuing toward `DONE`.

This is a publication-timing rule, not a history-rewrite rule. If Orchestrator review later requires rework, or a post-push handoff-only correction is legitimately required, a later authorized corrective push may occur on the same task branch. Do not reset, force-push, or erase prior remote history merely to simulate a single physical push.

## Commit/push invariant

A normal Executor handoff is not complete while the authoritative Stage 6 result exists only on the Executor's local machine.

Before the planned Stage 6 publication, the executor MUST ensure:
- all in-scope technical repair/test/eval changes intended for review are committed;
- Code Review & Verify is complete for the implementation anchor described by the handoff or the terminal blocker state is explicitly represented;
- required verification is complete for the implementation anchor described by the handoff;
- the handoff artifact is committed;
- no unreported in-scope working-tree changes would make the handoff misleading.

After that push and before returning status, the executor MUST ensure:
- the topic branch is present on the canonical remote;
- the visible reported `HEAD` equals the pushed topic-branch HEAD;
- `implementation_head_sha` is an ancestor of that visible HEAD;
- the handoff file is readable at that visible HEAD.

If pushing is impossible because of credentials/connectivity/permissions, persist a `BLOCKED` handoff locally if possible and report the inability to create a remotely auditable state. ChatGPT cannot accept a normal Stage 6 result from chat-only evidence.

## Refactor baseline checkpoints

When `docs/REFACTORING-WORKFLOW.md` requires RF1 baseline approval before structural mutation:
- run the required pre-refactor characterization suite;
- persist the Task Contract-specified baseline handoff/artifact;
- commit and push that checkpoint before structural mutation when the controlling refactor contract requires it;
- return a minimal `PARTIAL` pointer for ChatGPT baseline review;
- do not continue past the contracted gate until ChatGPT has persisted/communicated baseline acceptance according to the Task Contract/workflow.

This checkpoint is an explicit D048 exception and freezes evidence without inventing a third governance role. D053 `PRESERVED` requirements remain Orchestrator-owned acceptance semantics even when the executor produces technical characterization evidence. D068 does not retroactively change already-executed refactor baselines.

## Visible response pattern

The executor's terminal/chat response SHOULD be equivalent to:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/TNNN-executor-handoff.json`

`BRANCH: <topic-branch>`

`HEAD: <pushed-final-branch-head-sha>`

The visible `HEAD` is intentionally outside the handoff JSON because it may identify the commit that contains the final handoff itself.

For an intermediate RF1 checkpoint, the handoff path may be the baseline artifact specified by the Task Contract.

Additional narrative should be minimal. The repository handoff is authoritative.

## Persistence timing

The executor MUST persist the handoff after completing the applicable Stage 6 technical review/verification or reaching a terminal blocker and before claiming the task is DONE/BLOCKED/PARTIAL.

For a normal D068 DONE task, the planned Stage 6 sequence is:

`published candidate -> execution/diagnosis/repair -> Code Review & Verify -> final implementation/repair commit when needed -> handoff JSON referencing reviewed implementation commit -> handoff/finalization commit -> planned push -> remote HEAD verification -> visible final HEAD`

Intermediate Executor remote publication while the invocation continues toward `DONE` is not part of this sequence unless explicitly contracted.

Additional post-push handoff-only correction commits are allowed when legitimately required by review/finalization and when they do not change implementation/test/eval state and the JSON continues to identify the correct implementation/review anchor.

## Audit invariant

A reviewer must be able to reconstruct from the canonical Git remote:

- what ChatGPT requested: `docs/tasks/<task>.md` plus any persisted specification/Design/Plan revision/review directive;
- the exact published Stage 5 candidate/authority checkpoint when D068 applies;
- what final candidate/repair state the Executor attests to: `implementation_head_sha` in `handoffs/<task>-executor-handoff.json`;
- what Stage 6 technical review/verification the Executor performed and whether any upstream re-entry issue remains;
- how material requirement/spec-delta items map to implementation/evidence at the depth required by the SDD profile;
- what exact pushed branch state contains that handoff: the visible `HEAD` verified against the remote branch;
- what actually changed: pushed commits/diff and test/eval artifacts;
- what ChatGPT later accepted/rejected through Stage 7 convergence review.

Chat history and an Executor's unpushed local filesystem MUST NOT be required for this reconstruction.
