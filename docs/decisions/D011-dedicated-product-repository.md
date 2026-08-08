# D011 — Dedicated Governance product repository

Status: ACCEPTED
Authority: Human Owner
Date: 2026-08-08

## Decision

Governance Core, Governance Skill design/implementation, product decisions, tests and evals are developed in `ManuelBouza/agent-governance` rather than inside an adopting application repository.

Application repositories such as `script-uh` are consumers/testbeds only after an explicit installation/adoption step.

## Rationale

Developing the framework inside a consumer repository created ambiguity between reusable product state and project mission/task state. Physical repository separation removes that ambiguity and makes portability/testing independently verifiable.

## Consequences

- `agent-governance` is the canonical product source repository.
- Consumer repositories MUST NOT be treated as canonical sources for Governance Core or Governance Skill development.
- Consumer-specific mission/task/approval state never belongs in this product repository.
- Product testing uses dedicated fixtures/evals rather than relying on a consumer project's live coordination state.
- A future installation mechanism derives the consumer footprint from a released/pinned product revision.
