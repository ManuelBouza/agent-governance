# Existing-System Assurance Audit Architecture

Status: ACTIVE ARCHITECTURE — CORE ACTIVE  
Normative decision: `docs/decisions/D036-existing-system-assurance-audit-mode.md`  
Protocol migration: `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`  
Active Core module: `governance-core/ASSURANCE.md`

## Purpose

Agent Governance can be used not only to design and implement changes, but also to assess an existing repository, application, infrastructure stack or operational environment and produce an evidence-based assurance report covering implementation quality, applicable best practices and security posture.

The audit capability is intentionally different from asking an LLM to "review this system". The model coordinates and explains; assessment claims must trace to evidence, current authoritative controls and independent verification.

## Core model

```text
existing system
    │
    ▼
scope + authorization
    │
    ▼
applicable quality/security controls
    │
    ▼
evidence collection
    │
    ▼
independent verification
    │
    ▼
findings + coverage gaps
    │
    ▼
assurance report
    │
    ├── remediation roadmap
    └── retest plan
```

Important invariants:

```text
model opinion != evidence
report completeness != proof of no unknown defects
audit finding != permission to remediate
severity != confidence
NOT_ASSESSED != PASS
INCONCLUSIVE != PASS
```

## Active Core integration

D036's focused portable module `ASSURANCE.md` is active at version `1.0.0` and routed by Protocol `1.13.0`.

D040 Phase A prepared deterministic verification while Protocol remained `1.12.0`. Phase B activates the already-tested assurance semantics without reintroducing an executor-owned mutable exact-current protocol-version literal.

The active module defines portable semantics for:

- audit scope contracts;
- assessment-profile ceilings;
- evidence graph/provenance;
- explicit finding states;
- severity/confidence separation;
- coverage accounting and bounded conclusions;
- audit/remediation separation;
- temporal assurance posture;
- composition with D035 security authority and D033/D034 execution control.

It does **not** define a universal scanner, provider, evidence database, platform adapter or production audit runtime.

## D040 activation sequence

```text
Phase A — verification readiness

ASSURANCE.md STAGED
Protocol 1.12 unchanged
        │
        ▼
T010 deterministic assurance semantics
+ single current-version authority
        │
        ▼
T010 accepted / integrated / cleaned

Phase B — Markdown activation

GOVERNANCE.md -> Protocol 1.13.0
ASSURANCE.md -> ACTIVE
source-map/router/readiness -> ASSURANCE
        │
        ▼
OP012 exact-candidate verification
        │
        ▼
full deterministic suite remains green
without exact-current literal synchronization
```

If Phase B reveals a need for additional executable behavior, stop and create a new Task Contract rather than accepting a red canonical intermediate state.

## What can be audited

Depending on scope and evidence availability:

- functional implementation and requirements fidelity;
- architecture/responsibility/coexistence;
- application/software security;
- dependencies and software supply chain;
- infrastructure/system configuration;
- identity, privilege and secrets;
- network/trust-boundary exposure;
- data security and privacy;
- reliability/resilience/recovery;
- observability/detection/incident readiness;
- configuration/deployment/release safety;
- maintainability/testing/engineering practice;
- usability/accessibility where applicable;
- secure-development/process maturity;
- requested control/compliance mappings.

The audit uses `QUALITY.md` as the broad engineering envelope and D035 as the security-authority/freshness layer.

## Assessment profiles

Use the least intrusive technique that can establish the required evidence.

```text
EVIDENCE_REVIEW
    static/offline artifacts only
          │
          ▼
AUTHENTICATED_OBSERVE
    live read-only queries
          │
          ▼
SAFE_ACTIVE
    bounded non-destructive testing
          │
          ▼
INTRUSIVE_AUTHORIZED
    exploit/penetration/high-impact testing
```

Moving downward increases operational risk and authorization requirements.

`INTRUSIVE_AUTHORIZED` is never implied by a generic security-audit request. D033 controls authorization and D034 controls material assessment runbooks/adapters.

## Evidence-first findings

A material finding should be reducible to:

```text
SUBJECT
  +
EXPECTED STATE / CONTROL
  +
OBSERVED STATE
  +
METHOD
  +
EVIDENCE
  +
CURRENT SOURCE / VERSION
  +
STATUS
  +
SEVERITY
  +
CONFIDENCE
  +
REMEDIATION
  +
RETEST
```

The report prose is a human-readable projection of this evidence structure.

## Finding states

```text
PASS
FAIL
PARTIAL
NOT_APPLICABLE
NOT_ASSESSED
INCONCLUSIVE
ACCEPTED_EXCEPTION
```

