# D054 — Executor-owned operation resolution and verified runbook recipes

Status: ACCEPTED  
Date: 2026-08-23  
Authority: Human Owner / ChatGPT Orchestrator  
Refines: D033, D034, D041  
Preserves: D040 atomic protocol migration, D052 conformance ownership, D053 SDD stage ownership

## Problem

Agent Governance already separates execution authorization from terminal syntax:

- D033 authorizes effects by actor, target, resource, privilege, credential, network and approval mode rather than by command name;
- D034 makes runbooks the durable semantic procedure and treats PowerShell, Bash, CLI, API, SDK, SSH/remote transport and automation as Execution Adapters;
- D041 gives the Executor autonomy over technical implementation mechanics inside D053 stages 5-6.

That architecture is directionally correct but leaves two practical gaps.

First, source orchestration can still drift into asking the Human Owner to copy/paste routine Git, uv, PowerShell, Bash, cloud-CLI or equivalent command sequences even though command selection/execution is an implementation mechanic. Human authority should approve intent/risk/effect boundaries, not become the default terminal operator.

Second, D034 defines reusable runbooks but does not yet define a deterministic **operation-resolution and learning loop** for adapter syntax. A capable Executor needs a safe way to reuse known-good operations, resolve an unknown command/API operation from authoritative documentation, verify the result, and retain that verified adapter realization for future compatible invocations.

The required refinement is therefore:

```text
Governance/Human -> semantic intent + target/effect/risk authority
Executor         -> adapter selection + command/API mechanics + execution
Runbook          -> durable semantic procedure
Verified recipe  -> proven adapter realization for one bounded operation/context
```

## Decision

Agent Governance adopts **Executor-owned operation resolution** with **runbook-first, official-documentation fallback, evidence-gated recipe learning**.

For governed executable work, command/API mechanics belong to the abstract Implementation Agent/Executor. This includes, as applicable:

- Git and repository CLIs;
- package/build/test tooling such as uv;
- PowerShell, Bash, POSIX shells and equivalent command environments;
- cloud/provider CLIs such as AWS CLI;
- authenticated service APIs/SDKs;
- database, cluster, deployment and infrastructure CLIs;
- SSH-like and other remote-management transports;
- compatible automation/orchestration surfaces.

The Orchestrator defines the authorized outcome, complete controlling Design/Plan, execution capability envelope, required semantic runbook/checkpoints where applicable, and acceptance evidence. It MUST NOT make the Human Owner the routine command runner merely because the current interaction surface cannot itself execute the operation.

Human interaction remains required for D033 `REQUIRE_HUMAN` gates, MFA or external approval workflows that cannot be delegated, material secrets/credential decisions, destructive or privilege-sensitive authorization, or when the Human explicitly asks to inspect/execute exact syntax.

## Operation-resolution invariant

Before an Execution Adapter performs a command/API/remote operation, the Executor follows this resolution order:

```text
1. resolve semantic operation + actual target/effect context
2. select/reuse the applicable semantic runbook when required/present
3. look for a compatible VERIFIED adapter recipe
4. if recipe is absent or stale, resolve syntax from authoritative documentation
5. construct a bounded CANDIDATE recipe
6. preflight/preview/dry-run when meaningful and supported
7. re-evaluate D033 authorization against the actual bound invocation
8. execute using least privilege and bounded credentials/network
9. verify target identity + required postconditions
10. promote the candidate to VERIFIED only after successful verification
11. reuse only while its binding/provenance remains current
```

A successful process exit code or HTTP status alone is not sufficient promotion evidence for a material mutation. The required semantic postcondition must be established.

## Runbook and recipe are different artifacts

D034 remains controlling:

```text
procedure semantics != terminal syntax
```

A semantic runbook describes outcome, inputs, target constraints, required effects, preconditions, ordered semantic steps, checkpoints/Human gates, postconditions, recovery and evidence.

A **Verified Operation Recipe** is an adapter-specific realization of one semantic operation/step. It may contain a parameterized CLI argv template, PowerShell/Bash expression, API operation/request shape, SDK call pattern, remote-management operation or equivalent mechanism.

A recipe is technical evidence/cache. It does not become Governance authority and cannot broaden the runbook, Task Contract or D033 envelope.

For ordinary low-risk `ALLOW_TASK` operations where D034 does not require a dedicated semantic runbook, a verified recipe MAY bind directly to a stable `operation_id`. For material/repeatable/risky/cross-system/recovery-sensitive operations, absence of the required semantic runbook is a blocker; the Executor must not invent procedure authority merely by learning a command.

