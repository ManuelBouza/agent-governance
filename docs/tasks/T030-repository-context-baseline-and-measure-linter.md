# T030 — Repository Context Baseline And Measure Linter

## Identity

- Task ID: `T030`
- Status: `ACCEPTED`
- Type: infrastructure/test
- Base branch: `develop`
- Expected topic branch: `infra/t030-repository-context-baseline`
- Expected executor handoff: `handoffs/T030-executor-handoff.json`
- Current durable review: `docs/reviews/T030-R2.md`
- Review disposition: `ACCEPTED`
- Assurance-Class: `deterministic`
- Baseline: `none — this task establishes the first accepted source-repository context baseline`
- Verification-Planes: `static, deterministic`
- Release-Impact: `none`
- Context-Impact: `focused`

## Objective

Create a lightweight, offline, deterministic **measure-only** source-repository context analysis tool and freeze a reproducible baseline from the current tracked Git tree. The task measures context-relevant physical/structural properties; it does not enforce budgets, split files, or change Consumer behavior.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
- `docs/AGENT-CAPABILITY-ENGINEERING.md`
- `docs/CONTEXT-ARCHITECTURE.md`
- `docs/TASK-CONTRACTS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `governance-core/CONTEXT.md`
- `src/agent_governance/artifact.py`

## Authorized scope

- Source-only non-Markdown measurement/lint tooling outside the T020 Consumer runtime/package boundary; prefer a small `tools/repository_context.py` entrypoint or equivalent source-only location.
- Focused deterministic tests, normally `tests/test_repository_context.py` or equivalent.
- A non-Markdown machine-readable accepted-baseline candidate, for example `baselines/repository-context-source-v1.json`.
- An optional schema under `schemas/` only if it materially improves deterministic validation.
- Executor handoff JSON.

## Explicit exclusions

- Any committed Markdown edit.
- Any change to `governance-core/`, `governance-skill/`, Consumer runtime semantics, profile behavior, or artifact packaging.
- Any file split/refactor performed because a measurement is large.
- Any hard budget/warning enforcement against repository content.
- Any LLM, network, embeddings, vector database, remote tokenizer, remote index or telemetry dependency.
- Any dependency/lock/configuration change unless the task cannot be completed with the existing/std-lib environment; in that case stop and report `BLOCKED` rather than broadening scope.
- Any claim that static graph fan-out is actual runtime RFO, TMC or CAR.
- Any bytes/characters-to-token heuristic represented as token count.

## Invariants / constraints

- The tool is source-maintenance tooling and MUST NOT be placed under `src/agent_governance/` or another path T020 copies into the Consumer artifact.
- Measurement must operate from tracked Git/source files, not untracked local caches or generated workspace noise.
- The baseline output must avoid self-referential instability. Either exclude the baseline file itself from measurement or use another deterministic design whose unchanged rerun is byte-identical.
- Results must be deterministic for an unchanged tracked tree, canonically ordered and portable across normal supported local environments.
- UTF-8 bytes are the canonical tokenizer-neutral physical size metric.
- Binary/non-text files must be handled deterministically without decoding failures.
- The accepted T018–T020 Consumer behavior/package baseline remains unchanged.

## Required measurement surface

At minimum record or report deterministically:

- source Git revision used for the measurement;
- tracked file path and classification by file type/extension where applicable;
- byte size;
- text line count where meaningful;
- character count where meaningful;
- Markdown heading count for Markdown;
- SHA-256/content digest;
- repository totals by useful file type/category;
- largest context-relevant files by physical footprint;
- explicit bootstrap physical footprint for `AGENTS.md` plus `docs/orchestrator/CHECKPOINT.md` as the current source cold-start router path;
- structural Markdown reference counts/graph only where links can be parsed deterministically without pretending all references imply actual context loading.

Optional reference-tokenizer counts may be added only if an already-available local tokenizer can be used with zero dependency/config drift and every count identifies the tokenizer. They are not required for acceptance.

## Acceptance criteria

### AC-CTX-1 — deterministic inventory
An unchanged tracked tree produces byte-identical canonical baseline/report data across repeated runs, excluding only explicitly documented volatile execution metadata that is not part of the canonical baseline.

### AC-CTX-2 — honest metrics
The baseline distinguishes physical metrics from actual/observed context-load metrics. No estimated value is mislabeled as an observed token/RFO/TMC/CAR measurement.

### AC-CTX-3 — bootstrap baseline
The output deterministically records the current physical cold-start footprint of `AGENTS.md` plus the current Orchestrator checkpoint without enforcing an arbitrary target.

### AC-CTX-4 — source-only isolation
The measurement tool/baseline is absent from the T020 Consumer artifact and the existing artifact-isolation regression remains green.

### AC-CTX-5 — no enforcement or mutation
Running the tool does not rewrite/split source documents, change repository policy, or fail solely because an existing file is physically large.

## Verification requirements

- Focused unit/integration tests for deterministic measurement and canonical ordering.
- A repeated-run identity test for the same fixture/tree.
- Negative/edge cases for binary files, unusual text files, and baseline self-exclusion/stability.
- T020 artifact-isolation tests proving source-only tooling does not enter the Consumer payload.
- Full deterministic regression suite.
- Ruff/format and Python compilation checks for added Python.
- Diff inspection proving no Markdown, dependency/lock, Consumer Core/Skill, or packaged-runtime drift.
- No network access.

The handoff MUST map `AC-CTX-1` through `AC-CTX-5` to the exact tests/evidence that directly prove each criterion and identify evidence type (`deterministic`, `package/isolation`, `negative-control`, etc.).

## Stop / escalation conditions

Stop and report `BLOCKED` rather than guessing if:

- accurate measurement requires a new dependency or host-specific remote service;
- source-only tooling cannot be kept outside the T020 artifact boundary;
- a requested metric cannot be defined deterministically without semantic/model judgment;
- producing a stable baseline would require editing Markdown or changing Consumer/package semantics.

## Expected handoff

Before claiming `DONE`, `BLOCKED`, or `PARTIAL`, persist the executor handoff at `handoffs/T030-executor-handoff.json` according to `docs/EXECUTOR-HANDOFFS.md`, commit and push all authorized work, and return only the canonical completion fields required by `docs/TASK-CONTRACTS.md`.
