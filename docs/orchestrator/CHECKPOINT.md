# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O225  
Canonical-Branch: `develop`  
Current-Work-Unit: T058 formal re-entry/revalidation after baseline recovery  
Chat-Closure: ACTIVE  
Active-Executor: none  
Active-Executor-Surface: T058 continuation pending on current `develop`

## Durable frontier

- Human Owner explicitly authorized continuation of the previously stopped T058 work on 2026-09-06.
- T060 artifact-packaging baseline repair is accepted and integrated.
- T059 reference-integrity baseline repair is accepted and integrated by PR #310.
- Current canonical `develop` HEAD is `581b8f8bd785a78b942cffee320e3754707247e1`.
- Repository baseline recovery is complete: T059 final verification reports 49 focused reference-integrity tests passing, Ruff/format/code-health/diff checks passing, and the complete repository suite passing with 493 tests.
- T058 remains on branch `feat/t058-chatgpt-portable-workspace-adapter`, current branch HEAD `6ed319a1802cfd90d50d9dc95d969435c295a164`, implementation/review anchor `00134357e77f46d9cfcf82b03cedca3f386688f5`.
- The persisted T058 handoff is `BLOCKED` only by the two baseline failures now repaired by T059/T060. Its focused implementation evidence reports 26 T058 tests passing plus Ruff, format, code-health, diff, archive-safety and network-independence checks passing.
- Orchestrator re-entry review found no contract/design defect requiring T058 reimplementation. Existing implementation MAY be reused only through explicit continuation/revalidation against current `develop`; it is no longer `DO_NOT_COPY` solely because the former baseline blockers are resolved.
- Reuse authorization is bounded: do not silently reinterpret D066/R014/R015 gaps, expand scope, or treat prior verification as current. Current-base integration and complete reverification are mandatory.

## Next action

1. Continue T058 on branch `feat/t058-chatgpt-portable-workspace-adapter`.
2. Safely incorporate canonical `develop` HEAD `581b8f8bd785a78b942cffee320e3754707247e1` into the represented T058 branch without discarding represented or ambiguous local work.
3. Re-review the existing implementation against current `docs/tasks/T058-chatgpt-portable-workspace-adapter.md` and controlling D066 semantics; stop for SDD re-entry if a material mismatch is discovered.
4. Run all required focused T058 tests and the complete repository quality gate from a clean remote-derived worktree.
5. Update `handoffs/T058-executor-handoff.json`, commit, and push.
6. If T058 reports `DONE`, Orchestrator performs Converge/Accept on GitHub and integrates through PR to `develop`.

## T058 continuation minimum load

1. current `develop` and exact HEAD `581b8f8bd785a78b942cffee320e3754707247e1`;
2. `AGENTS.md`;
3. `docs/orchestrator/CHECKPOINT.md`;
4. `docs/tasks/T058-chatgpt-portable-workspace-adapter.md`;
5. branch `feat/t058-chatgpt-portable-workspace-adapter` and `handoffs/T058-executor-handoff.json`;
6. controlling `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` and `docs/CHATGPT-PORTABLE-GIT-WORKSPACE.md` only as needed to resolve concrete revalidation questions;
7. current T058 implementation/test files listed in the handoff.

## Do not

Do not reimplement T058 from scratch merely because its old handoff is `BLOCKED`. Do not copy only selected old files onto a new branch without preserving/reconciling represented Git history. Do not broaden T058, close unresolved D066/R014/R015 gaps, add Library/GitHub network mutations, or weaken fail-closed semantics. Do not discard local/ambiguous work. Do not write directly to `develop` or `main`.
