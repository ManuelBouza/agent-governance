# D036 — Existing-system assurance audit mode

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance is not limited to designing and implementing new changes. The same governance, quality, execution-control and security-verification mechanisms can be applied to a system that already exists in order to determine what is actually implemented, which practices are strong or weak, what security controls are present or missing, which risks are current, and what remediation should be prioritized.

A generic LLM review is not sufficient for this purpose. A probabilistic model can miss uncommon defects, overstate certainty, rely on stale guidance, or infer that a control exists without evidence. A credible audit therefore needs an explicit assessment scope, authoritative current control sources, evidence collection, independent verification, coverage accounting and durable findings.

The audit capability must also distinguish review from active security testing. Reading a repository, querying configuration, scanning a staging service, fuzzing an endpoint and exploiting a vulnerability have materially different operational risks and authorization requirements.

The missing capability is a reusable **Existing-System Assurance Audit Mode** that assesses implementation quality, operational/system configuration, security and applicable best practices using the mechanisms already established by D032–D035.

## Decision

Agent Governance SHALL support an **Existing-System Assurance Audit Mode** for assessing already-built systems, repositories, applications, services, infrastructure and operational environments.

The audit is evidence-first and scope-bounded.

Core invariants:

```text
model opinion != audit evidence

reported completeness = completeness against declared scope/methods
                      != proof that no undiscovered defect exists

successful command/query != control effectiveness

finding severity != finding confidence

audit finding != remediation authorization
```

The AI may coordinate the audit, select applicable assessment methods, correlate evidence, explain findings and propose remediation. It MUST NOT fabricate evidence, silently treat unassessed areas as passing, or use its own confidence as a substitute for verification.

## Relationship to existing decisions

D036 composes existing architecture rather than creating a parallel security system.

- **D032 / QUALITY** defines the cross-cutting engineering quality dimensions to inspect.
- **D033** defines what live/local/remote effects the assessor may perform.
- **D034** defines runbook-first terminal/platform-neutral execution for repeatable/material assessment procedures.
- **D035** defines current security authority, freshness, known-bad regression knowledge and independent verification.

Conceptually:

```text
D032 quality envelope
        +
D035 current security authority
        +
D033 assessment authorization
        +
D034 assessment runbooks/adapters
        ↓
D036 evidence-based existing-system audit
```

## Audit scope contract

Every audit must make the assessed boundary determinable before evidence is collected.

The applicable subset includes:

1. **subject identity** — repository/application/service/system/environment/account/tenant/cluster/database or other concrete subject;
2. **environment class** — development/test/staging/production or project-native equivalent;
3. **asset/resource boundary** — what is in scope and explicitly out of scope;
4. **data boundary** — whether personal, confidential, regulated, production or synthetic data may be observed;
5. **identity/access boundary** — accounts/roles/credentials the assessment is allowed to use;
6. **assessment methods** — source review, artifact analysis, authenticated queries, scanners, active tests, etc.;
7. **intrusiveness ceiling** — maximum permitted assessment profile;
8. **time/freshness boundary** — assessment date/window and required current-source refresh;
9. **evidence retention/redaction rules**;
10. **required standards/baselines/mappings** where the Human/project requires them;
11. **explicit exclusions and unavailable evidence**;
12. **report audience and required depth**.

An audit must not broaden scope merely because credentials, network reachability or tooling expose additional assets.

## Assessment profiles / intrusiveness levels

Use the least intrusive method that can establish the required evidence.

### `EVIDENCE_REVIEW`

Offline/static review only.

Examples:

- source code and repository structure;
- architecture/design documents;
- lockfiles/SBOMs/manifests;
- IaC/configuration files;
- CI/CD definitions;
- test/eval evidence;
- policies/runbooks;
- previously exported/sanitized system state.

No live target access is implied.

### `AUTHENTICATED_OBSERVE`

Read-only inspection of live system state through project/platform-native interfaces.

Examples:

- query versions, enabled features and configuration state;
- enumerate authorized resource inventory;
- inspect IAM assignments/role bindings;
- inspect network policy/state;
- inspect deployment/runtime metadata;
- query security/audit posture without intended mutation.

The access must remain within D033 and should use read-only identities where practical.

### `SAFE_ACTIVE`

Bounded, non-destructive active testing intended not to mutate persistent state or materially affect availability.

Examples may include:

- controlled vulnerability scanning;
- protocol/security-header tests;
- bounded web/API security tests;
- rate-limited negative requests;
- safe configuration probes;
- controlled fuzzing against a suitable test target when its failure mode is acceptable.

