# Security Authority and Verification

Security-Verification-Version: 1.0.0

Load this module when security is material to engineering strategy, readiness, implementation verification, release/operation posture, dependency/configuration state, or when a new advisory/vulnerability/drift signal may invalidate a previously acceptable security posture.

This module integrates D035 into the portable Governance Core. `QUALITY.md` remains authoritative for mandatory security triage; this module governs current security authority, freshness, known-bad state, independent verification, exceptions and temporal posture invalidation once security is material.

## Core invariants

```text
model output != security authority
security guidance freshness != model training freshness
security acceptance = applicable current controls + independent evidence
past task acceptance != permanent security posture
security PASS != execution authorization
execution authorization != security PASS
```

A model may propose architecture, implementation, configuration, remediation and mappings. It cannot establish a current security fact merely by asserting it, and it cannot convert a deterministic or authoritative security failure into `PASS` by explanation.

Security correctness and execution authority are independent control planes. D035 security evaluation may narrow/block an operation, but it cannot grant effects outside the D033 execution-capability envelope. Conversely, an allowed D033/D034 operation is not secure merely because it is authorized or because a runbook/adapter completed successfully.

## When security is material

`QUALITY.md` performs security triage for every implementation scope. Apply this module when the scope materially introduces, changes, depends on or verifies a security-sensitive property such as:

- authentication, authorization, privilege or trust boundaries;
- externally controlled/untrusted input or public/network exposure;
- secrets, credentials or cryptographic material;
- security-sensitive persistence/state or multi-tenant isolation;
- executable dependencies/plugins/automation/supply-chain artifacts;
- security-sensitive configuration, deployment or operational controls;
- a known vulnerability, advisory, exploit, insecure/deprecated pattern or hardening requirement;
- a security exception/compensating control;
- current security posture that can change without a repository commit.

Security controls must be resolved before implementation when they affect design/behavior. Post-generation verification is proof, not a substitute for missing requirements.

## Security authority classes

Resolve applicable security facts from explicit source classes rather than model prior knowledge.

### Project-authoritative state

Human-approved project requirements, accepted threat/security decisions, project-native security architecture/policy, accepted compensating controls and bounded security exceptions.

Project authority controls project-specific intent and risk tolerance until superseded. Exceptions that weaken a normal requirement must be time/review bounded.

### Product/vendor-authoritative state

Current product/version/platform-specific security documentation and advisories establish facts such as affected/fixed versions, secure/removed settings, supported mitigations, changed defaults and compatibility constraints.

A remembered/model-generated product fact is non-authoritative when a current product/vendor source can establish it.

### Current vulnerability/threat intelligence

Applicable current vulnerability/advisory/exploitation state may change without source-code change. Treat authoritative current intelligence as a time-sensitive input when it materially affects the target/component.

Applicable known-exploited or otherwise project-defined release-blocking exposure is blocking unless a bounded Human-approved exception with verified compensating controls applies.

### Versioned verification/security standards

Applicable stable standards/baselines may define testable requirements or secure configuration state. Pin an explicit version/revision when the source provides one. A newer standard does not silently mutate an in-flight contract; it creates a review/migration signal according to project policy and materiality.

### Model/internal knowledge

Model knowledge is useful for discovery, explanation, mapping and implementation alternatives. It is not an authority class for a security-sensitive fact that can be established by the applicable sources above.

Unresolved material conflicts between applicable authoritative sources fail closed until Strategy/Human resolves them.

## Security Source Resolver

Before a security-sensitive scope becomes READY, Strategy makes the applicable security source set determinable.

Record or make derivable the applicable subset of:

- component/product/technology identity;
- exact version/range/environment where material;
- project security decision/exception references;
- authoritative source identity/class;
- source version/revision/publication/advisory identifier when available;
- retrieval/check time when freshness matters;
- source digest/signature/provenance when supplied and material;
- applicability/exclusions;
- freshness class;
- unresolved source conflicts.

Distinguish stable/final material from draft/preview/deprecated material. Draft/newer material may inform Strategy but does not silently replace the selected stable baseline.

## Versioned Security Control Set

Represent applicable security requirements as a versioned/scoped control set. A serialization format is not mandated.

A material control must make the applicable subset of these facts determinable:

- `control_id` — stable local identity;
- `scope` — affected component/resource/operation;
- `source_class` and `source_ref`;
- `source_version` / revision / publication identity;
- `source_checked_at` when freshness is relevant;
- `applicability` — target/product/version/context predicate;
- `required_state` — property/state that must hold;
- `forbidden_state` — obsolete/vulnerable state or pattern when useful;
- `verification` — required independent evidence/verifier;
- `freshness_class`;
- severity/priority when controlling;
- `exception_ref` and expiration/review condition when applicable;
- `regression_ref` when durable anti-regression evidence exists;
- current status.

