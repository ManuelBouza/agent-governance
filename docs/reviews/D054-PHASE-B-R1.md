# D054 Phase-B R1 — Routed Core Activation Review

## Decision

Status: `ACCEPTED`

D040 Phase-B for D054 is accepted and integrated as a Markdown-only Core activation.

## Identity

- Decision: `D054`
- Migration control: `D040`
- Readiness prerequisites: T035 `ACCEPTED`, T036 `ACCEPTED`
- Activation branch: `feat/d054-phase-b-core-activation`
- Activation HEAD: `7ab00e5358ccf021312d3652f428624d6f9b279d`
- Integration PR: #211
- Integrated develop anchor: `37d163975f46b67573ee9ce1ffff6e1745195126`

## Activated Core state

- `governance-core/GOVERNANCE.md`: `Protocol-Version: 1.15.0`
- `governance-core/EXECUTION-CONTROL.md`: `Execution-Control-Version: 1.1.0`
- `governance-core/PROTOCOL.md`: `Protocol-Module-Version: 1.4.0`
- `governance-core/CONTEXT.md`: `Context-Version: 1.4.0`

## Convergence review

The remote PR diff is limited to the four routed Core Markdown modules authorized by D054 Phase-B.

The activation preserves:

- Consumer CLI v1 surface; no runtime or non-Markdown change;
- D033 effect/target authorization and Human-gate semantics;
- D034 separation of semantic procedure from terminal syntax;
- runbook meaning as Governance procedure authority;
- recipes as Implementation-owned bounded technical evidence/cache rather than execution authority;
- authoritative, version-compatible help/documentation fallback instead of model-memory command guessing;
- evidence-gated `CANDIDATE -> VERIFIED` promotion only after semantic postcondition verification;
- project-native runbook/recipe provider reuse before Governance-owned persistence;
- `.agent-coordination/runbooks/` native persistence without copying the registry into STATE;
- progressive context loading of only the active runbook/compatible recipe;
- Human Owner interaction for `REQUIRE_HUMAN`, MFA/external approval, material credential/risk decisions or explicit syntax inspection/execution, not routine command copy/paste.

T036 independently verified the pre-activation canonical baseline from an isolated native-Windows checkout (`6` focused tests, `355` full tests, Ruff check/format and diff checks all green) and explicitly removed the stale historical protocol-version pin that previously blocked this version transition.

No new executable behavior was required by the Phase-B Markdown activation. Local test execution from the Orchestrator environment was unavailable due network isolation, so acceptance relies on the D040 staged-readiness design, accepted T035/T036 evidence, and remote diff review rather than inventing a new executable work unit.

## Consequence

D054 Executor-owned operation resolution and verified runbook-recipe semantics are now routed Consumer Core behavior under protocol `1.15.0`.

The old `feat/d054-core-activation` branch and any unattached pre-T036 draft blobs remain non-authoritative historical scratch state and must not be reused.

T021/T022 remain paused and are not resumed by this activation.
