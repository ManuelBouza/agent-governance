# D068 — Library-First Candidate Materialization and Executor Verification Boundary

Status: ACCEPTED  
Date: 2026-09-06  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: source-product maintenance when ChatGPT Orchestrator uses the D066 local-Git/Library adapter

## Decision

Agent Governance adopts a **Library-first candidate materialization** boundary for source-product maintenance when the required ChatGPT runtime capabilities are available.

For this adapter, ChatGPT Orchestrator owns the complete candidate materialization before Executor verification. The Agente de IA Ejecutor no longer owns first-pass implementation for new work operating under this mode; it owns execution, diagnosis, bounded technical repair, and verification of the published candidate.

The effective source-maintenance stage map is:

```text
1 Explore / Frame                 -> ChatGPT Orchestrator
2 Specify                         -> ChatGPT Orchestrator
3 Design                          -> ChatGPT Orchestrator
4 Plan & Trace                    -> ChatGPT Orchestrator
5 Candidate Materialize           -> ChatGPT Orchestrator
6 Execute / Diagnose / Repair /
  Verify                          -> Agente de IA Ejecutor
7 Converge / Accept / Integrate /
  Evolve                          -> ChatGPT Orchestrator
```

No stage has dual authority. The Human Owner retains final authority.

This decision prospectively refines D053, D052, D054, D060, D065 and D066 for this source-maintenance adapter only. It does not automatically change Governance Core or consumer-project SDD semantics.

## Why this boundary exists

R014/R015 and D066 qualified a workflow in which ChatGPT can maintain real Git state in a temporary workspace, persist self-contained `.git` snapshots across chats through Library, and publish represented state to GitHub in bounded batches.

Once ChatGPT can materialize a coherent candidate directly, requiring a coding Executor to recreate the same candidate from the specification adds translation overhead and duplicates context. The Executor has stronger comparative value where local execution and host-native tools are required.

The intended split is therefore:

```text
ChatGPT
  = intent + specification + design + plan + complete candidate

Codex/Executor Coordinator
  = real execution + diagnostics + technical repair + verification

ChatGPT
  = semantic convergence + acceptance + integration + living-state evolution
```

## Applicability

D068 applies to a new source-maintenance objective when:

- the Human Owner has authorized the objective;
- the ChatGPT runtime exposes the capabilities required by the selected D066 mode;
- ChatGPT can materialize the candidate artifacts in a verified topic workspace;
- the work does not have persisted experimental authority fixing another authorship topology.

If the required Library/local-Git capability is unavailable, the Orchestrator may use the protected GitHub fallback and another currently accepted execution boundary. Missing capability must not be emulated by weakening D061/D062 freshness or ownership controls.

## Stage 5 — ChatGPT Candidate Materialize

ChatGPT may create and edit every candidate artifact needed to realize the approved objective, including:

- committed Markdown;
- application/source code;
- implementation tests;
- conformance tests/oracles already within ChatGPT semantic ownership;
- configuration;
- schemas;
- fixtures;
- scripts/CLI helpers;
- documentation;
- other in-scope repository artifacts.

This is a source-product role-boundary exception/refinement to earlier blanket statements that all non-Markdown implementation belongs to the Executor.

Candidate materialization remains subordinate to the approved specification, Design, Plan & Trace, security/compatibility boundaries, and branch/workspace controls. ChatGPT may not use Stage 5 to bypass Human approval gates or invent implementation outside the objective.

## Library-first working plane

After D061 establishes a verified short-lived topic branch/work-unit identity, iterative candidate work SHOULD occur in the D066 local-Git/Library working plane when available:

```text
verified topic branch identity
-> materialize standalone local Git workspace
-> edit Markdown/code/tests/config/fixtures locally
-> local diff/stage/commits as useful
-> persist validated Library snapshot when durability is needed
-> repeat without per-edit GitHub writes
```

Library is workspace persistence only. GitHub remains canonical repository authority.

The Orchestrator SHOULD prefer bounded/final GitHub publication checkpoints rather than one remote mutation per file or edit.

## Authority publication gate before Executor launch

Codex/Executor MUST NOT execute against authority that exists only in chat or Library.

Before Stage 6 starts, ChatGPT SHALL publish a coherent candidate checkpoint to the task topic branch on GitHub containing, as applicable:

- the exact Task Contract / Plan & Trace authority;
- controlling Decision/specification deltas needed by the task;
- candidate implementation;
- candidate tests/config/fixtures;
- required semantic conformance assets;
- the Git identity needed to verify the candidate checkpoint.

