# T016 — Consumer Skill final-authoring test transition

Task ID: T016
Status: READY_AFTER_PLANNING_MERGE
Type: test-maintenance
Base branch: `develop`
Expected topic branch: `test/consumer-skill-final-authoring-transition`
Expected executor handoff: `handoffs/T016-executor-handoff.json`

## Objective

Retire the now-completed T015 sequencing assertion that final `governance-skill/SKILL.md` must not exist, while preserving the permanent source-repository isolation guarantees before ChatGPT integrates the final Consumer Governance Skill Markdown.

T015 used absence of `governance-skill/SKILL.md` as a pre-authoring release-gate assertion. T015 is accepted, integrated and cleaned up, so that absence is no longer a product invariant. The permanent invariant remains that the source checkout must not contain live consumer runtime state.

## Required outcome

Make the smallest deterministic test-only change needed so the accepted T015 suite no longer requires `governance-skill/SKILL.md` to be absent after its release gate has closed.

Preserve explicit assertions that this source checkout has no live:

- `.agent-governance/`
- `.agent-coordination/`

The transition must not weaken corpus integrity, source independence, coexistence coverage, Consumer-vs-Maintainer separation, fail-closed grading, or any T014 runtime test.

## Boundaries

Executor owns implementation process but scope is deliberately narrow.

Executor MAY edit only:

- `tests/test_consumer_governance_trigger_corpus.py` as required for this transition;
- `handoffs/T016-executor-handoff.json`.

Executor MUST NOT edit committed Markdown, `governance-skill/SKILL.md`, the T015 corpus/grader, Governance Core, Consumer runtime implementation, package assets, Maintainer Skill state, dependencies, lockfiles or configuration.

Do not add a replacement assertion that attempts to validate final `SKILL.md` before ChatGPT authors it. Final Skill content/readiness is owned by the later focused release review.

## Acceptance

Remote Git evidence must show only the authorized test change plus executor handoff.

The focused test must pass:

```text
uv run --locked pytest -q tests/test_consumer_governance_trigger_corpus.py
```

Required repository gates:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The handoff must record executor identity, exact base SHA, implementation anchor SHA, changed paths, focused/full verification, dependency/config changes and limitations.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
TASK: T016
BRANCH: <implementation-branch>
BASE_SHA: <exact-base-sha>
HEAD_SHA: <exact-head-sha>
HANDOFF: handoffs/T016-executor-handoff.json
FOCUSED_PYTEST: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
```
