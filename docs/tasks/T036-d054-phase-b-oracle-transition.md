# T036 — D054 Phase-B Oracle Transition

## Identity

- Task ID: `T036`
- Status: `PLANNED`
- Type: `orchestrator-conformance`
- Base branch: `develop`
- Planning/oracle branch: `feat/t036-d054-phase-b-oracle-transition`
- Expected executor verification branch: `verify/t036-d054-phase-b-oracle-transition`
- Expected executor handoff: `handoffs/T036-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `orchestrator-conformance`
- Assurance-Class: `protocol-migration, conformance-oracle, execution-control`
- Verification-Planes: `deterministic, static, portability`
- Release-Impact: `unblocks D040 Phase-B D054 routed-Core activation without weakening T035 historical acceptance`

## Objective

Correct the lifecycle scope of the frozen T035 conformance oracle so it continues to prove the historical T035 non-expansion requirement without pinning the repository's future current protocol version to `1.14.0`.

T036 is a prerequisite gate for D040 Phase-B D054 Core activation. It does not activate D054, change the Consumer CLI, modify runtime behavior, or authorize any other queued work.

## Trigger / defect statement

The accepted T035 contract explicitly states that `Protocol-Version` remains `1.14.0` **throughout T035 implementation** and that D054 routed Core activation occurs later as a separate D040 Phase-B work unit.

The frozen T035 oracle currently projects that historical requirement as a live assertion against the repository's **current** `governance-core/GOVERNANCE.md`. That assertion is correct at T035 acceptance but becomes semantically stale when the separately authorized Phase-B protocol activation legitimately advances the current protocol version.

D040 forbids knowingly red canonical migration states. D052 states that when an Orchestrator-owned oracle conflicts with its controlling normative specification, the specification controls and the oracle must be corrected through persisted Orchestrator authority.

## Current specification carriers / controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md`
- `docs/tasks/T035-runbook-operation-resolution-readiness.md`
- `docs/reviews/T035-R1.md`
- `tests/test_t035_runbook_operation_resolution_conformance.py`
- `docs/orchestrator/CHECKPOINT.md`

## Dependency / sequencing

```text
T035 ACCEPTED + canonical develop green
        -> T036 Orchestrator oracle transition authored/reviewed/integrated
        -> T036 independent Executor Code Review & Verify / evidence
        -> T036 Converge/Accept
        -> D040 Phase-B D054 Markdown activation may restart from fresh develop
```

T021/T022 remain paused and MUST NOT auto-resume.

## Requirement / specification delta

### MODIFIED

- **R-T036-1 — historical scope correction**: the T035 preserved-surface oracle SHALL prove that T035's accepted contract preserved routed Protocol `1.14.0` during T035, rather than requiring the repository's future current protocol to remain `1.14.0` indefinitely.
- **R-T036-2 — current CLI non-regression**: the same oracle SHALL continue to assert the stable Consumer CLI v1 top-level command set exactly `bootstrap, validate, state, event, skill, ecosystem, archive`.

### PRESERVED

- **R-T036-P1** — every T035 recipe/runbook bootstrap, validation, trust-state, provenance, material-runbook binding, unsafe-path, duplicate/supersession and secret-value assertion remains unchanged.
- **R-T036-P2** — T035 accepted history and frozen revision identity remain intact as historical acceptance evidence; T036 is an explicit later semantic-scope correction, not a rewrite of T035's accepted result.
- **R-T036-P3** — no routed Core Markdown, current Protocol-Version, Consumer Skill Markdown, runtime implementation, template, CLI surface or package behavior changes in T036.
- **R-T036-P4** — no T035 assertion is removed merely because an implementation fails it; the sole corrected assertion is the stale temporal binding identified above.
- **R-T036-P5** — D040 green-baseline migration remains mandatory.

### ADDED / REMOVED

- No product capability is added or removed.

## Controlling Design

### 1. Bind the non-expansion assertion to T035 authority

Replace the live current-version assertion:

```text
current governance Protocol-Version == 1.14.0
```

with a deterministic assertion against the accepted T035 Task Contract's preserved requirement that records:

```text
R-T035-P1 -> Protocol-Version remains 1.14.0 throughout T035 implementation
```

This preserves the original acceptance meaning while allowing a later independently authorized protocol migration.

### 2. Preserve current CLI verification

Continue deriving the runtime parser and assert the exact CLI v1 command set. D054 Phase-B does not authorize a new top-level command.

### 3. No future-version oracle in T036

