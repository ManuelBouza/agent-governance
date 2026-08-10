# T003 — D032 deterministic policy-contract foundation

Status: READY
Type: test/eval + fix
Base branch: `develop`
Expected topic branch: `test/d032-deterministic-contract`
Expected executor handoff: `handoffs/T003-executor-handoff.json`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Restore deterministic harness alignment after D032 and add the smallest repository-owned mechanical contract that encodes D032 properties which do not require model interpretation.

T003 has two coherent responsibilities:

1. repair post-D032 deterministic drift in the accepted T001 harness so canonical Core version/module checks reflect current `develop`;
2. add a synthetic, data-driven D032 policy corpus and deterministic tests for interaction-register engineering invariance, quality-routing constraints, Primary Solution Diagram selection, and diagram refresh invalidation.

T003 does **not** claim to verify that ChatGPT, OpenCode, another model, or a future Consumer Skill correctly interprets arbitrary natural language. Agent-facing behavior remains a separate future eval increment under `docs/TESTING-AND-EVALUATION.md`.

## Current deterministic regression to characterize

Current `develop` contains D032 with:

- `governance-core/GOVERNANCE.md` protocol version `1.10.0`;
- new required Core modules `INTERACTION.md` and `QUALITY.md`.

The existing deterministic harness still contains:

- `SOURCE_PROTOCOL_VERSION = "1.9.0"` in `tests/_helpers.py`;
- `CORE_REQUIRED_MODULES` without `INTERACTION.md` and `QUALITY.md`.

Therefore the current source bytes imply that `test_governance_core_uses_documented_protocol_version` is stale/failing against D032-era `develop`. T003 must characterize that mismatch before mutation and then repair it without weakening the version assertion.

## Controlling references

Read and follow:

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`
- `docs/decisions/D030-source-maintainer-external-workflow-overlay-precedence.md`
- `docs/decisions/D031-gentle-ai-skill-registry-source-maintainer-boundary.md`
- `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`
- `docs/ARCHITECTURE-INTENT-ENGINEERING-PROXY.md`
- `governance-core/INTERACTION.md`
- `governance-core/QUALITY.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/LIFECYCLE.md`
- accepted T001/T002 deterministic harness on current `develop`

## Primary Solution Diagram

Dominant design question: local verification workflow/dependency change with no new runtime architecture.

Preferred view under D032: compact flow/dependency diagram.

```text
D032 Core (read-only)
INTERACTION + QUALITY + LIFECYCLE
              │
              ▼
     Synthetic D032 cases (JSON)
     ┌────────┼─────────┬──────────┐
     │        │         │          │
 register   quality   diagram    refresh
 variants   routing   selection   invalidation
     │        │         │          │
     └────────┴────┬────┴──────────┘
                   ▼
        Deterministic test-local model
                   │
      ┌────────────┼──────────────┐
      ▼            ▼              ▼
 engineering   material-only   correct diagram/
 invariance     disclosure      stale-on-change
      │            │              │
      └────────────┴──────┬───────┘
                          ▼
       protocol/module drift checks
       1.10.0 + INTERACTION + QUALITY
                          │
                          ▼
              canonical locked gate
              pytest + Ruff + no network
