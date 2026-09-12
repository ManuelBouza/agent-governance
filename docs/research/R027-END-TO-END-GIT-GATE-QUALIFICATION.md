# R027 — End-to-end Git gate qualification

Research-ID: R027  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Date: 2026-09-12  
Owner: ChatGPT Orchestrator  
Qualification repository: `ManuelBouza/test_biblioteca`  
Scope: deterministic Git/GitHub qualification of the candidate `G0 -> LOCAL -> G1 -> review/merge -> G2` transaction model. This qualification is parallel to the active T062 scientific frontier and does not authorize, consume, replay, or modify any T062 provider/model execution.  
Normative change: none

## 1. Purpose

R027 previously established a static and prospective case for concentrating generic Executor/Codex Git governance at three semantic boundaries:

```text
G0 ENTRY
    -> authoritative repo / branch / base-or-candidate / worktree / freshness

LOCAL TRANSACTION ZONE
    -> Executor-owned status / diff / add / commits / amend / tests / diagnosis

G1 PUBLISH
    -> complete represented state + handoff + normal push + exact remote HEAD

review / merge

G2 CLOSE
    -> exact-head branch/worktree retirement + no unique work + primary convergence
```

The remaining question for this qualification was whether the model actually fails closed across representative Git failure modes rather than merely reading well on paper.

The test deliberately included negative cases and retained failed harness attempts as evidence. A failed harness attempt is not counted as a gate PASS merely because later code was corrected.

## 2. Isolation and non-interference

The qualification used the disposable private repository:

`ManuelBouza/test_biblioteca`

Initial base:

`main@af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`

The Agent Governance repository's active T062/O281 frontier was not used as an execution surface. No T062 provider/model calls were made, no T062 scientific branch was mutated, and no T062 evidence was consumed.

All R027 branches created by this qualification in `test_biblioteca` were retired after evidence capture. A final direct GitHub branch search for `r027` returned no branches.

Historical R015/R026/test branches in the disposable repository were not modified by the cleanup.

## 3. Phase 1 — G0 / LOCAL / G1

### 3.1 Attempt 1 — useful failure

GitHub Actions run:

- run: `34680738188`
- job: `103518794780`
- harness commit: `18784f9f2aca1f02bec88b0a1ba5ffd6033e0151`

The run passed the intended G0 and LOCAL checks before G1:

- canonical remote `main` matched the local remote-tracking identity;
- a deliberately stale remote-tracking ref was detected before authority use;
- a fresh fetch restored the canonical identity;
- the exact topic branch/candidate/worktree identity was established;
- an unrepresented dirty file caused entry to fail closed;
- after exact synthetic-state removal, G0 was revalidated;
- native Git refused a second worktree for the already checked-out writable branch;
- the task branch was absent remotely throughout LOCAL work;
- an intentional failing test was diagnosed;
- the source was repaired and the test passed;
- `status`, `diff`, `add`, local commit and `commit --amend` all occurred without remote publication.

The run then failed the G1 clean-state check because Python had generated:

`r027_e2e/__pycache__/`

This was an important positive discovery even though the overall run failed: G1 correctly refused to treat the repository state as fully represented while a runtime artifact remained unreported/unclassified.

The implementation commit in this attempt was:

`6e9741c7822cdabe897d2a44b57b319f8277e844`

No task branch was published from this failed attempt.

### 3.2 Attempt 2 — runtime freshness discovery

GitHub Actions run:

- run: `34680784672`
- job: `103518922556`
- harness commit: `be75a4821e25c9ce8eb2a5e904ac26847e659fa0`
- artifact: `r027-gates-phase1-34680784672`
- artifact ID: `10294177000`
- artifact SHA256: `d98b0a93f1090b060698d696ba1e01a95ca52b82a9abe3f0d7da91cbc2c29b3c`

This attempt exposed a second, subtler issue inside LOCAL verification.

The first test imported a module containing `return 1` and correctly failed because the expected value was `2`. The source was then rewritten to `return 2`. Because the rewrite occurred within the same timestamp granularity and preserved the source file size, a later Python process reused stale bytecode cache metadata and still observed `1 != 2`.

The important conclusion is:

```text
Git working-tree cleanliness / source diff correctness
!=
runtime verification freshness
```

A runtime artifact can affect verification even when the tracked source is already correct. Therefore the LOCAL/G1 boundary must preserve D076-compatible reasoning about executable/runtime artifacts that materially influence the claimed verification result.

No task branch was published from this failed attempt.

