# T006 — D035 deterministic security-verification contract

Status: READY  
Type: test/eval + protocol alignment  
Base branch: `develop`  
Expected topic branch: `test/security-verification-contract`  
Expected executor handoff: `handoffs/T006-executor-handoff.json`  
Owner for execution: Agente de IA Ejecutor  
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Add the first deterministic repository-owned contract tests for the accepted D035 Security Authority & Verification Plane and its portable Core integration.

T006 must mechanically prove that the current Core now defines:

1. security-sensitive facts are resolved from explicit authoritative source/control facts rather than model prior knowledge;
2. security freshness is class-aware and may be `CURRENT | STALE | UNKNOWN | CONFLICT | SUPERSEDED`;
3. applicable active known-bad state blocks security acceptance even when the obsolete pattern is statistically common or model-recommended;
4. security acceptance requires independent evidence and uses `PASS | BLOCK | HUMAN_EXCEPTION` semantics;
5. a Human security exception is exact-scope, requires verified compensating controls and becomes blocking again when expired/out of scope;
6. historical task acceptance remains historical while new advisories/vulnerabilities/drift can invalidate current security posture;
7. security evaluation and D033/D034 execution authorization are independent non-expanding control planes;
8. `security PASS != execution authorization` and `execution authorization != security PASS`;
9. portable Core security semantics are provider/SDD/tool neutral and do not require a particular external product, scanner, feed, schema or model;
10. Protocol/module alignment includes `SECURITY.md` and Protocol `1.12.0`.

T006 is a deterministic policy-contract foundation. It does **not** fetch live vulnerability data, inspect real systems, run security scanners, call models, integrate an external provider or implement D036 assurance-audit reporting.

## Controlling references

Read and follow:

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md` subject to D037 precedence
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`
- `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`
- `docs/decisions/D033-execution-access-control-plane.md`
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md`
- `docs/decisions/D037-deterministic-code-only-verification.md`
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/QUALITY.md`
- `governance-core/SECURITY.md`
- `governance-core/EXECUTION-CONTROL.md`
- `governance-core/COEXISTENCE.md`
- accepted deterministic harness/tests from T001–T003 and T005.

D036 remains explicitly outside T006. D038/D030 external-provider decisions are not implementation dependencies for this task; T006 must remain provider-neutral. If external-provider behavior becomes necessary to satisfy the task, stop and escalate rather than adding it.

## Protocol alignment already authored by ChatGPT

The controlling `develop` for executor launch must include this ChatGPT-owned Markdown Core change:

- new `governance-core/SECURITY.md` version `1.0.0`;
- `governance-core/GOVERNANCE.md` Protocol-Version `1.12.0`;
- source-map/context-router/readiness invariants routing material security to `SECURITY.md`;
- explicit security/execution non-expansion and temporal-posture invariants.

The executor MUST NOT edit those Markdown files.

## Primary Solution Diagram

Dominant question: how current security authority constrains a security-sensitive scope, how deterministic verification determines posture, and how future security signals invalidate current posture without rewriting historical acceptance.

Preferred primary view: compact control/data-flow diagram.

```text
Security-sensitive scope
        │
        ▼
┌──────────── SECURITY AUTHORITY BOUNDARY ────────────┐
│ Security Source Resolver                            │
│ project · vendor/product · threat intel · baseline  │
│        │                                             │
│        ▼                                             │
│ Versioned Security Control Set                       │
│ required/forbidden state · applicability · source    │
│ freshness · verifier · exception · regression        │
│        │                                             │
│   ┌────┼──────────────┐                              │
│   ▼    ▼              ▼                              │
│fresh  known-bad     exception                        │
│state  applicability validity/expiry                  │
└───┬────┴──────┬───────┴──────────────────────────────┘
    └───────────▼───────────────────────────────────────┐
                current security posture               │
                │                                      │
                ▼                                      │
        independent deterministic verifier             │
                │                                      │
        PASS | BLOCK | HUMAN_EXCEPTION                 │
                │                                      │
                ├──────────────► acceptance/evidence   │
                │                                      │
                ▼                                      │
       temporal invalidation signal                    │
 advisory · vulnerability · drift · supersession       │
                │                                      │
                └─► STALE/VIOLATED/remediation         │
                                                       │
 historical task acceptance remains immutable          │
└───────────────────────────────────────────────────────┘

Separate composition plane:

security PASS/BLOCK/HUMAN_EXCEPTION
            ⟂
D033/D034 execution ALLOW/REQUIRE_HUMAN/DENY

Neither plane grants authority owned by the other.
```

