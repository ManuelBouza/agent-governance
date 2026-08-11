# Security Authority and Verification Architecture

Status: ARCHITECTURE OVERVIEW  
Normative decision: `docs/decisions/D035-security-authority-freshness-and-independent-verification.md`

## Purpose

Agent Governance uses probabilistic AI to design and implement software and system configuration. Security cannot depend on the probability that the model recalls the newest secure pattern.

The architecture therefore separates:

```text
security knowledge authority
          ≠
AI implementation proposal
          ≠
security verification authority
```

The model may be excellent at implementation while still being wrong about a recently changed security requirement. The system is designed so that this error becomes detectable and blocking.

## Three-stage safety model

```text
1. GROUND BEFORE GENERATION
   current/versioned security controls constrain the implementation

2. VERIFY AFTER GENERATION
   independent deterministic/technical evidence proves the controls

3. INVALIDATE AFTER DEPLOYMENT
   new advisories/vulnerabilities/drift can revoke current posture
```

Grounding lowers the probability of an insecure proposal. Verification determines acceptance. Continuous invalidation keeps acceptance from becoming stale.

## Authority model

Applicable security facts are resolved from current authoritative sources, not model memory alone.

```text
project security decisions / threat model / exceptions
                       +
current vendor version-specific guidance/advisories
                       +
current vulnerability/threat intelligence
                       +
versioned verification/configuration standards
                       ↓
              Security Source Resolver
                       ↓
             Versioned Security Control Set
```

Model knowledge remains useful for discovery, mapping and implementation ideas but is non-authoritative when a current source can establish the fact.

## Versioned Security Control Set

Each material control should be able to answer:

```text
WHAT       security property must hold?
WHERE      which component/target/version?
SOURCE     who/what establishes the requirement?
VERSION    which exact source revision/baseline?
BAD STATE  what obsolete/vulnerable state is forbidden?
VERIFY     how is compliance independently proved?
FRESHNESS  when must this source/check be revalidated?
EXCEPTION  is a bounded Human exception active?
REGRESSION what durable rule/test prevents recurrence?
```

The eventual serialized form may be project-native, JSON/YAML or compatible with established machine-readable control ecosystems. The semantic model is portable.

## Freshness classes

Not every security source changes at the same rate.

### Threat-live

Examples: known exploited vulnerabilities, active vendor advisories, affected/fixed version data.

These can change without a code commit and require current rechecks at relevant release/operation points.

### Product-version

Examples: exact product hardening/configuration guidance.

Bind the relevant product/version and recheck on product/context changes and before high-impact operations where stale information is material.

### Standard-pinned

Examples: stable ASVS/CIS/NIST baseline versions.

Pin the exact version used by the current work. New standards do not silently rewrite in-flight work, but may generate an explicit migration/review signal.

### Project-decision

Project-specific accepted security decisions persist until superseded. Exceptions that weaken security requirements are time/review bounded.

## Known-Bad Security Pattern Registry

When a vulnerability or insecure configuration is discovered, the system retains actionable **negative knowledge**.

```text
vulnerable state/pattern
      ↓
Known-Bad record
      ↓
applicability + source + affected versions
      ↓
forbidden state
      ↓
regression verifier
```

Examples:

- vulnerable dependency/version range;
- insecure deprecated API;
- unsafe vendor setting invalidated by advisory;
- previously exploited project bug pattern;
- obsolete cryptographic/protocol configuration;
- superseded insecure workaround.

This registry is scoped/versioned so old prohibitions do not become context-free folklore.

## Why this defeats the probabilistic-prior problem

Assume the model has seen one million examples of configuration A and only a small number of configuration B.

Later, configuration A is found vulnerable and B becomes required.

Without D035:

```text
prompt
  ↓
model prior strongly favors A
  ↓
A generated again
```

With D035:

```text
current advisory/baseline
  ↓
A becomes FORBIDDEN
B becomes REQUIRED
  ↓
controls grounded before generation
  ↓
model proposes implementation
  ↓
independent verifier checks actual state
  ├─ A → FAIL/BLOCK
  └─ B → PASS
```

The model may still probabilistically propose A. The system no longer depends on the model choosing correctly.

## Development verification stack

Use the least probabilistic evidence capable of establishing each control.

Typical applicable layers:

```text
threat model / abuse cases
          ↓
security requirements (versioned)
          ↓
implementation
          ↓
static analysis / secret checks
          ↓
dependency vulnerability analysis
          ↓
negative + structural + regression tests
          ↓
fuzzing / dynamic security tests where applicable
          ↓
security acceptance
```

