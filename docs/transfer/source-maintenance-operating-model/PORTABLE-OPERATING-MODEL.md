# Portable Source-Maintenance Operating Model

Status: EXTRACTED / NON-AUTHORITATIVE UNTIL ADOPTED BY TARGET

This document states the semantic operating model without source Decision IDs, source branch names, source paths, vendor model names, or source-only implementation details. A target repository may adopt these semantics only through its own authority.

## 1. Canonical authority and bootstrap

1. The repository provider's canonical remote state is authoritative for persisted source state.
2. A new orchestration chat/session begins by reading the current canonical integration baseline, repository-local governing instructions, and the current durable frontier/checkpoint.
3. Persisted Git state outranks remembered chat/session state.
4. A successor must verify every material expected identity before mutation: canonical branch/head, checkpoint/frontier sequence or identity, active work-unit state, and any retained portable-workspace ownership state.
5. A material mismatch is fail-closed. The successor reports expected versus observed state and does not repair, overwrite, reinterpret or continue the material objective.
6. Closure or bootstrap repair belongs to the predecessor/owning governance context and is bounded to durable handoff/frontier repair, not new objective work.

## 2. One objective per Orchestrator chat

A Human-visible Orchestrator chat owns one explicit, verifiable objective.

```text
ACTIVE
-> objective completed and durably represented
-> OBJECTIVE_COMPLETE
-> WAITING_FOR_NEXT_OBJECTIVE
-> successor bootstrap prepared
-> SUCCESSOR_VERIFIED
-> predecessor RETIRED
```

The predecessor must not execute the next material objective after its own objective closes. The next chat cold-starts from canonical repository state rather than private conversation history.

Closure requires, as applicable:

- accepted changes integrated;
- task/handoff state durable;
- canonical repository identity known;
- retained portable workspace synchronized and validated if used;
- ownership locks/workspaces cleaned or explicitly retained;
- checkpoint/frontier updated with the next permitted action.

## 3. Exclusive SDD/role ownership

Every governed development unit uses single-owner lifecycle stages.

```text
Orchestrator:
  Explore / Frame
  Specify
  Design
  Plan & Trace

Candidate materialization:
  Orchestrator may materialize the coherent source candidate
  when the adopted target adapter assigns that source-maintenance role.

Executor:
  Execute
  Diagnose
  bounded technical Repair
  Verify / technical review

Orchestrator:
  Converge
  Accept
  Integrate
  Evolve durable specification/frontier
```

No stage has dual semantic authority.

The Orchestrator owns requirements, controlling architecture/design, acceptance meaning, plan/trace boundaries and final semantic convergence. The Executor owns execution mechanics and technical implementation/review inside the approved boundary.

Executor discovery of an upstream requirement/design/acceptance defect causes re-entry to the earliest affected Orchestrator stage. It is not authority for silent redesign.

For target repositories that retain a different candidate-authoring owner, that mapping is an adaptation decision. The invariant to preserve is that technical execution/repair cannot silently acquire upstream semantic authority.

## 4. Delta-first specification and traceability

For brownfield work, specification grows through real changes rather than mandatory full historical backfill.

Material behavior changes classify affected requirements as:

- `ADDED`
- `MODIFIED`
- `REMOVED`
- `PRESERVED`

The target should reuse an adequate existing specification carrier instead of creating duplicate current truth.

Material work must be traceable in both directions:

```text
intent
-> requirement/spec delta
-> controlling design
-> plan/work contract
-> represented candidate
-> technical verification evidence
-> semantic convergence/acceptance
-> integrated current state
```

Tests/evals are evidence and executable projections of acceptance; they do not become independent normative authority.

## 5. Test/oracle ownership follows semantic authority

When an acceptance/conformance oracle encodes semantics owned by the Orchestrator/Human strategy layer, that authority may own the oracle. The Executor still runs it, diagnoses technical failures, and may add implementation/exploratory tests.

The Executor may repair mechanical harness defects only within explicit authority. Changing expected outcomes, thresholds, classifications, security expectations or other acceptance meaning is an upstream semantic change and requires Orchestrator re-entry.

Ordinary application unit/integration/regression testing may remain Executor-owned when it does not encode a separate semantic oracle.

## 6. Executor process autonomy and operation resolution

Governance controls the requested outcome, authority boundary, risk/effect envelope and required evidence. The Executor controls compatible technical mechanics inside that envelope.

```text
Governance owns WHAT + bounds + acceptance.
Executor owns HOW + execution mechanics.
```

For executable operations:

1. resolve the semantic operation and actual target/effect context;
2. reuse the applicable semantic runbook when required;
3. reuse a compatible verified adapter recipe when available;
4. otherwise resolve syntax from authoritative/version-compatible documentation rather than guessing;
5. preflight/preview when meaningful;
6. re-evaluate authorization against the actual bound invocation;
7. execute with least privilege and bounded credentials/network;
8. verify semantic postconditions;
9. promote reusable technical recipes only after verification.

A runbook defines procedure semantics. Commands, shells, CLIs, APIs, SDKs and remote transports are adapters, not authority.

