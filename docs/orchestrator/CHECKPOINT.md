# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O023  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — is `READY` on `develop` and has been launched to the Agente de IA Ejecutor. No final T004 executor handoff has been received yet.

T004 Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Expected T004 executor branch:

`eval/d032-agent-capability`

Expected T004 handoff:

`handoffs/T004-executor-handoff.json`

T004 remains governed by its existing contract. D033–D036 architecture work MUST NOT retroactively broaden or alter its running execution semantics.

## Accepted Architecture Frontier

Four complementary decisions are accepted architecture and not yet integrated into Governance Core/protocol:

- `docs/decisions/D033-execution-access-control-plane.md` — authorization by actor/target/effect/privilege/credential/resource scope;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — reusable runbook procedures and terminal/platform-neutral execution adapters;
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md` — current security authority, freshness, known-bad anti-regression and independent verification;
- `docs/decisions/D036-existing-system-assurance-audit-mode.md` — evidence-based assessment/audit of existing systems covering engineering quality, best practices, security, configuration and process maturity where applicable.

Consolidated overviews:

- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`;
- `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`.

## Combined Assurance / Execution Model

```text
D032 quality intent and engineering envelope
        ↓
D035 current/versioned security authority
        ↓
D036 assessment / independent verification
        ↕
D033 execution authorization
        ↓
D034 runbook + terminal-neutral adapter
        ↓
local/remote implementation or assessment effect
        ↓
observed evidence / retest / posture
```

Core invariants across the four decisions:

```text
transport or credential possession != execution authority
procedure semantics != terminal syntax
approved runbook != approved invocation
model output != security authority
security acceptance = applicable current controls + independent evidence
past task acceptance != permanent security posture
model opinion != audit evidence
reported audit completeness != proof of no undiscovered defect
finding severity != finding confidence
audit finding != remediation authorization
```

## D033 — Execution Authorization

Execution Capability Envelopes bind the applicable subset of:

- actor/role;
- exact target/environment/account/resource;
- effect classes;
- resource scope;
- privilege ceiling;
- credential source/use;
- network destinations/path;
- task/time/operation lifetime;
- rollback/recovery expectation;
- approval mode;
- audit/evidence requirement.

Approval outcomes:

- `ALLOW_TASK`;
- `ALLOW_EXPLICIT`;
- `REQUIRE_HUMAN`;
- `DENY`.

Child/nested execution cannot expand authority.

## D034 — Runbook-First Terminal-Neutral Procedure

Runbooks are preferred durable procedures for repeatable/material operational work.

A runbook describes the applicable subset of:

- purpose/outcome;
- applicability/exclusions;
- capability/target/privilege class;
- non-secret inputs;
- preconditions;
- ordered semantic steps;
- checkpoints/Human gates;
- postconditions;
- rollback/recovery;
- evidence requirements.

Reuse adequate project-native runbooks/workflows before creating Governance-owned procedures.

Terminal, shell, CLI, API, SDK, remote transport, CI/CD and orchestration products are replaceable execution adapters, not Governance authority.

## D035 — Security Authority, Freshness and Independent Verification

Security-sensitive work follows:

```text
GROUND BEFORE GENERATION
  resolve current applicable security controls
        ↓
AI implementation/configuration proposal
        ↓
VERIFY AFTER GENERATION
  independent technical/deterministic evidence
        ↓
PASS / BLOCK / HUMAN_EXCEPTION
        ↓
INVALIDATE AFTER DEPLOYMENT
  new advisory/KEV/baseline/system drift can revoke current posture
```

Security source classes include:

1. project-authoritative security decisions/exceptions;
2. exact product/vendor current security guidance/advisories;
3. current vulnerability/threat intelligence including applicable CISA KEV;
4. versioned verification/security standards/baselines;
5. model/internal knowledge only as non-authoritative discovery/implementation assistance.

Confirmed vulnerabilities/obsolete insecure patterns should become known-bad regression controls where practical so a later probabilistic model cannot silently reintroduce them.

## D036 — Existing-System Assurance Audit Mode

The Human Owner requires Agent Governance to support auditing/evaluating an already-built system, not only creating new implementations.

