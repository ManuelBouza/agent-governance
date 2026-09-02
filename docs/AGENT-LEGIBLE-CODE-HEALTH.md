# Agent-Legible Code Health

Status: `PROPOSED / T050 CONTROLLING DESIGN`

Owner: ChatGPT Orchestrator

Applies to: source-product executable code and technical test/eval harnesses in this repository.

## Purpose

Keep source code maintainable for humans and economical for coding agents to inspect, reason about, review and modify.

The policy treats context as a bounded engineering resource. Large monolithic files increase navigation cost, raise the probability that an agent must load irrelevant code, weaken prompt-cache locality, enlarge review surfaces and make responsibility boundaries harder to infer.

This policy does not substitute arbitrary line-count minimization for good design. Cohesion, stable interfaces, testability and dependency direction remain primary. Size limits are guardrails that force an explicit architectural decision before a module becomes an unbounded context sink.

## Research basis

External engineering guidance does not define one universal maximum file size, but established tools and practices consistently treat very large modules as a code-health problem:

- ESLint `max-lines` documents common project limits in the low hundreds and treats files with thousands of lines as generally excessive;
- Pylint's historical `max-module-lines` default is `1000`;
- Ruff exposes McCabe complexity (`C901`) and refactor-oriented rules such as excessive branches/statements (`PLR0912`, `PLR0915`);
- Google Engineering Practices recommends small, self-contained changes and warns that very large review units reduce review quality;
- agent-oriented coding systems use repository maps, symbol search and progressive disclosure to avoid sending whole repositories or giant files into every model turn;
- OpenAI's agent-oriented repository guidance emphasizes concise routing instructions, selective context loading, structural tests and custom linters rather than treating larger context windows as the primary solution.

The repository therefore adopts a ratchet plus progressive-disclosure design rather than a single universal LOC rule.

## Mechanical size policy

Count physical source lines deterministically using the repository-owned code-health checker. Generated/vendor/binary/data assets are outside this rule unless a Task Contract explicitly includes them.

### New or substantially rewritten Python modules

- target: `<= 500` physical lines;
- architectural warning: `> 600` physical lines;
- hard limit: `1000` physical lines.

Crossing the warning threshold requires the implementation/review to explain why the module remains one cohesive responsibility. Crossing the hard limit requires an explicit persisted Orchestrator exception or a narrower artifact class that is mechanically exempted.

### Existing oversized modules

An existing module above the hard limit enters a **no-net-growth ratchet**:

- its accepted baseline line count is persisted by the checker/configuration;
- ordinary changes MUST NOT increase that count;
- work that adds a new responsibility SHOULD extract a cohesive module rather than append to the oversized file;
- a dedicated refactor Task Contract may lower the baseline;
- once the file falls below a stricter threshold, the baseline ratchets downward and MUST NOT automatically rise again.

`evals/skill_activation_topology/harness.py` enters the ratchet at approximately `3,133` lines after the integrated V10 evidence/infrastructure state. T050 is expected to replace that temporary baseline with a substantially smaller facade through behavior-preserving extraction.

## Function-level complexity policy

Use Ruff or an equivalent repository-owned deterministic check to enforce, at minimum, prospectively selected limits for:

- McCabe complexity (`C901`), target/default maximum `10`;
- branches (`PLR0912`), target/default maximum `12`;
- statements (`PLR0915`), target/default maximum `50`.

Do not enable a rule globally when doing so would create unrelated repository-wide churn. A Task Contract may introduce scoped enforcement first, with explicit legacy baselines and a ratchet toward broader compliance.

## Architectural decomposition rules

Extract by responsibility, not by arbitrary line slices.

Preferred module boundaries for complex agent/eval harnesses include concerns such as:

- immutable input/schema validation;
- candidate/fixture materialization;
- host/workspace adapter mechanics;
- provider invocation and host-profile binding;
- trace parsing/activation observability;
- scheduling/retry/capacity/futility state;
- evidence persistence/provenance;
- scoring/selection;
- CLI/facade wiring.

A module SHOULD have a narrow public surface and one dominant reason to change. Circular dependencies are forbidden. Lower-level adapter/trace/evidence modules MUST NOT import CLI orchestration merely for convenience.

## Agent-context efficiency

The repository SHOULD make navigation cheaper than full-file reading.

For substantial Python surfaces, provide or generate a deterministic symbol map containing at least:

- module path;
- top-level class/function names;
- start/end lines when mechanically available;
- optionally direct imports and selected call/reference relationships;
- module physical LOC and selected complexity metrics.

The map is navigation metadata, not authority. It MUST be regenerable from source and MUST NOT require an LLM.

Coding agents SHOULD use progressive disclosure:

1. read `AGENTS.md` and the exact Task Contract;
2. inspect the relevant code-health/symbol map;
3. search symbols/usages;
4. load only the modules/ranges required by the task;
5. expand context only when a concrete dependency requires it.

Do not require an agent to preload every module merely because they share a package.

## Change-size policy

Implementation should prefer reviewable, semantically coherent deltas. A large refactor may be authorized when characterization tests make structural movement safer, but feature/behavior changes SHOULD NOT be mixed with broad structural decomposition unless the controlling Task Contract explicitly requires both.

For oversized legacy code, prefer:

1. freeze behavior with characterization tests;
2. extract one responsibility at a time behind stable interfaces;
3. keep semantic inputs/outputs byte- or behavior-equivalent where required;
4. run focused and full regressions after each extraction;
5. ratchet size downward.

## Skill integration

Do **not** create a separate top-level generic coding Skill for this repository.

`docs/MAINTAINER-SKILL-CONTRACT.md` defines the Maintainer Skill as the sole project-owned top-level source-maintenance Skill. When that Skill is implemented, its Executor route SHOULD progressively load this code-health policy (or an equivalent packaged reference) for implementation/refactoring/code-review work.

The Skill provides workflow/navigation guidance; deterministic checks provide enforcement. Source maintenance MUST remain possible when the Skill is absent or disabled.

## Mechanical enforcement requirements

The repository SHOULD provide a deterministic code-health checker that:

- measures module line counts;
- enforces new-module hard limits;
- enforces persisted no-net-growth baselines for oversized legacy modules;
- reports remediation-oriented failure messages;
- can emit a symbol/code map without model use;
- is covered by deterministic tests;
- runs in normal source verification/CI without requiring a Skill or external agent.

Ruff remains the preferred existing Python lint engine for complexity checks where suitable. Repository-specific size-ratchet and symbol-map semantics may be implemented with a small Python checker rather than adding a second large lint dependency.

## Exceptions

Exceptions MUST be explicit and narrow. Acceptable examples can include generated code, mechanically produced schemas or artifacts whose single-file form is externally mandated.

An exception MUST NOT be justified merely by:

- the model having a large context window;
- the code currently passing tests;
- a deadline;
- a preference to avoid creating modules;
- historical file size.

## Acceptance intent

The policy succeeds when new executable work cannot silently create context-sink modules, oversized legacy files cannot keep growing, agents can navigate complex packages from compact structural metadata, and decomposition preserves behavior through deterministic characterization evidence.
