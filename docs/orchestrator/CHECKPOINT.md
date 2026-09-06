# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O221  
Canonical-Branch: `develop`  
Current-Work-Unit: T059 — reference-integrity baseline repair before T058 re-entry  
Chat-Closure: ACTIVE  
Active-Executor: none  
Active-Executor-Surface: none; T059 planning integration pending

## Durable frontier

- O220 closed the fully offline/self-contained Transfer Bundle delivery and left the source-maintenance frontier waiting for a Human objective.
- Human Owner explicitly authorized continuation of the previously stopped T058 work on 2026-09-06.
- T058's persisted Executor handoff remains `BLOCKED` on branch `feat/t058-chatgpt-portable-workspace-adapter`, branch HEAD `6ed319a1802cfd90d50d9dc95d969435c295a164`, implementation/review anchor `00134357e77f46d9cfcf82b03cedca3f386688f5`.
- The T058 implementation reported 26 focused tests passing; its prior terminal block was the repository-wide quality gate on the then-current `develop` baseline.
- Of the two prior baseline failures, the former governance-artifact failure is no longer represented by current `develop`.
- One baseline defect remains material: `tests/_helpers.py::looks_like_path()` misclassifies the valid D058 comparison expression ``develop == origin/develop`` in `AGENTS.md` as a repository path, causing the canonical Markdown reference-integrity test to fail.
- Orchestrator classified this as a deterministic harness defect rather than a reason to rewrite valid governance prose.
- T059 is the controlling repair Task Contract: `docs/tasks/T059-reference-integrity-baseline-repair.md`.
- T059 planning branch: `docs/t059-reference-integrity-baseline-repair`, created from `develop` HEAD `0feb43f2b367c3df351dcc55a42fd48658a0fba6`.
- T058 is no longer Human-frozen, but its existing implementation remains `DO_NOT_COPY` / non-integrable until T059 restores the baseline and the Orchestrator performs explicit T058 re-entry/revalidation against updated `develop`.

## Next action

1. Review and integrate the T059 planning branch into `develop` through PR.
2. Launch a fresh Executor work unit for T059 from the exact integrated `develop` revision containing the Task Contract.
3. Require focused reference-integrity verification plus the full repository quality gate.
4. If T059 converges green, re-enter T058 against current `develop`; do not assume the old T058 branch is directly reusable or integrable.

## T059 minimum load

1. current `develop`;
2. `AGENTS.md`;
3. `docs/orchestrator/CHECKPOINT.md`;
4. `docs/tasks/T059-reference-integrity-baseline-repair.md`;
5. `tests/_helpers.py`;
6. `tests/test_reference_integrity.py`.

## T058 re-entry minimum load after T059

1. current integrated `develop` and exact HEAD;
2. `docs/tasks/T058-chatgpt-portable-workspace-adapter.md`;
3. `handoffs/T058-executor-handoff.json` from branch `feat/t058-chatgpt-portable-workspace-adapter`;
4. compare current `develop` against T058 implementation/review anchor and branch HEAD;
5. controlling D066 portable-workspace semantics only where a concrete revalidation question requires them.

## Do not

Do not modify, copy, merge, clean up, or otherwise consume T058 implementation while T059/baseline verification is unresolved. Do not weaken `tests/test_reference_integrity.py` to ignore arbitrary slash-containing prose. Do not rewrite `AGENTS.md` merely to satisfy the classifier. Do not add dependencies for T059. Do not write directly to `develop` or `main`.
