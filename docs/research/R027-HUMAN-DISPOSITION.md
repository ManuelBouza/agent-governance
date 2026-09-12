# R027 — Human disposition

Research-ID: R027  
Decision-State: APPROVED_DEFERRED  
Date: 2026-09-12  
Human disposition: approved direction; implementation deferred  
Normative change in this step: none  
Implementation authorization: not granted  
Merge/adoption authorization: not granted

## Human decision

The Human approves the R027 direction established by the completed research and Codex-host pilot:

```text
G0 ENTRY
  establish authoritative repository / branch / candidate / worktree identity
        |
        v
LOCAL TRANSACTION ZONE
  Executor-owned local Git / implementation / diagnosis / verification mechanics
        |
        v
G1 PUBLISH
  publish one complete represented task state and verify exact remote identity
        |
        v
Orchestrator review / acceptance / integration
        |
        v
G2 CLOSE
  retire branch/worktree only after exact integration and no-unique-work checks
```

The approved principle is:

> Governance controls identity, authority, semantic boundaries, evidence, and postconditions; the Executor owns compatible local Git/CLI/shell mechanics inside those boundaries.

The Human explicitly does **not** authorize implementation at this time. The present activity is documentation only.

## Effect of this disposition

This approval means:

- R027 is accepted as the intended future governance direction for normal Executor local Git transaction control;
- the G0 / LOCAL / G1 / G2 model may be used as the design basis for a later implementation task;
- the completed deterministic qualification and Codex-host pilot remain the supporting evidence package;
- no current normative document, runtime behavior, Task Contract template, Executor prompt, branch policy, cleanup policy, or implementation code is changed by this approval alone;
- `develop` and `main` remain untouched by this disposition;
- no current source-product frontier is displaced or reopened;
- no implementation branch/task is authorized by this record.

## Deferred implementation boundary

When the Human later chooses to implement R027, that work must start from then-current canonical repository authority and use the normal source-maintenance workflow. The implementation step should determine the smallest normative surface needed to encode the approved model and preserve task-specific `SPECIAL` controls rather than mechanically deleting existing safety requirements.

A future implementation should also retain the two evidence limitations already recorded by the pilot:

1. the Codex host did not expose sufficient internal model/effort observability to self-attest the selected UI profile precisely;
2. the final Human-disposition sequencing subtest was not observed prospectively in this Orchestrator transcript after the strict replay, even though the mechanical G2 result was correct and independently verified where GitHub-visible.

These limitations remain documented evidence boundaries; the Human approval does not erase or reinterpret them.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: APPROVED_DEFERRED
Implementation-State: NOT_STARTED
Normative-State: UNCHANGED
Next action: none until a future explicit Human implementation authorization
```
