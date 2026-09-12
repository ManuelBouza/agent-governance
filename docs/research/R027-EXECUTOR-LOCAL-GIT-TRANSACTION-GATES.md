# R027 — Executor local Git transaction gates

Research-ID: R027  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: source-product Executor/Codex local Git and worktree governance; control compression at repository transaction boundaries; no change to active T062/O279 execution authority  
Question: Can Agent Governance simplify control of Codex local Git by concentrating governance at entry, publication, and closure boundaries while preserving branch/worktree isolation, freshness, handoff identity, remote publication safety, and post-integration cleanup?  
Evaluation-Refs: D041; D042; D048; D054; D058; D062; D064; D071; `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`; `docs/EXECUTOR-HANDOFFS.md`; `docs/TASK-CONTRACTS.md`; `docs/BRANCHING.md`; `docs/BRANCH-CLEANUP.md`; official OpenAI Codex safety guidance 2026-05-08; current Git `push` and `worktree` documentation  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive conclusion

The current Agent Governance architecture already has the correct high-level intent:

```text
Governance owns outcome + boundaries + acceptance
Executor owns technical execution mechanics
```

The opportunity is therefore **not to govern more Git commands**. It is to compress distributed Git requirements into a small number of named semantic gates and leave the Executor autonomous between those gates.

Recommended analytical model:

```text
G0 ENTRY
  establish authoritative repository / branch / candidate / worktree identity
        |
        v
LOCAL TRANSACTION ZONE
  autonomous local Git + implementation + diagnosis + verification
        |
        v
G1 PUBLISH
  publish one complete represented task state and verify remote identity
        |
        v
Orchestrator review / acceptance / integration
        |
        v
G2 CLOSE
  retire merged branch/worktree safely and restore normal checkout baseline
```

This is primarily a **policy-compression and control-locality** opportunity, not a new Git transport architecture.

No normative change is adopted by R027.

## 1. Current policy already rejects command-level micromanagement

D041 gives the Executor implementation-process autonomy inside its authorized stages. D054 makes Git/CLI/shell mechanics Executor-owned and explicitly separates semantic authorization from adapter syntax.

That means Agent Governance should normally care about facts such as:

- which repository and work unit are active;
- which branch/worktree is writable;
- which remote/candidate/base identity authorizes execution;
- whether publication is allowed now;
- which exact final HEAD was published;
- whether cleanup can discard no unique work.

It should not normally prescribe:

- exact `git status`, `git diff`, `git add` ordering;
- number of unpublished local commits;
- whether the Executor amends or squashes unpublished local commits;
- private diagnostic branches/temporary local Git mechanics that remain inside the exclusive work unit and do not escape authority/evidence boundaries;
- routine tool syntax when an equivalent safe operation satisfies the contract.

The Executor remains responsible for preserving required evidence and must not use local Git autonomy to discard ambiguous/unrepresented work, weaken a frozen evaluation, rewrite published history, or cross the authorized repository scope.

## 2. Distinct controls that should remain distinct

The audit found several controls that may look repetitive in prose but defend different failure modes. They should not be removed merely to reduce text.

### 2.1 Remote freshness before authority load — KEEP

D042 requires canonical remote freshness and verified local identity before repository policy / Task Contract execution is loaded.

This prevents a stale checkout from interpreting an older contract as current authority.

This is an **entry identity control**, not a recurring requirement to micromanage every later local Git operation.

### 2.2 Exclusive branch/worktree ownership — KEEP

D058 requires one concurrently writable work unit to own one topic branch and one exclusive worktree.

Git itself refuses normal creation of a second worktree for a branch already checked out elsewhere unless force is used. That native safeguard is useful defense in depth, but Git does not understand Agent Governance work-unit ownership, coordinator continuity, stale local state, or whether a checkout contains unrepresented work. Governance therefore still needs the higher-level ownership invariant.

### 2.3 Single normal final publication — KEEP

D048 requires normal Executor work to remain local until the planned final publication boundary, subject to explicit checkpoint/terminal exceptions.

This prevents GitHub from becoming a scratch transport and keeps incomplete intermediate states from appearing as review candidates.

### 2.4 Server-side long-lived-branch protection — KEEP

D062 provides an independent provider-side control for `main`/`develop`-like long-lived branches. It protects against an unsafe request even if a process-level gate fails.

A compressed Executor Git contract must not replace this independent layer.

### 2.5 Exact remote handoff identity — KEEP

`docs/EXECUTOR-HANDOFFS.md` requires the final represented branch/HEAD, implementation ancestry, verification evidence and remote readability of the handoff.

This is the transaction's externally auditable commit boundary.

### 2.6 Post-integration freeze and cleanup — KEEP AS A SEPARATE PHASE

`docs/BRANCHING.md`, `docs/BRANCH-CLEANUP.md`, and D064 deliberately distinguish implementation completion from branch/worktree retirement.

Cleanup has different preconditions: accepted/merged PR identity, reviewed head identity, no post-merge branch advancement, no unique local work, remote branch retirement, worktree removal, and primary-checkout convergence.

