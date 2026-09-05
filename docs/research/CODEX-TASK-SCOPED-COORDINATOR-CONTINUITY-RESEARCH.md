# Codex Task-Scoped Executor Coordinator Continuity Research

Research-ID: R013  
Research-State: COMPLETE  
Decision-State: DECIDED  
Decision-Ref: `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md`  
Date: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Scope: source-product Executor session continuity; no Governance Core portability claim

## Research question

What should be the Human-visible Executor coordinator continuity boundary for Agent Governance source-maintenance work?

The concrete alternatives are:

1. a fresh coordinator for every prompt/phase;
2. one coordinator that can span several related Task Contracts in a broader dossier/workstream;
3. one coordinator root for exactly one complete governed work unit, retained through all same-task phases/rework until that task closes, followed by a new coordinator for the next work unit.

The Human Owner explicitly prefers option 3 provided the coordinator root is kept context-efficient and can retain a compact understanding of what has happened across the whole task.

## Executive conclusion

Adopt **one Human-visible Executor Coordinator Root per complete governed work unit**.

For source maintenance, the continuity key is the exact persisted `Task Contract` (`Txxx`) or `Operational Contract` (`OPxxx`), not an informal product-area dossier and not an individual prompt.

```text
new governed work unit
        -> NEW root-1
        -> same root through implementation / evidence / barriers / rework
        -> task closes
        -> root is retired for governance purposes
next governed work unit
        -> NEW root-1 for that new work unit
```

Inside one work unit, `CONTINUE` is the normal required behavior. A second Human-visible root for the same work unit is failover only, not a routine way to obtain fresh context. Freshness/independence should normally be obtained with bounded internal children/subagents while the task coordinator remains stable.

This conclusion is adopted prospectively by D060.

## Evidence

### 1. Existing Agent Governance evidence — T053

T053 is the strongest internal evidence for same-task root continuity.

It intentionally used one Human-visible Codex root across two governed phases separated by an Orchestrator barrier. Phase 2 used `CONTINUE` in the original root after repeating D042 freshness and reloading current authority.

`docs/reviews/T053-R1.md` accepted the pilot and recorded positive qualitative evidence:

- same root successfully continued Phase 1 -> Phase 2;
- Git/current authority remained authoritative;
- stale retained assumptions were corrected;
- branch/worktree incidents remained zero;
- completed children were disposable and not reused;
- concise child conclusions were retained instead of full transcripts;
- the root reported avoiding repeated rereads of large implementation surfaces and raw child traces.

T053 did **not** prove quantitative token/cost savings because root/child token/context metrics were not available. That limitation blocks a numerical efficiency claim, but it does not negate the observed same-task continuity and context-locality benefit.

### 2. Existing R006 conclusion needs a narrower continuity unit

R006 previously recommended a persistent root for a broader coherent continuity scope/dossier that could span related Task Contracts.

That design was intentionally conservative compared with a repository-wide permanent chat, but it still allows cross-task history to accumulate in one Human-visible coordinator.

The new Human requirement plus subsequent operational experience favor a clearer boundary:

```text
Task/Operational Contract boundary = coordinator root boundary
```

Reasons:

- task identity is already durable and unambiguous in Git;
- D055/D058 naming already uses `<work-unit>`;
- task closure is the natural point to discard implementation-specific assumptions;
- a new task often changes authority, branch, worktree, acceptance, and technical objective even when product area is related;
- cross-task persistence makes it harder to distinguish useful architectural familiarity from stale implementation state;
- same-task persistence captures most of the context-locality benefit demonstrated by T053 without needing an indefinite dossier root.

Therefore R006 remains useful historical evidence about persistent-root benefits and failure modes, but its cross-Task-Contract continuity recommendation is superseded by R013/D060.

### 3. Current D055/D058 are close but not strict enough

Current D055 says:

- first launch of a new Task Contract/work unit -> `NEW`;
- clean same-task/same-branch follow-up -> `CONTINUE`;
- fresh-context/independence, host/checkout changes, stale/contaminated context, or inability to reload authority may select `NEW`.

D058 adds deterministic coordinator names:

```text
AG | <repo> | <work-unit> | root-<n>
```

and says a forced fresh root increments the ordinal.

This already points toward task-scoped continuity, but it treats `CONTINUE` as a normal option rather than a stronger same-task invariant and does not clearly distinguish routine independent review from true coordinator failover.

D060 therefore prospectively refines D055/D058:

- same work unit -> keep the same Human-visible root by default and normally MUST `CONTINUE`;
- independent exploration/review/testing -> use internal fresh children where appropriate, not a second root;
- `root-2+` -> exceptional failover only when the original coordinator cannot safely continue.

### 4. Current OpenAI guidance supports long-running state plus deliberate compaction

Current OpenAI model guidance for long-running/tool-heavy agents recommends deliberate compaction and preservation of task-relevant state such as:

- completed actions;
- active assumptions;
- IDs;
- tool outcomes;
- unresolved blockers;
- the next concrete goal.

It also emphasizes sustained follow-through until the intended task is complete.

This supports maintaining one root through a complete task **provided root context is managed intentionally rather than allowed to become a raw transcript archive**.

Relevant current sources:

- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.5
- https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.2
- https://developers.openai.com/codex/use-cases

These sources are volatile vendor guidance and must be revalidated before future vendor-specific implementation claims.

### 5. Coordinator stability and child freshness are complementary

R012 separately finds that a real coordinator architecture should not leave worker delegation purely optional. The two questions are complementary but not identical:

