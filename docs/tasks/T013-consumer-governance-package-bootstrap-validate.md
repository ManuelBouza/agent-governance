# T013 — Consumer Governance package bootstrap and validate foundation

Task ID: T013
Status: READY
Type: implementation/test
Base branch: `develop`
Expected topic branch: `feat/consumer-governance-bootstrap-validate`
Expected executor handoff: `handoffs/T013-executor-handoff.json`

## Objective

Implement the first deterministic Consumer Governance Skill package increment defined by `docs/CONSUMER-GOVERNANCE-SKILL-V1-RELEASE-GATE.md`: canonical vendor-neutral template assets plus safe local `bootstrap` and structural `validate` behavior.

## Required outcome

Create the consumer package assets under `governance-skill/` and deterministic implementation/tests that prove:

- required v1 template assets exist and contain no project/vendor defaults;
- bootstrap can materialize the canonical consumer footprint in disposable unrelated repositories;
- bootstrap refuses unsafe pre-existing target/managed-file collisions rather than overwriting them;
- installed consumer output is operable without access to this source checkout;
- validate checks required layout, Core presence/reference/version structure, JSON/JSONL syntax and source/consumer separation and fails closed on unsupported/ambiguous structural state;
- no live `.agent-governance/` or `.agent-coordination/` footprint is created in this source checkout outside disposable synthetic fixtures;
- no production/external provider/network/model judgment is required for correctness.

The stable CLI path is `governance-skill/scripts/governance.py`. T013 needs only safe `bootstrap` and `validate`; later Tasks own the other reserved v1 subcommands.

## Boundaries

Executor owns implementation process. It may edit only authorized non-Markdown implementation, deterministic test/eval fixtures as needed, consumer package template assets required by this Task, and the executor handoff.

Executor MUST NOT edit committed Markdown, including this contract, Governance Core, decisions, architecture, reviews, checkpoint or final `governance-skill/SKILL.md`.

Executor MUST NOT implement the Maintainer Skill, contact production/external systems, introduce provider/model verification, install live third-party Skills/SDD products, replace an existing SDD methodology, or create tracked consumer runtime state in this source repository.

Prefer standard library and existing locked repository dependencies; dependency changes require material justification in the handoff and remain subject to review.

## Acceptance

Remote Git evidence must show only authorized non-Markdown changes and a persisted handoff. Required gates:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

Focused deterministic tests must also prove bootstrap success, overwrite refusal, structural validation failure cases, source independence and source-repository footprint isolation.

The handoff must record executor identity, base SHA, implementation anchor SHA, changed paths, focused/full verification, dependency/config changes and limitations.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
TASK: T013
BRANCH: <implementation-branch>
BASE_SHA: <exact-base-sha>
HEAD_SHA: <exact-head-sha>
HANDOFF: handoffs/T013-executor-handoff.json
FOCUSED_PYTEST: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
```
