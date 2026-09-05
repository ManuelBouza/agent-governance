# Library-First Source Maintenance Runbook

Status: ACTIVE  
Controlling decisions: D061, D062, D066, D067, D068

## Purpose

Define the normal source-maintenance flow when ChatGPT can use local Git plus Library for persistent working state and Codex/another Executor is used primarily to execute, diagnose, repair, and verify the candidate.

## Planes

```text
GitHub
= canonical repository / branch / PR authority

ChatGPT local Git + Library
= candidate authoring and persistent working plane

Executor Coordinator + workers
= execution / diagnostics / technical repair / verification plane

ChatGPT
= semantic acceptance / integration / current-state evolution
```

Library is never a Git remote and never overrides GitHub.

## Phase A — Bootstrap and objective

1. verify current `develop` from GitHub;
2. read `AGENTS.md` + current checkpoint;
3. verify predecessor bootstrap under D067 when this is a successor chat;
4. state one exact objective and observable completion condition;
5. load only directly controlling authority;
6. classify D066 capability availability.

If Library/local Git capability required by the chosen mode is unavailable, use the accepted protected fallback; do not weaken freshness or ownership controls.

## Phase B — Establish writable identity

Before candidate mutation:

```text
refresh protected develop
-> create unique short-lived topic branch
-> verify exact topic branch exists at intended develop SHA
-> establish local standalone Git workspace
-> acquire D066 lock/sentinel only when portable cross-chat writable mode requires it
-> create/validate unique Library workspace namespace when retained
-> WRITE_ALLOWED
```

No direct `main`/`develop` content mutation is permitted.

## Phase C — ChatGPT materializes the candidate

ChatGPT owns the complete candidate under D068:

- specification/Design/Plan/Task Contract;
- Markdown;
- source/application code;
- implementation tests;
- semantic conformance assets under ChatGPT ownership;
- configuration/schema;
- fixtures;
- scripts/helpers;
- documentation.

Normal working loop:

```text
edit locally
-> local Git diff/stage/commit as useful
-> inspect candidate coherence
-> persist/rotate validated Library snapshot when durability is needed
-> continue locally
```

Do not publish each small edit to GitHub.

## Phase D — Candidate publication gate

Before Executor launch:

1. re-read remote topic branch and require expected freshness;
2. ensure candidate local Git state is coherent;
3. ensure Task Contract/authority needed by the Executor is included;
4. publish the bounded candidate state to the topic branch;
5. verify resulting GitHub branch HEAD/tree/file set;
6. record exact candidate HEAD;
7. only then launch the Executor Coordinator.

The Executor must never be asked to use specification/Design/Plan that exists only in chat or Library.

## Phase E — Executor Coordinator

Before every launch, apply D055/D060 and identify:

```text
Executor
Session: NEW | CONTINUE
Coordinator-Chat
Model
Effort
Rationale
```

For a new Task Contract use a new root; same-task continuation uses the same recoverable root.

The root keeps compact task state and delegates materially separable execution slices when safe/capable.

Preferred worker slices include:

- focused tests;
- full test suite;
- lint/format/static checks;
- environment/package/build commands;
- app/CLI execution;
- Playwright/browser verification;
- Computer Use or equivalent interactive verification;
- logs/traces;
- independent code/risk review;
- bounded diagnosis;
- bounded repairs with explicit writable ownership.

The root synthesizes results rather than retaining unnecessary raw logs.

## Phase F — Repair loop

When a worker/root finds an implementation defect already covered by approved semantics:

```text
classify in-authority defect
-> repair on task branch/worktree
-> rerun affected checks
-> continue verification
```

When the finding would change requirement, architecture, acceptance, semantic oracle, open-gap status, material dependency/privilege, or another upstream authority:

```text
STOP
-> persist BLOCKED/PARTIAL evidence
-> return to ChatGPT for Specify/Design/Plan re-entry
```

Do not make tests green by weakening semantics.

## Phase G — Executor terminal publication

The Executor persists its final handoff and publishes the final represented task branch state according to the controlling Task Contract/handoff policy.

Visible transport remains compact, normally:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-head>
```

The GitHub branch/handoff is authority, not the terminal message.

## Phase H — Re-synchronize Library after Executor changes

If the Executor changed the candidate, the prior task Library snapshot is stale.

Before acceptance when Library task state is retained:

```text
fetch exact Executor GitHub HEAD
-> materialize standalone Git state
-> create replacement snapshot
-> checksum
-> safe extract
-> git fsck --full
-> verify branch/HEAD/tree/receipt
-> promote current
-> revalidate
```

Only the representation matching the final GitHub candidate is eligible to support Converge/Accept.

## Phase I — ChatGPT Converge / Accept

ChatGPT verifies:

- objective completeness;
- specification/Design/Plan fidelity;
- final GitHub diff;
- Executor repair/verification evidence;
- no unauthorized scope;
- no semantic weakening;
- Library/GitHub representation alignment when retained.

Outcome:

```text
ACCEPT
REWORK
BLOCK / upstream re-entry
```

Acceptance authority remains ChatGPT/Human, not Executor green tests.

## Phase J — Integration and canonical snapshot

After acceptance:

1. open/review PR to protected `develop`;
2. merge only under current integration authority;
3. verify canonical `develop` HEAD;
4. refresh target Library snapshot when Library mode is in use;
5. round-trip validate, promote, and revalidate target current;
6. perform only D066-positive feature snapshot GC;
7. release lock only with exact current owner/blob identity;
8. execute branch/worktree cleanup under existing authority;
9. refresh checkpoint.

Ambiguity means retain/block, not delete.

## Phase K — Close the ChatGPT objective

Apply D067:

```text
objective accepted/integrated
+ persistence complete
+ canonical/Library state reconciled
+ cleanup classified
+ checkpoint current
=> OBJECTIVE_COMPLETE
```

If no next objective has been supplied, enter `WAITING_FOR_NEXT_OBJECTIVE`.

When the Human Owner supplies the next objective, generate the successor bootstrap and do not execute that new objective in the predecessor chat.

## Fail-closed invariants

Never:

- use Library as canonical authority;
- bypass D061/D062;
- execute Codex against chat-only authority;
- retry stale lock CAS until ownership is obtained;
- let two writable work units share a Library snapshot/branch/worktree;
- accept a stale pre-repair Library snapshot;
- let Executor repair specification/Design/acceptance defects silently;
- infer a next objective from backlog/history;
- start a new objective in a completed predecessor chat.
