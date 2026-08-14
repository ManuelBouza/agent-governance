# Consumer Governance Skill Status

Status: FINAL-AUTHORED / RELEASE-APPROVED

This directory contains the **consumer-facing Governance Skill** defined by:
- `../docs/GOVERNANCE-SKILL-CONTRACT.md`
- `../docs/GOVERNANCE-SKILL-PACKAGE.md`

It is intentionally separate from `../maintainer-skill/`, which exists only for development/refactoring/testing/release work on the canonical source product.

Consumer Governance Skill v1 has completed its deterministic release gate. Accepted package/bootstrap validation, trigger/eval corpus, final-authoring transition, and the complete seven-command CLI v1 runtime are integrated. Focused release review R2 closes the prior runtime-completeness blocker and confirms final `SKILL.md` routing against the actual packaged surface.

The stable deterministic CLI v1 surface is exactly `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, and `archive`.

Release approval does not make this Skill an authority source, does not claim runtime model trigger accuracy, and does not authorize production/external service access. Canonical authority remains in `../governance-core/`, consumer-project state remains in each adopting repository, and consumer operation MUST NOT require read/write access to this source repository after installation.
