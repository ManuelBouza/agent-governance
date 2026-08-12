# T008 — EGLL deterministic learning-detector MVP

Task ID: T008  
Status: READY  
Type: infrastructure  
Base branch: `develop`  
Expected topic branch: `test/egll-deterministic-learning-detectors`  
Expected executor handoff: `handoffs/T008-executor-handoff.json`

## Objective

Implement the deterministic source-maintainer MVP for D039's Evidence-Driven Governance Learning Loop (EGLL): stable learning fingerprints, replay fixtures, local repository-state detectors, machine-readable findings, and regression tests that prove representative failure classes are detected without model/provider/network dependencies.

T008 hardens the Agent Governance source-maintenance process. It does not change Governance Core consumer semantics.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D039-evidence-driven-governance-learning-loop.md`
- `docs/ARCHITECTURE-GOVERNANCE-LEARNING-LOOP.md`
- `docs/GOVERNANCE-LEARNING.md`
- `docs/BRANCHING.md`
- `docs/BRANCH-CLEANUP.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- D022 source-product change procedure
- D037 deterministic code-only verification
- accepted T007 evidence/reviews only as regression-source facts

## Authorized scope

The Agente de IA Ejecutor is authorized to add or modify non-Markdown source-maintenance verification artifacts necessary for the deterministic EGLL MVP, including:

- a small deterministic learning-signal/fingerprint representation;
- local detector/helper code under repository-appropriate non-Markdown paths;
- deterministic JSON/JSONL fixtures representing compliant and noncompliant repository/workflow states;
- focused pytest tests for fingerprints and detector behavior;
- machine-readable detector output suitable for future CI/status-check integration;
- bounded local Git metadata interpretation when represented through fixtures or an isolated temporary repository created by tests;
- the persisted non-Markdown T008 executor handoff.

The executor MAY refactor adjacent non-Markdown test helpers only when required to avoid duplication and only if behavior remains covered.

## Required MVP fingerprints

At minimum, implement deterministic representation/replay coverage for:

1. `git.branch.post_merge_advance`
   - bad case: merged PR reviewed head differs from the current surviving source-branch head;
   - good case: merged PR reviewed head equals current source-branch head, or the source branch is already absent.

2. `git.branch.delete_before_review_resolution`
   - bad case: a destructive branch disposition is attempted while the candidate is still unresolved/`REVIEW` or lacks deletion-authorizing evidence;
   - good case: deletion is permitted only after an explicit resolved disposition and required identity evidence.

3. `task.handoff.identity_mismatch`
   - bad cases include expected branch/handoff path/task identity disagreeing with persisted/returned evidence;
   - compliant identity produces no mismatch finding.

4. `task.done_requires_rework`
   - represent a formal accepted-review fact where an executor returned `DONE` but the Orchestrator persisted rework;
   - emit a learning candidate fingerprint without treating it automatically as blame or task failure.

5. explicit persisted procedural nonconformance
   - detect/normalize a machine-readable handoff field or fixture representing procedural nonconformance into a stable learning candidate finding.

The T007 incidents SHALL be represented as synthetic regression fixtures, not by depending on mutable live branch state.

## Finding contract

Each detector finding MUST expose enough stable structured data for deterministic review and future aggregation, including at least:

- fingerprint;
- detector identifier/version or equivalent stable implementation identity;
- severity/classification appropriate to the detector contract;
- subject/reference identity from the fixture/input;
- deterministic reason/evidence fields;
- whether the finding is blocking, advisory, or learning-candidate-only under the accepted policy.

Do not encode agent product names or individual blame into fingerprints.

The exact schema is executor-owned implementation detail unless a material architecture ambiguity is discovered. Keep it minimal and versionable.

## Explicit exclusions

The executor MUST NOT:

- create or edit committed Markdown;
- modify `governance-core/` consumer protocol semantics;
- implement consumer EGLL state or create `.agent-governance/` / `.agent-coordination/` live source-repo footprints;
- modify T006/D035/D036 semantics or implementation;
- add live LLM/model calls, model-as-judge behavior, provider dependencies, or probabilistic verification;
- require network access in the core T008 test path;
- add a required external policy engine/service such as OPA;
- configure GitHub rulesets, branch protection, required checks, Actions workflows, or live GitHub API enforcement in this MVP;
- implement trend aggregation beyond what is minimally necessary to expose stable machine-readable fingerprints;
- automatically create/modify Governance policy, Task Contracts, decisions, learning Markdown records, or acceptance state;
- infer root cause or Human intent from detector findings;
- weaken existing tests, branch policy, D037, or security controls.

