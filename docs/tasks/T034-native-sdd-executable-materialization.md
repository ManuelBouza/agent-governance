# T034 — Native SDD Executable Materialization

## Identity

- Task ID: `T034`
- Status: `ACCEPTED`
- Type: `mixed`
- Base branch: `develop`
- Expected topic branch: `feat/t034-native-sdd-executable-materialization`
- Expected executor handoff: `handoffs/T034-executor-handoff.json`
- SDD-Profile: `ASSURED`
- Test-Authorship-Mode: `mixed`
- Assurance-Class: `protocol, package, behavioral`
- Verification-Planes: `static, deterministic, behavioral, package, portability`
- Release-Impact: `protocol-compatible materialization of accepted 1.14.0 semantics`
- Context-Impact: `focused Core/package/test paths only`

`READY` is effective only when this Task Contract and its required Orchestrator-owned conformance asset are integrated into canonical `develop`. The Executor MUST NOT launch from this planning branch.

## Objective

Make the already-accepted D053/A1 native SDD semantics operational in the deterministic Consumer Governance runtime/package and verification surfaces with the smallest coherent executable delta.

The implementation must make `governance-core/SDD.md` a real installed/validated Core module, align executable protocol/package expectations with `Protocol-Version: 1.14.0`, and replace the obsolete evaluation meaning that treated absence of an external SDD provider as a no-SDD mode.

No new SDD runtime/lifecycle, task parser, handoff schema, external SDD dependency, or parallel source of truth is authorized.

## Current specification carriers / controlling references

- `AGENTS.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/SDD-ADOPTION-PLAN.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/SDD.md`
- `governance-core/COEXISTENCE.md`
- `governance-core/LIFECYCLE.md`
- `governance-core/EXECUTION.md`
- `governance-core/HANDOFF.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/CONFORMANCE-ORACLE-CONTRACT.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`

## A2 executable-gap decision

A2 inspected the integrated A1 semantic state against the current deterministic runtime, package builder, consumer task template, schemas and existing test/eval surfaces.

The minimum coherent executable delta is:

1. **Core runtime inventory** — `src/agent_governance/engine.py` currently has a closed `CORE_FILES`/`CORE_VERSION_FIELDS` inventory that does not contain `SDD.md`, while integrated `GOVERNANCE.md` routes `.agent-governance/SDD.md`. `_validate_core()` requires routed Core references to equal the closed inventory. Therefore current bootstrap/validation cannot materialize the accepted A1 Core coherently.
2. **Deterministic Core/package expectations** — repository test helpers still enumerate the pre-A1 Core set, and artifact tests contain pre-A1 protocol-version expectations. The artifact builder itself already copies all `governance-core/*.md`, so no new artifact-copy mechanism is required.
3. **Native-fallback conformance** — the existing Consumer Governance trigger corpus/grader still encodes `no_sdd -> refuse_unsolicited_sdd`, which contradicts D053. Accepted semantics are `no adequate project-native/external SDD provider -> use Agent Governance native SDD, and do not install/propose an external SDD framework merely to obtain SDD`.

A2 explicitly found **no present need** for:

- a new parser/schema for the expanded Markdown `TASK.template.md`; the deterministic engine treats task-detail content as Governance/agent-readable Markdown and only requires the existing task identity metadata for its current state/event mechanics;
- a new handoff JSON schema/validator; no such consumer/runtime schema exists today, and A1 handoff review/trace semantics are protocol/Task-Contract obligations rather than a newly materialized machine schema;
- a second SDD state tree, queue, command family, or external SDD runtime;
- changes to T021/T022 represented history.

Discovery during implementation that one of these excluded mechanisms is actually required to satisfy an acceptance criterion is an SDD re-entry condition, not authorization to add it.

## Requirement / specification delta

### ADDED

- **R-T034-1 — installed native SDD Core**: Consumer Governance bootstrap SHALL copy `SDD.md` into `.agent-governance/`, validate its `SDD-Version` declaration, and require it wherever the closed Core inventory is used.
- **R-T034-2 — native fallback executable meaning**: Conformance SHALL represent absence of an adequate external/project-native SDD provider as use of Agent Governance native SDD while refusing unsolicited installation/proposal of an external SDD framework merely for methodology coverage.

### MODIFIED

