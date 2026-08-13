# T014 — Consumer Governance bootstrap and validate implementation

Task ID: T014
Status: READY_AFTER_PLANNING_MERGE
Type: implementation/test
Base branch: `develop`
Expected topic branch: `feat/consumer-governance-bootstrap-validate-r2`
Expected executor handoff: `handoffs/T014-executor-handoff.json`

## Objective

Complete the deterministic Consumer Governance package foundation after the ChatGPT-owned Markdown templates are integrated.

## Required outcome

Implement only authorized non-Markdown work needed to satisfy the accepted T013 outcome: `governance-skill/scripts/governance.py`, required JSON/JSONL template assets, deterministic tests/fixtures, and handoff evidence proving safe `bootstrap` and structural `validate` behavior.

The following Markdown assets are controlling pre-existing inputs and MUST NOT be edited by the executor:
- `governance-skill/assets/MISSION.template.md`
- `governance-skill/assets/WORKPLAN.template.md`
- `governance-skill/assets/TASK.template.md`

Bootstrap must materialize the canonical consumer footprint in disposable unrelated repositories, refuse unsafe collisions rather than overwrite them, remain operable without source-repository access, and never create live consumer state in this source checkout outside disposable fixtures.

Validate must fail closed for missing required files, malformed/ambiguous structural state, malformed JSON/JSONL, protocol/Core structural inconsistency, and source/consumer separation violations.

## Boundaries

Executor MUST NOT edit committed Markdown, Governance Core, decisions, architecture, checkpoint, reviews, or `governance-skill/SKILL.md`. Do not implement Maintainer Skill behavior, contact production/external systems, use model/provider judgment as a correctness gate, install live third-party Skills/SDD products, or add tracked consumer runtime state to this source repository.

Prefer standard library and existing locked dependencies. Any dependency/config change requires explicit justification in the handoff.

## Acceptance

Required verification:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

Focused deterministic tests must prove bootstrap success, overwrite refusal, structural validation failures, source independence, Markdown-template consumption without modification, and source-repository footprint isolation.

The handoff must record executor identity, exact base SHA, implementation anchor SHA, changed paths, focused/full verification, dependency/config changes and limitations.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
TASK: T014
BRANCH: <implementation-branch>
BASE_SHA: <exact-base-sha>
HEAD_SHA: <exact-head-sha>
HANDOFF: handoffs/T014-executor-handoff.json
FOCUSED_PYTEST: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
```