Do not encode provider-specific command syntax or one external schema into portable Core semantics. Existing compatible project-native control systems are reused/adapted under `COEXISTENCE.md` rather than mirrored.

## Freshness classes and states

Security sources change at different rates; do not apply one arbitrary global TTL.

### Freshness classes

- `THREAT_LIVE` — active advisories, exploitation state, affected/fixed-version intelligence and equivalent time-sensitive threat facts. Recheck at applicable security-sensitive release/operation/execution points.
- `PRODUCT_VERSION` — product/version/platform hardening guidance. Recheck when product/version/target/material context changes and before high-impact operations when stale guidance could cause harm.
- `STANDARD_PINNED` — explicit stable standard/baseline revision selected for the current contract. New releases create review signals; they do not silently rewrite in-flight requirements.
- `PROJECT_DECISION` — project-approved security decisions remain current until superseded, except weakening exceptions whose explicit expiry/review conditions control freshness.

### Freshness states

- `CURRENT` — required freshness condition is satisfied;
- `STALE` — required recheck is due or the bound context changed;
- `UNKNOWN` — reliable current source state was not established;
- `CONFLICT` — applicable authoritative sources materially disagree;
- `SUPERSEDED` — a newer accepted control replaced this record.

`STALE`, `UNKNOWN` and unresolved `CONFLICT` block security acceptance where current knowledge is required. `SUPERSEDED` controls are not evaluated as active requirements except for historical/audit context.

Freshness evaluation must be based on explicit source/control facts and a determinable evaluation point. Deterministic tests must use supplied/fixed evaluation times, never network state or wall-clock timing as hidden inputs.

## Known-Bad Security Pattern Registry

Retain actionable negative security knowledge when the project has concrete reason to reject a state/pattern.

Examples include vulnerable dependency ranges, deprecated insecure APIs/algorithms/configuration, advisory-invalidated settings, previously exploited project defects, forbidden baseline states and superseded insecure workarounds.

A record is scoped/versioned and includes applicability so a historical prohibition does not become context-free folklore.

Conceptual states:

- `ACTIVE` — currently forbidden when applicable;
- `MITIGATED` — exposure remains but an accepted verified mitigation applies;
- `SUPERSEDED` — replaced by a newer control;
- `NOT_APPLICABLE` — target/version/context predicate does not match;
- `EXCEPTION` — bounded Human-approved exception applies and remains valid.

An applicable `ACTIVE` known-bad record is blocking even when the pattern is statistically common, historically popular, model-recommended or previously accepted in another context.

## Ground-before-generation rule

When security is material, load only the applicable active security controls before the implementation model chooses the security-sensitive design/configuration.

This reduces probability of an obsolete proposal; it is not proof. The implementation remains subject to independent verification.

Do not flood unrelated tasks with broad security catalogs. Applicability and progressive context loading remain mandatory.

## Independent verification

Security acceptance depends on evidence independent of the implementation model's unsupported self-assertion.

Applicable evidence may include deterministic repository tests, static/dynamic analysis, dependency/vulnerability checks, configuration/compliance checks, actual target-state queries, policy-as-code/checklist evaluation, historical regression tests, or Human/Strategy security review for properties not mechanically decidable.

Where a property is mechanically decidable, deterministic/machine evidence is preferred.

A second model or probabilistic reviewer may contribute supplemental findings but cannot be the sole release-blocking verifier for a property with deterministic or authoritative verification. Source-product verification additionally follows D037.

No single scanner/tool pass constitutes universal proof of security. Select the least probabilistic evidence combination capable of establishing the required controls.

## Security acceptance outcomes

Use these conceptual outcomes after evaluating all applicable blocking controls:

### `PASS`

All release/operation-blocking applicable controls have current authoritative basis and all required independent evidence passes.

### `BLOCK`

One or more blocking conditions exist, including:

- applicable active known-bad state;
- failed required verifier;
- stale/unknown source where current knowledge is required;
- unresolved authoritative-source conflict;
- applicable unmitigated project-defined blocking vulnerability/exploitation state;
- required evidence missing;
- actual code/target/configuration differs from the verified state;
- expired/invalid exception.

### `HUMAN_EXCEPTION`

A bounded Human-approved exception applies to the exact violated/deferred control and scope, its compensating controls are independently verified, and its expiry/review condition remains valid.

`HUMAN_EXCEPTION` is not `PASS`; it is explicit accepted residual risk. It does not grant D033 execution authorization and does not waive unrelated controls.

A model cannot create an exception or convert `BLOCK` to `PASS` by rationale.

## Human security exceptions

Only Human/Strategy authority may establish a security exception.

A valid exception makes the applicable subset determinable:

