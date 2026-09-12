# D078 — Selective Capability Routing Evaluation Boundary

Status: ACCEPTED  
Date: 2026-09-12  
Authority: Human Owner / ChatGPT Orchestrator  
Trigger: advanced external research conducted before any T062 v15 provider/model execution  
Refines: D050, D074  
Preserves: D052, D053, D057, D061, D068, D076, D077

## Problem

T023 v15 correctly froze candidate and holdout material, made B2/F2/G3 non-blocking with respect to one another, and defined explicit activation and semantic metrics. However, its Stage 6 protocol still combines routing correctness, specialist execution correctness, and end-to-end correctness inside one expensive topology-level live experiment.

External research on tool/function routing, selective classification, open-set recognition, multi-label classification, model routing, calibration, and paired classifier comparison shows that the routing question can and should be isolated before paying the full specialist-execution cost.

The v15 live experiment has consumed exactly zero provider/model attempts and produced zero scientific observations. The methodology can therefore be corrected without discarding provider-backed evidence.

## Decision

Prospectively for the next T023 epoch, Agent Governance SHALL evaluate Skill activation topology through a **selective capability routing** abstraction before end-to-end specialist execution.

The canonical conceptual sequence is:

```text
request
  -> canonical capability truth
  -> selective routing decision
  -> topology-specific activation mapping
  -> routing qualification
  -> specialist execution for qualified finalists
  -> end-to-end confirmation
```

Routing truth SHALL be defined independently of B2/F2/G3 packaging.

## Canonical routing outcomes

The routing model must support zero, one, or multiple capabilities.

The empty capability set is a first-class expected outcome and means no Agent Governance specialist is applicable:

```text
NONE / DIRECT
```

Uncertainty is a different state:

```text
ABSTAIN / ASK
```

`NONE` means the system has enough evidence to conclude that no specialist is required. `ABSTAIN / ASK` means there is not enough evidence to select safely and the correct action is clarification or another fail-closed path defined by the future Task Contract.

A future implementation need not expose these exact strings, but the semantic distinction is mandatory.

## Multi-label semantics

The canonical oracle may assign multiple capabilities to one request. Multi-intent inputs SHALL therefore be represented as set-valued truth rather than forced into one mutually exclusive class.

A future topology maps the canonical capability set to its own activation units. This mapping separates semantic truth from packaging.

## Host-native portability

D078 does not require a new portable runtime router.

For the portable product baseline, the host's native Skill activation behavior may remain the router and be evaluated as a black box against the canonical capability oracle.

An explicit calibrated pre-router may be evaluated as an adapter-specific optimization only when the host permits it. It must not become a hidden dependency that violates D050 portability.

## Routing-first qualification

A candidate topology/policy SHALL establish routing viability before full specialist execution is used as confirmatory evidence.

At minimum the routing evaluation must distinguish:

- correct activation;
- missed specialist;
- wrong specialist;
- unnecessary specialist / overactivation;
- false activation on `NONE`;
- exact-set behavior for multi-label cases;
- critical cross-profile or permission-invalid activation.

If the router exposes a score used for thresholds, that score must be empirically calibrated or otherwise validated; a model-authored numeric confidence is not automatically probability.

## Execution boundary

Routing correctness and execution correctness are separate estimands.

For routing-qualified finalists, the evaluation SHALL separately report:

```text
P(execution success | routing correct)
```

and end-to-end success.

This permits attribution of failures to selection versus specialist behavior.

## Statistical boundary

Repeated trials of the same case SHALL NOT be counted as independent cases for generalization.

Future T023 evaluation must distinguish:

- across-case generalization; and
- within-case repeated-trial reliability.

Comparisons over common cases should be paired. The future analysis plan must pre-register the primary routing endpoint, critical gates, materiality/non-inferiority or superiority margins as applicable, and uncertainty intervals appropriate to the metric.

Point thresholds such as `>= 0.95` or `<= 0.05` must be labelled either:

- corpus acceptance SLOs; or
- population/inferential claims backed by an adequate sample-size and interval design.

They must not silently switch between those meanings.

## Cost and topology selection

Quality, safety/risk, context, provider cost, and latency remain distinct dimensions unless a Human-approved utility function explicitly combines them.

Routing-ineligible candidates are not required to consume a full end-to-end acceptance schedule merely to prove again that they route incorrectly.

Only routing-qualified finalists proceed to full confirmatory specialist execution under the next Task Contract.

## Relationship to B2/F2/G3

D078 does not pre-decide that B2, F2, or G3 is correct.

They remain meaningful packaging hypotheses for the activation surface. The next epoch may retain, revise, or replace them only through explicit Orchestrator specification/design authority.

The question changes from:

```text
which complete topology wins after full execution?
```

to:

```text
which capability partition makes the minimum correct activation set
reliably selectable, then preserves execution quality at acceptable
context/cost/latency?
```

## Treatment of T023 v15 / T062

The currently authorized T062 v15 Stage 6 SHALL NOT be consumed after acceptance of this decision.

Its frozen scientific branch, candidate, holdout, and handoff lineage remain historical unconsumed evidence. They are not deleted, rewritten, merged into a new epoch, or reclassified as scientific results.

R36 launch authority is prospectively superseded for execution purposes by the convergence review that records this D078 decision.

Provider/model calls consumed by v15 remain `0`. Scientific observations remain `0`.

A new T023 epoch must use a fresh Task Contract and fresh confirmatory holdout appropriate to D078. The old v15 live schedule is not silently repurposed as v16.

## Consequences

- T023 v15 is preserved but not executed.
- The next epoch must separate routing qualification from specialist execution.
- `NONE` and `ABSTAIN / ASK` become distinct semantic outcomes.
- Canonical capability truth is topology-independent and may be multi-label.
- repeated trials no longer inflate the independent sample count;
- paired and uncertainty-aware analysis becomes part of the planned experiment;
- an explicit router remains optional and adapter-scoped unless separately promoted to portable architecture;
- end-to-end live cost is concentrated on routing-qualified finalists.
