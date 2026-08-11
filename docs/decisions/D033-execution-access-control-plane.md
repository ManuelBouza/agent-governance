# D033 — Execution Access Control Plane

Status: ACCEPTED  
Authority: Human Owner / ChatGPT Orchestrator

## Problem

Agent Governance is intended to control the complete development cycle through AI while keeping the Human Owner in final authority over scope, risk and irreversible effects.

The current Core defines task readiness, sequential execution, strategic blockers and quality/security review, but it does not yet define a complete authorization model for terminal/process/system access.

That gap matters because implementation work may need to:

- invoke local shells and subprocesses;
- install or configure local development tooling;
- modify workstation-level configuration;
- use `sudo` or another privilege-elevation mechanism;
- connect to local services, containers, databases or virtual machines;
- connect to remote machines through SSH or equivalent transports;
- invoke cloud, cluster, database, deployment or infrastructure CLIs;
- use pre-existing credentials or authentication agents;
- operate on development, staging or production resources;
- run scripts/tools whose child processes can produce effects broader than the apparent top-level command.

A command-name allowlist is insufficient. `ssh host script`, a cloud CLI, a database client, a package-manager hook and a local shell script can produce equivalent system effects through different command strings. Conversely, the same binary may be safe for one target/effect and unacceptable for another.

The missing control is therefore an **effect- and target-oriented execution authorization layer** rather than a terminal-specific list of command names.

## Decision

Agent Governance SHALL define an **Execution Access Control Plane** for any implementation action capable of changing or inspecting external execution state.

The control plane governs terminal, shell, subprocess, remote-access and system-management capabilities regardless of the executor product used to invoke them.

Its primary authorization object is an **Execution Capability Envelope**.

The invariant is:

```text
transport or credential possession != execution authority
```

A shell, SSH connection, authenticated CLI session, cloud token, SSH key, `sudo` capability or open terminal only provides a mechanism. It does not independently authorize effects outside the approved envelope.

## Execution Capability Envelope

Before an Implementation Agent performs an execution effect that is not already covered by the ordinary local task baseline, the applicable task/decision must make the authorized envelope determinable.

The envelope describes at least the material subset of:

1. **actor / execution role** — which Governance role is acting;
2. **target identity** — exact resource/environment/account/host/cluster/worktree boundary;
3. **effect classes** — what categories of effects are permitted;
4. **resource scope** — files, services, namespaces, repositories, accounts, databases or equivalent resources inside the boundary;
5. **privilege ceiling** — maximum user/service identity, role or privilege level permitted;
6. **credential source/use** — which pre-existing authentication mechanism may be used and for what target;
7. **network destinations** — allowed remote endpoints or service boundaries when network access is material;
8. **task/time boundary** — which task/operation the authorization belongs to and when it expires;
9. **reversibility / rollback expectation** — recovery or rollback controls where mutation is material;
10. **approval mode** — whether the capability is task-authorized, explicitly bounded, Human-gated or denied;
11. **audit/evidence requirement** — the minimum observable evidence required after execution.

Not every low-risk local task needs a serialized matrix. The envelope must be explicit enough that the executor and reviewer can determine whether a proposed effect is inside or outside authorized scope.

## Effect-oriented classification

Authorization SHALL be evaluated by effect, not by executable name alone.

Useful effect families include:

- `OBSERVE` — read/inspect/query without intended mutation;
- `MUTATE_SCOPED` — modify artifacts/state explicitly owned by the current task boundary;
- `EXECUTE_LOCAL` — execute local code/processes inside the approved workspace/runtime boundary;
- `NETWORK_CONNECT` — initiate network communication to an approved destination;
- `REMOTE_EXECUTE` — cause commands/processes to execute on another system/account/environment;
- `INSTALL_CONFIGURE` — install/update/configure tooling, packages, services or workstation/project settings;
- `PRIVILEGE_ELEVATE` — act with an identity/role more privileged than the ordinary executor context;
- `SECRET_USE` — access/use credentials, tokens, private keys or equivalent authentication material;
- `DEPLOY_SERVICE_CHANGE` — change running services, deployments, infrastructure or operational configuration;
- `DATA_MUTATE` — mutate persistent application/operational data outside disposable test fixtures;
- `DESTRUCTIVE_IRREVERSIBLE` — delete, overwrite, rotate, revoke or otherwise perform an effect whose recovery is uncertain, costly or impossible.

