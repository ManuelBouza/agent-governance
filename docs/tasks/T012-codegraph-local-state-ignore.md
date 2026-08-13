# T012 — CodeGraph local-state ignore readiness

Task ID: T012  
Status: READY  
Type: infrastructure  
Base branch: `develop`  
Expected topic branch: `chore/codegraph-local-state-ignore`  
Expected executor handoff path: `handoffs/T012-executor-handoff.json`

## Objective

Prepare the source repository for local CodeGraph use by adding an effective root `.gitignore` rule for `.codegraph/` generated state. CodeGraph remains an optional executor capability, not product state or a correctness dependency.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D041-executor-process-autonomy.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/TASK-CONTRACTS.md`
- `.gitignore`

## Authorized scope

Tracked task changes are limited to root `.gitignore` plus the required executor handoff. Preserve all existing ignore behavior and add the minimal rule covering repository-local `.codegraph/`.

Local verification may create representative generated state only when it remains ignored and untracked.

## Exclusions

Do not modify committed Markdown, track `.codegraph/`, add CodeGraph to dependency/runtime configuration, add CodeGraph-dependent product/tests, alter executor-host configuration, or perform unrelated cleanup.

## Acceptance

- `.gitignore` effectively ignores repository-local `.codegraph/`;
- existing ignore entries remain intact except for the minimal addition;
- pushed diff contains no `.codegraph/` content and no unauthorized path;
- CodeGraph is not added as a product/runtime dependency;
- full pytest and Ruff verification remain green;
- the persisted handoff accurately reports identities, changed paths and evidence.

## Verification

Provide evidence that a representative `.codegraph/` path is ignored by Git, inspect the tracked diff, and run:

```text
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

## Stop / escalation

Return `BLOCKED` or `PARTIAL` if safe current base identity cannot be established, the baseline is independently red, or the result would require tracked/generated state outside scope.

## Expected handoff

Persist, commit and push `handoffs/T012-executor-handoff.json`, then return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T012-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
