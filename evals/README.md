# Governance / Skill Agent Evals

This directory contains agent-facing evaluations of behavior intrinsic to the Governance product.

The normative eval architecture, external references, isolation rules, grader selection, fixture policy, repeated-trial requirements, and release thresholds live in `../docs/TESTING-AND-EVALUATION.md`. The repository-owned harness language decision is `../docs/decisions/D023-python-testing-stack.md`. Skill/capability boundaries are defined by `../docs/TESTING-SKILL-CAPABILITIES.md` and D024. D052 authorship modes are defined by `../docs/decisions/D052-specification-owned-conformance-test-authorship.md`; oracle ownership/freeze/revision/`ORACLE_DEFECT` mechanics live in `../docs/CONFORMANCE-ORACLE-CONTRACT.md`. Ecosystem/SDD/Skill coexistence is defined by `../governance-core/COEXISTENCE.md` and D026.

## Harness language

Repository-owned eval harness/orchestration code SHOULD use Python `>=3.13` by default so deterministic checks, fixture manipulation, subprocess/tool traces, and behavioral eval orchestration share one language.

This decision does not select any model-provider SDK, hosted eval platform, executor CLI, or environment manager. Those are separate toolchain decisions. Language-specific adapter glue is allowed only when the target system cannot be exercised cleanly from the Python harness.

## Skill/capability boundary

The eval harness itself does not require an Agent Skill to run.

When the Maintainer Skill is available, it is the project-owned top-level Skill for source eval maintenance and should progressively route to Skill/eval or security testing context as needed. Do not create a separate generic eval/testing Skill merely to invoke the harness.

External Skill-authoring/evaluation/security Skills may be supplemental only after approval. Their generated prompts, reports, or candidate assertions do not replace repository-owned eval cases, traces, graders, or ChatGPT review.

## D052 ownership boundary

When a Task Contract selects `orchestrator-conformance` or `mixed`, exact Orchestrator-owned eval-oracle assets MUST be identified by that contract/gate. Their semantic lifecycle, freeze/revision rules, mechanical-correction boundary and `ORACLE_DEFECT` handling are defined only in `../docs/CONFORMANCE-ORACLE-CONTRACT.md`; do not duplicate or reinterpret them here.

The Agente de IA Ejecutor still owns eval execution, clean-session/environment orchestration, host/model/provider adapters, technical harness plumbing, traces, measurements, aggregation, supplementary exploratory/adversarial cases, and implementation-focused eval/test work unless an exact asset is designated as Orchestrator-owned oracle material.

Required frozen oracle cases and supplementary Executor cases MUST remain distinguishable in evidence.

## Eval rules

- every behavioral trial starts from clean disposable state;
- record the exact Governance revision, relevant Skill revision, executor product/model/configuration, fixture revision, grader version, outcome, and relevant trace evidence;
- grade observable outcomes/tool/file traces rather than agent self-report;
- use deterministic graders for mechanical assertions and model graders only when semantic interpretation requires them;
- repeated trials are required for probabilistic behavior;
- representative transcripts and failures must be inspected during release review;
- when a D052 frozen oracle applies, execute that exact revision and keep required versus supplementary cases separate.

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
- refusal to treat unaudited, changed, revoked, mismatched, or shadowed Skills as approved;
- operation without access to the canonical source repository after installation;
- refusal to activate for source-product maintenance tasks;
- refusal to activate as a generic SDD/planning/testing Skill merely because Gentle-AI-like, Spec Kit-like, OpenSpec-like or custom SDD artifacts are present;
- reuse/adapt behavior when an existing SDD owns specs/plans/tasks;
- no-SDD operation without proposing an unnecessary SDD install;
- `CONFLICT` behavior when another governance/orchestration Skill claims equivalent authority;
- preservation of third-party managed instruction/config surfaces.

### Maintainer Skill
- source-product maintenance trigger positives, negatives, and near misses;
- fixed train/validation trigger partitions;
- repeated trigger trials;
- correct routing to PD/RF, branch, release, Core, tests, and eval context;
- correct routing to the smallest relevant testing capability area defined by D024;
- correct ChatGPT Orchestrator / Agente de IA Ejecutor role interpretation;
- refusal to treat ordinary consumer-project governance as source maintenance;
- refusal to create a live consumer `.agent-coordination/` instance in this repository.

### Ecosystem coexistence behavior

Use synthetic fixtures modeled on public integration shapes rather than real user projects.

Minimum behavioral cases include:
- Gentle-AI-like environment: recognizes existing SDD/testing/registry capabilities and recommends reuse/adaptation rather than duplicate installation;
- Spec Kit-like environment: references existing spec/plan/tasks while retaining Governance readiness/Skill-trust/disclosure semantics;
- OpenSpec-like environment: treats existing specs/change artifacts as native project evidence rather than regenerating them;
- custom SDD: classifies capability boundaries from observed behavior/artifacts without requiring product recognition;
- no SDD: continues through Governance lifecycle without trying to install one;
- same-name Skill collision: distinguishes runtime precedence from approval and rejects an unapproved shadowing artifact;
- semantic Skill overlap: blocks rather than letting two governance/orchestration Skills both claim authority;
- managed-file collision: refuses blind overwrite and routes to bounded integration or `CONFLICT`;
- current-task disclosure: loads only native SDD artifacts referenced by the current Governance task, not the full external work backlog.

### Cross-product semantics
- semantic characterization needed to verify behavior-preserving Core/Skill refactors when deterministic checks alone are insufficient;
- explicit near-miss cases proving that Maintainer and Consumer Skills do not collapse into one broad trigger surface;
- explicit near-miss cases proving Consumer Governance does not collapse into generic SDD/planning/orchestration Skills;
- supported adapter/platform portability without assuming equivalent behavior across products.

### Security/adversarial behavior
- malicious natural-language Skill instructions;
- undeclared filesystem/network/process behavior where executable fixtures support it;
- spoofed/lookalike provenance;
- digest/revision/dependency/permission drift;
- same-name malicious project Skill shadowing a previously approved user Skill;
- unpinned/drifted external instructions;
- sandbox/isolation expectations;
- cross-platform security differences.

High-risk dynamic cases run only in disposable environments without production credentials or production service access.

## Sequential-disclosure observation

Synthetic future-task fixtures MAY contain canary markers so the harness can inspect observable file/tool traces for premature reads.

This is an Agent Governance-specific technique built on established trace/outcome verification practice; it is not represented as an external standard.

Coexistence fixtures MAY also place canaries in future native-SDD task artifacts to verify that adaptation does not become a route around Governance sequential disclosure.

## Out of scope

- coding-agent benchmarks;
- quality/speed of application task implementation;
- real business tasks;
- installing live Gentle-AI, Spec Kit, OpenSpec or another SDD product merely to run ordinary release evals.

Synthetic task records may be used only as minimal fixtures necessary to observe governance behavior.