### 3.3 Attempt 3 — successful G0 / LOCAL / G1 qualification

GitHub Actions run:

- run: `34680839587`
- job: `103519070475`
- harness commit: `94d6f14eace9a04c5ae6c936d044b7494a91002c`

Identities:

- base: `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`
- task branch: `test/r027-gates-34680839587`
- implementation HEAD: `e2e07f4f069f93e550f7d4d65de67f9b3ad8af34`
- final handoff/publication HEAD: `cf801fc78b7f71cb36c16a173cd3dd122e9eea19`

The run explicitly classified the stale Python bytecode condition, removed only the exact known mechanical cache, reran the test successfully, and later allowed G1 to detect the regenerated cache again before publication.

#### G0 results

| Check | Result |
| --- | --- |
| canonical remote freshness | PASS |
| deliberately stale remote-tracking identity detected | PASS |
| recovery fetch restores canonical identity | PASS |
| exact authorized topic/candidate/worktree identity | PASS |
| dirty/unrepresented local state blocks entry | PASS |
| controlled cleanup followed by G0 revalidation | PASS |
| second writable worktree for same branch refused | PASS |

#### LOCAL results

| Check | Result |
| --- | --- |
| remote task branch absent before G1 | PASS |
| `status` / `diff` inspection | PASS |
| intentional failing test / diagnosis | PASS |
| repair / rerun | PASS |
| stale bytecode cache detected as verification-affecting runtime state | PASS |
| exact cache invalidation + rerun | PASS |
| `add` / commit / amend | PASS |
| no remote publication during LOCAL operations | PASS |

#### G1 results

| Check | Result |
| --- | --- |
| regenerated unrepresented runtime residue blocks publication | PASS |
| exact mechanical residue classified/removed, then clean state revalidated | PASS |
| implementation and handoff state fully committed | PASS |
| implementation HEAD is ancestor of final handoff HEAD | PASS |
| one planned normal non-force push | PASS |
| remote HEAD equals intended final HEAD | PASS |
| handoff readable from represented remote HEAD | PASS |
| stale sibling normal push rejected non-fast-forward | PASS |
| concurrent winner preserved after stale push rejection | PASS |

The handoff recorded the runtime cache as a non-persisted mechanical ephemeral artifact rather than pretending the artifact never existed.

## 4. G1 race qualification

A separate synthetic race created two sibling candidates from the same base.

The concurrent winner was pushed first to the shared remote race branch. The stale sibling then attempted an ordinary normal push.

Result:

```text
stale normal push -> rejected non-fast-forward
remote winner      -> unchanged
force              -> never used
```

The synthetic race branch was retired after evidence capture.

This empirically supports the R027 claim that normal G1 publication can fail closed using native Git non-fast-forward semantics without adding command-level governance or normal force-push logic.

## 5. Review / merge qualification

A real disposable pull request was opened from the exact G1-published head:

`ManuelBouza/test_biblioteca#5`

PR identity:

- base: `main`
- base SHA: `af02345fcfed0ebe7d4b6503af7e89cdf48b84cf`
- source branch: `test/r027-gates-34680839587`
- reviewed head SHA: `cf801fc78b7f71cb36c16a173cd3dd122e9eea19`
- changed files: 3
- mergeable before merge: true

The reviewed patch contained exactly:

- `r027_e2e/transaction.py`
- `r027_e2e/test_transaction.py`
- `r027_e2e/handoff.json`

The merge used the expected reviewed head as a compare-and-merge guard rather than trusting the branch name alone.

Squash integration result:

`main@56a72cf847663c6af47e718fc52373072bf840a4`

The PR record remained durably tied to the reviewed head `cf801fc...` after merge.

## 6. Phase 2 — G2 qualification

### 6.1 G2 run 1 — semantic checks pass; harness command bug afterward

GitHub Actions run:

- run: `34680993162`
- job: `103519473476`
- harness head: `4e2ff48edf0aea91d4de8324001336f05f4e31aa`
- artifact: `r027-gates-g2-34680993162`
- artifact ID: `10293644175`
- artifact SHA256: `f07681af518ad55b098bcd00cf1a762ce1d1919ffdcf2e7ca5acaaf1c7daecf7`

The run verified:

- merged `main` exactly equalled `56a72cf...`;
- source branch still exactly equalled reviewed PR head `cf801fc...`;
- a cleanup worktree started from the exact reviewed head;
- an untracked/unrepresented file blocked normal `git worktree remove`;
- after exact harness-owned cleanup, the worktree became clean again;
- a **clean** worktree containing one unique local commit was detected as unsafe for retirement;
- a post-review remote branch advancement was classified `REVIEW` and deletion was withheld;
- the real merged source branch still matched the exact reviewed head;
- the real remote source branch was retired and absence verified;
- its associated local worktree and local topic branch were retired safely.

