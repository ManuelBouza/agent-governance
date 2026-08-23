# T035 — Runbook Operation Resolution Readiness

## Identity

- Task ID: `T035`
- Status: `BLOCKED`
- Type: `mixed`
- Base branch: `develop`
- Expected topic branch: `feat/t035-runbook-operation-resolution-readiness`
- Expected executor handoff: `handoffs/T035-executor-handoff.json`
- SDD-Profile: `ASSURED`
- Test-Authorship-Mode: `mixed`
- Assurance-Class: `execution-control, protocol-readiness, persistence, security`
- Verification-Planes: `static, deterministic, security, portability, package`
- Release-Impact: `prepares backward-compatible runtime support for later D054 Core activation`
- Context-Impact: `focused bootstrap/validation/assets/tests only`

T035 is blocked until T034 is accepted and integrated with a green canonical baseline. T035 MUST NOT absorb or bypass T034's frozen native-SDD materialization contract.

## Objective

Prepare the deterministic Consumer runtime for D054 operation-resolution/runbook-recipe semantics without activating a new routed Core protocol version and without changing the stable Consumer CLI v1 command surface.

T035 adds the native demand-driven runbook/recipe footprint, recipe structural/trust validation and negative controls required so a later D040 Phase-B Markdown activation can make D054 part of routed Consumer Core without leaving `develop` red.

## Current specification carriers / controlling references

- `AGENTS.md`
- `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md`
- `docs/RUNBOOK-OPERATION-RESOLUTION.md`
- `docs/decisions/D033-execution-access-control-plane.md`
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/decisions/D041-executor-process-autonomy.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/CONFORMANCE-ORACLE-CONTRACT.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `governance-skill/assets/RUNBOOK.template.md`
- `docs/tasks/T034-native-sdd-executable-materialization.md`

## Dependency / sequencing

```text
D054 + T035 gate integrated
        -> T034 Implement + Code Review & Verify
        -> T034 Converge/Accept + integrate
        -> canonical develop green
        -> T035 Implement + Code Review & Verify
        -> T035 Converge/Accept + integrate
        -> D040 Phase-B D054 Core activation
```

During T034's bootstrap period, D054 already assigns command/API mechanics to the Executor and requires runbook reuse/official-documentation fallback, but durable native recipe persistence remains provisional until T035 exists.

## Requirement / specification delta

### ADDED

- **R-T035-1 — native runbook footprint**: Consumer bootstrap SHALL create `.agent-coordination/runbooks/` and `.agent-coordination/runbooks/recipes/` as safe project-owned coordination directories.
- **R-T035-2 — semantic runbook template materialization**: bootstrap SHALL copy the Orchestrator-owned `RUNBOOK.template.md` into the native runbook directory without changing its semantics.
- **R-T035-3 — recipe template materialization**: bootstrap SHALL include a valid `RUNBOOK-RECIPE.template.json` that exactly represents the staged D054 recipe field/state contract and starts as non-executable `CANDIDATE` template data.
- **R-T035-4 — deterministic recipe validation**: normal `validate` SHALL fail closed on malformed/unsafe native recipe records and enforce the structural/trust invariants required by `docs/RUNBOOK-OPERATION-RESOLUTION.md`.
- **R-T035-5 — material-runbook binding validation**: recipes declaring `REMOTE_EXECUTE`, `PRIVILEGE_ELEVATE`, `SECRET_USE`, `DEPLOY_SERVICE_CHANGE`, `DATA_MUTATE`, or `DESTRUCTIVE_IRREVERSIBLE` SHALL require a resolvable semantic runbook and step reference.

### MODIFIED

- **R-T035-6 — bootstrap coordination inventory**: the existing coordination skeleton expands only with the new runbook/recipe paths and templates.
- **R-T035-7 — validation surface**: the existing `validate` operation expands backward-compatibly to validate native runbook/recipe structure when present.

### REMOVED

- None. D054 routed Core activation is intentionally deferred.

### PRESERVED

- **R-T035-P1** — current routed `Protocol-Version` remains `1.14.0` throughout T035 implementation; no routed Core Markdown is edited.
- **R-T035-P2** — stable deterministic Consumer CLI v1 top-level command set remains exactly `bootstrap, validate, state, event, skill, ecosystem, archive`.
- **R-T035-P3** — runbooks/recipes do not grant D033 execution authority.
- **R-T035-P4** — semantic runbook Markdown remains Strategy/Human/project-native procedure authority; Executor-owned recipe JSON cannot redefine it.
- **R-T035-P5** — project-native runbook/workflow providers remain reusable through D034/COEXISTENCE; the native footprint is fallback capability, not forced duplication.
- **R-T035-P6** — no secrets/credential values are introduced into templates, tests, handoffs or recipe fields.
- **R-T035-P7** — existing source/consumer separation, single-install/self-bootstrap, collision safety, symlink/junction safety, canonical LF and artifact identity invariants remain unchanged.
- **R-T035-P8** — T021/T022 and T034 represented semantics/history are not modified.

