# Testing and Evaluation Strategy

Status: ACTIVE

## Purpose

Define how the Agent Governance product is verified with deterministic code tests, state-machine/property tests, agent-facing evals, and security/supply-chain checks.

This strategy validates the Governance Core, the Consumer Governance Skill, and the Maintainer Skill. It does **not** benchmark the quality of application code produced in consumer projects.

## Core principle

Use the least probabilistic verifier that can correctly prove the property under test:

1. deterministic code checks for mechanical invariants;
2. property/state-machine testing for large transition spaces;
3. agent evals only for behaviors that depend on model interpretation, triggering, routing, or portability;
4. human/Orchestrator review for architectural or semantic judgments that cannot be reduced safely to code.

A model-based grader MUST NOT replace a deterministic check when the same property can be verified reliably by code.

## External technical basis

The following techniques are adopted from current specialized sources. The references below are normative research inputs for this testing strategy; Agent Governance may adapt them to its own protocol, but must not represent local adaptations as externally standardized techniques.

### Agent Skill structured evals

Agent Skills — `Evaluating skill output quality`
https://agentskills.io/skill-creation/evaluating-skills

Relevant sections:
- lines 45–78: test cases use realistic prompts, expected outputs, optional files, varied phrasing and edge cases;
- lines 83–140: compare `with_skill` against `without_skill` or a previous Skill version and start every run with clean context;
- lines 161–198: assertions should be objective where possible, and mechanical assertions should use verification scripts because scripts are more reliable than LLM judgment;
- lines 244–270: aggregate pass rate, timing and token deltas across runs;
- lines 287–324: combine automated results with human review and iterate using failures, feedback and transcripts.

Adoption in this repository:
- Consumer and Maintainer Skill evals use realistic prompts and isolated sessions;
- previous immutable Skill revisions are preferred baselines once a Skill exists;
- deterministic output/state assertions are graded by code;
- model/human grading is reserved for semantic behavior that cannot be proven mechanically.

### Skill trigger accuracy and overfitting control

Agent Skills — `Optimizing skill descriptions`
https://agentskills.io/skill-creation/optimizing-descriptions

Relevant guidance:
- `description` is the primary activation mechanism;
- evaluate both `should_trigger` and `should_not_trigger` cases;
- run queries multiple times because activation is probabilistic;
- keep a fixed train/validation split (the guide proposes roughly 60/40) to avoid optimizing only for known prompts;
- false-positive near-boundary cases are especially important when descriptions overlap.

Adoption in this repository:
- Consumer and Maintainer Skills MUST have separate trigger corpora;
- corpora MUST include positives, negatives, and near misses between the two Skills;
- trigger evaluation MUST use repeated trials and a fixed holdout/validation set;
- no Skill description is accepted from a single successful prompt.

### Agent eval harnesses, outcomes and graders

Anthropic — `Demystifying evals for AI agents` (2026-01-09)
https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Relevant techniques:
- define tasks, trials, graders, traces/transcripts, outcomes, harnesses and suites explicitly;
- run multiple trials because agent behavior varies between runs;
- combine code-based, model-based and human graders according to the property being measured;
- prefer deterministic graders where possible and use model graders where nuance is required;
- distinguish capability evals from regression evals; regression suites should approach 100% reliability;
- isolate each trial in a clean environment to avoid shared-state contamination;
- verify final environment outcomes rather than trusting the agent's statement that a task succeeded;
- read transcripts to distinguish agent failures from grader/harness defects.

Adoption in this repository:
- each agent eval records task, trial identity, fixture revision, Governance revision, Skill revision, executor product/model/configuration, outcome and grader results;
- regression suites are release gates; capability suites may be exploratory;
- fixtures are recreated/reset per trial;
- claims such as "state recovered" or "future task not read" require observable evidence from state/tool/file traces, not self-report.

### Policy-as-code testing pattern

Open Policy Agent — `Policy Testing`
https://www.openpolicyagent.org/docs/policy-testing

OPA documents policy-as-code as codifying system requirements and testing those policy rules with explicit allowed/denied inputs, including data-driven cases, mocking and coverage.

Adoption in this repository:
- Agent Governance borrows the **policy testing pattern**, not the OPA runtime;
- protocol rules such as legal transitions, blockers, authority constraints, reference requirements and install validation are expressed as deterministic inputs -> expected decisions;
- no Rego/OPA dependency is required unless future evidence justifies it.

### Property and state-machine testing

Hypothesis — `Stateful tests`
https://hypothesis.readthedocs.io/en/latest/stateful.html

