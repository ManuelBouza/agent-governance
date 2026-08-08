# D013 — Apache-2.0 public distribution

Status: ACCEPTED
Authority: Human Owner

## Decision

Distribute Agent Governance as a public reusable project under the Apache License 2.0.

## Rationale

The project is intended for broad third-party adoption, modification, redistribution and contribution. A permissive license is appropriate, and Apache-2.0 additionally provides an explicit patent grant and patent-termination mechanism that is useful for a reusable software/governance framework.

## Consequences

- `LICENSE` contains the Apache License 2.0 text.
- Contributions intentionally submitted for inclusion are accepted under Apache-2.0 unless explicitly stated otherwise.
- Public availability and licensing are separate from release stability: `main` remains development state until the stable release gate passes.
- Consumers should pin immutable releases/commits instead of trusting a floating branch.
- Contribution, security and release policies are part of the public project surface.
