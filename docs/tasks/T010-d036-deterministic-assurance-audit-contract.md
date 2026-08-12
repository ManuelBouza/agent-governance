# T010 — D036 deterministic assurance-audit readiness contract

Status: READY  
Type: test/eval + protocol-migration readiness  
Base branch: `develop`  
Expected topic branch: `test/d036-deterministic-assurance-audit-contract`  
Expected executor handoff: `handoffs/T010-executor-handoff.json`  
Owner for execution: Agente de IA Ejecutor  
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Establish the deterministic D036 Existing-System Assurance Audit foundation **without creating a red protocol-migration intermediate state**.

T010 has two coupled responsibilities:

1. add deterministic repository-owned contract tests for staged `governance-core/ASSURANCE.md` semantics;
2. implement D040's single-current-version-authority rule so repository verification no longer depends on a separately authored mutable literal duplicating `GOVERNANCE.md`'s current `Protocol-Version`.

T010 must mechanically prove that:

1. audit scope and authorization are explicit before evidence collection;
2. assessment profiles are ordered by intrusiveness and generic audit requests do not imply intrusive testing;
3. evidence-backed findings use explicit states rather than silent binary pass/fail assumptions;
4. `NOT_ASSESSED` and `INCONCLUSIVE` never become `PASS`;
5. severity and confidence remain independent dimensions;
6. coverage accounting exposes gaps and does not infer assurance from absence of findings;
7. model opinion/tool success cannot substitute for evidence or control effectiveness;
8. audit findings do not authorize remediation;
9. historical reports remain historical while later drift/advisories may invalidate current posture;
10. security-material conclusions compose D035 without creating new security authority;
11. assessment execution composes D033/D034 without creating execution authority;
12. portable audit semantics are provider/tool/platform/model neutral;
13. current protocol identity is parsed from authoritative Core rather than duplicated as a mutable exact-current test literal;
14. staged `ASSURANCE.md` is deterministically verifiable while Protocol remains `1.12.0` and is not yet treated as an active routed/required module.

T010 is a deterministic policy-contract/readiness foundation. It does **not** activate Protocol `1.13.0`, edit Markdown, inspect a real system, fetch current advisories, run scanners, call models, access credentials, perform live queries or implement platform-specific audit adapters.

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
- `docs/decisions/D036-existing-system-assurance-audit-mode.md`
- `docs/decisions/D037-deterministic-code-only-verification.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`
- `docs/learning/L001-protocol-version-baseline-drift.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/ASSURANCE.md`
- `governance-core/QUALITY.md`
- `governance-core/SECURITY.md`
- `governance-core/EXECUTION-CONTROL.md`
- accepted deterministic harness/tests through T006/T008/T009.

L002 remains explicitly outside T010. External scanner/provider behavior is not an implementation dependency. If real-system access or external-provider behavior becomes necessary, stop and escalate rather than adding it.

## Staged Core state for executor launch

The controlling `develop` for T010 launch must have:

- `governance-core/GOVERNANCE.md` still at Protocol `1.12.0`;
- staged `governance-core/ASSURANCE.md` version `1.0.0` with `Activation-State: STAGED`;
- no `ASSURANCE.md` source-map/router activation yet;
- D040 accepted;
- L001 recorded as `CONTROL_FAILURE` with T010 selected as part of the stronger prevention control.

The executor MUST NOT edit any of those Markdown files.

After T010 is accepted/integrated/clean, ChatGPT—not the executor—will perform a separate Markdown-only D036 activation change that bumps Protocol to `1.13.0` and routes `ASSURANCE.md`. That activation is outside T010 implementation scope.

## D040 migration requirement

Current protocol identity has one authority:

```text
Core Protocol-Version = current-version authority

test helper = parser / validator / compatibility verifier
             != second current-version authority
```

T010 must remove the requirement to manually synchronize a free-standing test-side exact-current protocol literal with `GOVERNANCE.md`.

Acceptable implementation patterns include a focused helper API that parses current protocol identity from the authoritative Core file and exposes deterministic semantic-version validation to tests. The exact implementation is executor-owned.

The change MUST preserve or strengthen meaningful protocol validation. It MUST NOT replace the old literal with a permissive assertion that accepts arbitrary/malformed versions or silently ignores module/protocol consistency.

Historical fixture versions or explicit compatibility bounds may remain literal when they are genuine historical/compatibility data rather than a second mutable current-version authority.

## Primary Solution Diagram

```text
STAGED D036 MODULE
ASSURANCE.md (not routed yet)
        │
        ├───────────────┐
        ▼               ▼
synthetic assurance   authoritative
cases/evaluator       GOVERNANCE.md 1.12
        │               │
        ▼               ▼
audit semantics      protocol parser/validator
        │               │
        └───────┬───────┘
                ▼
         deterministic green suite
                │
                ▼
        T010 accepted/integrated/clean
                │
                ▼
        later Markdown activation
        GOV 1.13 + ASSURANCE routing
```

