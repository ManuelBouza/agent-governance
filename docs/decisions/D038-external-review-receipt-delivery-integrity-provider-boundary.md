# D038 — External review-receipt and delivery-integrity provider boundary

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator  
Supersedes: D030 only for the capability-level Gentle-AI RDD disposition defined here  
Preserves: D026, D029, D030 fallback, D033, D034, D037

## Problem

D030 correctly identified a real source-maintenance authority collision: an external workflow overlay can become a second review/delivery authority and block or redefine Agent Governance handoff, acceptance, commit, push, PR or release semantics.

At the time, the safest disposition for Gentle-AI Receipt-Driven Development (RDD) was to classify its review/delivery authority as `CONFLICT` and disable that review mode only for the current clone when necessary.

Gentle-AI RDD has since evolved into a more explicit native integrity architecture with useful capabilities that are separable from Governance authority, including:

- freezing an exact candidate;
- deriving immutable candidate identity from Git/workspace evidence;
- provider-owned lifecycle/status/recovery;
- content-bound receipts;
- re-deriving live Git evidence at delivery gates;
- detecting candidate/scope drift;
- validating that commit/push/PR/release delivery still corresponds to the candidate/receipt;
- fail-closed handling for malformed/stale/conflicting provider state.

Discarding all of those capabilities merely because RDD also has review semantics wastes useful technical controls.

However, enabling RDD without a boundary would create two new problems:

1. its reviewer outcome or internal `approved` state could be confused with Agent Governance acceptance;
2. if its review depends on probabilistic agent/model judgments, making that review/receipt mandatory for source-product delivery would violate D037 deterministic code-only verification.

The required architecture is therefore **capability-level reuse under subordinate authority**.

## Decision

Agent Governance MAY reuse/adapt external review-receipt systems such as Gentle-AI RDD as **technical evidence and native delivery-integrity providers**, but they SHALL NOT acquire Governance authority.

Core invariants:

```text
external evidence != Governance acceptance

external provider lifecycle != Governance task lifecycle

external PASS = evidence, never acceptance authority

external native enforcement may narrow or block an execution path
but cannot expand Governance authorization

provider capability != source-product dependency
```

For Gentle-AI RDD specifically:

```text
RDD PASS != Governance ACCEPT
RDD internal approved != Task ACCEPTED
RDD receipt != merge/release authorization
```

The Human Owner remains final authority. ChatGPT remains source-maintenance Strategy/Markdown/acceptance authority. D029/Git remains the canonical handoff identity model.

## Capability decomposition

Gentle-AI RDD SHALL NOT be classified as one indivisible capability.

### 1. Candidate freezing and exact candidate identity

Classification: `REUSE` or bounded `ADAPT`.

Useful provider behavior includes:

- freezing exact candidate bytes/state;
- binding review/evidence to that candidate identity;
- distinguishing workspace/staged/base-diff projections where applicable;
- detecting candidate/scope changes after freezing;
- re-deriving candidate facts from live Git rather than trusting agent narration.

These facts are technical evidence. They do not determine Task Contract scope or acceptance.

### 2. Provider-owned status, recovery and reconciliation

Classification: `REUSE` or bounded `ADAPT`.

Provider-native status/recovery may be used to determine:

- whether provider state is current/stale/corrupt;
- whether a candidate changed;
- which provider transition is structurally valid;
- whether an exact retry is idempotent;
- whether a delivery-integrity gate can evaluate the current candidate.

This internal provider lifecycle is subordinate technical state.

It MUST NOT replace or mutate Agent Governance work states such as READY, IN_PROGRESS, DONE, ACCEPTED, REJECTED or CANCELLED.

### 3. Content-bound receipt / review identity

Classification: `REUSE` or bounded `ADAPT` as evidence.

A receipt may provide evidence that:

- a particular external review/verification transaction was bound to an exact candidate;
- the provider's recorded candidate identity matches its own validated state;
- later provider gates refer to the same candidate lineage/receipt.

A receipt MUST NOT mean:

- Agent Governance accepted the task;
- deterministic source-product verification passed;
- security acceptance passed;
- the Human authorized merge/release;
- the artifact is cryptographically attested against a malicious same-user local actor.

### 4. Delivery-integrity gates

Classification: bounded `ADAPT`.

A native gate may validate that an operation such as commit/push/PR/release still corresponds to provider-observed candidate/receipt state.

When such a provider path is explicitly selected and compatible with D037, its stricter denial is a real technical blocker for that path.

The provider gate MAY:

- reject candidate drift;
- reject stale/corrupt provider state;
- reject scope/identity mismatch;
- reject delivery that no longer matches the provider evidence.

It MUST NOT:

- grant Governance permission that D033/D034/Task Contract policy denies;
- convert provider `approved` into Governance acceptance;
- authorize a PR, merge or release that Human/ChatGPT policy has not authorized;
- broaden resource/effect scope to satisfy the gate.

