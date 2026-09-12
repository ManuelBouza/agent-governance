# R027 — Post-E2E candidate Git gate contract

Research-ID: R027  
Status: RESEARCH CANDIDATE — NON-NORMATIVE  
Date: 2026-09-12  
Evidence: `docs/research/R027-END-TO-END-GIT-GATE-QUALIFICATION.md`

This candidate incorporates the deterministic end-to-end findings. It is intended for review and any bounded real-Codex pilot. It does not change current repository policy.

## Candidate compact contract

```text
G0 — ENTRY

Before writable task execution, establish from current canonical Git state:
- correct repository and authorized work unit;
- fresh canonical remote/base identity;
- exact authorized topic branch and candidate/starting HEAD;
- required base/candidate relationship;
- exclusive writable worktree ownership;
- no ambiguous or unrepresented local state that would be overwritten or discarded.

If any fact is stale, conflicting or unsafe to establish, stop rather than guess, reset, clean or overwrite unknown work.

After recovery, worktree/branch switch, material remote/candidate movement, or newly controlling persisted authority, re-run the affected G0 checks before continuing.

LOCAL TRANSACTION ZONE

After G0 passes, the Executor owns compatible local Git and technical mechanics inside the authorized worktree/scope. Ordinary status, diff, staging, local commits, amend, tests and diagnosis do not by themselves require Governance revalidation and should remain unpublished until an authorized G1 boundary.

Preserve required evidence and do not discard ambiguous work, cross repository/scope boundaries, rewrite published history, or treat generated/untracked/runtime artifacts as irrelevant when they can affect the claimed verification result.

G1 — PUBLISH

Before terminal publication, require:
- required implementation/review/verification complete;
- complete represented implementation state committed;
- handoff committed and internally consistent;
- no unreported in-scope working state or verification-affecting residue makes the result misleading;
- publication still targets the authorized topic branch/remote.

Publish through the normal non-force path. Then verify:
- remote topic HEAD equals the intended final HEAD;
- handoff is readable at that remote HEAD;
- implementation/review HEAD is represented in the required ancestry.

Unexpected non-fast-forward movement fails closed and requires reconciliation; do not force the normal path.

REVIEW / INTEGRATION

Review and integrate the exact G1-published head. Branch name alone is not sufficient reviewed-state identity.

G2 — CLOSE

After accepted integration, require before retirement:
- merged/integrated identity and authorized target verified;
- current remote source HEAD equals the exact reviewed head;
- no unrepresented working-tree changes;
- no unique local commits or other unrepresented history would be discarded.

Unknown unique work or a post-review source-branch advance is REVIEW, not deletion authority.

When eligible:
- retire the remote source branch and verify absence;
- retire associated local worktree/topic branch only after unique-work checks pass;
- prune only stale administrative/tracking state;
- converge the primary checkout to the current authorized canonical base and verify it is clean/current.

The Executor chooses compatible Git commands under D054. Gate postconditions, not one command recipe, are the acceptance authority.
```

## Empirical refinements relative to the pre-E2E wording

Two clauses are intentionally stronger than the pre-E2E candidate:

1. G1 now distinguishes Git representation from **verification-affecting runtime residue**. The qualification demonstrated stale Python bytecode changing test meaning while tracked source was already correct.
2. G2 now requires an explicit **unique-commit/unrepresented-history** check. The qualification demonstrated a clean working tree with one unique local commit that would still be unsafe to retire.

These refinements preserve the original architecture: governance remains boundary-oriented, while concrete Git mechanics remain Executor-owned.
