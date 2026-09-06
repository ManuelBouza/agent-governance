# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O224  
Canonical-Branch: `develop`  
Current-Work-Unit: T059 revalidation after T060 baseline repair  
Chat-Closure: ACTIVE  
Active-Executor: none  
Active-Executor-Surface: T059 continuation pending on current `develop`

## Durable frontier

- Human Owner explicitly authorized continuation of the previously stopped T058 work on 2026-09-06.
- T058 remains non-integrable / `DO_NOT_COPY` on branch `feat/t058-chatgpt-portable-workspace-adapter`, branch HEAD `6ed319a1802cfd90d50d9dc95d969435c295a164`, implementation/review anchor `00134357e77f46d9cfcf82b03cedca3f386688f5`.
- T059 (`docs/tasks/T059-reference-integrity-baseline-repair.md`) corrected the reference-classifier defect on branch `fix/t059-reference-integrity-baseline-repair`; current pushed HEAD `c90df168375e2159344b161c83f1e1399f2c03dc`.
- T059 clean-worktree revalidation previously reported 49 focused reference-integrity tests passing plus Ruff, format, code-health, and diff checks passing. Its only blocker was the independent Governance artifact packaging defect.
- T060 corrected that packaging defect. The accepted implementation added `assets/REPOSITORY-BRANCH-PROTECTION.md` to the explicit Governance Skill artifact allowlist and added byte-equality regression coverage.
- T060 Plan & Trace re-entry was integrated by PR #307 with the narrow `PASS_WITH_KNOWN_T059_BASELINE` convergence rule for the exact known T059 failure only.
- T060 implementation was accepted and integrated by PR #308. Current `develop` HEAD after that integration is `b6c9c075a8db0be135ff5fe48e5452469889fe0c`.
- Baseline recovery now returns to T059. No T059 redesign is authorized unless revalidation against current `develop` exposes a T059-specific defect.

## Next action

1. Continue T059 on branch `fix/t059-reference-integrity-baseline-repair`.
2. Safely incorporate current canonical `develop` (`b6c9c075a8db0be135ff5fe48e5452469889fe0c`) into the T059 branch without discarding represented or unrepresented work.
3. Re-run the T059 focused reference-integrity tests and the complete repository quality gate from a clean remote-derived worktree.
4. Update `handoffs/T059-executor-handoff.json`, commit, and push.
5. If T059 converges green, integrate it into `develop` through PR.
6. Only then perform explicit T058 re-entry/revalidation against the new `develop`.

## T059 continuation minimum load

1. current `develop` and exact HEAD `b6c9c075a8db0be135ff5fe48e5452469889fe0c`;
2. `AGENTS.md`;
3. `docs/orchestrator/CHECKPOINT.md`;
4. `docs/tasks/T059-reference-integrity-baseline-repair.md`;
5. branch `fix/t059-reference-integrity-baseline-repair` and handoff;
6. `tests/_helpers.py` and `tests/test_reference_integrity.py`.

## T058 re-entry minimum load after T059

1. current integrated `develop` and exact HEAD;
2. `docs/tasks/T058-chatgpt-portable-workspace-adapter.md`;
3. `handoffs/T058-executor-handoff.json` from branch `feat/t058-chatgpt-portable-workspace-adapter`;
4. compare current `develop` against T058 implementation/review anchor and branch HEAD;
5. controlling D066 portable-workspace semantics only where a concrete revalidation question requires them.

## Do not

Do not modify, copy, merge, clean up, or otherwise consume T058 implementation while T059 is unresolved. Do not broaden T059 to change artifact packaging or governance semantics. Do not discard local/ambiguous work while updating the T059 branch. Do not write directly to `develop` or `main`.
