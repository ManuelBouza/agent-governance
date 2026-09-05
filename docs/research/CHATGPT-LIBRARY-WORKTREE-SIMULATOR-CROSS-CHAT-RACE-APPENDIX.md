# R015 Appendix — real cross-chat lock race qualification

Research-ID: R015 (supporting appendix)  
Status: QUALIFIED / NON_NORMATIVE  
Opened: 2026-09-05  
Last-Reviewed: 2026-09-05  
Owner: ChatGPT Orchestrator  
Parent-Research: `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md`  
Related-Appendix: `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-LOCK-LIFECYCLE-APPENDIX.md`  
Normative-Authority: D058 remains the workspace-isolation requirement  
Decision-Ref: none

## Purpose

R015 previously qualified the worktree-simulator core, reusable sentinel lifecycle, wrong-owner gate, post-merge retirement, and sequential collision behavior. The remaining high-value concurrency gap was a real race from two physically independent ChatGPT conversations attempting to acquire the same free logical worktree lock.

This appendix records that cross-chat race qualification.

## Lock namespace

Repository:

`ManuelBouza/test_biblioteca`

Dedicated lock branch:

`lock/r015-race-20260905`

Sentinel:

`.chatgpt-worktree-lock.json`

The branch is dedicated to lock coordination. No ordinary project work is authorized on this branch.

## Attempt 1 — infrastructure-blocked / inconclusive

Both independent chats completed preflight against:

```text
branch HEAD: 364e576c172dc651f1ff30fc94e3e2f3667caf2c
sentinel: 404 / Not Found
```

Chat A reached GitHub and acquired the sentinel:

```text
owner: race-chat-a
work_unit: R015-RACE-A
commit: 778560268d4d10c6893c8950b388d9f5c83d4cd7
sentinel blob: 701aa77b47df2ba1b158402a00e1aa280087c5b5
```

Chat B did not reach GitHub. Its tool call was blocked by an OpenAI safety-control layer before a GitHub response was produced.

Therefore Attempt 1 is classified:

`INCONCLUSIVE / INFRASTRUCTURE_BLOCKED`

It is not evidence for or against GitHub mutual exclusion.

The winner sentinel was then deleted with its exact blob SHA. Reset commit:

`f7de8a09f2bc98b1bc76c8c17c4aee2f39125d5c`

Post-reset state:

```text
branch HEAD: f7de8a09f2bc98b1bc76c8c17c4aee2f39125d5c
sentinel: 404 / Not Found
```

## Attempt 2 — real cross-chat race

Two new independent ChatGPT conversations were used.

Both completed preflight against exactly the same free state:

```text
expected/observed branch HEAD:
f7de8a09f2bc98b1bc76c8c17c4aee2f39125d5c

sentinel:
404 / Not Found
```

The Human Owner then sent `GO` to both conversations in close succession.

### Competitor A

Identity:

```text
owner: race2-chat-a
work_unit: R015-RACE2-A
```

Result:

```text
RACE_RESULT: SUCCESS
HTTP_STATUS: 201
commit: 890244fb5c5f76971e376ffb49e5e90cc57d052c
```

Independent GitHub verification proved:

```text
commit message: test: R015 race2 acquire chat-a
parent: f7de8a09f2bc98b1bc76c8c17c4aee2f39125d5c
tree: ed36e962ff421a1d582c42993d6f5fe5ec159ab1
```

The winning sentinel content was:

```json
{
  "schema": "chatgpt-worktree-simulator/v1",
  "race_id": "R015-RACE2-20260905",
  "owner": "race2-chat-a",
  "work_unit": "R015-RACE2-A",
  "state": "ACTIVE"
}
```

Winning sentinel blob:

`25930aa8403b2481b9077ad48399fb78f11b5c33`

### Competitor B

Identity:

```text
owner: race2-chat-b
work_unit: R015-RACE2-B
```

Result:

```text
RACE_RESULT: BLOCKED
COMMIT_SHA: NONE
HTTP_STATUS: 409
ERROR_MESSAGE: is at 890244fb5c5f76971e376ffb49e5e90cc57d052c but expected f7de8a09f2bc98b1bc76c8c17c4aee2f39125d5c
```

