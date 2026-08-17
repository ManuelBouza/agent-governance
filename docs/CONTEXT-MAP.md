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
| `unified-program` | D044 unified Governance architecture/program sequencing | `docs/decisions/D044-unified-governance-skill-architecture.md`, `docs/UNIFIED-GOVERNANCE-REFACTOR-PLAN.md` |
| `skill-capability` | routine capability lookup, intent ownership, profile/risk/context routing, topology-neutral projection lookup | `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`, `docs/CAPABILITY-CATALOG.md` |
| `capability-authoring` | changing capability identity/model/metadata rules or semantic clustering | `docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md`, `docs/CAPABILITY-SOURCE-CONTRACT.md`, `docs/CAPABILITY-CATALOG.md` |
| `consumer-routing-design` | reviewing/changing topology-neutral Consumer L1/L2 guard, routing or projection-mapping semantics | `docs/CAPABILITY-CATALOG.md`, `docs/CONSUMER-L1-GUARD-SPEC.md`, `docs/CONSUMER-L1-ROUTING-CONTRACT.md`, `docs/CONSUMER-L2-PROJECTION-MAPPING-CONTRACT.md` |
| `conformance-authoring` | D052 oracle ownership, freeze/revision or semantic conformance asset design | `docs/decisions/D052-specification-owned-conformance-test-authorship.md`, `docs/CONFORMANCE-ORACLE-CONTRACT.md` |
| `icae-rcab` | assurance design, context architecture, context budgets/projections | `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`, `docs/AGENT-CAPABILITY-ENGINEERING.md`, `docs/CONTEXT-ARCHITECTURE.md`, this map |
| `task-governance` | authoring/reviewing executor Task Contracts and handoffs | `docs/TASK-CONTRACTS.md`, `docs/EXECUTOR-HANDOFFS.md` |
| `operation-governance` | repository operations/cleanup and durable receipts | `docs/OPERATION-CONTRACTS.md`, `docs/OPERATIONAL-CONTRACTS.md` |

The table is intentionally small. The active checkpoint and current Task/Operational Contract select exact task, review, handoff, learning, release or evidence files only when needed.

For ordinary capability lookup, prefer `skill-capability`; load `CAPABILITY-SOURCE-CONTRACT.md` only when changing the capability model itself. This keeps routine routing on the compact catalog instead of the authoring contract.

Use `consumer-routing-design` for stable Consumer semantic routing contracts. Add `docs/CONSUMER-V1-SEMANTIC-TRACEABILITY.md` only for v1 preservation/equivalence review, and add the progressive-disclosure/reference-candidate documents only when comparing information placement or R* boundaries. They are intentionally not part of the default stable route.

The capability/routing routes deliberately exclude D051/D052 by default. Load D051 only when installation/package semantics are material and D052 only when conformance/test-authorship semantics are material.

The `conformance-authoring` route deliberately excludes `docs/TASK-CONTRACTS.md` and the full testing/eval strategy by default. Add `task-governance` when binding an oracle to a concrete executable task. Load testing/eval/provider/host material only when the selected assurance plane requires it.

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
      "path": "docs/decisions/D050-canonical-capability-source-and-evaluated-skill-topology.md",
      "class": "focused",
      "routes": ["skill-capability", "capability-authoring"]
    },
    {
      "path": "docs/CAPABILITY-CATALOG.md",
      "class": "focused",
      "routes": ["skill-capability", "capability-authoring", "consumer-routing-design"]
    },
    {
      "path": "docs/CAPABILITY-SOURCE-CONTRACT.md",
      "class": "focused",
      "routes": ["capability-authoring"]
    },
    {
      "path": "docs/CONSUMER-L1-GUARD-SPEC.md",
      "class": "focused",
      "routes": ["consumer-routing-design"]
    },
    {
      "path": "docs/CONSUMER-L1-ROUTING-CONTRACT.md",
      "class": "focused",
      "routes": ["consumer-routing-design"]
    },
    {
      "path": "docs/CONSUMER-L2-PROJECTION-MAPPING-CONTRACT.md",
      "class": "focused",
      "routes": ["consumer-routing-design"]
    },
    {
      "path": "docs/decisions/D052-specification-owned-conformance-test-authorship.md",
      "class": "focused",
      "routes": ["conformance-authoring"]
    },
    {
      "path": "docs/CONFORMANCE-ORACLE-CONTRACT.md",
      "class": "focused",
      "routes": ["conformance-authoring"]
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

Under D049, changing this live registry does not require an incidental refresh of the committed historical RCAB snapshot. Live RCAB state must be computed from this current map and registered files; explicit snapshot-vs-live currentness may therefore report the historical snapshot as stale.