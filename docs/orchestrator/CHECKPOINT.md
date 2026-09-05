# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O217  
Canonical-Branch: `develop`  
Current-Work-Unit: D066 / T058 — materialize the R014/R015-qualified ChatGPT local-Git + Library portable workspace transport  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: launch T058 only after this planning/decision change is integrated into `develop`

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056, D057, D058, D059, D060, D061, D062, D063, D064 and D065 remain controlling.
- Core protocol remains `1.15.0`.
- GitHub hard guard ruleset `22339910` remains active for `main` + `develop`; normal agentic writers have no routine bypass.
- T057/OP069 and OP070 are closed; their Human-visible roots are retired and MUST NOT be reused.
- R007 remains `COMPLETE / DEFERRED`; no adaptive child compute-routing policy is adopted.
- R010 remains `COMPLETE / DEFERRED`; no global GPT-6 Astra root migration is adopted.
- PR `#291` integrated the completed R014/R015 research only, without policy adoption, at `develop@538e88b44370d3d0003c66c9d616f9c0e41d8453`.
- The five R014/R015 research/appendix artifacts remain historical evidence and MUST NOT be rewritten to match later policy.
- This planning change adopts only the empirically qualified subset through D066 and explicitly preserves the unresolved gaps.

## R014 / R015 disposition in this change

Canonical research transitions after this change is integrated:

```text
R014 — ChatGPT Git workspace / Library / GitHub transport
  Research-State: COMPLETE
  Decision-State: DECIDED
  Decision-Ref: docs/decisions/D066-chatgpt-portable-git-workspace-transport.md

R015 — ChatGPT Library worktree simulator
  Research-State: COMPLETE
  Decision-State: DECIDED
  Decision-Ref: docs/decisions/D066-chatgpt-portable-git-workspace-transport.md
```

D066 adopts:

```text
GitHub
  = canonical repository / branch / PR authority

local temporary Git
  = iterative authoring/diff/commit surface

ChatGPT Library
  = optional persistent validated standalone .git snapshots

coordination-only GitHub lock branch
  + expected-HEAD CAS
  + owner sentinel
  = portable cross-chat writable ownership authority
```

The intended transport optimization is:

```text
verified topic branch
-> many local edits / local Git operations
-> optional Library snapshots for cross-chat durability
-> one bounded/final freshness-gated GitHub publication
-> PR / review / integration
```

D061 is preserved: no normal direct write to `main`/`develop` is authorized.

## Qualified fail-closed boundaries adopted by D066

Portable acquisition:

```text
same observed free lock HEAD H
A advances H -> H1
B expects H but observes H1
=> B BLOCKED_STALE_LOCK_HEAD
=> no automatic retry into ownership
```

Portable resume requires validated snapshot + exact receipt/owner/work-unit/topic + active matching sentinel + remote topic freshness/tree compatibility before `WRITE_ALLOWED`.

Post-merge feature snapshot GC requires positive merge/integration evidence plus a refreshed target snapshot that is round-trip validated, promoted, and revalidated before destructive feature-snapshot cleanup.

`closed && !merged`, missing/ambiguous integration, corrupt candidate, or ownership ambiguity remains retained/blocked fail-closed.

Lock release requires exact current sentinel ownership plus exact current sentinel blob SHA, followed by verification that the sentinel is absent.

## Explicit unresolved gaps

D066/T058 MUST NOT silently solve or claim solved:

- crash/orphan recovery after acquisition;
- TTL/heartbeat;
- abandoned-lock reclamation;
- closed-unmerged cross-chat resume;
- ownership transfer;
- automatic lock/topic branch-ref retirement;
- automatic quota-pressure GC selection;
- unusual-ref canonicalization/scale;
- unqualified ruleset interaction outside the verified envelope.

## T058

Task Contract:

`docs/tasks/T058-chatgpt-portable-workspace-adapter.md`

Expected implementation branch:

`feat/t058-chatgpt-portable-workspace-adapter`

Expected handoff:

`handoffs/T058-executor-handoff.json`

SDD profile: `ASSURED`  
Test authorship: `executor-implementation`

T058 implements a deterministic local helper/CLI only. The helper validates/classifies snapshots, lock observations, writable-entry gates, release, GC and publication manifests. It MUST NOT itself call GitHub or ChatGPT Library APIs or perform network mutation.

Required fail-closed test classes include:

- ownership mismatch;
- stale lock HEAD with no retry transition;
- wrong worktree/snapshot;
- corrupt/unsafe snapshot;
- exact-identity release;
- post-merge GC eligibility;
- closed-unmerged retention;
- standalone `.git` snapshot round trip;
- batched publication manifest.

## D065 posture for T058

T058 is ASSURED and has material delegation triggers: independent fail-closed verification, noisy/full-suite test execution, bounded archive/Git edge-case inspection and root-context protection.

The Human-visible root must delegate at least one eligible bounded slice unless a concrete safety/capability anti-trigger dominates at runtime. The Executor chooses the concrete child count, role, decomposition and sequencing.

## Repository/branch state

Planning branch:

`docs/d066-chatgpt-portable-workspace-adapter`

Planning base verified before mutation:

`develop@538e88b44370d3d0003c66c9d616f9c0e41d8453`

D061 sequence applied:

```text
refresh develop
-> create topic branch from exact SHA
-> verify exact branch/base
-> mutate only branch=docs/d066-chatgpt-portable-workspace-adapter
-> review complete diff
-> PR to protected develop
```

Known non-colliding historical/administrative branch residue may still include the PR #291 research branch and the O216 checkpoint branch. Do not broaden T058 implementation into their cleanup.

## Next action

1. Review the complete D066/runbook/T058/registry/O217 planning diff against `develop@538e88b44370d3d0003c66c9d616f9c0e41d8453`.
2. Open the planning PR to protected `develop`.
3. Because the Human Owner explicitly authorized immediate execution/integration of this research materialization, integrate the reviewed planning PR by normal protected PR flow without a separate confirmation.
4. Refresh canonical `develop` and read the integrated T058 contract.
5. Launch T058 as one NEW Human-visible Coordinator Root in an exclusive D058 writable worktree.
6. Executor returns only `STATUS/HANDOFF/BRANCH/HEAD` after pushed evidence.
7. Orchestrator converges T058 from GitHub; do not accept chat-only implementation evidence.
8. If accepted, integrate the implementation through protected PR flow under the same explicit Human authorization.
9. Perform current-spec/checkpoint evolution and evidence-safe closure after implementation acceptance/integration.
10. Do not launch R007 or MG1-v13 concurrently.

## T058 launch profile after planning integration

```text
Executor: Codex
Session: NEW
Coordinator-Chat: AG | agent-governance | T058 | root-1
Model: GPT-5.6 Sol
Effort: Medium
```

Rationale: fail-closed Git/archive/concurrency validation is moderately complex and safety-sensitive; Sol/Medium is sufficient, while D065 delegates eligible bounded verification/testing slices instead of inflating root compute.

`AGENTS.md` is intentionally unchanged by this planning change, so no D043 reload is required solely because of D066/T058 authoring.

## Next chat minimum load

Load only:

1. current `develop` identity;
2. current `AGENTS.md`;
3. this checkpoint.

Then follow the exact current T058 state. Load D066/T058/R014/R015 only as needed for T058 launch/convergence or a concrete conflict.

## Do not

Do not reinterpret Library as a Git remote or canonical authority. Do not weaken D061/D062. Do not retry a stale lock CAS automatically into ownership. Do not garbage-collect closed-unmerged or ambiguous work. Do not invent orphan recovery/TTL/ownership transfer/quota selection. Do not let the Executor author Markdown. Do not reuse retired T057/OP070 roots.