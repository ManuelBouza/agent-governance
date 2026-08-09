# Consumer Governance Skill Status

Status: DESIGN-APPROVED / NOT YET RELEASED

This directory is reserved for the **consumer-facing Governance Skill** defined by:
- `../docs/GOVERNANCE-SKILL-CONTRACT.md`
- `../docs/GOVERNANCE-SKILL-PACKAGE.md`

It is intentionally separate from `../maintainer-skill/`, which exists only for development/refactoring/testing/release work on the canonical source product.

The final `SKILL.md` is intentionally not authored yet.

Before implementation/release, finalize and test the exact consumer activation/trigger corpus, CLI contracts, template field sets, deterministic validation surface, focused Governance/Skill eval contract, and source-repository-independence behavior.

Canonical authority remains in `../governance-core/`, consumer-project state remains in each adopting repository, and consumer operation MUST NOT require read/write access to this source repository after installation.
