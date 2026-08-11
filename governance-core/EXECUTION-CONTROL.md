# Execution Access and Runbook Control

Execution-Control-Version: 1.0.0

Load this module when planning, authorizing, executing or reviewing work that can inspect or mutate execution state outside ordinary task-local source/test effects, including local-system, remote-system, privileged, credentialed, network, deployment, persistent-data or destructive operations.

This module integrates D033 and D034 into the Governance Core. `EXECUTION.md` remains authoritative for task sequencing/state; this module governs the capability/effect boundary and material execution procedure inside a task.

## Core invariants

```text
mechanism != authority
procedure semantics != terminal syntax
approved runbook != approved invocation
authority(child) ⊆ authority(parent)
```

A terminal, shell, CLI, API, authenticated session, credential, remote connection or elevated identity is an execution mechanism. Possession or availability does not authorize every effect it can produce.

A runbook defines an operational procedure. Its semantic contract is independent from the terminal, operating system, command interpreter, CLI, API, SDK, remote transport or automation host used to realize it.

## Execution Capability Envelope

For every material execution effect, Strategy must make the applicable authorization envelope determinable before F5/readiness. The minimum material dimensions are:

- actor / Governance execution role;
- actual target identity and environment;
- allowed effect classes;
- resource scope;
- privilege ceiling;
- credential/authentication class and target binding when credentials are required;
- allowed network destination/path when network access is material;
- task/operation lifetime;
- rollback/recovery expectation for material mutation;
- approval mode;
- required sanitized evidence.

Low-risk project-local work does not require a serialized envelope matrix when these facts are already unambiguous from the task and repository policy.

## Effect classes

Classify by effect rather than executable name. A single operation may have several classes; the strictest material authorization controls.

- `OBSERVE` — inspect/query without intended mutation.
- `MUTATE_SCOPED` — mutate state explicitly owned by the current task boundary.
- `EXECUTE_LOCAL` — execute code/processes inside the approved local workspace/runtime boundary.
- `NETWORK_CONNECT` — initiate communication to an approved destination.
- `REMOTE_EXECUTE` — cause execution on another system/environment/account.
- `INSTALL_CONFIGURE` — install/update/configure tooling, packages, services or settings.
- `PRIVILEGE_ELEVATE` — use an identity/role above the ordinary executor context.
- `SECRET_USE` — access/use credentials or equivalent authentication material.
- `DEPLOY_SERVICE_CHANGE` — change running services, deployments, infrastructure or operational configuration.
- `DATA_MUTATE` — mutate persistent application/operational data outside disposable fixtures.
- `DESTRUCTIVE_IRREVERSIBLE` — delete/overwrite/rotate/revoke or otherwise cause difficult-to-recover effects.

## Approval outcomes

### `ALLOW_TASK`

The approved task already contains the effect inside its normal local boundary.

Typical scope includes repository inspection, Git/status/diff operations, executor-owned changes on the authorized branch, repository-native build/test/lint commands and disposable synthetic test state.

`ALLOW_TASK` never means arbitrary workstation/global/system mutation.

### `ALLOW_EXPLICIT`

A persisted task/decision explicitly authorizes the target, effects, resource scope and privilege ceiling. The executor may choose implementation mechanics within that envelope.

### `REQUIRE_HUMAN`

Human Owner approval is required before the bounded material operation proceeds. Default triggers include:

- production mutation/deployment;
- root/administrator or equivalent high-impact privilege;
- workstation/system-global configuration;
- security-control, identity, authorization, firewall, trust-store or equivalent control changes;
- credential creation/rotation/revocation or broadened credential scope;
- destructive/irreversible data or infrastructure effects;
- materially irreversible production migration;
- an operation whose actual target/effect cannot be established confidently.

Approval is for the coherent bounded operation/runbook stage, not normally every adapter command. A material target/effect/privilege change makes the approval stale.

### `DENY`

Fail closed when the current envelope cannot authorize the effect. Default cases include:

- unknown/mismatched target identity;
- bypassing host/service identity verification to obtain access;
- unbounded privileged execution when only a narrow capability is required;
- credential discovery/exfiltration/persistence outside the approved source/use;
- disabling security/audit/access controls merely to unblock work;
- expanding project/clone-local permission into global workstation mutation without authority;
- remote forwarding/pivot/multi-hop access outside the approved path;
- dynamically obtained/unreviewed execution whose possible effects cannot be bounded;
- hiding required material execution evidence.

