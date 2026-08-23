# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O143  
Canonical-Branch: `develop`  
Current-Work-Unit: D054 Executor-owned operation resolution + T035 runbook-recipe readiness gate under review/integration  
Chat-Closure: KEEP_CURRENT_CHAT

## Human Owner Direction

On 2026-08-23 the Human Owner clarified that routine technical command/API mechanics are the responsibility of the Agente de IA Ejecutor, not a sequence of CLI/PowerShell/Bash/API commands handed to the Human for copy/paste.

The required product behavior is:

```text
semantic operation / authorized effect
    -> check applicable runbook
    -> check compatible verified adapter recipe
    -> if absent/stale: consult authoritative tool/API documentation
    -> build bounded candidate
    -> preflight/authorize/execute
    -> verify semantic postcondition
    -> persist as verified reusable recipe when eligible
```

This applies broadly to Git, uv, PowerShell, Bash, AWS/cloud CLIs, APIs/SDKs, SSH/remote-management and equivalent adapters.

## Existing Authority Confirmed

The request is a refinement, not a new architecture from zero.

- D033 already makes execution authorization target/effect/resource/privilege/credential/network oriented rather than command-name oriented and allows the Executor to select exact technical commands inside an approved envelope.
- D034 already defines runbook-first, terminal-neutral procedure semantics and Execution Adapters for shell/CLI/API/remote mechanisms.
- `governance-core/EXECUTION-CONTROL.md` already defines the Execution Capability Envelope, actual-target verification, least privilege, Human gates, runbook lifecycle, adapter equivalence, preview/dry-run, postconditions, rollback and sanitized evidence.
- D041 already gives Executor implementation-process/tool autonomy inside D053 stages 5-6.
- D039 already provides an evidence-driven learning pattern, but not a native operation-recipe registry.

The missing pieces were explicit Executor ownership of routine execution mechanics, mandatory recipe lookup before syntax discovery, official/version-specific documentation fallback, and evidence-gated durable recipe promotion/staleness.

## D054 / T035 Design

The current gate branch adds:

- `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md` — accepted Human-directed architecture;
- `docs/RUNBOOK-OPERATION-RESOLUTION.md` — staged exact recipe/persistence/validation contract;
- `governance-skill/assets/RUNBOOK.template.md` — Orchestrator-owned semantic runbook template;
- `docs/runbooks/RB001-source-executor-checkout-bootstrap.md` — first reusable source-maintainer semantic runbook for safe Executor checkout/toolchain bootstrap;
- `docs/tasks/T035-runbook-operation-resolution-readiness.md` — ASSURED/mixed executable readiness task, blocked on T034 acceptance;
- `tests/test_t035_runbook_operation_resolution_conformance.py` — Orchestrator-owned D052 oracle `T035-D054-v1`;
- `AGENTS.md` refinement assigning Executor-side CLI/API/shell/remote mechanics explicitly to the Executor while preserving Human/Orchestrator semantic authority;
- L007 recurrence evidence for an Orchestrator direct-`develop` write incident encountered during this gate preparation.

D054 preserves D034's key distinction:

```text
semantic runbook != raw command transcript
verified recipe = adapter-specific technical realization/evidence
```

Native fallback persistence selected by the staged Design is:

```text
.agent-coordination/runbooks/
    RUNBOOK.template.md
    <runbook-id>.md
    recipes/
        RUNBOOK-RECIPE.template.json
        <recipe-id>.json
```

Semantic runbook meaning remains Human/Strategy/project-native authority. Recipe JSON remains Executor-owned technical realization/evidence and cannot grant execution authority.

## Research Basis

The D054 design was checked against current official sources:

- OpenAI: safe agent execution uses bounded sandboxes, approvals, network policy, differentiated low-/high-risk command rules, managed configuration and agent-native telemetry.
- NIST: least privilege applies to processes acting for users; Zero Trust avoids implicit trust and uses least-privilege per-request decisions.
- AWS Systems Manager: runbooks encode ordered automation actions/inputs/outputs and may include approval pauses; AWS CLI provides built-in help and official API references.
- PowerShell: `Get-Help`/online help plus `ShouldProcess`, `-WhatIf` and `-Confirm` provide official discovery/preview/confirmation mechanisms.
- Azure Automation: runbooks should be modular/restartable, track progress and guard concurrent execution.
- Git/Bash/OpenSSH: official version/help/manual surfaces exist; OpenSSH strict host-key checking supports fail-closed remote identity rather than silent bypass.

External sources are research evidence, not Governance authority.

## D040 Staging / Sequence

D054 Consumer activation follows D040 atomic migration rather than editing routed Core while executable readiness is absent.

```text
Phase A now:
D054 design + T035 gate
        |
        v
T034 first: materialize already-frozen Protocol 1.14 native SDD gap
        |
        v
T034 accepted/integrated -> canonical green
        |
        v
T035: add runbook/recipe footprint + validation readiness
        |
        v
T035 accepted/integrated -> canonical green
        |
        v
Phase B Orchestrator Markdown activation:
EXECUTION-CONTROL / PROTOCOL / CONTEXT / GOVERNANCE + Consumer Skill
```

T034 is **not cancelled or redefined**. Its launch is paused only until the current D054/T035 planning gate is integrated so the interaction/command-ownership rule is durable.

T035 is `BLOCKED` until T034 is accepted/integrated. Its oracle may be frozen before then.

## Bootstrap-Period Execution Rule