A single command may belong to several families. The effective authorization requirement is the strictest material family involved.

## Approval modes

Use four conceptual approval outcomes.

### `ALLOW_TASK`

The current approved task/readiness contract already authorizes the effect without another Human interruption.

Typical examples:

- read-only inspection inside the current project scope;
- ordinary Git/status/diff operations required by the approved workflow;
- executor-owned file mutation inside the authorized topic branch;
- repository-native build/test/lint commands named or implied by the approved task;
- disposable/synthetic local test state inside the approved harness boundary.

`ALLOW_TASK` does not authorize workstation-global mutation merely because a task is READY.

### `ALLOW_EXPLICIT`

The effect is permitted only because a persisted task/decision explicitly bounds target, capability and privilege.

Typical examples:

- connection to a named remote development/staging target;
- use of a particular pre-existing authentication mechanism against that target;
- a bounded non-root service restart in a named non-production environment;
- a specifically approved tool/config update with known scope;
- a narrowly scoped external API/CLI mutation whose account/project/resource is explicit.

The executor may choose the exact technical command sequence inside the approved envelope without asking for every shell line.

### `REQUIRE_HUMAN`

The Human Owner must approve the bounded operation before execution continues.

This applies by default when the proposed effect materially includes one or more of:

- production deployment or production state mutation;
- privilege elevation to root/administrator or equivalent high-impact role;
- workstation/system-global configuration outside an already approved standing policy;
- security-control, firewall, SSH daemon, identity, authorization or trust-store change;
- credential creation/rotation/revocation or broadened credential scope;
- destructive/irreversible data or infrastructure action;
- schema/data migration with material irreversible or production risk;
- actions whose real target/effect cannot be established confidently before execution.

Approval SHOULD cover a coherent bounded operation/batch rather than forcing the Human to approve each mechanically necessary command. If the operation materially changes after approval, the authorization is stale and must be refreshed.

### `DENY`

The executor must fail closed and cannot proceed under the current authorization.

Default examples include:

- unknown or mismatched target identity;
- attempt to bypass host/server identity verification merely to make connectivity succeed;
- unbounded privilege such as arbitrary administrator/root execution when only a narrow capability is required;
- credential discovery/exfiltration/persistence outside the approved credential source;
- disabling audit/security/access controls merely to make a task easier;
- expanding from clone/project-local permission to global workstation mutation without authorization;
- remote forwarding/pivoting or multi-hop access not covered by the target/network envelope;
- executing dynamically obtained/unreviewed content whose possible effects cannot be bounded sufficiently;
- hiding material execution evidence required for review.

A denied capability requires a new Human/Strategy decision or narrower technical approach; it is not a prompt-engineering obstacle to bypass.

## Human authority without command-by-command micromanagement

The Human Owner remains final authority, but the system SHOULD minimize unnecessary approval interrupts.

The preferred model is:

```text
Human approves risk/effect boundary
        -> AI selects technical commands inside boundary
        -> enforcement prevents boundary expansion
        -> evidence proves what actually happened
```

Human approval is therefore primarily **capability/effect approval**, not raw command-string approval.

Command-level review MAY still be required when the command itself is the clearest representation of a high-risk or irreversible effect.

## Child-process and indirection rule

Authorization propagates downward but never expands.

A permitted parent process does not grant arbitrary authority to its descendants.

This applies to:

- `sh -c`, `bash -c`, PowerShell or equivalent shell nesting;
- scripts and generated scripts;
- pipelines and command substitution;
- build/package-manager hooks;
- task runners;
- `make`, package scripts or equivalent indirection;
- `ssh host <command>`;
- remote shell scripts;
- cloud/cluster/database CLIs that invoke server-side operations;
- plugins/hooks/extensions that spawn subprocesses.

