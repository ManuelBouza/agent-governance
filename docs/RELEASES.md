# Release Policy

Agent Governance uses semantic versioning for protocol/product releases.

## Stability levels

- `0.x` — active design/development; interfaces and package layout may change.
- `1.x` — first stable public contract; backward-compatible additions use minor versions and compatible clarifications/fixes use patch versions.
- major version — incompatible protocol or installed-footprint behavior.

## Stable release gate

Do not publish `v1.0.0` until all of the following are true:
1. Governance Core modules are internally consistent and versioned;
2. Governance Skill activation/trigger contract is finalized;
3. `governance.py` CLI contracts and template field sets are finalized;
4. deterministic governance/Skill tests pass;
5. agent-facing governance/Skill evals meet documented thresholds;
6. portability is demonstrated across at least two distinct agent adapters;
7. Skill discovery and supply-chain security checks are covered;
8. bootstrap/install/upgrade/uninstall behavior is documented and tested;
9. public licensing, contribution and security policies are present;
10. release artifacts contain no consumer-project state or private data.

## Release artifacts

A release may include:
- canonical Governance Core;
- Governance Skill package;
- bootstrap/templates and deterministic tooling;
- checksums or equivalent artifact identity information;
- migration notes when installed footprint or protocol behavior changes.

Tests, eval fixtures and product-development history may remain repository-only unless useful to adopters.

## Compatibility

A release must document:
- protocol version;
- supported installed-footprint version;
- known adapter limitations;
- migration requirements;
- security-relevant changes.

The repository `main` branch is development state and must not be treated as an immutable approved dependency. Consumers should pin a release/tag or immutable commit according to their own supply-chain policy.
