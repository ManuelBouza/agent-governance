# D060 — Task-Scoped Executor Coordinator Continuity

Status: ACCEPTED  
Date: 2026-09-05  
Owner: Human Owner / ChatGPT Orchestrator  
Research: `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` (`R013`)

## Decision

For source-product Executor work, one complete governed work unit owns one Human-visible Executor Coordinator Root from first launch through task completion.

The continuity key is the exact persisted Task Contract (`Txxx`) or Operational Contract (`OPxxx`).

```text
new work unit     -> NEW / root-1
same work unit    -> CONTINUE same root
work unit closes  -> retire root for governance purposes
next work unit    -> NEW / root-1 for that new work unit
```

This decision prospectively refines D055 session selection and D058 coordinator ordinals. It does not change Task Contract semantics, Executor process ownership, model-selection policy, or Governance Core.

## One-root invariant

Normal execution MUST NOT create multiple Human-visible coordinator roots for one active work unit merely to obtain fresh context, independent review, or a different technical perspective.

Fresh technical contexts inside the same task should be obtained through Executor-internal children/subagents or equivalent bounded fresh contexts when supported.

The Human-visible root remains the stable coordinator and integrates concise results back into the task's represented state.

## Same-task continuation

`CONTINUE` is the normal required mode for additional Executor prompts governed by the same Task/Operational Contract when the root is safely recoverable.

This includes:

- implementation phases inside the same Task Contract;
- return after an Orchestrator barrier;
- persisted same-task review/rework;
- same-task verification/follow-up;
- a resumable blocked/partial task whose controlling contract remains the same;
- final Executor-side actions still owned by that contract.

Every continuation still performs D042/RB001 remote freshness and reloads newly controlling persisted authority. Remembered chat state never overrides Git.

## Task boundary

A new Task/Operational Contract ID starts a new coordinator root even when it is closely related to the previous work.

Examples:

```text
T053 Phase 1 -> T053 Phase 2  = CONTINUE same root
T056 -> T057                  = NEW root
T057 same-task R1 rework      = CONTINUE same root when recoverable
OP067 -> OP068                = NEW root
```

A successor task is not entitled to inherit the previous root merely because it shares subsystem, branch ancestry, research lineage, or product objective.

## Failover roots

`root-2`, `root-3`, ... are exceptional failover identities for the same work unit, not routine fresh-session choices.

A failover root is allowed only when the prior root cannot safely continue, including:

- session/thread loss or non-recoverability;
- host/runtime failure;
- context materially contaminated beyond safe reconciliation/compaction;
- adapter/host migration that prevents continuation;
- supported session state corruption/inconsistency;
- explicit persisted experimental authority where the Human-visible coordinator itself must be replaced.

The failover reason MUST be stated in the launch rationale and should be persisted in the task handoff/receipt when material.

The old and replacement roots MUST NOT remain concurrently writable for the same task/worktree.

Independent review alone is not a failover reason; use a fresh child/reviewer context.

## Root context hygiene

The root is a compact task coordinator, not a raw transcript archive.

Retain primarily:

- exact task/authority pointer;
- current phase/status;
- branch/worktree identity;
- relevant accepted technical constraints;
- concise child results;
- completed actions represented in Git/evidence;
- unresolved blockers/findings;
- latest Orchestrator review/gate;
- next concrete action.

Avoid loading or retaining unnecessary raw test logs, large command output, full file dumps, full child transcripts, abandoned implementation traces, and repeated copies of persisted authority.

When supported, safe host-native compaction MAY be used to reduce root context pressure. Compaction is execution state only and must preserve enough task-relevant state for correct coordination; Git/persisted authority remains canonical.

## Relationship to delegation

D060 defines **root lifetime**, not the exact delegation policy.

R012 separately recommends a semantic obligation for when a coordinator should delegate bounded work. That decision remains separately controlled until adopted.

D060 nevertheless establishes that when fresh independent reasoning is needed inside one task, a child/subagent is normally preferable to opening another Human-visible coordinator root.

## Relationship to compute routing

D060 does not select child models or reasoning effort.

R007 remains the separate adaptive child-compute-routing question. The root's Human-facing model/effort continues to follow D055 and the active adapter guidance.

## Relationship to worktrees

D058 remains controlling:

```text
one concurrently writable work unit
-> one exclusive worktree/topic branch
```

The stable task coordinator owns/coordinates that represented workspace through the task lifecycle. Internal children must preserve one-writer and worktree-isolation constraints unless a persisted contract explicitly authorizes isolated parallel writer worktrees.

## R006 disposition

R006's positive same-task persistent-root/context-locality evidence remains valid historical evidence.

Its recommendation to let one coordinator root span a broader multi-Task-Contract continuity dossier is superseded by R013/D060.

The adopted boundary is deliberately narrower:

```text
one persisted work unit = one coordinator root lifecycle
```

This improves task attribution, stale-context disposal, chat navigation, worktree ownership, and deterministic NEW/CONTINUE selection.

## T057 compatibility

T057 is already running as `AG | agent-governance | T057 | root-1` and is conforming to D060.

D060 does not modify T057's frozen one-child experiment. If T057 later requires same-task Executor rework and the current root remains recoverable, the preferred launch is `CONTINUE` in the same `T057 | root-1` coordinator.

## Effective rule

After this decision is integrated:

```text
Task changes      -> NEW coordinator
Task does not change -> CONTINUE same coordinator
```

except for explicit failover conditions above.
