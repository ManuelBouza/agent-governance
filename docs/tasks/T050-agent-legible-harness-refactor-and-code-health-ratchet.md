# T050 — Agent-Legible Harness Refactor and Code-Health Ratchet

## Identity

- Task ID: `T050`
- Status: `PLANNED`
- Type: `behavior-preserving technical refactor + deterministic code-health tooling`
- Base branch: `develop`
- SDD profile: `ASSURED`
- Test-Authorship-Mode: `executor-implementation`
- Re-entry context: follows `docs/reviews/T023-R9.md`
- Affects: MG1/T023 technical harness maintainability; does **not** authorize a new T023 acceptance epoch

## Objective

Reduce the Agent Governance source-maintenance context burden and prevent further monolithic growth before any successor MG1 acceptance execution.

T050 MUST:

1. behavior-preservingly decompose `evals/skill_activation_topology/harness.py` into cohesive modules with a thin compatibility/CLI facade;
2. establish deterministic module-size and complexity guardrails aligned with `docs/AGENT-LEGIBLE-CODE-HEALTH.md`;
3. establish a no-net-growth ratchet for oversized legacy Python modules and a hard limit for new/substantially rewritten modules;
4. provide a deterministic symbol/code map so agents can navigate relevant definitions without loading entire large files;
5. preserve the integrated V10 technical behavior, evidence formats and frozen MG1 semantic assets;
6. make no live provider/model acceptance calls.

## Why this task is required now

After V10 integration, `evals/skill_activation_topology/harness.py` is approximately `3,133` physical lines. The V10 delta added about `269` net lines to an already oversized module.

The V10 blocker itself was a trace-classification defect, not file size. However, repeated execution-method revisions have concentrated unrelated responsibilities in one context-heavy file. Continuing T023 work directly on that monolith would increase agent context cost and technical risk.

T050 is therefore a structural precondition before another MG1 live epoch.

## Preserved semantic authority

T050 MUST NOT change:

- `evals/skill_activation_topology/oracle.json` semantics or identity;
- `corpus.json`;
- `trial-envelope.json`;
- `topologies.json`;
- candidate/reference/presentation bytes;
- expected classifications;
- qualification thresholds;
- D050 selection rules;
- paired 2+1, futility/materiality or capacity semantics;
- activation authority / host-observed body-read meaning;
- V10 evidence meaning or the terminal classification in `docs/reviews/T023-R9.md`;
- product Core/runtime/profile semantics.

No prior unscored acceptance attempt may be rescored or rewritten.

## Characterization-first requirement

Before structural mutation, Executor MUST establish and persist a characterization baseline for the current integrated harness.

At minimum, characterize:

- CLI subcommands/arguments and exit behavior;
- frozen-input validation behavior;
- candidate and fixture materialization;
- provider-free backend/workspace probes;
- Codex invocation construction and host-profile binding;
- trace parsing and activation/body-read extraction;
- access-rejection / host-surface-drift classification, including the corrected V10 regression;
- attempt/retry/capacity handling;
- scheduling and futility state;
- evidence filenames/shapes/provenance;
- scoring/selection calculations;
- deterministic verification commands.

Existing tests may provide part of this baseline. Add only the characterization coverage needed to make extraction fail closed.

Once structural mutation starts, do not weaken or rewrite the characterization baseline merely to make the refactor pass without Orchestrator re-entry.

## Target architecture

Keep `evals/skill_activation_topology/harness.py` as a stable thin facade/entrypoint where compatibility requires it.

Extract cohesive implementation modules under the same eval package. Exact filenames may vary only for mechanical reasons, but the approved responsibility boundaries are:

1. **models/constants** — dataclasses, immutable local types, narrow shared constants;
2. **frozen inputs** — JSON loading, identity/hash/schema validation, topology/corpus/manifest/envelope checks;
3. **materialization/workspace** — candidate/fixture projection, Windows disposable-workspace factory, ACL diagnostics, cleanup and provider-free workspace probe;
4. **Codex adapter** — version/backend resolution, invocation construction, minimal feature surface and host-profile identity;
5. **trace/observability** — JSONL event parsing, successful body/reference reads, token/tool telemetry, capacity signals, genuine access rejection and host-surface drift;
6. **scheduler/execution** — trial specifications, retry/capacity state, paired 2+1 scheduling, futility/materiality stop mechanics;
7. **evidence/provenance** — attempt journals, run metadata, completeness, deterministic evidence and immutable-runner provenance;
8. **scoring/selection** — case aggregation, metrics, thresholds and selection computations without redefining their semantics;
9. **CLI** — parser/subcommand wiring and delegation.

### Dependency direction

Prefer a one-way dependency graph:

```text
models/constants
    ↓
frozen-inputs
    ↓
materialization/workspace   codex-adapter   trace/observability
          \                    |                 /
           \                   |                /
             scheduler/execution
                    ↓
             evidence/provenance
                    ↓
             scoring/selection
                    ↓
                  CLI
```

Equivalent acyclic layering is acceptable. Circular imports are forbidden.

Host adapter/trace modules MUST NOT import CLI wiring. Scoring MUST NOT invoke Codex or mutate workspaces. Evidence serialization SHOULD remain separated from semantic calculations where practical.

## Size targets and ratchet

Use the canonical policy in `docs/AGENT-LEGIBLE-CODE-HEALTH.md`.

T050 acceptance targets:

- `harness.py` facade: `<= 500` physical lines;
- each newly extracted implementation module: target `<= 500`, MUST be `<= 1000`;
- no new Python module above `1000` physical lines;
- no new responsibility may remain in `harness.py` merely to avoid an extraction;
- if a module exceeds `600` lines, Code Review & Verify must explicitly justify cohesion in the handoff.