The topic branch is sufficient execution authority; D068 removes the requirement that every new Task Contract/candidate first be merged into `develop` in a separate planning PR before Executor verification.

Required invariant:

```text
current protected develop base
+ verified unique topic branch
+ coherent published authority/candidate checkpoint
=> Executor may verify that topic branch
```

This is not permission to execute from an arbitrary stale branch. The branch must have an auditable merge-base/current-base relationship under the controlling Task Contract and D042/D061 freshness rules.

## Task Contract semantics under D068

For a D068 task, the Task Contract describes:

- objective/specification/Design/Plan authority;
- candidate scope and invariants;
- exact published candidate checkpoint/branch expectations when known;
- what the Executor must execute/diagnose/repair/verify;
- repair authority;
- stop/re-entry boundaries;
- required evidence and handoff.

A D068 Task Contract is not an instruction to recreate the candidate from scratch. It is an instruction to validate the candidate and make only authorized technical repairs.

## Test authorship refinement

D052 semantic-oracle ownership remains intact.

Under D068:

- ChatGPT may author candidate implementation/regression/integration tests during Stage 5;
- ChatGPT continues to own semantic conformance/oracle meaning where D052 assigns that authority;
- Executor workers may add, correct, or strengthen technical tests when doing so stays inside the approved behavior/Design and does not redefine acceptance;
- an Executor may not weaken, reinterpret, delete, or change the expected semantic meaning of an Orchestrator-owned oracle merely to make the candidate pass.

A test bug that is purely technical may be corrected inside Executor repair authority. A requirement/oracle/acceptance defect requires Orchestrator re-entry.

## Stage 6 — Executor Coordinator role

The Human-visible Executor root is a **coordinator-first execution surface**, not the default primary author of the candidate.

The root retains:

- exact Task Contract/authority pointer;
- candidate branch/worktree identity;
- current execution phase;
- authorized repair envelope;
- summarized worker findings;
- unresolved blockers;
- final represented branch state;
- verification synthesis;
- final handoff accuracy.

When supported and safe, the root SHOULD delegate materially separable execution/noise-heavy slices to workers instead of absorbing their raw output into the root context.

Normal worker-eligible slices include:

- unit/integration/full-suite tests;
- lint/format/static checks;
- `uv`, package/build commands and environment diagnostics;
- running the application or CLI;
- browser/Playwright flows;
- Computer Use or equivalent host-native interactive validation;
- MCP/plugin-backed tool execution;
- log/trace inspection;
- bounded independent review;
- non-overlapping technical diagnosis;
- bounded technical repair when writable ownership is explicit and safe.

Availability is capability-dependent. D068 does not claim every Executor host exposes every named tool.

## Coordinator-first delegation rule

D068 strengthens D065 for Stage 6 tool execution.

```text
materially separable execution/diagnostic slice
+ compatible child/worker surface
+ no dominating safety/ownership anti-trigger
=> delegate the slice
```

One ceremonial worker does not satisfy this rule when several material, separable, noise-heavy execution slices exist and compatible workers are available.

The root may execute a slice directly when:

- the operation is tiny/tightly serial;
- worker orientation cost exceeds the value;
- mutable ownership would overlap unsafely;
- the child surface lacks required tools/permissions/reliability;
- exact controller topology is contract-fixed;
- another concrete safety/capability constraint dominates.

The handoff remains compact and need not expose private worker transcripts or chain-of-thought.

## Executor repair authority

When execution finds an implementation defect, the Executor may repair it without returning to ChatGPT if the correction preserves the approved semantics and Design.

In-authority repair examples include:

- implementation bugs;
- type/runtime errors;
- build failures;
- technical test defects;
- lint/format defects;
- compatibility defects already covered by the Design;
- incorrect selectors/paths/config wiring;
- edge cases and races whose correct behavior is already specified;
- implementation simplification needed to satisfy approved constraints.

The Executor MUST rerun affected verification after repair.

Out-of-authority findings include any need to:

- change a material requirement;
- alter public/product behavior not already authorized;
- change controlling architecture/trust boundaries materially;
- change acceptance criteria or thresholds;
- weaken semantic tests/oracles;
- close an explicitly open gap;
- introduce a new material dependency/privilege/risk outside the approved envelope;
- reinterpret ambiguous Design/Plan authority.

Those findings produce `BLOCKED`/`PARTIAL` plus explicit upstream re-entry evidence.

## Candidate correction synchronization

Executor repairs make the prior Library snapshot stale.

