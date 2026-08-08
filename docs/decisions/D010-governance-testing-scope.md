# D010 — Governance product testing scope

Status: ACCEPTED
Authority: Human Owner
Date: 2026-08-08

## Decision

Automated tests and agent evals for this repository validate the Governance Core and Governance Skill themselves. They do not evaluate the quality of application-task implementation performed by an Implementation Agent.

Synthetic task records MAY be used only as fixtures to exercise governance mechanics such as readiness, sequential disclosure, blockers, handoff and state reconstruction.

## Rationale

Application implementation quality belongs to each adopting project's own engineering/test process. Mixing it into Governance product evals would blur responsibility and make framework results dependent on unrelated coding capability.

## Consequences

- Deterministic tests cover protocol, lifecycle, state, routing, permissions, references, discovery and Skill supply-chain mechanics.
- Agent evals cover Governance Skill triggering, cold-start reconstruction, routing, handoff, portability and other behavior intrinsic to the framework.
- Synthetic tasks are minimal protocol fixtures, never coding benchmarks.
- Release criteria for Governance MUST NOT depend on an agent successfully implementing a real application feature.
