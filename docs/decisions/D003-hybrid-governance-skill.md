# D003 — Hybrid Core plus operational Skill

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
Keep canonical governance and project state in versioned repository files, with a reusable Agent Skill as an optional operational/distribution layer.

## Rationale
A Skill is useful for consistent bootstrap/validation/operation but its activation or availability cannot be the sole carrier of mandatory authority or durable state.

## Consequences
The system must remain fully operable without the Skill. The Skill may operate/validate the Core but never replace it.
