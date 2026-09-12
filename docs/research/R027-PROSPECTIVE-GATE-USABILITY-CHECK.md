# R027 Appendix — Prospective gate usability check

Research-ID: R027  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: non-executed prospective usability comparison of current-style generic Executor Git prose against the R027 G0/LOCAL/G1/G2 reference model; no normative change and no modification to the active T062 frontier  
Question: Can a future Task Contract preserve the same generic Git safety semantics while replacing repeated prose with references to a canonical gate contract and task-specific identity/SPECIAL deltas?  
Evaluation-Refs: `docs/research/R027-EXECUTOR-LOCAL-GIT-TRANSACTION-GATES.md`; `docs/research/R027-GATE-WORDING-AND-COMPRESSION-EVALUATION.md`; D042; D048; D058; D060; `docs/TASK-CONTRACTS.md`; `docs/EXECUTOR-HANDOFFS.md`; `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md`  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Purpose

This is the final prospective static check requested by R027 before any later normative proposal. It does not modify an actual Task Contract and does not authorize execution.

The comparison isolates **generic Git boundary prose only**. It does not count objective, specification, Design, authorized scope, acceptance, verification, scientific/security/release semantics, or other task-specific content.

## Synthetic current-style equivalent

A representative current-style Task Contract may need to restate the generic boundary semantics approximately as follows:

> Before writable Stage 6 begins, synchronize the canonical remote and establish that the local baseline reflects the current authorized base. Verify the exact topic branch and candidate HEAD, confirm its required relationship to the protected base, and ensure that the selected writable worktree is exclusively owned by this work unit. Preserve any unrepresented local state and stop rather than reset, overwrite, delete, or guess when identity cannot be established safely.
>
> During execution, keep normal progress local. Do not publish intermediate topic-branch state unless this Task Contract explicitly authorizes a checkpoint or the invocation is terminating BLOCKED or PARTIAL with an auditable handoff.
>
> At terminal publication, commit the complete represented in-scope state and the handoff, ensure no unreported in-scope working-tree state makes the handoff misleading, push the authorized topic branch without force, verify the canonical remote branch resolves to the reported final HEAD, verify the handoff is readable there, and verify the implementation/review anchor is represented in ancestry.
>
> After accepted integration, cleanup remains a separately authorized operation. Verify the merged PR and exact reviewed source HEAD, ensure the branch has not advanced and no unique unrepresented work would be discarded, retire and verify the remote branch, safely retire accessible local worktree/branch state, and restore the authorized primary checkout baseline.

Normalized word count for this synthetic generic block: **208 words**.

This is not quoted from one current Task Contract. It is a controlled synthesis of the generic semantics currently distributed across D042/D048/D058 and active operating guidance.

## Synthetic gate-referenced equivalent

With a canonical G0/LOCAL/G1/G2 contract, the same prospective Task Contract can carry identity and deltas instead:

> Git boundary policy: apply the canonical G0/LOCAL/G1/G2 semantics.
>
> Task identity:
> - base: `develop`
> - topic: `fix/TXXX-example`
> - candidate: `<published-authorized-head>`
> - handoff: `handoffs/TXXX-executor-handoff.json`
>
> Before writable Stage 6, pass G0 for this identity. Re-run G0 on CONTINUE, failover, worktree/branch switch, material remote/candidate movement, or newly controlling authority. Inside LOCAL, Git mechanics are Executor-owned.
>
> No intermediate publication is authorized. At terminal DONE/BLOCKED/PARTIAL, satisfy G1 and return only the standard status/handoff/branch/remote-HEAD fields. After accepted integration, G2 occurs only under separately persisted cleanup authority.
>
> SPECIAL: this task adds no Git-specific strengthening beyond the generic gates.

Normalized word count for this synthetic gate-referenced block: **90 words**.

Measured reduction for this isolated generic Git block:

```text
208 -> 90 words
reduction = 118 words
relative reduction ~= 56.7%
```

The result must not be misreported as a 56.7% reduction of the whole Task Contract. It is a reduction of the **generic Git-boundary prose segment** in this representative synthetic comparison.

## Semantic equivalence check

The gate-referenced version preserves the required generic facts:

| Required fact | Current-style block | Gate-referenced block |
| --- | --- | --- |
| canonical remote/base freshness | explicit prose | G0 |
| exact topic/candidate identity | explicit prose | task identity + G0 |
| protected-base relationship | explicit prose | G0 |
| exclusive worktree ownership | explicit prose | G0 |
| preserve ambiguous/unrepresented state | explicit prose | G0 |
| ordinary local Git autonomy | implicit through existing decisions | LOCAL explicit |
| no unauthorized intermediate push | explicit prose | G1 + task checkpoint delta |
| terminal coherent commit/handoff | explicit prose | G1 |
| non-force normal publication | explicit prose | G1 |
| remote final HEAD verification | explicit prose | G1 |
| handoff readability / ancestry | explicit prose | G1 |
| cleanup is separate authority | explicit prose | G2 + persisted cleanup authority |
| exact reviewed-head / no unique-work cleanup | explicit prose | G2 |
| local worktree/primary-baseline closure | explicit prose | G2 |

