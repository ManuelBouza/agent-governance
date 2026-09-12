# R026 — ChatGPT/GitHub interaction minimization

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT Orchestrator repository-read, authoring, publication, review-status, persistence and cross-chat transport surfaces for reducing logical GitHub interactions while preserving GitHub canonical authority, D061 freshness, branch protection and D066 workspace semantics  
Question: How can Agent Governance minimize routine ChatGPT interactions with GitHub without weakening canonical Git authority, freshness, branch isolation, conflict detection, review traceability or the Human/Orchestrator/Executor ownership model?  
Evaluation-Refs: desk research 2026-09-12; empirical qualification pending on a disposable repository such as `ManuelBouza/test_biblioteca` before normative adoption  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive synthesis

R014/R015 and D066 already reduce **write amplification** by allowing local Git authoring plus bounded publication to GitHub. R026 extends that analysis to the full interaction budget: reads, bootstrap, publication, PR observation and cross-chat resume.

The strongest target architecture is:

```text
GitHub
  = canonical remote authority and synchronization boundary

persistent local repository / exact local snapshot
  = normal read, search, diff and authoring surface

GitHub Git Data publication
  = bounded multi-file publication surface when direct Git transport is unavailable

GitHub PR event task / webhook
  = event-driven observation instead of polling

ChatGPT Library
  = optional durability/backup snapshot plane, not the hot read path
```

The optimization principle is:

```text
synchronize once
-> read and author locally many times
-> publish once/bounded
-> observe by event
-> verify once at convergence
```

The goal is not to remove GitHub from the workflow. GitHub remains canonical. The goal is to stop using GitHub as the per-file working filesystem.

R026 recommends a future qualification pilot before changing D066 or startup policy. The key unqualified point is whether ChatGPT Work Desktop can perform the required local Git synchronization/authoring mechanics without Human terminal mediation. OpenAI documents local-folder access for Work and explicit repository/terminal access for Codex, but does not in the reviewed Work documentation explicitly guarantee the exact Git command surface required by this Orchestrator design.

## Baseline from R014/R015/D066

D066 already adopts this optimization direction:

```text
bootstrap/verify topic branch
-> many local edits and Git operations
-> optional Library persistence
-> batched/final GitHub publication
-> PR/review/integration
```

It therefore already rejects one GitHub content write per edit as the desired workflow.

R026 does not supersede D066. It asks whether current ChatGPT product surfaces can make the same pattern substantially cheaper on the **read side** and on **post-publication observation**.

Important existing constraints remain unchanged:

- GitHub is canonical repository and branch authority;
- normal writes use a short-lived topic branch from exact intended `develop`;
- no direct development writes to `develop` or `main`;
- stale or ambiguous remote movement is fail-closed;
- Library is not a Git remote or canonical authority;
- T058 remains frozen by Human decision and is not resumed by this research.

## Evidence reviewed

### OpenAI official documentation

1. **Connecting GitHub to ChatGPT**  
   https://help.openai.com/en/articles/11145903  
   Reviewed 2026-09-12.

   Material findings:

   - GitHub repository content is retrieved on demand;
   - the generic GitHub connection does not create a synchronized repository index;
   - ChatGPT may issue multiple repository searches as needed;
   - eligible Work users can create event-triggered tasks from GitHub pull-request activity, including PR open/close/readiness and, depending on trigger, reviews/comments, commit updates and completed merges;
   - the public article describes the generic GitHub app as read-oriented and routes direct code submission to Codex.

2. **ChatGPT Work and Codex**  
   https://help.openai.com/en/articles/20001275  
   Reviewed 2026-09-12.

   Material findings:

   - Work Desktop can open a local folder/project and use local files with permission;
   - local Work chats run on the user's computer;
   - Codex explicitly supports local folders, repositories, terminals and developer tools;
   - Work and Codex remain distinct product surfaces.

3. **File storage and Library in ChatGPT**  
   https://help.openai.com/en/articles/20001052  
   Reviewed 2026-09-12.

   Material findings:

   - uploaded/generated files can persist in Library across chats;
   - Library is a persistent file store rather than a Git remote;
   - the public user documentation describes selecting/reusing Library files, but does not by itself establish a current agentic API for automated repository-snapshot materialization in every ChatGPT surface.

### GitHub and Git official documentation

4. **GitHub REST API — Git trees**  
   https://docs.github.com/en/rest/git/trees  
   Reviewed 2026-09-12.

   Material findings:

   - one `create tree` request can contain multiple path entries;
   - an entry may provide `content` directly, causing GitHub to create the blob for that path;
   - `base_tree` allows changes to be applied over an existing tree;
   - after tree creation, publication is completed by creating a commit and updating a reference;
   - recursive tree reads can return a repository tree inventory in one response up to documented limits.

