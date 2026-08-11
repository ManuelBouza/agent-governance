# D034 — Runbook-first terminal-neutral execution orchestration

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

D033 establishes the Execution Access Control Plane and correctly authorizes execution by target, effect, privilege, credential and resource scope rather than by command name.

A second layer is still needed: a reusable, auditable description of **how** an authorized operational change is performed without binding Agent Governance to one operating system, shell, terminal emulator, CLI syntax or remote transport.

Without that layer, execution guidance tends to collapse into examples such as Bash commands, PowerShell commands, SSH snippets or provider-specific CLIs. That is insufficient for a portable source product because:

- the same operation can be expressed through PowerShell, a POSIX shell, `cmd`, another command environment, a native CLI, an API, a remote session, a management console or an automation provider;
- terminal applications and shells are not equivalent concepts and neither should become Governance authority;
- exact command syntax can vary while the intended target/effect/preconditions/postconditions remain identical;
- repeated operational work needs a durable procedure with checkpoints, rollback and evidence rather than rediscovering a safe sequence in every session;
- an approved procedure still must not bypass D033 authorization for a particular invocation.

The missing abstraction is therefore a **runbook-first execution procedure layer** between authorization and platform-specific execution.

## Decision

Agent Governance SHALL use **runbooks** as the preferred durable execution procedure for repeatable or material system operations, while remaining **terminal-neutral and platform-neutral**.

The normative separation is:

```text
Human intent / Task Contract
        -> Execution Capability Envelope (D033: may this effect occur?)
        -> Runbook (D034: what procedure and checkpoints achieve it?)
        -> Execution Adapter (how is that procedure expressed here?)
        -> terminal / CLI / API / remote transport / automation surface
        -> target system
        -> evidence / recovery / handoff
```

Core invariant:

```text
procedure semantics != terminal syntax
```

A terminal, shell, CLI, API, SDK, remote transport or automation host is an execution adapter. It MUST NOT define the Governance meaning of the operation.

D033 remains authoritative for execution authorization. D034 defines procedure orchestration and portability.

## What a runbook is

A runbook is a durable operational procedure that describes the intended outcome, required conditions, authorized effects, ordered semantic steps, verification points, failure handling, rollback/recovery and evidence expectations.

A runbook is **not** merely:

- a shell script;
- a pasted command list;
- a provider-specific CLI transcript;
- an agent prompt;
- a replacement for authorization;
- proof that a target is safe to mutate;
- authority to use credentials or privilege.

A runbook MAY contain or reference adapter-specific command recipes, scripts, API operations or tooling, but those are implementations of the procedure rather than the procedure's canonical semantics.

## Runbook-first applicability

A durable runbook SHOULD be used when an operation is repeatable, operationally material, risky, cross-system or recovery-sensitive.

A runbook is REQUIRED by default when the operation materially includes one or more of:

- production deployment or production service mutation;
- privileged/administrator execution;
- remote system mutation beyond disposable test infrastructure;
- infrastructure/IAM/network/security-control changes;
- credential rotation/revocation or security-sensitive secret lifecycle work;
- persistent data/schema migration;
- destructive or difficult-to-reverse effects;
- multi-system sequencing where ordering matters;
- operational recovery/failover/restore procedures;
- recurring maintenance with meaningful failure modes;
- an operation whose safe execution depends on checkpoints or rollback.

A dedicated runbook is not required for every low-risk local command. Ordinary task-local inspection, compilation, tests, linting and bounded source edits may remain directly described by the Task Contract when a reusable operational procedure adds no value.

## Runbook reuse and coexistence

Use capability-first/reuse-before-create semantics from `COEXISTENCE.md`.

When a project already has an adequate native operational procedure in an owned system such as repository documentation, an operations platform, deployment system, infrastructure workflow or incident-management system:

- `REUSE` it when it already satisfies the needed procedure/evidence contract;
- `ADAPT` it by reference when Governance-specific authorization/checkpoints must be layered around it;
- do not mirror/copy it into a duplicate Governance source of truth merely to rename it a runbook;
- treat managed external runbook/workflow surfaces according to their existing ownership and collision policy;
- fail closed if two systems claim conflicting operational authority for the same effect.