## Controlling Design

### 1. Demand-driven native persistence

Extend the existing bootstrap skeleton rather than create another product/state system:

```text
.agent-coordination/
    ... existing state ...
    runbooks/
        RUNBOOK.template.md
        recipes/
            RUNBOOK-RECIPE.template.json
```

Bootstrap creates only these directories/templates. It must not generate tool-specific recipes or infer project operations.

### 2. Preserve role ownership by artifact type

`RUNBOOK.template.md` is already Orchestrator-owned semantic procedure content. T035 may only wire/copy it.

`RUNBOOK-RECIPE.template.json`, runtime validation, technical helper code and implementation tests are Executor-owned technical realization constrained by the exact staged contract.

### 3. Recipe schema/trust validation

The implementation must validate the exact top-level recipe field set and lifecycle states defined by `docs/RUNBOOK-OPERATION-RESOLUTION.md`.

At minimum:

- JSON object only; no unexpected top-level fields;
- non-empty `recipe_id`, `operation_id`, adapter identity/version, binding and invocation;
- lifecycle state is one of `CANDIDATE`, `VERIFIED`, `STALE`, `REVOKED`, `SUPERSEDED`;
- effect classes are valid D033 values;
- `authoritative_sources` is non-empty and uses only the accepted source classes;
- `VERIFIED` requires non-empty postconditions, `verification.result == "pass"`, verification timestamp/evidence, and non-empty stale triggers covering version drift and failed replay/postcondition;
- material effect classes require non-empty `runbook_id` + `runbook_step` and a safe native runbook file whose `Runbook-ID` matches;
- `SUPERSEDED` requires a non-empty supersession reference;
- credential storage is a class/reference only; no dedicated credential-value/secret field is accepted;
- duplicate recipe IDs and duplicate exact VERIFIED match bindings fail closed;
- symlink/junction traversal through native runbook/recipe paths fails closed.

Validation is structural/trust-record consistency only. It MUST NOT execute recipe content, contact external systems, or declare an invocation authorized.

### 4. No command-wrapper architecture

Do not add a universal command runner, shell wrapper, network proxy or execution daemon.

D054 resolution is an agent/execution-control procedure over a validated durable registry. Existing Execution Adapters remain native mechanisms.

### 5. No new CLI command

T035 reuses existing bootstrap/validate behavior. Do not add `runbook`, `exec`, `command`, `recipe` or another new top-level CLI command in this readiness task.

A later product decision may expose convenience operations if evidence shows they are needed, but D054 does not require one.

### 6. D040 phase separation

T035 is **readiness**, not protocol activation.

It MUST NOT edit:

- `governance-core/GOVERNANCE.md`;
- `governance-core/EXECUTION-CONTROL.md`;
- `governance-core/PROTOCOL.md`;
- `governance-core/CONTEXT.md`;
- routed Core module versions or current `Protocol-Version`;
- Consumer Skill Markdown.

After T035 acceptance, the Orchestrator owns the separate Markdown-only D054 activation.

## D052 conformance oracle

- Oracle-ID: `T035-RUNBOOK-OPERATION-READINESS`
- Oracle-Revision: `T035-D054-v1`
- Oracle-Assets:
  - `tests/test_t035_runbook_operation_resolution_conformance.py`
- Oracle-Semantic-Scope: native runbook/recipe bootstrap layout, exact recipe trust states/field contract, VERIFIED provenance/postcondition requirements, material runbook binding, fail-closed unsafe-path behavior and no routed protocol/CLI-surface expansion.
- Oracle-Freeze-State: `FROZEN` only when this Task Contract and exact oracle are integrated into canonical `develop`; T035 remains `BLOCKED` until T034 acceptance even after the oracle is frozen.
- Executor-Mechanical-Corrections: none to oracle semantics; implementation/harness/test mechanics outside the frozen oracle remain Executor-owned.

The Executor MUST NOT edit `tests/test_t035_runbook_operation_resolution_conformance.py`.

## Authorized scope

- deterministic bootstrap/validation implementation needed for the native runbook/recipe footprint;
- `src/agent_governance/engine.py` and/or a focused new non-Markdown helper module if the Executor judges separation materially cleaner;
- `governance-skill/assets/RUNBOOK-RECIPE.template.json` exactly according to the staged contract;
- existing non-Markdown test helpers/fixtures whose inventory expectations mechanically require the new footprint;
- Executor-owned supplementary deterministic/security/portability tests;
- artifact/package tests only when the new fallback footprint/assets require mechanical inventory alignment;
- `handoffs/T035-executor-handoff.json`.