It should therefore remain G2 rather than being folded into G1 publication.

## 3. Where the current architecture is unnecessarily distributed

The same Git identity facts recur across multiple authorities and operating documents:

- Task Contract launch/readiness text;
- D042 remote baseline freshness;
- D058 worktree topology gate;
- `EXECUTOR-SESSION-WORKTREE-HYGIENE`;
- `EXECUTOR-HANDOFFS`;
- D048 publication timing;
- branch cleanup policy.

The repetition is understandable because the documents evolved from different incidents. The risk is that an Executor must reconstruct an implicit state machine from several prose locations and may repeat equivalent checks unnecessarily or encounter wording that drifts over time.

The target should not be fewer safety facts. The target should be **one canonical semantic definition for each boundary**, referenced by the other documents.

## 4. Candidate three-gate model

### G0 — ENTRY / OPEN TRANSACTION

Before the Executor enters writable task execution, establish once for the current work-unit session:

```text
repository identity
+ current canonical remote synchronization
+ exact authorized topic branch
+ exact published candidate / starting HEAD
+ required protected-base relationship
+ exclusive worktree ownership for the work unit
+ no ambiguous local state that would be overwritten/discarded
+ governing repository instructions current for the session
=> LOCAL_TRANSACTION_OPEN
```

The exact Git commands remain Executor-owned under D054.

The facts already have natural homes in the Task Contract and handoff/workspace fields. R027 does **not** recommend a new competing durable receipt merely to duplicate them.

### Local transaction zone — EXECUTOR AUTONOMY

After G0 passes and until a publication/revalidation trigger occurs, the Executor may use compatible local Git mechanics as part of Stage 6 execution, including ordinary inspection, staging, unpublished commits, amendments, local history shaping, diagnostics and verification.

Constraints remain outcome/effect based:

```text
stay inside authorized repo/worktree/scope
preserve evidence required by the contract
preserve ambiguous/unrepresented work
no routine publication checkpoint
no unauthorized long-lived-branch write
no published-history rewrite
no semantic/design authority expansion
```

A local Git command is not governance-significant merely because it mutates the local task branch. It becomes governance-significant when it crosses one of those boundaries.

### G1 — PUBLISH / COMMIT TRANSACTION

Before the normal terminal publication:

```text
required implementation/review/verification complete
+ complete in-scope state committed
+ persisted handoff committed and internally consistent
+ no unreported in-scope working-tree state
+ authorized topic branch / remote identity revalidated as required
+ normal non-force publication
+ remote HEAD == intended final local HEAD
+ handoff readable at represented remote HEAD
+ implementation_head_sha is represented in required ancestry
=> REMOTE_CANDIDATE_PUBLISHED
```

D048's one planned final push remains the normal transport.

Normal `git push` already rejects a remote update when the remote branch is not an ancestor of the pushed state. Plain `--force` disables that safety and remains inappropriate for the normal path. R027 does not recommend adding `--force-with-lease` to normal publication merely because it exists; expected-value force is relevant only to an explicitly authorized history-rewrite workflow, which D048's normal path is designed to avoid.

### G2 — CLOSE / RETIRE TRANSACTION

After Orchestrator acceptance/integration, use the existing cleanup authority:

```text
merged PR into authorized target
+ exact reviewed PR head known
+ source branch frozen / no post-review advancement
+ no unique unrepresented local work
+ remote branch retired and absence verified
+ local worktree / branch safely retired where accessible
+ primary checkout restored/converged as required
=> WORK_UNIT_GIT_LIFECYCLE_CLOSED
```

D064 may keep this cleanup attached to the same task coordinator when its eligibility gate is satisfied, but the cleanup authority remains a distinct persisted operation.

## 5. Revalidation should be event-triggered, not command-triggered

A useful compression rule is to re-run the relevant gate when the facts that justified it may have changed, rather than after arbitrary local Git commands.

Candidate revalidation triggers include:

- Executor session/worktree recovery or switch;
- topic branch/worktree identity change;
- new remote publication checkpoint;
- detected remote branch movement or unexpected fetch result;
- explicit Task Contract freshness checkpoint;
- governing repository-policy change requiring reload;
- transition from implementation to terminal publication;
- transition from merged state to cleanup.

Routine `status`, `diff`, staging, local commits, amendments or test runs inside the same verified exclusive worktree are not by themselves reasons to repeat the complete remote/bootstrap gate.

This distinction requires prospective validation before becoming normative because current D068/task-specific contracts may impose stricter freshness checks for particular scientific or security-sensitive flows.

## 6. Expected gains

### 6.1 Less instruction duplication

Launch prompts and Task Contracts can point to named Git gates instead of restating overlapping branch/base/worktree/freshness rules.

### 6.2 Lower context and reasoning overhead

The Executor receives a small state machine rather than reconstructing policy from multiple partially overlapping passages.

### 6.3 Fewer contradictory Git instructions

One canonical definition per boundary reduces drift between Task Contracts, handoff procedure, worktree hygiene and cleanup text.

### 6.4 Better Executor autonomy