### 5. Probabilistic reviewer findings

Classification: `COEXIST` as supplemental evidence only.

RDD reviewer/lens output MAY be inspected as an additional review signal when available.

Under D037 it SHALL NOT be:

- required for repository source-product verification;
- the sole or mandatory release gate;
- a model-as-judge acceptance mechanism;
- a statistical/stochastic correctness threshold;
- evidence that overrides deterministic tests/current authoritative security controls.

A finding can trigger Human/ChatGPT investigation or rework, but its absence does not prove correctness/security.

### 6. External acceptance/task/scope authority

Classification: `DENY` / `CONFLICT`.

RDD or another external provider SHALL NOT own or redefine:

- Human intent/scope;
- Task Contract objective;
- architecture decisions;
- acceptance criteria;
- execution authorization envelope;
- security exceptions;
- Governance DONE/ACCEPTED transitions;
- PR authorization;
- merge authorization;
- release authorization.

### 7. External SDD/planning authority

Not changed by this decision.

Existing D026/D030 coexistence rules continue to apply. Agent Governance MUST NOT initialize/migrate to an external SDD merely to satisfy a receipt/review gate.

## D037 precedence — deterministic verification remains mandatory

D037 remains fully controlling.

The source product SHALL NOT become dependent on a live LLM/model reviewer in order to test, accept, push, PR, merge or release its own Governance contract.

Therefore an RDD integration is valid only when its selected source-maintenance role can be used without turning probabilistic reviewer approval into a mandatory repository verification/release prerequisite.

Conceptually:

```text
repository deterministic tests/evidence
            +
Git/D029 identity
            +
optional external native integrity evidence
            +
optional reviewer findings
            ↓
ChatGPT/Human Governance decision
```

Not:

```text
model reviewer approval
        ↓
required receipt
        ↓
source-product release allowed
```

If the installed/current RDD contract cannot preserve that boundary, D030 clone-local opt-out remains the approved safe adaptation.

## Selected-provider non-bypass rule

An external provider is optional at architecture level, but once a particular candidate/delivery path is intentionally placed under that provider, an unfavorable native integrity result must not be bypassed merely by changing mechanism.

Invalid pattern:

```text
selected RDD integrity path
    -> candidate mismatch / stale / corrupt / deny
    -> disable RDD only to push the same candidate
```

That is authority laundering through mechanism switching.

Instead:

1. diagnose the provider denial;
2. repair/revalidate the candidate/provider state when appropriate; or
3. Strategy/Human explicitly changes the provider disposition;
4. restart/revalidate the affected delivery evidence under the new disposition;
5. persist the change when it affects future source-maintenance behavior.

A provider bug/incompatibility may justify falling back to D030, but the fallback is an explicit Governance decision, not an executor convenience.

## D033/D034 relationship

D038 treats RDD native delivery-integrity behavior as a possible **execution enforcement/evidence provider** under D033/D034.

```text
Governance authorization
        ↓
selected procedure/delivery path
        ↓
external native integrity enforcement
        ↓
Git/delivery effect
```

The external provider can narrow/block the path but cannot widen the Execution Capability Envelope.

A valid provider receipt is not authority to perform a different target/effect/privilege operation.

## D029 relationship

D029 remains canonical for source-maintenance executor handoff identity:

```text
implementation_head_sha
        ↓
handoff-only finalization
        ↓
actual pushed branch HEAD
```

External candidate/receipt identities are supplemental evidence that may later be referenced from a handoff when a future Task Contract authorizes that integration.

Conceptually:

```text
implementation candidate
       ├── Git/D029 implementation anchor
       └── optional provider candidate identity/receipt
                    ↓
              ChatGPT remote review
```

D038 does not silently change the current handoff schema or make receipt fields mandatory.

## Security and trust boundary

Gentle-AI's published review-authority threat model explicitly does not claim authenticity/tamper resistance against a malicious local actor with the same user/filesystem access who can also rewrite provider state, Git state or the binary.

Therefore:

```text
RDD receipt != cryptographic remote attestation
```

Agent Governance SHALL continue to rely on the appropriate combination of:

- canonical remote Git state;
- D029 ancestry/diff evidence;
- deterministic repository tests;
- current security verification under D035 when applicable;
- native platform/CI/security enforcement where applicable;
- Human/ChatGPT authority.

RDD adds integrity/reconciliation evidence; it is not a complete hostile-local-executor trust anchor.

## Primary Solution Diagram

Dominant question: how useful external review/integrity evidence can constrain delivery without becoming Governance authority.

Preferred view: DFD / authority-flow diagram.