## Authoritative documentation fallback

When no compatible VERIFIED recipe exists, the Executor must not guess syntax from model memory.

Use this evidence order:

1. compatible project/platform-native owned procedure or generated command interface;
2. installed/version-specific tool help, introspection or schema (`Get-Help`, `git help`, AWS CLI `help`, Bash `help`/manual, OpenAPI/provider schema, etc.);
3. official vendor documentation for the installed tool/API version;
4. current official vendor documentation only after compatibility with the installed/API version is established.

Community posts, forums, model recall, generated examples and search-result snippets may help diagnosis but MUST NOT be the sole authority for a newly learned executable recipe.

Documentation lookup itself is an `OBSERVE` operation and remains subject to network/credential policy. Dynamically fetched scripts or examples MUST NOT be piped/executed merely because they came from a documentation page.

If official documentation is unavailable, contradictory, cannot be bound to the current version/context, or leaves material target/effect ambiguity, fail closed and escalate instead of guessing.

## Recipe identity and trust lifecycle

A durable recipe must make the following determinable without storing secrets:

- stable `recipe_id` and semantic `operation_id`;
- optional semantic `runbook_id`/step binding;
- lifecycle state: `CANDIDATE | VERIFIED | STALE | REVOKED | SUPERSEDED`;
- adapter family and exact tool/API identity/version used for verification;
- platform and command-environment/quoting context when material;
- target class/resource scope and D033 effect classes;
- privilege ceiling, credential class and network scope;
- parameterized non-secret invocation representation;
- authoritative documentation provenance;
- preconditions and preview/dry-run capability where applicable;
- postconditions and expected failure semantics;
- verification time/evidence reference;
- explicit staleness triggers.

`VERIFIED` means proven only for the recorded binding. It does not imply universal compatibility.

Default staleness triggers include:

- tool/API version or behavior drift;
- changed shell/platform quoting semantics;
- changed default account/profile/region/cluster/database/repository context;
- changed authentication/privilege model;
- changed target-selection or destructive/default behavior;
- official documentation/API-schema revision that invalidates the recorded basis;
- a later execution that violates the recorded expected result/postcondition;
- applicable security advisory or project-native control change.

A `STALE`, `REVOKED` or `SUPERSEDED` recipe is never executed as trusted cached syntax. It returns to authoritative-documentation resolution or a current replacement.

## Safe execution requirements

D033 remains the authorization authority. Recipe reuse never skips:

- actual target/principal/context verification;
- least privilege;
- credential and network-scope checks;
- sandbox/native enforcement where applicable;
- D033 approval/Human gates;
- preconditions/checkpoints;
- postcondition verification;
- rollback/recovery rules for material mutation;
- sanitized evidence.

Nested shells, scripts, child processes and remote commands remain subsets of the parent capability envelope.

Unsafe convenience patterns such as disabling TLS/certificate verification, bypassing changed SSH host identity, broadening IAM/credentials, disabling security/audit controls or executing unreviewed downloaded scripts do not become acceptable because a prior recipe used them. Such recipes must be rejected/revoked unless an explicit current security/authorization exception controls the exact case.

## Cross-system operations

Connections between systems use the same model.

For SSH, APIs, cloud accounts, clusters, databases or other remote targets, a recipe must bind enough identity/context to prevent alias/default-context confusion. Host keys/certificates, authenticated principal/account/project/tenant/region/cluster/database identity and network path are preflight evidence where material.

A recipe may describe connection establishment, but possession of the connection or credential remains mechanism rather than authority.

## Durable persistence model

Reuse project-native operational systems first under D034/COEXISTENCE.

When no adequate native runbook/recipe provider exists, Agent Governance will materialize a native project-owned store under the governed repository:

```text
.agent-coordination/runbooks/
    RUNBOOK.template.md
    <runbook-id>.md
    recipes/
        RUNBOOK-RECIPE.template.json
        <recipe-id>.json
```

Ownership is intentionally split:

- semantic runbook meaning is Human/Strategy-owned procedure authority;
- adapter recipes are Implementation-owned technical realizations/evidence;
- deterministic validation may verify structure/trust binding but never create execution authority;
- STATE remains a frontier and does not copy the runbook/recipe registry.

The native store is demand-driven. Bootstrap creates only the reusable skeleton/templates; it does not pre-populate arbitrary command catalogs.

## Learning and promotion

