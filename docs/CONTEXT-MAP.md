# Source Repository Context Map

Status: ACTIVE  
Policy: `docs/decisions/D047-rcab-context-map-and-ratchet-policy.md`  
Architecture: `docs/CONTEXT-ARCHITECTURE.md`

## Purpose

Provide a compact, stable routing map for source-maintenance context without duplicating the live frontier in `docs/orchestrator/CHECKPOINT.md` or enumerating repository history.

Use the checkpoint to determine **what is current**. Use this map to determine **which stable authority family to load next**.

## Stable routes

| Route | Use when | Load |
| --- | --- | --- |
| `cold-start` | every source-maintenance bootstrap | `AGENTS.md`, then `docs/orchestrator/CHECKPOINT.md` |
| `unified-program` | D044 unified Governance architecture/program work | `docs/decisions/D044-unified-governance-skill-architecture.md`, `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` |
| `icae-rcab` | assurance design, context architecture, context budgets/projections | `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`, `docs/AGENT-CAPABILITY-ENGINEERING.md`, `docs/CONTEXT-ARCHITECTURE.md`, this map |
| `task-governance` | authoring/reviewing executor Task Contracts and handoffs | `docs/TASK-CONTRACTS.md`, `docs/EXECUTOR-HANDOFFS.md` |
| `operation-governance` | repository operations/cleanup and durable receipts | `docs/OPERATION-CONTRACTS.md`, `docs/OPERATIONAL-CONTRACTS.md` |

The table is intentionally small. The active checkpoint and current Task/Operational Contract select exact task, review, handoff, learning, release or evidence files only when needed.

## Load discipline

- `bootstrap` and `router` context is paid before focused task selection and is therefore the first warning/ratchet target.
- `focused` authority is loaded only for the relevant concern.
- `task` and `evidence` artifacts are selected from the current checkpoint/contract, not preloaded from this map.
- Generated projections are discovery metadata only and are never normative authority.
- A large on-demand file is not a split candidate merely because it is large.

## Machine-readable registry

The block below is the canonical machine-readable registry for the stable routes above. T031 tooling may project it deterministically but MUST NOT infer additional semantic routes or rewrite this Markdown.

<!-- RCAB-MAP-V1:BEGIN -->
```json
{
  "schema_version": "1.0.0",
  "entries": [
    {
      "path": "AGENTS.md",
      "class": "bootstrap",
      "routes": ["cold-start"]
    },
    {
      "path": "docs/orchestrator/CHECKPOINT.md",
      "class": "router",
      "routes": ["cold-start"]
    },
    {
      "path": "docs/decisions/D044-unified-governance-skill-architecture.md",
      "class": "focused",
      "routes": ["unified-program"]
    },
    {
      "path": "docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md",
      "class": "focused",
      "routes": ["unified-program"]
    },
    {
      "path": "docs/decisions/D046-agent-capability-engineering-and-context-architecture.md",
      "class": "focused",
      "routes": ["icae-rcab"]
    },
    {
      "path": "docs/AGENT-CAPABILITY-ENGINEERING.md",
      "class": "focused",
      "routes": ["icae-rcab"]
    },
    {
      "path": "docs/CONTEXT-ARCHITECTURE.md",
      "class": "focused",
      "routes": ["icae-rcab"]
    },
    {
      "path": "docs/CONTEXT-MAP.md",
      "class": "focused",
      "routes": ["icae-rcab"]
    },
    {
      "path": "docs/TASK-CONTRACTS.md",
      "class": "focused",
      "routes": ["task-governance"]
    },
    {
      "path": "docs/EXECUTOR-HANDOFFS.md",
      "class": "focused",
      "routes": ["task-governance"]
    },
    {
      "path": "docs/OPERATION-CONTRACTS.md",
      "class": "focused",
      "routes": ["operation-governance"]
    },
    {
      "path": "docs/OPERATIONAL-CONTRACTS.md",
      "class": "focused",
      "routes": ["operation-governance"]
    }
  ],
  "bootstrap_ratchet": {
    "reference": "T030-R2",
    "file_count": 2,
    "byte_size": 21471,
    "line_count": 298,
    "warning_relative_growth": 0.05,
    "blocking": false
  }
}
```
<!-- RCAB-MAP-V1:END -->

## Change policy

Changes to route semantics, classifications or ratchet values are Orchestrator-owned Markdown policy changes and require normal reviewed Git integration.

The generated manifest may be regenerated after such changes, but it cannot establish or change those semantics by itself.