D036 defines an evidence-first, scope-bounded audit mode that can assess the applicable subset of:

- functional implementation fidelity;
- architecture/responsibility/coexistence;
- application/software security;
- dependency/software-supply-chain posture;
- infrastructure/system configuration;
- identity/privilege/secrets;
- network/trust-boundary exposure;
- data security/privacy;
- reliability/resilience/recovery;
- observability/detection/incident readiness;
- deployment/configuration/release safety;
- maintainability/testing/engineering practice;
- usability/accessibility where applicable;
- secure-development/process maturity;
- requested compliance/control mappings.

The audit uses D032 `QUALITY.md` for the broad engineering envelope and D035 for current security authority/freshness.

## D036 Assessment Profiles

Use the least intrusive method that can establish required evidence:

### `EVIDENCE_REVIEW`

Static/offline artifacts only: source, architecture, dependencies, IaC/configuration, CI/CD, tests, runbooks and previously exported state.

### `AUTHENTICATED_OBSERVE`

Live read-only queries of versions, configuration, IAM, network/resource/deployment/runtime/security state through authorized project/platform-native interfaces.

### `SAFE_ACTIVE`

Bounded non-destructive active tests such as safe vulnerability/security scans, protocol/header/API tests, controlled negative requests or suitable bounded fuzzing.

Does not imply exploitation, destructive effects, persistence, credential attacks, denial-of-service or uncontrolled load.

### `INTRUSIVE_AUTHORIZED`

Penetration/exploitation/high-impact testing that may mutate state, cross privilege boundaries, expose sensitive data or affect availability.

Never implied by a generic request to audit security. Requires explicit Human authorization under D033, exact targets/technique limits/stop conditions and appropriate D034 runbooks.

## D036 Evidence / Finding Model

A material finding/claim should preserve the applicable subset of:

- subject/resource identity;
- assessed domain/control/question;
- expected state/requirement;
- observed state;
- assessment method;
- evidence pointer/result;
- authoritative source/version/freshness;
- finding status;
- severity/impact;
- confidence/evidence strength;
- exploitability/current threat context when material;
- affected scope;
- remediation recommendation;
- retest method;
- exception/residual-risk reference.

Finding states:

- `PASS`;
- `FAIL`;
- `PARTIAL`;
- `NOT_APPLICABLE`;
- `NOT_ASSESSED`;
- `INCONCLUSIVE`;
- `ACCEPTED_EXCEPTION`.

Missing/unavailable evidence does not become `PASS`.

Severity and confidence remain independent.

## D036 Coverage Truth

Every comprehensive audit exposes gaps.

Coverage accounts for relevant domain/resource/method combinations and marks assessed/pass/fail/partial, not applicable, not assessed, inconclusive or blocked-by-access/evidence.

Preferred bounded conclusion:

```text
No material finding was identified within the declared scope,
using the declared methods and security-source versions,
as of the assessment time, subject to the listed coverage gaps.
```

Do not claim the system has no undiscovered vulnerabilities.

## D036 Audit Report Shape

A comprehensive report should include the applicable subset of:

1. executive summary;
2. scope/authorization/exclusions;
3. assessment timestamp/source freshness;
4. system/architecture summary;
5. methodology/intrusiveness profiles;
6. coverage matrix/gaps;
7. verified strengths/good practices;
8. prioritized evidence-backed findings;
9. security posture;
10. engineering/implementation quality;
11. privacy/data findings;
12. process/maturity findings where included;
13. exceptions/residual risk;
14. remediation roadmap;
15. retest plan;
16. sanitized evidence references.

Verified strengths are recorded as evidence-backed assurance, not generic praise.

## Audit Versus Remediation

Finding a defect does not authorize changing it.

```text
ASSESS
  ↓
REPORT FINDING
  ↓
PRIORITIZE / EXCEPTION / AUTHORIZE REMEDIATION
  ↓
D033 envelope
  ↓
D034 runbook
  ↓
IMPLEMENT
  ↓
RETEST via D035/D036
```

A combined audit-and-remediation engagement may be explicitly authorized, but assessment evidence and mutation authorization remain distinguishable.

