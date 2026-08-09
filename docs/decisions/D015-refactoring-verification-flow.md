# D015 — Independent refactoring verification flow

Status: SUPERSEDED by D016
Authority: Human Owner

## Supersession

D016 removes the Codex-specific verification role introduced here. The valid invariant that survives is the need for a pre-change characterization baseline and explicit post-change verification. Both are now responsibilities of the abstract `Agente de IA Ejecutor` role, with ChatGPT controlling the semantic contract and any baseline changes.

## Historical Decision

Refactoring of the `agent-governance` source product follows `docs/REFACTORING-WORKFLOW.md`.

A refactor is strictly behavior/semantic preserving. Before the refactor, ChatGPT defines the invariants and a coding agent establishes a green characterization baseline, adding focused tests/evals when coverage is insufficient. The authorized artifact owner then performs the refactor in small coherent units and verification is rerun before ChatGPT accepts the structural change.

Feature work, bug fixes that intentionally alter behavior, protocol semantic changes, dependency upgrades, and unrelated cleanup are not bundled into a refactor unit.

## Historical Rationale

The existing strategic discipline remains useful for framing, boundaries, atomicity, and acceptance, but the source repository should not self-install the consumer F0-F6 state machinery. Refactoring needs an additional behavior-preservation mechanism: a verified pre-change baseline and post-change verification.

The earlier decision incorrectly modeled Codex as a distinct governance role rather than another implementation of the coding-agent executor category. D016 corrects that distinction.
