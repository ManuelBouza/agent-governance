# D037 — Deterministic code-only verification policy

Status: ACCEPTED  
Decision owner: Human Owner  
Applies to: Agent Governance source-product verification, regression, release gating and repository-owned eval strategy

## Context

Agent Governance previously planned a model-facing D032 capability baseline in T004. That work required real LLM sessions through an execution adapter and became coupled to model/provider/host compatibility before any Governance behavior could be observed.

The Human Owner has now explicitly decided to discard model-based tests and keep repository verification code-based.

This decision is broader than stopping one OpenCode experiment. It changes the source-product verification policy so correctness and release readiness do not depend on probabilistic model executions, model identifiers, provider availability, hosted inference, transcript grading or agent-host compatibility.

## Decision

Agent Governance source-product verification SHALL be **deterministic/code-first and model-independent**.

Repository-owned verification and release gates SHALL use only mechanisms whose expected result is mechanically reproducible from repository state and explicitly controlled fixtures, including the applicable subset of:

- ordinary deterministic unit/contract/regression tests;
- data-driven JSON/JSONL fixtures;
- deterministic test-local policy/classifier models;
- property/state-machine tests where justified;
- schema and protocol-version checks;
- exact identity/digest/provenance checks;
- filesystem/state/transition assertions;
- synthetic coexistence fixtures;
- static analysis and security scanners whose version/config/result contract is recorded;
- dependency/advisory/configuration verifiers;
- runbook precondition/postcondition checks;
- deterministic or bounded technical probes against explicitly authorized systems when D033–D036 later govern them;
- Human/ChatGPT architectural review for judgments that cannot honestly be reduced to code.

Repository verification SHALL NOT require or use:

- live LLM/model calls;
- repeated probabilistic agent trials;
- model-as-judge graders;
- transcript scoring from generated model responses;
- provider/model availability as a test prerequisite;
- OpenCode, another agent host or a hosted model as a release-gating dependency;
- statistical pass-rate thresholds over stochastic model behavior.

## Core invariant

```text
probabilistic implementation assistant != verification authority

source-product acceptance = deterministic evidence + authorized Human/Orchestrator judgment
```

An AI model may still help a Human/Executor design or implement work under Agent Governance, but its generated response is not itself a repository test oracle and the source product does not need to call another model to prove correctness.

## What this means for D032

D032 remains accepted architecture.

Its engineering invariants are verified as **policy/contract semantics**, not as empirical claims about arbitrary LLM behavior.

T003 remains the accepted deterministic D032 foundation. Its synthetic corpus and code tests cover mechanically representable properties such as:

- presentation-register variants retaining the same engineering identity/controls;
- exact code-native token preservation in the contract fixture;
- material versus baseline quality routing;
- independent privacy routing;
- mandatory security triage in synthetic implementation scopes;
- Primary Solution Diagram family selection;
- material-design-change diagram refresh invalidation;
- Core/version/module consistency.

D037 supersedes the T003 statement that a later task must prove these semantics with model-facing trials.

Agent Governance SHALL NOT claim that an arbitrary model empirically satisfies D032 merely because the deterministic contract passes. The product claim is narrower and more rigorous:

> Agent Governance defines and mechanically verifies the required governance contract. Correct operation by a particular AI runtime depends on that runtime following the supplied contract and is not independently certified by repository LLM trials.

## Handling semantic judgments that are not reducible to code

When a requirement cannot be proven honestly with deterministic checks, use this order:

1. normalize the requirement into explicit contract facts when that preserves meaning;
2. verify all mechanically provable invariants in code;
3. leave genuinely qualitative architecture/acceptance judgment to Human Owner / ChatGPT review;
4. record the limitation rather than introducing a probabilistic grader.

Do not create a fake deterministic proxy that silently changes the meaning of the requirement merely to obtain a green test.

## Primary Solution Diagram

Dominant question: verification dependency and authority after removing the model-facing layer.

Preferred view: compact flow/dependency.

```text
Normative Governance Core / accepted decisions
                  │
                  ▼
         explicit test contracts
         + synthetic fixtures
                  │
                  ▼
      deterministic code verifiers
  unit · contract · state · security
  provenance · coexistence · runbook
                  │
          ┌───────┴────────┐
          ▼                ▼
    mechanical PASS   mechanical FAIL
          │                │
          ▼                ▼
 Human/ChatGPT review   rework/block
 for irreducible        with evidence
 semantic judgment
          │
          ▼
       acceptance

NO live LLM/provider/agent-host dependency in verification
```