## 7. Effect- and target-oriented execution authorization

Execution authority is evaluated by target, effect, privilege, credentials, network/resource scope, reversibility and evidence—not command name alone.

A portable approval model distinguishes:

- task-authorized bounded effects;
- explicitly authorized bounded effects;
- Human-gated material effects;
- denied/unknown/mismatched effects.

Possession of a shell, token, key, credential, elevated session or network path is mechanism, not authorization.

Nested processes and remote commands inherit a subset of the parent authority; they never expand it.

## 8. Topic-branch write guard

Normal automated source mutation must fail closed on branch target.

```text
refresh canonical integration branch
-> create short-lived topic branch from exact intended base
-> verify exact topic branch exists at that base
-> perform every mutation against that exact branch
-> review complete delta
-> merge through protected PR/MR flow
```

Missing, ambiguous, invalid or stale topic identity is a stop condition. A failed topic write must never be retried against a long-lived/default branch merely for convenience.

After mutation, verify the topic branch contains the intended state and the long-lived base did not move because of the authoring action.

## 9. Server-side long-lived branch protection

When the repository provider supports enforceable protection, writable readiness requires server-side controls on every relevant long-lived branch.

Minimum semantic protection:

- normal changes reach the branch through PR/MR transport;
- branch deletion is restricted;
- force/non-fast-forward updates are blocked;
- routine agent/app write identity has no bypass;
- enforcement is active.

Bootstrap must inspect existing native controls first:

```text
stronger compatible -> REUSE
compatible bounded change -> ADAPT
missing -> establish minimum control
conflicting/bypass-heavy -> CONFLICT / Human resolution
provider lacks equivalent -> explicit alternative-control/risk disposition
```

Do not weaken stronger compatible target controls to match a source example. Prefer effective provider/API state over screenshots when a supported read surface exists.

## 10. Executor coordinator continuity

One complete governed Task/Operational Contract maps to one Human-visible Executor coordinator root.

```text
new work unit -> NEW root
same work unit -> CONTINUE same root
task closes -> retire root for governance purposes
new work unit -> NEW root
```

A second Human-visible root for the same task is exceptional failover only when the original root cannot safely continue. Independent technical reasoning should normally use bounded child contexts rather than another peer coordinator.

A coordinator/session name is navigation metadata, never authority. Stable host IDs are corroborating evidence only when supported.

Every same-task continuation still revalidates canonical remote freshness and newly controlling persisted authority.

## 11. Coordinator-first delegation

For non-trivial execution, the Human-visible Executor root acts as coordinator and evaluates delegation before substantial execution and final verification.

Material delegation triggers include:

- independent read-heavy exploration;
- noisy tests/logs/traces;
- fresh independent verification;
- parallelizable non-overlapping slices;
- specialized capability;
- root-context protection.

Material anti-triggers include:

- small/straightforward work;
- tightly serial work;
- duplicated orientation cost;
- coordination cost greater than benefit;
- overlapping mutable ownership;
- contract-fixed topology;
- unavailable/unsafe worker permission or isolation surface.

When a material trigger applies and no anti-trigger dominates, delegate the eligible bounded slice. The coordinator retains contract, branch/workspace identity, synthesis, final represented state and handoff accountability.

Exact worker graph, count, vendor role names, model and spawn/wait mechanics remain Executor-adapter choices unless topology itself is an explicit acceptance/safety/experiment variable.

## 12. Workspace isolation

Every concurrently writable work unit has an exclusive writable workspace and topic branch.

```text
one writable work unit
-> one topic branch
-> one exclusive writable workspace
```

Two writable coordinators must not share a mutable checkout or topic branch.

Before writable use, classify local topology sufficiently to avoid collision. Unknown, unique or unrepresented work is preserved and blocks destructive cleanup.

After integration, retire obsolete task workspaces/branches only with positive evidence that no unrepresented work remains. The designated primary checkout should converge to a clean current long-lived baseline without destructive reset of unknown work.

## 13. Local Git / persistent snapshot adapter

When supported, separate four planes:

```text
canonical Git provider
local executable Git workspace
optional persistent snapshot store
coordination-only remote lock authority
```

The persistent store is not the Git remote, canonical authority or concurrency mutex.

Two modes are valid:

### Ephemeral local mode

Use one temporary standalone Git repository for one work unit when cross-chat persistence is unnecessary. Publish bounded/final checkpoints to the canonical topic branch.

### Portable cross-chat mode

Use when writable state must survive chat/runtime turnover or several chats may own concurrent work units.

Required mapping:

```text
one work unit
-> one unique topic branch
-> one coordination-only lock namespace/branch
-> expected lock-head optimistic CAS freshness
-> one owner sentinel
-> one unique standalone repository snapshot including real .git
-> one ownership/freshness receipt
```

A linked native `git worktree` directory is not independently portable when its `.git` entry points to metadata outside the archived directory.

## 14. Cross-chat lock / CAS / sentinel

A portable lock uses:

```text
coordination-only lock branch
+ expected-HEAD compare-and-swap freshness
+ owner sentinel
```