No generic invariant is intentionally removed.

## Revalidation usability check

The prospective wording answers the main ambiguity explicitly:

```text
G0 is not “once per Task ID”.
G0 remains valid only while its identity/authority assumptions remain valid.
```

Mandatory re-entry triggers remain visible in the Task Contract reference:

- `CONTINUE` after an Orchestrator barrier;
- root failover/recovery;
- worktree or branch switch;
- material remote/candidate movement;
- newly controlling persisted authority.

This is consistent with D060's requirement that same-task continuation still performs D042 freshness.

Task-specific workflows may add stronger revalidation triggers as `SPECIAL` without changing the generic model.

## Publication usability check

The gate-referenced form remains explicit about whether an intermediate checkpoint is authorized.

That property must stay task-local because D048 allows explicit exceptions. A Task Contract should therefore state one of the following clearly:

```text
intermediate publication: NONE
```

or name the exact authorized checkpoint/barrier.

This prevents a generic G1 reference from accidentally creating checkpoint authority.

The terminal return shape remains unchanged:

```text
STATUS
HANDOFF
BRANCH
HEAD
```

No new terminal transport field or Git receipt is required.

## SPECIAL visibility check

The compressed form must not make specialized controls visually disappear behind a generic gate reference.

A future Task Contract should therefore keep a small explicit `SPECIAL Git/authority constraints` section whenever applicable, for example:

- scientific frozen candidate/base and no-replay rules;
- security freshness/independent-verification requirements under D035;
- release/hotfix base/target/propagation rules under D018;
- explicit intermediate publication barrier;
- recovery-specific branch/worktree reconstruction evidence;
- provider/runtime candidate pinning that is part of experiment validity.

The generic gate is the floor, not the ceiling.

## Transport prompt finding

The Human-mediated Codex transport prompt should **not** absorb the G0/G1/G2 definitions.

D071 already requires the transport prompt to be complete for handoff while persisted Git remains canonical. Current compact prompts such as the T063 launch correctly identify repository/session/task/candidate and instruct synchronization plus execution of the persisted authority.

Therefore the intended layering is:

```text
Human-facing transport prompt
    -> short pointer + exact launch identity
persisted Task Contract
    -> task identity + acceptance + SPECIAL deltas + gate references
canonical Git gate contract
    -> G0 / LOCAL / G1 / G2 generic semantics
conditional detailed procedures
    -> cleanup / recovery / specialized operational recipe when invoked
```

This avoids moving policy bulk from the Task Contract into the Human copy/paste prompt.

## Prospective result

The usability check is positive:

1. the generic Git segment can be represented materially more compactly;
2. all sampled generic safety facts remain determinable;
3. re-entry triggers remain explicit;
4. D048 intermediate-checkpoint authority remains task-local;
5. the terminal handoff shape does not change;
6. specialized scientific/security/release constraints remain visibly additive;
7. the transport prompt remains compact rather than becoming a new policy carrier.

The measured synthetic reduction is sufficiently large to justify a later normative proposal, but the decision should be framed as **semantic centralization and conditional loading**, not as a repository-wide documentation-minimization target.

## R027 evaluation closure

R027 has now completed the planned analytical/static qualification for its scope:

```text
architecture audit                         PASS
field coverage via existing handoffs       PASS
T060/T053/T063 static classification        PASS
canonical gate wording                     PASS
recovery/CONTINUE mapping                  PASS
release/hotfix composition                 PASS
security-freshness separation              PASS
prospective gate-referenced usability      PASS
new Git receipt needed                     NO
Git mutation/provider experiment needed    NO
```

Remaining blockers are **integration/decision sequencing**, not missing research evidence:

1. R026/#371 must be integrated or otherwise durably dispositioned so the research ledger does not skip R026;
2. R027 must be refreshed against then-current `develop` and added to `docs/RESEARCH-TRACEABILITY.md`;
3. any normative adoption requires a separate Human-accepted Decision Record and coordinated edits to the active operating surfaces; R027 itself does not create policy.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Static/prospective evaluation: COMPLETE
Generic Git prose sample: 208 -> 90 words (~56.7% reduction)
Whole-Task-Contract reduction claim: NOT MADE
Runtime semantic compression: SUPPORTED
New receipt/protocol: NOT RECOMMENDED
Normative adoption: NOT YET
Next research action: none required for current scope
Next governance action after R026 sequencing: decide whether to adopt canonical G0/LOCAL/G1/G2 semantics
Active T062 frontier: unchanged / out of scope
T058: remains frozen
```