The child/nested operation must remain a subset of the parent Execution Capability Envelope.

If a dynamic script/tool can produce effects the agent cannot bound confidently, it must be isolated, narrowed, inspected first, or blocked.

## Target identity rule

The executor must identify the actual target before mutation.

Useful target dimensions include:

### Local

- current source worktree/clone;
- disposable test/eval directory;
- workstation user-level state;
- workstation system/global state;
- local service/container/VM identity.

### Remote

- environment class: development/staging/production or project-native equivalent;
- provider/account/subscription/project/tenant identity where relevant;
- hostname/service/cluster identity;
- namespace/database/schema/repository/resource identity where relevant;
- authenticated principal/role;
- host/service identity evidence when the transport provides it.

Aliases are convenience labels, not identity proof.

A target identity mismatch invalidates authorization and creates a blocker.

## Remote-access posture

Remote access follows the same capability envelope as local execution, with additional identity/network constraints.

For SSH-like transports:

- verify the remote host identity using the project's/admin's accepted trust mechanism;
- changed or unknown host identity must not be bypassed silently;
- agent/port/X11/socket forwarding is not implicitly authorized by shell access;
- multi-hop/bastion/pivot access must remain inside the approved network/target path;
- root/administrator login is not implied by possession of a key or credential;
- where practical, use native restrictions such as forced commands, destination restrictions, forwarding restrictions, dedicated principals/accounts or equivalent controls.

OpenSSH capabilities such as `ForceCommand`, `DisableForwarding`, `PermitOpen`, user/principal restrictions and host-key verification illustrate native enforcement mechanisms. Agent Governance does not require OpenSSH specifically.

## Privilege-elevation posture

Privilege elevation is a separate capability, not a normal continuation of shell execution.

Default posture:

- execute as the least-privileged identity sufficient for the approved effect;
- do not use `sudo`, root, administrator, privileged containers or equivalent escalation unless the envelope permits it;
- prefer narrow native privilege policies over broad unrestricted elevation;
- a privileged command must not become a route to an unrestricted privileged shell unless that shell itself is explicitly authorized;
- privilege obtained for one operation must not silently persist as authority for unrelated later work.

The Implementation Agent may perform an approved privileged operation; the policy does not require the Human to type it manually.

## Credential posture

Credential possession and Governance authorization are independent.

Rules:

- use only a credential/authentication mechanism authorized for the current target/effect;
- prefer existing OS-native agents/keychains/workload identities/short-lived tokens or project-native secret mechanisms when available;
- do not copy credentials/private keys/tokens into repository files, handoffs, transcripts or ordinary logs;
- do not broadly search a user's home/profile/configuration for credentials merely because authentication failed;
- do not persist a credential in a new location without explicit authorization;
- do not broaden token/key/account permissions merely to unblock automation;
- secret redaction must preserve enough non-secret evidence to audit target/principal/effect;
- authentication success proves identity/access, not permission under Governance.

Existing project-native identity/secret systems are reused under `COEXISTENCE.md`; Agent Governance should not create duplicate credential authority.

## Environment and command-context rule

The same command can have different effects depending on context.

Authorization evaluation must consider material context such as:

- working directory;
- environment/account/profile selection;
- config file selection;
- shell expansion/interpolation;
- input files/scripts;
- target environment variables;
- active cloud/cluster/database context;
- inherited credentials/agents;
- container/namespace/chroot/sandbox boundary;
- command arguments that change target or destructive behavior.

Unexpected context drift creates a blocker when it could change authorization.

## Native enforcement before prompt-only trust

When the risk is material and a native platform control can enforce the approved boundary, prefer that enforcement over relying only on agent instructions.

Examples may include:

- restricted OS users/service accounts;
- narrowly scoped `sudoers`/privilege policies;
- SSH forced commands/principals/destination/forwarding restrictions;
- container/user namespace/mount/network restrictions;
- `no_new_privs`, seccomp or other OS sandbox components as appropriate;
- cloud IAM roles/policies scoped to required resources/actions;
- database users/roles scoped to required schemas/actions;
- deployment/service accounts with bounded permissions.