After Executor Stage 6 reaches a terminal represented GitHub branch state, ChatGPT SHALL re-materialize that corrected remote state into the Library working plane before semantic acceptance when Library state is retained for the task.

Required alignment:

```text
Executor corrected/pushed topic branch
-> ChatGPT fetch/materialize exact remote state
-> create replacement Library snapshot
-> checksum/archive validation
-> safe extract
-> git fsck
-> verify expected branch/HEAD/tree/receipt
-> promote current task snapshot
-> revalidate promoted current
-> GitHub topic branch == represented Library task snapshot
-> Converge / Accept
```

A stale pre-Executor snapshot MUST NOT be treated as the accepted task state.

## Stage 7 — ChatGPT Converge / Accept / Integrate / Evolve

ChatGPT compares:

- objective/specification/Design/Plan;
- final GitHub candidate branch;
- Executor verification/repair handoff;
- relevant tests/evidence;
- synchronized Library representation when retained.

Only ChatGPT performs semantic acceptance and integration authorization.

After acceptance:

- integrate through protected PR flow;
- refresh the canonical target Library snapshot when Library mode is in use;
- validate/promote/revalidate under D066;
- perform only evidence-safe snapshot GC and lock/workspace cleanup;
- evolve current specification/checkpoint state;
- close the ChatGPT objective under D067.

## GitHub write-amplification objective

For D068 work, the normal remote pattern is:

```text
GitHub reads/bootstrap
-> verified topic branch identity
-> many local/Library edits and local Git operations
-> bounded candidate publication checkpoint
-> Executor verification/repair publication
-> PR/integration
-> final canonical verification
```

This replaces per-edit GitHub mutation as the normal authoring loop.

Corrective publications are allowed when review/re-entry requires them. The goal is bounded meaningful synchronization, not an artificial one-commit rule.

## Relationship to D054

D054 remains controlling for actual execution mechanics.

ChatGPT owns candidate materialization, but does not need to become the default shell/browser/operator. Executor workers own compatible command/API/SDK/browser/computer-use mechanics during Stage 6 and resolve executable syntax using the accepted runbook/official-source procedure.

Human interaction remains reserved for genuine Human/MFA/credential/risk gates or explicit Human requests.

## Relationship to D060

D060 still gives one Human-visible Executor Coordinator root to the exact Task/Operational Contract lifecycle.

D068 changes what that root primarily does:

```text
old default: implement + verify
new D068 default: coordinate execution + diagnose + repair + verify
```

Same-task follow-up remains `CONTINUE` when the root is recoverable.

## Relationship to D066

D066 supplies the workspace/transport primitives. D068 turns those primitives into the preferred working plane for candidate materialization when capabilities are available.

D066 unresolved gaps remain unresolved. D068 does not invent orphan recovery, TTL/heartbeat, ownership transfer, closed-unmerged resume, automatic retirement / GC selection, unusual-ref canonicalization, or unqualified ruleset behavior.

## Grandfathering and T058

D068 is prospective. Historical executed Task Contracts, handoffs, reviews, and evidence retain the authority and meaning they had when executed; this decision does not rewrite them retroactively.

T058 is no longer frozen or blocked. Its canonical lifecycle state is:

- accepted and integrated by PR #313;
- operationally closed through OP071 / PR #315;
- its previous Coordinator root is retired for unrelated work.

D068 does not reopen or redesign T058. The historical T058 Task Contract, handoffs, reviews, and evidence remain historical records rather than being reinterpreted as if D068 governed them.

## Legacy-document precedence

Current source-maintenance documentation is normalized prospectively to D068. Any preserved historical or grandfathered wording describing the earlier Stage 5/6 split or a planning-only merge to `develop` retains only its original historical scope.

For new D068-mode source-maintenance work, D068 controls: ChatGPT owns Stage 5 complete candidate materialization; the Executor owns Stage 6 execution, diagnosis, bounded technical repair and verification; and a coherent published topic-branch candidate is sufficient authority for Executor verification without a separate planning/candidate merge to `develop`.

No new executable task may rely on the old conflicting boundary without explicit grandfathered authority.

## Effective rule

```text
new D068-mode task
-> ChatGPT specifies/designs/plans/materializes complete candidate in local Git/Library
-> publish coherent authority + candidate to verified GitHub topic branch
-> Codex Coordinator uses workers to execute/diagnose/repair/verify
-> technical defects may be repaired inside authority
-> semantic/design/acceptance defects return to ChatGPT
-> corrected GitHub state is re-synchronized to Library
-> ChatGPT converges/accepts/integrates/closes objective
```