This diagram is current for T006. A material change from deterministic policy-contract verification into live security intelligence, scanner/provider integration, real-target verification or D036 audit/evidence-graph implementation invalidates this design and requires Strategy revision before implementation continues.

## Quality/security triage

- **Functional correctness / acceptance fidelity — MATERIAL:** security outcome precedence, applicability, freshness, exception validity and temporal invalidation must be deterministic and fail closed.
- **Architecture / coexistence — MATERIAL:** security authority/verification is a focused Core plane; D033/D034 execution control remains separate; external/native providers are optional capability/evidence sources, not Core dependencies.
- **Security — MATERIAL:** primary purpose of T006. The tests must demonstrate that obsolete/vulnerable state cannot pass because it is statistically common or model-supported.
- **Privacy/data governance — BASELINE:** synthetic fixtures contain no personal/confidential/regulated data.
- **Reliability/resilience — MATERIAL:** stale/unknown/conflicting authority and expired exceptions must block rather than degrade silently; invalidation must not corrupt historical acceptance.
- **Performance/resource cost — BASELINE:** small local deterministic fixtures/tests only.
- **Observability/diagnosability — MATERIAL:** test facts must make source/freshness/applicability/verifier/exception/posture outcomes mechanically inspectable.
- **Testability/verification — MATERIAL:** T006 is deterministic under D037; no model graders or live external data.
- **Maintainability/change isolation — MATERIAL:** use a focused fixture/test module and test-local evaluator; do not create a consumer runtime/security engine.
- **Compatibility/interoperability — MATERIAL:** Protocol `1.12.0` is a backward-compatible minor extension; T001–T003/T005 behavior must remain green.
- **Usability/accessibility/i18n — NOT_APPLICABLE** to the deterministic test harness; Human-facing interaction semantics are unchanged.
- **Dependency/supply-chain — MATERIAL conceptually, BASELINE operationally:** provenance is part of Core semantics, but T006 installs/fetches no packages/rulesets/providers and adds no dependency.
- **Configuration/deployment/rollback — BASELINE for implementation:** no real configuration/deployment occurs; temporal/system security semantics are represented synthetically only.
- **Safety/harm/compliance — MATERIAL:** security blockers/exceptions must not be weakened by model explanation or implementation convenience.

### Security threat disposition

T006 does not cross a real network, credential, target-system or provider boundary. No live threat-intelligence retrieval, vulnerability scanning, penetration environment or external security service is required.

The main failure mode is a policy-contract false `PASS`. Negative deterministic fixtures therefore control the task.

## Verification architecture under D037

Use explicit normalized facts. Do not parse arbitrary natural-language security prose, command text, external pages or model output.

```text
Core Markdown authority
        ↓
synthetic security cases (JSON)
        ↓
deterministic test-local evaluator
        ├─ source/applicability state
        ├─ freshness state
        ├─ known-bad applicability
        ├─ verifier/evidence state
        ├─ exception scope/expiry
        ├─ security acceptance outcome
        ├─ temporal posture invalidation
        └─ security/execution composition
        ↓
pytest assertions
```

The evaluator is test scaffolding only. It is not a consumer Security Source Resolver, policy engine, vulnerability manager, scanner adapter or runtime.

All time-sensitive cases must use explicit fixture evaluation timestamps/versions. Tests MUST NOT depend on wall-clock time, network state or mutable external advisory data.

## Authorized committed scope

The executor may modify/create only the minimum non-Markdown artifacts required, expected to include:

- `tests/_helpers.py` for Protocol `1.12.0` and required `SECURITY.md` module alignment;
- `tests/fixtures/security_verification/policy_cases.json` or one equivalently scoped non-Markdown fixture;
- `tests/test_security_verification_contract.py` or one equivalent focused deterministic test module;
- an existing Python test only if a narrow mechanical reference/version alignment is required;
- `handoffs/T006-executor-handoff.json`.

Prefer test-local helpers/evaluators inside the focused test module unless reuse clearly justifies another non-production Python file.

## Explicit exclusions

Do NOT in T006:

