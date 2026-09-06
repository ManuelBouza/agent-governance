# Objective-Scoped Chat Handoff Runbook

Status: ACTIVE  
Controlling decision: `docs/decisions/D067-objective-scoped-orchestrator-chat-lifecycle.md`

## Purpose

Provide the concrete source-maintenance procedure for closing one ChatGPT objective and handing the next objective to a fresh ChatGPT chat without relying on private prior conversation history.

## Rule

```text
one ChatGPT chat
= one explicit objective
```

Once the objective is complete, the chat does not start another material objective. If the Human Owner supplies the next objective in the completed chat, the predecessor uses it only to generate the successor bootstrap.

## Completion checklist

Before declaring `OBJECTIVE_COMPLETE`, verify the applicable subset:

1. requested objective is satisfied or explicitly blocked;
2. acceptance/review state is durable;
3. GitHub canonical state is current and identified;
4. Task/Operational Contract lifecycle state is durable;
5. Executor handoff/review evidence is durable when used;
6. D066/D068 Library task snapshot is current/validated or explicitly not retained;
7. any retained lock/worktree/branch state is classified;
8. cleanup/GC that belongs to the objective is complete or explicitly retained with reason;
9. `docs/orchestrator/CHECKPOINT.md` reflects the frontier;
10. no material fact required by the successor exists only in chat.

If any required item is false, do not close.

## When the next objective is not yet known

Set/represent:

`WAITING_FOR_NEXT_OBJECTIVE`

The predecessor may answer questions about the completed objective and repair closure defects. It does not select work from backlog/history.

When the Human Owner later supplies a new objective, generate a bootstrap prompt and do not execute the new objective in the predecessor.

## Bootstrap construction

Use this shape, omitting only genuinely inapplicable fields:

```text
Repository: <owner/repo>
Predecessor: <identity>
Completed objective: <what just finished>
Next objective: <exact new objective>

Canonical branch: <branch>
Expected canonical HEAD: <sha>
Checkpoint: docs/orchestrator/CHECKPOINT.md
Expected checkpoint sequence: <Oxxx>

Active/retained state:
- <task/operation status>
- <branch/head/handoff/PR as applicable>

Library state:
- namespace: <path or n/a>
- checksum: <sha256 or n/a>
- Git tree: <tree or n/a>
- represented GitHub HEAD: <sha or n/a>

Minimum load:
1. current canonical branch identity
2. current AGENTS.md
3. current checkpoint
4. <only direct controlling references>

Bootstrap verification:
- compare expected vs observed GitHub state
- verify referenced branches/heads/handoffs
- validate Library snapshot before writable use when required

FAIL-CLOSED:
If any material discrepancy exists, do not execute the new objective.
Return BOOTSTRAP_MISMATCH with expected vs observed values and identify the predecessor.
Ask the Human Owner to return that discrepancy packet to the predecessor chat for repair.
```

The bootstrap should be short enough to paste cleanly. References and exact identities are preferred over copied history.

## Successor procedure

The successor performs in order:

```text
fetch current canonical GitHub branch
-> read AGENTS.md
-> read checkpoint
-> load minimum references
-> verify bootstrap identities
-> validate Library state if required
-> verify active remote artifacts
-> either START_NEW_OBJECTIVE or BOOTSTRAP_MISMATCH
```

The successor does not treat a mismatch as permission to repair predecessor state while continuing the new objective.

## Discrepancy packet

Return something equivalent to:

```text
STATUS: BOOTSTRAP_MISMATCH
PREDECESSOR: <identity>
NEXT_OBJECTIVE: <objective>
EXPECTED: <state/value>
OBSERVED: <state/value>
SOURCE: <GitHub/Library artifact>
BLOCKER: <why safe continuation is impossible>
```

The Human Owner carries this packet to the predecessor.

## Predecessor repair

The predecessor may repair only closure/handoff state belonging to its completed objective. Typical repairs:

- stale checkpoint identity;
- stale bootstrap expected SHA;
- incomplete evidence-safe cleanup;
- Library/GitHub representation mismatch;
- incorrect retained-state classification.

After repair:

1. persist canonical correction;
2. verify corrected state;
3. issue replacement bootstrap;
4. remain `HANDOFF_READY`.

Do not begin successor work.

## Retirement

After the successor verifies the bootstrap and begins its objective, the predecessor is `RETIRED` for normal governance use.

Do not reuse the predecessor for a later objective merely because its context is still visible.
