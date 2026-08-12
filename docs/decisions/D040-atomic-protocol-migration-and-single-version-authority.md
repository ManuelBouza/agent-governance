# D040 — Atomic protocol migration and single version authority

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

The source repository splits ownership intentionally:

- ChatGPT owns committed Markdown, including `governance-core/GOVERNANCE.md` and protocol-module routing;
- the Agente de IA Ejecutor owns non-Markdown deterministic tests and helpers.

A hard-coded current protocol version duplicated in executor-owned test helpers therefore creates a sequencing hazard. A legitimate Markdown-owned protocol bump can make the canonical full test suite fail before the separately owned helper can be updated. The earlier L001 control corrected one concrete mismatch but retained this cross-owner duplicated mutable value.

During D036/T010 planning, an attempted `1.13.0` protocol bump reproduced the same mismatch on the planning branch before integration. The bump was reverted before reaching `develop`.

## Decision

`governance-core/GOVERNANCE.md` is the **single current protocol-version authority**.

Deterministic verification MUST parse and validate that authority; it MUST NOT maintain an independently authored exact-current-version literal whose synchronization is required for the suite to remain green.

```text
Core Protocol-Version = current-version authority

test helper = parser / validator / compatibility verifier
             != second current-version authority
```

Repository tests MAY encode:

- minimum/maximum compatibility bounds when a real compatibility contract requires them;
- expected historical fixture versions;
- explicit migration-transition states authorized by a Task Contract;
- module/version relationships that are deterministic consequences of Core state.

They MUST NOT encode a free-standing mutable duplicate of the current Core protocol version merely to compare it back to Core.

## Protocol migration sequence

When a protocol change crosses ChatGPT-owned Markdown and executor-owned verification, use a staged sequence that keeps canonical `develop` green.

### Phase A — verification readiness

1. Persist the decision/architecture/Task Contract from current green `develop`.
2. Add any new Core module as **staged/non-routed** Markdown when needed for deterministic testing.
3. Executor updates deterministic helpers/tests so they derive current protocol identity from Core and validate the pending module semantics without requiring the future protocol bump.
4. Accept/integrate/clean the executable readiness task while current protocol remains unchanged.

### Phase B — Markdown activation

1. From current green `develop`, ChatGPT activates the protocol change: version bump, source-map/router/readiness invariants and staged-module activation.
2. Existing deterministic tests must remain green because they consume Core as the version authority and already understand the new module semantics.
3. If activation requires new non-Markdown behavior beyond the pre-authorized readiness envelope, stop and create a new Task Contract rather than accepting a red intermediate baseline.

## Invariants

```text
protocol bump != permission to leave develop knowingly red
role separation != requirement for broken intermediate state
verification of authority != duplicate authority
staged module != active routed protocol module
```

A protocol transition that cannot preserve a green canonical baseline under this sequence requires an explicit migration decision before mutation.

## Relationship to L001

L001's original correction remains valid historical containment, but the D036 planning recurrence demonstrates that literal synchronization was not a sufficient systemic prevention control.

The stronger preventive control selected here is elimination of the independent mutable current-version literal plus staged protocol activation.

## D036/T010 application

For D036:

- `ASSURANCE.md` is first added as a staged module while Protocol remains `1.12.0`;
- T010 validates D036 assurance semantics and implements D040's single-version-authority test change;
- only after T010 is accepted/integrated/clean will ChatGPT activate `ASSURANCE.md` in `GOVERNANCE.md` and bump Protocol to `1.13.0` through a Markdown-only activation change;
- no real-system audit adapter/provider work is authorized by this migration.
