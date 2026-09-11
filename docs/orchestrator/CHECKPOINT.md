# Orchestrator Checkpoint

Checkpoint-ID: O266  
Date: 2026-09-11  
Current-Objective: T063 — adaptive worker routing requalification  
State: T063_V4_TASK_CONTRACT_CANONICAL_STAGE6_AUTHORIZED_AWAITING_HUMAN_START  
Active-Executor: none — Codex selected for pending Human launch  
Executor-Launch-State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Coordinator-ID: `AG | agent-governance | T063 | root-4` — reserved NEW same-work-unit failover root; not yet started  
Task-Contract: `docs/tasks/T063-adaptive-worker-routing-requalification.md`  
Current-Launch-Review: `docs/reviews/T063-R8.md`  
T063-V4-Candidate-Branch: `test/t063-adaptive-worker-routing-requalification-v4`  
T063-V4-Candidate-HEAD: `f06c8f48f7b1d59dff9fc117cca5b42453ad23e8`  
T063-V4-Candidate-Base: `9da2b6fed64ded9af8d38f67cd53cd066abef838`  
Historical-T063-V3-Evidence-HEAD: `746519abc6f159e959120f68d5c9f920d88d5797`  
Historical-T063-V2-Evidence-HEAD: `3ff745a8d29e031ca818c1bc618b15a54e0cbf2b`  
Historical-T063-V1-Evidence-HEAD: `3d8a9460988351383a90adfc6b76e2deff056504`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

O265/R7 correctly authorized the scientific v4 candidate after the v3 empty-rollout reattachment race, but the active T063 Task Contract had not been normalized to carry the complete v4 execution authority. As a result, material execution semantics were duplicated into review/checkpoint prose and an oversized Human-visible transport prompt.

The Human identified that regression and required the v4 Task Contract to become the durable execution carrier and reusable template pattern.

ChatGPT Orchestrator therefore performed a documentation-only authority repair with zero provider/model calls:

1. materialized `maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md`;
2. materialized `maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md`;
3. updated `maintainer-skill/STATUS.md` so the eventual Maintainer `SKILL.md` must use those references for every new/materially revised Task Contract;
4. normalized `docs/tasks/T063-adaptive-worker-routing-requalification.md` as the complete canonical v4 Task Contract;
5. added T063-R8 accepting the authority/transport correction without changing experiment semantics.

The Maintainer Skill remains `DESIGN-APPROVED / NOT YET RELEASED`; no premature `SKILL.md` was created.

## Current T063 authority

The active execution specification is now the Task Contract itself:

```text
docs/tasks/T063-adaptive-worker-routing-requalification.md
```

It carries the complete v4 durable authority, including:

```text
candidate freeze
same-child empty-rollout reattach barrier
frozen child matrix/order
probe/oracle semantics
D063 mandatory receipts
D076 Stage 6 materialization boundary
D077 version gate
pre-provider gates
scoring/pilot decision
stop/re-entry conditions
evidence/handoff schema
terminal return shape
Human launch state
thin transport invariant
```

R7 remains the scientific v4 authorization/provenance review. R8 is the current authority-normalization review. The checkpoint records frontier only and MUST NOT become a substitute Task Contract.

## Scientific candidate

No scientific candidate change was made by this authority normalization:

```text
branch: test/t063-adaptive-worker-routing-requalification-v4
HEAD:   f06c8f48f7b1d59dff9fc117cca5b42453ad23e8
base:   9da2b6fed64ded9af8d38f67cd53cd066abef838
```

No additional provider/model call has occurred.

Historical v1/v2/v3 results remain excluded from v4 scoring.

## Task Contract template invariant

For every new or materially revised source-product executable Task Contract, the Maintainer Skill Orchestrator route must use:

```text
maintainer-skill/references/TASK-CONTRACT-V4-TEMPLATE.md
maintainer-skill/references/TASK-CONTRACT-TEMPLATE-USAGE.md
```

as structural starting point/readiness checklist.

Historical Task Contracts need not be rewritten solely because the template exists. If a historical contract is materially revised for new execution authority, normalize it against the template before launch.

The template does not override `docs/TASK-CONTRACTS.md` or other canonical policy; it operationalizes those requirements and prevents authority from leaking into transport prompts.

## Thin transport invariant

The Human-visible launch prompt is transport/bootstrap only.

For T063 v4 it may contain only the minimum necessary to enter the correct governed state:

```text
Coordinator title
canonical repository
NEW session
Task Contract path
exact authorized candidate branch@HEAD
load canonical Git authority and execute Task Contract
return only Task Contract-defined terminal result
```

D055 launch profile is shown to the Human separately.

Do NOT duplicate experiment matrix, retry logic, evidence schema, exclusions, version runbook, acceptance criteria or stop conditions in the transport prompt.

If future execution requires a substantive instruction that is not already in Git, stop before launch and revise the Task Contract or another canonical authority.

## Launch profile

Current D055 Human-facing launch card remains:

```text
Executor:        Codex
Surface:         Codex Desktop / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-4
Root model:      gpt-5.6-sol
Root reasoning:  medium
Codex runtime:   exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

This launch profile is not itself Task semantics and normally remains outside the transport prompt.

## Held and frozen work

T062/T023 remains on Human hold exactly as previously recorded. Do not execute its old continuation authority without new Human selection and revalidation.

T058 remains frozen by explicit Human decision. Do not resume, integrate, clean or copy it without new explicit Human authorization.

R007 remains `EVALUATING`; no global adaptive worker-routing policy is adopted.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint):

1. for T063 launch/convergence, load `docs/tasks/T063-adaptive-worker-routing-requalification.md` first;
2. load `docs/reviews/T063-R8.md` only for the transport/authority-normalization rationale;
3. load R7/R022/R021/D063/D076/D077 only when the Task Contract references require deeper interpretation or a concrete conflict arises;
4. for creation/material revision/readiness review of any source-product Task Contract, load the Maintainer Skill v4 template + usage reference;
5. for T062 resumption, load its separate held-line authority instead;
6. do not reconstruct frontiers from prior chat/Project Memory.

## Next Action

After this authority change is integrated into `develop`, T063 v4 remains authorized for Human-mediated Stage 6 launch.

Before launch, revalidate `develop`, exact candidate HEAD and D077 stable-release state.

Then present the D055 launch card separately and give the Human only the thin transport prompt defined by the canonical T063 Task Contract.

ChatGPT MUST NOT start or directly control Codex under D071.

After the Human returns the Task Contract-defined terminal four-line result, ChatGPT performs remote verification and Stage 7 convergence.
