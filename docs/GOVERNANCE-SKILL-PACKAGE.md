# Governance Skill Minimal Package Design

Status: DESIGN-APPROVED

## Goal

Define the smallest reusable package that operates the modular Governance Core without duplicating authority, project state or unnecessary context, while remaining agent-product neutral.

## Reusable Product Source

```text
governance-product/
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
├── governance-skill/
│   ├── SKILL.md
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
└── tests/
    ├── trigger-cases.jsonl
    └── test-governance.py
```

The Core modules are canonical. `GOVERNANCE.md` is the small entrypoint/router; `ADAPTERS.md` maps product-specific integrations to stable governance roles; `SKILL-DISCOVERY.md` owns candidate-source/resolution semantics; `SKILL-SUPPLY-CHAIN.md` owns artifact provenance/audit/install semantics.

## Installed Project Footprint

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

## Required Skill Files

### `governance-skill/SKILL.md`
Purpose: activation, operation routing, non-authority invariant, mutation/read safety and deterministic-tooling routing.

Rules:
- minimal frontmatter for OpenAI/Codex compatibility;
- reference canonical Core rather than restating it;
- use role terms `strategy`/`implementation`, not a vendor as executor;
- never embed project state or future task content;
- target <2,500 tokens unless measured use proves more is required.

### `governance-skill/agents/openai.yaml`
OpenAI distribution metadata only. No governance authority or duplicated workflow rules.

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
- Skill approval records must pin immutable audited artifacts and stay outside WORKPLAN detail;
- bootstrap never silently overwrites existing state.

### `governance-skill/scripts/governance.py`

Single deterministic command surface. Initial subcommands:
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
- candidate Skill acquisition/inspection uses quarantine before active installation;
- detect unresolved canonical sources, unknown references, project contamination, vendor-coupled task records, invalid sequential-disclosure metadata and Skill artifacts that differ from their approval record.

## Release-Only Tests

### `tests/trigger-cases.jsonl`
Positive, negative and near-miss activation cases for install/bootstrap, cold-start/recovery, validation, handoff, checkpoint repair, sequential execution validation, Skill discovery/source resolution, Skill supply-chain audit and archive, plus negative generic planning/coding/Git cases.

### `tests/test-governance.py`
Must cover:
- clean bootstrap and overwrite refusal;
- role-based actor validation plus legacy aliases;
- valid/invalid EXCHANGE transitions;
- stale STATE/checkpoint derivation;
- context-budget/reference validation;
- deterministic WORKPLAN order/dependency validation;
- one-task-at-a-time disclosure fixture;
- autonomous A->B->C continuation on DONE without ACCEPTED gates;
- blocker stops sequence before future task disclosure;
- agent-product neutrality/contamination checks;
- cold-start using at least two distinct adapter fixtures;
- discovery result resolves to canonical owner/repository/path before acquisition;
- unresolved or lookalike provenance is rejected before audit;
- marketplace rank/install/security badge cannot satisfy approval validation;
- external Skill quarantine/inventory fixture;
- approval succeeds only for the exact audited canonical revision/digest;
- changed Skill content, dependency or permission envelope fails until re-audited;
- revoked/superseded Skill cannot validate for installation;
- archival safety.

No production/external services.

## Deliberately Excluded from v1

Do not add without evidence:
- duplicate prose reference layer;
- separate schema files when validator owns checks;
- multiple utility scripts;
- MCP/network dependencies for governance itself;
- decorative assets;
- Skill-local README/changelog/quick-reference files;
- copied product adapters;
- domain-specific sample projects.

## Operation Mapping

- bootstrap -> SKILL + Core + assets + `governance.py bootstrap`
- installation/context/adapter validation -> `governance.py validate`
- cold start -> STATE + GOVERNANCE router, then routed context
- execution validation -> EXECUTION + WORKPLAN metadata + current task only
- external Skill discovery -> SKILLS + SKILL-DISCOVERY + `governance.py skill`
- external Skill audit/approval matching -> SKILLS + SKILL-SUPPLY-CHAIN + `governance.py skill`
- state validation/refresh -> `governance.py state`
- handoff -> SKILL + HANDOFF + EXCHANGE delta/evidence
- event validation -> `governance.py event`
- archive -> `governance.py archive`
- portability -> multi-adapter tests + contamination/reference checks

## Activation Boundary

Trigger specifically for installing, operating, validating, recovering, handing off, checkpointing, sequentially executing/validating, discovering/auditing external Skills under this governance framework, or archiving a governed project.

Do not trigger merely for generic planning, project management, code writing/review, Git operations, architecture selection or AI discussion.

## Release Gate

Before authoring/releasing final `SKILL.md`, define and validate:
1. exact trigger corpus;
2. exact activation description;
3. CLI contract for each `governance.py` subcommand including `skill`;
4. exact template field sets including TASK, sequence metadata and Skill approval record;
5. progressive-context budget/reference checks;
6. agent-adapter neutrality and sequential-disclosure tests;
7. Skill discovery canonical-resolution tests;
8. Skill supply-chain provenance/revision/revocation validation tests.
