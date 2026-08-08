# D006 — Agent-neutral sequential execution

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
Tasks target the abstract `implementation` role, never a specific agent product. One compatible Implementation Agent executes the authorized plan sequentially, loading only the current task record and continuing automatically after DONE.

## Rationale
The framework must work with OpenCode, Codex, Claude Code, Antigravity or future agents without rewriting task contracts, while preventing future-task context from biasing current implementation.

## Consequences
Future task content remains undisclosed until the current task is DONE; WORKPLAN exposes only execution metadata/order; DONE satisfies normal dependencies for continuation; ACCEPTED is review, not the default inter-task gate; valid cross-responsibility blockers stop the sequence.
