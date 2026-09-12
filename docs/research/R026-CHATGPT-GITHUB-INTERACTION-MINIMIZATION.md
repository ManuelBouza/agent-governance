# R026 — ChatGPT/GitHub interaction minimization

Research-ID: R026  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-12  
Last-Reviewed: 2026-09-12  
Owner: ChatGPT Orchestrator  
Scope: ChatGPT Orchestrator repository-read, authoring, publication, review-status, persistence and cross-chat transport surfaces for reducing logical GitHub interactions while preserving GitHub canonical authority, D061 freshness, branch protection and D066 workspace semantics  
Question: How can Agent Governance minimize routine ChatGPT interactions with GitHub without weakening canonical Git authority, freshness, branch isolation, conflict detection, review traceability or the Human/Orchestrator/Executor ownership model?  
Evaluation-Refs: desk research 2026-09-12; empirical qualification pending on a disposable repository such as `ManuelBouza/test_biblioteca` before normative adoption; see correction appendices for current ChatGPT Web surface and Library approval constraints  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Executive synthesis

R014/R015 and D066 already reduce **write amplification** by allowing local Git authoring plus bounded publication to GitHub. R026 extends that analysis to the full interaction budget: reads, bootstrap, publication, PR observation and cross-chat resume.

The original desk-research architecture considered persistent local/Work Desktop and Library-assisted variants. Subsequent current-surface corrections narrow the actually testable architecture for Agent Governance in this chat to **ChatGPT Web only**:

```text
GitHub
  = canonical remote authority

ChatGPT Web runtime workspace
  = temporary working/cache surface when exact-ref materialization is possible

GitHub Git Data publication
  = bounded multi-file publication surface

GitHub PR event task / webhook
  = event-driven observation instead of polling
```

Library is excluded from the candidate path while it requires per-operation Human approval. Persistent user-local/Work Desktop repositories are also excluded from the current pilot because this project is operating in ChatGPT Web with no exposed PC-local repository.

The optimization principle remains:

```text
synchronize/materialize once
-> read and author in the web runtime many times
-> publish once/bounded
-> observe by event
-> verify once at convergence
```

The goal is not to remove GitHub from the workflow. GitHub remains canonical. The goal is to stop using GitHub as the per-file working filesystem.

R026 recommends an empirical qualification pilot before changing D066 or startup policy. The key current question is whether ChatGPT Web can materialize an exact repository snapshot into its runtime with sufficiently few remote operations, then publish a bounded change set safely through the connected GitHub tool surface.

## Baseline from R014/R015/D066

D066 already adopts this optimization direction:

```text
bootstrap/verify topic branch
-> many local edits and Git operations
-> optional persistence
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
- Library is not a Git remote or canonical authority and is excluded from the current candidate path;
- the current surface is ChatGPT Web, so persistent user-local repository assumptions are excluded from the current pilot;
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

   Current-surface correction: these Desktop/Work capabilities are not assumed for the active Agent Governance workflow because the Human Owner confirms the project is operating in ChatGPT Web.

3. **File storage and Library in ChatGPT**  
   https://help.openai.com/en/articles/20001052  
   Reviewed 2026-09-12.

   Material findings:

   - uploaded/generated files can persist in Library across chats;
   - Library is a persistent file store rather than a Git remote;
   - the public user documentation describes selecting/reusing Library files, but does not by itself establish a current agentic API for automated repository-snapshot materialization in every ChatGPT surface.

   Current-surface correction: the Human Owner reports per-operation approval prompts for Library. R026 therefore excludes Library from the optimized candidate path.

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

   Material finding: `git fetch` updates refs and downloads the objects needed to complete the requested histories, making a persistent clone an incremental cache rather than a repeated full repository download. This remains relevant engineering evidence, but a persistent local clone is not part of the current ChatGPT Web candidate path.

### Specialized engineering evidence

7. **GitHub Engineering — Git clone: a data-driven study on cloning behaviors**  
   https://github.blog/open-source/git/git-clone-a-data-driven-study-on-cloning-behaviors/  
   Reviewed 2026-09-12.

8. **GitHub Engineering — Get up to speed with partial clone and shallow clone**  
   https://github.blog/open-source/git/get-up-to-speed-with-partial-clone-and-shallow-clone/  
   Reviewed 2026-09-12.

9. **GitLab — Avoid the massive end-to-end tax of default full history clones**  
   https://about.gitlab.com/blog/git-clone-override-policy/  
   Published 2026-08-18; reviewed 2026-09-12.

These sources remain useful for general repository-materialization tradeoffs, but the current pilot must test the concrete capabilities of ChatGPT Web rather than assume Desktop clone semantics.

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

The current research branch has already demonstrated successful multi-file publication using Git Data primitives in this runtime, but stale-ref/race and exact snapshot-materialization behavior still require dedicated qualification.

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

## Proposed current architecture — Web Runtime, Publish Bounded, Observe by Event

### Plane A — ephemeral web-runtime working cache

Preferred current target:

```text
ChatGPT Web
-> obtain exact GitHub ref/snapshot with bounded remote interaction
-> materialize it into the available runtime workspace
-> read/search/diff/edit there
```

The runtime workspace is a cache/working surface, never canonical authority, and must be treated as ephemeral unless persistence is explicitly proven.

A new chat must still prove which remote commit its materialized state represents.

### Plane B — bounded remote publication

Preferred publication order:

```text
runtime diff/change set
-> revalidate expected remote topic HEAD/base
-> create Git tree from all changed paths
-> create one commit with expected parent
-> non-force ref update
-> verify resulting ref/tree/diff
```

The immediately testable connector path is:

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

### Plane D — excluded persistence assumptions

For the current surface:

```text
Library
  excluded because per-operation Human approval creates interaction amplification

