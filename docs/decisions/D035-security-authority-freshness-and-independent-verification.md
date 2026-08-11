# D035 — Security authority, freshness and independent verification

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance uses probabilistic AI systems to translate intent, design solutions and implement technical changes. A language model can generate a technically plausible implementation that reflects statistically common historical patterns rather than the most current secure practice for the exact product/version/context.

This risk is especially important when:

- a once-common implementation pattern has later been found vulnerable;
- a vendor has issued a mitigation or changed a secure default;
- a dependency version has acquired a newly disclosed vulnerability;
- a hardening benchmark has changed;
- a security control is uncommon enough that it is underrepresented in model training data;
- a model has seen conflicting old/new examples and selects the historically dominant pattern;
- an accepted system becomes insecure later without any source-code change because new threat intelligence is published.

Prompting the model to "be secure" is not a sufficient control. Grounding a model with current guidance reduces risk but remains probabilistic. Security acceptance therefore needs an authority and verification layer outside the model.

## Decision

Agent Governance SHALL define a **Security Authority & Verification Plane** for security-sensitive development and system/configuration work.

Core invariants:

```text
model output != security authority
security guidance freshness != model training freshness
security acceptance = applicable current controls + independent evidence
past task acceptance != permanent security posture
```

The AI may propose architecture, code, configuration, runbook realization and remediation. It MUST NOT be the sole authority that its own output is secure.

Security-sensitive work uses a two-part mechanism:

1. **pre-generation grounding / control resolution** — resolve the applicable current security control set before implementation so the model is less likely to choose an obsolete pattern;
2. **post-generation independent verification** — prove the implementation/configuration against deterministic or independent security checks so acceptance does not depend on model probability.

Where a property can be checked deterministically, deterministic evidence is preferred over model judgment.

## Security authority classes

Security requirements are resolved from explicit source classes rather than model prior knowledge.

### 1. Project-authoritative security state

Examples:

- Human-approved security requirements;
- accepted threat-model decisions;
- project-native security architecture;
- project security policies;
- accepted compensating controls;
- explicit, bounded security exceptions.

These define project-specific intent and risk tolerance.

### 2. Product/vendor-authoritative security state

For an exact product/version/platform, prefer current vendor-maintained security documentation and advisories for product-specific facts such as:

- affected/fixed versions;
- secure/removed settings;
- supported mitigations;
- changed defaults;
- compatibility constraints;
- patch/update instructions;
- product-specific hardening behavior.

A model's recollection of vendor behavior is non-authoritative when current vendor information is available.

### 3. Current vulnerability/threat intelligence

Use authoritative current vulnerability intelligence when applicable, including vendor advisories and CISA's Known Exploited Vulnerabilities (KEV) catalog as a prioritization input for vulnerabilities known to be exploited in the wild.

Applicable, unmitigated KEV exposure is a default release/operation blocker unless the Human Owner explicitly accepts a bounded exception with compensating controls.

### 4. Versioned verification/security standards

Use current, applicable external security standards/baselines as verification requirements rather than generic prose guidance.

Examples include:

- OWASP Application Security Verification Standard (ASVS) for applicable web application/service controls;
- CIS Benchmarks for secure configuration of supported technology families;
- NIST National Checklist Program security configuration checklists;
- other project/domain-native standards where authoritative and applicable.

Requirement references SHOULD include explicit version identifiers whenever the external project provides them.

### 5. Model/internal knowledge

Model knowledge is useful for discovery, explanation, implementation alternatives and mapping.

It is not authoritative for security-sensitive facts that can be checked against current external/project sources.

If model guidance conflicts with an applicable source above, the model guidance loses unless Strategy/Human explicitly resolves the source conflict.

## Security Source Resolver

Before a security-sensitive scope becomes READY, Strategy determines the applicable security source set.

The resolver records or makes determinable the applicable subset of:

- component/product/technology identity;
- exact version/range/environment where material;
- project security decisions/exceptions;
- vendor security guidance/advisories;
- vulnerability/threat intelligence sources;
- verification standard/baseline versions;
- source retrieval/check timestamp;
- source revision/version/digest when available;
- applicability/exclusions;
- unresolved source conflicts.

Source conflicts fail closed until resolved.

Security research MUST distinguish stable final standards from drafts/bleeding-edge material. Draft/newer guidance may inform a decision but does not silently replace the project's selected stable baseline.

## Versioned Security Control Set

The resolved security requirements are represented conceptually as a **Versioned Security Control Set**.

A control record should make the applicable subset of these fields determinable:

- `control_id` — stable local identifier;
- `scope` — component/resource/operation to which it applies;
- `source_class` — project, vendor, threat-intel, verification-standard;
- `source_ref` — source identity;
- `source_version` / publication or advisory revision;
- `source_checked_at`;
- `applicability` — exact product/version/context predicate;
- `required_state` — the security property/state that must hold;
- `forbidden_state` — known-bad/obsolete state or pattern when useful;
- `verification` — expected verifier/evidence;
- `freshness_class` — how/when the source must be revalidated;
- `severity_or_priority` — if used by the source/project;
- `exception_ref` — only when Human-approved;
- `exception_expiry` / recheck condition;
- `regression_ref` — durable test/rule/check that prevents recurrence when available;
- `status` — current, stale, conflict, violated, exception, superseded.

A later implementation task may choose JSON/YAML/OSCAL-compatible or project-native representation. D035 defines the semantics, not one serialization format.

## Freshness gate

Security requirements have different rates of change. Do not use one arbitrary global TTL.

Use freshness classes conceptually equivalent to:

### `THREAT_LIVE`

Examples: KEV, active vendor advisories, current affected-version information.

Recheck at security-sensitive execution/release/operation time when applicable because threat state can change without repository changes.

### `PRODUCT_VERSION`

Examples: product hardening guidance, vendor configuration/security docs.

Pin the exact relevant product/version guidance at planning; recheck when the product version, target environment or material execution context changes, and before high-impact operations when stale information could cause harm.

### `STANDARD_PINNED`

Examples: ASVS/CIS/NIST baseline releases.

Pin an explicit stable version for the current contract. A new release does not silently mutate an in-flight task, but creates a review signal for future/new work and may trigger explicit baseline migration when security impact is material.

### `PROJECT_DECISION`

Project security decisions remain authoritative until superseded, but exceptions MUST have explicit expiration/review conditions when they weaken a normal security requirement.

Freshness status:

- `CURRENT` — required freshness check satisfied;
- `STALE` — freshness requirement not satisfied;
- `UNKNOWN` — no reliable current source state was established;
- `CONFLICT` — applicable sources materially disagree;
- `SUPERSEDED` — a newer accepted control replaced this record.

`STALE`, `UNKNOWN` or unresolved `CONFLICT` security state blocks high-impact security acceptance unless the Human Owner explicitly accepts the bounded risk.

## Grounding-before-generation rule

When security is material, applicable active control records are loaded into implementation context before the model chooses the security-sensitive design/configuration.

This is a **probability-reduction control**, not proof.

The model is instructed by current, scoped controls instead of being asked to infer secure practice from its training distribution.

Only relevant controls are loaded. Do not flood every task with unrelated security catalogs.

## Independent verification rule

Security acceptance is performed against independent evidence.

The verifier must be independent of the model's unsupported self-assertion. It may be:

- deterministic repository tests;
- static/dynamic analysis tooling;
- dependency/vulnerability analysis;
- configuration/compliance assessment;
- actual target-state queries;
- policy-as-code/checklist evaluation;
- an independent Human/Strategy security review where automation cannot prove the property;
- a combination of the above.

A second model may provide supplemental review but MUST NOT be the sole release-blocking verifier for a security property that has a deterministic or authoritative external check.

## Development security verification

For security-sensitive software development, select the applicable subset of verification techniques based on threat model and technology.

The baseline toolbox includes:

- threat modeling / abuse-case review for design-level security issues;
- automated regression tests;
- static analysis for relevant weakness classes;
- secret detection where credentials/secrets could enter source/artifacts;
- dependency/software-composition vulnerability checks;
- negative/black-box security tests;
- code-structure tests where relevant;
- historical regression cases for previously confirmed vulnerabilities;
- fuzzing for parsers, protocols or high-input-complexity surfaces where useful;
- web/API dynamic security testing where applicable;
- verification of included libraries/packages/services;
- architecture/security review where the property is not mechanically decidable.

No single scanner constitutes proof of security. Apply the least probabilistic combination that can establish the required control.

## Security-fix regression invariant

A confirmed vulnerability or security defect SHOULD create durable negative knowledge.

When practical, remediation is not complete until the applicable subset exists:

1. a control states the corrected required behavior;
2. the vulnerable/obsolete state is recorded as forbidden or superseded;
3. a deterministic regression test/rule/check reproduces or detects the former defect;
4. the fix makes that regression pass;
5. the regression is retained so a later probabilistic model cannot silently reintroduce the old pattern.

This directly addresses the case where an obsolete vulnerable pattern remains statistically more common than its newer secure replacement.

A security regression artifact is stronger than a reminder in prompt text.

## Known-Bad Security Pattern Registry

D035 introduces the conceptual **Known-Bad Security Pattern Registry**.