## Assessment Reference Posture

External frameworks are selected by applicability rather than all applied universally.

Current useful reference families include:

- NIST CSF 2.0;
- NIST SP 800-53 / SP 800-53A;
- NIST SP 800-115;
- NIST SSDF;
- NIST security configuration/SCAP/OSCAL resources;
- CIS Controls / Controls Assessment Specification / Benchmarks;
- OWASP ASVS;
- OWASP Web Security Testing Guide;
- OWASP SAMM;
- CISA KEV and vendor advisories;
- project/domain/regulatory controls already governing the system.

Framework mappings do not imply certification Agent Governance is not authorized to issue.

## T004 State

T004 remains the current executable frontier and is unchanged by D033–D036.

T004 semantic grading remains `PENDING_CHATGPT` until final executor handoff/results/transcripts are remotely reviewed.

## Planned Core-Integration Frontier

After T004 PD5, the next architecture planning must treat D033–D036 as a coherent stack, but may decompose implementation into multiple Task Contracts after a fresh D032 diagram/quality review.

The first deterministic Core layer should cover the applicable subset of:

- execution authorization outcomes and envelope semantics;
- runbook reference/binding/preflight/Human-gate semantics;
- terminal-neutral execution adapter contract;
- security source/control/freshness/known-bad semantics;
- independent security-verifier evidence;
- audit assessment profiles;
- finding/evidence/coverage states;
- severity/confidence separation;
- audit/remediation separation;
- deterministic synthetic cases where a common-but-insecure model proposal is blocked by a current control/verifier;
- representative platform-neutral measurement/execution adapter fixtures.

Broad real-system scanner/provider adapters should follow only after the semantic Core is mechanically stable.

## Active Remote Artifacts

- T004 Task Contract: `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
- D033: `docs/decisions/D033-execution-access-control-plane.md`;
- D034: `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`;
- D035: `docs/decisions/D035-security-authority-freshness-and-independent-verification.md`;
- D036: `docs/decisions/D036-existing-system-assurance-audit-mode.md`;
- execution overview: `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- security overview: `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`;
- audit overview: `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`.

## Open Questions or Blockers

No known D033–D036 architecture blocker remains.

T004 still requires executor return and PD5.

The source product remains not stable/release-ready. D033–D036 Core integration, broader security/behavioral evals, property/state-machine coverage, Skill gates and release gates remain incomplete.

## Next Action

1. review/integrate the D036 Markdown branch if limited to D036 + audit overview + this checkpoint;
2. do not alter T004;
3. when T004 returns, perform remote PD5 over harness/results/transcripts;
4. after T004 is resolved, design the D033–D036 Core-integration frontier graphically before implementation;
5. prefer deterministic independent verifiers for mechanically checkable audit/security claims;
6. keep intrusive assessment techniques explicitly Human-authorized and target-bounded.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T004 is active/returned, load `docs/tasks/T004-d032-agent-facing-capability-eval.md` and handoff/results as needed;
2. for execution/security/audit planning, load only the relevant subset of D033–D036;
3. load consolidated architecture overviews only when useful;
4. load D032/`QUALITY.md` for graphical/quality readiness or comprehensive audit-domain interpretation.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not retroactively broaden/rewrite T004 because D033–D036 were accepted while it was running.
- Do not treat model output/self-review as security or audit authority.
- Do not report unassessed/missing evidence as passing.
- Do not claim exhaustive security from a bounded audit.
- Do not conflate finding severity with confidence.
- Do not perform intrusive security testing from a generic audit request.
- Do not treat an audit finding as authorization to remediate.
- Do not treat past task/audit acceptance as permanent security posture.
- Do not let stale/unknown/conflicting current security sources silently pass high-impact security conclusions.
- Do not let a model invent a security exception.
- Do not make one shell/OS/scanner/framework/provider a universal Core dependency.
- Do not duplicate adequate project-native security/runbook/audit tooling.
- Do not modify Core/protocol until a separate integrated Task Contract aligns semantics, code and deterministic verification.
- Do not declare the source product stable/release-ready from D033–D036 or T004 alone.
