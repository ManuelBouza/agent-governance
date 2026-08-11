# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O028  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 is terminal:

`CANCELLED_BY_HUMAN`

Controlling closure/policy:

- `docs/reviews/T004-CLOSURE.md`
- `docs/decisions/D037-deterministic-code-only-verification.md`

Do not resume T004, run model-facing verification, or integrate `eval/d032-agent-capability` without a new explicit Human Owner decision superseding D037.

## Verification Policy

D037 is active:

```text
probabilistic implementation assistant != verification authority
source-product acceptance = deterministic evidence + authorized Human/Orchestrator judgment
```

Repository-owned verification/release gates use deterministic code/fixtures/property/state/security/configuration/provenance evidence. No live LLM calls, model graders, generated-transcript scoring or stochastic model thresholds are source-product release dependencies.

## Architecture Decomposition D033–D036

The accepted execution/security/audit frontier is intentionally decomposed:

```text
T005  D033 + D034
      execution authorization + runbook/terminal-neutral procedure contract

T006  D035
      security authority/freshness/known-bad/independent verification

T007  D036
      existing-system assurance audit/evidence/coverage contract
```

Rationale: D033 and D034 are one authorization/procedure layer and must remain coherent. D035 depends on that foundation but adds independently testable current-security authority/posture semantics. D036 consumes the preceding layers and adds assessment/evidence/report semantics. This keeps work atomic and reworkable under D037.

## T005 — Current Active Work Unit

Task Contract:

`docs/tasks/T005-d033-d034-deterministic-execution-control-contract.md`

Status after planning integration: `READY`.

Expected executor branch:

`test/execution-control-contract`

Expected handoff:

`handoffs/T005-executor-handoff.json`

Owner for executable work: Agente de IA Ejecutor.

T005 tests the ChatGPT-owned Core execution-control integration; the executor must not edit Markdown.

### T005 Core integration authored by ChatGPT

T005 planning introduces:

- `governance-core/EXECUTION-CONTROL.md` — Execution-Control-Version `1.0.0`;
- `governance-core/EXECUTION.md` — Execution-Version `1.2.0`;
- `governance-core/GOVERNANCE.md` — Protocol-Version `1.11.0` with source-map/context-router/readiness execution-control routing.

Protocol `1.11.0` is a backward-compatible minor extension under `PROTOCOL.md` semver rules.

Core execution invariants:

```text
mechanism != authority
procedure semantics != terminal syntax
approved runbook != approved invocation
authority(child) ⊆ authority(parent)
```

Approval outcomes:

`ALLOW_TASK | ALLOW_EXPLICIT | REQUIRE_HUMAN | DENY`

Material execution is governed by actor/target/effect/resource/privilege/credential/network scope and approval mode, not executable name.

Runbooks are required for material/repeatable/risky/recovery-sensitive operations; ordinary local source/build/test work does not require a runbook when no durable procedure adds value.

Execution adapters remain terminal/platform neutral. T005 creates no real command broker, shell wrapper, cloud adapter or remote execution runtime.

## T005 Primary Solution Diagram

Primary view: DFD with trust boundaries.

```text
Human Owner / Strategy
        │ task + bounded approval
        ▼
┌──────── GOVERNANCE AUTHORITY BOUNDARY ────────┐
│ Task Contract                                  │
│       ▼                                        │
│ Execution Capability Envelope                  │
│ actor · target · effect · privilege · auth     │
│       ├─ ALLOW_TASK / ALLOW_EXPLICIT           │
│       ├─ REQUIRE_HUMAN ─► Human gate           │
│       └─ DENY ───────────► BLOCKED              │
│       ▼                                        │
│ Runbook: preconditions/steps/checkpoints/       │
│          postconditions/recovery/evidence       │
└──────────────────┬─────────────────────────────┘
                   ▼
┌──────── EXECUTION ADAPTER BOUNDARY ────────────┐
│ terminal/runner/CLI/API/remote/automation       │
│ authority(child) ⊆ authority(parent)           │
└──────────────────┬─────────────────────────────┘
                   ▼
┌──────────── TARGET SYSTEM BOUNDARY ────────────┐
│ actual resource + native access controls        │
└──────────────────┬─────────────────────────────┘
                   ▼
        observed postcondition/evidence
        PASS → continue/DONE
        FAIL → STOP/BLOCK/RECOVER
```

