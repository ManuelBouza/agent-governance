# Research and Evidence Appendix

Status: EVIDENCE ONLY  
Source repository: `ManuelBouza/agent-governance`  
Extraction baseline: `0e2edbca2cb0e620db7cdb7b93945bef8985fdfd`

Nothing in this appendix is normative merely because it is reproduced here. The portable operating model is derived from accepted source authority; research and experiments explain why those controls are defensible and what was actually qualified.

## Evidence discipline

The source research lifecycle separates:

```text
research finding
!= accepted decision
```

A research item may be complete while its recommendation is deferred, rejected, superseded, or not decision-requiring. Experiments and vendor documentation support decisions but do not silently create policy.

This distinction itself is a portable control: the target should preserve evidence-to-decision provenance and revalidate volatile external facts before relying on them.

## SDD and authority evidence

Source provenance:

- `docs/SPEC-DRIVEN-DEVELOPMENT-RESEARCH.md`
- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/decisions/D041-executor-process-autonomy.md`

Material conclusion adopted by source authority:

- tool-neutral spec-anchored, delta-first SDD is compatible with brownfield maintenance;
- one accountable owner per lifecycle stage avoids semantic authority collisions;
- Executor private planning/SDD/subagent mechanisms can remain implementation aids without becoming governing authority;
- conformance/oracle authorship can follow semantic authority while technical execution/review remains independent.

The target should adopt these semantics only if they fit its own governance topology.

## Coordinator/worktree evidence — R011

Source:

`docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md`

Source blob at extraction baseline:

`f461063f6df54e98d68ff0b09156fd199fe2c361`

Qualified/adopted observations:

- deterministic Human-visible coordinator naming improves navigation but is not authority;
- one concurrently writable work unit per exclusive worktree/topic branch is the safety invariant;
- stale/ambiguous local work must be preserved rather than destructively normalized;
- post-integration workspace retirement should leave a clean current primary baseline when safe.

Vendor-specific session naming syntax/version facts are volatile and adapter-only.

## Coordinator delegation evidence — R012

Source:

`docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md`

Source blob:

`826d2e1909e1f0d5189c6e9580648b7349f8e343`

Material evidence:

- a policy that merely permits delegation may under-delegate on executor hosts/modes that require explicit steering;
- a rigid universal worker graph over-couples governance to vendor orchestration mechanics;
- T053 showed that explicit coordinator/child topology can operate within Agent Governance boundaries;
- the resulting source decision adopted semantic delegation triggers while retaining Executor-owned concrete orchestration.

The research artifact's historical metadata may predate its later final disposition; the canonical research registry and accepted decision control the current source disposition.

## Coordinator continuity evidence — R006 / R013

Sources:

- historical persistent-root research (`R006`);
- `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` (`R013`);
- T053 pilot/review evidence.

R013 source blob:

`4fce86fc23740b89335281d7d4d633c1282fd456`

Material conclusion:

- same-task coordinator continuity is useful;
- cross-task persistent coordinator scope is too broad and was superseded;
- the adopted boundary is one complete Task/Operational Contract per Human-visible coordinator root;
- fresh technical reasoning is obtained with bounded children where supported;
- Git freshness remains mandatory on every continuation.

No quantitative token/cost saving claim is carried into the portable model.

## Local Git / Library / GitHub transport evidence — R014

Source:

`docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md`

Source blob:

`ecb745998e1579620b841a330a9e40f12e1ad193`

Empirically qualified in the tested ChatGPT/GitHub/Library environment:

- real local Git status/diff/staging/commit semantics in a temporary workspace;
- explicit connected GitHub read/write transport;
- GitHub -> Library -> edit -> GitHub round trip;
- multiple persistent Library versions before one remote update;
- packaged full repository snapshot including real `.git` persisted/restored;
- cross-chat snapshot recovery and continued local Git history;
- multi-file remote reconstruction in one GitHub commit;
- stale remote write rejection using exact prior state (`HTTP 409`);
- local and connector-created commit SHAs may differ even when trees are equivalent;
- exact Git tree equality can verify represented content;
- merged feature snapshot retirement only after target refresh/promotion/revalidation;
- closed-unmerged snapshot retention;
- corrupt candidate preservation of previous validated current snapshot.

Not qualified as universal facts:

- direct Git CLI network transport;
- Library as a native Git remote or mounted working tree;
- automatic merge/reconciliation;
- exact arbitrary commit-object preservation;
- automatic quota-pressure GC selection;
- large repository snapshot practicality near vendor limits.

Vendor Library quotas/retention and connector capabilities are explicitly volatile.

## Cross-chat isolation / lock evidence — R015

Primary source:

`docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md`

Source blob:

`c45a60cee065a4022504b1a1dbb6b98329f24b7d`

Supporting lifecycle appendix:

`docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-LOCK-LIFECYCLE-APPENDIX.md`

Source blob:

`7c38313b88c2bcf985d03fccbc77c454f1fb09ba`

Supporting real race appendix:

`docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-CROSS-CHAT-RACE-APPENDIX.md`

Source blob:

`9879b918d47cb0dd795cb5d3ef98fdbf6f328593`

Evidence progression:

1. independent topic branches isolated two logical writable chats;
2. linked native worktree directories were shown not to be self-contained portable snapshots;
3. standalone `.git` snapshots restored cleanly and matched remote trees;
4. wrong-owner snapshot use was blocked before mutation;
5. an initial ref-existence lock proved collision behavior but was not the final reusable lifecycle;
6. a persistent coordination-only lock branch plus sentinel qualified acquisition, exact-blob release and reacquisition;
7. a real two-chat race started from the same free lock-branch HEAD;
8. exactly one contender advanced the branch; the stale contender received HTTP `409` and created no competing commit;
9. the resulting qualified source model is expected-head CAS + sentinel on a coordination-only branch.

The earlier ref-only lock model is historical evidence, not the current preferred semantic model.

Still unqualified: automatic orphan recovery, TTL/heartbeat, ownership transfer, closed-unmerged resume, generalized ref retirement and quota-pressure GC.

## Branch-write incident evidence

Source authority:

`docs/decisions/D061-orchestrator-branch-target-write-guard.md`

Historical source incidents recorded there:

- `2a2f34baa5e90724c46555c876aabe68309a8b99`
- `59c44d88e202c24928fd4908470bd91099703023`
- `7a116b92c706801c9259ce152096609adb465563`

The incidents demonstrated that a process-only "do not write develop" rule was insufficient when the mutation surface could target the long-lived branch directly. This supports the two-layer control:

```text
process-side explicit topic target guard
+
provider-side long-lived branch protection
```

The incidents remain history and are not rewritten away.

## Source repository protection evidence

At extraction time, the source repository exposed active ruleset:

`Protect long-lived branches`

covering:

- `refs/heads/main`
- `refs/heads/develop`

with:

- pull-request transport;
- deletion protection;
- non-fast-forward protection;
- no bypass actors;
- current user cannot bypass.

This is evidence for the source repository only. The target must inspect its own provider state.

## Deferred/negative evidence that constrains transfer

### Adaptive child compute routing — R007

Source registry disposition: `COMPLETE / DEFERRED`.

A target must not infer a source-wide model/effort routing policy for workers. Concrete worker compute is an adapter/target decision.

### Model launch-profile migration — R010

Source registry disposition: `COMPLETE / DEFERRED`.

Vendor model names and launch-profile mappings are not portable correctness dependencies.

### Child observability/sandbox research — R008/R009

These support bounded, version-sensitive measurement claims. They do not justify assuming exact child permission provenance on a different provider/version.

## Frozen T058 evidence

T058 is retained only to prove what is **not** accepted.

```text
branch: feat/t058-chatgpt-portable-workspace-adapter
remote head: 6ed319a1802cfd90d50d9dc95d969435c295a164
implementation/review anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
state: BLOCKED / FROZEN_BY_HUMAN
```

Its implementation/tests are not production authority and are classified `DO_NOT_COPY`.

## Evidence use in a target

A target adoption may cite this appendix as provenance, but it must:

1. inspect target-native reality;
2. revalidate volatile provider/host facts;
3. decide explicitly which semantics to adopt;
4. record target-native receipts/decisions;
5. keep unresolved gaps unresolved unless separately qualified.