Work/Desktop user-local repository
  excluded because the active product surface is ChatGPT Web

cross-chat runtime persistence
  not assumed until empirically qualified
```

## Connector-minimized current candidate

The architecture to evaluate is:

```text
1. identify exact remote develop/topic SHA
2. materialize one exact-ref repository snapshot or equivalent bounded working set into the ChatGPT Web runtime
3. read/search/edit within that runtime without additional per-file GitHub reads
4. revalidate expected remote topic state
5. publish changed paths with create_tree + create_commit + update_ref
6. create PR if needed
7. observe by event where supported
8. verify final remote state once
```

The central unresolved capability is step 2: whether the current web tool/runtime combination can materialize a useful exact repository snapshot in a bounded way without Library and without a persistent user-local clone.

## Interaction-budget model

R026 defines a **logical GitHub interaction** as one explicit remote operation initiated by the Orchestrator surface: one connector action, one bounded repository materialization operation, or one webhook-delivered event consumption. This metric intentionally does not pretend that one logical operation equals one HTTP packet.

### Target — ChatGPT Web runtime

Simple work unit target:

```text
remote identity/snapshot boundary: 1-2
working-set reads/search:          0 remote after materialization
intermediate authoring writes:     0 remote
publication:                       3 mutations (tree/commit/ref)
PR creation:                       1 when needed
PR idle observation:               0 polling when webhook task available
convergence verification:          1 bounded read
```

Expected target: roughly 5-7 logical remote interactions for the simple path, independent of the number of files read or edited after materialization.

This is a design target, not an empirical claim. The pilot must determine whether the snapshot/materialization boundary is actually available from ChatGPT Web.

## Safety and authority invariants

Any adopted optimization must preserve all of the following:

```text
GitHub remains canonical
exact develop/topic SHA is recorded at synchronization/materialization
runtime state never silently overrides remote movement
normal writes target only the verified topic branch
ref movement is non-force unless separately authorized
stale/non-fast-forward publication fails closed
PR remains the normal integration path to develop
AGENTS/checkpoint are read from one exact snapshot
runtime cache provenance is explicit
no Human copy/paste terminal role becomes the default
no per-operation Library approval becomes the transport mechanism
T058 freeze remains intact
```

## Qualification gaps

The following points are not yet proven and block normative adoption.

### Gap 1 — bounded web snapshot materialization

Need empirical answer:

```text
Can ChatGPT Web obtain and materialize an exact useful repository snapshot
with a bounded number of GitHub interactions,
without Library and without a user-local clone?
```

### Gap 2 — Git Data stale-ref semantics

Multi-file Git Data publication works in the current runtime, but the pilot must explicitly verify stale topic movement and fail-closed publication semantics.

### Gap 3 — event-task coverage and payload sufficiency

OpenAI documents PR event tasks, but the exact events/payloads available to this account/surface must be tested to determine which polling calls can truly be removed.

### Gap 4 — cross-chat cost

The current web runtime should be assumed ephemeral. Need to measure the cost of reconstructing the working cache at the beginning of a new chat and ensure the optimization remains worthwhile without Library.

### Gap 5 — bootstrap semantic equivalence

A later decision should state explicitly whether one verified exact-ref materialization plus runtime reads of AGENTS/CHECKPOINT is accepted as semantically equivalent to separate remote file reads for the Orchestrator cold-start contract.

## Recommended empirical pilot

Use a disposable repository such as `ManuelBouza/test_biblioteca`, not `agent-governance`, for capability qualification.

Compare:

```text
M0 BASELINE
  connector on-demand file reads + normal connector writes

M1 WEB-RUNTIME / CONNECTOR-MINIMIZED
  exact-ref bounded materialization into ChatGPT Web runtime
  -> runtime reads/search/authoring
  -> Git Data create_tree/commit/ref publication
```

Record at least:

```text
logical GitHub interactions
remote file-content reads
remote mutations
Human approval prompts
changed-file count
exact base/head identities
stale-remote behavior
final tree equivalence
PR creation/observation calls
cross-chat reconstruction cost
```

Minimum acceptance proposal:

```text
A. bootstrap/materialization requires a bounded remote synchronization cost
B. normal exploration after materialization requires 0 per-file GitHub reads
C. N-file publication is constant-count, not O(N)
D. stale topic movement blocks publication fail-closed
E. final remote tree exactly represents intended runtime state
F. no direct write to develop/main is possible through the workflow
G. Human terminal copy/paste is not required for the normal path
H. PR idle waiting uses event notification where supported instead of polling
I. normal repository operations do not require per-operation Library approval
```

## Recommendation

Proceed toward a **Web Runtime, Publish Bounded, Observe by Event** refinement, but do not adopt it normatively yet.

Preferred evaluation order:

```text
1. qualify bounded exact-ref materialization in ChatGPT Web
2. qualify stale-safe multi-file create_tree + commit + non-force ref update
3. qualify PR webhook/event task coverage
4. measure interaction reduction against connector baseline
5. measure cross-chat reconstruction cost
6. only then decide whether D066 and the cold-start/bootstrap contract should be refined
```

## Current disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Current surface: ChatGPT Web
Library candidate: excluded
Persistent user-local/Work Desktop candidate: excluded
Remaining candidate: web-runtime connector-minimized workflow
Normative change: none
T058: remains frozen
Recommended next action: Human-selected empirical qualification on disposable repository
```

No downstream Task Contract or decision should rely on the proposed interaction budget until that empirical qualification is persisted and reviewed.