5. **GitHub REST API — repository archive download**  
   https://docs.github.com/en/rest/repos/contents#download-a-repository-archive-tar  
   Reviewed 2026-09-12.

   Material finding: GitHub exposes a tar archive for an exact ref, enabling whole-snapshot materialization without one content request per file when the active ChatGPT transport can consume the binary download.

6. **Git — git-fetch**  
   https://git-scm.com/docs/git-fetch  
   Reviewed 2026-09-12.

   Material finding: `git fetch` updates refs and downloads the objects needed to complete the requested histories, making a persistent clone an incremental cache rather than a repeated full repository download.

### Specialized engineering evidence

7. **GitHub Engineering — Git clone: a data-driven study on cloning behaviors**  
   https://github.blog/open-source/git/git-clone-a-data-driven-study-on-cloning-behaviors/  
   Reviewed 2026-09-12.

   Material finding: for a developer focused on one reasonably sized repository, GitHub's study recommends a full clone followed by normal full fetches; shallow and some partial-clone patterns can make later fetch behavior worse or trigger additional object retrieval.

8. **GitHub Engineering — Get up to speed with partial clone and shallow clone**  
   https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/  
   Reviewed 2026-09-12.

   Material finding: blobless partial clones can reduce initial transfer for very large repositories, but missing blob access creates later on-demand downloads. For a repeatedly accessed repository, a normal full clone remains the simpler cache unless repository size justifies the tradeoff.

9. **GitLab — Avoid the massive end-to-end tax of default full history clones**  
   https://about.gitlab.com/blog/git-clone-override-policy/  
   Published 2026-08-18; reviewed 2026-09-12.

   Material finding: clone strategy should be selected based on repository size/lifecycle because unnecessary history transfer has client, network and server cost. This supports measuring actual Agent Governance repository characteristics instead of adopting shallow/partial clone mechanically.

## Current ChatGPT runtime capability observation

The active ChatGPT environment used for this research exposes a connected GitHub plugin with functions including, among others:

```text
read:
  fetch / fetch_file
  fetch_commit
  compare_commits
  fetch_pr / fetch_pr_patch
  fetch_blob

write:
  create_branch
  create_tree
  create_commit
  update_ref
  create_file / update_file / delete_file
  create_pull_request
  review / merge related actions
```

This runtime-specific write surface is broader than the generic public OpenAI GitHub-app article, which currently describes the standard GitHub connection as read-oriented. Therefore:

```text
public generic GitHub app documentation
!= guaranteed schema of every installed ChatGPT GitHub plugin/runtime
```

Any adopted transport must qualify the **actual active tool schema**, not infer write capability from generic product documentation.

The currently exposed `create_tree` wrapper accepts generic tree elements, while GitHub's official endpoint supports `content` inline. This combination is a promising N-file batching primitive, but the wrapper's exact accepted element shape must be empirically exercised before D066 is changed to require it.

## Problem decomposition

The current interaction cost has four independent components.

### 1. Bootstrap read amplification

A cold chat normally needs at least:

```text
read develop HEAD
read AGENTS.md at that HEAD
read CHECKPOINT.md at that HEAD
```

Additional task/spec/research files then add more GitHub calls.

The semantic requirement is to consume the exact current `develop` snapshot, not to fetch each file through a separate remote API invocation.

### 2. Working-set read amplification

GitHub connected access is on-demand and not a synchronized index. Searching and reading a repository directly through the connector can therefore generate one or more remote calls for each exploration step.

This is appropriate for occasional repository questions, but inefficient for a repository that acts as the Orchestrator's continuously consulted source tree.

### 3. Publication write amplification

Per-file Contents API updates serialize repository mutation and normally create one commit per request. Git Data APIs permit a better shape:

```text
N changed text files
-> one tree request with N entries/content
-> one commit request
-> one ref update
```

Thus N-file publication can be constant in logical mutation count instead of O(N).

### 4. PR/status polling amplification

Repeatedly fetching a PR, comments, reviews, workflow state or merge state wastes calls when the desired action is simply "wake me when state changes". OpenAI's current GitHub/Work documentation exposes webhook-backed event-triggered PR tasks for eligible users.

## Proposed architecture — Read Local, Publish Bounded, Observe by Event

### Plane A — persistent local read/authoring cache

Preferred target:

```text
ChatGPT Work Desktop
-> open persistent local repository folder
-> one remote synchronization boundary
-> all AGENTS/checkpoint/spec/research/source reads local
-> local search/diff/edit operations
```

The local repository is a cache/working copy, never canonical authority.

A new chat must still prove which remote commit it represents. The intended bootstrap semantic becomes:

```text
synchronize current develop from GitHub once
-> record exact develop SHA
-> read AGENTS.md and CHECKPOINT.md from that exact local commit
-> continue local reads while the work unit remains bound to that snapshot
```

This can satisfy the existing cold-start intent with one logical remote synchronization instead of one remote call per bootstrap file, provided the local Git synchronization mechanics are empirically qualified.

### Plane B — bounded remote publication

Preferred publication order:

```text
local diff/change set
-> revalidate expected remote topic HEAD/base
-> create Git tree from all changed paths
-> create one commit with expected parent
-> non-force ref update
-> verify resulting ref/tree/diff
```

When direct local Git push is safely available to the Orchestrator surface, a normal push may be even cheaper as one logical transport operation. However Work documentation reviewed here does not explicitly establish the exact local terminal/Git execution guarantee needed to adopt that path.

Therefore the immediately testable connector fallback is the Git Data sequence:

```text
create_tree
create_commit
update_ref
```

with a final verification read.

### Plane C — event-driven PR observation

After PR creation, replace routine polling with an event-triggered GitHub task where supported:

```text
PR/review/comment/commit/merge event
-> ChatGPT task wakes
-> perform only the verification needed for that event
```

Polling remains a fallback when event triggers are unavailable or when a specific gate requires an immediate point-in-time read.

### Plane D — Library as optional durability, not hot path

D066's Library snapshot model remains useful for cross-chat recovery where the runtime supports the required operations. R026 recommends removing Library from the normal read path when Work Desktop can expose a persistent local repository directly.

Reason:

```text
persistent local repository
  already contains .git + working tree + cache

Library archive round trip
  adds package/upload/materialize/extract/validate steps
```

Library remains valuable as:

- backup/portable checkpoint;
- cross-device or non-Work fallback;
- recovery artifact when local workspace persistence cannot be guaranteed.

This recommendation does not invalidate R014/R015. It changes the preferred hot path only if the Work-local capability is qualified.

## Connector-only fallback when persistent local Work is unavailable

A second architecture can reduce calls without assuming a persistent desktop clone:

```text
1. fetch exact remote develop HEAD/tree once
2. download/materialize one exact-ref repository archive
3. read/search/edit locally in the temporary workspace
4. publish changed paths with create_tree + create_commit + update_ref
5. verify once
```

This changes repository materialization from O(number of files read) connector calls into one snapshot download plus bounded publication.

Limits:

- archive materialization does not contain `.git` history by itself;
- exact commit identity must be carried separately;
- the active ChatGPT surface must support the binary archive download safely;
- direct Git history operations are weaker than a persistent full clone unless a local repository is reconstructed.

Therefore archive mode is a fallback, not the preferred long-lived mode.

## Interaction-budget model

R026 defines a **logical GitHub interaction** as one explicit remote operation initiated by the Orchestrator surface: one connector action, one Git synchronization command such as fetch/push, one archive download, or one webhook-delivered event consumption. This metric intentionally does not pretend that one Git command equals one HTTP packet.

### Target — warm persistent local repository

Normal work unit after initial clone:

```text
bootstrap synchronization:       1
bootstrap file reads:            0 remote
working-set reads/search:        0 remote
intermediate authoring writes:   0 remote
publication:                     1 direct push
  OR connector fallback:         3 mutations (tree/commit/ref)
PR creation:                     1
PR idle observation:             0 polling when webhook task available
convergence verification:        1 bounded read
```

Expected target:

```text
direct-Git qualified path:       about 3-4 logical remote interactions/work unit
connector publication fallback:  about 5-6 logical remote interactions/work unit
```

The count is independent of the number of files locally read or edited.

### Target — cold/ephemeral archive fallback

```text
remote identity read:            1
exact snapshot archive:          1
working-set reads/search:        0 remote
publication:                     3 mutations
PR creation:                     1
convergence verification:        1
```

Expected target: about 7 logical interactions for the simple path, again independent of local file count.

These are design targets, not empirical claims.

## Why not use shallow clone by default

The optimization target is repeated use of one source repository, not disposable CI.

Shallow/treeless clones may reduce initial bytes but can increase later fetch/object-request costs and remove history required for ordinary Git analysis. GitHub engineering specifically recommends a full clone for a developer repeatedly focused on one reasonably sized repository.

