# T015 — Consumer Governance trigger/eval corpus

Task ID: T015
Status: READY_AFTER_PLANNING_MERGE
Type: implementation/test
Base branch: `develop`
Expected topic branch: `test/consumer-governance-trigger-corpus`
Expected executor handoff: `handoffs/T015-executor-handoff.json`

## Objective

Implement the repository-owned deterministic Consumer Governance Skill v1 trigger/eval corpus required before final `governance-skill/SKILL.md` authoring.

## Required outcome

Create only authorized non-Markdown eval definitions, fixtures and deterministic graders/harness additions needed to establish fixed positive, negative and near-miss partitions for the Consumer Governance activation boundary.

The corpus must distinguish at minimum:

- positive: explicit Agent Governance bootstrap/install, validate/reconstruct, mission/state/event/handoff, coexistence inspection, Governance Skill discovery/audit, and sequential-disclosure/readiness operations in an adopting repository;
- negative: generic planning, coding, testing, refactoring, release work, generic SDD workflows, generic Skill installation/search, source-product maintenance and ordinary application implementation;
- near-miss: generic spec/plan/tasks, feature/test work in a governed repo, generic Skill installation, Maintainer-only work, ordinary continuation of existing SDD artifacts, equivalent governance/orchestration overlap, and generic registry lookup without Governance context;
- coexistence: Gentle-AI-like, Spec Kit-like, OpenSpec-like, custom-SDD and no-SDD synthetic shapes, including preservation of third-party managed surfaces and refusal to install an unnecessary SDD;
- Consumer-vs-Maintainer separation and source-repository independence.

Use fixed train/validation partitions with stable case identifiers. Mechanical corpus integrity and partition rules must be graded deterministically. Do not require a live model/provider/model-as-judge for correctness in T015. If repeated probabilistic trigger trials require a later model-capable release-eval task, persist the corpus and deterministic harness boundary now without fabricating such evidence.

## Boundaries

Executor owns implementation process. It may edit only authorized non-Markdown files under `evals/`, deterministic tests/fixtures as needed, and the executor handoff.

Executor MUST NOT edit committed Markdown, `governance-skill/SKILL.md`, Governance Core, decisions, architecture, reviews, checkpoint, package runtime implementation from T014, or Maintainer Skill product state.

Do not contact production/external systems, install live third-party Skills/SDD products, create live `.agent-governance/` or `.agent-coordination/` state in the source checkout, or make any provider/model result a release authority.

## Acceptance

Focused deterministic verification must prove:

- fixed positive/negative/near-miss train and validation partitions exist and have unique stable IDs;
- no case appears in more than one partition/category;
- the minimum activation, non-activation, Consumer-vs-Maintainer and coexistence surfaces above are represented;
- fixtures are synthetic/disposable and source-repository independent;
- no final `governance-skill/SKILL.md` is authored;
- no live source-checkout consumer runtime footprint is created.

Required repository gates:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The handoff must record executor identity, exact base SHA, implementation anchor SHA, changed paths, corpus counts by partition/category, focused/full verification, dependency/config changes and any deferred probabilistic/model-backed eval work.

## Completion response

```text
STATUS: DONE | BLOCKED | PARTIAL
TASK: T015
BRANCH: <implementation-branch>
BASE_SHA: <exact-base-sha>
HEAD_SHA: <exact-head-sha>
HANDOFF: handoffs/T015-executor-handoff.json
CORPUS_CHECK: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
```
