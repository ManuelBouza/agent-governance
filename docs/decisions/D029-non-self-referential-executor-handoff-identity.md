# D029 — Non-self-referential executor handoff identity

Status: ACCEPTED
Authority: Human Owner / ChatGPT Orchestrator review contract

## Problem

The previous executor handoff contract required a handoff JSON committed on a topic branch to embed the exact pushed branch HEAD SHA of the commit containing that same handoff JSON.

That requirement is self-referential and cannot converge: changing the JSON to insert the commit SHA changes the Git object and therefore changes the SHA again.

T001 exposed this defect when the executor correctly separated the reviewed implementation commit from the later handoff-only commit and reported the actual pushed branch HEAD in the visible transport response.

## Decision

Executor handoff identity SHALL use two non-self-referential anchors:

1. **Persisted implementation anchor** — the handoff JSON records `implementation_head_sha`, identifying the committed implementation/test/eval state that the evidence describes. This SHA MUST be an ancestor of the final pushed topic-branch HEAD.
2. **Visible pushed branch HEAD** — after the handoff JSON itself is committed and the topic branch is pushed, the executor's minimal visible response reports `HEAD: <pushed-final-branch-head-sha>`.

The handoff JSON MUST NOT be required to contain the SHA of the commit that contains itself.

## Review invariant

ChatGPT validates a normal handoff by checking all of the following remotely:

- the visible `HEAD` equals the current pushed topic-branch HEAD;
- the handoff JSON exists at that visible HEAD;
- `implementation_head_sha` is reachable as an ancestor of the visible HEAD;
- the implementation diff/evidence described by the handoff corresponds to that implementation anchor plus any later handoff-only metadata commits;
- no unreported implementation changes occur after `implementation_head_sha` unless the handoff is regenerated with a new implementation anchor.

A handoff-only finalization commit may therefore follow the implementation commit without creating an impossible self-reference.

## Compatibility

Existing handoffs that use `head_sha` MAY be interpreted as an implementation/review anchor when accompanied by an explicit kind/note explaining that the actual pushed branch HEAD is supplied by the visible response. New or revised handoffs SHOULD use `implementation_head_sha` explicitly.

## Consequences

- `docs/EXECUTOR-HANDOFFS.md` is updated to remove the impossible convergence loop.
- T001 review revision R1 uses this model.
- Future Task Contracts should request an implementation anchor in the persisted JSON and the actual final pushed branch HEAD in the visible response.
- Git remains sufficient for audit: the visible HEAD resolves the exact handoff commit, while the JSON points backward to the implementation state it attests to.
