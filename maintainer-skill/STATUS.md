# Maintainer Skill Status

Status: DESIGN-APPROVED / NOT YET RELEASED

This directory is reserved for the source-product Maintainer Skill defined in `../docs/MAINTAINER-SKILL-CONTRACT.md`.

The Maintainer Skill is one top-level source-maintenance Skill with two approved progressive-routing surfaces:

- **Orchestrator route** — strategy, architecture, Decision Records, Task Contracts, committed Markdown, review/acceptance, executor launch/handoff control, and Orchestrator checkpointing.
- **Executor route** — authorized non-Markdown implementation, deterministic tests/evals, verification execution, local toolchain context, and persisted executor handoff.

These routes do not create new governance roles or separate role-named Skills. D016 ownership remains authoritative, and both roles must retain their documented no-Skill bootstrap paths.

The final `SKILL.md` is intentionally not authored yet. Before implementation/release, finalize and test its activation description, positive/negative/near-miss trigger corpus, role-route selection and non-blending behavior, progressive-context routing, source-repository branch/workflow behavior, and interaction with the product-agnostic Agente de IA Ejecutor.

For implementation/refactoring/code-review work, the future Executor route SHOULD progressively load `../docs/AGENT-LEGIBLE-CODE-HEALTH.md` (or an equivalent packaged reference) rather than introducing a separate top-level generic coding Skill. Mechanical size/complexity/architecture checks remain repository tooling and MUST work when the Maintainer Skill is absent or disabled.

This Skill is for maintaining the canonical `agent-governance` repository only. It MUST NOT install or operate a live consumer governance instance here.
