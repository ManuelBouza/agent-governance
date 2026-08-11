# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O021  
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

T004 remains governed by its existing contract. D033/D034 architecture work MUST NOT retroactively broaden or alter its running execution semantics.

## Accepted Execution-Control Architecture

The Human Owner requires the AI to control the technical development/operations cycle while strict policy determines what local/remote effects are authorized.

The accepted architecture is now split deliberately into two complementary decisions:

- `docs/decisions/D033-execution-access-control-plane.md` — authorization by actor/target/effect/privilege/credential/resource scope;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — reusable runbook procedures and terminal/platform-neutral execution adapters.

Consolidated overview:

`docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`

D033/D034 are `ACCEPTED` architecture but are not yet integrated into Governance Core/protocol.

## Core Execution-Control Model

```text
Human intent / approved task
          │
          ▼
Execution Capability Envelope
          │
          ▼
       Runbook
 semantic procedure
          │
          ▼
   Execution Adapter
  ┌───────┼─────────┬────────────┐
  ▼       ▼         ▼            ▼
 shell   native    API/SDK     remote/
        CLI/runner             automation
  └───────┴─────────┴──────┬─────┘
                           ▼
                   target resource
                           │
                           ▼
                 sanitized evidence
                           │
                           ▼
              continue / rollback / review
```

Normative invariants:

```text
transport or credential possession != execution authority
procedure semantics != terminal syntax
approved runbook != approved invocation
```

## D033 — Execution Capability Envelope

For material process/system access, authorization is defined by the applicable subset of:

- actor/execution role;
- exact target/environment/account/resource identity;
- effect classes;
- resource scope;
- privilege ceiling;
- credential source/use;
- network destinations/path;
- task/time/operation lifetime;
- rollback/recovery expectation;
- approval mode;
- audit/evidence requirement.

Authorization is effect-oriented rather than executable-name-oriented.

### Approval modes

- `ALLOW_TASK` — routine effects already inside the approved task boundary.
- `ALLOW_EXPLICIT` — a persisted decision/contract explicitly bounds the non-baseline effect.
- `REQUIRE_HUMAN` — Human approval required for a bounded high-impact operation/stage.
- `DENY` — fail closed under the current authority.

Human approval normally applies to a coherent bounded operation/runbook stage rather than every terminal command.

Child/nested execution may inherit only a subset of the parent envelope.

## D034 — Runbook-first Procedure Layer

Runbooks become the preferred durable operational procedure for repeatable/material execution.

A runbook describes the applicable subset of:

- purpose/outcome;
- applicability/exclusions;
- required capability/target/privilege class;
- non-secret inputs;
- preconditions;
- ordered **semantic steps**;
- checkpoints and Human gates;
- postconditions;
- rollback/recovery;
- evidence requirements.

The canonical semantic step states the required effect/state transition, not a Bash/PowerShell/provider-specific command.

A durable runbook is required by default for material operations such as:

- production deploy/service mutation;
- privileged execution;
- remote persistent system mutation;
- infrastructure/IAM/network/security-control changes;
- credential lifecycle operations;
- persistent schema/data migrations;
- destructive/recovery-sensitive actions;
- multi-system sequencing;
- recurring material maintenance;
- recovery/failover/restore procedures.

Ordinary low-risk local development commands do not require a dedicated runbook when the Task Contract already bounds them adequately.

## Runbook Reuse / Coexistence

Reuse project-native operational procedures before creating Governance-owned runbooks.

```text
native runbook/workflow
   ├─ adequate             -> REUSE
   ├─ needs Governance gate -> ADAPT by reference
   └─ conflicting ownership -> CONFLICT / fail closed
```

Do not copy/mirror native runbooks into duplicate Governance truth merely to rename them.

Runbook procedural validity does not authorize an invocation. Before each material invocation, bind the real target/context/inputs and re-evaluate D033.

## Terminal / Platform Neutrality

Agent Governance MUST NOT center execution methodology on Linux, POSIX shells, PowerShell, Windows, SSH or any other terminal/platform family.

These are replaceable adapter layers:

- terminal/UI host;
- command environment/shell;
- native CLI/task runner;
- remote transport;
- API/SDK;
- automation/orchestration system;
- executor host.

Possible adapters include PowerShell, POSIX-style shells, `cmd`, Nushell, project task runners, cloud/database/cluster/deployment CLIs, APIs, remote-management systems, CI/CD/orchestration providers and safe graphical/admin surfaces.

None is Governance authority or a required Core dependency.

An Execution Adapter must preserve:

- target/effect/privilege boundaries;
- semantic ordering/state transitions;
- checkpoints/Human gates;
- success/failure semantics;
- rollback/recovery;
- audit evidence.

Different command syntax is acceptable. Different semantic effects are not.

## Runbook Invocation Lifecycle

Conceptual sequence:

```text
SELECT RUNBOOK
 -> BIND INPUTS/TARGET
 -> PREFLIGHT CURRENT STATE
 -> AUTHORIZE AGAINST D033
 -> HUMAN GATE if required
 -> EXECUTE semantic step through adapter
 -> VERIFY checkpoint
 -> ...
 -> VERIFY postconditions
 -> DONE
```

Failure behavior:

- identity/authorization mismatch -> `BLOCKED`;
- checkpoint failure -> stop and rollback/recover or block;
- material tool/platform/context drift -> stale/revalidate;
- Human denial -> cancel/block under the controlling lifecycle.

Material runbooks must address idempotency/retries/concurrency where repeated/partial execution could cause harm.

## Execution Evidence

Material evidence should be keyed to the **runbook invocation**, not only raw command transcripts.

Capture the applicable subset of:

- task/envelope authorization reference;
- runbook identity/revision;
- adapter identity/version when material;
- bound non-secret inputs;
- actual target/principal/environment;
- semantic steps/checkpoints completed;
- postcondition result;
- rollback/recovery result;
- unexpected gate/context deviation.

Raw terminal logs are optional supplemental evidence and must not become the canonical record or persist credentials/hidden reasoning.

## Native Enforcement

For material risk, prefer actual platform controls over prompt-only trust.

Governance defines authorization/procedure semantics; project/platform-native IAM, privilege, network, resource, sandbox, remote-management and audit controls enforce them where practical.

No single OS/security/terminal mechanism is universal.

## T004 State

T004 remains the current executable frontier and is unchanged by D033/D034.

Its child-eval isolation is one narrow example of capability bounding but does not constitute general execution-control implementation.

T004 semantic grading remains `PENDING_CHATGPT` until its final handoff/results/transcripts are remotely reviewed.

## Planned Core-Integration Frontier

After T004 PD5, the leading planned architecture increment is the smallest coherent integration of **D033 + D034 together**, tentatively T005.

It should be diagrammed/contracted before execution and should cover the applicable subset of:

- focused execution-control Core module;
- progressive routing from `GOVERNANCE.md`;
- linkage from `EXECUTION.md` so READY does not mean unlimited system authority;
- Task Contract support for Execution Capability Envelopes;
- Task Contract/native-artifact support for material runbook references;
- runbook selection/binding/preflight/Human-gate semantics;
- terminal-neutral Execution Adapter contract;
- handoff evidence keyed by runbook invocation;
- deterministic authorization/runbook/version/module tests;
- synthetic adapter fixtures spanning materially different terminal/platform families;
- dynamic security/adapter tests only where deterministic verification is insufficient.

Do not implement a POSIX/Linux-only execution-control model.

## Active Remote Artifacts

- canonical `develop` before D034 planning: `c431ce4f475521f54224b99806ec25bb49b8c153`;
- T004 Task Contract: `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
- D032 decision: `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`;
- D033 decision: `docs/decisions/D033-execution-access-control-plane.md`;
- D034 decision: `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`;
- execution-control overview: `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`.

## Open Questions or Blockers

No known D033/D034 architecture blocker remains.

T004 still requires executor return and PD5.

The source product remains not stable/release-ready. D033/D034 Core integration, broader behavioral/security evals, property/state-machine coverage, Skill gates and other release gates remain incomplete.

## Next Action

1. Review and integrate the D034 Markdown planning change if its diff is limited to D034 + execution overview + this checkpoint.
2. Do not alter the running T004 contract.
3. When T004 returns, perform remote PD5 over its branch/handoff/results/transcripts.
4. After T004 is resolved, design the D033+D034 Core-integration increment with a fresh Primary Solution Diagram and quality/security triage.
5. Ensure that increment includes materially different synthetic adapter families so terminal neutrality becomes mechanically testable rather than documentation-only.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T004 is active/returned, load `docs/tasks/T004-d032-agent-facing-capability-eval.md` and its handoff/results as needed;
2. for execution-control work, load D033 + D034;
3. load `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md` when a consolidated view is useful;
4. load D032/`QUALITY.md` only as needed for diagram/quality readiness or T004 semantic review.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not retroactively broaden/rewrite T004 because D033/D034 were accepted while it was running.
- Do not interpret terminal/credential availability as authorization.
- Do not treat local execution as inherently trusted compared with remote execution.
- Do not authorize by executable name alone when target/effect/privilege changes meaning.
- Do not treat runbook approval as invocation authorization.
- Do not let runbooks/adapters/child processes expand the parent capability envelope.
- Do not make Bash/POSIX/Linux, PowerShell/Windows, SSH, a cloud provider or another execution mechanism a Governance Core dependency.
- Do not duplicate adequate project-native runbooks/workflows.
- Do not weaken native IAM/privilege/security/audit controls to simplify automation.
- Do not commit credentials, secret values, raw secret-bearing environments or hidden reasoning.
- Do not update Core/protocol for D033/D034 until a separate integrated Task Contract can align deterministic verification.
- Do not declare the source product stable/release-ready from D033/D034 or T004 alone.
