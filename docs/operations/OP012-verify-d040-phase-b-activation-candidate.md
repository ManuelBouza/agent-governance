# OP012 — Verify D040 Phase-B activation candidate

Operation ID: OP012  
Status: READY  
Type: read-only pre-merge verification  
Base branch: `develop`

## Objective

Verify the exact current remote head of the future D040 Phase-B Markdown activation branch before it is merged to `develop`, proving that Protocol `1.13.0` activation and `ASSURANCE.md` routing preserve the deterministic repository baseline without any executor-owned source mutation.

## Durable candidate target

Candidate branch:

`docs/d040-phase-b-assurance-activation`

The executor MUST resolve the exact current remote candidate HEAD from canonical Git at execution time. Chat text is not authority for the candidate SHA.

The candidate is expected to contain only ChatGPT-owned Markdown activation/review/checkpoint changes. Any non-Markdown candidate diff is a verification failure and MUST be reported rather than repaired.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/reviews/T010-R1.md`
- `docs/learning/L001-protocol-version-baseline-drift.md`
- `governance-core/GOVERNANCE.md`
- `governance-core/ASSURANCE.md`
- `docs/OPERATION-CONTRACTS.md`

## Authorized operations

The executor may synchronize canonical Git refs; establish a safe current `develop` baseline under D042; inspect the candidate branch and its diff against current `develop`; create/use a disposable local checkout/worktree for the exact candidate HEAD; run the required deterministic verification commands; and inspect resulting command output/status.

The executor chooses its compatible internal process and tools under D041.

## Explicit exclusions

The executor MUST NOT modify/create/format/commit/push repository content; alter the candidate branch or `develop`; repair failures; update lockfiles/dependencies/configuration; create a handoff artifact; initialize CodeGraph/SDD tracked project state; access real systems; use network/provider/model judgment as a verification gate; merge/close PRs; or perform any remediation.

If verification reveals a required non-Markdown change, return `BLOCKED` so ChatGPT can create a new Task Contract rather than mutating the candidate under this operation.

## Preconditions

Before running gates, verify all of the following:

1. current local bootstrap baseline is safely reconciled with canonical `origin/develop`;
2. remote candidate branch `docs/d040-phase-b-assurance-activation` exists;
3. exact candidate HEAD is recorded for the run;
4. candidate diff against current `develop` contains no non-Markdown paths;
5. candidate Core state declares `Protocol-Version: 1.13.0`;
6. candidate `ASSURANCE.md` is active rather than staged and is routed by `GOVERNANCE.md`.

Failure of any precondition returns `BLOCKED` rather than compensating or editing.

## Required verification

Run exactly these repository gates against the exact candidate HEAD:

```text
uv run --locked pytest -q tests/test_assurance_audit_contract.py
uv run --locked pytest -q
uv run --locked ruff check .
uv run --locked ruff format --check .
```

All four gates MUST exit successfully.

The full-suite PASS must occur without any test/helper current-version literal update after T010. The operation must not modify the working tree to obtain PASS.

## Verification evidence

Before returning, determine and report:

- exact candidate HEAD tested;
- whether candidate diff is Markdown-only;
- focused pytest result;
- full pytest result;
- Ruff check result;
- Ruff format-check result;
- whether repository tracked/untracked state created by the operation requires cleanup;
- confirmation that no repository content commit/push occurred.

## Stop / escalation

Return `BLOCKED` if any precondition fails, any gate fails, candidate HEAD changes during verification, required verification cannot run in the locked environment, or PASS would require repository mutation.

## Completion response

Return only:

```text
STATUS: DONE | BLOCKED | PARTIAL
OPERATION: OP012
CANDIDATE_HEAD: <exact-tested-sha>
MARKDOWN_ONLY: YES | NO
FOCUSED_PYTEST: PASS | FAIL | NOT_RUN
FULL_PYTEST: PASS | FAIL | NOT_RUN
RUFF_CHECK: PASS | FAIL | NOT_RUN
RUFF_FORMAT: PASS | FAIL | NOT_RUN
REPO_MUTATION: NONE | <description>
```