The Executor may create a candidate only inside already-authorized execution semantics.

Promotion to `VERIFIED` requires:

1. authoritative documentation provenance;
2. exact adapter/tool/API binding;
3. D033 authorization for the invocation;
4. successful execution or safe non-mutating verification as applicable;
5. required semantic postcondition evidence;
6. no unexpected authority/context expansion;
7. a parameterized secret-free durable representation.

A failed candidate is not promoted. Repeated failures or a previously VERIFIED recipe failing within its recorded binding are learning/control signals under D039 and should trigger diagnosis/staleness rather than repeated blind retries.

## Research basis

This refinement is consistent with current external practice:

- OpenAI describes safe coding-agent deployment as bounded sandboxing plus approvals, constrained network egress, differentiated low-risk vs dangerous command rules, managed configuration and agent-native telemetry: https://openai.com/index/running-codex-safely/
- NIST least privilege explicitly applies to users and processes acting on their behalf, and NIST Zero Trust emphasizes least-privilege per-request decisions rather than implicit trust: https://csrc.nist.gov/glossary/term/least_privilege and https://csrc.nist.gov/pubs/sp/800/207/final
- AWS Systems Manager Automation models runbooks as ordered actions with inputs/outputs and supports explicit approval pauses; AWS CLI exposes built-in command help and API references: https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-documents.html and https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-help.html
- Microsoft PowerShell exposes local/online `Get-Help` and `ShouldProcess`/`-WhatIf`/`-Confirm` safety mechanisms: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/get-help and https://learn.microsoft.com/powershell/scripting/developer/cmdlet/requesting-confirmation-from-cmdlets
- Azure Automation recommends modular/restartable runbooks, progress/state checks and concurrency guards: https://learn.microsoft.com/azure/automation/manage-runbooks
- Git documents version-specific help through `git help`; Bash exposes built-in/manual help; OpenSSH documents strict host-key checking rather than silent identity bypass: https://git-scm.com/docs/git-help.html, https://www.gnu.org/software/bash/manual/, https://man.openbsd.org/ssh_config

These sources support the control pattern; they do not become Agent Governance authority.

## D040 staged adoption

D054 is accepted architecture immediately for source-maintainer interaction and planning, but reusable Consumer Core activation follows D040 so canonical `develop` is not knowingly broken by a cross-owner protocol transition.

### Phase A — accepted design and executable readiness

1. persist D054 and the staged operation-resolution contract;
2. integrate T035 plus its Orchestrator-owned conformance gate while current Protocol remains `1.14.0`;
3. complete already-frozen T034 first to restore the current native-SDD executable baseline;
4. T035 then adds the native runbook/recipe footprint, validation/resolution mechanics and implementation tests without changing the stable Consumer CLI command set.

### Phase B — protocol activation

After T035 is accepted/integrated and canonical verification is green, Orchestrator updates the routed Core semantics (`EXECUTION-CONTROL`, `PROTOCOL`, `CONTEXT`, `GOVERNANCE`/protocol version, Consumer Skill/template references as required) through a Markdown activation change. Runtime readiness must already understand the new footprint.

## Bootstrap-period rule

Until T035 native recipe persistence is integrated, source Executor work still follows D033/D034 plus this decision: command/API mechanics are Executor-owned; reuse an existing project/runbook procedure where present; otherwise resolve syntax from authoritative documentation and verify postconditions.

During this narrow bootstrap period, resolved operation evidence is provisional and must be recorded in the task handoff rather than treated as a reusable VERIFIED native recipe. T035 may seed a durable recipe only after revalidating that evidence against the then-current tool/version/documentation and its own conformance contract.

This temporary limitation is preferable to either making the Human the command runner or pretending a durable recipe registry already exists.

## Consequences

- routine CLI/API/PowerShell/Bash/remote mechanics move decisively to the Executor;
- Human approval remains risk/effect approval, not command-by-command micromanagement;
- D034 semantic runbooks remain separate from adapter syntax;
- known-good adapter operations become reusable, provenance-bound technical recipes rather than remembered chat snippets;
- unknown syntax is resolved from official/version-specific sources before execution;
- successful execution alone does not establish reusable trust without postcondition evidence;
- recipe drift fails closed;
- remote/cloud operations use the same target/effect/credential model as local commands;
- no universal terminal wrapper, external SDD/runtime dependency or command-name allowlist is introduced;
- T034 is not cancelled or semantically rewritten by D054; its launch is paused only until this source-level interaction refinement and T035 gate are durably represented.