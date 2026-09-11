# Maintainer Skill — Task Contract Template Usage

Status: REQUIRED PACKAGE REFERENCE  
Owner: ChatGPT Orchestrator  
Template: `TASK-CONTRACT-V4-TEMPLATE.md`  
Controlling policy: `../../docs/TASK-CONTRACTS.md`

## Rule

For every **new or materially revised source-product executable Task Contract**, the Maintainer Skill Orchestrator route MUST use `TASK-CONTRACT-V4-TEMPLATE.md` as its structural starting point/checklist.

The template is not independent authority and does not override `AGENTS.md`, `docs/TASK-CONTRACTS.md`, accepted Decisions, the current checkpoint, or task-specific specification/Design authority. Its purpose is to prevent structural drift and ensure that durable execution semantics remain in Git.

The Orchestrator route MUST verify before Executor launch that the persisted Task Contract carries every material instruction required for execution, including when applicable:

- objective and current specification carrier;
- requirement/specification delta;
- controlling Design and Plan/Trace;
- Stage ownership and published candidate identity;
- authorized scope and exclusions;
- invariants/constraints;
- acceptance and verification evidence;
- D076 materialization boundary;
- version-sensitive gates;
- stop/re-entry conditions;
- handoff/evidence requirements;
- terminal return shape;
- Human launch state.

Sections that are not applicable may be removed rather than populated ceremonially. Material requirements MUST NOT be omitted merely to keep the contract short.

## Thin transport enforcement

The Maintainer Skill MUST treat the Human-visible chat/terminal launch prompt as transport/bootstrap only.

Normal task launch transport is limited to the minimum information needed to enter the correct governed context: Coordinator/session identity where required, canonical repository, the Task Contract pointer, and enough candidate identity/bootstrap context to load the exact authorized Git state.

The launch prompt MUST NOT duplicate task semantics already present or required in canonical Git, including objective, Design, Plan/Trace, detailed scope/exclusions, experiment matrix, retry logic, acceptance criteria, evidence schema, test commands, version-specific runbooks, or stop conditions.

If substantive execution instructions appear necessary in the launch prompt, the Orchestrator route MUST stop before launch and persist them into the Task Contract or another referenced canonical authority.

D055 launch-profile presentation remains separate from the Task Contract and normally separate from the transport prompt.

## Revision rule

A Task Contract created before this template may remain historical. When it is **materially revised for new execution authority**, the Orchestrator route MUST normalize the active contract against this template before launch rather than compensating for missing fields through chat-only instructions or review/checkpoint prose.

## Future SKILL.md requirement

When the Maintainer Skill `SKILL.md` is eventually implemented, its Orchestrator route MUST load/apply this reference whenever the active work creates, materially revises, reviews for readiness, or launches an executable source-product Task Contract.

The future Skill MUST preserve the no-Skill bootstrap path and MUST NOT make this template a substitute for canonical repository policy.
