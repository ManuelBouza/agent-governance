# D076 — Stage 6 Ephemeral Executable Materialization Boundary

Status: ACCEPTED  
Date: 2026-09-10  
Authority: Human Owner / ChatGPT Orchestrator  
Trigger: T063 blocked execution and subsequent Human-visible review of Executor-created temporary Python controllers  
Refines: D041, D052, D054, D059, D068  
Preserves: D033, D053, D060, D061, D062, D065, D071, D075

## Problem

D068 assigns complete Stage 5 candidate materialization to ChatGPT Orchestrator and Stage 6 execution, diagnosis, bounded technical repair and verification to the Agente de IA Ejecutor.

The repository nevertheless retained broad language allowing Executor-private tooling, testing/review helpers and "technical harness work" during Stage 6. T063 exposed an ambiguity in that wording: a substantial new evaluation controller/harness could be created as an untracked temporary artifact, executed, deleted before commit and summarized only as temporary execution mechanics while the final Git diff remained inside the authorized evidence boundary.

That creates a governance blind spot. Whether code is tracked, committed, temporary or deleted is not a reliable ownership classifier. A substantial controller, harness, orchestration program, semantic fixture generator or oracle implementation is still candidate materialization when it implements material task behavior.

## Decision

For D068-mode source maintenance, **materiality and semantic function control Stage 5/Stage 6 ownership; persistence status does not**.

The effective boundary is:

```text
small execution mechanics
    -> Executor Stage 6

substantial new executable materialization
    -> Orchestrator Stage 5
    -> publish candidate
    -> Executor Stage 6 executes/diagnoses/repairs/verifies
```

`ephemeral`, `temporary`, `untracked`, `outside the worktree`, `deleted before commit`, or `not part of the final diff` SHALL NOT by themselves make substantial executable work Executor-owned.

## Executor Stage 6 — allowed execution mechanics

Subject to the controlling Task Contract and D033/D054 envelopes, the Executor may create or compose small mechanical aids whose purpose is only to perform already-authorized execution mechanics, for example:

- shell/PowerShell/Bash command composition and pipelines;
- one-off inline snippets;
- small format-conversion, parsing, extraction or transport adapters;
- mechanically generated request/response payloads;
- temporary schema/help captures;
- bounded diagnostic snippets;
- tiny glue needed to invoke an already-materialized candidate or supported API;
- bounded repair of an already-published candidate/harness when the repair preserves approved semantics and Design.

These aids must not become a substitute for missing Stage 5 candidate materialization.

No rigid line-count threshold defines this class. Size is evidence only. Classification depends on step depth, semantic content, orchestration responsibility, state/control flow, task-specific logic, risk and whether the artifact implements material behavior that should have existed before Stage 6.

## Executor Stage 6 — materialization stop condition

The Executor MUST NOT independently first-pass materialize a substantial new artifact whose role is to implement the task/evaluation rather than merely invoke it.

Material examples include:

- a new controller or orchestration program;
- a substantial test/evaluation harness;
- a substantial script/CLI helper required to make the task executable;
- a state machine or workflow controller not already materialized by the Orchestrator;
- a semantic fixture generator whose choices affect experimental/acceptance meaning;
- an oracle/grader/acceptance implementation not already under the authorized ownership boundary;
- a non-trivial program implementing provider/session/worker lifecycle, telemetry correlation or experiment sequencing that is material to reproducibility;
- any new executable artifact whose absence means the published Stage 5 candidate was not actually complete for the authorized Stage 6 work.

When such a need is foreseeable, the Executor SHALL stop **before creating it** and report an Orchestrator re-entry condition.

Required transition:

```text
material executable artifact is missing
    -> STOP
    -> persist BLOCKED/PARTIAL evidence
    -> Orchestrator re-entry
    -> ChatGPT materializes the missing Stage 5 artifact
    -> publish coherent candidate
    -> Executor resumes under new/revised authority
```

The Executor may still propose a concise technical diagnosis or required capability. It may not turn that diagnosis into first-pass substantial implementation under the label of private execution mechanics.

## Late-discovered materiality

Sometimes an artifact begins as apparently small mechanical glue and becomes material only while being developed.

If that occurs, the Executor SHALL stop as soon as materiality becomes apparent. It must not continue expanding or executing the artifact merely because some code has already been written.