- violated/deferred control;
- exact scope/target/version;
- rationale and risk/impact;
- compensating controls;
- independent evidence for compensating controls;
- owner;
- expiration/review condition;
- remediation trigger.

Exceptions are exact-scope and non-transitive. A child task/adapter/component cannot inherit a broader exception than the controlling record authorizes.

Expired, out-of-scope or unverifiable exceptions are blocking again.

## Security-fix regression invariant

A confirmed vulnerability/security defect should produce durable negative knowledge when technically practical:

1. corrected required behavior/control;
2. vulnerable/obsolete state recorded as forbidden/superseded;
3. deterministic regression rule/test/check that detects the former defect;
4. remediation passes that verifier;
5. regression remains so a later probabilistic implementation cannot silently reintroduce the old pattern.

A durable regression artifact is stronger than a prompt reminder.

## Dependency and vulnerability posture

A dependency/component approved at one time is not permanently secure.

Where material:

- resolve exact identity/version from project-native inventory/lock state where available;
- evaluate applicable current authoritative vulnerability/advisory state;
- ground known fixed-version/mitigation requirements before changes;
- verify mitigations when a direct fix is unavailable;
- convert newly applicable vulnerabilities into current posture changes/remediation work without rewriting historical task acceptance.

## Temporal posture invalidation

Historical task acceptance is immutable evidence about the past; current security posture is temporal.

```text
accepted task/release at time A
        +
new applicable advisory/vulnerability/drift at time B
        -> historical acceptance remains accepted
        -> affected current security posture becomes STALE/VIOLATED/BLOCKING
        -> create/reopen remediation work through normal Governance
```

An invalidation signal never authorizes remediation by itself. It updates posture. Remediation still passes D032 quality, D033 authorization and D034 procedure controls when those layers apply.

Relevant invalidation signals may come from authoritative advisories/intelligence, dependency findings, confirmed project incidents, selected baseline changes or actual configuration drift.

## Composition with D033/D034 execution control

For material system/configuration operations the conceptual order is:

```text
applicable Security Control Set
        ↓
Execution Capability Envelope (D033)
        ↓
selected/reused Runbook (D034)
        ↓
bind exact target/version/context
        ↓
preflight security freshness/current state
        ↓
authorize and execute semantic steps
        ↓
query/verify actual resulting state independently
        ↓
security PASS | BLOCK | HUMAN_EXCEPTION
```

Composition rules:

- security evaluation can narrow/block but cannot expand execution authority;
- D033 `DENY`/required Human gate is not bypassed by security `PASS`;
- D033/D034 success is not security `PASS` without D035 evidence;
- command/adapter/runbook exit success is not a secure-state verifier when actual state can be checked independently;
- target/context drift may invalidate both execution authorization and security evidence and requires revalidation of each affected plane;
- native security/access controls that deny an operation remain real constraints and are not bypassed to satisfy Governance workflow.

## Provider and ecosystem boundary

Portable Core defines security capabilities and authority semantics, not mandatory security products, SDD frameworks, scanners, feeds, schemas or workflow providers.

Use `COEXISTENCE.md` to detect/reuse/adapt compatible project-native security control, policy, scanning, compliance, vulnerability, configuration or evidence providers. External provider lifecycle/status/receipts/findings are evidence/capability inputs only unless separately bound by Governance authority.

A provider may impose stricter native blocking constraints. It cannot grant Governance scope, task acceptance, execution authority, merge or release authority merely because its own lifecycle reports success.

Absence of a particular provider is valid. Security requirements must remain expressible and verifiable through suitable project-native or otherwise approved mechanisms.

## Readiness rule

Before F5 passes for a security-material task, Strategy verifies the applicable subset is determinable:

- relevant authoritative source/control set and applicability;
- freshness class/state and required recheck point;
- known-bad records relevant to the scope;
- independent verifier/evidence required for each blocking control;
- security exception semantics where any exception is intended;
- temporal invalidation/recheck conditions where posture can change;
- D033/D034 composition when material execution effects exist;
- no unresolved security-source/provider/authority conflict.

If current security authority, applicability or required verification cannot be established, the task is not READY.

## Blocker routing

Security blockers include at least:

- stale/unknown/conflicting required security source state;
- active applicable known-bad state;
- failed/missing independent verifier;
- target/component/version mismatch;
- expired/out-of-scope/unverified exception;
- new applicable vulnerability/advisory/drift invalidating current posture;
- provider/native control denial that cannot be safely reconciled;
- attempted model self-approval or unsupported security assertion used as acceptance evidence.

Persist the concise blocker/evidence and stop/re-enter the controlling Governance phase/task. Do not weaken the security requirement, switch providers merely to bypass a denial, or broaden execution authority as a workaround.
