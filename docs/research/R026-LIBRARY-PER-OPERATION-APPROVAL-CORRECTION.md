# R026 — Library per-operation approval correction

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: correction to the Library feasibility assumptions inside `R026-CHATGPT-GITHUB-INTERACTION-MINIMIZATION.md`  
Question: Does current ChatGPT Library remain operationally suitable even as an optional persistence/fallback plane for a workflow whose objective is to minimize Human and GitHub interaction overhead?  
Evaluation-Refs: Human Owner current-surface observation on 2026-09-12; R026; R014/R015/D066 historical Library qualification  
Decision-Ref: none  
Supersedes: R026 Library-feasibility statements only  
Superseded-By: none

## Correction trigger

The Human Owner reports that the current ChatGPT Library surface requests explicit user permission for each Library operation.

This is materially different from the earlier R014/R015 capability experiments, where programmatic Library operations were usable as part of an agentic persistence workflow.

For R026's optimization objective, per-operation Human approval is not a minor usability cost. It defeats the purpose of an autonomous low-interaction repository workflow because every snapshot upload, materialization, read, replacement or cleanup may create a Human interaction gate.

## Corrected R026 interpretation

For the current ChatGPT surface:

```text
ChatGPT Library
  != normal persistence plane
  != normal fallback plane
  != cross-chat repository transport candidate
  = excluded from the R026 optimized operational path
    while per-operation Human approval is required
```

Therefore Library is removed entirely from the candidate optimized workflow.

No Library operation is required by the candidate path.

## Effect on R026 modes

The Library-dependent paths are excluded. The separate web-surface correction further narrows the current pilot to the ChatGPT Web runtime and removes Work-local assumptions.

Library is not part of any current candidate mode.

Cross-chat durability must come from a future capability that does not require per-operation Human approval. Until one is qualified, R026 must accept ephemeral web runtime workspaces rather than reintroduce Library as an approval-heavy transport.

## Human-interaction metric correction

R026's optimization metric must count Human approval prompts, not only GitHub calls.

A candidate workflow is not acceptable merely because it reduces GitHub operations if it replaces them with repeated Human permission gates.

Add the following acceptance invariant:

```text
I. normal repository read/author/persist/resume operations require no per-operation Human approval
```

Human involvement remains appropriate for explicit governance gates, consequential approvals and actions that product security intentionally requires, but not as the routine transport mechanism for repository state.

## Relationship to R014/R015/D066

This correction does not claim that R014/R015 were historically wrong. Their experiments remain evidence about the runtime that existed when they were executed.

It establishes only that their Library-based operational path is not currently suitable for R026's interaction-minimization objective under the observed approval model.

D066 remains unchanged by this research. Its historically qualified Library mode is not revoked here; any future normative refinement requires a separate accepted decision. T058 remains frozen.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Library in R026 candidate architecture: EXCLUDED
Reason: per-operation Human approval overhead
Normative change: none
```

The next empirical pilot should not use Library.