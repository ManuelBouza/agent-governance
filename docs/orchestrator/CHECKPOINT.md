# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O061  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T011 — Assurance active-routing deterministic verification — is `ACCEPTED` and integrated. T011-R1 reviews executor HEAD `c231eec0cf5e96b676df9932402a3166fa4589c2`; implementation PR #84 is integrated in `develop`.

Canonical Core on `develop` remains Protocol `1.12.0` with `ASSURANCE.md` staged until D040 Phase B is integrated.

The original D040 Phase-B candidate PR #81 remains unmerged historical blocked evidence. OP012 correctly failed that candidate before T011 readiness. A later mechanical `develop` -> old candidate refresh attempt was non-mergeable and PR #85 was closed without merge.

## D040 Phase-B v2 candidate

Current candidate branch:

`docs/d040-phase-b-assurance-activation-v2`

This candidate is rebuilt directly from current `develop` containing T011 readiness.

Candidate intent:

```text
GOVERNANCE.md -> Protocol 1.13.0
ASSURANCE.md  -> ACTIVE
Source Map / Context Router -> ASSURANCE
assurance architecture -> CORE ACTIVE
        ↓
OP017 exact-candidate deterministic verification
        ↓
merge only on all-green read-only evidence
```

L001 remains `CONTROL_FAILURE` until the exact v2 candidate passes verification and the activation is integrated.

## OP017 — exact v2 verification

Operational Contract:

`docs/operations/OP017-verify-d040-phase-b-v2-candidate.md`

Status: `READY`.

OP017 requires the exact current v2 HEAD, Markdown-only diff, Protocol `1.13.0`, ACTIVE/routed `ASSURANCE.md`, and these gates:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The operation is read-only and must return `BLOCKED` on any failed gate or candidate mutation.

## Learning state

L001 — `verification.regression.protocol_version_drift` — remains `CONTROL_FAILURE` pending v2 PASS and activation integration.

L002 — `task.handoff.identity_mismatch` — remains `ANALYZED`, separate and non-blocking.

## CodeGraph / Context7

CodeGraph project initialization remains the next separate capability operation after D040 Phase B is integrated and cleaned. `.codegraph/` must remain local generated state and canonical `.gitignore` should exclude it.

Context7 remains an optional executor-host external documentation capability, not Governance authority, deterministic verification, or required repository state.

## Next Action

1. Open/review the v2 activation PR from `docs/d040-phase-b-assurance-activation-v2` to `develop`.
2. Verify its effective diff is Markdown-only and limited to the intended D040 Phase-B activation/checkpoint surfaces.
3. Execute OP017 against the exact current v2 candidate HEAD.
4. If OP017 is `DONE` with all gates PASS and `REPO_MUTATION: NONE`, merge exactly the tested candidate HEAD.
5. Persist L001 recovery evidence/status only after activation integration.
6. Retire the v2 activation branch plus obsolete historical D040/T011 branches through persisted cleanup operations.
7. Then initialize CodeGraph as a separate executor-owned capability task/operation.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. load OP017 + exact v2 candidate diff + D040 + T011-R1 for verification/review;
2. after v2 integration, load L001 + exact OP017 result + merged activation PR identity;
3. load branch-cleanup policy for post-integration cleanup;
4. for CodeGraph work, load current `.gitignore`, D041 and the separate CodeGraph contract created for that scope;
5. load L002 only on a concrete identity conflict or explicit separate control-selection work.

## Do Not

- Do not merge the original blocked PR #81.
- Do not merge the v2 candidate without exact-candidate green OP017 evidence.
- Do not mark L001 `VERIFIED` before activation integration.
- Do not create another mutable exact-current protocol-version authority.
- Do not write directly to `develop` or `main`.
- Do not prescribe executor-internal methodology/tool routing.
- Do not add an unconditional `read AGENTS.md` directive to normal executor launch prompts.
- Do not initialize CodeGraph inside D040 Phase B.
- Preserve prior procedural audit history.
