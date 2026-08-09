# Agent Governance Skill Package Design

Status: DESIGN-APPROVED

## Goal

Define two small, coherent Agent Skill packages over one canonical Governance Core:

1. a **Consumer Governance Skill** for installing/operating governance in adopting repositories;
2. a **Maintainer Skill** for developing/refactoring/testing/releasing the canonical source product.

The Skills MUST remain distinct in activation, context, permissions, tests/evals, and distribution expectations even when they share underlying code.

## Reusable Product Source

```text
agent-governance/
├── governance-core/
│   ├── GOVERNANCE.md
│   ├── CONTEXT.md
│   ├── ADAPTERS.md
│   ├── LIFECYCLE.md
│   ├── EXECUTION.md
│   ├── PROTOCOL.md
│   ├── HANDOFF.md
│   ├── SKILLS.md
│   ├── SKILL-DISCOVERY.md
│   └── SKILL-SUPPLY-CHAIN.md
├── governance-skill/                 # consumer-facing
│   ├── SKILL.md                      # release-gated
│   ├── agents/
│   │   └── openai.yaml
│   ├── assets/
│   │   ├── MISSION.template.md
│   │   ├── WORKPLAN.template.md
│   │   ├── TASK.template.md
│   │   ├── SKILL-APPROVAL.template.json
│   │   ├── STATE.template.json
│   │   └── EXCHANGE.template.jsonl
│   └── scripts/
│       └── governance.py
├── maintainer-skill/                 # source-product only
│   ├── SKILL.md                      # release-gated
│   └── optional maintainer routing/assets
├── src/                              # optional shared implementation when justified
├── tests/
└── evals/
```

The Core modules are canonical. Neither Skill duplicates or overrides Core authority.

## Consumer Governance Skill

Purpose: install, bootstrap, validate, operate, recover, hand off, audit, and archive governance inside an adopting repository.

Controlling contract: `GOVERNANCE-SKILL-CONTRACT.md`.

### Installed Project Footprint

```text
.agent-governance/
├── GOVERNANCE.md
├── CONTEXT.md
├── ADAPTERS.md
├── LIFECYCLE.md
├── EXECUTION.md
├── PROTOCOL.md
├── HANDOFF.md
├── SKILLS.md
├── SKILL-DISCOVERY.md
└── SKILL-SUPPLY-CHAIN.md

.agent-coordination/
├── MISSION.md
├── WORKPLAN.md
├── STATE.json
├── EXCHANGE.jsonl
├── tasks/
├── skills/
└── decisions/
```

Product adapters such as `AGENTS.md`, `opencode.json`, Codex/Claude/other native instructions remain project/tool-specific and are not task semantics.

### `governance-skill/SKILL.md`

Purpose: consumer activation, operation routing, non-authority invariant, source-independence, mutation/read safety, and deterministic-tooling routing.

Rules:
- minimal frontmatter for compatible Agent Skill consumers;
- reference canonical Core rather than restating it;
- use governance roles, not vendor identities;
- never embed source-product maintenance workflow, project state, or future task content;
- target <2,500 tokens unless measured use proves more is required;
- do not require read/write access to the canonical source repository after installation.

### Bootstrap assets

- `MISSION.template.md` — strategic objective/scope skeleton.
- `WORKPLAN.template.md` — gates, deterministic execution-order metadata and task pointers only.
- `TASK.template.md` — agent-neutral atomic task objective/scope/dependencies/acceptance/Skills/constraints.
- `SKILL-APPROVAL.template.json` — discovery source + exact canonical artifact provenance/revision/digest/risk/permission/dependency approval record.
- `STATE.template.json` — constant-size frontier.
- `EXCHANGE.template.jsonl` — role-based event seed.

Rules:
- placeholders only; no domain/vendor defaults;
- future task detail stays outside WORKPLAN;
- Skill approval records pin immutable audited artifacts;
- bootstrap never silently overwrites existing state.

### `governance-skill/scripts/governance.py`

Single deterministic consumer command surface. Initial subcommands:
- `bootstrap` — safely create Core/instance/task/Skill-record structure;
- `validate` — validate layout, references, context budgets, versions, adapters, STATE, WORKPLAN sequence, Skill approval records and EXCHANGE coherence;
- `state` — derive/check/refresh frontier checkpoint;
- `event` — validate role actors, EXCHANGE events/state transitions and DONE dependency semantics;
- `skill` — support candidate source resolution/inventory and validate canonical-source/approval-record/revision/digest/permission/dependency matching; MUST NOT decide strategic approval;
- `archive` — validate/prepare mission archival without destroying history.

Rules:
- read-only validation by default;
- explicit mutation only;
- standard library where practical;
- no production/external services;
- no strategic decisions in scripts;
- directory install commands are never executed during discovery;
- candidate Skill acquisition/inspection uses quarantine before active installation.

## Maintainer Skill

Purpose: develop, refactor, test/evaluate, and release this canonical source repository only.

Controlling contract: `MAINTAINER-SKILL-CONTRACT.md`.

The Maintainer Skill MAY route to source-specific paths/workflows such as `AGENTS.md`, `docs/DEVELOPMENT-WORKFLOW.md`, `docs/REFACTORING-WORKFLOW.md`, `docs/BRANCHING.md`, `docs/RELEASES.md`, Decision Records, product source, tests, and evals.

It MUST NOT:
- install a live consumer `.agent-coordination/` instance here;
- broaden into ordinary consumer governance;
- duplicate consumer operation instructions;
- redefine ChatGPT Orchestrator / Agente de IA Ejecutor authority;
- bypass topic-branch/PR or release rules.

The Maintainer Skill may call shared deterministic source tooling where useful, but its activation/context surface remains separate from the consumer Skill.

## Shared Implementation Rule

If both Skills require the same deterministic implementation, prefer a shared source module with thin Skill-specific routing rather than duplicated code.

Shared code does NOT imply shared `SKILL.md` instructions or trigger descriptions.

## Test/Eval Separation

At minimum maintain distinguishable coverage for:

### Core
- deterministic protocol/layout/reference/state invariants.

### Consumer Skill
- bootstrap/install/overwrite refusal;
- cold-start/recovery;
- state/event validation;
- context budgets;
- sequential disclosure;
- Skill discovery/supply-chain controls;
- source-repository independence;
- positive/negative/near-miss consumer activation.

### Maintainer Skill
- source-product activation vs consumer near misses;
- ChatGPT Orchestrator / Agente de IA Ejecutor role routing;
- PD/RF workflow routing;
- branch-policy routing;
- release preparation;
- refusal to create a live consumer instance in the source repository.

No production/external services are required for release-only tests.

## Deliberately Excluded from v1

Do not add without evidence:
- one combined maintainer+consumer `SKILL.md`;
- duplicate prose reference layers;
- multiple overlapping utility scripts;
- MCP/network dependencies for governance itself;
- decorative assets;
- domain-specific sample projects;
- consumer dependence on a floating source checkout.

## Release Gate

Before authoring/releasing either final `SKILL.md`, define and validate that Skill's:
1. exact trigger corpus;
2. exact activation description;
3. context-routing contract;
4. mutation/read boundary;
5. focused tests/evals and near-miss separation from the other Skill.

Additionally, before releasing the Consumer Governance Skill, finalize CLI contracts, template field sets, progressive-context checks, adapter neutrality, sequential disclosure, discovery resolution, supply-chain validation, and source-independence tests.