It records active security anti-patterns that the project has concrete reason to reject, such as:

- a vulnerable dependency/version range;
- a deprecated insecure API/algorithm/configuration;
- a product setting invalidated by advisory;
- a previously exploited project bug pattern;
- a configuration state forbidden by the selected baseline;
- a previously accepted workaround that has been superseded.

Records are scoped and versioned. They must include applicability so obsolete prohibitions do not become permanent folklore after technology changes.

States may include:

- `ACTIVE` — currently forbidden when applicable;
- `MITIGATED` — underlying exposure remains but accepted mitigation exists;
- `SUPERSEDED` — replaced by a newer control;
- `NOT_APPLICABLE` — does not apply to this target/version;
- `EXCEPTION` — Human-approved bounded exception with expiry/review.

Only relevant active records enter implementation context.

## Dependency and vulnerability freshness

A dependency approved at one point in time is not permanently secure.

For included libraries/packages/services:

- exact dependency identity/version must be known from project-native lock/inventory data where available;
- vulnerability checks use current authoritative/advisory data appropriate to the ecosystem;
- known fixed-version/mitigation guidance is grounded before changing versions/configuration;
- applicable KEV exposure receives priority;
- an unavailable fix may use a bounded mitigation only when documented and verified;
- new vulnerability discovery creates remediation work without rewriting historical acceptance.

## System/configuration security verification

For security-sensitive configuration and operations, D035 composes with D033/D034.

The conceptual flow is:

```text
Execution Capability Envelope
    -> applicable Versioned Security Control Set
    -> selected/reused Runbook
    -> bind exact target/version/context
    -> preflight current security state
    -> execute semantic steps through terminal-neutral adapter
    -> independently verify resulting state
    -> record evidence
    -> monitor for drift/new vulnerability
```

Configuration security is not accepted because a command/script/runbook returned exit code 0.

Acceptance depends on the resulting target state satisfying the control set.

## Secure configuration baseline sources

Prefer project/vendor-native secure configuration guidance and established machine-verifiable baselines where applicable.

NIST's National Checklist Program and CIS Benchmarks are examples of external secure configuration baseline sources. SCAP/OVAL-compatible content is an example of machine-readable configuration/vulnerability assessment technology. OSCAL is an example of machine-readable control/baseline/implementation representation.

Agent Governance does not require SCAP, OSCAL, CIS tooling or one compliance product. These are capability providers/adapters under coexistence rules.

## System configuration verification stack

For material system configuration, use the applicable subset of:

- verify exact target/product/version/principal before mutation;
- capture baseline/current state;
- use preview/plan/dry-run when trustworthy and available;
- compare desired state against current vendor/project security baseline;
- apply through D034 runbook semantics and D033 authorization;
- query the actual post-change system state independently of command success;
- run applicable configuration/compliance checks;
- check patch/vulnerability state;
- verify privilege/network/logging/security-control postconditions;
- verify rollback/recovery path where material;
- detect drift/unauthorized configuration change after deployment.

When machine-readable/executable security checklist content exists, prefer using or adapting it over re-encoding the same requirement manually.

## Policy-as-code / machine-verification preference

Security requirements that can be expressed as machine-evaluable facts SHOULD have a machine verifier.

Conceptually:

```text
human-readable security requirement
        +
versioned machine-checkable assertion
        +
actual target/code evidence
        -> PASS / FAIL
```

Examples include:

- dependency version not in prohibited range;
- configuration flag equals required secure value;
- insecure protocol/cipher/feature disabled;
- required authorization rule exists;
- forbidden network exposure absent;
- code pattern/API absent;
- security header/policy present with required semantics;
- vulnerability regression exploit no longer succeeds;
- actual target matches approved security baseline.

Do not force every nuanced architectural requirement into simplistic policy-as-code if it would produce false confidence. Semantic design controls retain expert review plus targeted testing.

## Security exceptions

Only Human/Strategy authority may accept a security exception.

An exception must make the applicable subset explicit:

- violated/deferred control;
- exact scope/target/version;
- rationale/business constraint;
- risk/impact;
- compensating controls;
- verification of those compensating controls;
- owner;
- expiration/review condition;
- remediation trigger.

The implementation model MUST NOT create or silently assume a security exception because the secure implementation is inconvenient.

## Security posture is temporal

Task acceptance is immutable history, but security posture can change.

A new advisory, KEV entry, exploit, benchmark change or discovered project vulnerability does not rewrite a previously accepted task. Instead it may transition the affected security control/posture to `STALE` or `VIOLATED` and create a new remediation work unit.

Conceptually:

```text
T123 ACCEPTED at time A
        +
new vulnerability/advisory at time B
        -> historical T123 remains ACCEPTED
        -> current security posture becomes VIOLATED/STALE
        -> create remediation task/runbook
```

This avoids the false assumption that Git history alone determines current security.

## Continuous security invalidation

For deployed/operational systems and released software, a future integration SHOULD support event/poll based invalidation signals from applicable sources such as:

- vendor security advisories;
- current vulnerability feeds/catalogs;
- project security incidents/findings;
- dependency advisories;
- benchmark/baseline updates;
- actual configuration drift detection.

An invalidation signal does not automatically authorize remediation. It updates security posture and routes through normal D032 quality, D033 authorization and D034 runbook controls.

## Supply-chain protection of security controls

Security baselines/rules/checklists are themselves security-sensitive inputs.

Where practical, retain source provenance such as:

- canonical publisher/source;
- exact version/revision;
- retrieval timestamp;
- digest/signature when supplied;
- source status (stable/draft/deprecated);
- local approved adaptation delta.

Do not accept an arbitrary downloaded ruleset merely because it claims to be a security benchmark.

Existing project-native security tooling/baselines follow D026 coexistence/reuse rules.

## Security acceptance outcomes

Use conceptual outcomes:

### `PASS`

All release/operation-blocking applicable controls have current authoritative basis and required independent evidence passes.

### `BLOCK`

One or more blocking conditions exist, including:

- applicable known-bad state;
- failed security verifier;
- stale/unknown source where current security knowledge is required;
- unresolved authoritative-source conflict;
- applicable unmitigated known-exploited vulnerability;
- required security evidence missing;
- actual target/configuration differs from verified state.

### `HUMAN_EXCEPTION`

A bounded Human-approved security exception exists with compensating controls and expiration/review conditions.

A model cannot convert `BLOCK` to `PASS` by explanation.

## Relationship to D032

D032 already requires security triage inside the implicit quality envelope.

D035 makes the security dimension operationally stronger:

```text
D032: security is always triaged
D035: material security uses current authority + independent verification
```

The Human-facing explanation remains adapted to the user's technical register. The underlying verification rigor does not change.

## Relationship to D033/D034

D033 controls authorization of system effects.

D034 controls reusable runbook procedure and terminal-neutral realization.

D035 controls security correctness/freshness of what is being built/configured.

Combined:

```text
Human intent
   -> security source/control resolution (D035)
   -> solution + quality/threat design (D032)
   -> execution authorization envelope (D033)
   -> runbook semantic procedure (D034)
   -> terminal/platform adapter
   -> independent security verification (D035)
   -> evidence / acceptance / continuous posture
```

None of these layers may be replaced by model confidence.

## Primary Solution Diagram

Dominant question: control/data flow from current security authority to probabilistic implementation and independent verification.

Preferred view: DFD/control-flow hybrid.

```text
                 SECURITY-SENSITIVE CHANGE
                           │
                           ▼
                Security Source Resolver
      ┌────────────────────┼─────────────────────┐
      ▼                    ▼                     ▼
 project decisions    vendor/version docs   current security intel
 + exceptions         + advisories          KEV/CVE/advisories
      │                    │                     │
      └────────────────────┼─────────────────────┘
                           ▼
            Versioned Security Control Set
      required state · forbidden state · source
      applicability · freshness · verifier · expiry
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
         AI implementation          Runbook/config
      proposal, never authority     adapter realization
               │                       │
               └───────────┬───────────┘
                           ▼
               INDEPENDENT VERIFICATION
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
       code             dependencies       system state
 SAST/tests/fuzz/       advisories/SCA   benchmark/checklist/
 historical regressions                 postcondition/drift
         └─────────────────┼──────────────────┘
                           ▼
                SECURITY ACCEPTANCE GATE
             PASS / BLOCK / HUMAN_EXCEPTION
                           │
                           ▼
                 durable regression rule
```

## Security feedback / anti-regression loop

```text
new advisory / vulnerability / incident
             │
             ▼
   source/control freshness invalidated
             │
             ▼
  affected component/target resolution
             │
       ┌─────┴─────────┐
       ▼               ▼
   not applicable    applicable
                        │
                        ▼
             Known-Bad record/control
                        │
                        ▼
               remediation task
                        │
                        ▼
              fix + regression verifier
                        │
                        ▼
                 verified secure state
```

The anti-regression verifier is the mechanism that prevents a later model from choosing the historically common vulnerable pattern.

## Research basis

Primary/authoritative sources reviewed during this decision include:

### NIST Secure Software Development Framework