The Executor can use native Git efficiently without treating every local mutation as a Governance event, consistent with D041/D054.

### 6.5 Stronger audit semantics

Named gates make it clearer which facts prove:

- authorization to start writable work;
- authorization to publish a final represented state;
- authorization to retire branch/worktree state.

### 6.6 No loss of independent defenses

Server-side branch protection, Git worktree safeguards, non-fast-forward push rejection, persisted handoffs and post-merge exact-head cleanup remain defense in depth rather than being collapsed into one fragile mechanism.

## 7. What R027 does not recommend

R027 does not recommend:

- central Orchestrator control over every Git command;
- a command-name allowlist for normal local Git;
- replacing D054 Executor-owned operation resolution;
- replacing D048 with connector-style Git Data publication for Codex;
- force-push as a normal conflict-resolution mechanism;
- removing D042 entry freshness;
- allowing two work units to share a writable worktree or branch;
- treating Git's native worktree refusal as sufficient work-unit ownership proof;
- merging G1 publication and G2 post-integration cleanup;
- adding a second durable Git receipt that duplicates Task Contract/handoff fields;
- changing active T062/O279 authority or consuming any T062 provider/model execution;
- resuming frozen T058.

## 8. External evidence

### OpenAI — boundary-oriented Codex safety

OpenAI's 2026-05-08 description of internal Codex deployment states a simple operating principle: keep the agent inside clear technical boundaries, make low-risk everyday actions frictionless, and require review for higher-risk actions. The mechanisms include sandbox writable roots, approval policy, constrained network access, rules and agent-native telemetry.

Source:

- https://openai.com/index/running-codex-safely/

This supports the general control-locality pattern. It does not itself define Agent Governance policy.

### Git — native worktree exclusion

Current Git worktree documentation states that normal `git worktree add` refuses to check out a branch already checked out in another worktree unless force is used, and that removal of an unclean worktree is refused unless forced.

Source:

- https://git-scm.com/docs/git-worktree

This is useful defense in depth but does not replace D058's work-unit ownership semantics.

### Git — normal push and forced-update semantics

Current Git push documentation states that normal push rejects updates that are not fast-forwards, while plain `--force` disables those protections. `--force-with-lease=<ref>:<expect>` supplies an expected-value guard for explicitly forced rewrites.

Source:

- https://git-scm.com/docs/git-push

For Agent Governance's normal D048 publication path, avoiding history rewrite is simpler than introducing forced-update mechanics.

## 9. Evaluation gaps before a normative compression

The analytical model is stable, but adoption should remain `EVALUATING` until the following are checked prospectively:

1. **Field coverage:** prove that existing Task Contract + handoff/workspace fields can carry all G0/G1/G2 evidence without a new duplicated receipt.
2. **Freshness equivalence:** map every existing freshness check to G0, G1, G2 or an explicit revalidation trigger; do not accidentally remove a distinct security/scientific requirement.
3. **Prompt reduction:** compare representative current Executor launch/return flows against a gate-referenced version and quantify duplicated Git instructions/context.
4. **Recovery behavior:** verify that same-task `CONTINUE`, root failover and worktree recovery correctly force G0 revalidation when local identity may have changed.
5. **Specialized workflows:** confirm release/hotfix, explicit intermediate checkpoints, scientific frozen baselines and security-sensitive tasks can add stricter gates without weakening the normal model.
6. **Cleanup continuity:** preserve D064 attached-closure semantics and exact-head branch retirement evidence.
7. **No authority duplication:** ensure any deterministic helper validates existing authority/evidence instead of becoming a second acceptance authority.

## 10. Recommended next step

Do not create a new Git-control subsystem yet.

First perform a **static compression evaluation** over representative existing Task/Operational Contracts and their handoffs:

```text
current instructions/checks
  -> classify each as G0 | LOCAL | G1 | G2 | SPECIAL
  -> identify exact duplicates and distinct defenses
  -> propose canonical gate wording
  -> measure prompt/policy reduction
  -> prove no invariant disappears
```

Use historical/closed work units for this evaluation; do not perturb the active T062/O279 scientific execution.

If that evaluation is positive, the likely normative change is a small canonical Executor Git transaction-boundary specification referenced by existing documents, not a command wrapper and not a new receipt protocol.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Core finding: governance should compress local-Git control into named transaction boundaries, not micromanage Executor Git mechanics
Candidate gates: G0 ENTRY -> autonomous LOCAL zone -> G1 PUBLISH -> G2 CLOSE
Independent controls preserved: D042, D048, D058, D062, D064, handoff identity, cleanup exact-head checks
New durable receipt: NOT RECOMMENDED
Active T062/O279: unchanged
T058: remains frozen
Normative change: none
```

### Integration sequencing note

At the time R027 was opened, canonical `develop` contained registry entries through R025 while R026 existed on the still-open PR #371. R027 therefore reserves the next identifier but must not be made ready/integrated with a ledger that silently skips R026. Before R027 is ready for integration, reconcile `docs/RESEARCH-TRACEABILITY.md` against then-current canonical `develop`, preserving the integrated disposition of R026 and all later frontier changes.