- **R-T034-3 — protocol/package expectations**: Deterministic test/package expectations SHALL align with the integrated `Protocol-Version: 1.14.0` and the expanded Core inventory containing `SDD.md`.
- **R-T034-4 — legacy no-SDD eval projection**: The T015 Consumer Governance corpus/grader SHALL no longer encode `refuse_unsolicited_sdd` as the complete `no_sdd` outcome. It SHALL mechanically reflect R-T034-2 using the frozen semantic names defined below.

### REMOVED

- **R-T034-5 — no-SDD fallback acceptance**: The executable/eval acceptance meaning that Governance continues with no SDD discipline when no external provider exists is removed.

### PRESERVED

- **R-T034-P1** — no external SDD product becomes a required dependency.
- **R-T034-P2** — adequate project-native SDD remains `REUSE`/`ADAPT`/`COEXIST` under the existing coexistence rules; T034 changes only the missing-provider fallback.
- **R-T034-P3** — source/consumer separation, single-install/self-contained artifact behavior, bootstrap collision safety, source independence and fail-closed validation remain unchanged.
- **R-T034-P4** — the stable Consumer Governance CLI command surface remains exactly `bootstrap, validate, state, event, skill, ecosystem, archive`.
- **R-T034-P5** — D053 single-owner stages remain semantic protocol authority; T034 does not create executable stage ownership or a parallel lifecycle.
- **R-T034-P6** — existing consumer task records remain Markdown contracts; no migration/backfill is required solely because the task template now carries SDD fields.
- **R-T034-P7** — historical T021/T022/T015 Task Contracts and represented Git history are not rewritten.

## Controlling Design

### 1. Extend the existing closed Core inventory

Use the existing deterministic Core model rather than inventing discovery logic.

`SDD.md` joins the same explicit `CORE_FILES` inventory as the other required Core Markdown modules and joins `CORE_VERSION_FIELDS` with `SDD-Version`.

This preserves the current fail-closed property:

```text
GOVERNANCE routed Core references == deterministic required Core inventory
```

A missing, stripped, unversioned or unrouted `SDD.md` must fail through the same validation boundary as other required Core modules.

### 2. Preserve the existing package architecture

`src/agent_governance/artifact.py` already copies all canonical `governance-core/*.md` into the self-contained artifact. Do not add a second SDD packaging path or special-case copy mechanism.

Update only executable expectations/tests that still assume the pre-A1 Core/version state unless implementation evidence proves a real builder defect.

### 3. Keep task-detail SDD semantics Markdown-native

The expanded consumer `TASK.template.md` is an agent-facing contract carrier under D053. T034 does not add a deterministic parser for `SDD-Profile`, requirement delta, Design, trace, or re-entry sections.

The current deterministic engine may continue to consume only the task identity/status information required by state/event mechanics. Governance/agent protocol interprets the rest.

### 4. Keep handoff trace semantics protocol-native

Do not create a universal handoff schema solely because A1 added Code Review & Verify/trace expectations. Source Executor handoffs remain governed by `docs/EXECUTOR-HANDOFFS.md`; consumer handoff semantics remain governed by Core Markdown and project records.

A future schema is a separate design decision if evidence shows deterministic machine validation is required.

### 5. Native-fallback vocabulary is frozen

For the existing Consumer Governance coexistence corpus, the `no_sdd` shape means **no adequate external/project-native SDD provider is present**, not absence of SDD discipline.

The exact required semantic behavior identifiers are:

```text
use_native_sdd
refuse_unsolicited_external_sdd
```

The exact required explicit surface tags are:

```text
native_sdd_fallback
no_unsolicited_external_sdd
```

The `cg-pos-validation-001` case must clearly state that Agent Governance native SDD applies and an external SDD framework is not proposed/installed merely to obtain SDD coverage.

The grader must fail closed if either required `no_sdd` behavior is absent or replaced by the legacy `refuse_unsolicited_sdd` meaning.

### 6. No semantic choice is delegated in the oracle synchronization

The Executor may update the existing T015 corpus/grader/self-tests only to make them exactly satisfy the frozen T034 conformance asset and vocabulary above. This is a bounded implementation/materialization operation, not authority to choose alternate expected behaviors, tags, case classification, membership, thresholds, or stage semantics.

Any proposed alternate semantic vocabulary/meaning is `ORACLE_DEFECT`/SDD re-entry territory and must stop before mutation.

## D052 conformance oracle

