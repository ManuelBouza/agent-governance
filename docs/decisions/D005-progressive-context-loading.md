# D005 — Progressive context loading

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
Use a small always-loaded bootstrap plus explicit routing to focused Core modules, task records, Decision Records and EXCHANGE deltas. Do not preload large project/control documents.

## Rationale
Governance must scale without forcing Strategy or Implementation agents to repeatedly consume unrelated instructions or growing project history.

## Consequences
GOVERNANCE is the router; STATE remains approximately constant-size; WORKPLAN is metadata/index; task detail lives in `tasks/`; rationale-bearing decisions live in `decisions/`; product adapters preload only STATE and GOVERNANCE where supported.
