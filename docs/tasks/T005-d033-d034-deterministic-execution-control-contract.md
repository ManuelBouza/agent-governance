# T005 — D033/D034 deterministic execution-control contract

Status: READY  
Type: test/eval + protocol alignment  
Base branch: `develop`  
Expected topic branch: `test/execution-control-contract`  
Expected executor handoff: `handoffs/T005-executor-handoff.json`  
Owner for execution: Agente de IA Ejecutor  
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Add the first deterministic repository-owned contract tests for the accepted D033/D034 Core integration.

T005 must mechanically prove that the current Core now defines:

1. effect/target-oriented execution authorization rather than command-name authorization;
2. `ALLOW_TASK | ALLOW_EXPLICIT | REQUIRE_HUMAN | DENY` outcomes with fail-closed behavior;
3. non-expansion of authority through child processes/adapters/indirection;
4. actual-target/context mismatch invalidation;
5. runbook-required versus ordinary task-local operation routing;
6. `approved runbook != approved invocation`;
7. runbook precondition/checkpoint/postcondition/recovery semantics;
8. terminal/platform-neutral adapter equivalence based on semantic effects, not command syntax;
9. unsupported/stale adapter/runbook paths blocking rather than approximating;
10. protocol/module alignment for new Core module `EXECUTION-CONTROL.md` and Protocol `1.11.0`.

T005 is a deterministic policy-contract foundation. It does **not** execute real administrative commands, remote targets, credentials, shells, cloud APIs or LLM/model calls.

## Controlling references

Read and follow:

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md` subject to D037 precedence
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`
- `docs/decisions/D030-source-maintainer-external-workflow-overlay-precedence.md`
- `docs/decisions/D031-gentle-ai-skill-registry-source-maintainer-boundary.md`
- `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`
- `docs/decisions/D033-execution-access-control-plane.md`
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`
- `docs/decisions/D037-deterministic-code-only-verification.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/EXECUTION.md`
- `governance-core/EXECUTION-CONTROL.md`
- `governance-core/COEXISTENCE.md`
- `governance-core/PROTOCOL.md`
- accepted T001–T003 deterministic harness/tests.

D035 and D036 remain accepted future layers but are explicitly outside T005 behavior scope except that T005 must leave clean extension points for them.

## Protocol alignment already authored by ChatGPT

The controlling `develop` for T005 includes the ChatGPT-owned Markdown Core change:

- `governance-core/EXECUTION-CONTROL.md` version `1.0.0`;
- `governance-core/EXECUTION.md` version `1.2.0`;
- `governance-core/GOVERNANCE.md` Protocol-Version `1.11.0`;
- Governance source-map/context-router/readiness invariants for execution control.

The executor MUST NOT edit those Markdown files. T005 verifies them mechanically.

## Primary Solution Diagram

Dominant question: how authorization, procedural execution and target effects cross control/trust boundaries.

Preferred primary view: DFD with trust boundaries.

```text
Human Owner / Strategy
        │ task + bounded approval
        ▼
┌──────── GOVERNANCE AUTHORITY BOUNDARY ────────┐
│ Task Contract                                  │
│       │                                        │
│       ▼                                        │
│ Execution Capability Envelope                  │
│ actor · target · effect · privilege · auth     │
│       │                                        │
│       ├─ ALLOW_TASK / ALLOW_EXPLICIT           │
│       ├─ REQUIRE_HUMAN ──► Human gate          │
│       └─ DENY ─────────────► BLOCKED            │
│                                                │
│ allowed material operation                     │
│       ▼                                        │
│ reused/Governance Runbook                      │
│ preconditions · semantic steps · checkpoints   │
│ postconditions · recovery · evidence           │
└──────────────────┬─────────────────────────────┘
                   │ semantic operation
                   ▼
┌──────── EXECUTION ADAPTER BOUNDARY ────────────┐
│ command environment / runner / CLI / API /     │
│ remote-management / automation adapter         │
│                                                │
│ authority(child) ⊆ authority(parent)           │
└──────────────────┬─────────────────────────────┘
                   │ bounded effect
                   ▼
┌──────────── TARGET SYSTEM BOUNDARY ────────────┐
│ actual resource/state                          │
│ native identity/privilege/security controls    │
└──────────────────┬─────────────────────────────┘
                   │ observed state/evidence
                   ▼
          checkpoint/postcondition
          PASS → continue/DONE
          FAIL → STOP/BLOCK/RECOVER