`SAFE_ACTIVE` does not authorize exploitation, destructive payloads, persistence, credential attacks, denial-of-service or uncontrolled load.

### `INTRUSIVE_AUTHORIZED`

Penetration/exploitation or other actions that can materially mutate state, cross privilege boundaries, expose sensitive data, affect availability or reproduce a real attack path.

This profile is **never implied** by a generic request to "audit security".

It requires explicit Human authorization under D033, exact targets, technique limits, stop conditions, recovery expectations and appropriate runbooks under D034.

A production intrusive assessment requires an especially narrow envelope and operational coordination.

## Audit is separate from remediation

Finding a defect does not automatically authorize fixing it.

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

The Human may explicitly authorize an assessment-and-remediation engagement, but assessment evidence and remediation mutations remain distinguishable in the audit trail.

A scanner or assessor must not silently change configuration merely to make a finding disappear.

## Audit domains

The audit composes D032 quality dimensions into an existing-system assessment. Applicability is determined by the subject and scope; non-applicable dimensions are explicit rather than silently omitted.

### 1. Functional implementation fidelity

Assess whether implemented behavior, interfaces, invariants and edge cases match current intended requirements where those requirements can be established.

Evidence may include tests, code paths, schemas, API behavior and accepted product/architecture decisions.

### 2. Architecture and ownership/coexistence

Assess boundaries, responsibilities, coupling, trust boundaries, external integrations, native tooling/SDD overlap and duplicated/ambiguous ownership.

Architecture drift between documentation and implemented state is reportable.

### 3. Application/software security

Assess applicable threat surfaces and controls including authentication, authorization, session/state handling, input validation, output encoding, cryptography, secrets, error handling, business logic, multi-tenancy/isolation and abuse cases.

Use D035 current/versioned requirements and verification sources rather than model memory.

For web applications/services, OWASP ASVS and WSTG are possible current verification/testing sources when applicable; they are not universal dependencies.

### 4. Dependency and software supply-chain security

Assess direct/transitive dependencies, lock/provenance state, vulnerable versions, package/source trust, build integrity, CI/CD execution surfaces, artifact provenance and relevant current advisories/KEV exposure.

### 5. Infrastructure and system configuration

Assess actual configuration against applicable vendor guidance, project baselines, CIS Benchmarks/checklists or other current authoritative configuration sources.

Verification should prefer observed resulting state over command/config intent alone.

### 6. Identity, privilege and secrets

Assess identities, roles, privilege boundaries, least privilege, service accounts, credential lifecycle, secret storage/use, MFA/strong-auth assumptions and administrative access paths.

### 7. Network and trust-boundary exposure

Assess exposed services, ingress/egress paths, segmentation, management planes, remote access, encryption in transit, trust relationships and unintended reachability.

### 8. Data security and privacy

Assess data classification, minimization, access boundaries, encryption, storage, retention/deletion, backup copies, logging/telemetry exposure, third-party flows and privacy obligations where material.

Privacy findings remain separate from cybersecurity findings when the risk is privacy-specific.

### 9. Reliability, resilience and recovery

Assess failure handling, retries/idempotency, availability assumptions, capacity-sensitive failure modes, backups, restore testing, disaster/failover mechanisms, recovery objectives and partial-state handling.

### 10. Observability, detection and incident readiness

Assess whether material failures/security events are detectable and diagnosable; evaluate logging/metrics/tracing/audit coverage, alerting, evidence quality, retention and incident/recovery runbooks without requiring excessive sensitive logging.

### 11. Configuration/deployment/release safety

Assess environment separation, declarative configuration where appropriate, change controls, rollout mechanisms, migration safety, rollback/fallback, drift detection and production release evidence.

### 12. Maintainability and engineering practice

Assess modularity, change isolation, testing depth, obsolete/dead patterns, documentation needed for operation, complexity hotspots and recurrence-prevention mechanisms.

### 13. Human-facing quality

Where applicable, assess usability, accessibility and internationalization against project requirements/current external standards such as WCAG for web interfaces.

### 14. Secure-development/process maturity

When the audit scope includes the development organization/process rather than only the deployed system, assess requirements, threat modeling, secure build/deployment, defect management, verification, incident management and operational practices.

OWASP SAMM is an applicable technology/process-agnostic maturity reference when requested or useful; the audit must not confuse process maturity with proof that a specific product has no vulnerability.

### 15. Compliance/control mappings

