# Governance / Skill Agent Evals

This directory contains agent-facing evaluations of behavior intrinsic to the Governance product.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown executable eval definitions, fixtures, harness inputs, eval execution, and verification evidence under `evals/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product behavior/invariants that evals must measure. The executor must not modify evals to redefine the approved contract.

For behavior-preserving refactors, eval cases accepted as part of the RF1 characterization baseline are frozen for that refactor unit unless ChatGPT explicitly authorizes a correction.

## In scope

- Governance Skill trigger/near-miss behavior;
- cold-start reconstruction from synthetic governed fixtures;
- context routing/progressive disclosure behavior;
- handoff and blocker interpretation;
- portability across compatible agent adapters;
- discovery-vs-artifact-trust interpretation;
- refusal to treat unaudited Skills as approved;
- semantic characterization needed to verify behavior-preserving Core/Skill refactors when deterministic checks alone are insufficient.

## Out of scope

- coding-agent benchmarks;
- quality/speed of application task implementation;
- real business tasks.

Synthetic task records may be used only as minimal fixtures necessary to observe governance behavior.

Eval results should record the exact Governance revision, Skill revision, executor product/model/configuration, and fixture revision so behavioral changes are attributable.
