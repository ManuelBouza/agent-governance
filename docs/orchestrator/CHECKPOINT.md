# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O010  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001 is accepted and integrated. T002 — synthetic coexistence fixtures and reference-target corpus — is `READY` on `develop`, but before executor launch the Human Owner challenged an over-broad `.atl/` restriction. Research against current Gentle-AI documentation/implementation confirmed that `.atl/skill-registry.md` and its cache are normal project-local Skill discovery state refreshed automatically by supported OpenCode startup/plugin hooks.

D031 and `docs/reviews/T002-R0.md` now define the corrected source-maintainer boundary: Gentle-AI skill registry is a non-authoritative `COEXIST` capability; Gentle-AI RDD review/delivery authority remains a D030 `CONFLICT` disabled clone-locally.

## Completed

- Source-product foundation decisions D022-D030 remain accepted.
- T001 is `ACCEPTED`; implementation integration commit: `80f7a4d5735bdc47539768eb844c55b7cc4dacdb`.
- T002 Task Contract was integrated to `develop` by PR #19 as `f29e68470fdb7d835ede1cb5573e31cc3eeb34a1` and is `READY`.
- T002 remains limited to deterministic synthetic coexistence fixture/classification mechanics for `REUSE|ADAPT|COEXIST|MISSING|CONFLICT`.
- Current Gentle-AI research established:
  - OpenCode startup/plugin hooks normally refresh the project-local Skill registry;
  - the registry writes `.atl/skill-registry.md` and `.atl/.skill-registry.cache.json`;
  - registry refresh is fingerprint-cached;
  - the registry is discovery/delegation evidence, not Agent Governance approval or authority;
  - current `skill-registry refresh` ensures `.atl/` is present in root `.gitignore` unless invoked with `--no-gitignore`.
- D031 persists the source-maintainer classification: Gentle-AI skill registry `COEXIST`; RDD review/delivery authority remains governed by D030.
- `docs/reviews/T002-R0.md` supersedes only the original T002 clauses that prohibited `.atl/` refresh/mutation and blanket-forbade `.gitignore` change.
- T002 R0 authorizes only the minimal `.atl/` `.gitignore` compatibility entry; `.atl/` contents remain local/uncommitted and tests must not depend on Gentle-AI.

## Controlling References

For the immediate next action:

- `AGENTS.md`
- `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`
- `docs/reviews/T002-R0.md`
- `docs/decisions/D031-gentle-ai-skill-registry-source-maintainer-boundary.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`
- `governance-core/COEXISTENCE.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

D029/D030 remain controlling for handoff identity and clone-local RDD disposition.

## Active Remote Artifacts

- Canonical branch before this clarification PR: `develop@f29e68470fdb7d835ede1cb5573e31cc3eeb34a1`.
- Current Markdown clarification branch: `docs/t002-atl-runtime-boundary`.
- T002 Task Contract: `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`.
- Active pre-execution revision: `docs/reviews/T002-R0.md`.
- Expected executor branch after clarification integration: `test/coexistence-fixtures`.
- Expected handoff: `handoffs/T002-executor-handoff.json`.
- No T002 executor implementation should be launched until D031/R0 are integrated into `develop`.

## Open Questions or Blockers

No architecture, dependency, workstation, or coexistence blocker remains after D031/R0.

The repository is still not declared stable/release-ready. T002 remains one release-readiness increment.

## Next Action

1. Review the `docs/t002-atl-runtime-boundary` diff and merge the clarification PR into `develop` if it contains only D031, T002-R0, and this checkpoint update.
2. Verify resulting `develop` HEAD.
3. Launch an Agente de IA Ejecutor from current `develop` with a minimal prompt pointing to both T002 and T002-R0.
4. Allow normal Gentle-AI skill-registry read/refresh/cache behavior and the exact D031 `.gitignore` `.atl/` compatibility adaptation; do not commit `.atl/` contents.
5. Keep Gentle-AI RDD clone-locally disabled under D030; do not change global RDD state.
6. Executor implements only authorized non-Markdown fixture/test/handoff artifacts, runs the canonical locked gate, commits/pushes, and returns STATUS/HANDOFF/BRANCH/HEAD.
7. ChatGPT performs remote PD5 review before any implementation PR is opened.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T002-synthetic-coexistence-fixtures-reference-corpus.md`;
2. `docs/reviews/T002-R0.md`;
3. `docs/decisions/D031-gentle-ai-skill-registry-source-maintainer-boundary.md`;
4. `docs/TESTING-AND-EVALUATION.md`;
5. `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`;
6. `governance-core/COEXISTENCE.md`.

Load D029/D030 only if exact handoff/RDD mechanics need verification.

## Do Not Load or Do

- Do not reopen T001 absent a concrete regression.
- Do not broaden T002 into behavioral/model evals, property/state-machine testing, security dynamic testing, or production capability inventory code.
- Do not treat Gentle-AI skill registry use as forbidden merely because `.atl/` changes locally.
- Do not commit `.atl/` registry/cache contents or make T002 tests depend on them.
- Do not install/initialize real external SDD products for T002 regression.
- Do not add dependencies or change `pyproject.toml`/`uv.lock` without a persisted Task Contract revision.
- Do not re-enable or globally alter Gentle-AI RDD for this repository clone.
- Do not treat host Skill precedence/selection as Governance approval or authority.
- Do not launch T002 executor work until D031/R0 are integrated into `develop`.
- Do not declare the source product stable/release-ready from T001/T002 alone.