- edit/create/delete any committed `*.md` file;
- implement D036 audit mode, findings graph, assurance report, coverage model or audit evidence graph;
- create a production Security Source Resolver, Versioned Security Control Set runtime/database, Known-Bad registry service, policy daemon or posture monitor;
- fetch live CVE/KEV/vendor/advisory/benchmark data;
- add network calls to ordinary tests;
- integrate or require any external SDD, workflow, review-receipt, vulnerability, compliance, scanner, policy-as-code or security provider;
- add provider-specific paths, commands, schemas, receipts or lifecycle states to portable Core/test semantics;
- add LLM/model calls, model graders or probabilistic reviewer gates;
- treat a model/reviewer assertion as security verification evidence;
- execute real privileged, destructive, remote, deployment or persistent-system changes;
- read/use real credentials or secret stores;
- add dependencies or modify `pyproject.toml`, `uv.lock` or `.python-version`;
- create Consumer/Maintainer Skills;
- create live `.agent-governance/` or `.agent-coordination/` consumer state outside disposable synthetic fixtures;
- modify global agent/SDD/workstation configuration;
- open or merge an implementation PR before ChatGPT acceptance.

## Required deterministic fixture families

### A. Security authority and source conflict

Represent explicit source/control facts sufficient to prove:

1. project-authoritative, product/vendor, threat-intelligence and versioned-baseline source classes can participate without model knowledge becoming authoritative;
2. applicable compatible sources produce a usable control set;
3. unresolved material authoritative-source conflict produces `CONFLICT`/blocking state;
4. an unsupported/model-only assertion cannot establish current authoritative security state.

Do not encode real vendor/product names as required semantics. Synthetic identities are sufficient.

### B. Freshness classes and states

Represent `THREAT_LIVE`, `PRODUCT_VERSION`, `STANDARD_PINNED` and `PROJECT_DECISION` cases with explicit fixture evaluation points.

Tests must cover at least:

- current threat-live source at required recheck point;
- stale threat-live source;
- product-version context change invalidating prior source state;
- pinned stable baseline remaining selected despite a newer available revision signal;
- project decision current until superseded;
- weakening security exception expiry affecting its validity;
- `UNKNOWN` and unresolved `CONFLICT` blocking when current knowledge is required;
- `SUPERSEDED` control excluded from active acceptance evaluation.

No test may call current wall-clock time or the network.

### C. Known-bad applicability and probabilistic-prior resistance

Represent scoped/versioned known-bad records covering `ACTIVE | MITIGATED | SUPERSEDED | NOT_APPLICABLE | EXCEPTION`.

Tests must prove:

```text
applicable ACTIVE known-bad -> BLOCK
```

regardless of inert fixture metadata such as:

- `model_recommends: true`;
- `historically_common: true`;
- high synthetic prevalence/popularity;
- a prior acceptance from a different context/version.

Also prove that non-applicable/superseded records do not block merely because their pattern exists historically.

### D. Independent verification and acceptance outcomes

Represent controls requiring independent evidence.

Tests must cover all outcomes:

- all blocking applicable controls current + evidence passes -> `PASS`;
- any failed required verifier -> `BLOCK`;
- required evidence missing -> `BLOCK`;
- stale/unknown/conflict source -> `BLOCK`;
- applicable active known-bad state -> `BLOCK`;
- actual-state mismatch -> `BLOCK`;
- valid exact-scope Human exception with compensating evidence -> `HUMAN_EXCEPTION`.

A synthetic `model_claims_secure`/reviewer claim must have no authority to change the result.

### E. Human exception scope, evidence and expiry

Represent at least:

- exact target/control/version match + verified compensating controls + unexpired review condition -> `HUMAN_EXCEPTION`;
- target/version/control mismatch -> invalid/block;
- missing compensating-control evidence -> invalid/block;
- expired exception -> invalid/block;
- attempted use of one exception for an unrelated control -> invalid/block.

Tests must prove exception scope does not expand through child/related context.

### F. Temporal posture invalidation

Represent historical acceptance and current posture as separate facts.

Tests must prove:

```text
historical_acceptance = ACCEPTED
new applicable advisory/vulnerability/drift
        -> historical_acceptance remains ACCEPTED
        -> current posture becomes STALE/VIOLATED/BLOCKING
```

Also include a non-applicable invalidation signal that leaves current posture unchanged.

The evaluator must not rewrite historical acceptance state.

### G. Security and execution-control composition

Use normalized synthetic security outcome and D033/D034 authorization facts.

