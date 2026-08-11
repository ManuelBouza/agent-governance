# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O022  
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

T004 remains governed by its existing contract. D033/D034/D035 architecture work MUST NOT retroactively broaden or alter its running execution semantics.

## Accepted Architecture Frontier

Three complementary execution/security decisions are now accepted architecture:

- `docs/decisions/D033-execution-access-control-plane.md` — authorization by actor/target/effect/privilege/credential/resource scope;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — reusable runbook procedures and terminal/platform-neutral execution adapters;
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md` — current security authority, freshness, known-bad anti-regression and independent verification.

Consolidated overviews:

- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`.

D033/D034/D035 are architecture decisions only and are not yet integrated into Governance Core/protocol.

## D033 — Execution Authorization

Core invariant:

```text
transport or credential possession != execution authority
```

Execution Capability Envelopes bound the applicable subset of:

- actor/role;
- exact target/environment/account/resource;
- effect classes;
- resource scope;
- privilege ceiling;
- credential source/use;
- network path/destinations;
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

Core invariants:

```text
procedure semantics != terminal syntax
approved runbook != approved invocation
```

Runbooks are preferred durable procedures for repeatable/material operational changes and describe the applicable subset of:

- outcome;
- applicability/exclusions;
- capability/target/privilege class;
- non-secret inputs;
- preconditions;
- ordered semantic steps;
- checkpoints/Human gates;
- postconditions;
- rollback/recovery;
- evidence.

Reuse adequate project-native runbooks/workflows before creating Governance-owned procedures.

Terminal, shell, CLI, API, SDK, remote transport, CI/CD and orchestration products are execution adapters, not Governance authority.

## D035 — Security Authority, Freshness and Independent Verification

The Human Owner identified a specific AI-security risk: a probabilistic model may choose a historically common implementation/configuration that has since been found vulnerable, especially when the secure replacement is newer or less represented in model training data.

D035 addresses this structurally rather than through stronger prompting.

Core invariants:

```text
model output != security authority
security guidance freshness != model training freshness
security acceptance = applicable current controls + independent evidence
past task acceptance != permanent security posture
```

Security-sensitive work follows three stages:

```text
1. GROUND BEFORE GENERATION
   resolve/load applicable current security controls

2. VERIFY AFTER GENERATION
   independent deterministic/technical evidence decides acceptance

3. INVALIDATE AFTER DEPLOYMENT
   advisories/vulnerabilities/drift can revoke current posture
```

Grounding lowers probability of insecure output. Independent verification is the acceptance authority.

## D035 Security Source Classes

Applicable security requirements may come from:

1. project-authoritative security decisions/threat model/exceptions;
2. exact product/vendor current security documentation/advisories;
3. current vulnerability/threat intelligence, including applicable CISA KEV as prioritization input;
4. versioned verification/security standards such as applicable OWASP ASVS, CIS Benchmarks and NIST security configuration checklists;
5. model/internal knowledge only as non-authoritative discovery/implementation assistance.

Current external/project sources override unsupported model recollection when applicable.

Material source conflicts fail closed until resolved.

## Versioned Security Control Set

A later Core implementation should make the applicable subset of these fields determinable:

- control identity;
- component/target/version applicability;
- source class/reference/version/revision;
- source freshness/check timestamp;
- required state;
- forbidden/known-bad state;
- independent verifier/evidence;
- freshness class;
- priority/severity where relevant;
- Human exception reference/expiry;
- regression verifier reference;
- status: current/stale/conflict/violated/exception/superseded.

D035 defines semantics, not one serialization.

## Security Freshness

Do not use one arbitrary global TTL.

Conceptual freshness classes:

- `THREAT_LIVE` — KEV/active advisories/affected-version data; recheck at relevant security-sensitive execution/release/operation points;
- `PRODUCT_VERSION` — vendor/product hardening; bind exact version/context and recheck on material product/target/context change;
- `STANDARD_PINNED` — stable ASVS/CIS/NIST baseline version pinned to the current contract; newer releases trigger explicit review rather than silently changing in-flight work;
- `PROJECT_DECISION` — persists until superseded; weakening exceptions must be time/review bounded.

Freshness outcomes:

- `CURRENT`;
- `STALE`;
- `UNKNOWN`;
- `CONFLICT`;
- `SUPERSEDED`.