## Orchestrator-owned / immutable during Executor work

- all committed Markdown;
- `governance-skill/assets/RUNBOOK.template.md`;
- `tests/test_t035_runbook_operation_resolution_conformance.py`;
- D054 semantic field/state/source hierarchy and material-effect runbook requirement.

## Explicit exclusions

- any committed Markdown edit by the Executor;
- any edit/weakening of the T035 frozen conformance oracle;
- D054 routed Core activation or protocol-version bump;
- new top-level CLI commands;
- universal shell/command wrapper, execution daemon or remote broker;
- embedded secrets or production credentials;
- automatic execution of recipe content during validation;
- fuzzy/model-based recipe matching as a trusted execution path;
- community/search/model content as sole recipe provenance;
- migration/prepopulation of arbitrary tool command catalogs;
- T021/T022/T034 semantic/history changes;
- direct writes to `develop`/`main` or force-push of represented history.

## Acceptance criteria

### AC-T035-1 — bootstrap footprint

A clean Consumer bootstrap creates safe native `runbooks/` and `runbooks/recipes/` directories and copies both templates. Normal validation succeeds.

### AC-T035-2 — exact recipe trust contract

The recipe template and validator implement exactly the staged D054 field/state/source contract. `CANDIDATE` is non-trusted; `VERIFIED` requires authoritative provenance, semantic postconditions, passing verification evidence and stale triggers.

### AC-T035-3 — material operation fails closed without runbook

A recipe containing any of the six D054 material effect classes fails validation unless its `runbook_id` and step resolve to a safe native semantic runbook with matching identity.

### AC-T035-4 — malformed/unsafe registry fails closed

Unknown fields/states, duplicate IDs/exact verified bindings, unsafe links/junctions, invalid supersession and designated secret-value storage are rejected through controlled Governance errors rather than ignored.

### AC-T035-5 — no authority/runtime expansion

Validation does not execute recipes or contact targets; no new command runner/daemon/network path exists; CLI v1 top-level command set and routed Protocol `1.14.0` remain unchanged.

### AC-T035-6 — package/source independence

The self-contained artifact carries the new templates/runtime readiness through the existing single-install architecture and remains source-checkout independent.

### AC-T035-7 — canonical native-Windows baseline green

On a safe current native-Windows checkout after T034 integration:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

All required focused/package/security tests are also green.

## Verification and trace requirements

Required Orchestrator conformance:

```text
R-T035-1/2/3 -> tests/test_t035_runbook_operation_resolution_conformance.py
R-T035-4/5   -> tests/test_t035_runbook_operation_resolution_conformance.py
R-T035-6/7   -> frozen oracle + existing package/canonical suites
```

Executor SHALL additionally:

- add focused implementation tests for all parser/validator branches introduced;
- test unsafe symlink/junction paths with platform-equivalent fixtures rather than host-capability skips;
- prove bootstrap rollback/collision behavior remains safe;
- run complete artifact/self-contained package coverage affected by new assets;
- run stable CLI v1 tests;
- run complete canonical Ruff + pytest on native Windows;
- perform D053 Code Review & Verify against this Design/Plan;
- record exact requirement/AC -> test/command evidence in the handoff;
- distinguish required frozen oracle from supplementary Executor tests;
- confirm no committed Markdown or T035 oracle drift on the implementation branch.

## Stop / escalation / SDD re-entry conditions

Return `BLOCKED`/`PARTIAL` rather than expand scope when:

- T034 is not accepted/integrated or canonical baseline is not green;
- a runtime change requires changing D054 semantic recipe fields/states/source hierarchy;
- secure validation requires executing recipes or adding a command broker;
- a new top-level CLI command appears necessary;
- the semantic runbook template appears insufficient/contradictory;
- deterministic validation cannot distinguish a required material runbook binding without inventing new Strategy semantics;
- package/self-bootstrap support would require a new distribution architecture;
- a required security property cannot be proven without weakening existing controls;
- a proposed change requires routed Core/protocol activation during T035.

A frozen-oracle semantic concern is `ORACLE_DEFECT`-equivalent and requires Orchestrator re-entry.

## Expected handoff

Before terminal status, persist `handoffs/T035-executor-handoff.json` under `docs/EXECUTOR-HANDOFFS.md` with:

- exact accepted T034/current-develop base;
- frozen oracle revision `T035-D054-v1`;
- implementation review anchor;
- requirement/AC trace;
- focused/canonical/package/security verification;
- no-Markdown/no-oracle-drift evidence;
- any re-entry blocker.

Commit authorized work and perform one planned final push under D048. Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T035-executor-handoff.json
BRANCH: feat/t035-runbook-operation-resolution-readiness
HEAD: <pushed-commit-sha>
```