No single mechanism is universal. In particular, syscall filtering such as seccomp reduces kernel attack surface but is not by itself a complete logical sandbox.

Agent Governance defines the authorization semantics; project/platform-native controls should enforce them where practical.

## Reversibility and destructive effects

Mutation risk is evaluated before execution.

For material changes, Strategy/Implementation should establish the applicable subset of:

- current-state capture;
- dry-run/plan/preview when trustworthy and available;
- backup/snapshot/export where appropriate;
- transactional or staged rollout;
- rollback command/path;
- recovery owner and expected recovery evidence;
- stop condition when observed state differs from assumptions.

A dry-run is evidence, not authorization.

Destructive/irreversible effects default to `REQUIRE_HUMAN` and must make the actual target and consequence visible before execution.

## Audit/evidence rule

Execution control must be auditable without persisting secrets or private chain-of-thought.

For material terminal/system access, evidence should capture the applicable subset of:

- task/authorization reference;
- target identity/environment;
- executing principal/role when observable;
- effect class;
- sanitized command/operation or equivalent provider action identifier;
- working/resource scope;
- start/end or ordered execution evidence where useful;
- exit/result status;
- changed resource/artifact summary;
- rollback/recovery result when used;
- unexpected prompts/escalations/denials;
- evidence that native restrictions/sandboxing were active when acceptance depends on them.

Do not record credentials, secret values, sensitive raw environment dumps or hidden reasoning.

NIST audit/accountability controls and privileged-command concepts support recording security-relevant administrative activity; exact implementation remains platform/project specific.

## Unexpected interaction / prompt rule

The executor must stop or safely abort when an interactive prompt reveals material authority/context not covered by the current envelope, including:

- password/credential input from an unapproved source;
- first-use or changed remote identity that cannot be verified under accepted policy;
- confirmation of a broader destructive effect than expected;
- privilege escalation not already authorized;
- target/account/environment mismatch;
- request to disable a security/audit/control mechanism;
- MFA/Human approval workflow whose completion is itself an external Human control not delegated to the executor.

The agent may continue normal non-material prompts whose choices are already mechanically determined by the approved operation and do not broaden authority.

## Coexistence with project-native controls

Project/platform-native access controls remain authoritative for their owned technical boundary when they are compatible with Governance.

Agent Governance:

- reuses/adapts existing IAM, SSH, bastion, PAM, privilege, secrets, deployment and audit mechanisms;
- does not weaken them to obtain convenience;
- treats a stricter native denial as a real constraint, not something to route around;
- fails closed on conflicting authority/security overlays until Strategy/Human resolves the conflict;
- does not require one universal terminal wrapper for all consumer projects.

## Source-maintainer relationship

For the `agent-governance` source repository, existing D030/D031 rules remain examples of bounded execution authorization:

- clone-local Gentle-AI RDD configuration is allowed only under its accepted narrow disposition;
- global/workstation reconfiguration is not implied;
- `.atl/` normal local registry state may operate under D031 without becoming canonical source authority.

This decision generalizes the underlying boundary without retroactively changing already-running T004.

## Primary Solution Diagram

The dominant question is security-sensitive execution/data/control flow across local and remote trust boundaries. The preferred primary view is a DFD with trust boundaries.

```text
Human Owner
   │ approves scope/risk
   ▼
Strategy / Task Contract
   │
   │  Execution Capability Envelope
   │  target + effect + privilege + credentials
   │  network + reversibility + approval mode
   ▼
┌──────────── POLICY / AUTHORIZATION BOUNDARY ────────────┐
│ Preflight: target identity + state + capability         │
│ Decision: ALLOW_TASK / ALLOW_EXPLICIT /                │
│           REQUIRE_HUMAN / DENY                          │
└───────────────────────┬─────────────────────────────────┘
                        │ allowed
                        ▼
                Executor / Terminal
             ┌──────────┼───────────┐
             ▼          ▼           ▼
        local process   ssh/API    privileged op
             │          │           │
             └──────────┴─────┬─────┘
                              ▼
                 OS/native enforcement
          sandbox · privilege · SSH/IAM restrictions
                              │
                              ▼
                     Local/Remote Resource
                              │
                              ▼
                 observable audit evidence
                              │
                              ▼
                     Handoff / review
```

