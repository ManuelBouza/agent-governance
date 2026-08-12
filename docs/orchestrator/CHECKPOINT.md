# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O029  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under:

- `docs/reviews/T004-CLOSURE.md`;
- `docs/decisions/D037-deterministic-code-only-verification.md`.

Do not resume model-facing verification without a new explicit Human Owner decision superseding D037.

## T005 — ACCEPTED, integration pending

Task Contract:

`docs/tasks/T005-d033-d034-deterministic-execution-control-contract.md`

Acceptance review:

`docs/reviews/T005-R1.md`

Executor return reviewed:

```text
STATUS: DONE
HANDOFF: handoffs/T005-executor-handoff.json
BRANCH: test/execution-control-contract
HEAD: 04b88b31790c8254dd9d0c40f29cd4720e957843
```

D029 identity:

- controlling base: `658826e8b17e7b8454cfce5a5e6c7850f07f8d35`;
- implementation anchor: `f4d6119c4351d6968588e9cfb9d921d1a10c0404`;
- final pushed HEAD: `04b88b31790c8254dd9d0c40f29cd4720e957843`;
- implementation-anchor -> final-HEAD delta is handoff-only.

Complete implementation diff is exactly:

- `tests/_helpers.py`;
- `tests/fixtures/execution_control/policy_cases.json`;
- `tests/test_execution_control_contract.py`;
- `handoffs/T005-executor-handoff.json`.

No Markdown, dependencies, lockfile, Python version, production runtime, real adapter, network/model call or real-system execution is present.

Accepted deterministic evidence:

- focused T005: 11 passed;
- T001–T003 regression subset: 115 passed;
- full suite: 126 passed;
- Ruff check/format green;
- Protocol helper alignment: `1.11.0` + `EXECUTION-CONTROL.md`;
- all required D033/D034 fixture families covered.

No GitHub commit status checks are attached to the final branch HEAD; acceptance is based on remotely persisted executor evidence plus ChatGPT remote diff/content review.

T005 implementation is authorized for normal PR to `develop`, squash preferred.

## Current Core execution-control state

Already integrated in `develop` before T005 executable work:

- `governance-core/EXECUTION-CONTROL.md` — Execution-Control-Version `1.0.0`;
- `governance-core/EXECUTION.md` — Execution-Version `1.2.0`;
- `governance-core/GOVERNANCE.md` — Protocol-Version `1.11.0`.

Core invariants:

```text
mechanism != authority
procedure semantics != terminal syntax
approved runbook != approved invocation
authority(child) ⊆ authority(parent)
```

Approval outcomes:

`ALLOW_TASK | ALLOW_EXPLICIT | REQUIRE_HUMAN | DENY`

## Human-requested D038 frontier — Gentle-AI RDD reuse without authority transfer

The Human Owner requested a durable decision to reuse useful Gentle-AI Receipt-Driven Development capabilities without transferring Agent Governance authority.

Current Gentle-AI public architecture (stable path as of this checkpoint) provides native candidate freezing, immutable candidate identity, content-bound receipts, provider-owned status/recovery and delivery-gate validation against the same receipt. It also documents that its local receipt/store does **not** authenticate against a malicious same-user local actor with equivalent filesystem/Git/binary access.

D038 must refine/supersede the blanket Gentle-AI RDD disposition in D030 by capability surface rather than enabling RDD as a parallel governance system.

Required D038 invariants:

```text
external evidence may constrain review
but cannot grant Governance acceptance

external native enforcement may block an operation
but cannot expand Governance authorization

RDD PASS != Governance ACCEPT
```

D037 remains controlling: live probabilistic/model reviewer output cannot become a required source-product verification or release gate.

Therefore D038 should distinguish at least:

- native candidate freezing / exact identity / Git re-derivation: `REUSE|ADAPT`;
- content-bound receipt and deterministic delivery-integrity validation: `REUSE|ADAPT` when usable without violating D037;
- provider status/recovery/reconciliation: `REUSE|ADAPT` as technical evidence/control;
- probabilistic reviewer findings: supplemental evidence only, never acceptance authority or mandatory D037 release proof;
- RDD task/scope/acceptance/lifecycle authority over Agent Governance: `CONFLICT|DENY`;
- RDD ability to grant merge/release authorization: `DENY`;
- stricter native denial while a selected provider path is active: real blocker, not authority to broaden scope;
- disabling RDD merely to bypass a negative selected-provider result: not allowed without an explicit Strategy/Human provider-disposition change and revalidation.

D030 clone-local disable remains the safe fallback when a bounded RDD integration cannot satisfy D037/Agent Governance authority boundaries.

Do not add Gentle-AI as a source-product dependency.

## Architecture sequence after T005

Planned deterministic stack remains:

```text
T005  D033 + D034  execution authorization/runbooks
T006  D035         security authority/freshness/verification
T007  D036         assurance audit/evidence/coverage
```

D038 is an external-provider coexistence refinement and must not silently expand T006/T007 scope.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.

## Next Action

1. Integrate `docs/reviews/T005-R1.md` + O029 through normal Markdown PR flow.
2. Open/merge the accepted T005 implementation branch through a normal implementation PR to `develop`.
3. From the resulting current `develop`, create a separate Markdown branch for D038.
4. Persist D038 and a narrow D030 supersession/reference update; preserve D037 code-only verification authority.
5. Refresh the checkpoint after D038 integration.
6. Then proceed to T006 unless the Human Owner redirects.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T005 integration is still pending, load `docs/reviews/T005-R1.md`, T005 handoff and exact branch HEAD;
2. for D038, load D030, D031, D033, D037 and current Gentle-AI public RDD architecture/threat-model evidence only as needed;
3. load D035 only when T006 planning begins;
4. do not load T004 history absent a concrete audit conflict.

## Do Not Load or Do

- Do not reopen T001–T004 absent explicit controlling reason.
- Do not add live LLM/model verification as a source-product release gate.
- Do not let RDD or another external provider grant Agent Governance acceptance, merge, release or scope authority.
- Do not treat an RDD receipt as cryptographic attestation against a same-user malicious local actor.
- Do not bypass a selected native provider denial merely by switching mechanism.
- Do not add Gentle-AI as a canonical source dependency.
- Do not start T006 before T005 implementation integration and checkpoint refresh unless Human explicitly redirects.
- Do not declare the source product stable/release-ready.
