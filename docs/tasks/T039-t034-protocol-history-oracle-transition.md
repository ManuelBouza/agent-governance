# T039 — T034 Protocol-History Oracle Transition

## Identity

- Task ID: `T039`
- Status: `PLANNED`
- Type: `orchestrator-conformance`
- Base branch: `develop`
- Planning/oracle branch: `feat/t039-t034-oracle-transition`
- Expected executor verification branch: `verify/t039-t034-oracle-transition`
- Expected executor handoff: `handoffs/T039-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `orchestrator-conformance`
- Assurance-Class: `protocol-migration, conformance-oracle, package`
- Verification-Planes: `deterministic, static, portability`
- Release-Impact: `removes a stale historical T034 protocol pin so T038 can restore the canonical T020 artifact baseline`

## Objective

Correct the lifecycle scope of the frozen T034 conformance oracle so it continues to prove that T034 was accepted against Protocol `1.14.0` while allowing later independently authorized protocol migrations to advance the repository's current Core version.

T039 changes no runtime, Consumer CLI behavior, Core semantics, templates, artifact builder behavior, T021 implementation, or T038 implementation. It is a narrow D052 oracle transition required because T038 correctly exposed a stale live-current-version assertion in the T034 oracle.

## Trigger / defect statement

T034 was accepted as the executable materialization of D053 native SDD against the then-current Core `Protocol-Version: 1.14.0`. Its frozen oracle therefore asserted that a freshly built artifact reported exactly `1.14.0`.

D054 Phase-B later advanced canonical Core to `1.15.0` under separate accepted authority. T038 now removes duplicated mutable current-version literals from Consumer package templates and derives installed protocol identity from packaged Core. T038 focused verification is green, but the full suite fails only because `tests/test_t034_native_sdd_conformance.py` still compares a newly built artifact from the current Core to historical literal `1.14.0`.

The T034 Task Contract is the durable historical authority for what T034 accepted. The current `governance-core/GOVERNANCE.md` is the sole authority for the repository's current protocol version. The oracle must not conflate those two time scopes.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/tasks/T034-native-sdd-executable-materialization.md`
- `tests/test_t034_native_sdd_conformance.py`
- `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md`
- `handoffs/T038-executor-handoff.json`
- `docs/orchestrator/CHECKPOINT.md`

## Dependency / sequencing

```text
T038 implementation BLOCKED only by stale T034 oracle
        -> T039 Orchestrator oracle transition authored/integrated
        -> T039 independent Executor Code Review & Verify
        -> T039 Converge/Accept
        -> T038 re-verification from current canonical develop
        -> T038 Converge/Accept
        -> T021-R1 may resume only after T038 acceptance
```

T021 remains blocked; T022 and downstream unified-refactor work remain ineligible.

## Requirement / specification delta

### MODIFIED

- **R-T039-1 — historical T034 protocol binding**: the T034 oracle SHALL prove from the accepted T034 Task Contract that T034's package/materialization acceptance was against Protocol `1.14.0`, instead of requiring every future artifact built from current Core to remain `1.14.0`.
- **R-T039-2 — current artifact/Core parity**: the same oracle SHALL continue to build a current artifact and verify that its recorded protocol identity equals the protocol version derived from current canonical `governance-core/GOVERNANCE.md`.

### PRESERVED

- **R-T039-P1** — T034 installed `SDD.md` Core parity remains unchanged.
- **R-T039-P2** — T034 native-SDD fallback behavior vocabulary, corpus/grader semantics and negative controls remain unchanged.
- **R-T039-P3** — artifact inclusion of `core/SDD.md` and byte parity with canonical Core remain unchanged.
- **R-T039-P4** — no T038 implementation/runtime/template/test change is made by T039.
- **R-T039-P5** — no current protocol-version literal is introduced as a second authority outside canonical Core; historical `1.14.0` remains only where proving T034's accepted history.
- **R-T039-P6** — no T021/T022 implementation or queue resumption.

## Controlling Design

### 1. Separate historical acceptance from current identity

In the single T034 oracle function that currently pins a newly built artifact to `1.14.0`:

1. read the accepted T034 Task Contract as the historical carrier;
2. deterministically prove that T034's accepted protocol/package requirement was `1.14.0`;
3. build the artifact from the current repository;
4. derive the current protocol from `governance-core/GOVERNANCE.md` using the existing artifact builder parser;
5. assert the artifact identity equals that derived current Core value.

