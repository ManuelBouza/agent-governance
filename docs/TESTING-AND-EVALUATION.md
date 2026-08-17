# Testing and Evaluation Strategy

Status: ACTIVE

## Purpose

Define how the Agent Governance product is verified with deterministic code tests, state-machine/property tests, agent-facing evals, ecosystem-coexistence tests, and security/supply-chain checks.

This strategy validates the Governance Core, the Consumer Governance Skill, and the Maintainer Skill. It does **not** benchmark the quality of application code produced in consumer projects.

## Core principle

Use the least probabilistic verifier that can correctly prove the property under test:

1. deterministic code checks for mechanical invariants;
2. property/state-machine testing for large transition spaces;
3. agent evals only for behaviors that depend on model interpretation, triggering, routing, coexistence classification, or portability;
4. human/Orchestrator review for architectural or semantic judgments that cannot be reduced safely to code.

A model-based grader MUST NOT replace a deterministic check when the same property can be verified reliably by code.

## Skill/capability execution rule

`docs/TESTING-SKILL-CAPABILITIES.md` and D024 define the Skill boundary for this strategy.

The repository test/eval suites MUST remain executable without any Agent Skill or external SDD system installed or activated. Skills may provide specialized routing and procedural context, but the suite itself is code and repository state remains authoritative.

When available, the source-product Maintainer Skill is the only project-owned top-level Skill that should activate for source test/eval maintenance. It progressively routes to deterministic, property/state-machine, Skill/eval, coexistence, or security/supply-chain capability context as needed.

Do not create a generic pytest/testing/TDD Skill merely to run the approved stack. External authoring/evaluation/security Skills are supplemental only after the applicable supply-chain/coexistence approval and cannot replace repository-owned verification.

## Test authorship and semantic-oracle rule

D052 defines authorship of repository-owned tests/evals when ownership is material.

Three modes are supported:

- `orchestrator-conformance`: ChatGPT authors the required acceptance/conformance oracle; the executor executes it and may add supplementary technical tests.
- `executor-implementation`: the executor authors technical tests/evals and executes them inside the ChatGPT-owned Task Contract/acceptance boundary.
- `mixed`: ChatGPT authors the semantic conformance oracle while the executor authors implementation/exploratory tests and executes both classes.

Agent Skill, governance/policy and documentation-managed protocol work should normally use `orchestrator-conformance` or `mixed` when ChatGPT owns the correctness semantics. Ordinary consumer-application implementation remains `executor-implementation` by default.

Orchestrator-owned conformance assets may include approved assertions, positive/negative/near-miss/cross-profile/ambiguous cases, expected classifications/outcomes, frozen corpora/holdouts, semantic negative controls, thresholds represented as data, golden fixtures, security acceptance cases and deterministic grader expectations.

The executor remains responsible for execution, environment/harness mechanics, diagnostics, implementation tests, property/fuzz exploration, supplementary edge/adversarial cases, traces, result aggregation and evidence.

A conformance test is an executable projection of its controlling Core/Decision/Task Contract, not normative authority. If an executor identifies a semantic oracle defect, it reports an `ORACLE_DEFECT`-equivalent blocker with evidence rather than changing expected semantics. Mechanical corrections require durable authorization and must preserve meaning.

## Ecosystem coexistence test rule

D026 and `governance-core/COEXISTENCE.md` define how consumer Governance interacts with pre-existing SDD, Skills, registries, memory, permissions, testing and other project capabilities.

Tests/evals MUST validate the generic capability/ownership behavior, not make third-party products release dependencies.

Therefore:
- use synthetic fixtures modeled on documented public integration shapes;
- test `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` outcomes;
- verify references/adapters are preferred over duplicate native specs/plans/tasks;
- verify same-name host Skill precedence is distinguished from artifact approval;
- verify semantic governance/orchestration overlap fails closed;
- verify third-party managed instruction/config surfaces are preserved;
- include no-SDD/no-third-party-Skill fixtures;
- do not require live Gentle-AI, Spec Kit, OpenSpec or another external system for ordinary release regression.

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

### Skill trigger accuracy, collisions and overfitting control

Agent Skills — `Optimizing skill descriptions`
https://agentskills.io/skill-creation/optimizing-descriptions

Agent Skills — `How to add skills support to your agent`
https://agentskills.io/client-implementation/adding-skills-support

Relevant guidance:
- `description` is the primary activation mechanism;
- evaluate both `should_trigger` and `should_not_trigger` cases;
- run queries multiple times because activation is probabilistic;
- keep a fixed train/validation split (the optimization guide proposes roughly 60/40) to avoid optimizing only for known prompts;
- false-positive near-boundary cases are especially important when descriptions overlap;
- project/user Skill clients should apply deterministic name-collision precedence and surface warnings;
- project-level Skills commonly override same-name user-level Skills.