High-impact security acceptance blocks on stale/unknown/conflicting current-security state unless the Human explicitly accepts bounded risk.

## Known-Bad Security Pattern Registry

Confirmed vulnerabilities and obsolete insecure patterns should become durable negative knowledge when applicable.

Examples:

- vulnerable dependency/version range;
- deprecated insecure API/algorithm/configuration;
- vendor setting invalidated by advisory;
- previous project exploit/bug pattern;
- configuration forbidden by selected baseline;
- superseded insecure workaround.

Records are scoped/versioned and may be `ACTIVE`, `MITIGATED`, `SUPERSEDED`, `NOT_APPLICABLE` or `EXCEPTION`.

Only relevant active records enter implementation context.

## Security-Fix Regression Invariant

When technically practical, remediation is not complete until:

1. corrected required behavior is defined;
2. former vulnerable state is forbidden/superseded;
3. deterministic regression rule/test/check detects the former defect;
4. the fix makes that verifier pass;
5. the verifier remains in regression coverage.

This is the primary defense against a later model statistically preferring the old vulnerable pattern.

## Independent Security Verification

Model self-review is not sufficient where independent verification is possible.

Software-development verification may include the applicable subset of:

- threat modeling/abuse cases;
- automated regression tests;
- static analysis;
- secret checks;
- dependency/software-composition vulnerability checks;
- negative/black-box/structural tests;
- historical security regressions;
- fuzzing;
- web/API dynamic security tests;
- included-library/service verification;
- independent architecture/security review for non-mechanical properties.

No single scanner constitutes complete proof.

For material system/configuration work:

```text
Security Control Set
 -> Execution Capability Envelope (D033)
 -> Runbook (D034)
 -> bind exact target/version/principal
 -> preflight actual state
 -> execute through terminal-neutral adapter
 -> query actual resulting state
 -> configuration/compliance/vulnerability verification
 -> PASS / BLOCK / HUMAN_EXCEPTION
```

Command/runbook success is not security proof. Resulting target state is verified independently.

## Machine-Readable Security Verification

Where a security property is deterministic, prefer a machine-evaluable assertion.

Examples:

- required secure setting/value;
- forbidden feature absent;
- dependency outside vulnerable range;
- required access rule present;
- forbidden network exposure absent;
- known vulnerable code/API absent;
- exploit/regression no longer succeeds;
- target configuration matches selected baseline.

Potential providers include project-native policy-as-code/configuration tooling, NIST SCAP/OVAL ecosystems, NIST checklist content, CIS assessment tooling and equivalent platform-native mechanisms.

No single provider is a Core dependency.

## Security Posture Is Temporal

Historical task acceptance and current security posture are separate.

```text
T123 ACCEPTED at time A
        +
new advisory/KEV/vulnerability at time B
        -> T123 remains historically ACCEPTED
        -> affected current control becomes STALE/VIOLATED
        -> create remediation task/runbook
```

New vulnerability intelligence does not silently authorize remediation; it routes through D032 quality/design, D033 authorization and D034 runbook controls.

## Human Security Exceptions

Only Human/Strategy authority may accept an exception.

A bounded exception records the applicable subset of:

- violated/deferred control;
- exact scope/target/version;
- rationale/risk;
- compensating controls;
- verification of compensation;
- owner;
- expiration/review condition;
- remediation trigger.

The model cannot invent an exception because the secure solution is inconvenient.

## Security-Control Supply Chain

Security baselines/rules/checklists are security-sensitive inputs.

Retain appropriate provenance:

- canonical publisher/source;
- stable/draft/deprecated status;
- exact revision/version;
- retrieval/check time;
- digest/signature when supplied;
- local approved adaptation delta.

Reuse project-native security systems/baselines before duplicating them.

## D035 Research Baseline — August 2026

Current authoritative sources reviewed:

- NIST SP 800-218 SSDF 1.1 — current final SSDF; SSDF 1.2 remains initial public draft;
- NIST IR 8397 — developer verification techniques including threat modeling, automated testing, static analysis, secret detection, historical tests, fuzzing, web scanners and included-component monitoring;
- OWASP ASVS 5.0.0 — current stable ASVS and explicit version-qualified requirement references;
- NIST SP 800-70 Rev. 5 — final May 2026 security configuration checklists including machine-readable/executable content, verification and unauthorized-change detection;
- SCAP 1.4 — current final June 2026 security configuration/vulnerability/compliance automation framework;
- OSCAL — machine-readable security-control/baseline/implementation/assessment formats;
- CIS Benchmarks — consensus secure configuration recommendations;
- CISA KEV — living catalog of vulnerabilities exploited in the wild;
- NIST AI RMF — ongoing testing/monitoring and Human intervention where AI cannot detect/correct errors.

Empirical AI-code-security studies reviewed show context-dependent/mixed security outcomes rather than deterministic reliability. D035 therefore does not depend on a particular failure rate; independent verification is required by architecture.

## T004 State

T004 remains the current executable frontier and is unchanged by D033/D034/D035.

T004 semantic grading remains `PENDING_CHATGPT` until its final handoff/results/transcripts are remotely reviewed.

## Planned Core-Integration Frontier

After T004 PD5, the leading architecture integration must consider **D033 + D034 + D035 together**, though implementation may be decomposed into multiple Task Contracts after graphical/quality readiness.

The smallest coherent future design should include the applicable subset of:

- execution-control Core routing;
- Execution Capability Envelope semantics;
- runbook selection/binding/preflight/Human gates;
- terminal-neutral adapter contract;
- Security Source Resolver;
- Versioned Security Control Set;
- Known-Bad Security Pattern Registry;
- security freshness/invalidation;
- independent verifier/evidence requirements;
- handoff evidence keyed by runbook/security control;
- deterministic synthetic tests for obsolete vulnerable patterns, stale security guidance, vendor advisory override, dependency vulnerability, actual configuration drift and Human exceptions;
- materially different adapter/platform fixtures so security semantics remain terminal-neutral.

Do not start this Core integration until T004 is resolved and a fresh D032 Primary Solution Diagram/quality triage has been presented.

## Active Remote Artifacts

- current T004 Task Contract: `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
- D033: `docs/decisions/D033-execution-access-control-plane.md`;
- D034: `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`;
- D035: `docs/decisions/D035-security-authority-freshness-and-independent-verification.md`;
- execution-control overview: `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- security-verification overview: `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`.

## Open Questions or Blockers

No known D035 architecture blocker remains.

T004 still requires executor return and PD5.

The source product remains not stable/release-ready. D033/D034/D035 Core integration, broader security/behavioral evals, property/state-machine coverage, Skill gates and other release gates remain incomplete.

## Next Action

1. review/integrate the D035 Markdown branch if limited to D035 + security architecture overview + this checkpoint;
2. do not alter T004;
3. when T004 returns, perform remote PD5 over harness/results/transcripts;
4. after T004 is resolved, design the combined D033+D034+D035 Core frontier graphically before implementation;
5. use deterministic security verifiers wherever the security property is mechanically checkable.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T004 is active/returned, load `docs/tasks/T004-d032-agent-facing-capability-eval.md` and handoff/results as needed;
2. for execution/security-control planning, load D033 + D034 + D035;
3. load `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md` and/or `docs/ARCHITECTURE-SECURITY-VERIFICATION.md` only when consolidated views are useful;
4. load D032/`QUALITY.md` only when diagram/quality readiness or T004 semantic review requires it.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not retroactively broaden/rewrite T004 because D033/D034/D035 were accepted while it was running.
- Do not treat model output/self-confidence/self-review as security authority.
- Do not rely on model training freshness for a security-sensitive current fact when an authoritative source can establish it.
- Do not treat past task acceptance as permanent security posture.
- Do not accept a successful command/runbook as proof of secure resulting state.
- Do not let stale/unknown/conflicting security-source state silently pass high-impact security acceptance.
- Do not let a model invent a security exception.
- Do not remove historical vulnerability regression checks merely because newer code appears different.
- Do not make ASVS/CIS/SCAP/OSCAL or another external security product a universal Core dependency.
- Do not duplicate adequate project-native security baselines/runbooks/tooling.
- Do not modify Core/protocol until a separate integrated Task Contract aligns code, protocol and deterministic verification.
- Do not declare the source product stable/release-ready from D035 or T004 alone.