Before removal, when safe and permitted, the Executor should preserve enough audit metadata to explain what occurred without persisting secrets or private chain-of-thought. The Orchestrator then decides whether any artifact content may be retained, reconstructed, discarded or re-materialized under Stage 5 authority.

## Ephemeral artifact audit rule

For D068 Stage 6, any file-based executable artifact created by the Executor and actually executed or used to influence verification MUST be classified in the persisted handoff when it is not already part of the published/authorized candidate.

The handoff SHALL include `ephemeral_artifacts` or a semantic equivalent. An empty array is valid when none existed.

For each relevant artifact record at least:

```text
label_or_path
kind
purpose
materiality: mechanical | material | uncertain
authority_basis
approximate_size_or_lines_if_known
content_digest_if_safe_and_available
executed: true|false
persisted: true|false
removed: true|false
reentry_required: true|false
```

Absolute local paths may be sanitized when they expose irrelevant machine/user information. Secrets and credentials must never be persisted merely to satisfy this audit rule.

Routine commands and inline one-liners that never become file-based executable artifacts do not require per-artifact inventory beyond the normal verification/command evidence.

## Deletion and terminal-state rule

Deleting an unauthorized or temporary artifact before commit does not erase the need to report its existence when it materially influenced Stage 6.

If a material ephemeral executable artifact was created/executed and then removed before it could be represented or adequately audited, the Executor SHALL NOT return a normal `DONE` claim that implies the Stage 6 process is fully reconstructable. It must return `BLOCKED` or `PARTIAL` as appropriate and identify the missing audit/materialization boundary.

The final Git diff may still be clean and scope-correct; that does not by itself prove process-boundary correctness.

## Relationship to D041 process autonomy

D041 remains valid for private methodology and tool choice.

D076 narrows one ambiguity: process autonomy covers **how the Executor executes authorized Stage 6 work**, not authority to create a missing substantial executable implementation outside the Stage 5 candidate merely because that implementation is private or ephemeral.

Private planning and tool choice remain private. Material executable artifacts that implement task behavior are not exempt from ownership simply because they are implementation aids.

## Relationship to D052 technical harness wording

Any older wording that assigns broad "technical harness work" to the Executor is prospectively read as:

```text
Executor
    = execute/diagnose/technically repair an authorized harness
      + small mechanical Stage 6 aids

Orchestrator
    = first-pass materialize substantial new harness/controller/fixture/oracle artifacts
      when D068 applies
```

D052 semantic-oracle ownership remains unchanged.

## Relationship to D054 execution mechanics

D054 continues to give the Executor ownership of concrete CLI/API/SDK/shell/browser/host execution mechanics.

D054 does not authorize building a substantial new program simply to avoid Orchestrator Stage 5 materialization. Commands and adapters remain Executor-owned; the material executable candidate remains Orchestrator-owned under D068.

## Relationship to D068 repair authority

D076 does not remove bounded technical repair.

After ChatGPT has published a complete candidate/harness, the Executor may repair technical defects inside approved semantics/Design, rerun verification and persist the corrected candidate as D068 already permits.

The forbidden case is **missing first-pass materialization**, not legitimate repair of represented candidate code.

## T063 trigger and historical treatment

T063 terminal remote evidence at `3d8a9460988351383a90adfc6b76e2deff056504` contains only the two authorized JSON evidence files and no product/Markdown mutation.

Its telemetry also records that temporary controllers were removed before commit. After the run, the Human supplied Executor-UI evidence showing two temporary Python files named `t063_controller.py` and `t063_prepare.py` with large create/delete edit counts. Their contents are not represented in canonical Git and therefore cannot be reconstructed as repository state.

D076 does not retroactively accuse the Executor of violating an unambiguous rule that did not yet exist. The incident is treated as evidence that the previous Stage 5/Stage 6 wording was insufficiently precise.

T063 is separately reviewed under `docs/reviews/T063-R3.md`.

## Effective rule

```text
D068 Stage 6 needs an executable aid
    -> small/mechanical and subordinate to an already-complete candidate
         => Executor may create/use it and report file-based aids as required

    -> substantial/material task implementation, harness, controller, fixture logic or oracle
         => STOP before first-pass implementation
         => Orchestrator re-entry / Stage 5 materialization

tracked vs untracked
committed vs deleted
persistent vs ephemeral
    => not the ownership classifier
```
