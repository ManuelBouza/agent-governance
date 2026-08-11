# Execution Access Control Architecture

Status: ARCHITECTURE OVERVIEW  
Normative decision: `docs/decisions/D033-execution-access-control-plane.md`

## Purpose

Agent Governance aims to let AI control the technical development cycle end-to-end without turning an open terminal, SSH key, cloud login or administrator-capable workstation into unlimited authority.

The model separates:

- **what the Human Owner authorizes**;
- **how the AI chooses to implement that authorized operation**;
- **what the operating system/platform actually permits**;
- **what evidence is retained for review**.

The Human approves meaningful effect/risk boundaries. The AI remains free to choose routine commands inside those boundaries.

## Core model

```text
Human intent / approved task
          │
          ▼
Execution Capability Envelope
          │
          ▼
preflight authorization decision
          │
    ┌─────┼───────────┐
    ▼     ▼           ▼
 allow   ask Human    deny
    │
    ▼
AI executes terminal/API/SSH/CLI operations
    │
    ▼
platform-native least-privilege enforcement
    │
    ▼
resource changes + sanitized evidence
    │
    ▼
review / acceptance
```

The important distinction is:

```text
mechanism != authority
```

Having `ssh`, `sudo`, a cloud CLI or an authenticated token available does not authorize all effects those mechanisms can produce.

## Why command allowlists are insufficient

A command string does not fully describe its effect.

For example:

```text
git status
```

is normally local observation, while:

```text
git push
```

mutates a remote repository.

Likewise:

```text
ssh server systemctl status app
```

and:

```text
ssh server systemctl restart app
```

use the same transport but have very different operational effects.

A cloud CLI can switch accounts/projects/regions without changing the executable name. A script or package-manager hook can spawn child processes that perform effects absent from its top-level name.

Agent Governance therefore authorizes **target + effect + privilege + resource scope**, not just executable names.

## Execution Capability Envelope

For material system access, the authorization boundary can be understood as:

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

The complete normative fields and rules are in D033.

## Approval model

### ALLOW_TASK

Routine effects already contained by an approved task.

Examples:

- inspect project files/status;
- execute project-native tests;
- edit executor-owned files in the authorized branch;
- create disposable synthetic test state.

No additional Human prompt is needed.

### ALLOW_EXPLICIT

The effect is outside the routine baseline but explicitly described by the controlling task/decision.

Examples:

- connect to a named staging server;
- use an existing credential for one approved account/project;
- restart one named non-production service;
- modify one explicitly authorized workstation/project setting.

The AI can autonomously choose commands inside that explicit boundary.

### REQUIRE_HUMAN

The Human Owner must approve the bounded operation before execution.

Default cases include:

- production mutation/deployment;
- root/administrator privilege;
- workstation/system-global changes;
- firewall/SSH/IAM/security-control changes;
- credential creation/rotation/revocation;
- destructive or difficult-to-reverse operations;
- production/schema/data migrations with material risk;
- uncertain target/effect.

The approval is normally for a coherent operation rather than every command line.

### DENY

Fail closed under the current authorization.

Examples:

- target identity mismatch;
- disabling host verification just to connect;
- arbitrary/unbounded root shell when only one narrow privileged action is required;
- searching/copying/persisting credentials outside the approved source;
- disabling audit/security controls for convenience;
- jumping through unapproved remote hosts/forwarding paths;
- executing dynamically acquired content whose effects cannot be bounded.

## Local boundaries

“Local” does not mean “safe by default”. Distinguish at least:

```text
repository worktree
      ↓ increasing blast radius
disposable test/eval state
      ↓
workstation user configuration
      ↓
local services/containers/VMs
      ↓
workstation system/global configuration
      ↓
root/administrator/security controls
```

An ordinary source task normally authorizes only the upper, narrow project boundaries. It does not automatically authorize package-manager/global shell/profile/service/system changes.

## Remote boundaries

A remote target should be identified by the dimensions that matter to the platform:

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

A convenient alias such as `prod`, `server1` or a current cloud context is not sufficient when a mistake could target another resource.

