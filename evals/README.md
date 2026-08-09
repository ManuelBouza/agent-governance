# Governance / Skill Agent Evals

This directory contains agent-facing evaluations of behavior intrinsic to the Governance product.

The normative eval architecture, external references, isolation rules, grader selection, fixture policy, repeated-trial requirements, and release thresholds live in `../docs/TESTING-AND-EVALUATION.md`.

## Agent ownership

The `Agente de IA Ejecutor` owns non-Markdown executable eval definitions, fixtures, harness inputs, eval execution, and verification evidence under `evals/`. The executor role is product agnostic: OpenCode, Codex, Claude Code, Antigravity, or another compatible coding agent may fulfill it.

ChatGPT owns committed Markdown instructions/specifications and defines the product behavior/invariants that evals must measure. The executor must not modify evals to redefine the approved contract.

For behavior-preserving refactors, eval cases accepted as part of the RF1 characterization baseline are frozen for that refactor unit unless ChatGPT explicitly authorizes a correction.

## Eval rules

- every behavioral trial starts from clean disposable state;
- record the exact Governance revision, relevant Skill revision, executor product/model/configuration, fixture revision, grader version, outcome, and relevant trace evidence;
- grade observable outcomes/tool/file traces rather than agent self-report;
- use deterministic graders for mechanical assertions and model graders only when semantic interpretation requires them;
- repeated trials are required for probabilistic behavior;
- representative transcripts and failures must be inspected during release review.

## Eval surfaces

### Consumer Governance Skill
- install/bootstrap activation;
- trigger positives, negatives, and near misses;
- fixed train/validation trigger partitions;
- repeated trigger trials;
- with-Skill vs no-Skill or previous-version baseline where meaningful;
- cold-start reconstruction from synthetic governed fixtures;
- context routing/progressive disclosure behavior;
- handoff and blocker interpretation;
- portability across compatible agent adapters;
- discovery-vs-artifact-trust interpretation;
- refusal to treat unaudited, changed, revoked, or mismatched Skills as approved;
- operation without access to the canonical source repository after installation;
- refusal to activate for source-product maintenance tasks.

### Maintainer Skill
- source-product maintenance trigger positives, negatives, and near misses;
- fixed train/validation trigger partitions;
- repeated trigger trials;
- correct routing to PD/RF, branch, release, Core, tests, and eval context;
- correct ChatGPT Orchestrator / Agente de IA Ejecutor role interpretation;
- refusal to treat ordinary consumer-project governance as source maintenance;
- refusal to create a live consumer `.agent-coordination/` instance in this repository.

### Cross-product semantics
- semantic characterization needed to verify behavior-preserving Core/Skill refactors when deterministic checks alone are insufficient;
- explicit near-miss cases proving that Maintainer and Consumer Skills do not collapse into one broad trigger surface;
- supported adapter/platform portability without assuming equivalent behavior across products.

### Security/adversarial behavior
- malicious natural-language Skill instructions;
- undeclared filesystem/network/process behavior where executable fixtures support it;
- spoofed/lookalike provenance;
- digest/revision/dependency/permission drift;
- unpinned/drifted external instructions;
- sandbox/isolation expectations;
- cross-platform security differences.

High-risk dynamic cases run only in disposable environments without production credentials or production service access.

## Sequential-disclosure observation

Synthetic future-task fixtures MAY contain canary markers so the harness can inspect observable file/tool traces for premature reads.

This is an Agent Governance-specific technique built on established trace/outcome verification practice; it is not represented as an external standard.

## Out of scope

- coding-agent benchmarks;
- quality/speed of application task implementation;
- real business tasks.

Synthetic task records may be used only as minimal fixtures necessary to observe governance behavior.