## T004 disposition

T004 — `docs/tasks/T004-d032-agent-facing-capability-eval.md` — is terminated by explicit Human Owner decision.

Disposition: `CANCELLED_BY_HUMAN`.

Rules:

- do not continue R1/R2/R3;
- do not run additional model/provider/OpenCode trials;
- do not integrate the partial `eval/d032-agent-capability` implementation branch;
- do not create `T004-baseline.jsonl` later merely to complete the historical contract;
- preserve T004 reviews/handoffs/branch history as non-authoritative audit evidence of the abandoned experiment;
- no T004 implementation PR is authorized;
- T004 may be reopened only by a new explicit Human Owner decision that supersedes D037.

The partial harness/adapter code on the unmerged T004 topic branch is not source-product state and SHALL NOT be used as a release dependency.

## Testing-strategy precedence

This decision supersedes any earlier text in `docs/TESTING-AND-EVALUATION.md`, T003, T004 or related planning that requires, recommends or permits live model/agent evals as source-product verification or release gates.

The useful deterministic portions of `docs/TESTING-AND-EVALUATION.md` remain in force, including:

- deterministic policy tests;
- property/state-machine testing when justified;
- adapter/installation/coexistence contract tests using synthetic fixtures;
- security/adversarial verification;
- provenance/identity checks;
- deterministic release gates.

Any sections describing Skill trigger trials, behavioral model trials, transcript review, repeated stochastic runs or model-based graders are historical/non-operative under D037 until the document is consolidated.

## Skills and runtime behavior

D037 does not prohibit Agent Skills or AI executors from being part of the product workflow.

It prohibits making **live probabilistic execution** the mechanism by which the repository decides whether its own governance contract is correct.

For Skills, code may verify the deterministic surfaces available to the repository, such as:

- required metadata and structure;
- source identity/digest;
- allowed dependencies/permissions;
- collision/precedence rules represented in fixtures;
- install/bootstrap footprints;
- managed-surface preservation;
- deterministic routing inputs when explicit facts are available.

The repository SHALL NOT claim statistically measured trigger accuracy without running such trials; under D037, that claim is simply outside the source-product verification contract.

## Security relationship

D037 strengthens D035 rather than weakening security verification.

Security-sensitive implementation/configuration remains subject to current/versioned security authority plus independent technical verification. Suitable deterministic verifiers may query actual authorized state, run scanners/checklists, validate versions/configuration and test known-bad regressions.

The prohibition is against using an LLM's opinion or stochastic behavior as the security gate, not against active deterministic technical verification.

## D033–D036 relationship

The next implementation frontier after D037 is the deterministic integration of:

- D033 execution authorization;
- D034 runbook-first terminal-neutral execution;
- D035 security authority/freshness/independent verification;
- D036 existing-system assurance audit.

That work SHALL use code-testable contracts and synthetic fixtures first. Real-system probes, when later needed for assurance/configuration verification, must be deterministic/bounded technical operations governed by D033/D034; they are not model evals.

## Quality implications

- **Correctness — MATERIAL:** deterministic tests must preserve actual contract meaning; no false proxy green.
- **Architecture — MATERIAL:** model/provider/host is removed from verification authority and release dependencies.
- **Security — MATERIAL:** security gates rely on current authoritative controls and independent technical evidence, never model judgment.
- **Reliability — MATERIAL:** tests must be repeatable and fail closed.
- **Testability — MATERIAL:** repository verification must run without network/model credentials unless a specific authorized technical system assessment requires network state.
- **Supply chain — MATERIAL:** no inference provider/agent host becomes a release dependency.
- **Cost — IMPROVED:** ordinary verification has no model-token/provider usage cost.

## Acceptance consequences

From D037 onward:

1. no new Task Contract may require live LLM calls for source-product acceptance without a new Human Owner decision superseding D037;
2. release gates must be mechanically reproducible;
3. semantic Human/ChatGPT review may complement but not masquerade as a code test;
4. unsupported probabilistic-runtime claims must be stated as limitations, not inferred from deterministic fixtures;
5. T004 remains cancelled and unintegrated;
6. the next source-product implementation task may proceed from the D033–D036 architecture frontier using deterministic code verification.