#### Important G2 finding — clean status is insufficient

The synthetic unique local commit was:

`a27b1c1e6d6dac6e6c952eb4a32645d423027197`

At that point:

```text
git status = clean
local branch contains unique commit = true
```

Therefore:

```text
G2 safe retirement
!=
working-tree clean only
```

G2 needs an explicit unique-work/reachability check in addition to working-tree state. Unknown unique commits must become `REVIEW` and be preserved; they must not be reset merely to make cleanup pass.

The harness reset the synthetic unique commit only because the exact commit had been created by the qualification itself and was independently identified by its exact expected message/state.

#### Important G2 finding — post-review advance

A synthetic remote branch was first created at the expected reviewed head and then advanced with an additional harness-owned commit.

The exact-head mismatch was detected. The branch was classified `REVIEW`, and the test verified it remained present rather than deleting it automatically. It was disposed only afterward under explicit harness ownership.

This validates the existing exact-reviewed-head cleanup invariant.

#### Harness failure after G2-F

The run then failed while trying to restore the primary checkout because the test harness used an ambiguous short refspec:

```text
git fetch --prune origin main:refs/remotes/origin/main --force
```

In this context Git interpreted the source side unexpectedly and deleted the local remote-tracking ref, after which `origin/main` could not be resolved.

This failure occurred **after** the actual source branch and associated cleanup worktree had already been safely retired.

The failure is evidence for, not against, the D054 mechanics boundary:

```text
Governance should specify the semantic postcondition
Executor should resolve compatible Git command mechanics
```

R027 should not encode a brittle refspec recipe merely because one worked in a harness.

### 6.2 G2 continuation — success

The continuation corrected only the harness mechanics, using an explicit remote refspec:

```text
+refs/heads/main:refs/remotes/origin/main
```

GitHub Actions run:

- run: `34681042516`
- job: `103519614863`
- harness head: `0f78bb95d2488336cd38cf9aa557094d3c8eeaf6`
- conclusion: SUCCESS
- artifact: `r027-gates-g2-continuation-34681042516`
- artifact ID: `10294078346`
- artifact SHA256: `836b4d56dbc4ab48f7e8af2d9423f8b711c345a6735b009e648c5efd700d7ca8`

The continuation verified:

- prior source-branch retirement remained durable;
- merged `main` remained exactly `56a72cf...`;
- primary checkout converged to current remote `main`;
- local `HEAD == remote main == 56a72cf...`;
- tracked working state was clean;
- all harness-created R027 auxiliary branches were retired only after exact expected-head checks;
- the phase-1 harness branch was retired only at its exact qualified head `94d6f14...`;
- the closure harness self-retired only at its exact run head `0f78bb95...`;
- no R027 remote ref remained;
- exactly one clean primary worktree remained in the runner repository.

A direct GitHub branch search after completion returned no branch containing `r027`.

## 7. Refined gate semantics from empirical evidence

### G0 — ENTRY

The empirical qualification supports these generic semantic postconditions:

```text
canonical remote identity is fresh
+ exact authorized branch/candidate/base relationship is known
+ exclusive writable worktree is established
+ no ambiguous/unrepresented local state would be overwritten
=> writable transaction may open
```

Stale authority, collision, or ambiguous state fails closed. Recovery or cleanup that could have changed those facts is followed by G0 revalidation.

### LOCAL TRANSACTION ZONE

The Executor may use compatible local Git mechanics without turning every local mutation into a governance event:

```text
status / diff / add / commit / amend / tests / diagnosis
```

provided it remains inside the authorized repository/worktree/scope and does not cross an uncontracted publication boundary.

However, verification-affecting runtime/ephemeral artifacts are not automatically irrelevant merely because they are untracked or generated. The stale-bytecode result demonstrates that such state can change the meaning of test evidence independently of tracked Git state.

### G1 — PUBLISH

The empirical qualification supports separating two subclaims:

**Representation/coherence**

```text
required implementation/review/verification complete
+ represented implementation state committed
+ handoff committed and internally consistent
+ no unreported in-scope or verification-affecting residue makes the result misleading
```

**Publication**

```text
normal non-force publication
+ remote HEAD == intended final HEAD
+ handoff readable at that remote HEAD
+ implementation HEAD represented in required ancestry
=> remote review candidate published
```

