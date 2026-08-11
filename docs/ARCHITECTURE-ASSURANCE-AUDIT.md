# Existing-System Assurance Audit Architecture

Status: ARCHITECTURE OVERVIEW  
Normative decision: `docs/decisions/D036-existing-system-assurance-audit-mode.md`

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
```

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

This matches D034 terminal neutrality and the CIS Controls Assessment Specification pattern of defining what to measure separately from how a platform-specific tool measures it.

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
- CIS Controls / Controls Assessment Specification / Benchmarks;
- OWASP ASVS;
- OWASP Web Security Testing Guide;
- OWASP SAMM;
- CISA KEV and vendor advisories.

No framework is automatically applied to every system.

## Planned Core integration

D036 is accepted architecture only while T004 is still running.

The post-T004 Core-integration frontier should now treat D033–D036 as a coherent assurance/execution stack:

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

Future implementation should establish deterministic audit-state semantics, evidence/finding schemas, assessment profiles, coverage accounting and representative platform-neutral verifier fixtures before adding broad real-system scanner adapters.