For SSH-like access, remote identity/host-key verification and forwarding/pivot behavior are part of authorization, not connectivity details to bypass.

## Privilege and credentials

Two independent questions must be answered:

```text
Can this identity authenticate?
              ≠
Is this effect authorized?
```

A valid SSH key/token proves that an authentication mechanism works. It does not prove Governance permission for the operation.

Similarly:

```text
normal user → sudo/root
```

is an authorization boundary. The preferred design grants the smallest privileged capability necessary rather than an unrestricted privileged shell.

Credentials remain external operational state. They must not become repository artifacts, handoff content or ordinary transcript/log material.

## Child-process non-expansion

Authority may be inherited only downward as a subset:

```text
approved command
   └── child/script/shell
         └── nested command
               └── remote operation
```

Every descendant operation remains inside the original envelope.

A parent command cannot “launder” new authority merely because it was allowed to start.

This is especially relevant to:

- shell interpolation/substitution;
- scripts;
- build/package hooks;
- plugin systems;
- remote shell commands;
- infrastructure/cloud/database CLIs;
- tools that download and execute code.

## Enforcement layers

Agent Governance should not depend exclusively on prompt compliance when a native security boundary is available.

```text
Governance authorization
          │
          ▼
executor-host permissions/sandbox
          │
          ▼
OS / IAM / SSH / database / cluster restrictions
          │
          ▼
actual resource
```

Possible mechanisms include restricted users/service accounts, narrow privilege rules, SSH forced/restricted commands, IAM roles, database roles, container/user-namespace controls and OS sandbox components.

These mechanisms are adapters/enforcement providers; none is universal Governance authority.

## Remote SSH example

A broad design:

```text
AI
 │ unrestricted SSH key
 ▼
remote shell as admin
```

has an unnecessarily large capability surface.

A narrower design may be:

```text
AI
 │ approved key/principal
 ▼
SSH identity restriction
 │
 ├─ forwarding disabled
 ├─ only expected account
 └─ bounded command/privilege
        │
        ▼
   target service/resource
```

OpenSSH provides mechanisms such as forced commands, user/principal restrictions and forwarding/destination restrictions that can implement parts of this pattern. Other platforms use their native equivalents.

## Approval lifecycle

```text
1. Strategy determines required effect
2. identify exact target and privilege
3. classify approval mode
4. show material risk/rollback at user's register
5. Human approves only when required
6. persist authorization effect
7. executor preflights actual context
8. native controls enforce where possible
9. executor operates autonomously inside envelope
10. capture sanitized evidence
11. review verifies actual effects vs envelope
```

If target, privilege, destructive scope or architecture changes materially after approval, the envelope is stale and must be refreshed.

## Audit model

For material operations retain enough evidence to answer:

```text
What task authorized this?
What target was actually used?
Which principal/role acted?
What class of effect occurred?
What changed?
Did it succeed?
Was rollback/recovery needed?
Did any unexpected prompt/escalation occur?
```

Do not solve auditability by recording secrets, raw credential-bearing environments or hidden model reasoning.

## Relation to D032

D032 requires the quality/security layers to be applied silently by default and surfaced only when material.

Execution control follows the same interaction principle.

A non-technical user might see:

```text
This change needs administrator access to the production server and will restart the service. I can execute it after you approve that production operation; rollback is X.
```

An expert user might see the exact target identity, role, service, migration/rollback sequence and privilege boundary.

The underlying execution safety is the same in both cases.

## Planned Core integration

D033 deliberately does not modify the current Core protocol while T004 is already executing.

A later dedicated increment should integrate the architecture through a focused Core module tentatively named:

`governance-core/EXECUTION-CONTROL.md`

and connect it to:

- `GOVERNANCE.md` routing;
- `EXECUTION.md` eligibility/blockers;
- Task Contract authorization fields;
- handoff execution evidence;
- deterministic policy tests;
- later adapter/security tests.

Until that integration is implemented and accepted, D033 is the durable architecture decision and future-work constraint; it does not retroactively rewrite T004.
