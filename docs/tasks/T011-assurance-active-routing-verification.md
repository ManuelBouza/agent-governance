# T011 — Assurance active-routing deterministic verification

Task ID: T011  
Status: READY  
Type: test/eval  
Base branch: `develop`  
Expected topic branch: `test/assurance-active-routing-verification`  
Expected executor handoff path: `handoffs/T011-executor-handoff.json`

## Objective

Update executor-owned deterministic verification so the already-accepted D036 assurance semantics can be verified in both their staged Protocol `1.12.0` state and their active/routed Protocol `1.13.0` state, without reintroducing an independently authored mutable current-protocol-version literal.

This task exists because OP012 correctly blocked the D040 Phase-B candidate: the focused assurance test still asserts `Activation-State: STAGED`, and the shared required-Core module inventory does not yet model `ASSURANCE.md` as required when active.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/reviews/T010-R1.md`
- `docs/operations/OP012-verify-d040-phase-b-activation-candidate.md`
- `docs/learning/L001-protocol-version-baseline-drift.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/ASSURANCE.md`
- `tests/_helpers.py`
- `tests/test_assurance_audit_contract.py`

## Authorized scope

The executor may modify only non-Markdown deterministic test/helper/fixture code required to support the D040 Phase-B activation state, plus the required non-Markdown executor handoff.

Expected areas are limited to:

- `tests/_helpers.py`;
- `tests/test_assurance_audit_contract.py`;
- other existing deterministic test files only if required to keep their current invariants coherent with active `ASSURANCE.md` routing;
- `handoffs/T011-executor-handoff.json`.

## Explicit exclusions

The executor MUST NOT:

- create or edit committed Markdown;
- edit `governance-core/GOVERNANCE.md` or `governance-core/ASSURANCE.md`;
- modify PR #81 or its branch;
- change D036 assurance semantics, finding states, profiles, authority boundaries or activation intent;
- weaken tests merely to accept the candidate;
- reintroduce a mutable exact-current protocol-version constant outside Core;
- add provider/model/network/scanner/live-system behavior;
- add dependencies, lockfile changes or runtime production code unless a genuine blocker requires escalation first;
- initialize or commit CodeGraph/SDD project state.

## Invariants / constraints

`governance-core/GOVERNANCE.md` remains the sole current protocol-version authority.

Verification must model state consequences rather than duplicate the current version as a second authority.

At minimum, the deterministic contract must distinguish:

```text
ASSURANCE STAGED
  -> Protocol 1.12.0
  -> not routed / not required Core

ASSURANCE ACTIVE
  -> Protocol 1.13.0 or later compatible active state
  -> routed / required Core
```

The implementation may choose a stronger state-derived design, but must not hard-code a free-standing mutable `SOURCE_PROTOCOL_VERSION = "1.13.0"` equivalent.

The existing D036 A–I assurance semantics and all unrelated deterministic guarantees must remain intact.

## Acceptance criteria

ChatGPT will accept only if remote evidence shows:

1. no Markdown changes;
2. no independent mutable exact-current protocol-version authority was introduced;
3. the assurance contract test no longer assumes that `ASSURANCE.md` must always be staged;
4. active `ASSURANCE.md` routing/required-Core membership is deterministically validated;
5. staged behavior remains representable/validated where relevant rather than being erased as historical readiness state;
6. the Protocol `1.13.0` activation candidate can pass the focused and full deterministic suites without modifying the candidate;
7. existing assurance, security and execution-control semantics are not weakened.

## Verification requirements

Run at minimum:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The executor should additionally verify the D040 Phase-B activation state using a safe local/disposable composition of its implementation with the exact current PR #81 candidate, without pushing or modifying PR #81. This is verification evidence only; the executor implementation branch remains based on current `develop` containing this Task Contract.

If validating the candidate requires any Markdown mutation, stop and report `BLOCKED`.

## Stop / escalation conditions

Stop and report `BLOCKED` or `PARTIAL` if:

- the required behavior cannot be achieved without changing Markdown semantics;
- a second current-version authority appears necessary;
- candidate PASS would require weakening an unrelated invariant;
- dependencies/runtime/provider/network/live-system behavior becomes necessary;
- the exact PR #81 candidate cannot be safely inspected/combined for verification.

## Expected handoff

Persist the result at:

`handoffs/T011-executor-handoff.json`

The handoff must identify base/head, changed paths, verification results, candidate-composition verification result, confirmation of no Markdown changes, and confirmation that no mutable current-version authority was reintroduced.
