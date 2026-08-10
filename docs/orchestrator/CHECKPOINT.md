# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O009  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001 is accepted and integrated. ChatGPT reviewed the next deterministic testing need against D026 / `docs/TESTING-AND-EVALUATION.md` and confirmed that the next bounded increment is T002 — synthetic coexistence fixtures and reference-target corpus.

`docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md` is the new controlling Task Contract. It is intended to become executable only after this planning change is merged to `develop` with status `READY`.

## Completed

- Source-product foundation decisions D022-D030 remain accepted.
- T001 is `ACCEPTED`; implementation integration commit: `80f7a4d5735bdc47539768eb844c55b7cc4dacdb`.
- Current pre-T002 `develop` frontier: `14fd49485911ce33697a8185123ee95f1b19803f`.
- The T002 candidate was independently validated against the testing strategy and D026 rather than adopted merely from the executor recommendation.
- T002 scope is limited to deterministic synthetic fixture/classification mechanics for `REUSE|ADAPT|COEXIST|MISSING|CONFLICT`.
- T002 explicitly excludes real external SDD/Skill dependencies, behavioral/model evals, state-machine/property testing, new dependencies/toolchain changes, and production runtime implementation.
- T002 includes no-SDD, reuse/adapt/coexist/conflict, same-name Skill precedence/trust separation, managed-surface collision, and generic known-system-shaped fixture requirements.

## Controlling References

For the immediate next action:

- `AGENTS.md`
- `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`
- `governance-core/COEXISTENCE.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

D029/D030 are controlling only for handoff identity and the existing external-overlay disposition; load them if exact mechanics need verification.

## Active Remote Artifacts

- Planning branch: `docs/t002-coexistence-fixtures`.
- T002 Task Contract: `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`.
- Expected executor branch after contract integration: `test/coexistence-fixtures`.
- Expected handoff: `handoffs/T002-executor-handoff.json`.
- No executor branch should be created before the T002 contract is merged into `develop`.

## Open Questions or Blockers

No architecture, dependency, workstation, or coexistence blocker is known for T002 planning.

The repository is still not declared stable/release-ready. T002 is one additional release-readiness increment, not the complete stable-version gate.

## Next Action

1. Review the `docs/t002-coexistence-fixtures` diff and merge the T002 planning PR into `develop` if it contains only the intended Task Contract/checkpoint changes.
2. Verify the resulting `develop` HEAD and that T002 is `READY` there.
3. Launch an Agente de IA Ejecutor from current `develop` with a minimal prompt pointing to `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`.
4. Executor creates `test/coexistence-fixtures`, implements only non-Markdown fixture/test/handoff artifacts, runs the canonical locked gate, commits/pushes, and returns only STATUS/HANDOFF/BRANCH/HEAD.
5. ChatGPT performs remote PD5 review before any implementation PR is opened.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`;
2. `docs/TESTING-AND-EVALUATION.md`;
3. `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`;
4. `governance-core/COEXISTENCE.md`;
5. `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

## Do Not Load or Do

- Do not reopen T001 absent a concrete regression.
- Do not broaden T002 into behavioral/model evals, property/state-machine testing, security dynamic testing, or production capability inventory code.
- Do not install or execute real Gentle-AI, Spec Kit, OpenSpec, or another SDD/Skill product for ordinary T002 regression.
- Do not add dependencies or change `pyproject.toml`/`uv.lock` without a persisted Task Contract revision.
- Do not re-enable or globally alter Gentle-AI RDD for this repository clone.
- Do not modify/delete external untracked `.atl/` state as source-product work.
- Do not launch the executor until the T002 contract is integrated into `develop`.
- Do not declare the source product stable/release-ready from T001/T002 alone.