Agent Governance creates a Governance-owned runbook only when no adequate native procedure exists or when the procedure is itself a Governance-owned capability.

## Runbook semantic contract

A runbook must make the following material information determinable without depending on one shell syntax.

### Identity and intent

- stable runbook identifier/name;
- purpose / intended operational outcome;
- applicability and exclusions;
- owning system/team/artifact boundary;
- revision/version or immutable reference when the host system supports one.

### Authorization binding

- required D033 effect classes;
- expected target class/identity constraints;
- required privilege ceiling;
- credential/authentication class without storing secret values;
- network/remote-access assumptions;
- expected approval mode or Human gate locations.

The runbook does not grant these permissions. It declares what its safe invocation requires.

### Inputs

- required parameters and types/constraints;
- resource identifiers;
- environment selection;
- references to approved secrets/credentials rather than embedded values;
- optional execution/adaptation parameters that do not change semantic intent.

### Preconditions

- target identity checks;
- current-state checks;
- dependency/service/tool availability;
- backups/snapshots/readiness conditions when required;
- authorization validity;
- concurrency/maintenance-window conditions when material;
- invariant checks that must hold before mutation.

### Semantic steps

Each material step should define the applicable subset of:

- step identifier and purpose;
- required effect/capability;
- input/resource scope;
- expected state transition or observable effect;
- pre-step assertion;
- post-step assertion;
- evidence to capture;
- retry/idempotency behavior when applicable;
- failure route;
- rollback/compensation relationship.

The canonical step should describe **what effect is required**, not assume one command interpreter.

### Checkpoints and Human gates

- points that require verified state before continuation;
- points that invalidate execution on mismatch;
- D033 `REQUIRE_HUMAN` gates when the operation/risk boundary requires them;
- conditions under which prior Human approval becomes stale and must be refreshed.

A Human gate normally approves the bounded runbook stage/operation, not every adapter command generated beneath it.

### Verification and postconditions

- final expected state;
- service/data/health/integrity assertions;
- acceptance evidence;
- absence of unexpected side effects where material;
- required audit references.

### Recovery

- rollback or compensation procedure;
- stop conditions where rollback is unsafe or impossible;
- recovery prerequisites;
- evidence required after rollback/recovery;
- escalation route when the system cannot be returned to an acceptable state.

## Runbook invocation is not authorization

A runbook can be procedurally valid while a particular invocation is unauthorized.

Before each material invocation:

1. resolve the actual target/context;
2. bind the runbook inputs;
3. evaluate the required D033 Execution Capability Envelope;
4. verify approval mode and Human gates;
5. only then execute the bound runbook.

Normative invariant:

```text
approved runbook != approved invocation
```

Examples:

- a deployment runbook may be reusable for development and production, while production still requires `REQUIRE_HUMAN`;
- a database-migration runbook may be valid but blocked because the connected database identity does not match the approved target;
- a credential-rotation runbook may be valid but unusable by an executor whose current credential cannot satisfy the required privilege boundary.

## Terminal neutrality

Agent Governance MUST NOT encode execution semantics around a particular terminal application or command interpreter.

Distinguish these concepts:

- **terminal/user interface host** — an application/window/session hosting command interaction;
- **command environment/shell** — PowerShell, POSIX-compatible shells, `cmd`, Nushell or another interpreter;
- **native CLI** — project/cloud/database/cluster/deployment tooling;
- **remote transport** — SSH-like sessions, remote-management protocols, provider consoles or equivalent;
- **API/SDK/automation surface** — direct service APIs, orchestration engines, CI/CD systems or management automation;
- **executor host** — OpenCode, Codex, Claude Code or another compatible agent product.

None of these layers is Governance authority.

The same semantic runbook may be realized through different combinations of these layers as long as the adapter preserves the same target/effect/privilege/evidence contract.

## Execution Adapter contract

An Execution Adapter translates a runbook's semantic step into the available platform mechanism.

An adapter may target, for example:

- PowerShell or another Windows command environment;
- a POSIX-style shell on Unix-like platforms;
- a project-native task runner;
- a cloud/cluster/database/deployment CLI;
- an authenticated API;
- a remote management transport;
- an automation/orchestration system;
- a graphical/admin control surface when that is the only safe project-native route.