A material change into a real execution runtime or real-system adapter invalidates T005 readiness and requires Strategy revision.

## T005 Quality/Security Disposition

Material:

- correctness/acceptance;
- architecture/coexistence;
- security;
- reliability/recovery;
- observability/evidence;
- testability;
- maintainability/change isolation;
- compatibility/protocol alignment;
- configuration/deployment/rollback semantics;
- destructive/privileged safety semantics.

Baseline/not applicable for the local test harness:

- privacy/data: baseline, no real sensitive data;
- performance/resource cost: baseline;
- human UI/accessibility/i18n: not applicable;
- dependency supply chain: baseline, no new dependencies.

T005 security testing is synthetic/deterministic. It must include negative authority-escalation, target-mismatch, credential misuse and security-control-bypass cases but must not touch real credentials/networks/privilege/remote systems.

## T005 Expected Executable Scope

Expected non-Markdown implementation shape:

- `tests/_helpers.py` — Protocol `1.11.0` + required `EXECUTION-CONTROL.md`;
- `tests/fixtures/execution_control/policy_cases.json` or equivalent;
- `tests/test_execution_control_contract.py` or equivalent;
- `handoffs/T005-executor-handoff.json`;
- only a narrowly required existing Python test if mechanical alignment demands it.

No production runtime, real adapter, network/model call, dependency/config change or Markdown mutation is authorized.

Required deterministic families include:

- all four approval outcomes and strictest-effect precedence;
- envelope/target/resource/privilege/credential/network/context mismatch;
- child/adapter authority non-expansion;
- runbook-required routing;
- runbook validity versus invocation authorization;
- runbook lifecycle/failure/stale/recovery behavior;
- terminal-neutral adapter semantic equivalence;
- unsupported/stale/native-denied adapter blocking;
- semantic/sanitized invocation evidence;
- Protocol/Core module reference alignment.

Canonical verification remains:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

No network, credentials, LLM/provider or real-system mutation in ordinary T005 verification.

## Future Frontier

After T005 acceptance/integration:

1. T006 integrates D035 security authority/freshness/known-bad/security-posture deterministic semantics on top of T005;
2. T007 integrates D036 audit scope/profiles/evidence graph/findings/coverage deterministic semantics;
3. only after those foundations should project-native real-system verifier/runbook adapters be considered, under explicit D033/D034 authorization and D037 deterministic evidence.

The source product remains not stable/release-ready.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.

## Next Action

1. Review the Markdown diff on `docs/t005-execution-control-core`.
2. Integrate the planning/Core change to `develop` through normal Markdown PR flow if the diff contains only the intended Core/Task/checkpoint paths.
3. Launch the executor from the resulting current `develop` with only a pointer to `docs/tasks/T005-d033-d034-deterministic-execution-control-contract.md`.
4. On return, verify D029 identity, remote diff and deterministic evidence.
5. Accept/rework T005 before any implementation PR.
6. After T005 integration, define T006; do not implement D035/D036 inside T005.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T005-d033-d034-deterministic-execution-control-contract.md`;
2. load `governance-core/EXECUTION-CONTROL.md` and `governance-core/EXECUTION.md`;
3. load D033/D034/D037 only if semantic/review context is needed;
4. if executor returned, fetch `handoffs/T005-executor-handoff.json` and exact remote branch/diff;
5. do not load T004 history absent a concrete audit conflict;
6. do not load D035/D036 until T005 is accepted or a concrete dependency question requires them.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent regression.
- Do not resume/integrate T004.
- Do not add live LLM/model verification.
- Do not turn T005 into a terminal/shell/OS-specific implementation.
- Do not execute real remote/privileged/destructive/credentialed operations in T005.
- Do not implement D035/D036 inside T005.
- Do not allow executor Markdown edits.
- Do not open/merge T005 implementation PR before ChatGPT acceptance.
- Do not declare source product stable/release-ready.
