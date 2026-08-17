# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O106  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Frontier

Accepted architecture/method authority: D044, D049, D050, D051, D052.

Human Owner direction creates two lanes:

```text
Executor lane     = PAUSED until Human explicitly re-enables it
Orchestrator lane = ACTIVE for architecture/research/Markdown/D052 oracle design
```

Executable order remains:

```text
T032 R1 -> green baseline -> T021 R1 -> T022 -> MG1 -> T023 -> T024
```

T026 remains separately gated/BLOCKED.

## Executor lane

- T032 canonical remote remains rejected `fix/t032-rcab-snapshot-live-separation@b43b306e56c6b90969c3dd10e23ccf8e00cc8ba5`.
- T021 remains frozen at `969e2130ca9abb27c6ae5ad830923582f45b8a2f`.
- OP066 is integrated but MUST NOT execute until Human explicitly reports Executor capacity is available.
- PR #144 / proposed OP067 closed without merge; OP067 is non-authoritative.
- Do not launch/infer/accept T032/T021/T022 work while this lane is paused.

When Human later re-enables Executor capacity: execute OP066 first; only after verified `DONE` may a fresh T032 re-entry be prepared.

## Integrated Orchestrator architecture

### Capability model

- PR #145: `docs/CAPABILITY-SOURCE-CONTRACT.md`.
- D050 topology-neutral families: `consumer.lifecycle`, `consumer.skill-trust`, `source.maintenance`.
- capability/sub-capability IDs are routing units, not Skills.

### Focused context routing

- PR #146: `skill-capability` route.
- PR #147: `docs/CONFORMANCE-ORACLE-CONTRACT.md` + `conformance-authoring` route.
- PR #148: testing/eval docs defer D052 oracle lifecycle to the oracle contract instead of duplicating it.

D047 bootstrap reference/ratchet is unchanged. Under D049, live Context Map changes do not require incidental historical snapshot refresh.

### L007

Accidental direct `develop` write `dffe9cc18696ae04e57b9fef9a4b5b833f0c3435` is recorded in `docs/learning/L007-orchestrator-direct-develop-write.md`, state `CONTROL_PLANNED`.

Current write sequence is fail-closed:

```text
capture develop SHA -> create docs/* branch -> verify branch -> write -> exact review -> PR
```

Do not rewrite incident history.

## Current Orchestrator work — capability catalog

Branch: `docs/capability-catalog-v1`.

Adds `docs/CAPABILITY-CATALOG.md`, compacted from an initial 428-line draft to 162 lines before review.

Stable focused routes currently represented:

```text
consumer.lifecycle.installation
consumer.lifecycle.state
consumer.lifecycle.execution
consumer.lifecycle.mission
consumer.lifecycle.coexistence
consumer.skill-trust.discovery
consumer.skill-trust.audit
source.maintenance.orchestrator
source.maintenance.executor
source.maintenance.testing
source.maintenance.release
```

`source-maintainer-target` is explicitly prospective and does not claim T022 runtime completion.

`consumer.skill-trust` remains a distinct semantic/risk family, but a separate `External Skill Trust` release entrypoint is only the D050 G3 challenger until MG1/T023 evidence.

Context Map candidate change:

```text
skill-capability
    -> D050 + docs/CAPABILITY-CATALOG.md

capability-authoring
    -> D050 + docs/CAPABILITY-SOURCE-CONTRACT.md + docs/CAPABILITY-CATALOG.md
```

This is a structural routing improvement only; do not claim physical token/byte savings without RCAB measurement.

## MG1/T023 boundary

Current Orchestrator work MAY define topology-neutral capability metadata and reusable oracle structure.

It MUST NOT define/freeze T023 candidate descriptions, concrete corpus, expected outcomes, thresholds, holdout split, host/model matrix or winner before T022 acceptance and MG1.

## Next Action

1. Review/integrate `docs/capability-catalog-v1` only if Markdown-only, compact/topology-neutral, D047/D049 unchanged, and no claim that `source-maintainer-target` is implemented.
2. Then characterize the accepted/current Consumer Skill against the catalog: capability-to-entrypoint/reference mapping, duplicated routing/context, and candidate progressive-disclosure cuts. Characterization only; no topology selection and no Skill behavior change.
3. Continue Orchestrator-only work while Executor lane is paused.
4. T021 only after accepted/integrated T032; MG1/T023 only after T022; T026 only after its separate gate.

## Next Chat Minimum Load

After normal bootstrap:

- routine capability work: `skill-capability` route;
- capability model changes: `capability-authoring` route;
- oracle design: `conformance-authoring` route;
- D051 only for package/install semantics;
- OP066 only after Human re-enables Executor;
- task-specific T032/T021/T023 material only when its gate is active.

## Do Not

Do not wait for unseen Executor work; execute OP066 early; preauthorize T032 re-entry; accept rejected T032; resume T021 early; pre-register MG1/T023; retrofit D052 onto T032/T021; weaken D049/D047/T032-R1; treat capability count as Skill count; treat `source-maintainer-target` as implemented; require Skill-to-Skill invocation; introduce unapproved multi-agent product architecture; independently version generated Skills; violate D051; treat catalog/oracles/tests as Governance authority; claim RCAB savings without measurement; refresh historical snapshot incidentally; rewrite L007 history; write directly to `develop`/`main`; or launch T026 early.
