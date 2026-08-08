# Agent Adapter Contract

Adapter-Version: 1.0.0

Load this module when configuring an agent product to participate in the governance framework.

## Role Abstraction

Governance defines roles, not products:
- `human` — Human Owner;
- `strategy` — Strategy/Governance Agent;
- `implementation` — Implementation Agent.

OpenCode, Codex, Claude Code, Antigravity, or another capable agent product MAY fill the `implementation` role. A product MAY also fill the `strategy` role when explicitly assigned. Product identity never changes task semantics or authority.

## Adapter Responsibilities

A product-specific adapter MUST, as far as the product supports it:
1. bootstrap with STATE + GOVERNANCE only;
2. follow the Governance Context Router for lazy loading;
3. map the active product to a protocol role;
4. protect Governance Core and project strategic/state records from the Implementation role;
5. permit the Implementation role to append valid EXCHANGE events;
6. preserve project safety rules;
7. support sequential disclosure by loading only the current task record;
8. avoid silently weakening governance when a native permission feature is unavailable.

If a product cannot enforce a restriction mechanically, the adapter MUST state the restriction normatively and the agent MUST obey it.

## Task Neutrality

Task records MUST NOT depend on a specific agent product. They define objective, scope, dependencies, acceptance, required Skills and constraints only.

Vendor-specific invocation syntax, tool configuration, permissions, local command aliases, or model behavior belongs in the product adapter or an approved Skill, never in the task contract unless the Human Owner explicitly makes that product a project requirement.

## Sequential Disclosure

The adapter MUST NOT preload future task records. The Implementation Agent may inspect metadata required to select the next eligible task, but the objective/scope/acceptance content of that task is loaded only after the current task reaches DONE.