A confirmed security bug should produce a historical regression case whenever technically practical.

A scanner pass alone is not a complete security proof; verification composition depends on the threat/control.

## System/configuration verification stack

D035 composes with D033 authorization and D034 runbooks.

```text
Security Control Set
        ↓
Execution Capability Envelope (D033)
        ↓
Runbook (D034)
        ↓
bind exact product/version/target/principal
        ↓
preflight actual state
        ↓
execute through terminal/platform-neutral adapter
        ↓
query actual resulting state
        ↓
configuration/compliance/vulnerability verification
        ↓
PASS / BLOCK / HUMAN_EXCEPTION
```

A successful command or runbook exit code does not prove a secure configuration.

The postcondition is verified from the target state.

## Machine-readable security checks

When a security property is deterministic, prefer a machine-verifiable assertion.

Examples:

```text
required setting = expected secure value
forbidden feature = absent/disabled
dependency version ∉ vulnerable range
network exposure = absent
required access rule = present
vulnerability regression = not reproducible
actual configuration = selected baseline
```

Potential providers include project-native policy-as-code, configuration/compliance tooling, NIST SCAP/OVAL ecosystems, NIST checklist content, CIS assessment tooling or equivalent platform-native mechanisms.

Agent Governance does not require one of these products universally.

## Security standards and current sources

As of August 2026, research for D035 confirmed relevant current reference points:

- NIST SP 800-218 SSDF 1.1 is the current final SSDF; SSDF 1.2 is still an initial public draft.
- OWASP ASVS 5.0.0 is the current stable ASVS and supports version-qualified requirement references.
- NIST SP 800-70 Rev. 5 is final (May 2026) and explicitly supports machine-readable/executable security configuration checklists, verification and unauthorized-change detection.
- SCAP 1.4 is final (June 2026) for standardized automated configuration/vulnerability/compliance assessment content.
- OSCAL provides machine-readable security-control/baseline/implementation/assessment formats.
- CIS Benchmarks provide consensus secure configuration baselines for many product families.
- CISA KEV is a living source for vulnerabilities known to be exploited in the wild.

These are source/provider examples. The actual project/product determines applicability.

## Continuous posture invalidation

Security posture is not immutable.

```text
accepted release/system
       │
       ├── new vendor advisory
       ├── new KEV/CVE applicability
       ├── dependency advisory
       ├── new confirmed project vulnerability
       └── configuration drift
               │
               ▼
       affected control invalidated
               │
       ┌───────┴────────┐
       ▼                ▼
 not applicable     applicable
                        │
                        ▼
                 STALE / VIOLATED
                        │
                        ▼
                 remediation task
```

Historical task acceptance remains true about what was accepted at that time. Current security posture changes independently.

## Human exceptions

The model cannot invent a security waiver.

A Human-approved exception records:

```text
control + exact scope + risk
+ compensating controls
+ verification
+ expiry/review condition
+ remediation trigger
```

Expired exceptions become blocking again.

## Security content supply chain

Verification rules and security baselines can themselves be compromised or outdated.

Retain relevant provenance:

- canonical publisher;
- stable/draft/deprecated status;
- exact version/revision;
- retrieval/check time;
- digest/signature where supplied;
- local adaptation delta.

Reuse project-native security-control systems before creating duplicate Governance truth.

## Relationship to Agent Governance architecture

```text
D032  quality/security triage + Human-facing presentation
D035  security authority/freshness + independent proof
D033  execution capability authorization
D034  runbook procedure + terminal-neutral adapter
```

Combined security-sensitive operation:

```text
Human intent
   ↓
current security control resolution
   ↓
solution/threat design
   ↓
Execution Capability Envelope
   ↓
Runbook
   ↓
platform adapter
   ↓
actual code/system change
   ↓
independent security verification
   ↓
security posture + evidence
   ↓
continuous invalidation signals
```

## Planned implementation boundary

D035 is architecture only while T004 is running.

The next execution/security Core integration should consider D033 + D034 + D035 together and mechanically test at least:

- model proposes an obsolete known-bad pattern → verifier blocks it;
- vendor advisory supersedes old configuration guidance;
- stale security-source state blocks a high-impact operation;
- new dependency vulnerability invalidates current posture;
- actual system configuration differs from expected postcondition;
- previous vulnerability has a regression verifier;
- Human exception is scoped and expires;
- terminal/platform adapter differences do not alter security semantics.