A stale non-fast-forward publication fails closed and preserves the concurrent winner.

### G2 — CLOSE

The empirical qualification strengthens the candidate G2 contract:

```text
accepted/merged integration identity verified
+ current remote source HEAD == exact reviewed PR head
+ working tree has no unrepresented changes
+ local branch/worktree has no unique unrepresented commits
+ remote source branch retired and absence verified
+ associated local worktree/branch safely retired
+ primary checkout converged to current canonical base
=> work-unit Git lifecycle closed
```

A clean `git status` is not sufficient evidence of “no unique work.” Reachability/unique-commit state must also be considered.

Unknown unique work or post-review remote advancement becomes `REVIEW`, not deletion authority.

## 8. Command syntax is not the policy surface

The qualification intentionally exercised real Git mechanics, but the result does not justify codifying those exact commands.

Two harness-specific phenomena demonstrate why:

1. runtime bytecode freshness affected verification independently of Git source state;
2. a syntactically legal-looking short fetch refspec behaved differently than the intended semantic postcondition.

The durable rule should therefore remain:

```text
Governance defines semantic entry/publication/closure facts.
D054-compatible Executor mechanics satisfy those facts.
```

A specific command recipe may be operational guidance, but it should not become the acceptance authority when equivalent safe mechanics exist.

## 9. Qualification matrix

| Area | Result |
| --- | --- |
| G0 canonical remote freshness | PASS |
| G0 stale-local identity detection | PASS |
| G0 exact branch/candidate/worktree | PASS |
| G0 dirty/unrepresented-state block | PASS |
| G0 duplicate writable worktree defense | PASS |
| LOCAL inspection/staging/commits/amend | PASS |
| LOCAL tests/diagnosis without publication | PASS |
| LOCAL verification-affecting runtime artifact discovery | PASS / specification refinement required |
| G1 unrepresented residue block | PASS |
| G1 one normal final publication | PASS |
| G1 exact remote HEAD verification | PASS |
| G1 remote handoff readability/ancestry | PASS |
| G1 stale sibling non-fast-forward rejection | PASS |
| review against exact G1 HEAD | PASS |
| merge guarded by expected reviewed HEAD | PASS |
| G2 merged/frozen exact-head verification | PASS |
| G2 dirty worktree block | PASS |
| G2 clean-but-unique-commit block | PASS / specification refinement required |
| G2 post-review advance -> REVIEW/preserve | PASS |
| G2 remote branch retirement/absence | PASS |
| G2 local worktree/topic retirement | PASS |
| G2 primary canonical-base convergence | PASS |
| G2 final R027 remote residue | PASS: none |
| T062/provider-call isolation | PASS |

## 10. What is and is not qualified

### Qualified empirically

The Git/GitHub semantics of the candidate gate model have been exercised end to end, including deliberately adversarial/stale/ambiguous states and recovery.

The qualification is stronger than the earlier static T060/T053/T063 mapping because it created and closed an actual repository transaction and retained exact run/commit/PR evidence.

### Not yet qualified by this test

GitHub Actions is a real Git environment, but it is **not the actual Codex Desktop/local persistent host** used by the Agent Governance Executor.

Therefore this qualification does not yet prove host-specific behavioral claims such as:

- whether Codex interprets the compact gate contract without reverting to command-level micromanagement;
- whether Codex naturally avoids rerunning the entire G0 sequence after every local command;
- whether Codex correctly recognizes recovery/worktree-switch events as G0 revalidation triggers;
- whether its actual host/session/worktree lifecycle exposes any adapter-specific state that the generic gates fail to capture.

A bounded real-Codex pilot would provide the final host-specific confidence layer if the Human wants maximum evidence before normative adoption.

## 11. Current R027 disposition

```text
static architecture evaluation             PASS
prospective wording/compression             PASS
deterministic Git/GitHub end-to-end         PASS
negative stale/dirty/race/cleanup cases     PASS
runtime artifact refinement                 REQUIRED IN FINAL DESIGN
unique-commit cleanup refinement            REQUIRED IN FINAL DESIGN
new durable Git receipt                     NOT JUSTIFIED
command-level Git governance                NOT JUSTIFIED
actual Codex-host behavioral pilot          NOT YET RUN
normative adoption                          NONE
Decision-State                              EVALUATING
```

The next R027 action is not implementation. If host-specific confidence is required, run one bounded real-Codex pilot against a disposable work unit using the compact gate wording and compare its observed behavior to this deterministic baseline.