If achieving the `<=500` facade target would require semantic redesign rather than extraction, stop for Orchestrator re-entry rather than changing behavior.

## Complexity guardrails

Implement scoped deterministic enforcement sufficient to prevent regression without causing unrelated repository-wide churn.

For T050-owned/refactored Python surfaces, target:

- McCabe complexity `<= 10` (`C901` or equivalent);
- branches `<= 12` (`PLR0912` or equivalent);
- statements `<= 50` (`PLR0915` or equivalent).

Use Ruff where practical. Repository-specific size-ratchet semantics may use a small deterministic Python checker.

Do not add Pylint solely for module-size enforcement unless the existing toolchain cannot implement the required policy cleanly.

## Deterministic code-health checker

Add a repository-owned checker, location chosen consistently with source tooling, that can run without an LLM and at minimum:

- enumerate governed Python modules;
- report physical LOC;
- enforce `1000` hard limit for new/substantially rewritten modules;
- enforce persisted no-net-growth baselines for explicitly grandfathered oversized modules;
- emit remediation-oriented failures naming file, current LOC, allowed baseline/limit and expected action;
- emit a machine-readable result suitable for tests/CI;
- fail closed on malformed baseline/configuration.

After the T050 refactor, do not preserve the old `harness.py ~3133` baseline as permission to regrow it. Ratchet the accepted baseline down to the new facade size.

## Deterministic symbol/code map

Add a model-free source navigator based on Python AST or equivalent standard-library parsing.

It MUST be able to produce compact machine-readable metadata containing at least:

- module path;
- physical LOC;
- top-level class/function names;
- definition start/end lines when available;
- direct imports.

Optional call/reference relationships are allowed if deterministic and cheap.

The map MUST be generated from source rather than manually maintained and MUST NOT become correctness authority.

A human-readable compact output mode is desirable but not required if the machine-readable artifact is clear.

## Maintainer Skill relationship

Do not create a new top-level generic coding Skill.

The future Maintainer Skill remains the sole project-owned top-level source-maintenance Skill. Its Executor route will progressively load the code-health policy for implementation/refactoring/review tasks.

T050 deterministic checks MUST work with the Maintainer Skill absent/disabled.

## No live evaluation spend

T050 MUST NOT issue:

- synthetic Skill canary calls;
- T023 acceptance prompts;
- other provider/model calls for MG1 scoring.

Local Codex CLI/help inspection that does not invoke a provider/model is unnecessary unless required to preserve/refactor adapter code, and no new host behavior should be inferred from live model execution in this task.

## Required verification

Executor MUST run at minimum:

1. Ruff check;
2. Ruff format check;
3. full pytest;
4. focused skill-activation-topology harness tests;
5. new code-health checker tests;
6. new symbol-map tests;
7. deterministic MG1 validation/scoring unit coverage that requires no live provider;
8. an import-cycle/dependency-direction check sufficient for the extracted package;
9. a comparison proving frozen D052 assets are byte-identical to the T050 base.

## Acceptance criteria

### AC-T050-1 — behavior-preserving characterization
The pre-refactor characterization baseline remains green after decomposition and was not weakened post-mutation without Orchestrator authority.

### AC-T050-2 — thin facade
`evals/skill_activation_topology/harness.py` is `<=500` physical lines and delegates cohesive responsibilities to extracted modules.

### AC-T050-3 — bounded modules
Every newly extracted implementation module is `<=1000` physical lines; modules above `600` include an explicit cohesion justification in the handoff; target is `<=500`.

### AC-T050-4 — mechanical ratchet
A deterministic checker enforces new-module hard limits and persisted no-net-growth baselines, with tests and remediation-oriented output.

### AC-T050-5 — complexity enforcement
T050-owned/refactored surfaces satisfy the scoped complexity/branch/statement limits or a narrowly persisted preimplementation exception. No silent per-file ignore is added merely to make the task pass.

### AC-T050-6 — model-free navigation
A deterministic symbol/code map can identify module LOC, top-level definitions, line ranges and imports without reading all source into an LLM context.

### AC-T050-7 — semantic assets unchanged
Oracle/corpus/envelope/topology/presentation/reference bytes and product Core/runtime/profile semantics remain unchanged.

### AC-T050-8 — evidence formats/technical behavior preserved
Existing deterministic tests plus added characterization prove CLI, workspace/backend adapter, trace classification, scheduling, evidence, scoring and provenance behavior are preserved.

### AC-T050-9 — no live MG1 spend
Synthetic canary calls = `0`; acceptance prompts = `0`; scored observations = `0`.

### AC-T050-10 — full verification green
Ruff, full pytest, focused harness tests, code-health/symbol-map tests and dependency checks all pass.

## Ownership

ChatGPT Orchestrator owns this Task Contract, code-health policy, architectural decomposition and acceptance.

Agente de IA Ejecutor owns authorized non-Markdown implementation: refactor mechanics, checker, AST navigator, Ruff configuration, deterministic tests and Code Review & Verify.

Executor MUST NOT edit committed Markdown or any D052 semantic oracle asset.

## Handoff

Persist the standard Executor handoff and include:

- base/submitted/reviewed HEADs;
- before/after LOC for `harness.py` and every extracted module;
- resulting size-ratchet baseline/configuration;
- complexity check results;
- symbol-map sample/verification;
- characterization evidence;
- confirmation of zero provider/model MG1 calls;
- frozen semantic-asset hash comparison;
- full verification results;
- any module >600 LOC and its cohesion justification.
