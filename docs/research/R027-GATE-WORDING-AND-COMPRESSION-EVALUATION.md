# R027 Appendix — Gate wording and compression evaluation

Research-ID: R027  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: prospective wording and static compression evaluation for R027 Executor local-Git transaction gates; no normative change and no modification to the active T062 frontier  
Question: Can a compact canonical G0/LOCAL/G1/G2 contract replace repeated generic Git boundary prose in active Executor guidance while preserving task-specific scientific, security, release, recovery, and cleanup controls?  
Evaluation-Refs: `docs/research/R027-EXECUTOR-LOCAL-GIT-TRANSACTION-GATES.md`; D018; D035; D042; D048; D058; D060; D064; `docs/TASK-CONTRACTS.md`; `docs/EXECUTOR-HANDOFFS.md`; `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`; `docs/BRANCH-CLEANUP.md`; `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`; T060; T053; T063  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Purpose

The main R027 memo established that Agent Governance should control Codex local Git at semantic boundaries rather than at command granularity. This appendix tests the next question: whether those boundaries can be expressed compactly enough to reduce runtime policy/context duplication without deleting distinct safety controls.

The result is positive, but narrower than a raw-document-size claim. The largest expected gain is **runtime semantic compression across active operating guidance**, not wholesale shortening of every Task Contract.

No normative change is adopted here.

## Candidate compact gate contract

The following wording is a research candidate only. It is intentionally terminal-neutral and command-neutral.

> **G0 ENTRY** — Before writable Stage 6 begins, and again after any re-entry event that may have changed authority or workspace identity, establish the canonical repository and remote base, the exact authorized topic branch/candidate HEAD, the required base relationship, and exclusive worktree ownership. Preserve unrepresented local state. If current authority/workspace identity cannot be established safely, stop rather than reset, overwrite, delete, or guess.
>
> **LOCAL** — While G0 remains valid, the Executor owns compatible local Git mechanics inside the authorized repository/worktree/scope. Inspection, staging, unpublished commits, amendments, local history shaping, diagnosis, tests, and verification do not by themselves require a Governance recheck. Revalidate only when a boundary fact may have changed.
>
> **G1 PUBLISH** — At an explicitly authorized checkpoint or terminal boundary, ensure the represented in-scope state, required technical review/verification, and handoff are coherent and committed; no unreported in-scope working state makes the handoff misleading. Publish the authorized topic branch without force, verify canonical remote HEAD equals the intended final HEAD, verify the handoff is readable there, and verify the implementation/review anchor is represented in ancestry. Intermediate publication requires explicit checkpoint authority or a terminal BLOCKED/PARTIAL outcome.
>
> **G2 CLOSE** — After accepted integration and persisted cleanup authority, verify the merged PR/target and exact reviewed source HEAD, confirm no post-review advancement or unique unrepresented work, retire the eligible remote branch and verify absence, retire accessible local worktree/branch state safely, prune stale metadata, and restore the authorized primary checkout baseline. Ambiguity fails closed and is preserved for review.
>
> **Revalidation triggers** — session/root recovery or failover; worktree/branch switch; material remote/candidate movement; newly controlling persisted authority; explicit publication checkpoint; terminal publication; post-integration cleanup. Task-specific scientific, security, release, recovery, or other SPECIAL controls may strengthen these gates but do not become generic Git policy.

This candidate is approximately 282 words. The compactness is sufficient for use as one loadable semantic contract if later adopted, rather than requiring the Executor to reconstruct the generic Git state machine from multiple prose locations.

## Measurement method

This evaluation does not claim that every repeated word can be deleted. Decision Records remain historical/normative evidence, and detailed procedures such as branch cleanup retain value even when a compact gate references them.

The useful unit is therefore a **semantic restatement block**: a current passage that independently re-expresses a generic Git boundary already represented elsewhere.

Manual classification of the current authority/procedure set found more than ten such generic restatement blocks across:

- D042/D058/D060 entry/freshness/worktree rules;
- `TASK-CONTRACTS.md` remote-freshness and candidate-publication gates;
- `EXECUTOR-SESSION-WORKTREE-HYGIENE.md` prelaunch topology and post-integration workspace rules;
- D048 plus multiple publication/finalization sections in `EXECUTOR-HANDOFFS.md`;
- D058/D064 plus `BRANCH-CLEANUP.md` and the post-integration cleanup prompt for closure.

This is a **manual semantic-site classification**, not a token-perfect repository-wide corpus metric. Its purpose is to establish whether repeated generic definitions exist in material quantity. They do.

The target compression is therefore:

```text
many generic boundary restatements
    -> one canonical G0 definition
    -> one LOCAL autonomy definition
    -> one canonical G1 definition
    -> one canonical G2 definition
    -> task/procedure references + SPECIAL deltas only
```

Historical Decision Records and specialized detailed procedures are not candidates for deletion merely to improve the count.

## Task Contract reduction is real but modest

T060, T053, and T063 show that Task Contracts contain many fields that are not duplication:

- exact base/topic/candidate identity;
- handoff path;
- authorized scope and acceptance;
- task-specific clean-worktree qualification;
- scientific candidate/oracle/profile/schedule constraints;
- continuity phase barriers and telemetry.

