# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O060  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T006, T008, T009 and T010 are `ACCEPTED`, integrated and post-integration-cleaned. D041, D042 and D043 are integrated and cleaned. L002 remains `ANALYZED` and separate.

D036 — Existing-System Assurance Audit Mode — remains `ACCEPTED`; canonical Core on `develop` remains Protocol `1.12.0` with `ASSURANCE.md` staged.

D040 Phase B activation candidate is PR #81 from `docs/d040-phase-b-assurance-activation`.

OP012 verified exact candidate HEAD `1207637673619b40234556d0b37cac8401ffc83a` and returned `BLOCKED`:

```text
MARKDOWN_ONLY: YES
FOCUSED_PYTEST: FAIL
FULL_PYTEST: FAIL
RUFF_CHECK: PASS
RUFF_FORMAT: PASS
REPO_MUTATION: NONE
```

PR #81 MUST NOT be merged while this failure remains unresolved.

## Root cause / T011

Repository inspection shows the deterministic readiness work is incomplete for the active state:

- `tests/test_assurance_audit_contract.py` still explicitly asserts `Activation-State: STAGED` and Protocol `1.12.0`;
- `tests/_helpers.py` does not include `ASSURANCE.md` in `CORE_REQUIRED_MODULES`;
- therefore the Phase-B candidate correctly fails deterministic verification even though Ruff remains green.

This is executor-owned non-Markdown verification work, not a Markdown-candidate repair.

Corrective Task Contract:

`docs/tasks/T011-assurance-active-routing-verification.md`

T011 updates deterministic verification to model staged and active assurance states while preserving `governance-core/GOVERNANCE.md` as the sole mutable current-version authority.

## D040 invariant

```text
Phase-B candidate red
    -> do not merge
    -> persist corrective executable contract
    -> executor updates verification on current develop
    -> accept/integrate/clean corrective task
    -> refresh/rebase candidate from current develop
    -> rerun OP012 against exact new candidate HEAD
```

No `SOURCE_PROTOCOL_VERSION = "1.13.0"`-style second authority may be introduced.

L001 remains `CONTROL_FAILURE`.

## PR #81 state

PR #81 remains open and unmerged.

Its activation intent remains valid:

- `GOVERNANCE.md` -> Protocol `1.13.0`;
- `ASSURANCE.md` -> `ACTIVE`;
- source-map/context routing -> Assurance;
- assurance architecture -> Core active;
- no live-system/provider/scanner/remediation authority.

Do not mutate PR #81 to compensate for executor-owned test readiness. After T011 integration, the activation branch must be refreshed from current `develop` through a policy-compliant Markdown update and reverified as a new exact candidate HEAD.

## OP015 — T011 planning cleanup

Operational Contract:

`docs/operations/OP015-retire-t011-planning-branch.md`

OP015 becomes `READY` only after the PR integrating T011/OP015/this checkpoint is recorded in the contract.

## Executor bootstrap policy

D041:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D042 requires canonical remote freshness before contract load.

D043 removes unconditional `read AGENTS.md` from normal prompts; this planning change does not modify `AGENTS.md`, so T011/OP015 launches require no explicit AGENTS reload line.

## CodeGraph / Context7

CodeGraph initialization remains deferred until D040 Phase B is fully integrated and cleaned.

Context7 is treated as optional executor-host external documentation capability: useful for current library/API documentation, but not Governance authority, deterministic verification, security authority or repository state requirement.

## Next Action

1. Review/integrate the T011 planning PR and record its identity in OP015.
2. Execute OP015 to retire the planning branch.
3. Launch T011 from current `develop` containing the exact Task Contract.
4. Review T011 remote handoff/diff/evidence; accept only if no Markdown and no duplicate current-version authority.
5. Integrate and clean T011 implementation/acceptance branches under normal workflow.
6. Refresh PR #81 activation branch from then-current `develop` without changing its accepted activation semantics.
7. Rerun OP012 against the new exact candidate HEAD.
8. Merge Phase B only if all OP012 gates PASS with `REPO_MUTATION: NONE`.
9. Persist L001 recovery only after successful activation integration.
10. Execute OP014 activation-branch cleanup.
11. Then prepare separate CodeGraph initialization / `.gitignore` work.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. load T011 + D040 + T010-R1 for corrective implementation/review;
2. load OP015 when its cleanup is pending;
3. after T011 integration, load PR #81 exact diff + OP012 for candidate refresh/reverification;
4. load L001 only when evaluating recovery state;
5. load L002 only on a concrete handoff-identity conflict or explicit separate work.

## Do Not

- Do not merge PR #81 while OP012 is blocked.
- Do not repair executor-owned tests from the Markdown activation branch.
- Do not mark L001 `VERIFIED` before a green exact-candidate OP012 run and integration.
- Do not create another mutable exact-current protocol-version authority.
- Do not write directly to `develop` or `main`.
- Do not prescribe executor-internal methodology/tool routing.
- Do not add an unconditional `read AGENTS.md` directive.
- Do not infer live/intrusive audit or remediation authority from D036.
- Do not initialize CodeGraph in the middle of D040 recovery.
- Preserve prior procedural audit history.
