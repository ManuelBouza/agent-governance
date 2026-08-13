# Assurance Audit

Assurance-Audit-Version: 1.0.0  
Activation-State: ACTIVE

## Activation boundary

This module is an active routed Core module under Protocol `1.13.0`.

Activation does not itself authorize an audit, live-system access, scanner/provider use or remediation. Scope, assessment profile and execution authority remain explicit and bounded by this module plus `SECURITY.md` and `EXECUTION-CONTROL.md` where applicable.

## Purpose

Define the portable evidence-first contract for assessing an already-built repository, application, service, infrastructure stack or operational environment without turning model opinion, tool success or missing evidence into assurance.

This module operationalizes D036 and composes the quality envelope, current security authority and execution-control planes. It defines audit semantics, not a universal scanner, provider, runtime or remediation engine.

## Core invariants

```text
model opinion != audit evidence
reported completeness != proof that no undiscovered defect exists
successful command/query != control effectiveness
finding severity != finding confidence
audit finding != remediation authorization
NOT_ASSESSED != PASS
INCONCLUSIVE != PASS
```

An audit claim is valid only inside its declared subject, scope, methods, evidence and assessment time. Later system drift or new authoritative security information may invalidate current posture without rewriting the historical report.

## Scope contract

Before evidence collection, make the applicable subset explicit and determinable:

- subject identity;
- environment class;
- in-scope and out-of-scope assets/resources;
- data boundary and sensitivity;
- identity/access boundary;
- authorized assessment methods;
- maximum intrusiveness profile;
- assessment time/window and freshness requirements;
- evidence retention/redaction rules;
- required standards/baselines/mappings;
- unavailable evidence and explicit exclusions;
- report audience/depth.

Observed reachability, available credentials or installed tooling MUST NOT broaden audit scope.

## Assessment profiles

Profiles are ordered by operational intrusiveness:

```text
EVIDENCE_REVIEW
      <
AUTHENTICATED_OBSERVE
      <
SAFE_ACTIVE
      <
INTRUSIVE_AUTHORIZED
```

Use the least intrusive profile sufficient for the required evidence.

- `EVIDENCE_REVIEW` — static/offline artifacts; no live target access implied.
- `AUTHENTICATED_OBSERVE` — read-only live observation through authorized project/platform interfaces.
- `SAFE_ACTIVE` — bounded non-destructive active testing without intended persistent mutation or material availability impact.
- `INTRUSIVE_AUTHORIZED` — exploitation, privilege-boundary crossing or other materially risky testing; requires explicit Human authorization, exact targets/technique limits, stop conditions and recovery expectations under execution-control/runbook rules.

A generic audit request never implies `INTRUSIVE_AUTHORIZED`.

## Audit domains

Select only domains applicable to the subject and declared scope. Material candidates include:

- functional implementation fidelity;
- architecture, ownership and coexistence;
- application/software security;
- dependency and software supply chain;
- infrastructure/system configuration;
- identity, privilege and secrets;
- network and trust-boundary exposure;
- data security and privacy;
- reliability, resilience and recovery;
- observability, detection and incident readiness;
- configuration/deployment/release safety;
- maintainability, testing and engineering practice;
- human-facing quality where applicable;
- secure-development/process maturity;
- explicitly requested compliance/control mappings.

Non-applicable domains are explicit rather than silently omitted.

## Evidence graph

A material claim or finding must make the applicable subset determinable:

- subject/resource identity;
- domain/control/question;
- expected state/requirement;
- observed state;
- assessment method/profile;
- evidence pointer/artifact/query/result;
- authoritative source/version/freshness when applicable;
- result/status;
- severity/impact;
- confidence/evidence strength;
- affected scope;
- remediation recommendation;
- retest/verification method;
- exception/residual-risk reference when applicable.

Prose is a projection of this evidence graph and MUST NOT discard provenance.

## Evidence strength

Prefer the strongest applicable evidence, context permitting:

```text
verified observed state / deterministic test
        ↓
structured authoritative tool output
        ↓
versioned artifact/config/source evidence
        ↓
manual technical observation/reproduction
        ↓
reasoned inference from multiple facts
        ↓
model-only hypothesis
```

