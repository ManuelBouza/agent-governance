# Execution Access Control Architecture

Status: ARCHITECTURE OVERVIEW  
Normative decisions:

- `docs/decisions/D033-execution-access-control-plane.md`
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md`

## Purpose

Agent Governance aims to let AI control the technical development cycle end-to-end without turning an open terminal, authenticated session, remote connection, cloud login, administrator-capable workstation or automation system into unlimited authority.

The model separates:

- **what the Human Owner authorizes**;
- **what reusable procedure defines safe execution**;
- **how the AI/platform adapter realizes that procedure**;
- **what the target platform actually permits**;
- **what evidence is retained for review/recovery**.

The Human approves meaningful effect/risk boundaries. The AI remains free to choose routine technical realization inside those boundaries.

## Core model

```text
Human intent / approved task
          │
          ▼
Execution Capability Envelope
          │
          ▼
       Runbook
   semantic operation
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

Two distinctions are fundamental:

```text
mechanism != authority
procedure semantics != terminal syntax
```

Having a shell, CLI, remote session, API credential or privileged identity available does not authorize every effect those mechanisms can produce.

Likewise, a runbook does not become Bash, PowerShell, `cmd`, SSH syntax or a provider-specific CLI transcript. Those are possible adapter realizations.

## D033: authorization by effect

D033 authorizes **target + effect + privilege + resource scope**, not executable names.

For material system access the Execution Capability Envelope can be understood as:

```text
WHO       actor/principal
WHERE     exact local/remote target
WHAT      permitted effects/resources
HOW HIGH  maximum privilege
AUTH      approved credential mechanism
NETWORK   permitted destinations/path
WHEN      task/time/operation lifetime
RECOVERY  rollback/recovery expectation
PROOF     evidence required afterward
```

### Approval modes

`ALLOW_TASK`

Routine effects already contained by an approved task, such as project inspection, task-owned source mutation, project-native verification and disposable synthetic state.

`ALLOW_EXPLICIT`

An operation is outside the routine baseline but a persisted contract/decision explicitly bounds target, effect and privilege. The AI may choose technical realization inside that boundary.

`REQUIRE_HUMAN`

Human approval is required for a coherent bounded high-impact operation. Default examples include production mutation, administrator/high-impact privilege, global system configuration, security/identity control changes, credential lifecycle changes, destructive actions, material migrations and uncertain targets/effects.

The approval is normally attached to the **operation/runbook stage**, not each mechanically required command.

`DENY`

Fail closed when target identity is unknown/mismatched, privilege is unbounded, credentials/security controls would be bypassed, access pivots outside the approved path, dynamically obtained execution cannot be bounded, or required evidence would be hidden.

## D034: runbook-first procedure orchestration

D034 adds the reusable procedure layer between authorization and platform syntax.

A runbook describes:

```text
purpose / outcome
        +
applicability / exclusions
        +
required capabilities / target class
        +
inputs (non-secret references)
        +
preconditions
        +
ordered semantic steps
        +
checkpoints / Human gates
        +
postconditions
        +
rollback / recovery
        +
evidence
```

The canonical runbook step describes the **required effect/state transition**, not one command interpreter.

For example, a semantic step may be:

```text
STEP: restart application service
PRE: target identity and health snapshot verified
EFFECT: service lifecycle mutation on named service only
POST: new process generation healthy + dependency checks pass
FAILURE: restore prior service state / stop and escalate
```

An adapter may implement that operation differently on different platforms without changing the runbook semantics.

## Runbook applicability

Runbooks are preferred for repeatable/material operational work and normally required for:

- production deploy/service changes;
- privileged operations;
- remote persistent system mutations;
- infrastructure/IAM/network/security-control work;
- credential lifecycle operations;
- persistent schema/data migrations;
- destructive/recovery-sensitive actions;
- multi-system sequencing;
- recurring maintenance with meaningful failure modes;
- recovery/failover/restore procedures.

A runbook is not required merely to execute every ordinary local development command. Source inspection, tests, linting or bounded task-local edits may remain directly governed by the Task Contract when no durable procedure is useful.

## Runbook reuse before creation

Agent Governance does not automatically create its own runbooks if the project already owns an adequate procedure.