Relevant sections:
- lines 43–55: stateful testing generates entire tests/sequences of primitive actions and searches for sequences that produce a failure;
- rule-based state machines chain operations across evolving state rather than testing each input independently.

Adoption in this repository:
- use property/state-machine tests for lifecycle/task/EXCHANGE transition spaces that are impractical to enumerate manually;
- candidate invariants include monotonic sequence numbers, blocker disclosure rules, dependency readiness, terminal-state behavior, and non-creation of strategic decisions by derived state;
- found counterexamples are reduced to reproducible regression tests where useful.

### Artifact provenance and immutable verification

SLSA v1.2 — `Build: Verifying artifacts`
https://slsa.dev/spec/v1.2/verifying-artifacts

Relevant guidance:
- verification means checking artifact provenance against predefined expectations;
- verify trusted identity/signature where available and expected build/external parameters;
- unrecognized material parameters should fail verification.

Adoption in this repository:
- Skill approval tests compare the exact canonical source/revision/content digest and approved dependency/permission envelope;
- changed artifact content or material execution envelope invalidates prior approval;
- Agent Governance does not claim full SLSA conformance merely by borrowing the provenance-verification pattern.

### Agent Skill security and dynamic testing

OWASP Agentic Skills Top 10 — checklist
https://owasp.org/www-project-agentic-skills-top-10/checklist.html

Relevant checklist items:
- AST03: explicit least-privilege permissions and scoped filesystem/network access;
- AST05: external references should be inventoried and, where relied on, pinned/reverified;
- AST06: isolation and restricted filesystem/network behavior should be verified dynamically;
- AST07: immutable content hashes, controlled updates and re-scanning;
- AST08: scan code and natural-language instructions separately; use isolated scanning and sandboxed dynamic behavioral testing; do not trust a single scanner as the sole gate;
- AST09: inventory, risk tier, approval record and invocation auditability;
- AST10: validate independently on each target platform rather than assuming equivalent security behavior.

Adoption in this repository:
- malicious/adversarial Skill fixtures exercise prompt/instruction abuse, path/permission overreach, dependency drift, digest drift, spoofed provenance and external-reference drift;
- dynamic security tests run in disposable isolated fixtures with no production credentials;
- marketplace/directory scan results are supplemental evidence only.

## Test architecture

### Layer 1 — Structural and deterministic policy tests

Use normal code tests for:
- repository/package layout;
- JSON/JSONL syntax and schemas/checks;
- direct references and protocol-version consistency;
- context-budget metadata;
- allowed actors/events;
- legal lifecycle/task transitions;
- blocker/dependency rules;
- STATE/EXCHANGE coherence and stale-state derivation;
- sequential disclosure metadata;
- canonical source/revision/digest matching;
- approval/revocation/dependency/permission envelope checks;
- bootstrap/archive overwrite and safety rules.

Expected release behavior: deterministic regression suite must pass 100%.

### Layer 2 — Property/state-machine tests

Use Hypothesis or an equivalent property-based engine for stateful protocol surfaces.

Minimum invariant families:
- sequence/event identifiers remain monotonic and valid;
- terminal task states do not illegally re-enter execution;
- BLOCKED prevents later-task disclosure;
- dependencies constrain READY consistently;
- STATE refresh derives from authority records/events and never invents strategy;
- invalid event sequences are rejected regardless of generated ordering;
- approval identity cannot remain valid after material artifact/dependency/permission drift.

No discovered counterexample may remain unexplained at release.

### Layer 3 — Adapter/installation contract tests

Synthetic fixtures prove:
- installed footprint generation and validation;
- source-repository independence after Consumer Skill installation;
- adapter-neutral semantics;
- at least two supported executor/adapter configurations at stable-release gates;
- Maintainer Skill cannot initialize a live consumer instance in the source repository.

### Layer 4 — Skill trigger evals

Maintain separate Consumer and Maintainer corpora.

Each corpus contains:
- positive cases;
- negative cases;
- near misses against the other Skill and adjacent generic coding/planning tasks;
- fixed train and validation partitions;
- repeated trials per query.

Store the exact Skill revision and executor/model/configuration for every run.

Initial threshold policy is defined in the release-gate section below and MAY be tightened using empirical results. Thresholds are Agent Governance policy, not universal standards from Agent Skills.

### Layer 5 — Governance behavioral evals

Use isolated synthetic repositories/sessions for behaviors such as:
- cold-start reconstruction with no chat history;
- progressive context loading/routing;
- stale STATE detection and reconstruction;
- handoff interpretation;
- blocker handling;
- one-task-at-a-time sequential disclosure;
- discovery-vs-artifact-trust behavior;
- refusal to treat unaudited/changed Skills as approved;
- consumer operation with no access to the canonical source repository;
- Maintainer routing to PD/RF/release/branch context.