```

The diagram represents the proposed T003 solution and is current for this Task Contract. A material change from a deterministic test-local contract into model-driven/runtime behavior invalidates this diagram and requires ChatGPT contract/diagram revision before execution continues.

## Quality-envelope disposition

D032 quality triage for this increment:

- **Functional correctness / acceptance fidelity — MATERIAL:** T003 repairs a known deterministic mismatch and must not weaken the version/module invariant.
- **Architecture / coexistence — BASELINE:** no production architecture or authority surface changes; D030/D031 host coexistence rules remain unchanged.
- **Security — BASELINE, explicitly triaged:** synthetic local data only; no secrets, credentials, untrusted executable content, public/network surface, privilege, authentication or production state.
- **Privacy / data governance — NOT_APPLICABLE:** fixtures contain no personal, confidential, regulated or consumer/business data.
- **Reliability / resilience — BASELINE:** deterministic local tests must be repeatable and fail loudly.
- **Performance / resources — BASELINE:** fixture corpus must remain small; no load/performance layer is justified.
- **Observability / operability — BASELINE:** pytest failure names/messages and handoff evidence are sufficient for this local harness increment.
- **Testability / verification — MATERIAL:** this is the primary purpose of T003.
- **Maintainability / change isolation — MATERIAL:** use data-driven fixtures and test-local helpers; do not add a production policy engine.
- **Compatibility / migration — MATERIAL:** accepted T001/T002 tests and toolchain must remain green; no protocol rollback to 1.9.0 is allowed.
- **Usability / accessibility / internationalization — NOT_APPLICABLE:** no end-user interface is introduced.
- **Dependency / supply chain — BASELINE:** no new packages or external runtime/eval services.
- **Deployment / rollback / release safety — BASELINE:** repository-only test artifacts; implementation must be independently revertible.
- **Safety / compliance — NOT_APPLICABLE** beyond repository safety/ownership rules already controlling the source product.

No additional threat model or DFD is justified because T003 introduces no material security trust boundary or sensitive data flow.

## Verification-layer decomposition

`docs/TESTING-AND-EVALUATION.md` requires the least probabilistic verifier that can prove the property.

T003 therefore covers only deterministic/mechanical D032 contract properties.

A later Task Contract must cover model-dependent behavior such as:

- interpreting semantically equivalent natural-language requests at different registers;
- choosing what technical detail to surface in real conversations;
- preserving supplied code semantics in generated technical responses;
- recognizing material quality concerns from natural-language scenarios;
- producing/using the correct diagram in an actual agent planning session.

T003 fixtures MAY be designed for later reuse by those evals, but no model call, transcript grader, hosted eval service or Agent Skill activation is authorized here.

## Checkout / branch precondition

Before mutation:

1. fetch current canonical `develop` containing this exact READY Task Contract;
2. verify tracked working state is clean;
3. create `test/d032-deterministic-contract` from that `develop` revision;
4. permit normal Gentle-AI Skill Registry `.atl/` local operation under D031, but do not commit `.atl/` contents;
5. keep Gentle-AI RDD clone-locally disabled under D030 and do not alter global state.

Do not write directly to `develop` or `main`.

## Required pre-mutation characterization

Before changing tests, run the narrowest deterministic check that demonstrates the known protocol drift, for example:

```text
uv run --locked python -m pytest tests/test_canonical_layout.py::test_governance_core_uses_documented_protocol_version
```

Record the exact result in the handoff. The expected mismatch is current Core `1.10.0` versus stale harness expectation `1.9.0`.

If the check unexpectedly passes because current `develop` changed after this contract was authored, stop and persist `PARTIAL` rather than silently rewriting the contract premise.

## Authorized scope

The executor may modify/create only the minimum non-Markdown artifacts needed for this increment, expected to include:

- `tests/_helpers.py`;
- a non-Markdown synthetic D032 corpus under `tests/fixtures/d032/`, preferably JSON;
- one focused Python module such as `tests/test_d032_policy_contract.py`;
- existing Python tests only if a small mechanical alignment is necessary and clearly justified;
- `handoffs/T003-executor-handoff.json`.

Do not create production/runtime policy code. Test-local helpers are preferred.

## Required harness alignment

Repair, do not weaken, existing deterministic invariants:

1. `SOURCE_PROTOCOL_VERSION` must match canonical D032-era Core protocol `1.10.0`.
2. `CORE_REQUIRED_MODULES` must include `INTERACTION.md` and `QUALITY.md` in addition to previously required modules.
3. Existing canonical layout/version tests must remain strict: do not replace exact version/module assertions with looser checks merely to make the suite green.
4. No D032 Markdown may be changed by the executor.

## Required synthetic D032 policy corpus

Use explicit mechanical fields. Do not parse arbitrary natural-language prose to infer D032 semantics in T003.

The corpus must cover at least these property families.

### 1. Interaction-register engineering invariance

Represent at least one semantic engineering case through multiple presentation registers, including:

- plain/domain;
- practitioner/technical or expert/architecture;
- code-native.

Equivalent variants must share an explicit engineering identity/fingerprint and must require the same normalized engineering controls, acceptance meaning and material quality decisions. Presentation metadata may differ.

Tests must mechanically prove that changing only presentation register cannot change the engineering fingerprint/required controls for the equivalent case.

### 2. Code-native semantic preservation fixture

Include at least one code-native case with explicit supplied identifiers/schema/command tokens and an expected preserved-token set.

The deterministic test verifies corpus/contract preservation exactly. It does not generate new code or claim model behavior.

### 3. Quality routing

Represent quality outcomes using explicit mechanical facts rather than natural-language inference.

Cover at minimum:

- `BASELINE` concern that requires no special Human-visible disclosure;
- `MATERIAL` concern that constrains the execution contract;
- `MATERIAL` concern with explicit Human impact that must be surfaced;
- `NOT_APPLICABLE` concern that must not produce user-visible checklist noise;
- security present in every scenario as an explicitly triaged dimension;
- at least one scenario proving privacy can be `MATERIAL` independently from a non-material/baseline cybersecurity posture.

Tests must fail if:

- a `MATERIAL` requirement is omitted from the scenario's contract-control set;
- a user-visible concern is not `MATERIAL` and Human-impacting;
- a `BASELINE`/`NOT_APPLICABLE` item is surfaced merely as checklist noise;
- security triage is absent;
- privacy is mechanically collapsed into the security field.

### 4. Primary Solution Diagram selection

Cover every D032/QUALITY dominant-question mapping with explicit expected values:

- system/actor boundary -> C4 System Context;
- application/service/data-store boundary -> C4 Container;
- internal component/dependency boundary -> C4 Component;
- temporal participant collaboration -> dynamic/sequence;
- lifecycle/state transition -> state diagram;
- sensitive/untrusted data and trust boundaries -> DFD with trust boundaries;
- persistent entity/relationship structure -> ER/data model;
- local workflow/algorithm/dependency -> compact flow/dependency diagram.

Product/user labels must not determine diagram selection; only the explicit dominant-question fact may do so.

### 5. Diagram refresh invalidation

Represent at least:

- no design change -> no refresh required;
- cosmetic/local implementation detail preserving solution -> no refresh required;
- material architecture/data-flow/state/responsibility change -> refresh required before readiness.

Tests must mechanically enforce those outcomes.

## Deterministic model boundary

Any classifier/router/helper created by T003 is test infrastructure only.

It MUST NOT:

- become a public Governance runtime API;
- infer intent from free-form Human text;
- call an LLM;
- claim to simulate full ChatGPT/Consumer Skill behavior;
- introduce a second normative source competing with D032/INTERACTION/QUALITY.

The fixtures/tests encode explicit policy examples so future regressions are observable.

## Explicit exclusions

Do NOT in T003:

- edit/create/delete committed `*.md` as the executor;
- modify D032, `INTERACTION.md`, `QUALITY.md`, `GOVERNANCE.md` or `LIFECYCLE.md`;
- downgrade Core protocol version to 1.9.0;
- weaken exact version/module assertions;
- implement production interaction/quality/diagram routing code;
- add model/LLM calls, agent sessions, transcript graders or hosted eval services;
- implement Consumer/Maintainer Skill trigger evals;
- add Hypothesis/state-machine testing;
- add new dependencies or modify `pyproject.toml`, `uv.lock` or `.python-version`;
- install or execute real external SDD products as test dependencies;
- reconfigure Gentle-AI RDD or global/workstation tools;
- commit `.atl/` contents;
- open or merge an implementation PR before ChatGPT remote acceptance.

## Invariants / constraints

- `presentation complexity != engineering quality` remains normative.
- D032/INTERACTION/QUALITY are the semantic authority; test fixtures encode examples but do not redefine them.
- Equivalent register variants preserve engineering controls and acceptance meaning.
- Security is explicitly triaged in every synthetic implementation scenario.
- Privacy remains a distinct dimension.
- Only material/Human-impacting concerns become Human-visible in fixtures; baseline internal discipline does not become checklist noise.
- Primary diagram selection follows dominant design question, not product label or user technicality.
- Material design-boundary changes invalidate diagram readiness until refresh.
- No new dependency or network/runtime service is required.
- T001 and T002 accepted regression coverage remains green.
- No Agent Skill or external SDD activation is required by the deterministic suite.

## Acceptance criteria

ChatGPT may accept T003 only if:

1. execution begins from current `develop` containing this exact Task Contract;
2. work occurs on `test/d032-deterministic-contract`;
3. the known 1.9.0 vs 1.10.0 drift is characterized before mutation and then repaired by aligning the harness to current Core, not by weakening Core/tests;
4. `INTERACTION.md` and `QUALITY.md` become mechanically required Core modules in the deterministic harness;
5. a minimal synthetic D032 corpus exists in non-Markdown format;
6. register-variant tests prove equivalent cases retain the same engineering fingerprint/controls/acceptance facts;
7. code-native fixture checks preserve explicit supplied tokens exactly;
8. quality-routing tests cover `BASELINE|MATERIAL|NOT_APPLICABLE`, Human-visible materiality, mandatory security triage and independent privacy routing;
9. all eight Primary Solution Diagram mapping families are mechanically covered;
10. diagram refresh tests distinguish none/cosmetic from material solution-boundary changes;
11. classification/routing logic is test-local and generic, with no branches based on product/user labels;
12. no Markdown, dependency, lockfile, Python-version, production runtime, external SDD or committed `.atl/` scope is introduced;
13. focused T003 tests pass;
14. accepted T001/T002 regression tests remain green;
15. canonical locked verification passes completely;
16. test runtime requires no network or credentials;
17. `handoffs/T003-executor-handoff.json` accurately records implementation/evidence under D029;
18. the implementation branch is committed and pushed before visible completion;
19. visible executor response contains only STATUS/HANDOFF/BRANCH/HEAD.

## Verification requirements

Run focused checks during implementation, then the canonical complete gate:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

The final handoff must record:

- pre-mutation protocol-drift characterization command/result;
- exact focused T003 commands/results;
- complete full-suite pass/fail/skip/collected counts;
- Python/uv/pytest/Ruff versions;
- exact fixture/test files added or modified;
- protocol constant and Core-module-list alignment;
- register-invariance cases;
- quality-routing cases;
- all diagram-selection families;
- diagram refresh cases;
- confirmation that test helpers remain test-local and no model/runtime API was introduced;
- dependency/config/network/credential facts;
- D031 `.atl/` local/uncommitted evidence when present;
- D030 clone-local RDD disposition without global mutation;
- branch/base/implementation identity and clean tracked state;
- unresolved issues, if any.

## Stop / escalation conditions

Stop and persist `BLOCKED` or `PARTIAL` instead of guessing if:

- current `develop` no longer exhibits the characterized 1.9.0/1.10.0 mismatch before mutation;
- D032/INTERACTION/QUALITY leave a required deterministic mapping ambiguous;
- satisfying a property requires interpreting arbitrary natural language or calling a model;
- a proposed fix would weaken accepted T001/T002 assertions;
- a new dependency, production runtime module or committed Markdown is required;
- canonical tests fail for an unrelated regression outside authorized test scope;
- global/workstation mutation would be required.

## Expected persisted handoff

Before returning, create/update:

`handoffs/T003-executor-handoff.json`

Follow `docs/EXECUTOR-HANDOFFS.md` and D029. The JSON must identify the committed implementation/test state using `implementation_head_sha`; the visible executor response reports the actual pushed final branch HEAD after handoff finalization.

## Visible executor response

After handoff finalization is committed and pushed, return only:

`STATUS: DONE | BLOCKED | PARTIAL`

`HANDOFF: handoffs/T003-executor-handoff.json`

`BRANCH: test/d032-deterministic-contract`

`HEAD: <actual-pushed-final-branch-head-sha>`