Adoption in this repository:
- Consumer and Maintainer Skills MUST have separate trigger corpora;
- Consumer corpora MUST also include generic SDD/planning/orchestration near misses;
- corpora MUST include positives, negatives, and near misses;
- trigger evaluation MUST use repeated trials and a fixed holdout/validation set;
- same-name Skill shadowing tests separate runtime selection from Governance approval;
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
- claims such as "state recovered", "existing SDD reused", "managed file preserved", or "future task not read" require observable evidence from state/tool/file traces, not self-report.

### Policy-as-code testing pattern

Open Policy Agent — `Policy Testing`
https://www.openpolicyagent.org/docs/policy-testing

OPA documents policy-as-code as codifying system requirements and testing those policy rules with explicit allowed/denied inputs, including data-driven cases, mocking and coverage.

Adoption in this repository:
- Agent Governance borrows the **policy testing pattern**, not the OPA runtime;
- protocol rules such as legal transitions, blockers, authority constraints, coexistence classifications, reference requirements and install validation are expressed as deterministic inputs -> expected decisions where semantics permit;
- no Rego/OPA dependency is required unless future evidence justifies it.

### Property and state-machine testing

Hypothesis — `Stateful tests`
https://hypothesis.readthedocs.io/en/latest/stateful.html

Relevant sections:
- lines 43–55: stateful testing generates entire tests/sequences of primitive actions and searches for sequences that produce a failure;
- rule-based state machines chain operations across evolving state rather than testing each input independently.

Adoption in this repository:
- use property/state-machine tests for lifecycle/task/EXCHANGE transition spaces that are impractical to enumerate manually;
- candidate invariants include monotonic sequence numbers, blocker disclosure rules, dependency readiness, terminal-state behavior, non-creation of strategic decisions by derived state, and invalidation of capability/Skill selection after material provider drift;
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
- runtime-selected/shadowed Skill identity must still match the approved artifact;
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
- malicious/adversarial Skill fixtures exercise prompt/instruction abuse, path/permission overreach, dependency drift, digest drift, spoofed provenance, same-name shadowing and external-reference drift;
- dynamic security tests run in disposable isolated fixtures with no production credentials;
- marketplace/directory/registry scan results are supplemental evidence only.

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
- CAPABILITIES inventory structure/non-authority constraints;
- sequential disclosure metadata;
- canonical source/revision/digest matching;
- host-selected Skill identity vs approved artifact;
- approval/revocation/dependency/permission envelope checks;
- bootstrap/archive overwrite and managed-file safety rules.

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
- approval identity cannot remain valid after material artifact/dependency/permission drift;
- material capability/provider/selected-artifact drift cannot leave stale coexistence approval silently valid.

No discovered counterexample may remain unexplained at release.

### Layer 3 — Adapter/installation/coexistence contract tests

Synthetic fixtures prove:
- installed footprint generation and validation;
- source-repository independence after Consumer Skill installation;
- adapter-neutral semantics;
- at least two supported executor/adapter configurations at stable-release gates;
- Maintainer Skill cannot initialize a live consumer instance in the source repository;
- no-SDD/no-third-party-Skill bootstrap works;
- existing SDD/spec/task ownership is referenced/adapted rather than duplicated;
- same-name Skill precedence is observable but cannot replace exact artifact approval;
- third-party managed instructions/configuration are preserved or installation fails closed;
- `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` records cannot create authority by themselves.

### Layer 4 — Skill trigger evals

Maintain separate Consumer and Maintainer corpora.

Each corpus contains:
- positive cases;
- negative cases;
- near misses against the other Skill and adjacent generic coding/planning/SDD/orchestration tasks;
- fixed train and validation partitions;
- repeated trials per query.

Store the exact Skill revision and executor/model/configuration for every run.

Initial threshold policy is defined in the release-gate section below and MAY be tightened using empirical results. Thresholds are Agent Governance policy, not universal standards from Agent Skills.

### Layer 5 — Governance behavioral/coexistence evals

Use isolated synthetic repositories/sessions for behaviors such as:
- cold-start reconstruction with no chat history;
- progressive context loading/routing;
- stale STATE detection and reconstruction;
- handoff interpretation;
- blocker handling;
- one-task-at-a-time sequential disclosure;
- discovery-vs-artifact-trust behavior;
- refusal to treat unaudited/changed/shadowed Skills as approved;
- consumer operation with no access to the canonical source repository;
- reuse/adaptation of compatible native SDD/spec/task artifacts;
- refusal to install an SDD framework when none is needed;
- semantic `CONFLICT` for competing governance/orchestration authority;
- managed-file preservation;
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
- same-name malicious project Skill shadowing an approved user Skill;
- unpinned/drifted external instructions;
- unsafe configuration/serialization cases where supported;
- cross-platform permission differences.

