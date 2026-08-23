# Agent Adapter Contract

Adapter-Version: 1.1.0

Load this module when configuring an agent product to participate in the governance framework.

## Role Abstraction

Governance defines roles, not products:
- `human` — Human Owner;
- `strategy` — Strategy/Governance Agent;
- `implementation` — Implementation Agent.

OpenCode, Codex, Claude Code, Antigravity, or another capable agent product MAY fill the `implementation` role. A product MAY also fill the `strategy` role when explicitly assigned. Product identity never changes task semantics or authority.

Under native `SDD.md`, the role mapping is fixed independent of product:

```text
strategy       -> Explore / Specify / Design / Plan & Trace
implementation -> Implement / Code Review & Verify
strategy       -> Converge / Accept / Evolve
```

An adapter MUST NOT use host-native planner/spec/review labels to create dual ownership or transfer a Strategy-owned SDD stage to the Implementation role.

## Adapter Responsibilities

A product-specific adapter MUST, as far as the product supports it:
1. bootstrap with STATE + GOVERNANCE only;
2. follow the Governance Context Router for lazy loading;
3. map the active product to a protocol role;
4. protect Governance Core and project strategic/specification/Design/state records from the Implementation role where that role lacks write authority;
5. permit the Implementation role to append valid EXCHANGE events;
6. preserve project safety rules;
7. support sequential disclosure by loading only the current task record and exact referenced specification/Design artifacts;
8. preserve native SDD stage ownership even when the host offers its own SDD/planning/review workflow;
9. avoid silently weakening governance when a native permission feature is unavailable.

If a product cannot enforce a restriction mechanically, the adapter MUST state the restriction normatively and the agent MUST obey it.

## Task Neutrality

Task records MUST NOT depend on a specific agent product. They define the applicable SDD profile/specification delta/Design references, objective, scope, dependencies, acceptance, verification/trace obligations, required Skills and constraints.

Vendor-specific invocation syntax, tool configuration, permissions, local command aliases, host-native SDD state, or model behavior belongs in the product adapter or an approved Skill/private executor process, never in the task contract unless the Human Owner explicitly makes that product/method a project requirement.

## Sequential Disclosure

The adapter MUST NOT preload future task records. The Implementation Agent may inspect metadata required to select the next eligible task, but the objective/scope/specification/Design/acceptance content of that task is loaded only after the current task reaches DONE.