- Oracle-ID: `T034-NATIVE-SDD-MATERIALIZATION`
- Oracle-Revision: `T034-A2-v1`
- Oracle-Assets:
  - `tests/test_t034_native_sdd_conformance.py`
- Oracle-Semantic-Scope: installed `SDD.md` Core parity, Protocol 1.14.0/package identity, deterministic Core test inventory, and exact native-SDD missing-provider fallback semantics.
- Oracle-Freeze-State: `FROZEN` only when this Task Contract and the exact oracle asset are reachable from canonical `develop`; otherwise treat them as `DRAFT` and do not launch.
- Executor-Mechanical-Corrections: implementation/harness wiring and exact synchronization of legacy T015 corpus/grader/self-tests to the frozen identifiers/expectations above; no edit to the frozen oracle asset and no alternate semantic outcome.

The Executor MUST NOT edit `tests/test_t034_native_sdd_conformance.py`.

## Authorized scope

- `src/agent_governance/engine.py` — required Core inventory/version materialization only.
- `tests/_helpers.py` — canonical required-Core test inventory alignment.
- `tests/test_governance_artifact.py` — pre-A1 protocol/Core package expectation alignment.
- `evals/consumer_governance/corpus.json` — exact bounded synchronization of the existing `no_sdd` case to the frozen native-fallback semantics.
- `evals/consumer_governance/grader.py` — exact bounded synchronization of allowed behavior/tag vocabulary and fail-closed `no_sdd` validation to the frozen semantics.
- `tests/test_consumer_governance_trigger_corpus.py` — exact bounded self-test synchronization for the changed frozen corpus/grader semantics.
- Other non-Markdown deterministic tests only when a failure is mechanically caused by the same Protocol 1.14.0/Core-inventory expansion and the change does not create new acceptance semantics.
- Executor-owned supplementary implementation/regression tests that do not redefine the frozen oracle.
- `handoffs/T034-executor-handoff.json`.

## Orchestrator-owned / immutable during Executor work

- `tests/test_t034_native_sdd_conformance.py` — frozen semantic conformance asset.
- All committed Markdown, including this Task Contract and D053/A1 specification carriers.
- Expected behavior names, tags, case classification/membership and fail-closed meaning defined by the frozen oracle.

## Explicit exclusions

- Any committed Markdown edit by the Executor.
- Any edit to the frozen T034 conformance asset.
- New SDD commands, state files, directories, queues or independent lifecycle machinery.
- A new parser/schema for SDD task sections unless Orchestrator re-entry explicitly revises this Design.
- A new handoff JSON schema/validator unless Orchestrator re-entry explicitly revises this Design.
- Installing or depending on OpenSpec, Spec Kit, Kiro or another external SDD framework.
- Reclassifying project-native SDD coexistence semantics outside the missing-provider fallback.
- Changing D053 stage ownership or giving Executor-private SDD/plans specification/Design/Plan/acceptance authority.
- Changing CLI v1 command names/surface.
- Changing artifact identity schema semantics, source-independence guarantees, bootstrap overwrite/collision behavior, security/fail-closed checks, or release policy.
- T021/T022 implementation/history or automatic resumption of that queue.
- Direct writes to `develop`/`main` or force-push of represented history.

## Acceptance criteria

### AC-T034-1 — installed Core parity

A source-layout Consumer Governance bootstrap succeeds from the integrated Protocol 1.14.0 Core, copies `SDD.md` into `.agent-governance/`, validates the installation successfully, and treats `SDD.md`/`SDD-Version` as required Core structure.

Deleting, stripping or removing the required routed `SDD.md` must remain fail-closed through the existing Core validation model.

### AC-T034-2 — self-contained artifact parity

A self-contained Governance Skill artifact built from the submitted source includes `core/SDD.md`, records protocol version `1.14.0`, and continues to bootstrap/validate/run without source-checkout or sibling dependencies under the existing package/identity contract.

### AC-T034-3 — native SDD missing-provider fallback

The authoritative Consumer Governance corpus/grader represents `no_sdd` as:

```text
use_native_sdd
+
refuse_unsolicited_external_sdd
```

and explicitly carries `native_sdd_fallback` plus `no_unsolicited_external_sdd` tags. The grader rejects mutation that removes either required behavior.

The legacy complete outcome `refuse_unsolicited_sdd` is no longer accepted for this shape.

### AC-T034-4 — no unnecessary runtime/schema expansion

