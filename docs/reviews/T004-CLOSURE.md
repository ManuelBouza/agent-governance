# T004 Closure — model-facing eval cancelled by Human Owner

Status: CLOSED  
Task: `T004`  
Disposition: `CANCELLED_BY_HUMAN`  
Controlling decision: `docs/decisions/D037-deterministic-code-only-verification.md`

## Closure decision

The Human Owner explicitly directed Agent Governance to discard model-based tests and retain code-based verification.

T004 was created to execute real model sessions and evaluate D032 behavior from generated transcripts. That objective is no longer part of the product verification strategy.

T004 is therefore closed without implementation acceptance.

## Historical state at closure

Latest executor return before cancellation:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: eb20dc0fed2674190a82ef40aa0e02436c02ced4
```

Latest implementation anchor reported under D029:

`edc7fe186c0c84f6f30e3a2d8bbb4022ac609356`

The branch never produced the required real capability baseline:

- required sessions: 18;
- required turns: 21;
- completed sessions: 0;
- completed turns: 0;
- baseline artifact: none.

R1–R3 established useful diagnostic facts about the abandoned OpenCode/model path, but they are not product acceptance evidence.

## Integration disposition

Do not merge or cherry-pick the partial T004 implementation branch into `develop` or `main` as part of T004.

Specifically, do not integrate its model-facing harness/adapter solely because deterministic adapter tests passed. Those artifacts exist to support a verification mode that D037 has now removed.

Preserve the branch, handoff and reviews as audit/history unless normal repository retention later removes stale branches through an explicitly authorized maintenance action.

## D032 verification after closure

D032 remains accepted.

Its repository verification baseline is the accepted deterministic T003 contract and tests. Future D032 verification must follow D037:

- explicit fixtures;
- deterministic code assertions;
- property/state-machine verification where justified;
- Human/ChatGPT review for irreducible semantic judgment;
- no live LLM calls or stochastic transcript grading as repository acceptance gates.

This means the product does **not** claim that arbitrary models have been empirically proven to exhibit D032 behavior. It claims that the required Governance contract is defined and mechanically checked where mechanically representable.

## R1/R2/R3 status

The following reviews become historical and inactive:

- `docs/reviews/T004-R1.md`;
- `docs/reviews/T004-R2.md`;
- `docs/reviews/T004-R3.md`.

Do not continue their next actions.

## Next frontier

With T004 closed, the next source-product design/implementation frontier is D033–D036 under D037 code-only verification:

- execution authorization;
- runbook-first terminal-neutral procedure;
- current security authority + independent verification;
- existing-system assurance/audit.

Before implementation readiness, Strategy must produce a fresh D032 Primary Solution Diagram and quality/security triage for that combined or intentionally decomposed task.

## Acceptance effect

T004 terminal state is `CANCELLED_BY_HUMAN`, not `ACCEPTED`, `DONE` or `FAILED`.

No further executor action is required for T004.
