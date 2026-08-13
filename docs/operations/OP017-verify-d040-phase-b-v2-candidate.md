# OP017 — Verify D040 Phase-B v2 candidate

Operation ID: OP017  
Status: READY  
Type: read-only pre-merge verification  
Base branch: `develop`

## Objective

Verify the exact current remote head of `docs/d040-phase-b-assurance-activation-v2` before merge.

The v2 candidate is rebuilt from current `develop` after accepted/integrated T011 readiness. It must remain Markdown-only and preserve the D040 Phase-B activation intent.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/reviews/T011-R1.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/ASSURANCE.md`

## Authorized operations

The executor may synchronize canonical refs, establish a safe current `develop` baseline, inspect the candidate diff, use a disposable checkout for the exact candidate HEAD, and run the required repository verification commands.

## Preconditions

Before running gates verify:

1. the candidate branch exists;
2. the exact candidate HEAD is recorded;
3. the candidate diff against current `develop` is Markdown-only;
4. `GOVERNANCE.md` declares Protocol `1.13.0`;
5. `ASSURANCE.md` is ACTIVE and routed by `GOVERNANCE.md`.

## Required verification

Run exactly:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

All four gates must pass without modifying repository content.

## Explicit exclusions

Do not edit, format, commit, push, repair, merge, close, or otherwise mutate repository content or branches during this operation. If a gate fails or the candidate changes during verification, return `BLOCKED`.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP017
CANDIDATE_HEAD: <exact-tested-sha>
MARKDOWN_ONLY: YES | NO
FOCUSED_PYTEST: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
REPO_MUTATION: NONE | <description>
```
