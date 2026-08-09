# D015 — Independent refactoring verification flow

Status: ACCEPTED
Authority: Human Owner

## Decision

Refactoring of the `agent-governance` source product follows `docs/REFACTORING-WORKFLOW.md`.

A refactor is strictly behavior/semantic preserving. Before the refactor, ChatGPT defines the invariants and Codex establishes a green characterization baseline, adding focused tests/evals when coverage is insufficient. The authorized artifact owner then performs the refactor in small coherent units, and Codex independently reruns the applicable verification before ChatGPT accepts the structural change.

Artifact ownership remains:
- Markdown/instruction refactor -> ChatGPT;
- executable/config refactor -> Implementation Executor;
- test/eval refactor -> Codex.

Feature work, bug fixes that intentionally alter behavior, protocol semantic changes, dependency upgrades, and unrelated cleanup are not bundled into a refactor unit.

## Rationale

The existing strategic discipline remains useful for framing, boundaries, atomicity, and acceptance, but the source repository should not self-install the consumer F0-F6 state machinery. Refactoring needs an additional behavior-preservation mechanism: a verified pre-change baseline and independent post-change verification.

Independent test ownership reduces the risk that an implementation agent changes verification to accommodate its own refactor instead of preserving the approved behavior.

## Consequences

- Missing characterization coverage is addressed before executable refactoring begins.
- A failing baseline is resolved or isolated before refactoring.
- Each accepted refactor unit leaves the repository working and independently verifiable.
- If intended behavior must change, work exits the refactor flow and re-enters normal product development.
- Core Markdown restructuring is treated as semantically sensitive even without executable code changes.
