# R026 — ChatGPT Web surface scope correction

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: correction to R026 assumptions about persistent local repositories and Work Desktop availability  
Question: What interaction-minimization architecture is actually available when the Orchestrator is operating in ChatGPT Web rather than ChatGPT Desktop/Work with access to a user-local repository?  
Evaluation-Refs: Human Owner current-surface clarification on 2026-09-12; R026; active ChatGPT Web tool inventory  
Decision-Ref: none  
Supersedes: R026 Work-local feasibility statements for the current operating surface only  
Superseded-By: none

## Correction trigger

The Human Owner clarifies that the active operating surface is ChatGPT Web. There is no user PC or persistent user-local repository exposed to this chat.

Therefore references in R026 to a persistent local repository on the user's machine, Work Desktop folder access, or direct local Git operation are not available assumptions for the current Agent Governance Orchestrator workflow.

## Corrected meaning of "local"

For the current ChatGPT Web surface, "local" can only mean an execution/runtime workspace made available to ChatGPT during the current session or tool invocation.

It does **not** mean:

- a repository stored on the Human Owner's PC;
- a persistent ChatGPT Desktop/Work folder;
- a user-controlled long-lived `.git` worktree automatically available across chats.

Unless separately qualified, such runtime workspace state must be treated as ephemeral and non-canonical.

## Corrected R026 candidate architecture

For the current web-only surface, the candidate architecture becomes:

```text
GitHub
  = canonical remote authority

ChatGPT Web runtime workspace
  = temporary working/cache surface when materialization is possible

GitHub Git Data publication
  = bounded multi-file publication surface

GitHub PR event task / webhook
  = event-driven observation where supported
```

The optimization target is therefore:

```text
obtain exact GitHub snapshot with the fewest remote reads
-> materialize/work in the ChatGPT Web runtime
-> perform many reads/searches/edits without additional GitHub access
-> publish one bounded change set
-> observe PR state by event rather than polling
-> verify final remote state once
```

## Candidate modes after both R026 corrections

The valid comparison for the current surface is now:

```text
M0 BASELINE
  connector on-demand file reads
  + ordinary connector writes

M1 WEB-RUNTIME / CONNECTOR-MINIMIZED
  obtain one exact-ref repository snapshot or equivalent bounded materialization
  -> use temporary ChatGPT runtime for reads/search/authoring
  -> publish via create_tree + create_commit + non-force update_ref
  -> create PR
  -> event-driven observation where supported
  -> bounded final verification
```

`M2 WORK-LOCAL` is removed from the current-surface pilot because ChatGPT Web has no exposed persistent user-local repository.

Library also remains excluded by the separate R026 Library correction because current per-operation approval gates create Human interaction amplification.

## Consequence for cross-chat persistence

The current web-only design does not yet have a qualified low-friction persistent repository cache across chats.

Therefore cross-chat reuse cannot be assumed. Each new chat may require a fresh bounded synchronization/materialization step unless a future ChatGPT Web capability provides persistent workspace state without per-operation Human approval.

This is a limitation of the current surface and must be measured explicitly rather than hidden behind Desktop/Library assumptions.

## Updated pilot focus

The next empirical pilot should use a disposable repository such as `ManuelBouza/test_biblioteca` and test only capabilities actually available from ChatGPT Web:

1. minimum remote calls required to identify an exact source ref;
2. whether the repository can be materialized into the runtime in one bounded operation;
3. zero additional per-file GitHub reads during local exploration after materialization;
4. multi-file publication with constant logical mutations using Git Data;
5. fail-closed stale-ref behavior;
6. exact final-tree equivalence;
7. Human approval count;
8. cross-chat cost when runtime state is not persistent.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Current operating surface: ChatGPT Web
Persistent user-local repository: NOT AVAILABLE
Work-local mode for current pilot: EXCLUDED
Library mode: EXCLUDED by separate correction
Remaining candidate: web-runtime connector-minimized workflow
Normative change: none
```

This correction narrows R026 to the capabilities of the actual current product surface. D066 remains unchanged and T058 remains frozen.