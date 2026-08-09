# D014 — Source repository agent roles

Status: ACCEPTED
Authority: Human Owner

## Decision

Development of the `agent-governance` source repository uses role-separated agent ownership independent from the consumer governance protocol:

- ChatGPT is Orchestrator, architectural/specification owner, and exclusive normal author/editor of committed Markdown (`*.md`).
- OpenCode or another compatible Implementation Executor owns approved non-test implementation code/config/assets.
- Codex owns deterministic test/eval authoring, modification, and execution.
- The Human Owner retains final authority.

The source repository MUST NOT become a consumer instance of its own Governance Core. Real project implementations, missions, workplans, STATE/EXCHANGE records, and application code live in separate consumer repositories. Only synthetic fixtures required to test the product may model installed consumer footprints here.

## Rationale

The product repository has a different responsibility from repositories that consume the framework. Self-installing the consumer protocol would blur source-product decisions with example project state and create recursive governance ambiguity.

Separating Markdown specification, implementation, and verification write ownership also prevents one agent from silently changing the contract or weakening tests to make its own work pass.

## Consequences

- `AGENTS.md` defines normative role/write boundaries.
- Product-development workflow lives in `docs/DEVELOPMENT-WORKFLOW.md` rather than `.agent-coordination/`.
- OpenCode may use repository-specific mechanical permission restrictions, but task semantics remain executor-neutral.
- Green verification claimed by an Implementation Executor is not acceptance evidence until Codex runs the applicable tests/evals.
- Codex reports implementation defects instead of editing implementation code; executors report specification ambiguity instead of editing Markdown.