```

This diagram is current for T005. A material change from policy-contract verification into a real execution runtime/wrapper or real-system integration invalidates this design and requires Strategy revision before implementation continues.

## Supporting runbook state view

```text
SELECT
  -> BIND_INPUTS
  -> PREFLIGHT
  -> AUTHORIZE
  -> READY
  -> EXECUTE_STEP
  -> VERIFY_CHECKPOINT
  -> EXECUTE_STEP ...
  -> VERIFY_POSTCONDITIONS
  -> DONE

mismatch/failure -> BLOCKED or STOP -> RECOVER/ROLLBACK
material context/adapter drift -> STALE -> revalidate
```

This is supporting test semantics, not a new consumer persisted state machine in T005.

## Quality/security triage

- **Functional correctness / acceptance fidelity — MATERIAL:** authorization precedence and runbook semantics must be exact; a false ALLOW is a contract defect.
- **Architecture / coexistence — MATERIAL:** authorization, procedure and adapter are separate layers; project-native runbooks are reused/adapted rather than duplicated.
- **Security — MATERIAL:** T005 defines privilege, credential, remote, destructive and target boundaries. Fail-closed behavior is mandatory.
- **Privacy/data governance — BASELINE:** fixtures contain no real personal/confidential data or credentials.
- **Reliability/resilience/recovery — MATERIAL:** stale context, failed checkpoints, retries and recovery semantics must not permit accidental continuation.
- **Performance/resource cost — BASELINE:** small local fixtures/tests only.
- **Observability/diagnosability — MATERIAL:** policy decisions/blockers/evidence facts must be mechanically inspectable without raw secret-bearing transcripts.
- **Testability/verification — MATERIAL:** primary purpose of T005; D037 applies.
- **Maintainability/change isolation — MATERIAL:** test-local policy helpers only; no production execution engine.
- **Compatibility/interoperability — MATERIAL:** protocol extension is backward-compatible minor `1.11.0`; previous T001–T003 tests remain green.
- **Usability/accessibility/i18n — NOT_APPLICABLE** to the test harness; D032 interaction behavior remains unchanged.
- **Dependency/supply-chain — BASELINE:** no new packages or external executable providers.
- **Configuration/deployment/rollback — MATERIAL as policy semantics, not real execution:** fixtures cover runbook/recovery rules without changing systems.
- **Safety/harm/compliance — MATERIAL for destructive/privileged policy cases:** such effects default to Human gating/denial as defined by Core.

### Security threat disposition

T005 does not itself cross a real target/network/credential boundary, so no dynamic sandbox or live penetration environment is required. Security verification is synthetic and deterministic.

The contract must nevertheless include negative fixtures for authority escalation, target mismatch, credential misuse and control-bypass patterns because these are the Core behaviors being introduced.

## Verification architecture under D037

Use explicit facts rather than parsing arbitrary natural-language commands.

```text
Core Markdown authority
        ↓
synthetic execution-control cases (JSON)
        ↓
deterministic test-local evaluator
        ├─ authorization outcome
        ├─ runbook-required routing
        ├─ authority subset check
        ├─ target/context validity
        ├─ runbook lifecycle validity
        └─ adapter semantic equivalence
        ↓