```text
existing project-native runbook/workflow
          │
          ├─ adequate ──────────────► REUSE
          │
          ├─ needs Governance gate ─► ADAPT by reference
          │
          └─ conflicting ownership ─► CONFLICT / fail closed
```

Native procedures may live in repository documentation, deployment platforms, infrastructure workflows, operations systems, CI/CD pipelines or other project-owned tooling.

Do not copy/mirror them into duplicate Governance truth merely to call them runbooks.

## Runbook approval versus invocation authorization

These are different decisions.

```text
runbook is valid procedure
          ≠
this invocation is authorized now
```

Each material invocation binds actual inputs/target/context and then re-evaluates D033.

A production deployment runbook can be trusted as a procedure while every production invocation still requires Human approval.

A migration runbook can be valid but blocked because the connected database/account is not the authorized target.

## Terminal neutrality

Agent Governance treats the terminal/platform stack as replaceable adapters.

Distinguish:

```text
terminal / UI host
        ↓
command environment / shell
        ↓
native CLI / task runner
        ↓
remote transport / API / automation surface
        ↓
target system
```

Possible adapter families include, without preference or dependency:

- PowerShell and other Windows command environments;
- POSIX-style shells and other Unix-like command environments;
- `cmd`, Nushell or other interpreters;
- project-native task runners;
- cloud/database/cluster/deployment CLIs;
- APIs/SDKs;
- remote-management protocols/transports;
- CI/CD or orchestration systems;
- graphical/admin control surfaces when they are the project-native safe mechanism.

No terminal application, shell, OS, remote protocol, provider or executor product becomes Governance authority.

## Execution Adapter contract

The adapter translates a semantic runbook step into the available mechanism while preserving:

- exact target/resource identity;
- effect boundary;
- privilege/credential boundary;
- ordering and state transitions;
- preconditions/checkpoints;
- Human gates;
- success/failure semantics;
- rollback/recovery behavior;
- required audit evidence.

Different syntax is acceptable. Different semantics are not.

If an adapter cannot implement or verify a required semantic step safely, execution blocks rather than approximating it.

## Adapter selection

Prefer project-native capability rather than an Agent Governance OS/shell preference.

```text
existing project-native operation/workflow
        ↓
existing safe automation/runbook provider
        ↓
native CLI/API/management interface
        ↓
compatible command environment
        ↓
custom adapter only when justified
```

Choose among available adapters using material criteria such as least privilege, deterministic target selection, structured/verifiable output, idempotency, preview support, rollback, auditability and existing project ownership.

This does **not** imply that APIs are always superior to shells or that shells are always more portable than native automation. Capability and safety control selection.

## Local and remote boundaries

“Local” does not mean inherently trusted.

```text
repository worktree
      ↓ increasing blast radius
disposable test/eval state
      ↓
workstation user configuration
      ↓
local services/VMs/containers
      ↓
system/global configuration
      ↓
administrator/security controls
```

Remote resources should be identified by the dimensions material to their platform:

```text
environment (dev/stage/prod)
        +
provider/account/project/tenant
        +
host/cluster/service
        +
namespace/database/resource
        +
principal/role
```

Aliases/current-context names are convenience, not sufficient identity evidence when a targeting error is material.

## Privilege and credentials

Two independent questions remain:

```text
Can this identity authenticate?
              ≠
Is this runbook effect authorized?
```

Credentials remain external operational state. Runbooks reference the expected credential/identity class and target but do not contain secret values.

Privilege escalation is a distinct capability. Prefer the narrowest privilege that can perform the semantic runbook step rather than unrestricted elevated sessions.

## Child-process and adapter non-expansion

Authority may only narrow through execution indirection.

```text
Execution Capability Envelope
      └── Runbook
            └── Adapter
                  └── shell/CLI/API/remote operation
                        └── child/server-side effect
```

Every layer remains a subset of the original envelope.

A runbook or adapter cannot launder additional authority merely because its parent operation was allowed.

## Runbook lifecycle

A material invocation follows the conceptual sequence:

```text
SELECT RUNBOOK
   ↓
BIND INPUTS / TARGET
   ↓
PREFLIGHT CURRENT STATE
   ↓
AUTHORIZE AGAINST D033
   ↓
HUMAN GATE (only when required)
   ↓
EXECUTE SEMANTIC STEP THROUGH ADAPTER
   ↓
VERIFY CHECKPOINT
   ↓
next step ...
   ↓
VERIFY POSTCONDITIONS
   ↓
DONE
```

Failure routes:

```text
identity/authorization mismatch → BLOCKED
checkpoint failure              → STOP → rollback/recover or BLOCKED
material context/tool drift     → STALE → revalidate
Human denial                    → CANCEL/BLOCK under controlling lifecycle
```

## Idempotency and retries

Runbooks must not assume repeatability.

When material, each semantic step should define:

- whether repetition is safe;
- retry conditions/limits;
- partial-completion detection;
- concurrency constraints;
- server/target state checks before retry;
- compensation/rollback if the previous request may have succeeded despite client-side failure.

Postcondition inspection is generally more reliable than assuming a client exit code fully represents remote state.

## Preview/dry-run

When a platform offers a trustworthy plan/preview/dry-run that reduces risk, the runbook should use it where material.

A preview is evidence, not authorization, and does not eliminate the need to revalidate identity/context before the real mutation.

## Enforcement layers

For material risk, prefer real platform controls over prompt-only trust.

```text
Governance authorization + runbook
          │
          ▼
executor/automation permissions
          │
          ▼
platform-native identity / privilege / network / resource controls
          │
          ▼
actual resource
```

Possible adapters/enforcement providers vary by platform. Linux, Windows, SSH, IAM, database roles, orchestration platforms and other mechanisms are examples, not Governance dependencies.

## Audit model

Evidence is keyed to the **runbook invocation**, not merely a raw terminal transcript.

For material operations retain enough sanitized evidence to answer:

```text
What task/envelope authorized this?
Which runbook revision/procedure was used?
Which adapter/platform mechanism realized it?
What target/principal was actually bound?
Which semantic steps/checkpoints completed?
What final postconditions were observed?
Was rollback/recovery needed?
Did any unexpected gate/context deviation occur?
```

Raw shell/terminal logs may supplement evidence when useful and safe, but they are not the canonical operational record.

Do not persist credentials, raw secret-bearing environments or hidden reasoning.

## Relation to D032

Interaction complexity remains separate from engineering rigor.

A non-technical Human Owner can approve:

```text
Deploy the tested release to production. The procedure verifies the target first,
creates a recovery point, rolls out the new version, checks service health and
returns to the previous version if validation fails.
```

An operations expert may instead inspect target/principal identifiers, runbook revision, adapter, exact checkpoints, rollout strategy and recovery semantics.

Both represent the same governed execution procedure.

## Primary Solution Diagram

```text
Human intent / Task Contract
            │
            ▼
Execution Capability Envelope
            │
            ▼
        RUNBOOK
   ┌───────────────────────┐
   │ outcome / preconditions│
   │ target / capabilities  │
   │ semantic steps         │
   │ checkpoints / gates    │
   │ rollback / evidence    │
   └───────────┬───────────┘
               │
               ▼
       Execution Adapter
   ┌───────────┼───────────────┐
   ▼           ▼               ▼
command env  native runner  CLI/API/remote
   │           │               │
   └───────────┴──────┬────────┘
                      ▼
             Local/Remote System
                      │
                      ▼
             observable evidence
                      │
                      └──► continue / rollback / handoff
```

## Planned Core integration

D033 and D034 deliberately remain architecture decisions while T004 is already running.

The next dedicated execution-control increment after T004 should integrate them together through the smallest coherent Core change, including:

- `governance-core/EXECUTION-CONTROL.md` or the final focused equivalent;
- progressive routing from `GOVERNANCE.md`;
- linkage from `EXECUTION.md`;
- Task Contract support for Execution Capability Envelopes and material runbook references;
- runbook invocation/preflight/Human-gate rules;
- terminal-neutral Execution Adapter semantics;
- handoff evidence keyed to invocation/runbook rather than command transcripts;
- deterministic authorization/runbook tests;
- synthetic tests spanning materially different adapter families;
- later dynamic security/adapter evals where deterministic evidence is insufficient.

Until that integration is accepted, D033 + D034 are durable architecture constraints and future-work requirements; they do not retroactively rewrite T004.