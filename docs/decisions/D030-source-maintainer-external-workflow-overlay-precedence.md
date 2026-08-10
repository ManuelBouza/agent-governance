# D030 — Source-maintainer external workflow overlay precedence

Status: ACCEPTED
Authority: Human Owner / ChatGPT Orchestrator under D022 and D026

## Problem

The source repository may be executed from an agent host that has pre-existing workflow overlays such as SDD, review-driven development, receipt gates, commit/push hooks, Skill registries, memory, or other agent-development infrastructure.

T001 exposed a concrete authority collision: OpenCode was running with Gentle-AI Receipt-Driven Development (RDD), whose native review authority escalated the candidate and stopped delivery before the repository's own D022/D029 handoff flow could complete.

Agent Governance already has a source-maintenance authority chain: Human Owner -> ChatGPT Orchestrator review -> persisted Task Contract/review directives -> Agente de IA Ejecutor -> pushed handoff -> ChatGPT acceptance -> PR. A host overlay MUST NOT silently become a second review, acceptance, commit, push, PR, or release authority for this source repository.

## Decision

External executor-host capabilities SHALL be classified by capability boundary before use in source maintenance.

- `REUSE` or `COEXIST` is allowed when the external capability is non-authoritative and does not alter the repository's Task Contract, ownership, review, acceptance, handoff, branch, PR, or release semantics.
- `ADAPT` is allowed only through an explicit bounded source-maintenance disposition persisted by ChatGPT.
- `CONFLICT` applies when an external workflow claims overlapping review/delivery authority or blocks the D022 execution/handoff sequence.
- unresolved `CONFLICT` fails closed.

When a conflicting external overlay supports a narrower local opt-out, prefer the narrowest available scope. Do not disable a user's global workflow merely to operate this repository.

## Source authority rule

For `agent-governance` source maintenance, the authoritative delivery/review sequence is the one defined by `AGENTS.md`, D022, Task Contracts, persisted review directives, D029 handoff identity, and ChatGPT remote review.

An external host or ecosystem may provide execution, search, memory, Skill discovery, test assistance, or other non-overlapping capabilities. It does not acquire acceptance authority because it is installed in the executor environment.

If an external review/delivery gate stops an otherwise authorized source task:

1. stop; do not bypass the gate implicitly;
2. identify the capability/authority collision;
3. persist a ChatGPT source-maintenance disposition;
4. if the external tool provides a narrowly scoped opt-out, use only that scope after authorization;
5. verify the resulting mode/state;
6. continue under repository-native policy;
7. record the disposition in the executor handoff when material.

## Gentle-AI RDD adapter disposition

Gentle-AI is a supported example of an external executor-host ecosystem, not a dependency of Agent Governance.

Gentle-AI's current public RDD contract states that review mode is user-owned; a clone can opt out with `--scope clone`; when review is disabled, native delivery gates defer to ordinary repository policy rather than fabricating approval.

For the Agent Governance source repository, Gentle-AI RDD review/delivery authority is classified `CONFLICT` because D022 already assigns review/acceptance authority to ChatGPT and repository contracts.

Therefore, when Gentle-AI RDD is present and blocks source-maintenance delivery, the approved adaptation is clone-local only:

```text
gentle-ai review mode status --cwd .
gentle-ai review mode disable --scope clone --cwd .
gentle-ai review mode status --cwd .
```

Requirements:

- run from the intended Agent Governance clone;
- MUST include `--scope clone` on disable;
- MUST NOT disable RDD globally as part of source maintenance;
- do not initialize or migrate Agent Governance into Gentle-AI SDD merely to satisfy the gate;
- do not treat Gentle-AI `disabled/unmanaged` as Agent Governance approval; it only means delivery is delegated back to repository policy;
- ChatGPT still performs the required remote review before any implementation PR is opened/merged.

Re-enabling Gentle-AI RDD for another clone/project remains the Human Owner's choice and is outside Agent Governance source state.

## Repository mutation boundary

A clone-local external-tool setting is workstation/clone operational state, not canonical product state.

It MUST NOT be committed as a generated Gentle-AI/SDD footprint unless a future Task Contract explicitly authorizes such an adapter artifact.

If the opt-out command changes tracked or untracked repository files, the executor must stop and report the exact delta before continuing.

## Relationship to D026

D026 remains the product-level capability-first/reuse-before-install/no-authority-collision policy, especially for consumer repositories.

D030 applies the same principle to development of the Agent Governance source product itself. It does not change the Governance Core protocol and does not make Gentle-AI a canonical integration dependency.

## Research basis

Gentle-AI public documentation:

- https://github.com/Gentleman-Programming/gentle-ai

Current documented behavior used by this decision:

- review mode is user-owned;
- clone-local disable is supported with `--scope clone`;
- a clone-local disabled source wins without disabling review globally;
- disabled native delivery gates defer to ordinary repository policy (`disabled/unmanaged`) rather than issuing approval.

## Consequences

- T001 R1 may continue after a persisted clone-local Gentle-AI RDD opt-out.
- the Gentle-AI escalation remains useful evidence that coexistence detection works; it is not a reason to add Gentle-AI to the source toolchain.
- future executor hosts with comparable review/delivery overlays follow the same capability/authority classification rather than receiving product-specific governance authority.
- source tasks should stop and escalate when no safely scoped adaptation exists.