The task is satisfied without a second SDD runtime/lifecycle, new external dependency, new task-section parser/schema, or new handoff schema. If implementation evidence shows one is genuinely required for AC-T034-1 through AC-T034-3, return `BLOCKED` for Orchestrator Design re-entry rather than adding it.

### AC-T034-5 — preserved CLI/consumer behavior

The existing stable CLI v1 surface and all unrelated Consumer v1/bootstrap/state/event/skill/ecosystem/archive behavior remain green. Existing project-native SDD reuse/adapt/conflict semantics remain unchanged outside the missing-provider fallback.

### AC-T034-6 — canonical native-Windows baseline green

On a safe fresh/rematerialized native-Windows checkout of the submitted branch, all canonical verification succeeds:

```text
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

No use of the known stale pre-T033 CRLF operational checkout is valid evidence.

## Verification and trace requirements

Required Orchestrator conformance:

```text
R-T034-1 / AC-T034-1 -> tests/test_t034_native_sdd_conformance.py
R-T034-2 / AC-T034-3 -> tests/test_t034_native_sdd_conformance.py
R-T034-3 / AC-T034-2 -> tests/test_t034_native_sdd_conformance.py + existing artifact tests
R-T034-4 / AC-T034-3 -> tests/test_t034_native_sdd_conformance.py + existing trigger-corpus self-tests
```

The Executor SHALL also:

- run focused bootstrap/validate tests, including missing/tampered Core negative controls;
- run the complete existing Governance artifact suite;
- run the complete Consumer Governance trigger corpus/grader suite;
- run the stable CLI v1 tests proving command-surface/non-regression behavior;
- add supplementary implementation tests when needed for technical coverage without changing the frozen semantic oracle;
- run the complete canonical Ruff + pytest suite on native Windows;
- record requirement/AC -> exact test/command evidence in the T034 handoff;
- identify the exact integrated `develop` base containing `T034-A2-v1` and confirm the frozen oracle file was not changed on the implementation branch.

## Code Review & Verify obligations

Before `DONE`, the Executor must review the submitted implementation against this specification/Design/Plan for:

- exact closed-Core integration of `SDD.md` without special-case drift;
- absence of duplicate/special package machinery;
- exact frozen native-fallback semantics and removal of only the obsolete T015 meaning;
- no new task/handoff schema or SDD lifecycle machinery;
- unchanged CLI v1 surface and unrelated coexistence semantics;
- maintainability and unnecessary complexity;
- all required deterministic/package/behavioral evidence;
- unauthorized scope additions.

In-authority implementation defects may be corrected. Any need to alter frozen semantics, stage ownership, excluded schemas/runtime, or acceptance meaning requires upstream re-entry.

## Stop / escalation / SDD re-entry conditions

Return `BLOCKED` or `PARTIAL` rather than guessing when:

- the frozen T034 oracle appears inconsistent with D053/A1;
- satisfying bootstrap/package parity requires a new protocol architecture rather than extending the existing Core inventory;
- task-section machine parsing is actually required for correctness rather than merely desirable;
- a handoff schema is actually required for correctness rather than merely desirable;
- the existing artifact builder cannot include SDD through its current generic Core-copy path;
- native fallback cannot be represented without changing broader coexistence authority/classification semantics;
- a required test implies changing the stable CLI v1 surface;
- a failure requires weakening existing fail-closed/security/source-independence assertions;
- canonical verification remains red for an unrelated defect outside this task;
- a proposed change touches T021/T022 represented work.

A semantic oracle concern is `ORACLE_DEFECT`-equivalent: identify the exact assertion/case and controlling authority; do not edit the frozen oracle.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist `handoffs/T034-executor-handoff.json` under `docs/EXECUTOR-HANDOFFS.md` with D053 Code Review & Verify evidence, requirement trace, exact frozen oracle identity, implementation review anchor, verification results and any re-entry blocker.

Commit all authorized work and perform the one planned final push under D048. Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T034-executor-handoff.json
BRANCH: feat/t034-native-sdd-executable-materialization
HEAD: <pushed-commit-sha>
```

## Launch gate

The first Executor launch governed by A1/T034 occurs after `AGENTS.md` changed in A1. Therefore the canonical launch MUST include the D043 conditional reload line after synchronizing a safe current `develop` baseline and before loading this Task Contract.

The launch must use a safe fresh/rematerialized native-Windows checkout. The stale pre-T033 CRLF operational checkout is prohibited as T034 execution evidence.