When explicitly required, map observed evidence/findings to the selected regulatory/control framework.

Compliance mapping is evidence organization; it must not be presented as legal certification unless the engagement and assessor authority actually provide that status.

## Security assessment source model

D035 applies in full.

Before security conclusions are drawn, the audit resolves the applicable current source set, including the relevant subset of:

- project-approved security decisions/exceptions;
- vendor guidance/advisories for exact versions;
- CISA KEV/current vulnerability intelligence where applicable;
- NIST/CIS/OWASP/project-native security standards and baselines;
- known-bad historical project patterns/regression rules.

A stale model recollection cannot override a current authoritative advisory or baseline.

## Assessment methods and verifier composition

No universal scanner or single technique can prove complete security.

The audit composes the minimum set of methods necessary for the declared scope/risk, such as:

- document/architecture review;
- source code review;
- threat modeling;
- SAST/semantic/code-query analysis;
- secret scanning;
- dependency/SCA/advisory matching;
- SBOM/provenance analysis;
- IaC/configuration analysis;
- authenticated runtime/configuration state queries;
- benchmark/checklist measurements;
- unit/integration/e2e/negative/security regression tests;
- fuzzing/property tests where material;
- DAST/web/API tests where appropriate;
- network/service exposure assessment;
- vulnerability scanning;
- manual validation of high-impact findings;
- controlled penetration testing only when explicitly authorized;
- process/runbook/evidence review.

NIST SP 800-115 is a reference for planning/conducting technical security tests and examinations, analyzing findings and developing mitigation strategies. It is not a mandate to run every technique.

## Evidence hierarchy

Findings should rely on the strongest available evidence.

Conceptual evidence strength, subject to context:

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

A model-only hypothesis may create an investigation lead, but it is not by itself a confirmed high-impact security finding.

For destructive/high-impact findings, reproduce or independently corroborate when safe and authorized before presenting the issue as confirmed.

## Evidence graph

The canonical conceptual unit is not a prose paragraph but a traceable claim.

Each material assessment claim/finding should make the applicable subset determinable:

- subject/resource identity;
- domain/control/question assessed;
- expected state/requirement;
- observed state;
- assessment method;
- evidence pointer/artifact/query/result;
- authoritative source and version/freshness where applicable;
- result/status;
- severity/impact;
- confidence/evidence strength;
- exploitability/current threat context when material;
- affected scope;
- remediation recommendation;
- retest/verification method;
- exception/residual-risk reference if applicable.

The model may synthesize this graph into prose, but prose must not discard evidence provenance.

## Finding statuses

Use explicit assessment states rather than binary pass/fail only.

### `PASS`

Sufficient evidence demonstrates the assessed requirement/control/outcome for the declared scope and method.

### `FAIL`

Evidence demonstrates that the assessed requirement/control is absent, incorrectly implemented or ineffective.

### `PARTIAL`

The control/requirement is implemented incompletely or only over part of the required subject scope.

### `NOT_APPLICABLE`

The requirement genuinely does not apply to the assessed subject/context, with rationale when not obvious.

### `NOT_ASSESSED`

The area is inside a broader possible domain but was explicitly outside the engagement scope or method set.

### `INCONCLUSIVE`

The area was attempted but available evidence is insufficient or conflicting.

### `ACCEPTED_EXCEPTION`

A known nonconformance/risk is covered by a current Human-approved exception under D035 with scope, compensating controls and expiry/review conditions.

Expired/stale exceptions revert to unresolved findings.

## Severity and confidence are independent

A finding may be high severity but low confidence, or low severity but high confidence.

Do not collapse both dimensions into a single opaque score.

Severity/risk considers the material subset of:

- impact on confidentiality/integrity/availability/privacy/safety/business outcome;
- exploitability/exposure;
- privilege/preconditions;
- affected population/assets/data;
- current threat intelligence such as active exploitation;
- compensating controls;
- recovery difficulty.

Confidence considers the quality/directness/reproducibility of evidence.

A high-severity low-confidence finding should trigger targeted verification, not be silently downgraded or presented as confirmed fact.

## Coverage accounting

A credible audit reports what it did **not** prove.

Maintain a coverage view across relevant domains/resources/methods with states such as:

- assessed/pass;
- assessed/fail;
- assessed/partial;
- not applicable;
- not assessed;
- inconclusive;
- blocked by access/evidence constraint.

The report SHALL NOT use wording equivalent to "the system is secure" or "no vulnerabilities exist" merely because no finding was produced.