For Agent Governance the pilot should first measure repository size. Use a blobless partial clone only if repository size materially justifies it. Do not equate "smaller initial clone" with "fewer long-term GitHub interactions."

## Safety and authority invariants

Any adopted optimization must preserve all of the following:

```text
GitHub remains canonical
exact develop/topic SHA is recorded at synchronization
local state never silently overrides remote movement
normal writes target only the verified topic branch
ref movement is non-force unless separately authorized
stale/non-fast-forward publication fails closed
PR remains the normal integration path to develop
AGENTS/checkpoint are read from one exact snapshot
local cache provenance is explicit
no Human copy/paste terminal role becomes the default
T058 freeze remains intact
```

A cached copy may reduce reads only while its exact represented remote SHA is known. It cannot replace remote freshness checks when a decision depends on current remote state.

## Qualification gaps

The following points are not yet proven and block normative adoption.

### Gap 1 — Work local Git mechanics

Official documentation proves Work Desktop local-folder access, but the reviewed material does not explicitly prove that the Orchestrator can independently execute the exact Git fetch/status/diff/commit/push workflow required here.

Need empirical answer:

```text
Can ChatGPT Work Desktop, without Human terminal mediation,
operate a local repository with the Git mechanics required by D061/D066?
```

### Gap 2 — plugin create_tree inline-content compatibility

GitHub officially supports `content` entries in `create tree`; the active ChatGPT GitHub wrapper must be tested with multiple paths in one call and verified to produce the exact intended tree.

### Gap 3 — event-task coverage and payload sufficiency

OpenAI documents PR event tasks, but the exact events/payloads available to this account/surface must be tested to determine which polling calls can truly be removed.

### Gap 4 — Library surface requalification

R014 qualified programmatic Library snapshot behavior in an earlier runtime. The current public Library documentation and this chat's exposed tools do not establish the same agentic API surface. D066's portable mode remains historically qualified, but any new implementation depending on programmatic Library operations should revalidate the current runtime before use.

### Gap 5 — bootstrap semantic equivalence

A later decision should state explicitly whether:

```text
one verified fetch of exact develop
+ local read of AGENTS/CHECKPOINT from that fetched commit
```

is accepted as semantically equivalent to separate remote file reads for the Orchestrator cold-start contract.

R026 recommends that equivalence if the fetch/local-integrity pilot passes.

## Recommended empirical pilot

Use a disposable repository such as `ManuelBouza/test_biblioteca`, not `agent-governance`, for capability qualification.

Compare three modes against the same synthetic multi-file work unit:

```text
M0 BASELINE
  connector on-demand file reads + normal connector writes

M1 CONNECTOR-MINIMIZED
  one exact-ref snapshot/archive + local reads
  Git Data create_tree/commit/ref publication

M2 WORK-LOCAL
  persistent local full clone in Work Desktop
  one fetch boundary + local reads/authoring
  direct Git publication if available, otherwise Git Data publication
```

Record at least:

```text
logical GitHub interactions
remote file-content reads
remote mutations
Human interventions
changed-file count
exact base/head identities
stale-remote behavior
final tree equivalence
PR creation/observation calls
cross-chat resume behavior
```

Minimum acceptance proposal:

```text
A. warm bootstrap requires <= 1 logical remote synchronization
B. normal local exploration requires 0 per-file GitHub reads
C. N-file publication is constant-count, not O(N)
D. stale topic movement blocks publication fail-closed
E. final remote tree exactly represents intended local state
F. no direct write to develop/main is possible through the workflow
G. Human terminal copy/paste is not required for the normal path
H. PR idle waiting uses event notification where supported instead of polling
```

## Recommendation

Proceed toward a **Read Local, Publish Bounded, Observe by Event** transport refinement of D066, but do not adopt it normatively yet.

Preferred order of evaluation:

```text
1. qualify Work Desktop persistent local repository + Git mechanics
2. qualify multi-file create_tree(content) + commit + non-force ref update
3. qualify PR webhook/event task coverage
4. measure actual interaction reduction against connector baseline
5. only then decide whether D066 and the cold-start/bootstrap contract should be refined
```

If Work-local Git mechanics fail qualification, retain the same architecture with the connector-minimized archive/cache mode as fallback. If event tasks are unavailable, keep bounded point-in-time PR reads rather than introducing unsafe assumptions.

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Normative change: none
T058: remains frozen
Recommended next action: Human-selected empirical qualification on disposable repository
```

No downstream Task Contract or decision should rely on the proposed interaction budgets until that empirical qualification is persisted and reviewed.