Grade observable final state and traces. Do not rely on the agent claiming compliance.

### Layer 6 — Security/adversarial tests

Fixtures SHOULD include:
- malicious natural-language Skill instructions;
- scripts/hooks requesting undeclared effects;
- path traversal/symlink or filesystem-scope attempts where relevant;
- spoofed/lookalike provenance;
- changed digest/revision;
- changed dependency/permission envelope;
- unpinned/drifted external instructions;
- unsafe configuration/serialization cases where supported;
- cross-platform permission differences.

High-risk dynamic cases run only in disposable isolated environments without production credentials or production service access.

## Synthetic fixture policy

Fixtures model governance protocol states, not application implementation quality.

Minimum fixture families:
- empty/uninitialized consumer repo;
- F3 missing-Skill state;
- ready state;
- blocked state;
- stale STATE;
- malformed/truncated/duplicate-sequence EXCHANGE;
- minimal A -> B -> C tasks for sequential-disclosure mechanics;
- approved exact Skill artifact;
- changed/unapproved/malicious Skill artifact;
- source-product repository fixture for Maintainer Skill routing.

Real business repositories and production services are not test dependencies.

## Sequential-disclosure observation

Agent Governance MAY use canary markers in synthetic future-task fixtures and inspect observable file/tool access traces to prove that future task content was not read prematurely.

This **canary design is an Agent Governance-specific test technique**, not an externally standardized technique. It is an application of trace/tool-call/outcome verification described in agent-evaluation practice.

## Eval isolation and reproducibility

Every behavioral trial records at least:
- repository/fixture revision;
- Governance Core revision;
- relevant Skill revision;
- executor product and model/version where available;
- agent configuration/adapter;
- test prompt/task ID;
- clean-session/environment identifier;
- grader/assertion versions;
- result/outcome;
- relevant transcript/tool/file-access evidence;
- tokens/duration when available.

Trials MUST start from clean disposable state. Shared mutable state between trials is prohibited unless the test explicitly targets shared-state behavior.

## Initial release gates

These are project policy thresholds and MUST NOT be represented as industry-standard numeric thresholds.

Before a stable release:

1. deterministic regression tests: **100% pass**;
2. state-machine/property tests: **zero unresolved counterexamples** in the configured release run;
3. supply-chain exact identity/digest/revocation checks: **100% pass**;
4. security fixtures classified release-blocking: **100% rejected/contained as expected**;
5. cold-start/state/protocol mandatory behavioral cases: **100% pass across supported adapter fixtures**;
6. trigger validation set: target **>= 90% correct classification** and **<= 10% false-positive rate**, with no known systematic confusion between Maintainer and Consumer Skills;
7. repeated behavioral evals: record per-task success rate and investigate material run-to-run instability before release;
8. human/ChatGPT review: inspect representative transcripts and all release-blocking failures before acceptance.

Thresholds MAY be tightened after enough empirical data exists. Relaxing a release-blocking threshold requires a documented decision.

## Capability vs regression suites

- capability evals explore new/weak behaviors and may intentionally have lower pass rates;
- once a capability is accepted as supported behavior, its case moves into regression coverage;
- release-blocking regression behavior should approach deterministic reliability; persistent probabilistic failures require explicit product decision rather than silent tolerance.

## Ownership

Per `AGENTS.md`:
- ChatGPT Orchestrator owns this Markdown strategy, test/eval contracts, acceptance meaning and release interpretation;
- Agente de IA Ejecutor owns non-Markdown test/eval implementation, fixtures/data, harness code, execution and reproducible evidence;
- the executor may improve broken test implementation but may not redefine the approved behavioral contract without returning to ChatGPT.

## Implementation constraint

Do not adopt heavy frameworks merely because they are referenced here.

Initial preference:
- standard Python test tooling for deterministic checks;
- Hypothesis only where generated/property/stateful coverage adds clear value;
- a small repository-owned eval harness before adopting a hosted eval platform;
- no OPA runtime solely to obtain policy tests;
- security scanners/dynamic tools are supplemental and introduced only after supply-chain review and demonstrated need.

## Maintenance

Testing/eval suites are living product artifacts.

When a bug, ambiguity, security issue, portability failure, trigger collision, or regression is confirmed, add the smallest reproducible case to the appropriate suite before or with the fix whenever practical.

Review external references periodically because agent-evaluation and Agent Skill security guidance is evolving quickly.