Preferred claim:

```text
No material finding was identified within <declared scope>,
using <declared methods>, against <declared source versions>,
as of <assessment time>, subject to the listed coverage gaps.
```

## Audit report structure

A comprehensive report should include the applicable subset of:

1. **Executive summary** — material posture, strongest risks and strengths at the audience's register;
2. **Scope and authorization** — systems/environments/data/methods and explicit exclusions;
3. **Assessment timestamp/freshness** — when current advisories/baselines were resolved;
4. **System/architecture summary** — assessed components, boundaries and material data/trust flows;
5. **Methodology and assessment profiles** — what techniques were actually used;
6. **Coverage matrix/gaps**;
7. **Positive controls/strengths** — verified good practices, not only defects;
8. **Findings** — prioritized, evidence-backed and source-mapped;
9. **Security posture** — vulnerabilities, configuration, identity, network, supply chain and security-development findings as applicable;
10. **Engineering/implementation quality** — correctness, architecture, maintainability, testability, reliability, operability, release safety, etc.;
11. **Privacy/data findings** when applicable;
12. **Maturity/process findings** when included;
13. **Exceptions/residual risk**;
14. **Remediation roadmap** — ordered by risk/dependency/effort where useful;
15. **Retest plan / acceptance verification**;
16. **Evidence appendix/references** with secrets and unnecessary sensitive data redacted.

## Strengths and good practices

The audit should record verified strengths, not merely list failures.

A strength must still be evidence-backed. Examples include:

- deterministic security regression coverage;
- least-privileged identities confirmed in runtime state;
- strong deployment rollback evidence;
- current dependency provenance controls;
- tested restore procedures;
- effective segmentation;
- clear ownership/runbooks;
- current and enforceable secure configuration baselines.

Do not inflate report quality by praising ordinary controls without evidence or relevance.

## Remediation roadmap

Recommendations must be actionable and distinguish:

- immediate containment/urgent remediation;
- structural/root-cause remediation;
- defense-in-depth improvements;
- observability/detection gaps;
- process/control improvements;
- future hardening that is useful but non-blocking.

Where possible, convert fixed vulnerabilities or insecure configurations into D035 known-bad regression checks so the issue cannot be reintroduced probabilistically by a later AI or Human implementation.

The remediation roadmap is not authorization to execute those changes.

## Retest / closure semantics

A finding closes only when the defined verification method demonstrates the required post-remediation state.

```text
finding
  ↓
remediation
  ↓
retest against original + current controls
  ↓
PASS / PARTIAL / FAIL / ACCEPTED_EXCEPTION
```

A changed implementation may require updated threat/control assessment rather than merely replaying the original exact check.

## Current-threat invalidation

An audit report is a point-in-time assurance artifact.

New advisories, KEV additions, benchmark updates, asset/configuration changes or discovered scope errors can make a prior conclusion stale without changing the report's historical correctness.

The report should state its assessment timestamp and source versions/freshness.

Where ongoing monitoring is configured, material current-threat/control changes should create a new reassessment/remediation trigger rather than rewriting historical evidence.

## Privacy and sensitive audit evidence

Audits frequently encounter sensitive information.

Default rules:

- collect the minimum evidence needed for the claim;
- prefer hashes/identifiers/redacted values over secret material;
- never persist credentials/private keys/tokens in the report;
- do not persist unnecessary production records/PII merely to prove access;
- protect raw scanner/runtime evidence according to project policy;
- distinguish report-safe evidence from restricted raw evidence;
- do not persist private model chain-of-thought.

## Active-testing safety

Security testing itself is an execution effect governed by D033.

Before `SAFE_ACTIVE` or `INTRUSIVE_AUTHORIZED` testing, establish the applicable subset of:

- exact target and ownership/authorization;
- environment class;
- allowed test techniques;
- request/load/rate limits;
- prohibited payloads/effects;
- test accounts/data;
- monitoring/contact/escalation path;
- stop conditions;
- backup/recovery expectation;
- evidence handling;
- testing window where relevant.

Unexpected destructive behavior, target mismatch or scope expansion stops testing.

## Platform and tooling neutrality

The assessment methodology is platform-neutral.

The same assessment claim may be measured through different adapters:

```text
assessment question
      ↓
required evidence / measurement semantics
      ↓
platform-specific verifier adapter
      ↓
observed state
```

Possible adapters include repository analyzers, compiler/toolchain tests, PowerShell, POSIX-style shells, APIs, cloud CLIs, database interfaces, orchestration systems, CI/CD APIs, scanners and platform-native audit systems.