Adapters MUST:

- preserve runbook intent and ordering;
- preserve D033 target/effect/privilege boundaries;
- map preconditions/postconditions to observable checks;
- preserve stop/Human-gate behavior;
- avoid silently broadening credential/network/resource scope;
- produce the evidence required by the runbook;
- declare/raise unsupported semantic steps rather than approximating them unsafely.

An adapter MUST NOT rewrite a semantic operation merely because a different command syntax is more convenient.

## Adapter selection

Select an adapter based on project/platform-native capability rather than an OS preference imposed by Agent Governance.

Preferred order:

```text
existing project-native operational mechanism
        -> existing safe automation/runbook provider
        -> native CLI/API/management interface
        -> compatible shell/command environment
        -> custom adapter only when justified
```

This ordering is capability-oriented, not a requirement that APIs are always safer than shells or vice versa.

If multiple adapters are available, prefer the one that best satisfies:

- least privilege;
- deterministic target selection;
- preview/dry-run support when meaningful;
- structured/verifiable output;
- idempotency/retry behavior;
- rollback/recovery support;
- auditability;
- existing project ownership/support;
- portability needs of the project.

## Adapter equivalence and drift

Two adapters are equivalent for a runbook only when they preserve the material procedure contract.

Equivalent adapters must produce materially equivalent:

- target selection;
- allowed effects;
- privilege/credential requirements;
- ordering/state transitions;
- checkpoints;
- success/failure semantics;
- rollback/recovery behavior;
- audit evidence.

A different command sequence is acceptable. A different effect boundary is not.

Material adapter/tool/platform drift can invalidate prior runbook verification. Examples include:

- CLI/API behavior changes;
- default target/context changes;
- altered authentication/privilege behavior;
- removed/changed dry-run semantics;
- changed exit/status semantics;
- changed rollback behavior;
- platform changes that make a precondition/postcondition unverifiable.

When such drift is detected, mark the affected invocation/runbook adapter path stale until revalidated.

## Runbook execution lifecycle

A material runbook invocation follows this conceptual state flow:

```text
SELECT
  -> BIND_INPUTS
  -> PREFLIGHT
  -> AUTHORIZE
  -> READY
  -> EXECUTE_STEP
  -> VERIFY_CHECKPOINT
  -> EXECUTE_STEP ...
  -> VERIFY_POSTCONDITIONS
  -> DONE
```

Failure paths:

```text
PREFLIGHT/AUTHORIZE mismatch -> BLOCKED
step/checkpoint failure      -> STOP -> RECOVER/ROLLBACK or BLOCKED
material context drift       -> authorization/runbook becomes STALE -> BLOCKED
Human denial                 -> CANCELLED/BLOCKED under controlling lifecycle
```

The exact persisted state machine is deferred to the future Core-integration task; this decision defines the required semantics.

## Idempotency, retries and concurrency

A runbook must not assume that repeating an operation is safe.

When material:

- state whether a step is idempotent;
- define retry conditions and limits semantically;
- detect partial completion before retrying;
- guard against concurrent runs when concurrency could corrupt state;
- avoid executing a destructive step twice because an adapter lost connection after the remote effect occurred;
- prefer postcondition/state inspection over relying solely on a client-side exit code.

## Dry-run / plan / preview

Where a platform provides a trustworthy preview/plan/dry-run mode, a runbook SHOULD use it when it materially reduces execution risk.

A preview is:

- preflight evidence;
- not Human approval;
- not proof that the later mutation will target the same resource unless identity/context is revalidated;
- not a substitute for rollback where rollback remains necessary.

## Runbook evidence

Persist enough sanitized evidence to reconstruct the invocation without depending on the exact terminal transcript.

Material runbook evidence should identify the applicable subset of:

- runbook identifier/revision;
- invocation/task reference;
- adapter identity/version where relevant;
- bound non-secret inputs;
- actual target/principal/environment identity;
- D033 authorization/approval reference;
- steps attempted/completed;
- checkpoint results;
- final postcondition result;
- rollback/recovery result;
- unexpected adapter/platform prompts or deviations;
- sanitized native operation identifiers/log references when useful.