High-risk dynamic cases run only in disposable isolated environments without production credentials or production service access.

## Synthetic fixture policy

Fixtures model governance protocol states and ecosystem boundaries, not application implementation quality.

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
- same-name project/user Skill shadowing fixture;
- Gentle-AI-like capability/registry fixture;
- Spec Kit-like spec/plan/tasks fixture;
- OpenSpec-like specs/change fixture;
- generic custom-SDD fixture;
- no-SDD/no-third-party-Skill fixture;
- shared managed-instruction/config collision fixture;
- source-product repository fixture for Maintainer Skill routing.

Named external-system fixtures reproduce only the public integration shape needed for the test. Ordinary release regression does not install or execute the real external product.

Real business repositories and production services are not test dependencies.

## Sequential-disclosure observation

Agent Governance MAY use canary markers in synthetic future-task fixtures and inspect observable file/tool access traces to prove that future task content was not read prematurely.

This **canary design is an Agent Governance-specific test technique**, not an externally standardized technique. It is an application of trace/tool-call/outcome verification described in agent-evaluation practice.

Coexistence fixtures MAY place canaries in future native-SDD task artifacts to verify that adaptation does not become a route around Governance disclosure rules.

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
3. supply-chain exact identity/digest/revocation/host-selection checks: **100% pass**;
4. release-blocking coexistence fixtures: expected `REUSE|ADAPT|COEXIST|MISSING|CONFLICT` outcomes and managed-file behavior **100% pass**;
5. security fixtures classified release-blocking: **100% rejected/contained as expected**;
6. cold-start/state/protocol mandatory behavioral cases: **100% pass across supported adapter fixtures**;
7. trigger validation set: target **>= 90% correct classification** and **<= 10% false-positive rate**, with no known systematic confusion between Maintainer, Consumer, or generic SDD/orchestration Skills;
8. repeated behavioral evals: record per-task success rate and investigate material run-to-run instability before release;
9. human/ChatGPT review: inspect representative transcripts and all release-blocking failures before acceptance.

Thresholds MAY be tightened after enough empirical data exists. Relaxing a release-blocking threshold requires a documented decision.

## Capability vs regression suites

- capability evals explore new/weak behaviors and may intentionally have lower pass rates;
- once a capability is accepted as supported behavior, its case moves into regression coverage;
- release-blocking regression behavior should approach deterministic reliability; persistent probabilistic failures require explicit product decision rather than silent tolerance.

## Ownership

Per D052 and `AGENTS.md`:
- ChatGPT Orchestrator owns this Markdown strategy, test/eval contracts, acceptance meaning and release interpretation;
- under `orchestrator-conformance` or the Orchestrator side of `mixed`, ChatGPT owns the designated non-Markdown conformance/oracle assets that directly encode its approved acceptance semantics;
- the Agente de IA Ejecutor owns implementation-focused tests/evals, supplementary fixtures/cases, technical harness/adapters, execution and reproducible evidence, and all test/eval implementation under `executor-implementation`;
- the executor may improve a mechanically broken harness only within durable authorization and without redefining approved behavior;
- a suspected semantic oracle defect must be escalated with evidence rather than silently changed.

## Implementation constraint

Do not adopt heavy frameworks, external SDD products or extra Skills merely because they are referenced here.

Initial preference:
- standard Python test tooling for deterministic checks;
- Hypothesis only where generated/property/stateful coverage adds clear value;
- the Maintainer Skill, when available, routes to task-specific testing/eval context rather than acting as a test runner;
- no generic testing/pytest/TDD Skill is required for canonical execution;
- synthetic external-ecosystem fixtures before live compatibility dependencies;
- a small repository-owned eval harness before adopting a hosted eval platform;
- no OPA runtime solely to obtain policy tests;
- security scanners/dynamic tools and external Skills are supplemental and introduced only after supply-chain review and demonstrated need.

## Maintenance

Testing/eval suites are living product artifacts.

When a bug, ambiguity, security issue, portability failure, coexistence conflict, trigger collision, or regression is confirmed, add the smallest reproducible case to the appropriate suite before or with the fix whenever practical. D052 authorship mode determines who owns the semantic expected behavior; executor-discovered technical regressions may remain executor-authored when they do not redefine the acceptance oracle.

Review external references periodically because agent-evaluation, SDD tooling and Agent Skill security guidance are evolving quickly.
