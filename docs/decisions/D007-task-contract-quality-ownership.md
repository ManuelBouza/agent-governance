# D007 — Task contract quality ownership

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
The Strategy/Governance role owns the correctness and completeness of task objectives and execution contracts before F5/F6 handoff. Implementation owns technical realization, not reconstruction of missing strategy.

## Rationale
Autonomous sequential execution only works reliably when each disclosed task contains sufficient context, boundaries, dependencies, acceptance criteria, required capabilities and material constraints to succeed without hidden chat context or guessed intent.

## Consequences
F4/F5 must reject ambiguous or under-specified tasks. The Implementation Agent must resolve normal technical choices autonomously, but must block on missing strategic requirements, scope meaning or acceptance meaning rather than inventing them.
