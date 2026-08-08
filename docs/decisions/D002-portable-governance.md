# D002 — Portable governance boundary

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
Reusable governance semantics are separated from project-specific coordination state.

## Rationale
The framework must be deployable into unrelated repositories without carrying testbed/domain assumptions.

## Consequences
Reusable Core and product source stay independent from consumer mission, work, state and coordination history; product-specific adapters remain outside canonical task semantics.