A denial is a blocker, not a prompt obstacle to route around.

## Authorization evaluation

Before a material effect:

1. resolve the actual target/context;
2. identify all material effect classes;
3. bind resource, privilege, credential and network scope;
4. evaluate the strictest applicable approval outcome;
5. satisfy any required Human gate;
6. revalidate the target/context immediately before mutation when drift would matter;
7. execute only inside the resulting envelope.

Authentication success is evidence of technical access, not Governance authorization.

## Target identity

Target identity must be specific enough to detect a material targeting mistake.

Local dimensions may include worktree/clone, disposable test state, workstation user state, workstation global/system state and local service/container/VM identity.

Remote dimensions may include environment class, provider/account/project/tenant, host/service/cluster, namespace/database/resource and authenticated principal/role.

Aliases/current-context labels are convenience, not identity proof when a mismatch could cause material harm.

A target mismatch invalidates authorization and blocks execution.

## Privilege and credential rules

Use the least-privileged identity sufficient for the approved effect.

Privilege elevation is a separate capability. A narrow privileged operation must not silently become an unrestricted privileged shell/session.

Use only an approved credential/authentication mechanism for the approved target/effect. Prefer existing project/platform-native agents, keychains, workload identities or secret systems where compatible.

Do not:

- copy credentials/tokens/private keys into repository artifacts, handoffs or ordinary logs;
- broadly search user/system locations for credentials merely because authentication failed;
- persist a credential to a new location without explicit authority;
- broaden credential permissions to unblock automation.

## Child-process / indirection non-expansion

Authorization may narrow through indirection but never expand.

This applies to scripts, nested command environments, pipelines, task runners, build/package hooks, remote execution, CLIs that trigger server-side actions, plugins and child processes.

If a child/dynamic operation cannot be proven to stay within the parent envelope, narrow/inspect/isolate it or block.

## Context drift

Material command/adapter context is part of authorization. Re-evaluate when relevant context changes, including working/resource scope, account/profile/cluster/database selection, input script/config, inherited credentials, sandbox/container boundary or arguments that change target/destructiveness.

Context drift that could change the authorized effect makes the current authorization stale.

## Runbook requirement

Use a durable runbook when an operation is repeatable, operationally material, risky, cross-system or recovery-sensitive.

A runbook is required by default for:

- production deployment/service mutation;
- privileged/administrator execution;
- remote persistent mutation outside disposable test infrastructure;
- infrastructure/IAM/network/security-control changes;
- credential rotation/revocation or other material secret lifecycle work;
- persistent data/schema migrations;
- destructive/difficult-to-reverse effects;
- material multi-system sequencing;
- recovery/failover/restore;
- recurring maintenance with meaningful failure modes;
- operations whose safe continuation depends on checkpoints/rollback.

Routine local inspection, source edits, compilation, linting and tests do not require a runbook when a durable procedure adds no material value.

## Reuse before creating runbooks

Apply `COEXISTENCE.md` to project-native procedures.

- `REUSE` an adequate native runbook/workflow.
- `ADAPT` by reference when Governance authorization/checkpoints must wrap it.
- Do not mirror/copy a native procedure into duplicate Governance truth.
- `CONFLICT` blocks when two systems claim incompatible authority over the same effect.

Create a Governance-owned runbook only when no adequate native procedure exists or the procedure is itself Governance-owned.

## Runbook semantic contract

A material runbook must make the applicable subset determinable without depending on one terminal syntax:

- stable identity/revision and owning artifact/system;
- purpose/outcome, applicability and exclusions;
- required D033 effect classes and target constraints;
- privilege/credential/network requirements without secret values;
- bound inputs/resource identifiers;
- preconditions and current-state assertions;
- ordered semantic steps/state transitions;
- per-step required capability/resource scope;
- checkpoints and Human gates;
- postconditions/verification;
- retry/idempotency/concurrency semantics when material;
- failure/stop route;
- rollback/compensation/recovery semantics;
- required sanitized evidence.

The runbook declares capabilities it requires; it does not grant them.

## Runbook invocation lifecycle

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

Failure routes:

```text
target/preflight/authorization mismatch -> BLOCKED
step/checkpoint failure                 -> STOP -> RECOVER/ROLLBACK or BLOCKED
material context/adapter drift          -> STALE -> revalidate before continuation
Human denial                            -> BLOCKED/CANCELLED under controlling work lifecycle
```