## Quality-envelope result

Material dimensions for this decision:

- security/least privilege;
- identity and target verification;
- privacy/credential handling;
- reliability and failure containment;
- auditability/observability;
- reversibility/recovery;
- interoperability with project-native IAM/terminal/deployment systems;
- maintainability and adapter neutrality;
- supply-chain/executable-content risk;
- production/release safety.

Accessibility is not directly material to the execution-control mechanism itself, but Human approval prompts/diagrams must still follow `INTERACTION.md` when the future Core integration is implemented.

## Research basis

Primary references reviewed for this decision include:

- NIST SP 800-207 — Zero Trust Architecture: resource-focused authentication/authorization and removal of implicit trust based only on network location: `https://csrc.nist.gov/pubs/sp/800/207/final`
- NIST CSRC least-privilege definition / SP 800-53 lineage: minimum necessary authorizations/resources: `https://csrc.nist.gov/glossary/term/least_privilege`
- NIST CSRC privileged-command definition / SP 800-53 lineage: administrative/security-relevant command activity: `https://csrc.nist.gov/glossary/term/privileged_command`
- NIST SP 800-53 Audit and Accountability control family, including audit generation/session audit concepts: `https://csrc.nist.gov/projects/risk-management/about-rmf/assess-step/assessment-cases-download-page`
- OpenSSH `sshd_config(5)` — native command, forwarding, destination, principal/user and other restriction mechanisms: `https://man.openbsd.org/sshd_config`
- OpenSSH `ssh_config(5)` — host-key verification/trust configuration: `https://man.openbsd.org/ssh_config`
- Linux kernel `no_new_privs` — preventing privilege gain through `execve()` paths: `https://www.kernel.org/doc/html/latest/userspace-api/no_new_privs.html`
- Linux kernel seccomp filter documentation — syscall surface reduction and explicit warning that syscall filtering alone is not a complete sandbox: `https://www.kernel.org/doc/html/latest/userspace-api/seccomp_filter.html`

These sources inform architecture and enforcement patterns. Agent Governance remains platform-neutral and does not mandate NIST compliance, Linux, OpenSSH, sudo, systemd or one specific access-control product.

## Core-integration plan

D033 is accepted architecture immediately, but its protocol integration SHALL be performed in a separate controlled increment after the currently running T004 work is reviewed.

That future increment should introduce the smallest coherent normative changes, expected to include:

- a focused `governance-core/EXECUTION-CONTROL.md` module;
- progressive routing from `GOVERNANCE.md`;
- linkage from `EXECUTION.md` so task readiness does not imply unlimited terminal/system authority;
- Task Contract support for an Execution Capability Envelope when non-baseline effects are needed;
- handoff/evidence requirements for material terminal/remote/privileged execution;
- deterministic tests for authorization classifications, child-process non-expansion, target/privilege/credential boundaries and protocol/module-version alignment;
- later adapter/dynamic security tests proving native enforcement where supported.

The implementation task must follow D032 graphical readiness and quality/security triage before becoming READY.

## Consequences

- Agent Governance can remain highly autonomous while maintaining explicit Human control of meaningful risk boundaries.
- The Human Owner does not need to approve harmless terminal mechanics one command at a time.
- READY task status no longer conceptually means unlimited local/remote execution authority once D033 is integrated into Core.
- Credential possession never substitutes for Governance authorization.
- local vs remote is not the primary trust distinction; actual resource identity, effect and privilege are.
- production/destructive/privileged operations receive stronger Human gating by default.
- future executor adapters should expose/enforce capability envelopes where their host supports permissions/sandboxing.
- platform-native controls are reused for enforcement rather than replaced by prompt-only policy.
- T004 remains governed by its existing contract and is not retroactively changed by this decision.