```text
Human Owner
    │
    ▼
ChatGPT Strategy / Task Contract
    │
    │ scope + acceptance + D033 authorization
    ▼
Executor
    │
    ▼
implementation candidate
    │
    ├──────────────────────────────────────┐
    │                                      │
    ▼                                      ▼
Git/D029 identity                 External RDD provider
implementation anchor             ┌────────────────────────┐
+ final branch HEAD               │ freeze exact candidate │
                                  │ derive identity         │
                                  │ status/recovery         │
                                  │ optional review signal  │
                                  │ receipt/integrity facts │
                                  └───────────┬────────────┘
                                              │ evidence only
    └───────────────────┬──────────────────────┘
                        ▼
                 ChatGPT remote review
                 deterministic evidence
                        │
               ┌────────┴────────┐
               ▼                 ▼
            REWORK            ACCEPT
                                 │
                                 │ Governance delivery authorization
                                 ▼
                    optional native RDD integrity gate
                    ├─ mismatch/stale/corrupt -> BLOCK
                    └─ integrity valid -> continue
                                 │
                                 ▼
                            PR / merge / release
                      under Governance/Human authority
```

Normative interpretation:

```text
RDD PASS -> evidence; Governance still decides
RDD native integrity FAIL -> selected path blocks
Governance DENY -> RDD cannot override
```

## Gentle-AI adapter disposition

For the Agent Governance source repository, replace D030's blanket RDD classification with this capability-level disposition when the installed Gentle-AI version exposes compatible behavior.

| Gentle-AI RDD surface | Disposition |
| --- | --- |
| exact candidate freezing/identity | `REUSE` / `ADAPT` |
| live-Git re-derivation/drift detection | `REUSE` / `ADAPT` |
| provider status/recovery/reconciliation | `REUSE` / `ADAPT` |
| content-bound receipt as supplemental evidence | `REUSE` / `ADAPT` |
| deterministic delivery-integrity validation | `ADAPT` subject to D037 |
| probabilistic reviewer/lens findings | `COEXIST` supplemental only |
| reviewer/model approval as required source release gate | `DENY` under D037 |
| Governance task/scope/acceptance authority | `DENY` |
| Governance merge/release authorization | `DENY` |
| external SDD initialization solely to satisfy RDD | `DENY` |

## Compatibility/fallback behavior

Gentle-AI remains optional and non-canonical.

Before using this integration, the source-maintainer task must establish that the installed provider exposes the required compatible capability/contract surface.

Do not mutate global user configuration merely to make the integration work.

If the bounded disposition cannot be implemented safely:

```text
D038 bounded integration unavailable/incompatible
        ↓
D030 fallback
        ↓
clone-local review mode opt-out only
        ↓
ordinary Agent Governance source policy
```

The existing D030 approved commands remain the fallback when applicable:

```text
gentle-ai review mode status --cwd .
gentle-ai review mode disable --scope clone --cwd .
gentle-ai review mode status --cwd .
```

Do not disable globally.

## Research basis at decision date

Current Gentle-AI public documentation inspected on 2026-08-12 states, among other things:

- RDD is the supported stable path; public README identifies stable `v2.3.0` at that date;
- review starts by freezing exact candidate bytes/state and binding transitions to immutable candidate identity;
- delivery gates validate the same receipt and do not silently restart review for unchanged content;
- provider status/recovery/reconciliation is intended to derive safe continuation from native state rather than agent narration;
- disabled/unmanaged behavior defers to ordinary repository policy rather than fabricating provider approval;
- live-Git gate re-derivation detects incompatible scope/identity changes;
- the local review store is not claimed to resist a malicious same-user local actor with equivalent filesystem/Git/binary access.

Sources:

- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/README.md`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/architecture/organic-rdd.md`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/review-authority-threat-model.md`

These research facts justify the capability decomposition; they do not make `main`, a particular Gentle-AI version or Gentle-AI itself a product dependency.

## Relationship to D030

D030 remains accepted and controls general external-workflow precedence.

D038 supersedes only the D030 statement that treats Gentle-AI RDD review/delivery as one blanket `CONFLICT` surface.

The updated rule is:

```text
classify RDD by capability
    ├─ subordinate deterministic integrity/evidence -> REUSE/ADAPT
    ├─ optional reviewer signal -> COEXIST supplemental
    └─ overlapping Governance authority -> DENY/CONFLICT
```

D030 clone-local opt-out remains the fallback when capability-level coexistence cannot be made safe.

## Consequences

- Agent Governance can benefit from current/future RDD candidate-integrity mechanisms without surrendering acceptance authority.
- D037 remains intact; source-product correctness/release does not depend on stochastic reviewer output.
- RDD receipt/gate evidence can later strengthen D029 delivery integrity if a dedicated Task Contract defines the adapter/schema integration.
- provider-native denial is respected as a technical constraint while the provider path is selected, but it cannot create new authority.
- provider approval never substitutes for ChatGPT/Human acceptance.
- no Gentle-AI dependency is added to the source product.
- T005 remains accepted/integrated and unchanged.
- T006/D035 remains the next planned deterministic Core increment unless the Human Owner redirects.