Different measurement mechanisms are acceptable if they preserve equivalent evidence semantics.

CIS Controls Assessment Specification is a useful external example of this separation: define what should be measured in a platform-agnostic way while leaving how a tool obtains the measurements to platform-specific implementations.

## Framework/reference mapping posture

External frameworks are selected by applicability and user/project need, not all applied indiscriminately.

Useful reference families include:

- NIST CSF 2.0 for cybersecurity risk-management lifecycle/coverage;
- NIST SP 800-53 / 800-53A for control and assessment procedure structures;
- NIST SP 800-115 for technical security assessment planning/testing;
- NIST SSDF for secure software development practice;
- NIST configuration/checklist/SCAP/OSCAL resources where applicable;
- CIS Controls / Controls Assessment Specification / Benchmarks;
- OWASP ASVS for application verification requirements;
- OWASP WSTG for web/application testing methods;
- OWASP SAMM for software assurance maturity assessment;
- CISA KEV and vendor advisories for current exploited/product vulnerability context;
- project/domain/regulatory requirements that already control the system.

Framework mappings must name versions where practical and must not imply certification that Agent Governance is not authorized to issue.

## Primary Solution Diagram

Dominant question: how an existing system is assessed across evidence sources and methods while preserving authorization and coverage truth.

```text
Existing system / repository / environment
                 │
                 ▼
        Audit Scope & Authorization
      systems · data · accounts · methods
                 │
                 ▼
       Assessment Profile / Coverage
   ┌─────────────┼──────────────┬─────────────┐
   ▼             ▼              ▼             ▼
implementation  security      runtime       process/
architecture    controls      config/state  maturity
   │             │              │             │
   └─────────────┴──────┬───────┴─────────────┘
                        ▼
             Evidence Collection Plane
       artifacts · read-only queries · scanners
       tests · current advisories · interviews
                        │
                        ▼
               Independent Verifiers
        control checks · SAST/SCA · config
        checks · tests · threat analysis
                        │
                        ▼
                   Evidence Graph
      expected state ↔ observed state ↔ source
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
           Findings           Coverage gaps
      PASS/FAIL/PARTIAL       NOT_ASSESSED/
      + severity/confidence   INCONCLUSIVE
              │                   │
              └─────────┬─────────┘
                        ▼
                Assurance Audit Report
      strengths · defects · security · practices
      risk · remediation · retest · residual gaps
```

## Research basis

Primary/current references reviewed for this decision include:

- NIST SP 800-53A Rev. 5, including Release 5.2.0 assessment procedure updates: https://csrc.nist.gov/pubs/sp/800/53/a/r5/final
- NIST SP 800-53 Rev. 5 / current release resources: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- NIST SP 800-115 Technical Guide to Information Security Testing and Assessment: https://csrc.nist.gov/pubs/sp/800/115/final
- NIST Cybersecurity Framework 2.0: https://www.nist.gov/cyberframework
- NIST SSDF project / SP 800-218: https://csrc.nist.gov/projects/ssdf
- CIS Controls v8.1: https://www.cisecurity.org/controls/v8-1
- CIS Controls Assessment Specification: https://www.cisecurity.org/controls/cis-controls-assessment-specification
- OWASP ASVS: https://owasp.org/www-project-application-security-verification-standard/
- OWASP Web Security Testing Guide: https://owasp.org/www-project-web-security-testing-guide/
- OWASP SAMM: https://owaspsamm.org/
- CISA Known Exploited Vulnerabilities Catalog: https://www.cisa.gov/known-exploited-vulnerabilities-catalog

## Consequences

- Agent Governance can be used for greenfield development, change implementation **or** evidence-based assessment of existing systems.
- Audit/reporting becomes a first-class lifecycle mode, not an informal side effect of code review.
- The product can report both implementation quality and security posture using the same D032 quality envelope and D035 authority model.
- Audit completeness is always tied to declared scope, evidence and methods; unassessed areas remain explicit.
- Active/intrusive security testing is never implied and remains controlled by D033/D034.
- Findings are evidence-backed and preserve severity/confidence separately.
- Remediation is a separate authorization step and can create durable regression controls.
- Audit reports become point-in-time assurance artifacts subject to freshness/invalidation by later vulnerabilities or system drift.
- A future Core integration increment after T004 should incorporate D033–D036 coherently rather than implementing each decision as an isolated subsystem.