T036 SHALL NOT pre-author an assertion that current protocol must be `1.15.0`, because integrating such an oracle before Phase-B activation would intentionally make current `develop` red and violate D040.

Current protocol identity remains owned by `governance-core/GOVERNANCE.md`; T036 only removes the stale future pin from the historical T035 oracle.

### 4. Narrow oracle revision

The Orchestrator-owned asset remains `tests/test_t035_runbook_operation_resolution_conformance.py`, but the semantic transition is explicitly authorized by this Task Contract as Oracle revision `T036-D054-ACTIVATION-TRANSITION-v1` for the preserved-surface assertion only.

All other T035 oracle semantics remain frozen and unchanged.

## Authorized scope

Orchestrator-owned preimplementation conformance gate:

- `docs/tasks/T036-d054-phase-b-oracle-transition.md`;
- the single preserved-surface test function in `tests/test_t035_runbook_operation_resolution_conformance.py` required to bind T035's `1.14.0` preservation historically rather than to current protocol state;
- a T036 review/acceptance Markdown record as required.

Executor verification scope after integration:

- read-only review of the T036 semantic transition against this contract and controlling references;
- execution of focused T035/T036-related tests and the canonical required suite on the supported native-Windows baseline;
- `git diff --check`, Ruff check/format and required pytest evidence;
- persisted `handoffs/T036-executor-handoff.json` only; no implementation changes unless a purely mechanical verification blocker is separately authorized.

## Explicit exclusions

- D054 Core activation or protocol bump in T036;
- editing any other T035 oracle assertion;
- weakening recipe/runbook/security negative controls;
- runtime/source implementation changes;
- new Consumer CLI commands;
- changes to templates/assets;
- T021/T022 resumption;
- direct writes to `develop`/`main`;
- using a current protocol-version literal outside `governance-core/GOVERNANCE.md` as a second version authority.

## Acceptance criteria

### AC-T036-1 — historical T035 preservation remains proven

The oracle deterministically verifies that the accepted T035 contract contains the preserved requirement that routed Protocol `1.14.0` remained unchanged throughout T035 implementation.

### AC-T036-2 — no future protocol pin

The T035 oracle no longer requires the repository's current `governance-core/GOVERNANCE.md` to remain `1.14.0` after T035 acceptance.

### AC-T036-3 — all other T035 semantics unchanged

Diff review proves no other T035 conformance assertion/fixture/constant/negative-control meaning changed.

### AC-T036-4 — current CLI surface still protected

The oracle continues to assert exactly the existing CLI v1 top-level command set.

### AC-T036-5 — canonical baseline green

Focused T035 oracle plus complete required canonical native-Windows verification are green after the T036 oracle transition while current protocol remains `1.14.0`.

### AC-T036-6 — D040 Phase-B becomes structurally eligible

After T036 acceptance, a future Markdown-only Phase-B activation may change the current protocol version without this historical T035 oracle creating an artificial red baseline. This criterion does not itself authorize or perform that activation.

## Verification / trace

```text
R-T036-1 -> preserved-surface test reads T035 Task Contract R-T035-P1
R-T036-2 -> preserved-surface test retains parser/CLI exact-set assertion
R-T036-P1/P4 -> diff review against frozen T035 oracle
AC-T036-5 -> focused + full canonical verification evidence in T036 handoff
```

Required Executor evidence:

- exact accepted `develop` base containing T036 planning/oracle transition;
- focused execution of `tests/test_t035_runbook_operation_resolution_conformance.py`;
- complete required native-Windows canonical pytest suite;
- Ruff check/format and `git diff --check`;
- technical Code Review & Verify statement that no hidden runtime/version-authority workaround was introduced;
- no Markdown/oracle drift beyond the integrated T036 authority.

## Stop / re-entry conditions

Return to Orchestrator rather than expand scope if:

- preserving the original T035 meaning requires modifying any other frozen assertion;
- current CLI/runtime implementation must change to make the corrected oracle green;
- another live test independently duplicates/pins current Protocol `1.14.0` and would make Phase-B red;
- canonical verification is red for reasons attributable to this transition;
- a protocol-version migration cannot remain green without further executable changes.

Any such finding blocks D040 Phase-B until a new persisted revision/Task Contract resolves it.

## Expected Executor handoff

After this planning/oracle gate is integrated, the Executor returns only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T036-executor-handoff.json
BRANCH: verify/t036-d054-phase-b-oracle-transition
HEAD: <pushed-commit-sha>
```