NIST SP 800-218 SSDF 1.1 remains the current final SSDF as of this decision; NIST has an initial public draft for SSDF 1.2. SSDF integrates secure development practices throughout the SDLC and includes responding to vulnerabilities to prevent recurrence.

- https://csrc.nist.gov/pubs/sp/800/218/final
- https://csrc.nist.gov/projects/ssdf
- https://csrc.nist.gov/pubs/sp/800/218/r1/ipd

### NIST minimum developer verification

NIST IR 8397 recommends a portfolio including threat modeling, automated testing, static scanning, hardcoded-secret checks, black-box/structural/historical tests, fuzzing, web app scanning where applicable, and checking included software. NIST specifically notes included components must be continually monitored because new vulnerabilities can be reported later.

- https://csrc.nist.gov/pubs/ir/8397/final
- https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-supply-chain-security-guidance-3

### OWASP ASVS

OWASP ASVS provides testable application security requirements. The current stable ASVS is 5.0.0. OWASP explicitly recommends including the ASVS version in requirement references because identifiers/content can change between versions.

- https://owasp.org/www-project-application-security-verification-standard/
- https://github.com/OWASP/ASVS

### NIST secure configuration / security automation

NIST SP 800-70 Rev. 5 (final, May 2026) defines security configuration checklists that can contain instructions, procedures or machine-readable/executable content to configure products, verify correct configuration, identify unauthorized changes and produce security posture artifacts.

SCAP 1.4 is current final as of June 2026 and supports automated configuration, vulnerability, patch, measurement and technical-control compliance activities.

OSCAL provides standardized machine-readable formats for control baselines, implementation and automated assessment workflows.

- https://csrc.nist.gov/pubs/sp/800/70/r5/final
- https://csrc.nist.gov/projects/security-content-automation-protocol/scap-releases/scap-1-4
- https://pages.nist.gov/OSCAL/

### CIS Benchmarks

CIS Benchmarks provide consensus-developed secure configuration recommendations across many vendor product families and are useful as a configuration-baseline provider where applicable.

- https://www.cisecurity.org/cis-benchmarks

### CISA Known Exploited Vulnerabilities

CISA maintains KEV as a living catalog of vulnerabilities known to be exploited in the wild and recommends organizations use it as an input to vulnerability-management prioritization.

- https://www.cisa.gov/known-exploited-vulnerabilities-catalog

### NIST AI Risk Management Framework

NIST AI RMF treats validity/reliability as requiring ongoing testing/monitoring and notes that human intervention may be needed where AI cannot detect/correct errors. This supports treating probabilistic AI output as a proposal requiring independent assurance for high-impact security decisions.

- https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/
- https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

### Empirical AI-code-security evidence

Empirical literature does not support assuming AI-generated code is intrinsically secure; results vary by task/model/study. This decision does not depend on a particular measured failure rate. The architectural response is independent verification.

Examples reviewed:

- Perry et al., "Do Users Write More Insecure Code with AI Assistants?" (2022 preprint);
- Sandoval et al., "Lost at C" (USENIX Security 2023);
- Chen et al., "Insecure Coding Preferences in Long-Term Memory" (2026 preprint).

The mixed empirical results reinforce that model behavior is context-dependent/probabilistic and unsuitable as security acceptance authority.

## Consequences

- security-sensitive tasks cannot rely solely on the model's internal knowledge;
- current/versioned security sources are resolved before material implementation;
- secure implementation guidance is grounded into the task context;
- model self-review is insufficient where independent verification is feasible;
- previously fixed vulnerabilities become durable regression rules/checks when practical;
- system configuration is verified by resulting state, not command success;
- security posture can become stale/violated after historical task acceptance;
- new advisories/vulnerability intelligence can create remediation work without rewriting history;
- security-control content itself requires provenance/freshness discipline;
- future Core integration of D033/D034 must also incorporate D035 rather than treating execution authorization as equivalent to security correctness.

## Current implementation boundary

D035 is an accepted architecture decision only in this change.

It MUST NOT modify the running T004 contract or current Governance Core/protocol while T004 is executing.

After T004 PD5, the next Core-integration planning SHOULD treat D033 + D034 + D035 as one coherent execution/security-control frontier, while still decomposing implementation tasks if necessary.

The later integration should define and test the smallest viable representation for:

- Security Source Resolver results;
- Versioned Security Control Set;
- Known-Bad Security Pattern Registry;
- security freshness/invalidation;
- independent verifier requirements/evidence;
- D033 authorization + D034 runbook + D035 postcondition composition;
- deterministic synthetic cases for stale guidance, superseded vulnerable pattern, vendor advisory override, dependency vulnerability, configuration drift and Human exception.