No `R015 race2 acquire chat-b` commit was found in the repository.

The final lock branch HEAD was exactly the winner commit:

`890244fb5c5f76971e376ffb49e5e90cc57d052c`

Therefore exactly one competitor mutated the lock branch.

## Concurrency finding — branch CAS is the observed race primitive

The sequential reusable-lock test had already shown this occupied-path behavior:

```text
sentinel already exists
-> second create_file
-> HTTP 422
```

The real cross-chat race exposed a stronger and more precise concurrent behavior:

```text
both contenders observe FREE at HEAD H
A commits lock from H -> H1
B attempts write expecting H
GitHub/connector observes branch at H1
-> HTTP 409 stale expected branch SHA
-> B creates no commit
```

Therefore the qualified concurrent mutual-exclusion mechanism is not merely "the file path exists". In the tested connected GitHub write path, the lock branch also behaves as an optimistic compare-and-swap authority on its expected HEAD.

For a dedicated lock branch this is desirable:

```text
same free HEAD observed by multiple contenders
-> at most one contender advances the branch from that HEAD
-> stale contenders fail closed
```

The sentinel remains necessary because it carries current owner/work-unit/state identity and supports explicit release/reacquisition.

The combined qualified model is now:

```text
dedicated lock branch
+ expected-HEAD freshness/CAS
+ .chatgpt-worktree-lock.json owner sentinel
```

## Important design constraint

Because any unexpected lock-branch advancement can invalidate a contender's expected HEAD, the dedicated lock branch must remain a coordination-only authority.

Do not place ordinary project commits or unrelated metadata writes on the same lock branch while acquisition is in progress.

If the lock branch changes unexpectedly:

`BLOCKED_STALE_LOCK_HEAD`

The caller must re-read and classify state. It must not force, reset, or silently retry into writable mode.

## Release after race

After independent verification, the winning sentinel was released using its exact blob SHA:

```text
winning blob: 25930aa8403b2481b9077ad48399fb78f11b5c33
release commit: c2d99a2b701d3ca27c1b9a011e773254f23f28c2
```

A subsequent sentinel fetch returned:

`404 / Not Found`

The reusable lock namespace therefore returned to FREE state.

## Qualification result

`PASS`

The previously open R015 gap:

`true simultaneous/tightly concurrent two-chat race against the same free lock`

is now closed for the tested ChatGPT + GitHub connector path.

Supported bounded conclusion:

```text
two independent ChatGPT conversations can observe the same free lock state;
when they contend on the same dedicated lock branch, exactly one tested contender advances the branch and acquires the sentinel;
the stale contender is rejected with HTTP 409 and produces no competing commit.
```

This does not prove implementation details for every future connector/runtime version. The result is empirical and version/surface-sensitive.

## Updated capability delta

| Capability | Status | Evidence |
| --- | --- | --- |
| two independent chats preflight same free lock state | VERIFIED | R015 Race 2 |
| real cross-chat contention on same lock namespace | VERIFIED | R015 Race 2 |
| exactly one contender commits acquisition | VERIFIED | A commit `890244fb...`; no B commit |
| stale concurrent contender rejected | VERIFIED | B HTTP 409 expected `f7de8a09...`, actual `890244fb...` |
| winning sentinel owner matches successful chat | VERIFIED | owner `race2-chat-a` |
| post-race explicit release | VERIFIED | commit `c2d99a2...`; sentinel 404 |
| sequential occupied-sentinel rejection | VERIFIED | prior HTTP 422 test |
| crash/orphan automatic recovery | NOT VERIFIED | future qualification |
| TTL / heartbeat | NOT VERIFIED | future qualification |
| closed-unmerged cross-chat resume | NOT VERIFIED | future qualification |
| branch/ref retirement mechanics | NOT VERIFIED | future qualification |

## Disposition

R015 remains:

```text
Research-State: COMPLETE
Decision-State: NOT_REQUIRED
```

This appendix adds qualification evidence only. It does not itself adopt a normative Agent Governance adapter or change D058.