A material change into live target assessment, scanner/provider integration, credentialed observation or active testing invalidates this T010 design and requires a separately persisted strategy/task contract.

## Verification architecture under D037

Use explicit normalized synthetic facts. Do not parse arbitrary prose, external pages, command output or model output.

```text
staged ASSURANCE.md semantics
        +
synthetic assurance cases (JSON)
        ↓
deterministic test-local evaluator
        ├─ scope completeness
        ├─ profile ceiling
        ├─ evidence status
        ├─ severity/confidence separation
        ├─ coverage accounting
        ├─ remediation authorization separation
        ├─ temporal invalidation
        └─ security/execution composition

GOVERNANCE.md
        ↓
current protocol parser/validator
        ↓
no duplicated mutable current-version literal
```

The assurance evaluator is test scaffolding only. It is not a production audit engine, scanner orchestrator, evidence database or consumer runtime.

All time-sensitive cases use explicit fixture timestamps. Tests MUST NOT depend on wall-clock time, network state or mutable external sources.

## Authorized committed scope

The executor may modify/create only the minimum non-Markdown artifacts required, expected to include:

- `tests/_helpers.py` to eliminate the duplicated mutable exact-current protocol authority and provide deterministic current-version parsing/validation;
- existing deterministic Python tests that currently import/compare the duplicated `SOURCE_PROTOCOL_VERSION`, only as narrowly required to migrate them to the D040 authority model;
- `tests/fixtures/assurance_audit/policy_cases.json` or one equivalently scoped non-Markdown fixture;
- `tests/test_assurance_audit_contract.py` or one equivalent focused deterministic test module;
- `handoffs/T010-executor-handoff.json`.

Prefer test-local assurance evaluator logic inside the focused test module unless reuse clearly justifies another test-only Python file.

## Explicit exclusions

Do NOT in T010:

- edit/create/delete any committed `*.md` file;
- change `governance-core/GOVERNANCE.md` to `1.13.0` or activate `ASSURANCE.md` routing;
- weaken protocol tests into unbounded/permissive acceptance;
- create another independently authored exact-current protocol-version literal under a different name;
- inspect or connect to a real repository/application/service/system/environment other than this source repository as normal test input;
- make live authenticated system queries;
- run vulnerability scanners, DAST, fuzzing against real targets, penetration testing or intrusive assessment;
- fetch live CVE/KEV/vendor/benchmark data;
- add network calls to ordinary tests;
- integrate any external audit/security/compliance/scanner provider;
- add provider-specific commands, schemas, endpoints or lifecycle states to portable semantics;
- add LLM/model calls, graders or probabilistic reviewer gates;
- treat model/reviewer assertions as audit evidence;
- implement remediation actions or mutation workflows;
- execute privileged, destructive, remote, deployment or persistent-system changes;
- read/use real credentials or secret stores;
- add dependencies or modify `pyproject.toml`, `uv.lock` or `.python-version`;
- create live `.agent-governance/` or `.agent-coordination/` consumer state outside disposable synthetic fixtures;
- fold L002 control work into T010;
- open or merge an implementation PR before ChatGPT acceptance.

## Required deterministic fixture families

### A. Scope and authorization

Represent explicit audit-scope facts sufficient to prove:

- subject/environment/resource boundary is determinable;
- allowed methods and maximum profile are explicit;
- unavailable evidence/exclusions remain visible;
- extra credentials/reachability/tool capability cannot broaden scope;
- materially incomplete required scope fields produce blocking/not-ready state rather than implicit defaults.

### B. Assessment profile ceiling

Represent all profiles:

- `EVIDENCE_REVIEW`;
- `AUTHENTICATED_OBSERVE`;
- `SAFE_ACTIVE`;
- `INTRUSIVE_AUTHORIZED`.

Tests must prove monotonic intrusiveness and that a requested method above the authorized ceiling is rejected/blocking. Generic `security_audit: true` or tool availability MUST NOT authorize intrusive testing.

### C. Evidence graph and finding states

Represent material claims with explicit expected/observed/method/evidence/source/status fields.

Tests must cover:

- `PASS`;
- `FAIL`;
- `PARTIAL`;
- `NOT_APPLICABLE`;
- `NOT_ASSESSED`;
- `INCONCLUSIVE`;
- `ACCEPTED_EXCEPTION`.

Missing/conflicting evidence must not become `PASS`. A model-only hypothesis must not become a confirmed material finding.

### D. Severity and confidence independence

Represent combinations proving at least:

- high severity + low confidence remains high severity and triggers verification need;
- low severity + high confidence remains low severity;
- confidence cannot silently down-rank severity;
- severity cannot manufacture confidence.

