# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O058  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T006, T008, T009 and T010 are `ACCEPTED`, integrated and post-integration-cleaned. L002 remains `ANALYZED` and separate.

D036 — Existing-System Assurance Audit Mode — is `ACCEPTED` with Core module `governance-core/ASSURANCE.md` still staged. D040 controls atomic protocol migration/single-version authority. T010 completed D040 Phase A.

D041 executor-process autonomy, D042 remote-baseline freshness and D043 host-native repository-instruction loading are integrated and their cleanup operations OP008–OP011 are complete. Canonical remote branch inventory after OP011 is `develop`, `main`.

Current `develop` is `b68dfe0d43b691e471462eb62a910d4a01a00999`.

## D040 Phase B — current work

D040 Phase B is now the active frontier.

Required activation result:

```text
GOVERNANCE.md -> Protocol 1.13.0
ASSURANCE.md  -> ACTIVE
source-map/router/readiness -> ASSURANCE
        ↓
exact candidate verification
        ↓
full deterministic suite green
without current-version literal synchronization
        ↓
merge activation
        ↓
L001 -> VERIFIED
```

There is no repository CI workflow capable of supplying the required pre-merge deterministic evidence automatically.

Therefore OP012 is being persisted before activation so the Agente de IA Ejecutor can verify the exact future Markdown activation candidate read-only, without mutating it.

## OP012 — D040 Phase-B candidate verification

Operational Contract:

`docs/operations/OP012-verify-d040-phase-b-activation-candidate.md`

Status: `READY` after this planning PR is integrated.

Durable candidate branch:

`docs/d040-phase-b-assurance-activation`

OP012 verifies the exact remote candidate HEAD, requires a Markdown-only diff and runs:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

OP012 MUST NOT modify/repair/commit/push candidate content. Any need for non-Markdown correction becomes `BLOCKED` and requires a new Task Contract.

## OP013 — verification-prep cleanup

Operational Contract:

`docs/operations/OP013-retire-d040-phase-b-verification-prep-branch.md`

OP013 remains `DRAFT` until the PR integrating OP012/OP013/checkpoint is durably recorded and OP013 is marked `READY`.

## D040 / D036 staged state

Until the activation candidate is created:

- canonical Protocol remains `1.12.0`;
- `governance-core/ASSURANCE.md` remains `Assurance-Audit-Version: 1.0.0`, `Activation-State: STAGED`;
- `ASSURANCE.md` is not yet a routed required Core module;
- L001 remains `CONTROL_FAILURE`.

T010-R1 confirms the test helper now derives current protocol identity from `governance-core/GOVERNANCE.md` and no independent mutable exact-current-version literal remains.

## Executor bootstrap policy

D041:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D042 requires canonical remote freshness before contract load.

D043 removes unconditional `read AGENTS.md` from normal delegated prompts. Add an explicit AGENTS reload only when the governing integrated change modified `AGENTS.md`.

Neither this verification-prep change nor the planned D040 activation modifies `AGENTS.md`, so normal OP012/OP013 launches do not require an explicit AGENTS reload line.

## Learning state

L001 — `verification.regression.protocol_version_drift` — remains `CONTROL_FAILURE` until the exact Protocol `1.13.0` activation candidate passes OP012 without test/helper version synchronization and is integrated.

L002 — `task.handoff.identity_mismatch` — `ANALYZED`, non-blocking and separate.

## Next Action

1. Review/open the OP012/OP013/checkpoint planning PR from `docs/d040-phase-b-verification-prep`.
2. Persist that PR identity in OP013, mark OP013 `READY`, merge the planning PR and freeze its source branch.
3. Execute OP013 and verify planning-branch cleanup.
4. Create fresh Markdown branch `docs/d040-phase-b-assurance-activation` from then-current `develop`.
5. Apply only the D040 Phase-B Markdown activation: Protocol `1.13.0`, ASSURANCE activation/routing, architecture/checkpoint updates. Do not mark L001 `VERIFIED` yet.
6. Run OP012 against the exact activation-candidate remote HEAD.
7. If OP012 is `DONE` with all gates PASS and no mutation, persist final activation evidence/L001 `VERIFIED` on the same candidate branch, review exact diff, then merge.
8. If OP012 is not green, do not merge activation; create a new Task Contract for any required non-Markdown correction.
9. After activation integration, perform post-integration branch cleanup through a separately persisted Operational Contract.
10. Do not start real-system audit adapters/providers until a later explicit decision/Task Contract authorizes them.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. while verification-prep PR/OP013 is pending, load OP012, OP013 and D040;
2. for activation drafting, load D040, T010-R1, `governance-core/GOVERNANCE.md`, `governance-core/ASSURANCE.md`, `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`, and L001;
3. for OP012 result review, load exact candidate diff + OP012 response + relevant deterministic evidence;
4. load L002 only on a concrete handoff-identity conflict or explicit separate control-selection work.

## Do Not

- Do not write directly to `develop` or `main`.
- Do not merge Protocol `1.13.0` activation without exact candidate deterministic PASS evidence.
- Do not mark L001 `VERIFIED` before that evidence exists.
- Do not mutate the activation candidate during OP012 verification.
- Do not accept a red intermediate `develop`.
- Do not create another mutable exact-current protocol-version authority.
- Do not prescribe executor-internal methodology/tool routing.
- Do not add an unconditional `read AGENTS.md` directive to normal launch prompts.
- Do not infer intrusive/live assessment authorization from D036/T010.
- Do not add scanner/provider/model/network dependencies to this phase.
- Do not fold L002 into D036/D040.
- Preserve prior procedural audit history.