```text
R013 / D060
  How long does the Human-visible coordinator root live?
  -> exactly one complete governed work unit

R012
  When should that root delegate bounded work to children?
  -> semantic delegation policy, still pending separate adoption

R007
  What compute/model profile should each child receive?
  -> separate adaptive-routing question
```

D060 does not adopt R012's delegation triggers or R007's compute routing. It only establishes coordinator continuity and context-hygiene requirements.

## Adopted task-scoped lifecycle

### New work unit

When a new persisted Task Contract or Operational Contract begins:

```text
Session: NEW
Coordinator-Chat: AG | <repo> | <work-unit> | root-1
```

A related prior task does not justify `CONTINUE` across the boundary.

### Same work unit

All normal same-task continuations use the same Human-visible root, including:

- multi-phase implementation;
- Orchestrator barrier return;
- persisted review/rework;
- additional same-task verification;
- same-task blocked->resumed execution when authority still permits continuation;
- final Executor-side closure steps belonging to the same contract.

Every continuation still performs D042/RB001 freshness reconciliation. Chat continuity never makes remembered Git state authoritative.

### Fresh independent reasoning inside the same work unit

Need for a fresh technical perspective does not normally create a second Human-visible coordinator.

Use bounded internal contexts when the active Executor supports them:

- Explorer;
- Verifier/Reviewer;
- test/log-analysis child;
- specialist;
- other read-only/fresh child context.

Their result returns concisely to the root. They are disposable implementation mechanics and do not become task authority.

### Exceptional root failover

A same-task `root-2`, `root-3`, ... is allowed only when the previous Human-visible root cannot safely continue, for example:

- thread/session cannot be recovered;
- host/runtime lost the root;
- context is materially contaminated and cannot be safely reconciled/compacted;
- adapter migration makes continuation impossible;
- supported host state is corrupted or inconsistent;
- explicit persisted authority requires a distinct Human-visible root because the coordinator itself is the experimental variable.

Failover must be recorded with the reason and the prior coordinator must not remain concurrently writable for the same task.

A desire for a fresh review alone is not sufficient; use a child/fresh internal reviewer.

## Root context hygiene

The root should retain a compact task ledger, not implementation exhaust.

Retain:

```text
current task objective / exact authority pointer
current phase/status
branch + worktree identity
important accepted technical constraints
concise child findings
completed actions represented in Git/evidence
unresolved blockers/findings
latest Orchestrator review/gate
next concrete action
```

Avoid retaining when not needed:

```text
raw test logs
large command output
full file dumps
full child transcripts
abandoned implementation traces
repeated copies of persisted Task Contract text
large diagnostic explorations that can live in child context/evidence
```

When the host provides supported compaction, it may be used to reduce root context pressure while preserving task-relevant state. Compaction is an execution optimization, never authority.

There is no fixed token threshold in D060 because reliable host-neutral context occupancy is not currently guaranteed. The semantic requirement is that the root remain able to coordinate the current task without allowing accumulated noise to dominate reasoning.

## Task boundary semantics

For this decision:

```text
work unit = exact persisted Task Contract ID/path
         or exact persisted Operational Contract ID/path
```

A review revision or rework document that continues the same Task ID remains the same work unit.

A successor Task ID is a new work unit even when it continues the same product area or experiment lineage.

Examples:

```text
T056 -> T057       = new root (new Task Contract)
T053 Phase 1 -> Phase 2 = same root (same Task Contract)
T057 R1 rework     = same root if T057 remains the controlling Task Contract
OP067 -> OP068      = new root (different Operational Contracts)
T057 -> future T058 = new root
```

## Interaction with worktrees

D058 remains controlling for writable isolation.

One task-scoped root owns/coordinates the task's represented branch/worktree. Internal children must respect the same one-writer/worktree constraints unless an explicit Task Contract authorizes isolated parallel writer worktrees.

At task integration/operational closure, the root identity becomes historical navigation metadata. It is not reused for the next task.

## Interaction with T057

T057 was already launched as:

```text
AG | agent-governance | T057 | root-1
```

and therefore already conforms to the D060 task-scoped root rule.

D060 does not change T057's frozen one-child experimental topology, model, effort, worktree, version gate, or acceptance. If T057 needs ordinary same-task rework after Orchestrator convergence and the original root remains safely recoverable, D060 prefers `CONTINUE` in `T057 | root-1` rather than opening a new Human-visible coordinator.

## Decision

Adopt the task-scoped root boundary prospectively for source-product Executor work.

The central invariant is:

```text
one complete governed work unit
= one Human-visible Executor Coordinator Root
= NEW at task start
= CONTINUE through same-task lifecycle
= retire at task closure
```

with `root-2+` reserved for explicit failover rather than routine context refresh.

## Supersession

R013/D060 supersede only the **cross-Task-Contract persistence recommendation** from R006.

They do not supersede:

- T053 evidence that same-root continuity can preserve useful context locality;
- D041 Executor process autonomy;
- D042 remote freshness;
- D053 role/stage ownership;
- D054 execution-mechanics ownership;
- D058 worktree isolation/naming;
- R012 delegation research;
- R007 adaptive child compute routing.

## Authoring incident

While R013 was being prepared, an Orchestrator file-create call accidentally targeted `develop` directly and created this research path with placeholder content at commit:

```text
59c44d88e202c24928fd4908470bd91099703023
```

The history is not rewritten. Correct R013/D060 content is authored on `docs/r013-task-scoped-coordinator-continuity` and integrated through normal PR review. The placeholder has no normative meaning.