A model-only hypothesis is an investigation lead, not a confirmed material finding.

## Finding states

Use explicit states:

- `PASS` — sufficient evidence establishes the assessed requirement for the declared scope/method.
- `FAIL` — evidence establishes absence, incorrect implementation or ineffectiveness.
- `PARTIAL` — requirement/control is implemented only partially or over part of required scope.
- `NOT_APPLICABLE` — requirement genuinely does not apply.
- `NOT_ASSESSED` — intentionally outside the engagement scope/method set.
- `INCONCLUSIVE` — attempted, but evidence is insufficient or conflicting.
- `ACCEPTED_EXCEPTION` — current exact-scope Human-approved exception with required compensating evidence and review/expiry conditions.

Missing evidence MUST NOT collapse to `PASS`.

Expired, stale or out-of-scope exceptions do not remain `ACCEPTED_EXCEPTION`.

## Severity and confidence

Severity and confidence are independent dimensions.

Severity considers applicable impact, exploitability/exposure, privilege/preconditions, affected assets/data/population, current threat context, compensating controls and recovery difficulty.

Confidence considers evidence directness, quality, corroboration and reproducibility.

High-severity low-confidence findings trigger targeted verification; they are neither silently downgraded nor presented as confirmed fact.

## Coverage accounting

Maintain a coverage view across declared domains/resources/methods. Each covered cell is classified by explicit evidence state, including pass/fail/partial/not applicable/not assessed/inconclusive and access/evidence-blocked conditions where needed.

Coverage truth obeys:

```text
unassessed area != passing area
absence of finding != evidence of absence
```

A bounded no-finding conclusion should state scope, methods, source versions, assessment time and coverage gaps. Do not claim that a system is secure or free of vulnerabilities merely because no finding was produced.

## Security composition

When a claim is security-material, `SECURITY.md` applies in full:

- model output is not security authority;
- applicable current/versioned controls and source freshness must be resolved;
- active applicable known-bad state blocks security acceptance;
- required independent evidence cannot be replaced by reviewer/model assertion;
- Human security exceptions remain exact-scope, evidence-supported and expiry-sensitive;
- historical audit/task acceptance does not establish permanent current security posture.

Security finding status and current security posture are related but not interchangeable.

## Execution composition

Assessment procedure and authorization remain separate.

`EXECUTION-CONTROL.md` governs any material local/remote/system effect. Runbooks define repeatable procedure but do not authorize an invocation.

```text
audit method selected != execution authorized
execution authorized != audit finding PASS
security PASS != execution authorization
```

Read-only/live and active profiles must remain within the applicable Execution Capability Envelope. Child tools/adapters cannot expand parent authority.

## Audit versus remediation

Default lifecycle:

```text
ASSESS
  ↓
REPORT FINDING
  ↓
PRIORITIZE / ACCEPT RISK / EXCEPTION
  ↓
separate authorized remediation work
  ↓
RETEST / VERIFY
```

An assessor/scanner MUST NOT silently mutate the subject to make its own finding disappear. Combined assessment-and-remediation engagements still preserve distinct evidence and mutation records.

## Temporal posture

An assurance report is point-in-time.

```text
historical report remains historical
new advisory / vulnerability / drift / supersession
        -> may invalidate current posture
        -> does not rewrite historical evidence
```

Current conclusions must expose the assessment timestamp and applicable freshness boundary.

## Report minimum

A material assurance report should make the applicable subset visible:

- executive summary;
- scope, authorization and exclusions;
- assessment timestamp/source freshness;
- system/architecture boundary;
- methods/profiles actually used;
- coverage matrix/gaps;
- evidence-backed strengths;
- prioritized findings with severity and confidence separated;
- security/engineering/privacy/process sections as applicable;
- exceptions/residual risk;
- remediation roadmap;
- retest plan;
- sanitized evidence references.

The report records verified strengths as well as defects; strengths require evidence.

## Provider neutrality

Core audit semantics are independent of any scanner, cloud, SDD, review provider, operating system, shell, agent product or model provider.

Platform/provider adapters may collect normalized evidence. They do not redefine scope, finding states, assurance authority, security authority or execution authorization.