A client/adapter exit code alone is not a sufficient postcondition for a material remote/system effect when actual target state can be verified independently.

## Terminal/platform-neutral Execution Adapter

An Execution Adapter translates semantic runbook steps into the available project/platform mechanism.

Possible adapter families include command environments, project-native task runners, cloud/database/cluster/deployment CLIs, APIs/SDKs, remote-management transports, CI/CD/automation systems and safe administrative interfaces.

Adapters must preserve:

- target/resource identity;
- effect/privilege/credential/network boundary;
- semantic ordering/state transitions;
- preconditions/checkpoints/Human gates;
- success/failure semantics;
- rollback/recovery behavior;
- required evidence.

Different syntax is acceptable. Different material semantics are not.

If an adapter cannot implement or verify a required semantic step safely, it must report unsupported/block rather than approximate or broaden the operation.

Prefer existing project-native mechanisms, then existing safe automation, then native CLI/API/management interfaces, then compatible command environments, and custom adapters only when justified. This is a capability/reuse preference, not an OS or shell preference.

## Adapter equivalence and drift

Two adapters are equivalent only when their material semantic contract is equivalent across target, effects, privilege/credential requirements, ordering, checkpoints, postconditions, recovery and evidence.

Material tool/platform drift invalidates prior adapter equivalence when it changes target defaults, auth/privilege behavior, preview semantics, status/exit semantics, rollback/recovery behavior or the ability to verify required conditions.

## Idempotency, retries and concurrency

Do not assume retry is safe.

Where material, define whether repetition is safe, retry conditions/limits, partial-completion detection, concurrency guards, target-state inspection before retry and compensation when a remote effect may have succeeded despite a client-side failure.

## Preview / dry-run

A trustworthy preview/plan/dry-run should be used when it materially reduces risk.

It is preflight evidence, not authorization, and does not eliminate target revalidation or rollback requirements.

## Native enforcement

For material risk, prefer enforceable project/platform controls over prompt-only trust when available: scoped identities/roles, resource permissions, restricted privilege, sandbox/container boundaries, network restrictions, database roles, deployment/service accounts or equivalent mechanisms.

A stricter native denial is a real constraint and must not be bypassed merely to satisfy Governance workflow.

## Interactive prompts

Stop or safely abort when an interaction reveals authority/context outside the envelope, including unapproved credential input, unverified changed target identity, broader destructive confirmation, unauthorized privilege escalation, account/environment mismatch, security-control disablement or an external Human/MFA gate not delegated to the executor.

Normal non-material prompts may proceed when their answer is mechanically determined by the already authorized operation.

## Evidence

For material execution/runbook invocation, retain enough sanitized evidence to determine the applicable subset of:

- task/authorization reference;
- runbook identity/revision;
- adapter identity/version when relevant;
- bound non-secret inputs;
- actual target/environment/principal;
- effect classes and resource scope;
- approval/Human-gate reference;
- semantic steps/checkpoints attempted/completed;
- postcondition result;
- rollback/recovery result;
- unexpected prompts/context deviations;
- evidence that required native restrictions were active.

Raw terminal transcripts are optional supplemental evidence, not the canonical record. Never persist secrets, raw secret-bearing environment dumps or private reasoning.

## Readiness rule

Before F5 passes for a task containing material execution effects, Strategy must verify:

- the Execution Capability Envelope is determinable;
- actual-target verification is possible;
- required approval mode/Human gates are explicit;
- required runbook exists or a controlling project-native procedure is referenced;
- preconditions/postconditions and recovery evidence are sufficient for the risk;
- the selected adapter class can preserve the semantic contract without authority expansion;
- no unresolved authority/native-control conflict exists.

If any of these cannot be established, the task is not READY.

## Blocker routing

Execution-control blockers include at least:

- authorization/approval unavailable;
- target/context mismatch;
- required privilege/credential boundary unavailable;
- required runbook/procedure absent or stale;
- precondition/checkpoint/postcondition cannot be verified;
- adapter cannot preserve required semantics;
- required recovery path is unavailable for the approved risk;
- native security/access control denies the operation;
- material context drift invalidates prior authorization.

Persist the concise blocker/evidence and stop the current task under `EXECUTION.md`; do not disclose/start later tasks.
