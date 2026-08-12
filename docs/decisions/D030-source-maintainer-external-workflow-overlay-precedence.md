# D030 — Source-maintainer external workflow overlay precedence

Status: ACCEPTED
Authority: Human Owner / ChatGPT Orchestrator under D022 and D026

Supersession note: `docs/decisions/D038-external-review-receipt-delivery-integrity-provider-boundary.md` supersedes only the blanket Gentle-AI RDD capability disposition below. D030 remains authoritative for general external-workflow precedence and for the clone-local RDD opt-out fallback when D038-compatible bounded coexistence is unavailable.

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

D038 adds a more precise alternative for Gentle-AI RDD: reuse/adapt subordinate candidate-integrity/evidence capabilities when they preserve D037 and Governance authority. A stricter selected-provider denial remains a real technical blocker for that provider path, but the provider cannot grant Governance acceptance or expand authorization.

## Gentle-AI RDD adapter disposition

Gentle-AI is a supported example of an external executor-host ecosystem, not a dependency of Agent Governance.

Gentle-AI's public RDD contract supports clone-local review-mode opt-out and ordinary repository-policy fallback when review is disabled.

### Historical/base disposition

Before D038, the Agent Governance source repository classified Gentle-AI RDD review/delivery as one `CONFLICT` surface because D022 already assigns review/acceptance authority to ChatGPT and repository contracts.

D038 now classifies RDD **by capability**:

- subordinate deterministic/native candidate identity, receipt/integrity, Git re-derivation and provider status/recovery may be `REUSE`/`ADAPT`;
- probabilistic reviewer findings may only `COEXIST` as supplemental evidence under D037;
- external Task Contract/scope/acceptance/merge/release authority remains `DENY`/`CONFLICT`.

Use D038 when the installed provider exposes a compatible bounded capability surface.

### Clone-local fallback

When D038-compatible bounded coexistence is unavailable, incompatible, or would make probabilistic reviewer approval a required source-product gate, the approved fallback remains clone-local only:

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
- ChatGPT still performs the required remote review before any implementation PR is opened/merged;
- do not disable a currently selected D038 provider path merely to bypass a negative integrity result without an explicit Strategy/Human disposition change and revalidation.

Re-enabling Gentle-AI RDD for another clone/project remains the Human Owner's choice and is outside Agent Governance source state.

## Repository mutation boundary

A clone-local external-tool setting is workstation/clone operational state, not canonical product state.

It MUST NOT be committed as a generated Gentle-AI/SDD footprint unless a future Task Contract explicitly authorizes such an adapter artifact.

If the opt-out command changes tracked or untracked repository files, the executor must stop and report the exact delta before continuing.

## Relationship to D026

D026 remains the product-level capability-first/reuse-before-install/no-authority-collision policy, especially for consumer repositories.

D030 applies the same principle to development of the Agent Governance source product itself. It does not change the Governance Core protocol and does not make Gentle-AI a canonical integration dependency.

D038 is a specialization of this capability-first rule, not a new authority tier.

## Research basis

Gentle-AI public documentation:

- https://github.com/Gentleman-Programming/gentle-ai

The original D030 disposition relied on documented clone-local disable and `disabled/unmanaged` fallback behavior. D038 contains the later capability-level research for candidate freezing, content-bound receipts, native delivery-integrity gates and the provider threat boundary.

## Consequences

- the original T001 collision remains valid audit evidence and is not rewritten;
- clone-local RDD opt-out remains an approved safe fallback;
- compatible subordinate RDD integrity capabilities may now be reused/adapted under D038 rather than disabling the entire surface by default;
- no provider receives Agent Governance acceptance authority merely because it can block or verify a technical delivery path;
- future executor hosts with comparable review/delivery overlays follow the same capability/authority classification rather than receiving product-specific governance authority;
- source tasks should stop and escalate when no safely scoped adaptation exists.
