# D014 — Source repository agent roles

Status: SUPERSEDED by D016
Authority: Human Owner

## Supersession

D016 replaces the three-agent/product-specific split introduced here. OpenCode, Codex, Claude Code, Antigravity, and similar coding agents are all implementations of one abstract `Agente de IA Ejecutor` role. The historical decision below is retained for traceability only.

## Historical Decision

Development of the `agent-governance` source repository used role-separated agent ownership independent from the consumer governance protocol:

- ChatGPT was Orchestrator, architectural/specification owner, and exclusive normal author/editor of committed Markdown (`*.md`).
- OpenCode or another compatible Implementation Executor owned approved non-test implementation code/config/assets.
- Codex owned deterministic test/eval authoring, modification, and execution.
- The Human Owner retained final authority.

The source repository MUST NOT become a consumer instance of its own Governance Core. Real project implementations, missions, workplans, STATE/EXCHANGE records, and application code live in separate consumer repositories. Only synthetic fixtures required to test the product may model installed consumer footprints here.

## Historical Rationale

The product repository has a different responsibility from repositories that consume the framework. Self-installing the consumer protocol would blur source-product decisions with example project state and create recursive governance ambiguity.

The additional distinction between implementation executor and Codex was later determined to be an incorrect product-identity distinction and is superseded by D016.
