# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O201  
Canonical-Branch: `develop`  
Current-Work-Unit: T054 adaptive subagent compute-routing pilot is accepted/integrated with formal outcome `NOT_QUALIFIED`; R006 and R007 are consciously `DEFERRED`; no global routing or D055 session-policy change is adopted  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: none

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling. Core protocol remains `1.15.0`.
- D057 research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md`.
- Canonical research ledger: `docs/RESEARCH-TRACEABILITY.md`.
- Research findings remain evidence rather than normative authority; persisted `Research-State` and `Decision-State` transitions control.
- T050 remains `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- D055 remains unchanged as the global Human-facing Executor launch-profile policy.

## T054 final state

T054 is **ACCEPTED as an execution** with frozen pilot decision **`NOT_QUALIFIED`**.

Authoritative records:

- Task Contract: `docs/tasks/T054-adaptive-subagent-compute-routing-pilot.md`;
- final review: `docs/reviews/T054-R1.md`;
- executor handoff: `handoffs/T054-executor-handoff.json`;
- telemetry: `handoffs/T054-adaptive-routing-telemetry.json`;
- submitted Executor HEAD: `e5b0988eead750c3e3228ed8a537226b9685944a`;
- implementation/evidence HEAD: `c19285cf67d97318d70f6e5edcf13ea65805f6c6`;
- evidence PR: `#277`;
- integrated evidence commit: `ffd21fc0c4002de7976581227849cc0d612cafaf`.

Formal score:

```text
CONTROL  2 / 3
ADAPTIVE 1 / 3 first attempt
adaptive diagnosis escalations 2
material false negatives 0
material false positives 0
verified effective adaptive profiles 0 / 3
```

### T054 probe interpretation

P1:

- CONTROL passed;
- requested `Luna / Low` ADAPTIVE failed exact physical-LOC semantics by using a line-count method that excluded blank lines;
- fresh permitted `Terra / Medium` diagnosis recovered the exact oracle;
- the first-attempt adaptive failure remains scored and is real negative evidence for this frozen `Luna / Low` task mapping.

P2:

- both CONTROL and requested `Terra / Medium` ADAPTIVE returned the same 18 characterized edges plus one facade-to-package-`__init__` edge;
- both therefore fail the frozen exact-edge-set oracle while getting acyclicity and all six symbol owners correct;
- the canonical characterization in `tests/test_repository_context_extraction.py` excludes the package-bootstrap edge;
- because both arms made the identical interpretation and the prepared probe asked for dynamic source-package loads, P2 is a shared task/oracle-semantics confound for causal model comparison; do not use it to claim Terra underperformed CONTROL.

P3:

- both CONTROL and requested `Terra / High` ADAPTIVE passed the seeded same-process `sys.modules` contamination review;
- both identified the material mechanism and source-specific namespace/isolation fix direction with no invented material finding;
- effective child profile identity was not observable, so this is requested-profile quality evidence rather than verified effective-profile evidence.

### T054 observability

The host accepted child-specific `model`, `reasoning_effort` and `fork_turns` requests but exposed no effective child model/reasoning/service-tier receipts and no attributable child token metrics.

Coordinator-observed durations exist but are not token/cost evidence. No quantitative savings claim is authorized.

The Executor branch changed only the two authorized non-Markdown evidence files; no product code, Markdown, D055 policy, static `.codex/agents/` catalog, authority boundary, root profile or write-safety invariant changed.

## Research dispositions

### R006 — persistent Executor coordinator

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Evidence: T053 accepted; T054 adds no persistence-causal evidence
Decision-Ref: none
```

T053 remains positive qualitative evidence for persistent-root context locality/reduced rereading, but host observability did not establish attributable token/context savings. No global D055 persistence-session change is adopted.

Reconsider only with materially better persistence observability or a separate normative justification that does not depend on an unverified efficiency claim.

### R007 — adaptive subagent compute routing

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Evaluation: T054 accepted / NOT_QUALIFIED
Decision-Ref: none
```

The frozen mapping is not qualified. P1 is real negative evidence for `Luna / Low`; P2 is a shared semantics confound; P3 is positive requested-profile quality evidence. Effective profiles and attributable usage remain unobservable.

No global child-routing policy is adopted.

Reconsider only after a successor evaluation removes the P2 confound, uses a mapping that preserves first-attempt quality, and preferably runs on a surface that exposes effective child-profile and attributable usage receipts.

## Next action

1. Do not rerun T054 unchanged.
2. Do not change D055 or adopt a global child-routing policy from T053/T054.
3. Before authorizing any successor adaptive-routing pilot, ChatGPT Orchestrator should open a new D057-tracked research item (`R008`) to determine whether the current Codex ecosystem exposes a materially better surface for:
   - effective child model/reasoning receipts;
   - attributable child token/usage metrics;
   - explicit child capability/sandbox controls;
   - and, if relevant, more precise spawn/profile observability through Codex CLI, App Server, SDK or official telemetry surfaces.
4. R008 must use current official OpenAI documentation as primary authority and specialized sources only as secondary evidence; volatile capability claims must be dated and sourced.
5. Only after R008 convergence should the Orchestrator decide whether a corrected successor routing pilot is justified and specify it as a new Task Contract.
6. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then:

- for the immediate next action, load D057 and `docs/RESEARCH-TRACEABILITY.md`, then create/conduct R008;
- load `docs/reviews/T054-R1.md` only when the new research needs exact T054 limitations or probe interpretation;
- load no additional project history unless a concrete conflict requires it.

## Do not

Do not treat T054 `NOT_QUALIFIED` as a failed execution; the execution is accepted and the hypothesis result is negative. Do not attribute the shared P2 failure specifically to Terra. Do not promote R006/R007 without a persisted D057 transition and accepted normative authority. Do not claim effective child profile identity or token/cost savings from T054. Do not rerun T054 unchanged. Do not change D055, persistent-root policy, consumer policy or global child-routing policy from this evidence boundary. Do not rerun MG1-v12 or launch V13.
