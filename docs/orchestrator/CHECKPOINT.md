# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O059  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T006, T008, T009 and T010 are `ACCEPTED`, integrated and post-integration-cleaned. D041, D042 and D043 are integrated and cleaned. L002 remains `ANALYZED` and separate.

D036 — Existing-System Assurance Audit Mode — is `ACCEPTED`. D040 controls atomic protocol migration/single-version authority. T010 completed D040 Phase A and removed the independently mutable current-protocol literal from executor-owned verification.

Canonical `develop` before this candidate is `cc703f3e2abd71d73be91d602e484175ef35cd46`.

## D040 Phase B activation candidate

Current candidate branch:

`docs/d040-phase-b-assurance-activation`

PR:

`#81`

Candidate intent:

```text
GOVERNANCE.md -> Protocol 1.13.0
ASSURANCE.md  -> ACTIVE
source map/router/invariants -> ASSURANCE
architecture -> CORE ACTIVE
        ↓
OP012 exact-candidate deterministic verification
        ↓
merge only if all gates PASS without mutation
```

L001 remains `CONTROL_FAILURE` in the candidate. Do not mark it `VERIFIED` before OP012 proves the exact candidate and the activation is integrated.

## OP012 — exact candidate verification

Operational Contract:

`docs/operations/OP012-verify-d040-phase-b-activation-candidate.md`

Status: `READY`.

OP012 must verify the exact current remote HEAD of `docs/d040-phase-b-assurance-activation` and requires:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

The operation is read-only. It MUST NOT repair, format, commit or push candidate content. Any required non-Markdown correction blocks the activation and requires a new Task Contract.

## OP014 — activation-branch cleanup

Operational Contract:

`docs/operations/OP014-retire-d040-phase-b-assurance-activation-branch.md`

Status: `READY` but executable only after PR #81 is successfully merged.

OP014 retires only the merged PR #81 source branch.

## Assurance state in this candidate

- `governance-core/GOVERNANCE.md`: `Protocol-Version: 1.13.0`;
- `governance-core/ASSURANCE.md`: `Assurance-Audit-Version: 1.0.0`, `Activation-State: ACTIVE`;
- `ASSURANCE.md` is routed in the Source Map and Context Router;
- assurance claims remain evidence-first and bounded;
- activation does not grant live-system, scanner/provider, intrusive-assessment or remediation authority.

## Executor bootstrap policy

D041:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D042 requires canonical remote freshness before contract load.

D043 removes unconditional `read AGENTS.md` from normal delegated prompts. PR #81 does not modify `AGENTS.md`, so OP012 does not require an explicit AGENTS reload line.

## Learning state

L001 — `verification.regression.protocol_version_drift` — `CONTROL_FAILURE` pending exact-candidate verification and activation integration.

Recovery requires the Protocol `1.13.0` candidate to pass all OP012 gates without any executor-side current-version synchronization and then be integrated without introducing a second version authority.

L002 — `task.handoff.identity_mismatch` — `ANALYZED`, non-blocking and separate.

## CodeGraph next

CodeGraph project initialization remains deliberately separate from D040 Phase B.

After D040 Phase B is integrated and OP014 cleanup closes, prepare a separate executor-owned change/operation to:

- initialize CodeGraph locally for this repository;
- add `.codegraph/` to canonical `.gitignore`;
- verify CodeGraph is usable;
- verify generated `.codegraph/` state remains local/untracked;
- keep CodeGraph as executor capability, not Governance authority, correctness dependency or product state.

## Next Action

1. Review exact PR #81 changed paths/diff and stabilize candidate HEAD.
2. Launch OP012 against that exact remote HEAD using D042/D043 bootstrap.
3. If OP012 is `DONE`, all four gates are PASS, candidate is Markdown-only and `REPO_MUTATION: NONE`, merge exact tested PR #81 HEAD.
4. Persist L001 recovery evidence/status in a follow-up Markdown record from resulting `develop`; do not mutate the tested candidate before merge.
5. Execute OP014 and verify remote/local activation-branch cleanup.
6. Then create the separate CodeGraph initialization work.
7. Do not start real-system assurance adapters/providers until a later explicit decision/Task Contract authorizes them.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. for OP012 review/execution, load OP012 + exact PR #81 diff + D040 + T010-R1;
2. after OP012 PASS/merge, load L001 + exact verification result + merged PR #81 identity;
3. for OP014, load its Operational Contract plus branch-cleanup policy;
4. for CodeGraph work, load the current `.gitignore`, D041 and the separate CodeGraph contract/decision created for that scope;
5. load L002 only on a concrete handoff-identity conflict or explicit separate control-selection work.

## Do Not

- Do not write directly to `develop` or `main`.
- Do not merge PR #81 without exact-candidate OP012 PASS evidence.
- Do not mark L001 `VERIFIED` before activation integration.
- Do not mutate the candidate during OP012 verification.
- Do not accept a red intermediate `develop`.
- Do not create another mutable exact-current protocol-version authority.
- Do not prescribe executor-internal methodology/tool routing.
- Do not add an unconditional `read AGENTS.md` directive to normal launch prompts.
- Do not initialize CodeGraph as part of D040 Phase B.
- Do not infer intrusive/live assessment authorization from D036/T010.
- Do not add scanner/provider/model/network dependencies to this phase.
- Do not fold L002 into D036/D040.
- Preserve prior procedural audit history.