Tests must prove at least:

- security `PASS` + execution `DENY` -> operation remains execution-blocked;
- security `PASS` + execution `REQUIRE_HUMAN` -> Human execution gate remains required;
- security `BLOCK` + execution `ALLOW_TASK/ALLOW_EXPLICIT` -> security acceptance remains blocked;
- security `HUMAN_EXCEPTION` does not create execution authorization;
- execution/runbook/adapter success does not manufacture security `PASS` when evidence is missing;
- target/context drift invalidates the affected security evidence independently of execution authorization.

The focused test may reuse conceptual outcome names from T005 but must not alter T005 implementation semantics.

### H. Core/protocol/provider-neutrality alignment

Tests must mechanically prove:

- `SOURCE_PROTOCOL_VERSION == "1.12.0"`;
- `SECURITY.md` is in `CORE_REQUIRED_MODULES`;
- `protocol_version_from(governance)` equals `1.12.0`;
- Governance source-map/router references `.agent-governance/SECURITY.md`/`SECURITY.md` as applicable;
- `SECURITY.md` exists and declares `Security-Verification-Version: 1.0.0`;
- the new security fixture/test contains no hard dependency on named SDD/agent/review-provider products, shell/OS syntax, network endpoints or model execution.

Provider-neutrality assertions should target the T006 fixture/test/evaluator, not reject generic compatibility examples that already exist elsewhere in repository documentation.

## Acceptance criteria

ChatGPT accepts T006 only if remote Git evidence proves all of the following:

1. changed executor-owned paths are within authorized non-Markdown scope;
2. no committed Markdown was modified by the executor;
3. all required fixture families A–H exist with deterministic assertions;
4. obsolete/applicable known-bad state blocks despite model recommendation/statistical-commonness metadata;
5. source freshness/conflict/unknown states fail closed where current authority is required;
6. independent verification is required for `PASS` and model/reviewer self-assertion cannot substitute for it;
7. Human exceptions are exact-scope, independently supported and expiry-sensitive;
8. temporal invalidation changes current posture without rewriting historical acceptance;
9. security and D033/D034 execution outcomes cannot grant each other's authority;
10. Protocol `1.12.0`/`SECURITY.md` module alignment is mechanically verified;
11. no external network/model/provider dependency is introduced;
12. no dependency/runtime/agent-host/OS-specific drift occurs;
13. focused and full deterministic verification are green;
14. executor handoff is valid under D029 and `docs/EXECUTOR-HANDOFFS.md`.

Passing tests are necessary evidence, not acceptance authority. ChatGPT reviews the remote contract, handoff, branch identity and complete diff before acceptance.

## Required verification

Run in the locked repository environment:

```text
uv run --locked pytest -q tests/test_security_verification_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

If an authorized existing test is updated for protocol/module alignment, it must be included in focused/regression evidence as appropriate.

Verification must be local/deterministic: no live security source, network, model, real system, credential or external provider is required.

## Stop / escalation conditions

Stop, persist a `BLOCKED`/`PARTIAL` handoff and do not guess if:

- the controlling Markdown/Core on `develop` does not contain the exact T006 contract and `SECURITY.md`/Protocol `1.12.0` alignment;
- implementation would require editing Markdown;
- a required behavior cannot be represented deterministically without inventing semantics not present in D035/Core;
- implementing the tests would require a production security engine rather than test scaffolding;
- a live source/network/provider/model call appears necessary;
- D036 audit/report/evidence-graph behavior appears necessary;
- an external SDD/provider-specific adapter/schema/lifecycle becomes necessary;
- a dependency change appears necessary;
- required scope would exceed the authorized files materially;
- current branch/base identity does not satisfy the Task Contract integration gate.

## Expected handoff

Before returning `DONE`, `BLOCKED`, or `PARTIAL`, persist `handoffs/T006-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit all current authorized task state and push the topic branch.

The handoff must identify at least:

- task `T006`;
- controlling `develop` base/contract identity;
- implementation anchor/final implementation identity according to D029;
- changed paths;
- focused/full pytest evidence;
- Ruff check/format evidence;
- confirmation that no Markdown/dependency/network/model/provider/real-system scope was introduced;
- any blocker/deviation.

Return to ChatGPT only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T006-executor-handoff.json
BRANCH: test/security-verification-contract
HEAD: <pushed-commit-sha>
```