This preserves T034 history without turning a historical release condition into a future version lock.

### 2. Preserve SDD package semantics

Keep all existing assertions that:

- `SDD.md` belongs to the required Core inventory;
- built artifacts contain `core/SDD.md`;
- artifact `core/SDD.md` is byte-identical to canonical Core;
- missing external/project-native SDD uses the accepted native-SDD fallback semantics.

### 3. Narrow oracle revision only

- Oracle asset remains `tests/test_t034_native_sdd_conformance.py`.
- Oracle revision: `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1`.
- Only the temporal/current-version meaning of the T034 package identity assertion may change.
- No other T034 assertion, fixture, corpus, grader behavior, threshold, command surface or runtime behavior may change.

## Authorized scope

Orchestrator-owned preimplementation gate:

- `docs/tasks/T039-t034-protocol-history-oracle-transition.md`;
- only the single T034 oracle function containing the stale live `1.14.0` artifact assertion in `tests/test_t034_native_sdd_conformance.py`;
- `docs/orchestrator/CHECKPOINT.md` and later T039 acceptance review as required.

Executor verification after integration:

- read-only review of T039 against this Task Contract and T034/T038 authority;
- focused execution of `tests/test_t034_native_sdd_conformance.py`;
- complete canonical native-Windows pytest suite;
- repository-wide Ruff check/format and `git diff --check`;
- persisted `handoffs/T039-executor-handoff.json` only.

## Explicit exclusions

- any runtime, template, artifact-builder, Core or Consumer CLI change;
- any T038 implementation change;
- any other T034 oracle assertion or eval/corpus change;
- weakening native-SDD fallback semantics;
- introducing a current `1.15.0` literal into the oracle;
- T021/T022 implementation or automatic resumption;
- direct writes to `develop`/`main`.

## Acceptance criteria

### AC-T039-1 — T034 historical protocol acceptance remains proven

The oracle deterministically proves from `docs/tasks/T034-native-sdd-executable-materialization.md` that T034's accepted package/materialization protocol was `1.14.0`.

### AC-T039-2 — no future current-version pin

The oracle no longer requires an artifact built from the repository's future current Core to report `1.14.0`.

### AC-T039-3 — current Core/artifact identity parity remains proven

The oracle builds a current artifact, derives the current protocol from canonical Core, and asserts artifact identity equals that value without a duplicated current-version literal.

### AC-T039-4 — all other T034 semantics unchanged

Diff review proves installed SDD parity, Core inventory assertions, native-SDD fallback semantics and all other T034 oracle behavior are unchanged.

### AC-T039-5 — canonical baseline green before T038 integration

Focused T034 oracle and complete canonical native-Windows verification pass on current `develop` containing only the T039 oracle transition, without requiring T038 implementation changes.

### AC-T039-6 — T038 becomes structurally re-verifiable

After T039 acceptance, T038 may reconcile/reverify its already implemented protocol-derived asset repair against fresh canonical `develop` without the historical T034 oracle creating an artificial failure.

## Verification / trace

```text
R-T039-1 -> T034 oracle reads accepted T034 Task Contract historical protocol requirement
R-T039-2 -> diff review confirms removal of live exact-current 1.14.0 artifact assertion
R-T039-2/R-T039-3 -> current artifact identity == builder-derived current Core protocol
R-T039-P1..P4 -> focused T034 oracle + diff review
AC-T039-5 -> full canonical pytest + Ruff + diff check on native Windows
```

Required Executor evidence:

- exact canonical `develop` base containing T039 planning/oracle revision;
- focused T034 oracle result;
- full locked pytest result;
- Ruff check/format result;
- `git diff --check` result;
- technical review confirming no runtime/template/Core/T038/T021 change and no semantic drift outside the single temporal assertion;
- no unresolved findings/upstream re-entry.

## Stop / re-entry conditions

Return `BLOCKED` rather than expanding scope if:

- another T034 assertion independently pins current protocol identity to `1.14.0`;
- preserving T034 historical acceptance requires changing native-SDD behavior or other frozen oracle semantics;
- the corrected oracle requires runtime/template/Core changes;
- canonical verification remains red for an unrelated reason;
- T038 implementation would need semantic redesign after this transition.

## Expected Executor handoff

After the planning/oracle gate is integrated, the Executor returns only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T039-executor-handoff.json
BRANCH: verify/t039-t034-oracle-transition
HEAD: <pushed-commit-sha>
```
