# T002 — Synthetic coexistence fixtures and reference-target corpus

Status: READY
Type: test/eval infrastructure
Base branch: `develop`
Expected topic branch: `test/coexistence-fixtures`
Expected executor handoff: `handoffs/T002-executor-handoff.json`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Extend the accepted deterministic harness with a focused, repository-owned synthetic fixture corpus that mechanically exercises ecosystem coexistence and reference-target classification without installing or executing real third-party SDD/Skill products.

T002 must make the generic D026 / `governance-core/COEXISTENCE.md` capability model testable as deterministic input -> expected classification/ownership outcomes for representative synthetic repository shapes.

This increment establishes fixtures and deterministic classification assertions only. It does not implement model-driven coexistence judgment, behavioral agent evals, state-machine/property testing, real third-party integration, or Consumer/Maintainer Skill trigger evaluation.

## Readiness status

T001 is accepted and integrated into `develop`, providing the locked uv/Python/pytest/Ruff harness required by this task.

D026 and `governance-core/COEXISTENCE.md` already define the generic coexistence semantics required here. `docs/TESTING-AND-EVALUATION.md` explicitly requires synthetic coexistence fixture families and deterministic `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` coverage without making external products release dependencies.

No additional architecture decision is required for this bounded increment. This Task Contract is `READY` only after this Markdown planning change is merged into `develop`.

## Controlling references

