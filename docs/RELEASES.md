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

## Verification policy

`docs/TESTING-AND-EVALUATION.md` is normative for test/eval architecture, isolation, fixture policy, grader selection and release thresholds.

Mechanical invariants use deterministic code tests where practical. Probabilistic agent behavior uses repeated isolated eval trials. Project-defined numeric thresholds are local release policy and are not represented as universal industry standards.

## Stable release gate

Do not publish `v1.0.0` until all of the following are true:
1. Governance Core modules are internally consistent and versioned;
2. consumer Governance Skill activation/trigger contract is finalized;
3. source-product Maintainer Skill activation/trigger contract is finalized sufficiently for supported maintenance/release workflows;
4. `governance.py` CLI contracts and template field sets are finalized;
5. deterministic governance/Skill regression tests pass 100%;
6. configured property/state-machine release runs have zero unresolved counterexamples;
7. mandatory agent-facing governance/Skill evals meet the thresholds in `docs/TESTING-AND-EVALUATION.md`;
8. portability is demonstrated across at least two distinct supported agent adapters/fixtures;
9. Skill discovery and supply-chain security checks are covered, including exact artifact identity/revocation/drift behavior;
10. release-blocking adversarial/security fixtures are rejected or contained as expected;
11. bootstrap/install/upgrade/uninstall behavior is documented and tested;
12. public licensing, contribution, branch, testing, and security policies are present;
13. release artifacts contain no consumer-project state or private data;
14. consumer Governance operation does not require read/write access to the canonical source repository after installation;
15. representative release eval transcripts/outcomes and all release-blocking failures have been reviewed before acceptance.

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