This prevents missing evidence from being interpreted as success.

## Coverage truth

A useful audit explicitly shows gaps.

Example:

```text
Domain                 Source review  Live state  Active test  Result
Application auth       YES            YES         SAFE         PASS/FAIL
Dependency security    YES            N/A         N/A          PASS/FAIL
Backup restore         PARTIAL        YES         NOT RUN      INCONCLUSIVE
Production pentest     N/A            N/A         NOT AUTH     NOT_ASSESSED
```

The correct conclusion is bounded:

```text
No material finding identified within the declared scope,
methods and source versions, subject to the listed gaps.
```

Not:

```text
The system is secure.
```

## Positive assurance

The report records verified strengths as well as defects.

Examples:

- regression tests preventing known vulnerabilities;
- least privilege confirmed in actual IAM state;
- tested backup/restore evidence;
- rollback mechanisms confirmed;
- current dependency provenance controls;
- effective segmentation;
- mature security requirements/threat modeling;
- validated secure configuration baseline.

Strengths require evidence just like failures.

## Security authority and freshness

Before security conclusions, D035 resolves current sources such as:

```text
project security decisions
      +
vendor advisories/version guidance
      +
current vulnerability intelligence / KEV
      +
versioned standards/baselines
      +
known-bad project regressions
```

The model's memory is not a security source of record.

A report is point-in-time. A later CVE/advisory/baseline update or system drift may invalidate current posture without invalidating the historical report.

## Platform-neutral measurement

The assessment question is semantic; collection is adapter-specific.

```text
"Is administrative access least privileged?"
               │
               ▼
required evidence semantics
               │
     ┌─────────┼─────────┐
     ▼         ▼         ▼
 cloud API   OS tool   cluster/database interface
     │         │         │
     └─────────┴────┬────┘
                    ▼
               observed state
```

This matches D034 terminal neutrality: define what must be measured separately from how a platform-specific adapter collects normalized evidence.

## Audit versus remediation

```text
AUDIT
  ↓
finding + evidence
  ↓
Human/Strategy prioritization
  ├── accept exception
  ├── defer with tracked risk
  └── authorize remediation
              ↓
       D033 envelope
              ↓
       D034 runbook
              ↓
         implementation
              ↓
           RETEST
```

The assessment process does not silently mutate targets to improve its own score.

## Deterministic foundation before adapters

The implementation order remains conservative:

```text
portable Core assurance semantics
      ↓
deterministic fixtures/evaluator + protocol readiness (T010)
      ↓
Protocol 1.13 / ASSURANCE routing
      ↓
representative normalized evidence schemas/adapters
      ↓
optional provider/platform integrations
      ↓
real-system audit workflows under explicit authorization
```

T010 uses synthetic normalized facts only. It proves scope, profile ceilings, evidence/finding states, coverage, temporal posture and control-plane composition without wall-clock time, network access, models or real targets. It also implements D040's single-current-version-authority verification model.

Broad scanner or live-target integration requires a later separately persisted decision/Task Contract and must satisfy D033/D034/D035 plus coexistence/supply-chain constraints.

## Report shape

A comprehensive report normally contains:

1. executive summary;
2. scope/authorization/exclusions;
3. assessment date and security-source freshness;
4. system/architecture boundary;
5. methodology and intrusiveness profiles;
6. coverage matrix and gaps;
7. verified strengths;
8. prioritized findings with evidence;
9. security posture;
10. implementation/engineering quality;
11. privacy/data findings where applicable;
12. process/maturity findings where included;
13. exceptions/residual risk;
14. remediation roadmap;
15. retest plan;
16. sanitized evidence references.

## External assessment references

The methodology is designed to compose, not replace, applicable standards and project-native assurance processes.

Representative sources include:

- NIST SP 800-53A assessment procedures;
- NIST SP 800-115 technical security testing/assessment;
- NIST CSF 2.0;
- NIST SSDF;
- CIS Controls / assessment specifications / Benchmarks;
- OWASP ASVS;
- OWASP Web Security Testing Guide;
- OWASP SAMM;
- CISA KEV and vendor advisories.

No framework is automatically applied to every system, and none is a runtime dependency of portable Core or T010.

## Coherent assurance/execution stack

```text
D032 quality intent
      ↓
D035 security authority
      ↓
D036 assessment / verification
      ↕
D033 execution authorization
      ↓
D034 runbook/adapters
```

Neither audit status, security status nor execution authorization expands authority owned by another plane.
