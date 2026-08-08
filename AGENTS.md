# Agent Governance Product Repository

## Repository role

This repository develops and tests the reusable Agent Governance product. It is NOT an installed consumer-project instance.

- Canonical protocol source: `governance-core/`.
- Governance Skill design: `docs/GOVERNANCE-SKILL-CONTRACT.md` and `docs/GOVERNANCE-SKILL-PACKAGE.md`.
- Product decisions: `docs/decisions/`.
- Governance Skill implementation: `governance-skill/` when release gates permit it.
- Product tests/evals: `tests/` and `evals/`.

Do not infer application missions/tasks from this repository and do not create a live `.agent-coordination/` instance merely because the product defines that installed format.

## Product boundaries

- Keep the Governance Core agent-product neutral.
- Keep consumer mission/task/state out of this repository except minimal synthetic fixtures under tests/evals.
- The Governance Skill is operational tooling, never authority over the Core.
- Do not author final `governance-skill/SKILL.md` until the documented release gate is satisfied.
- Tests/evals validate Governance/Skill behavior, not application implementation quality.

## Change discipline

When changing protocol behavior, update the smallest relevant Core module, applicable product decision/design documentation, and focused tests/evals. Preserve progressive context loading and avoid duplicating normative rules.

External Skill research for this product follows `governance-core/SKILL-DISCOVERY.md` and `governance-core/SKILL-SUPPLY-CHAIN.md`.