No opaque single score may replace both dimensions in evaluator semantics.

### E. Coverage accounting and bounded conclusions

Represent declared domains/resources/methods with assessed and unassessed cells.

Tests must prove:

- unassessed/inconclusive cells remain coverage gaps;
- absence of FAIL findings with gaps does not yield a global `SECURE`/`COMPLETE` state;
- bounded no-material-finding conclusion requires declared scope, methods, source versions/time and listed gaps;
- `NOT_APPLICABLE` is distinguishable from `NOT_ASSESSED`.

### F. Audit versus remediation

Represent finding production separately from mutation authority.

Tests must prove:

```text
finding FAIL != remediation authorized
```

and that explicit remediation authorization is a separate fact. Scanner/tool capability or assessor recommendation must not manufacture mutation authority.

### G. Temporal posture

Represent a historical accepted/completed report plus later applicable advisory/drift/supersession.

Tests must prove:

```text
historical report stays historical
new applicable signal -> current posture changes
```

A non-applicable signal leaves current posture unchanged. Explicit fixture timestamps only.

### H. Security and execution composition

Represent normalized audit status plus D035 security outcome and D033/D034 authorization facts.

Tests must prove at least:

- audit `PASS` cannot create security `PASS` when current security evidence blocks;
- security `PASS` cannot authorize a live assessment method;
- execution authorization cannot manufacture audit `PASS`;
- `INTRUSIVE_AUTHORIZED` method selection still requires explicit execution authorization;
- `ACCEPTED_EXCEPTION` remains scope/expiry-bound and does not authorize execution/remediation.

### I. Staged Core and D040 protocol-authority alignment

Tests must mechanically prove:

- current authoritative `protocol_version_from(governance)` is `1.12.0` during T010;
- current protocol value is obtained from/parses the Core authority rather than compared against a separately authored mutable exact-current helper literal;
- malformed/missing protocol declarations still fail deterministically;
- staged `ASSURANCE.md` exists and declares `Assurance-Audit-Version: 1.0.0` and `Activation-State: STAGED`;
- `ASSURANCE.md` is **not yet** required/routed by active Protocol `1.12.0` semantics;
- focused fixture/test/evaluator contains no hard dependency on named scanner/SDD/agent/review-provider products, shell/OS syntax, network endpoints or model execution.

The executor may retain genuinely historical or compatibility-bound version literals when tests clearly distinguish them from current-version authority.

## Acceptance criteria

ChatGPT accepts T010 only if remote Git evidence proves all of the following:

1. changed executor-owned paths are within authorized non-Markdown scope;
2. no committed Markdown was modified by the executor;
3. fixture families A–I exist with deterministic assertions;
4. scope/authorization cannot silently expand from credentials, reachability or tooling;
5. profile ceiling is deterministic and intrusive testing is never implied;
6. `NOT_ASSESSED`/`INCONCLUSIVE` cannot become `PASS`;
7. evidence provenance is required for confirmed material claims;
8. severity/confidence remain independent;
9. coverage gaps prevent unbounded completeness/security claims;
10. finding/remediation authorization are mechanically separate;
11. temporal invalidation changes current posture without rewriting historical report state;
12. D035 security and D033/D034 execution control cannot grant audit authority they do not own;
13. the duplicated mutable exact-current protocol literal is eliminated as an independent authority without weakening protocol validation;
14. staged `ASSURANCE.md` is tested while active Protocol remains `1.12.0` and routing remains inactive;
15. no external network/model/provider/dependency/runtime drift is introduced;
16. focused and full deterministic verification are green;
17. executor handoff is valid under D029 and `docs/EXECUTOR-HANDOFFS.md`.

Passing tests are necessary evidence, not acceptance authority. ChatGPT reviews the remote contract, handoff, exact base/head identities and complete diff before acceptance.

## Required verification

Run exactly these required gates, plus any narrower diagnostics needed during implementation:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

## Post-T010 activation gate

T010 acceptance does **not** activate D036 in `GOVERNANCE.md`.

After T010 is accepted/integrated/clean, ChatGPT must perform the D040 Phase-B Markdown activation from current green `develop`:

- bump `GOVERNANCE.md` to Protocol `1.13.0`;
- route/load `ASSURANCE.md` where applicable;
- change `ASSURANCE.md` from staged to active;
- update architecture/checkpoint;
- confirm the deterministic suite remains compatible without any exact-current literal synchronization.

If a new executable change is required at that point, stop and persist a new Task Contract; do not accept a red canonical intermediate state.

## Executor completion

Before returning `DONE`, `BLOCKED` or `PARTIAL`, persist `handoffs/T010-executor-handoff.json`, commit and push all authorized task state.

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T010-executor-handoff.json
BRANCH: test/d036-deterministic-assurance-audit-contract
HEAD: <pushed-commit-sha>
```
