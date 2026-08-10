# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O008  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001 — deterministic test harness foundation — is accepted and integrated into `develop`. There is no active executor task. The next work unit is source-product planning for the next deterministic testing increment; the executor handoff recommends a T002 coexistence-fixture/reference-corpus increment, but that recommendation is non-authoritative until ChatGPT frames and persists a new Task Contract.

## Completed

- Source-product foundation decisions D022-D030 remain accepted.
- T001 passed PD5 reviews R1, R2, and R3 and is now `ACCEPTED`.
- Final reviewed executor branch: `test/governance-harness`.
- Final reviewed executor HEAD: `3b01e5cd67966011b47d62544feede0c352467b9`.
- Final implementation anchor: `89644eebe425f691ca3cf119902acffb4b77b6d8`.
- Final executor handoff: `handoffs/T001-executor-handoff.json`.
- Final canonical gate reported 82 passed, 0 failed, 0 skipped under Python 3.13.14 / uv 0.11.33 / pytest 9.1.1 / Ruff 0.16.2.
- T001 implementation PR #17 was squash-merged to `develop` as `80f7a4d5735bdc47539768eb844c55b7cc4dacdb`.
- The accepted harness now provides repository-owned locked uv/pytest/Ruff verification for canonical layout, direct local references, source/consumer separation, and harness-foundation invariants.
- R1-R3 review directives are resolved; no T001 rework remains active.
- The original unauthorized workstation `uv self update 0.11.33` remains recorded as historical procedural noncompliance and was not retroactively authorized.
- Gentle-AI RDD remains disabled only for the current clone under D030; no Gentle-AI/SDD repository asset is part of T001 and the canonical source toolchain no longer names `.atl` or another external overlay.

## Controlling References

For the immediate next action:

- `AGENTS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`
- `governance-core/COEXISTENCE.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`

T001 acceptance details are available in `docs/tasks/T001-deterministic-test-harness-foundation.md` and `handoffs/T001-executor-handoff.json` but do not need to be reloaded unless the next planning step depends on exact prior evidence.

## Active Remote Artifacts

- Canonical integration branch: `develop`.
- T001 accepted integration commit: `80f7a4d5735bdc47539768eb844c55b7cc4dacdb`.
- Historical executor branch: `test/governance-harness` at `3b01e5cd67966011b47d62544feede0c352467b9`.
- Persisted T001 handoff: `handoffs/T001-executor-handoff.json`.
- No active READY/IN_PROGRESS executor Task Contract exists after T001.

## Open Questions or Blockers

No active architecture, workstation, test-harness, or coexistence blocker remains from T001.

The repository is not declared stable/release-ready merely because T001 is accepted. Stable-version readiness remains a broader product milestone and must be established by the remaining roadmap/work units rather than inferred from one harness increment.

## Next Action

1. Review the next deterministic testing need against D019/D026 and the now-integrated T001 harness.
2. Treat the handoff recommendation “T002 — Synthetic coexistence fixtures and reference-target corpus” as a candidate, not as authority.
3. If that candidate is still the correct next increment, ChatGPT authors a new T002 Task Contract on a Markdown topic branch with focused synthetic coexistence/reference mechanics and explicit exclusions for real third-party dependencies, behavioral/model evals, and unnecessary toolchain expansion.
4. Review and merge the T002 contract into `develop` with status `READY` before launching any Agente de IA Ejecutor.
5. Only after that integration, launch an executor with a minimal pointer to the new Task Contract.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/TESTING-AND-EVALUATION.md`;
2. `docs/decisions/D026-ecosystem-coexistence-and-capability-reuse.md`;
3. `governance-core/COEXISTENCE.md`;
4. `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`.

Load the T001 task/handoff or R1-R3 review history only if a concrete T002 scope question requires exact prior evidence.

## Do Not Load or Do

- Do not reopen T001 or its resolved R1-R3 findings absent a concrete regression.
- Do not erase or retroactively authorize the historical uv workstation mutation.
- Do not re-enable or globally alter Gentle-AI RDD for this repository clone.
- Do not modify/delete external untracked `.atl/` state as source-product work.
- Do not treat an executor-proposed next task as authoritative strategy.
- Do not launch T002 or any executor work before a new Task Contract is persisted and `READY` on `develop`.
- Do not declare the source product stable/release-ready solely from T001 acceptance.