## Invariants / constraints

```text
automatic detection != governance authority
finding != root cause
fingerprint != blame
written lesson != verified learning
model reflection != verification authority
```

The detector layer consumes explicit facts and emits deterministic findings. It does not decide architecture or remediation.

For every required fingerprint, tests MUST include both positive and negative controls so a detector cannot pass merely by flagging all inputs.

Synthetic T007 fixtures MUST preserve the semantic distinction between:

- unsafe action before ambiguity resolution; and
- later exact-SHA authorized deletion after persisted disposition.

The `git.branch.post_merge_advance` replay MUST prove the merged-branch freeze invariant introduced after T007.

## Required execution sequence

1. Start from current `develop` containing accepted D039, `docs/GOVERNANCE-LEARNING.md`, and this exact T008 contract.
2. Create `test/egll-deterministic-learning-detectors` from that `develop` revision.
3. Inspect existing test/helper conventions and choose the smallest coherent non-Markdown implementation surface.
4. Implement the stable finding/fingerprint representation.
5. Add synthetic fixtures for the required good/bad cases, including T007-derived regressions.
6. Implement deterministic detectors/replay interpretation.
7. Add focused tests proving positive detection, negative controls, stable fingerprint identity, and no model/network dependency.
8. Run focused tests, full pytest, Ruff check, and Ruff formatting checks.
9. Persist `handoffs/T008-executor-handoff.json` with exact implementation/evidence identity.
10. Commit and push all authorized work, then return only the canonical minimal executor response.

## Acceptance criteria

ChatGPT accepts T008 only when remote evidence shows:

- all five required MVP signal classes have stable deterministic findings;
- T007-derived synthetic bad states reproduce the intended fingerprints;
- corresponding compliant/control states do not emit those fingerprints;
- `git.branch.post_merge_advance` catches surviving merged-branch head drift deterministically;
- deletion-before-resolution is distinguishable from deletion after explicit authorized resolution;
- Task Contract/handoff identity mismatch is mechanically testable;
- `task.done_requires_rework` is a learning candidate rather than an automatic blame/failure verdict;
- procedural nonconformance can be normalized from structured evidence;
- findings are machine-readable and agent-product neutral;
- no live network/model/provider/external-policy-engine dependency exists in the core verification path;
- no committed Markdown or Governance Core consumer semantics changed;
- existing test suite remains green;
- handoff identity is remotely auditable under D029/D021 conventions.

## Verification requirements

Required commands:

```text
uv run --locked pytest -q tests/test_governance_learning.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

If the executor chooses a different focused test filename, that filename MUST be established in the handoff and the equivalent focused command MUST be run in addition to the full suite. Do not remove the full-suite/Ruff gates.

The handoff must include:

- branch/base/head identity;
- changed-file inventory;
- implemented fingerprint catalog;
- fixture inventory and mapping to required good/bad cases;
- detector/finding schema summary;
- exact verification commands/results;
- statement confirming no Markdown/Governance Core/network/model/provider/ruleset/Actions scope expansion;
- any discovered ambiguity or procedural nonconformance.

## Stop / escalation conditions

Return `BLOCKED` or `PARTIAL` rather than inventing semantics if:

- a required fingerprint cannot be represented deterministically without changing its accepted D039 meaning;
- implementation would require live GitHub/network state in the core MVP;
- a material finding schema decision would create new Governance authority;
- satisfying the task would require committed Markdown changes;
- existing repository test architecture materially conflicts with the contract;
- a required T007 fact cannot be represented safely as synthetic fixture evidence;
- a new dependency or external service appears necessary.

## Sequencing

T008 executes after outstanding post-integration branch cleanup and before T006.

After T008 is accepted, integrated, and post-integration branch cleanup is verified, resume T006 unchanged. Do not implement D036 before T006 closes.

## Expected handoff

Persist `handoffs/T008-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push it on `test/egll-deterministic-learning-detectors`, then return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T008-executor-handoff.json
BRANCH: test/egll-deterministic-learning-detectors
HEAD: <pushed-commit-sha>
```
