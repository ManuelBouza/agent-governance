# Consumer Governance Skill Status

Status: FINAL-AUTHORED / RELEASE-BLOCKED

This directory contains the **consumer-facing Governance Skill** defined by:
- `../docs/GOVERNANCE-SKILL-CONTRACT.md`
- `../docs/GOVERNANCE-SKILL-PACKAGE.md`

It is intentionally separate from `../maintainer-skill/`, which exists only for development/refactoring/testing/release work on the canonical source product.

The final `SKILL.md` activation/routing artifact has been authored after acceptance of the deterministic package/tooling foundation, trigger/eval corpus, and final-authoring test transition.

Consumer Governance Skill v1 is **not yet release-approved**. Focused release review R1 identified a deterministic package/runtime completeness blocker: the stable v1 CLI contract requires `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, and `archive`, while the current integrated CLI exposes only `bootstrap` and `validate`.

Release remains blocked until the missing v1 deterministic command surfaces are implemented, independently reviewed, integrated, and the focused release review is rerun successfully.

Canonical authority remains in `../governance-core/`, consumer-project state remains in each adopting repository, and consumer operation MUST NOT require read/write access to this source repository after installation.