Until T035 native recipe persistence exists:

- the Executor owns CLI/API/PowerShell/Bash/remote mechanics;
- the Human is not asked to run routine source-maintainer commands;
- existing D033/D034 authorization/runbook controls remain active;
- use `docs/runbooks/RB001-source-executor-checkout-bootstrap.md` for source checkout/toolchain bootstrap once the gate is integrated;
- if a compatible reusable recipe does not yet exist, the Executor resolves syntax from project-native or installed/version-specific help and official vendor/API documentation;
- model memory/community examples/chat snippets are not sole execution authority;
- newly resolved successful operations are provisional handoff evidence until T035 can revalidate/promote them into the native recipe store.

## L007 Recurrence / Containment

During preparation of this gate, the Orchestrator accidentally issued two GitHub contents writes directly to `develop`, creating `noop` and `noop2` in commits:

- `a09e1d8cc84e0591ca2cd0401b30cd69844914ba`;
- `87319e9167c60d64a2f16f0a79367000c048bfb9`.

No history rewrite/force-reset was used. PR #188 removed only those unintended files and restored the intended tree as `3694cd7ec562f2baa127965f4269a609957f4783`.

`docs/learning/L007-orchestrator-direct-develop-write.md` is updated on the current gate branch with the recurrence and stronger mechanical-control requirement. L007 remains `CONTROL_PLANNED`, not `VERIFIED`.

## Current Remote State

```text
last verified develop          = 3694cd7ec562f2baa127965f4269a609957f4783
containment PR                  = #188 — MERGED
D054/T035 gate branch           = test/t035-operation-resolution-gate
D054 decision                   = docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md
operation-resolution contract   = docs/RUNBOOK-OPERATION-RESOLUTION.md
source bootstrap runbook        = docs/runbooks/RB001-source-executor-checkout-bootstrap.md
T035 task                       = docs/tasks/T035-runbook-operation-resolution-readiness.md
T035 status                     = BLOCKED on T034 acceptance
T035 oracle                     = tests/test_t035_runbook_operation_resolution_conformance.py
T035 oracle revision            = T035-D054-v1
T035 oracle freeze              = DRAFT until gate integration

T034 status                     = READY — LAUNCH PAUSED until D054 gate integration
T034 task                       = docs/tasks/T034-native-sdd-executable-materialization.md
T034 oracle                     = tests/test_t034_native_sdd_conformance.py
T034 oracle revision            = T034-A2-v1 — FROZEN
T034 implementation branch     = feat/t034-native-sdd-executable-materialization

T021/T022                       = PAUSED
```

Resolve current branch/PR head and current canonical `develop` again immediately before integration or Executor launch.

## T035 Readiness Boundary

T035 will prepare, but not activate, Consumer D054 semantics.

Required:

- add native `runbooks/` + `runbooks/recipes/` bootstrap skeleton;
- copy the Orchestrator-owned semantic runbook template;
- add Executor-owned JSON recipe template according to the frozen contract;
- validate recipe identity/status/adapter/binding/effects/provenance/postconditions/verification/staleness;
- require semantic runbook binding for the six D054 material effect classes;
- reject duplicate/ambiguous exact verified bindings and unsafe registry paths;
- preserve package/source independence and stable CLI v1 surface.

Not authorized in T035:

- routed Core/protocol activation;
- new top-level CLI command;
- universal command wrapper/daemon;
- execution of recipe content during validation;
- fuzzy/model-based trusted matching;
- secrets in recipe records;
- T021/T022/T034 semantic changes.

## Next Action

1. Review the complete `test/t035-operation-resolution-gate` diff against D033, D034, D040, D041, D052, D053 and the Human Owner instruction.
2. Confirm the only non-Markdown change in the gate is the Orchestrator-owned D052 T035 conformance oracle.
3. Open/integrate the gate to `develop` only if D054, the staged contract, RB001, T035 and the oracle converge.
4. Reverify canonical `develop` and refresh this checkpoint after integration.
5. Launch T034 through the Executor — **not through Human-run CLI commands** — using the current canonical Task Contract prompt plus current `AGENTS.md`; bootstrap follows RB001/D054 and unknown syntax uses authoritative documentation.
6. Perform remote T034 Converge/Accept; integrate it if accepted.
7. Only after T034 acceptance/integration and a green current baseline may T035 launch.
8. Do not resume T021/T022 automatically.

## Next Chat Minimum Load

Until this gate is integrated, load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint;
- D054;
- `docs/RUNBOOK-OPERATION-RESOLUTION.md`;
- T035 + its oracle;
- the gate PR/diff when opened;
- D033/D034/D040 only when resolving a concrete conflict.

After gate integration and before T034 execution, load only current `develop`, checkpoint, T034/frozen oracle and RB001/D054 execution boundary. Do not reconstruct A1/A2 from chat history.

## Do Not Load Or Do

Do not hand routine CLI/API/PowerShell/Bash command sequences to the Human as the default execution path; do not let recipe syntax become execution authority; do not store secrets in recipes; do not guess unknown commands from model memory; do not execute stale/revoked recipes; do not bypass target/identity/privilege/credential/network checks; do not disable TLS/host-key/security controls for convenience; do not activate D054 routed Consumer Core before T035 readiness; do not absorb T035 into T034; do not resume T021/T022; do not write directly to `main`/`develop`; and do not treat the repaired L007 tree as proof that the direct-write control is verified.