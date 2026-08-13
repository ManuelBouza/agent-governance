# Consumer Governance Skill v1 Release Gate

Status: APPROVED-FOR-IMPLEMENTATION-PLANNING

## Sequencing

`governance-skill/SKILL.md` remains release-gated. Sequence: deterministic consumer package/tooling -> acceptance -> trigger/eval corpus -> final `SKILL.md` -> focused release review.

## Activation boundary

Activate only for explicit Agent Governance operations in an adopting repository: bootstrap/install, validate/reconstruct state, mission/state/event/handoff operations, coexistence inspection, Governance Skill discovery/audit, and sequential-disclosure/readiness checks.

Do not activate merely for generic planning/coding/testing/refactoring/release work, generic SDD workflows, generic Skill installation, source-product maintenance, or application implementation because Governance is present.

Near-miss evals must cover generic spec/plan/tasks, feature/test work in a governed repo, generic Skill installation, Maintainer-only work, equivalent governance overlap, and ordinary continuation of existing SDD artifacts.

## CLI v1

`governance-skill/scripts/governance.py` is the stable deterministic surface: `bootstrap`, `validate`, `state`, `event`, `skill`, `ecosystem`, `archive`.

T013 implements package foundation, vendor-neutral canonical templates, safe `bootstrap`, and structural `validate`. Later Tasks extend the remaining stable subcommands.

No production/external service dependency, model/provider correctness gate, strategic decision logic, or floating source-checkout dependency is allowed.

## Templates

Required assets remain those specified by `docs/GOVERNANCE-SKILL-PACKAGE.md`: MISSION, WORKPLAN, TASK, SKILL-APPROVAL, CAPABILITIES, STATE, and EXCHANGE templates. They contain placeholders only. WORKPLAN must not embed future-task implementation content; STATE remains constant-size frontier; approval records pin immutable artifact identity; capability classifications remain `REUSE|ADAPT|COEXIST|MISSING|CONFLICT`.

## T013 acceptance

Disposable synthetic repositories must prove bootstrap creates the consumer footprint safely, refuses unsafe collisions/overwrites, remains source-independent, and needs no network/provider/model service.

Structural validation must fail closed for missing required files, malformed or ambiguous protocol authority, malformed JSON/JSONL, source/consumer separation violations, reusable-asset contamination, forbidden live consumer footprints in this source repository, and bootstrap collision cases.

Tests must not create live `.agent-governance/` or `.agent-coordination/` state in the source checkout outside disposable fixtures.

## Before final SKILL.md

Repository-owned evals must provide fixed positive, negative, and near-miss partitions proving Consumer-vs-Maintainer separation, non-overlap with generic SDD/planning/testing, source independence, coexistence preservation, no-SDD operation without unsolicited SDD installation, and fail-closed governance/managed-file conflicts.

T013 does not author final `SKILL.md`, implement the Maintainer Skill, acquire/install external Skills live, contact production services, replace an SDD methodology, or add vendor-specific defaults.
