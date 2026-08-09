# Governance / Skill Agent Evals

This directory is for agent-facing evaluations of behavior intrinsic to the Governance product.

## Agent ownership

Codex is the normal write owner of executable eval definitions, fixtures, harness inputs, and eval execution under `evals/`.

ChatGPT owns Markdown instructions/specifications in this directory and defines the product behavior/invariants that evals must measure. Implementation Executors may inspect evals read-only but must not modify them to accommodate implementation behavior.

Eval failure routing follows `docs/DEVELOPMENT-WORKFLOW.md` and `docs/REFACTORING-WORKFLOW.md`: implementation defects return to the Implementation Executor, test/eval defects to Codex, and product-contract ambiguity to ChatGPT.

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

Eval results should record the exact Governance revision, Skill revision, agent product/model/configuration and fixture revision so behavioral changes are attributable.
