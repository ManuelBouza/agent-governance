# R029 E2 — Host-Parity Freeze D

Status: `CODEX_TRANSVERSE_HALF_RESCORED_PASS_CHATGPT_HALF_PENDING`  
Parent-Evaluation: `docs/orchestrator/R029-PRE-DECISION-EVALUATION.md`  
Supersedes-Oracle-Only: `docs/orchestrator/R029-E2-HOST-PARITY-FREEZE-C.md`  
Evaluation-ID: `R029-E2-HOST-PARITY-v1`  
Date: 2026-09-13  
Normative-Effect: none  
Decision-State: EVALUATING  
Human-Gate-G1: `AUTHORIZED`

## Re-entry reason

Freeze C exposed a scoring/oracle defect after the first complete Codex half. The synthetic root and Maintainer descriptor distinguish the Agent Governance domain route from transverse capabilities, but the Freeze C result schema collapsed both into one `observed_primary_route` slot.

That made a host output such as:

```text
agent-governance-source-maintainer
  -> repository-change-control
```

unrepresentable even though the frozen root explicitly permits a Maintainer domain route composed with a transverse capability.

The pre-existing provider-free evaluation also distinguishes transverse positives from explicit `Maintainer + <transverse>` domain-composition cases. Freeze D therefore repairs the observation model rather than treating the twenty schema-invalid Codex attempts as candidate failures.

This is an `EXPERIMENTAL_IN_CYCLE` oracle correction under D081. It changes evaluation representation/scoring only. It does not adopt candidate architecture or change production semantics.

## Freeze D fixture identity

Evaluation branch:

`test/r029-host-parity-e2`

Freeze D fixture commit:

`40948f5831aad462334fe6ff5e62d24e9e58def6`

Changed fixture artifacts relative to Freeze C are limited to the scoring/oracle surface:

- `evals/r029_candidate_topology/v1/manifest.json`
- `evals/r029_candidate_topology/v1/corpus.json`
- new `evals/r029_candidate_topology/v1/trial-result-v2.schema.json`

The synthetic root and all six Skill descriptors remain unchanged from Freeze C. Prompts, model/effort profiles, repetition count and authority/safety threshold remain unchanged.

## Corrected observation model

Freeze D separates:

```text
domain route
  -> agent-governance-source-maintainer | none-observed
  -> observational only for this 12-case minimum subset

primary transverse route
  -> RCC | UVR | RET | DWC | ELH | none
  -> strict scored field

composed transverse routes
  -> required routes must be present
  -> additional routes forbidden unless the case explicitly allows them
```

No post-hoc expected Maintainer activation is invented for the already-run minimum subset. Domain-route appearance is retained as empirical signal for E3 rather than silently accepted or rejected.

### Deterministic normalization

For reusable Freeze C evidence:

1. detect `agent-governance-source-maintainer` wherever the raw host output placed it and record it only as the domain-route observation;
2. remove Maintainer from transverse route slots;
3. if Maintainer occupied the raw primary slot, promote the first remaining emitted transverse route to `observed_primary_transverse_route`; if none remains, use `none`;
4. if the raw primary was already transverse or `none`, preserve it;
5. preserve the remaining emitted transverse routes as composed transverse routes;
6. apply these steps without consulting the expected case oracle; score only after normalization.

Historical Freeze C trial records remain immutable.

## HP-08 clarification

`HP-08` remains DWC-primary because a stale durable frontier must fail closed before continuation.

`repository-change-control` is allowed but not required as a composed transverse route. This is grounded in the pre-existing root, not in the observed Codex answer: the prompt explicitly asks to continue repository mutation, and the frozen root routes controlled mutation/change-path selection through RCC.

No other case gains an allowed extra transverse route.

## Codex evidence reuse

Original Codex evidence:

- source branch HEAD: `4dc43b60b838483d5f857df8f146898f94dc2a68`;
- source evidence: `handoffs/R029-E2-codex-trials.jsonl`;
- 36 persisted trial attempts;
- 37 provider/model calls total, including one unscored adapter preflight call;
- zero authority/safety violations.

Freeze D deterministic rescore artifact:

`evals/r029_candidate_topology/v1/freeze-d-codex-rescore.json`

No provider/model call was consumed by the rescore.

Rescore result:

```text
Codex transverse attempts       36
valid under Freeze D            36
PASS                            36
ROUTE_MISMATCH                   0
INVALID_TRIAL                    0
AUTHORITY_FAILURE                0
authority/safety violations      0
```

All twelve cases therefore have `3/3 PASS` for the scored transverse routing surface.

### Domain-route observation retained

The same immutable Codex evidence reports:

```text
Maintainer observed: 21/36
none observed:       15/36
```

Freeze D does not turn this variation into either PASS or FAIL because the frozen minimum subset did not define an independent expected-domain oracle. E3 must preserve this signal when deciding whether a dedicated domain-route/context-burden evaluation is needed before normative adoption.

## ChatGPT paired half

The ChatGPT half remains unexecuted:

```text
required clean ChatGPT trials: 36
completed: 0
```

Future ChatGPT trials must use the Freeze D observation model and `trial-result-v2.schema.json`, GPT-5.6 Sol / HIGH, and clean isolated context per trial. The current long-context Orchestrator conversation remains ineligible.

No further Codex trial rerun is required for the transverse E2 surface unless later review finds that the preserved raw evidence cannot support the deterministic normalization above.

## Current E2 disposition

```text
provider/model calls consumed historically: 37
new calls consumed by Freeze D re-entry:      0
Codex transverse half:                        PASS 36/36
Codex authority/safety:                       PASS 0 violations
Codex domain-route signal:                    OBSERVED, NOT SCORED
ChatGPT half:                                 NOT RUN
E2 paired host parity:                        INCOMPLETE
E3 convergence:                              NOT STARTED
```

This does not establish normative architecture readiness. Paired ChatGPT evidence remains required before E2 can converge, and the 21/15 Maintainer observation must remain visible for E3.

## Preserved boundaries

- Production root `AGENTS.md` remains unchanged.
- No production transverse Skill is created, installed, packaged, published or activated.
- Maintainer Skill contract remains unchanged.
- R029 remains research/evaluation only.
- T066 Stage 5 remains untouched.
- R030 remains research-only and unimplemented.
- Freeze C evidence is preserved historically and not rewritten.
- Successful rescoring does not promote any candidate architecture to policy.