Do not persist credentials, secret values, raw secret-bearing environments or private reasoning.

Raw terminal transcripts are optional evidence only when they add review value and can be safely sanitized. They are not the canonical runbook record.

## Runbook revision and trust

Runbooks are operational artifacts and can drift.

A material change to any of the following requires re-review/revalidation before relying on prior procedural trust:

- target/effect scope;
- privilege/credential requirement;
- step ordering;
- state-transition semantics;
- Human gates;
- destructive behavior;
- rollback/recovery semantics;
- adapter requirements;
- security/integrity checkpoints.

Cosmetic wording or equivalent adapter syntax changes need not create a new Governance decision when semantic behavior is unchanged, but artifact revision/history should remain auditable in the owning system.

## Security relationship

D034 strengthens D033 by moving sensitive execution away from ad-hoc command generation toward a preconditioned, checkpointed and recoverable procedure.

Security properties include:

- authorization checked before runbook execution;
- least-privilege adapter selection;
- explicit target binding;
- no authority expansion through adapter indirection;
- Human gates for D033-sensitive stages;
- secret references rather than embedded credentials;
- checkpoint verification before irreversible progression;
- bounded failure/recovery paths;
- auditable invocation evidence.

A runbook is not automatically safe because it is documented. Its semantics, adapter and invocation must all remain within current Governance authorization and project-native security controls.

## Interaction relationship

D032 interaction adaptation applies to runbooks.

The Human Owner normally sees:

- operation purpose;
- target;
- material risk/impact;
- required approval decision;
- expected verification/rollback.

The Human does not need to see platform command syntax unless:

- they request it;
- their current interaction register is code/operations-native;
- exact syntax materially affects risk or decision quality.

The Implementation Agent/execution adapter may operate at a much more technical level than the Human-facing representation without changing the underlying runbook semantics.

## Primary Solution Diagram

Dominant question: how a reusable operational procedure is translated into platform-specific execution without changing authorization or semantics.

Preferred primary view: flow/dependency diagram.

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
PowerShell   shell/runner    CLI/API/remote
   │           │               │
   └───────────┴──────┬────────┘
                      ▼
             Local/Remote System
                      │
                      ▼
             observable evidence
                      │
                      └──► resume / rollback / handoff
```

The labels are examples of adapter families, not required products or operating systems.

## Relationship to D033

D033 answers:

```text
Is this actor allowed to cause this effect on this target with this privilege now?
```

D034 answers:

```text
What reusable procedure, checkpoints and recovery semantics safely produce that effect, and how is it adapted to the available platform?
```

Neither subsumes the other.

## Planned Core integration

Like D033, D034 is accepted architecture and MUST NOT retroactively change the already-running T004 contract.

The post-T004 execution-control increment should integrate D033 and D034 together rather than creating a terminal-specific implementation.

The future Core/contract work should include the smallest coherent support for:

- an execution-control Core module;
- Execution Capability Envelopes;
- runbook reference/reuse semantics;
- runbook invocation/preflight/Human-gate rules;
- terminal-neutral Execution Adapter semantics;
- Task Contract fields/references for material runbooks;
- handoff evidence keyed by runbook/invocation rather than raw command transcripts;
- deterministic tests for authorization + runbook invariants;
- synthetic adapters covering materially different command environments/platform mechanisms;
- dynamic security/adapter tests only where deterministic verification is insufficient.

No shell, terminal, operating system, SSH implementation, cloud provider or executor host may become a Governance Core dependency merely to implement D034.

## Consequences

- runbooks become the preferred operational procedure abstraction for material/repeatable execution;
- project-native runbooks/workflows are reused before Governance creates its own;
- Human approval is attached to the bounded operation/stage, not every command line;
- exact terminal syntax moves into adapters and ceases to be Governance semantics;
- Linux/POSIX examples remain allowed as adapter examples but cannot define the methodology;
- Windows/PowerShell and other command environments are first-class equivalent adapter possibilities;
- APIs/CLIs/remote-management/automation systems are equally valid when they preserve the runbook contract;
- an approved runbook does not grant permission to invoke it against an unauthorized target;
- future tests must demonstrate semantic equivalence across at least materially different adapter families.