Those facts must remain local to the Task Contract.

A gate reference can remove generic explanations such as “synchronize current remote, establish correct worktree, preserve local state, perform one authorized final push, verify remote HEAD,” but it cannot replace the task's actual identity or acceptance semantics.

Therefore R027 does **not** predict a dramatic size reduction for every Task Contract. The stronger benefit is fewer repeated generic Git semantics across the operating surface and less policy reconstruction during Executor execution.

## Recovery / continuity mapping

D060 requires every same-task `CONTINUE` to perform D042 freshness and reload newly controlling persisted authority. That maps directly to a G0 revalidation event:

```text
CONTINUE same root
    != reuse prior Git authority snapshot
    -> G0 revalidation
```

Likewise:

```text
root failover/recovery -> G0
worktree switch        -> G0
branch identity switch -> G0
new controlling review -> G0
```

No additional Git-specific recovery protocol is required merely because the coordinator session changes. The existing work-unit/root rules remain the authority; G0 only re-establishes repository/workspace identity before writable execution resumes.

## Release and hotfix mapping

D018 uses `develop` for normal topic work, optional `release/<semver>` stabilization, and exceptional `hotfix/<semver>` work from `main` with required propagation back to `develop`.

The generic gates still apply:

- G0 verifies the **authorized** base/topic relationship rather than assuming `develop`;
- G1 publishes only the authorized branch/checkpoint;
- G2 closes only after the specialized workflow's required integrations are complete.

Release/hotfix target topology, propagation order, tag/release semantics and any additional verification remain `SPECIAL`. They must not be flattened into the normal Git gate definition.

## Security-sensitive mapping

D035 establishes security freshness and independent verification that may depend on current vendor guidance, threat intelligence, versioned standards and actual target state. Git freshness cannot prove those facts.

Therefore:

```text
G0 PASS
    => repository/workspace authority is current enough for Git execution
    != security authority is current
```

Security-source freshness, control resolution, independent security verification and Human security exceptions remain `SPECIAL` under D035. R027 must never collapse those controls into repository freshness.

## Scientific workflow mapping

T063 remains the representative scientific case.

Its exact branch/candidate/base relationship maps to G0, and terminal represented evidence maps to G1. Frozen profiles, schedule, probes/oracles, provider-call boundaries, retries, no-replay semantics and measurement receipts remain task-specific scientific authority.

This confirms the intended composition rule:

```text
generic Git gate
+
Task Contract SPECIAL constraints
=
actual execution boundary
```

The generic gate never broadens or overrides the Task Contract.

## Detailed cleanup remains valuable

`BRANCH-CLEANUP.md` contains exact-head freeze, squash-merge handling, remote-absence verification, unique-work checks, local checkout/worktree retirement and backlog classification. Those are useful G2 procedure details.

A compact G2 contract should therefore serve as the state-transition invariant while the detailed cleanup procedure remains the operational recipe when G2 is actually executed.

This is compression by **reference and conditional loading**, not deletion of procedure knowledge.

## Evaluation result

The candidate wording passes the static compression test:

1. it expresses the generic Executor Git lifecycle in one compact state machine;
2. existing T060/T053 handoff fields are sufficient to evidence the sampled G0/G1 facts;
3. D060 recovery maps cleanly to G0 revalidation;
4. D018 release/hotfix semantics compose as SPECIAL deltas rather than forcing a second generic model;
5. D035 security freshness remains independent and is not weakened;
6. T063 scientific controls remain independent and are not generalized into Git policy;
7. G2 can reference the existing detailed cleanup procedure without duplicating it.

The principal benefit is therefore judged **material enough for one further prospective usability check**, but not yet sufficient for normative adoption.

## Remaining evaluation gap

Before proposing a Decision Record, perform one prospective static rewrite of a representative future-style Task Contract/launch-return flow using only:

```text
Task-specific identity + acceptance + SPECIAL constraints
+ reference to G0/LOCAL/G1/G2
```

Compare it with the equivalent current-style flow for:

- semantic completeness;
- safety invariant retention;
- amount of generic Git prose loaded/repeated;
- whether an Executor can determine exactly when G0 must re-run;
- whether G1 terminal evidence remains unambiguous;
- whether SPECIAL constraints remain visibly stronger than the generic gate.

This can be a synthetic/non-executed example. No provider/model call or Git mutation experiment is needed because R027 evaluates policy/context compression, not Git transport mechanics.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Candidate gate contract: ~282 words
Generic semantic duplication: material (>10 manually identified restatement blocks)
Per-Task-Contract size reduction: modest
Runtime/operating-context compression potential: material
New Git receipt: not recommended
Recovery: CONTINUE/failover/worktree switch -> G0 revalidation
Release/hotfix: generic gates + SPECIAL branch topology/propagation
Security: G0 does not satisfy D035 security freshness
Scientific workflows: generic gates + SPECIAL frozen experimental controls
Next evaluation: one prospective synthetic gate-referenced Task Contract/flow rewrite
Normative change: none
Active T062 frontier: unchanged / out of scope
T058: remains frozen
```