Acquisition:

1. read lock branch and record expected head `H`;
2. require sentinel absent;
3. attempt sentinel creation against observed `H`;
4. success -> re-read sentinel and verify repository/owner/work-unit/topic -> acquired;
5. stale expected head / conflict -> `BLOCKED_STALE_LOCK_HEAD`;
6. existing sentinel -> `BLOCKED_OWNER_EXISTS`;
7. missing/corrupt/ambiguous metadata -> `BLOCKED_AMBIGUOUS_LOCK`.

A stale CAS failure is not permission to retry until winning. Re-read and reclassify.

The lock branch contains coordination state only; unrelated commits can invalidate acquisition freshness.

Release requires exact current ownership plus the exact current sentinel object/blob identity, then deletion and read-back proving absence. Failure or mismatch leaves the lock occupied/ambiguous.

## 15. Portable snapshot validation and resume

A portable snapshot must be self-contained and include actual repository Git state.

Before promotion or writable resume validate, as applicable:

- archive/checksum integrity;
- safe extraction without traversal/link hazards;
- repository/owner/work-unit/topic receipt;
- `git fsck --full` or equivalent repository integrity;
- clean pre-mutation working state;
- local head/tree;
- expected topic branch;
- remote topic-head freshness;
- exact tree equivalence when local and connector-created commit IDs intentionally differ.

Commit SHA equality is not required when the transport reconstructs an equivalent commit and the receipt records the canonical remote head; exact represented tree equality may be the content invariant.

Any mismatch is write-blocking. Do not reset, clean, overwrite, change owner or delete state to force the gate to pass.

## 16. Bounded publication and freshness

Before publishing local candidate state:

1. re-read the canonical remote topic branch;
2. require exact expected remote freshness;
3. derive the complete changed-file/tree set;
4. publish a bounded multi-file/final checkpoint when the transport supports it;
5. verify resulting remote head/tree and changed-file set;
6. only then refresh persistent snapshots/receipts.

Unexpected remote movement is fail-closed; no silent overwrite or automatic merge.

Before the Executor runs, the coherent candidate plus controlling Task/Operational Contract must be represented on the canonical topic branch. Chat-only or persistent-store-only authority is not executable authority.

## 17. Executor Execute / Diagnose / Repair / Verify boundary

The Executor may repair technical defects discovered during execution when the repair stays inside approved semantics/design/plan.

Typical in-authority repair classes:

- implementation/runtime/type/build defects;
- lint/format/static-analysis defects;
- test defects that do not redefine semantic acceptance;
- technical configuration/environment wiring inside scope;
- deterministic compatibility defects inside approved architecture;
- mechanical conformance-harness defects when explicitly authorized.

Out-of-authority classes include:

- requirement/public-behavior changes;
- architecture/design changes;
- acceptance/oracle meaning changes;
- new dependency or material risk not already authorized;
- scope expansion;
- ambiguous conflict requiring product/strategy choice.

Out-of-authority findings cause `BLOCKED`/`PARTIAL` plus durable evidence and Orchestrator re-entry.

Executor `DONE` is technical evidence, not semantic acceptance.

## 18. Re-synchronization after Executor correction

When a persistent Library/snapshot candidate was retained and the Executor corrected the canonical topic branch:

```text
Executor final GitHub state
-> Orchestrator materializes exact corrected state
-> rebuild replacement portable snapshot
-> checksum/archive/repository validation
-> verify expected canonical remote head/tree
-> promote replacement current
-> re-materialize/revalidate promoted current
-> only then retire superseded snapshot
```

A stale pre-repair snapshot must never be treated as the accepted candidate.

## 19. Snapshot lifecycle and fail-closed cleanup

Destructive snapshot cleanup requires positive evidence.

A merged feature/work-unit snapshot becomes retirement-eligible only after:

- merge/integration is positively proven;
- exact integrated state is represented/verified;
- target canonical snapshot is refreshed;
- target candidate round-trip validation succeeds;
- target current is promoted and revalidated.

Fail-closed retention:

```text
closed but not merged -> RETAIN
remote branch missing but integration unproven -> RETAIN
ambiguous remote/persistent state -> RETAIN
replacement validation failure -> RETAIN previous current
```

Quota pressure is not itself deletion authority.

## 20. Research/evidence separation

Research, vendor documentation and experiments are evidence, not policy.

A target must maintain an explicit evidence-to-decision disposition so that:

- `COMPLETE` research does not imply adoption;
- experiments/pilots do not silently become authority;
- deferred/rejected/superseded findings remain visible;
- volatile vendor facts are revalidated before reliance;
- target decisions explicitly name the evidence they adopt.

## 21. Target coexistence rule

The target must inspect existing governance before installing anything and classify each overlapping capability as exactly one of:

`REUSE | ADAPT | COEXIST | MISSING | CONFLICT`

Preserve stronger compatible native controls. Do not create duplicate current-truth artifacts or competing authority merely to mirror Agent Governance naming.

Target-native authority must be sufficient for later operation without consulting the source repository.
