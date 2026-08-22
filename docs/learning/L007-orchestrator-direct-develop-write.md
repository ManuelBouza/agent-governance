# L007 — Orchestrator direct write to `develop`

Learning ID: L007  
State: CONTROL_PLANNED  
Fingerprint: `workflow.direct_protected_branch_write`

## Detection

On 2026-08-17, while preparing `docs/CAPABILITY-SOURCE-CONTRACT.md`, ChatGPT Orchestrator intended to create the file on a fresh Markdown topic branch but issued a GitHub contents write with `branch: develop` after repeated failed attempts against a not-yet-created branch.

GitHub accepted that request and created commit:

`dffe9cc18696ae04e57b9fef9a4b5b833f0c3435`

containing a placeholder version of `docs/CAPABILITY-SOURCE-CONTRACT.md` directly on `develop`.

This violates the repository branch invariant even though the content was Markdown and Orchestrator-owned.

## Controlling policy

- `AGENTS.md` — normal Markdown work occurs on a short-lived topic branch from `develop` and returns through PR.
- `docs/BRANCHING.md` — normal direct development writes to `develop`/`main` are prohibited.

Role ownership does not waive branch discipline.

## Immediate containment

The Orchestrator did **not** reset, force-update, rewrite or hide the canonical history.

Containment is:

1. preserve the accidental direct commit as auditable evidence;
2. create `docs/canonical-capability-source-contract` from the resulting canonical `develop`;
3. replace the placeholder with the intended reviewed contract on that topic branch;
4. record this learning and checkpoint state on the topic branch;
5. review the aggregate diff and return the correction through PR to `develop`.

The correction restores valid repository content but does not claim that the original direct-write procedure was conforming.

## Causal analysis

The repository policy was explicit. The failure occurred because branch existence and target-branch identity were not treated as a mandatory fail-closed precondition immediately before the write.

The failed sequence was effectively:

```text
intend topic-branch write
    -> target branch does not yet exist
    -> repeated write attempts fail
    -> fallback write targets develop
    -> GitHub accepts direct mutation
```

The systemic defect is therefore a tooling/orchestration boundary problem:

```text
Orchestrator owns Markdown
    != Orchestrator may write Markdown to any branch
```

A safe write requires both:

```text
correct file ownership
+ approved topic-branch target
```

## Selected systemic control direction

For future Orchestrator repository writes:

1. resolve current canonical `develop` SHA;
2. create/verify the intended `docs/*` topic branch before any content mutation;
3. read the branch ref back and prove it exists;
4. every create/update/delete request must name that exact topic branch;
5. a write whose target is `develop` or `main` must be treated as invalid unless an explicit separately accepted emergency procedure authorizes it;
6. after writes, compare topic branch to the captured canonical base before PR creation;
7. unexpected canonical-branch movement caused by Orchestrator tooling is a procedural incident and must be persisted rather than repaired by history rewrite.

Where tooling permits, branch-target validation should become mechanically fail-closed rather than relying on operator attention alone.

## Verification status

L007 is `CONTROL_PLANNED`, not `VERIFIED`.

Verification requires representative future Orchestrator write flows showing that:

- a nonexistent topic branch cannot lead to fallback mutation of `develop`/`main`;
- a normal Markdown write succeeds only after topic-branch existence/identity is verified;
- canonical `develop` moves only through the reviewed PR integration path in that flow.

A later recurrence after the control is `VERIFIED` must be evaluated as a potential control failure under EGLL.
