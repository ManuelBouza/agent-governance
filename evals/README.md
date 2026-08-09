# Governance / Skill Agent Evals

This directory contains agent-facing evaluations of behavior intrinsic to the Governance product.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown executable eval definitions, fixtures, harness inputs, eval execution, and verification evidence under `evals/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product behavior/invariants that evals must measure. The executor must not modify evals to redefine the approved contract.

For behavior-preserving refactors, eval cases accepted as part of the RF1 characterization baseline are frozen for that refactor unit unless ChatGPT explicitly authorizes a correction.

## Eval surfaces

### Consumer Governance Skill
- install/bootstrap activation;
- consumer trigger positives, negatives, and near misses;
- cold-start reconstruction from synthetic governed fixtures;
- context routing/progressive disclosure behavior;
- handoff and blocker interpretation;
- portability across compatible agent adapters;
- discovery-vs-artifact-trust interpretation;
- refusal to treat unaudited Skills as approved;
- operation without access to the canonical source repository after installation;
- refusal to activate for source-product maintenance tasks.

### Maintainer Skill
- source-product maintenance trigger positives, negatives, and near misses;
- correct routing to PD/RF, branch, release, Core, tests, and eval context;
- correct ChatGPT Orchestrator / Agente de IA Ejecutor role interpretation;
- refusal to treat ordinary consumer-project governance as source maintenance;
- refusal to create a live consumer `.agent-coordination/` instance in this repository.

### Cross-product semantics
- semantic characterization needed to verify behavior-preserving Core/Skill refactors when deterministic checks alone are insufficient;
- explicit near-miss cases proving that maintainer and consumer Skills do not collapse into one broad trigger surface.

## Out of scope

- coding-agent benchmarks;
- quality/speed of application task implementation;
- real business tasks.

Synthetic task records may be used only as minimal fixtures necessary to observe governance behavior.

Eval results should record the exact Governance revision, relevant Skill revision, executor product/model/configuration, and fixture revision so behavioral changes are attributable.