Read and follow:

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`
- `docs/decisions/D030-source-maintainer-external-workflow-overlay-precedence.md`
- `governance-core/COEXISTENCE.md`
- accepted T001 harness/configuration on current `develop`

## Approved toolchain

Use the existing repository-managed T001 harness only:

- uv compatible with repository `tool.uv.required-version`;
- Python `>=3.13` through the existing `.python-version` / uv environment;
- pytest `>=9,<10`;
- Ruff `>=0.16,<0.17`;
- Python standard library first;
- existing `pyproject.toml` and `uv.lock`.

T002 does not authorize new dependencies. In particular, do not add Hypothesis, external SDD SDKs/CLIs, Agent Skill packages, model/eval SDKs, schema libraries, Docker, Node.js, or other tooling.

Do not alter workstation/global tools. Gentle-AI RDD remains governed by D030 and the existing clone-local disposition; T002 must not re-enable, reconfigure, or depend on it.

## Checkout / branch precondition

Before mutation:

1. fetch current canonical `develop` containing this exact READY Task Contract and accepted T001;
2. verify the working tree is clean for tracked files;
3. create `test/coexistence-fixtures` from that current `develop`;
4. verify Git/uv and ordinary repository push capability;
5. do not mutate external untracked host-overlay state such as `.atl/`.

Do not write directly to `develop` or `main`.

## Authorized scope

The executor may create/modify only non-Markdown test/evidence artifacts required for this increment, including:

- synthetic fixture data under `tests/fixtures/` using non-Markdown formats such as JSON, TOML, YAML only if parsable with existing dependencies/stdlib, plain text without `.md`, or directory/file shapes that do not require committed Markdown;
- Python tests under `tests/`;
- small Python helper modules under `tests/` when needed to load/classify fixture evidence;
- `handoffs/T002-executor-handoff.json`.

Existing `pyproject.toml`, `.python-version`, `uv.lock`, and `.gitignore` are expected to remain unchanged. Any claimed need to change dependencies or source-toolchain configuration is a stop/escalation condition unless ChatGPT first persists a contract revision.

## Required fixture families

Implement the smallest coherent deterministic corpus that represents these generic capability situations without requiring live third-party products:

1. **No-SDD / no-third-party-Skill**
   - no native SDD/spec/task provider exists;
   - absence itself is valid and must not imply installation of an SDD framework;
   - classification can express `MISSING` only for a specifically required capability, not as a repository defect by default.

2. **SDD provider sufficient — REUSE**
   - synthetic native spec/plan/task provider already covers the required capability;
   - Governance should reference/reuse the provider rather than duplicate equivalent artifacts.

3. **SDD provider plus bounded Governance metadata — ADAPT**
   - native provider remains primary owner of specs/plans/tasks;
   - a bounded Governance reference/adapter is required without mirroring the native source of truth.

4. **Distinct non-overlapping providers — COEXIST**
   - two capabilities have clearly separate ownership surfaces and can operate side by side.

5. **Authority/ownership overlap — CONFLICT**
   - two systems claim the same plan/task/governance/managed-instruction ownership or equivalent authority;
   - deterministic evidence must produce a fail-closed conflict outcome rather than silently selecting a winner.

6. **Same-name Skill shadowing / host precedence**
   - project/user synthetic Skill candidates share a name;
   - deterministic host precedence/selection evidence is observable;
   - selection must remain distinct from Governance approval/trust.

7. **Managed instruction/config collision**
   - a synthetic third-party-managed surface would be overwritten by an attempted Governance writer;
   - expected outcome is preservation/adapter path when composition evidence exists, otherwise `CONFLICT`.

8. **Known-system-shaped examples without hard-coding product authority**
   - include minimal synthetic shapes modeled on publicly documented patterns for Gentle-AI-like, Spec Kit-like, and OpenSpec-like ecosystems;
   - product names may label fixtures for traceability, but classification logic must operate on generic capability/ownership facts rather than `if product == ...` branches.

A generic custom-SDD fixture may be used to prove the classifier is not limited to named examples.

## Deterministic classification model

T002 may implement test-local helpers that map explicit synthetic evidence to expected classifications:

- `REUSE`
- `ADAPT`
- `COEXIST`
- `MISSING`
- `CONFLICT`

The helper/model is test infrastructure, not a new public Governance runtime or new authority tier.

Classification inputs must be explicit mechanical facts in fixtures, such as:

- required capability;
- provider presence;
- provider capability coverage;
- artifact/surface owner;
- whether a bounded adapter/reference is needed;
- whether two providers claim the same write/authority surface;
- selected Skill identity/precedence evidence;
- whether safe composition of a managed surface is mechanically represented.

Do not infer semantic intent from arbitrary natural-language third-party files in this task.

## Required assertions

Tests must prove at minimum:

1. every required fixture has an explicit expected classification and the deterministic classifier returns it;
2. `REUSE` does not create duplicate owned spec/plan/task artifacts in the synthetic expected outcome;
3. `ADAPT` preserves native ownership and represents only a bounded Governance reference/adapter need;
4. `COEXIST` requires non-overlapping ownership/capability surfaces;
5. overlapping write/authority ownership produces `CONFLICT` and cannot be downgraded to `COEXIST` by product-name precedence;
6. no-SDD fixtures remain valid without external installation;
7. same-name Skill host precedence identifies the selected candidate but does not mark it approved/trusted;
8. a different selected artifact from an approved artifact identity is represented as conflict/unapproved rather than silently accepted;
9. managed instruction/config collision preserves the external owner or fails closed when safe composition is unavailable;
10. named external-system fixture labels do not affect the generic classification outcome when capability/ownership facts are otherwise identical;
11. fixtures/tests make no network calls and execute with no real Gentle-AI, Spec Kit, OpenSpec, Skill registry, consumer repository, or production service;
12. the existing T001 regression suite remains green.

## Fixture quality constraints

- Fixtures are synthetic product-test assets only; no real consumer/business state.
- Keep each fixture minimal enough that the expected classification can be audited from its explicit fields/file shape.
- Prefer data-driven parametrization over duplicating one test function per product label.
- Avoid fixtures that encode entire third-party repositories or copy copyrighted third-party documentation/content.
- Named examples should reproduce only the minimal public integration shape needed for the test.
- Do not create committed Markdown fixtures because Markdown ownership belongs to ChatGPT; use non-Markdown synthetic representations for T002.
- Do not create live `.agent-governance/` or `.agent-coordination/` state at repository root; any such names used in fixtures must be nested disposable/synthetic test data only and must not act as living product state.

## Explicit exclusions

Do NOT in T002:

- edit/create/delete committed `*.md` as the executor;
- change Governance Core semantics or D026 classifications;
- implement production/bootstrap capability inventory code unless a later Task Contract explicitly creates that product surface;
- install or invoke real Gentle-AI, Spec Kit, OpenSpec, or another SDD system as a test dependency;
- initialize or refresh external registries such as `.atl/`;
- reconfigure Gentle-AI RDD;
- install Agent Skills;
- perform supply-chain network discovery or audit real external artifacts;
- implement Consumer/Maintainer Skill trigger evals;
- implement model-based/LLM coexistence classification evals;
- implement state-machine/property testing or add Hypothesis;
- add behavioral agent sessions/transcript graders;
- add security/adversarial dynamic execution beyond the deterministic collision cases stated above;
- change `pyproject.toml`, `uv.lock`, `.python-version`, or `.gitignore` without a persisted contract revision;
- add production/runtime code merely to make tests pass;
- open or merge a PR before ChatGPT reviews the pushed implementation and handoff.

## Invariants / constraints

- D026 / `COEXISTENCE.md` control classification semantics; tests may encode them but cannot redefine them.
- Product names are fixture examples, never branches in Governance authority semantics.
- Classification evidence is routing/test state, not authority.
- One owner per overlapping write/authority surface remains fail-closed.
- External managed surfaces are preserved.
- Host Skill selection/precedence remains distinct from exact artifact approval/trust.
- No-SDD remains a supported valid mode.
- The deterministic suite remains executable with no Agent Skill or external SDD activated.
- T002 does not turn test-local helpers into normative product runtime APIs.
- All verification remains local and deterministic for identical fixture/repository inputs.

## Acceptance criteria

ChatGPT may accept T002 only if:

1. execution starts from current `develop` containing this READY Task Contract and accepted T001;
2. work occurs on `test/coexistence-fixtures`;
3. no committed Markdown is modified by the executor;
4. no new dependency or toolchain configuration change is introduced;
5. the required fixture families above are represented with minimal synthetic evidence;
6. tests mechanically exercise all five D026 classifications;
7. named-system examples are classified from generic facts rather than hard-coded product-name logic;
8. reuse/adapt assertions preserve native spec/plan/task ownership rather than creating parallel truth;
9. conflict cases fail closed for overlapping authority/write surfaces;
10. Skill precedence tests separate host selection from Governance approval/trust;
11. managed-surface collision tests preserve owner boundaries or produce conflict;
12. no live external product/service/network/consumer repository is required by test runtime;
13. existing T001 tests remain green with no weakening;
14. canonical verification passes completely;
15. `handoffs/T002-executor-handoff.json` accurately describes the pushed implementation and evidence under D029;
16. executor commits and pushes the reviewable branch before returning status;
17. visible response contains only STATUS/HANDOFF/BRANCH/HEAD.

## Verification requirements

Run focused tests while implementing as useful, then run the canonical complete gate:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

The final handoff must record:

- exact focused and canonical commands;
- complete pytest pass/fail/skip/collected counts;
- Python/uv/pytest/Ruff versions;
- fixture families/files added;
- classification cases covered, including all five outcomes;
- confirmation that product labels do not control classification logic;
- confirmation that no real external SDD/Skill dependency or test-runtime network was used;
- confirmation that repository dependency/configuration files remain unchanged;
- `git status`/branch/base/implementation identity evidence;
- unresolved issues, if any.

## Stop / escalation conditions

Stop and persist `BLOCKED` or `PARTIAL` instead of guessing if:

- D026 / `COEXISTENCE.md` does not determine an expected classification for a required fixture without new semantic judgment;
- a test requires changing public Governance semantics rather than mechanically encoding existing rules;
- a required fixture cannot be represented without committed Markdown and the executor would need to violate file ownership;
- implementation appears to require new runtime production code or a new dependency;
- a real third-party product must be installed/executed to establish the expected result;
- a conflict between current `develop` and this contract materially changes scope;
- canonical T001 tests regress and the cause cannot be corrected within T002's authorized test/fixture surface;
- global/workstation mutation would be required.

## Expected persisted handoff

Before returning, create/update:

`handoffs/T002-executor-handoff.json`

Follow `docs/EXECUTOR-HANDOFFS.md` and D029. The JSON must identify the committed implementation/test/fixture state using `implementation_head_sha`; the visible executor response reports the actual pushed final branch HEAD after handoff finalization.

Include at minimum:

- `task_id: T002`;
- `status`;
- `task_contract_path`;
- branch/base/base SHA;
- `implementation_head_sha`;
- files changed;
- fixture-family inventory;
- classification-case inventory;
- implementation rationale;
- verification commands/results/tool versions;
- dependency/configuration delta (`none` expected);
- provisioning-network and test-runtime-network facts;
- external ecosystem required/modified facts (`false` expected for repository assets/dependencies);
- Git status/commit/push evidence;
- unresolved issues;
- `chatgpt_read_path: handoffs/T002-executor-handoff.json`.

## Visible executor response

After handoff finalization is committed and pushed, return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/T002-executor-handoff.json`

`BRANCH: test/coexistence-fixtures`

`HEAD: <actual-pushed-final-branch-head-sha>`

Do not open or merge a PR.