pytest assertions
```

The test-local evaluator is not a consumer runtime or policy engine.

## Authorized committed scope

The executor may modify/create only the minimum non-Markdown artifacts required, expected to include:

- `tests/_helpers.py` for Protocol `1.11.0` and required `EXECUTION-CONTROL.md` module alignment;
- `tests/fixtures/execution_control/policy_cases.json` or one equivalently scoped non-Markdown fixture;
- `tests/test_execution_control_contract.py` or one equivalent focused deterministic test module;
- an existing Python test only if a narrow mechanical reference/version alignment is required;
- `handoffs/T005-executor-handoff.json`.

Prefer test-local helpers inside the focused test module unless reuse clearly justifies another non-production Python file.

## Explicit exclusions

Do NOT in T005:

- edit/create/delete any committed `*.md` file;
- create a production execution-control engine, command broker, shell wrapper, remote-access service or policy daemon;
- implement D035 Security Source Resolver/Versioned Security Control Set/Known-Bad registry;
- implement D036 audit findings/evidence graph/reporting;
- add real PowerShell/POSIX/cmd/Nushell/cloud/database/cluster adapters;
- execute real privileged, destructive, remote or persistent-system changes;
- read/use real credentials or secret stores;
- add network calls to ordinary tests;
- add LLM/model calls, model graders or agent-facing evals;
- add dependencies or modify `pyproject.toml`, `uv.lock` or `.python-version`;
- create Consumer/Maintainer Skills;
- create live `.agent-governance/` or `.agent-coordination/` consumer state outside disposable synthetic fixtures;
- install/configure external SDD/security/runbook products;
- modify global OpenCode/Gentle-AI/workstation configuration;
- open or merge an implementation PR before ChatGPT acceptance.

## Required deterministic fixture families

### A. Approval outcome / strictest-effect cases

Represent at least:

1. ordinary repository observation/build/test within task → `ALLOW_TASK`;
2. explicitly named non-production remote/service mutation with bounded identity/privilege → `ALLOW_EXPLICIT`;
3. production deployment/service mutation → `REQUIRE_HUMAN`;
4. administrator/root/global-system configuration → `REQUIRE_HUMAN`;
5. credential lifecycle broadening/rotation/revocation → `REQUIRE_HUMAN` unless the fixture explicitly models a previously Human-approved bounded gate;
6. destructive/irreversible persistent effect → `REQUIRE_HUMAN`;
7. unknown/mismatched target → `DENY`;
8. host/service identity verification bypass → `DENY`;
9. credential discovery/exfiltration/persistence outside approved use → `DENY`;
10. disabling security/audit controls merely to unblock work → `DENY`.

Tests must prove the strictest material effect/outcome wins; a lower-risk effect in the same operation cannot downgrade the result.

### B. Envelope and target identity

Represent explicit fields sufficient to prove that authorization depends on actor + target + effect + resource + privilege + credential/network scope where applicable.

Tests must reject or block:

- missing material target identity;
- requested target different from approved target;
- requested resource outside scope;
- privilege above ceiling;
- network/credential binding outside the approved target/effect;
- material context drift that changes the effective target/authority.

### C. Child/adapter authority non-expansion

Represent parent/child capability sets.

Tests must prove:

```text
authority(child) ⊆ authority(parent)
```

and fail an attempted child/adapter/script/server-side effect expansion.

The fixture must not special-case shell names; use semantic capability/effect sets.

### D. Runbook-required routing

At minimum, route as `runbook_required = true` for:

- production service/deploy mutation;
- privileged administration;
- remote persistent mutation;
- infrastructure/IAM/network/security-control changes;
- credential lifecycle work;
- persistent data/schema migration;
- destructive/recovery-sensitive operation;
- material multi-system sequencing;
- recovery/failover/restore;
- recurring maintenance with meaningful failure modes.

Represent ordinary task-local source inspection/build/test as `false`.

### E. Approved runbook versus invocation authorization

Represent a procedurally valid reusable runbook with at least two invocations:

- one authorized target/context;
- one production/mismatched target that requires Human approval or blocks.

Tests must prove runbook validity does not grant invocation authority.

### F. Runbook lifecycle / failure paths

Mechanically validate the legal conceptual sequence:

`SELECT -> BIND_INPUTS -> PREFLIGHT -> AUTHORIZE -> READY -> EXECUTE_STEP -> VERIFY_CHECKPOINT -> VERIFY_POSTCONDITIONS -> DONE`

with repeated `EXECUTE_STEP/VERIFY_CHECKPOINT` allowed for additional semantic steps.

Cover at least:

- preflight/authorization mismatch → `BLOCKED`;
- checkpoint failure → `STOP` then `RECOVER/ROLLBACK` or `BLOCKED`;
- material context/adapter drift → `STALE` requiring revalidation;
- Human denial → no transition to execution;
- successful client exit without required postcondition evidence → not `DONE`.

Do not create a new production state machine module; this is test-local contract modeling.

### G. Terminal-neutral adapter equivalence

Use materially different synthetic adapter labels/families, for example:

- a command-environment realization;
- a native CLI/API/automation realization.

Their command/syntax strings, if included as inert fixture data, SHOULD differ while their semantic fingerprints match.

Tests compare semantic target/effect/privilege/order/checkpoint/recovery/evidence facts, not executable names.

A fixture whose adapter changes a material semantic boundary must be non-equivalent/fail.

### H. Unsupported/stale adapter path

Cover:

- adapter cannot implement/verify required semantic step → block/unsupported;
- adapter/tool drift changes target/auth/status/recovery semantics → stale/revalidate;
- stricter native denial remains a blocker and is not converted into another adapter bypass.

### I. Evidence semantics

Verify that a material invocation evidence fixture contains the required applicable semantic references (task/authorization, target, runbook, adapter, checkpoints/postconditions/recovery) and does not require a raw terminal transcript or secret value as canonical evidence.

## Core-reference/version assertions

Tests must prove:

- `SOURCE_PROTOCOL_VERSION == "1.11.0"`;
- `CORE_REQUIRED_MODULES` contains `EXECUTION-CONTROL.md`;
- `governance-core/GOVERNANCE.md` declares Protocol-Version `1.11.0`;
- Governance source map references `.agent-governance/EXECUTION-CONTROL.md`;
- `EXECUTION.md` routes applicable work to `EXECUTION-CONTROL.md`;
- no command-environment/OS product becomes a required correctness dependency.

Do not weaken existing exact protocol/module assertions.

## Acceptance criteria

ChatGPT may accept T005 only if:

1. work begins from a `develop` revision containing this exact READY Task Contract and Core `1.11.0` execution-control integration;
2. implementation occurs on `test/execution-control-contract`;
3. executor changes no Markdown;
4. protocol/module helper alignment is updated exactly to `1.11.0` + `EXECUTION-CONTROL.md`;
5. all four approval outcomes are mechanically covered with strictest-effect behavior;
6. target/resource/privilege/credential/network/context mismatch cases fail closed as applicable;
7. child/adapter authority expansion is mechanically rejected;
8. runbook-required routing distinguishes material operational work from ordinary task-local work;
9. valid runbook does not imply authorized invocation;
10. runbook conceptual lifecycle and failure/stale/recovery paths are mechanically represented;
11. adapter equivalence depends on semantic fingerprint, not command/shell syntax;
12. unsupported/stale/native-denied adapter cases block rather than approximate/bypass;
13. material invocation evidence is semantic/sanitized and does not require raw terminal transcript or secrets;
14. no production/runtime execution engine or platform-specific adapter is introduced;
15. tests use no network, credentials, LLM/provider or real-system mutation;
16. no dependency/toolchain changes are introduced;
17. focused T005 tests pass;
18. previously accepted T001–T003 regression coverage remains green;
19. canonical locked verification passes completely;
20. handoff accurately records implementation/evidence under D029 and branch is pushed before visible completion.

## Verification requirements

Run focused tests during implementation, then the canonical gate:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

The final handoff must record:

- exact implementation base SHA;
- D029 `implementation_head_sha` and final pushed branch HEAD semantics;
- exact changed paths;
- focused T005 command/result counts;
- full-suite pass/fail/skip/collected counts;
- Python/uv/pytest/Ruff versions;
- fixture families implemented;
- approval/outcome cases;
- envelope/target mismatch cases;
- authority subset cases;
- runbook routing/lifecycle cases;
- adapter-equivalence/stale/unsupported cases;
- evidence-semantics cases;
- protocol/module alignment facts;
- confirmation of zero network/credential/model/real-system execution;
- confirmation of no Markdown/dependency/global-config mutation;
- Gentle-AI RDD/`.atl` facts under D030/D031 when applicable;
- unresolved issues, if any.

## Stop / escalation conditions

Stop and persist `BLOCKED` or `PARTIAL` instead of guessing if:

- current `develop` no longer contains the exact Core `1.11.0`/`EXECUTION-CONTROL.md` premise;
- D033/D034/Core text leaves a required deterministic outcome materially ambiguous;
- satisfying the contract would require interpreting arbitrary natural language rather than explicit fixture facts;
- a real system/credential/network/privilege operation would be required;
- implementation would require Markdown, dependency, production runtime or global configuration changes;
- an unrelated canonical regression exists outside authorized scope.

## Expected handoff

Persist before visible completion:

`handoffs/T005-executor-handoff.json`

Then commit and push the implementation branch.

Visible executor return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T005-executor-handoff.json
BRANCH: <topic-branch>
HEAD: <actual-pushed-final-branch-head-sha>
```
