# D017 — Separate maintainer and consumer Skills

Status: ACCEPTED
Authority: Human Owner

## Decision

Agent Governance SHALL use two distinct Agent Skills with non-overlapping operational purposes:

1. **Maintainer Skill** — operates only when developing, refactoring, testing, evaluating, or releasing the canonical `agent-governance` source product.
2. **Consumer Governance Skill** — installs, bootstraps, validates, operates, recovers, hands off, audits, and archives governance inside an adopting repository.

The two Skills MAY reuse source code and canonical Governance Core artifacts, but they MUST have separate activation descriptions, trigger/eval corpora, operational instructions, permission expectations, and release surfaces.

## Maintainer boundary

The Maintainer Skill may know source-repository-specific paths and workflows such as `AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, `docs/REFACTORING-WORKFLOW.md`, release policy, product tests/evals, and source layout.

It MUST NOT create a consumer `.agent-coordination/` instance in this repository or treat the source repository as a governed application project.

## Consumer boundary

The Consumer Governance Skill MUST remain project/domain neutral and MUST NOT require users to modify, clone, or have write access to the canonical source repository after installation.

Consumers use an immutable release/tag/commit artifact. Installed governance must remain operable from the consumer repository even when the canonical source repository is unavailable.

The Consumer Skill MUST NOT load source-product maintenance decisions, PD/RF workflows, or maintainer-only context during normal operation.

## Rationale

Source-product maintenance and consumer-project governance have different triggers, context, permissions, mutation targets, risks, and expected outcomes. Combining them into one Skill would broaden activation, load irrelevant context, and create an avoidable path for consumer agents to confuse upstream product maintenance with local governance operation.

## Consequences

- `governance-skill/` denotes the consumer-facing Governance Skill.
- `maintainer-skill/` denotes the source-product Maintainer Skill.
- Consumer and maintainer trigger/eval suites are separated.
- Shared implementation MAY live in reusable source modules rather than duplicated Skill instructions.
- Neither Skill becomes authority over the Governance Core.
