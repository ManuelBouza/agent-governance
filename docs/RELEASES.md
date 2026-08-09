# Release Policy

Agent Governance uses semantic versioning for protocol/product releases.

## Branch relationship

Release operation follows `docs/BRANCHING.md`:

- `main` is the latest accepted stable/potentially releasable state;
- `develop` is the next unreleased integration state;
- normal topic branches merge to `develop`;
- release promotion normally occurs by PR from `develop` to `main`;
- optional `release/<semver>` branches are used only when stabilization must proceed while `develop` continues;
- exceptional `hotfix/<semver>` branches start from `main` and their effective fix is propagated to `develop`.

Published tags/releases originate from `main` only.

## Stability levels

- `0.x` — pre-1.0 public releases; each tag is a stable published artifact even though interfaces/package layout may still evolve between minor releases.
- `1.x` — first stable public contract; backward-compatible additions use minor versions and compatible clarifications/fixes use patch versions.
- major version — incompatible protocol or installed-footprint behavior.

## Stable release gate

Do not publish `v1.0.0` until all of the following are true:
1. Governance Core modules are internally consistent and versioned;
2. consumer Governance Skill activation/trigger contract is finalized;
3. source-product Maintainer Skill activation/trigger contract is finalized sufficiently for supported maintenance/release workflows;
4. `governance.py` CLI contracts and template field sets are finalized;
5. deterministic governance/Skill tests pass;
6. agent-facing governance/Skill evals meet documented thresholds;
7. portability is demonstrated across at least two distinct agent adapters;
8. Skill discovery and supply-chain security checks are covered;
9. bootstrap/install/upgrade/uninstall behavior is documented and tested;
10. public licensing, contribution, branch, and security policies are present;
11. release artifacts contain no consumer-project state or private data;
12. consumer Governance operation does not require read/write access to the canonical source repository after installation.

## Release artifacts

A release may include:
- canonical Governance Core;
- consumer Governance Skill package;
- bootstrap/templates and deterministic tooling;
- checksums or equivalent artifact identity information;
- migration notes when installed footprint or protocol behavior changes.

The Maintainer Skill, tests, eval fixtures, and product-development history may remain repository-only unless deliberately published for maintainers/contributors.

## Compatibility

A release must document:
- protocol version;
- supported installed-footprint version;
- known adapter limitations;
- migration requirements;
- security-relevant changes.

## Immutable consumption

`develop` is unreleased development state and MUST NOT be used as a consumer dependency.

`main` is stable but still a moving branch. Consumers SHOULD pin a release/tag or immutable commit according to their supply-chain policy. Published `v*` tags are intended to be immutable identities.
