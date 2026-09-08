# R017 — ChatGPT Library-only document governance and Codex bridge research

Research-ID: R017  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-06  
Last-Reviewed: 2026-09-06  
Owner: ChatGPT Orchestrator  
Decision-Ref: none  
Related-Research: R014, R015  
Related-Decision: D066 (Git-backed source-maintenance path only; does not govern Library-only document projects)

## Provenance note

This investigation was initially drafted under the provisional identifier `R016` before the Orchestrator observed that another concurrent workstream had already integrated a different canonical R016 into `develop` (`docs/research/R016-MG1-V12-REFERENCE-FAMILY-REENTRY.md`). To preserve D057 stable research identity, this Library-only investigation is canonically allocated as **R017**.

Historical test fixture/probe identifiers containing `R016` are retained exactly as executed and are evidence labels only; they do not define the canonical research ID.

## Question

Can some projects intentionally keep documentary/project content in ChatGPT Library and avoid GitHub entirely when publication to GitHub is undesirable, while retaining enough control over canonical state, revisions, concurrency and recovery? Separately, can Codex directly or indirectly consume that Library-resident content?

## Scope

This research is limited to projects whose authoritative payload is documentary/content-oriented rather than a normal Git source repository. Examples include private research notes, internal dossiers, reports, specifications, collected evidence and other artifacts that may appropriately live inside ChatGPT Library but should not be published to GitHub.

This research does **not** alter D066. D066 remains the authority for the existing Git-backed ChatGPT Orchestrator source-maintenance adapter. R017 evaluates a separate Library-only content model.

## Sources checked on 2026-09-06

Official OpenAI sources reviewed:

- File storage and Library in ChatGPT
- Chat/file retention
- ChatGPT Work and Codex
- Using Codex with your ChatGPT plan
- Plugins in ChatGPT and Codex
- Built-in browser in the ChatGPT desktop app

Current official documentation states that Library files are saved for reuse, Library is available on web, files can be searched/browsed and added back to chats, and Library storage is independent of daily attachment/chat limits. Library itself does not add real-time external collaboration.

Current Codex documentation describes local folders/repositories/developer tools, plugins/apps and browser use. No official documentation found in this review states that Codex has a native first-party `ChatGPT Library` filesystem/source connector.

A Plugin Directory search for ChatGPT Library / Files / Codex did not expose a first-party plugin whose function is to mount or search the user's native ChatGPT Library from Codex. This is evidence about the discoverable surface on 2026-09-06, not a universal claim about future/private integrations.

## Empirical Library-only control experiment

A disposable namespace was used:

`/library-only-control-research-20260906/`

and deleted after the experiment.

### Same-path overwrite

Initial content:

```text
version: 1
content: alpha
```

Initial identities:

```text
file_id:         file_00000000a06881f4be1f3f3d5bbdef04
library_file_id: libfile_fdfd6b1e90348191bccd35d3a70c710a
visible version_id: 1
```

The same Library path was then overwritten with:

```text
version: 2
content: beta
```

After overwrite:

```text
library_file_id: unchanged
file_id:         file_00000000c0fc81f49cc28406d9293f07
visible version_id: still 1
```

The current read returned v2, while the earlier result reference for the v1 backing object was no longer resolvable through the active Library surface.

Bounded conclusion:

- `library_file_id` is a logical Library-item identity, not immutable content identity;
- a backing `file_id` can change after overwrite;
- the tested surface did not expose a usable Git-like historical content chain;
- governed history must not rely on in-place overwrite alone.

### Expected-version replacement path

The exposed Library management schema includes an `expected_current_version` field in some replacement flows. In this experiment, replacement by `library_file_id` + expected version returned:

`Shared-file replacement is not available.`

Therefore optimistic version/CAS replacement through that path is **not qualified** for this Library surface.

### Duplicate-name collision

A second upload targeted the already occupied path with overwrite disabled.

Library did not reject the operation as create-if-absent. It created:

`control(1).txt`

Therefore:

```text
same requested Library pathname
!= atomic create-if-absent mutex
```

A Library pathname cannot substitute for the GitHub CAS/sentinel lock qualified in R015/D066.

## Library-only governance model

### Core principle

Library can act as the authoritative **artifact store**, but should not be modeled as a Git repository or transactional key-value store.

Preferred model:

```text
immutable content objects
+ SHA-256 content identity
+ append-only receipts/manifests
+ append-only promotion records
+ explicit fork detection
```

Avoid:

```text
one mutable current.docx/current.md
+ repeated overwrite
```

### Suggested namespace

```text
/projects/<project-id>/
  project.json

  objects/
    <document-id>/
      <revision>-<sha256-prefix>.<ext>

  work/
    <work-unit-id>/
      candidate-<nonce>-<sha256-prefix>.<ext>
      receipt-<nonce>.json

  promotions/
    promote-<timestamp>-<nonce>.json

  checkpoints/
    checkpoint-<timestamp>-<nonce>.json

  tombstones/
    retire-<timestamp>-<nonce>.json
```

Files under `objects/`, `promotions/`, `checkpoints/` and `tombstones/` should normally be immutable after creation.

### Receipt identity

Each governed artifact should record at least:

```json
{
  "schema": "library-document-governance/v1",
  "project_id": "...",
  "document_id": "...",
  "work_unit": "...",
  "content_sha256": "...",
  "library_file_id": "...",
  "file_id": "...",
  "parent_content_sha256": "... or null",
  "created_at": "...",
  "state": "CANDIDATE | PROMOTED | RETIRED"
}
```

`library_file_id` alone is not sufficient immutable identity.

### Versioning rule

```text
never overwrite a promoted content object
```

Every revision is a new Library object with a unique name containing a revision/timestamp/nonce and SHA prefix.

Promotion records link parent -> candidate -> promoted child and produce an application-level history/DAG.

### Single-writer mode

If a project guarantees one active canonical writer, a mutable compact `HEAD.json` may point to the currently promoted SHA, provided promoted objects and prior promotion receipts remain immutable.

### Multi-writer mode

Pure Library currently has no qualified atomic mutex/CAS primitive.

Multiple chats may safely create isolated immutable candidate namespaces:

```text
/work/WT-A/...
/work/WT-B/...
```

but must not silently overwrite one shared canonical pointer.

Every promotion identifies its parent SHA. Reconstruction computes the promotion DAG.

Healthy state:

```text
exactly one reachable canonical head
```

If two promotions name the same parent but different children:

```text
FORK_DETECTED
-> fail closed
-> no automatic winner
-> explicit reconciliation required
```

This detects concurrency without losing either candidate, but does not provide strict mutual exclusion.

### Hybrid mode

Where strict writer exclusion is required but payload must remain outside GitHub, a separate approved coordination authority can provide CAS/locking while all documentary content remains in Library. That authority must be explicitly approved and must not contain prohibited payload.

## Integrity protocol

### Write

```text
1. create candidate bytes
2. compute SHA-256
3. upload under unique immutable Library path
4. rediscover/materialize exact object
5. recompute SHA-256
6. require exact match
7. create append-only receipt
8. create promotion record only after validation
9. reconstruct canonical head(s)
10. one head -> accepted progression
11. multiple heads -> FORK_DETECTED / stop
```

### Read/resume

```text
1. locate project namespace
2. load promotion receipts
3. reconstruct valid DAG
4. require one canonical head unless reconciling
5. locate exact content object from receipt
6. materialize
7. recompute SHA-256
8. compare receipt hash
9. only then use/edit
```

### GC

The R014 fail-closed principle still applies conceptually:

```text
new canonical state validated first
-> older state becomes retirement-eligible later
```

Never remove the sole validated promoted copy. Never automatically delete unresolved fork heads.

## Codex access to ChatGPT Library

### Native source/mount

Status:

`NOT DOCUMENTED / NOT DISCOVERED`

Do not instruct Codex as though `/ChatGPT Library/...` were a native filesystem path or mounted source.

### Manual bridge

Status:

`SUPPORTED COMPOSITION / MANUAL`

```text
Library
-> Human downloads exact immutable object + receipt
-> Codex local folder
-> Codex verifies SHA-256
```

### Browser-mediated bridge

The initial research classified:

```text
Codex Desktop/browser
-> authenticated ChatGPT Library web UI
-> exact object lookup
-> download
-> local workspace
```

as plausible but requiring empirical qualification.

That qualification was subsequently completed successfully. See:

`docs/research/CHATGPT-LIBRARY-CODEX-BROWSER-BRIDGE-QUALIFICATION-APPENDIX.md`

Current bounded status:

`EMPIRICALLY VERIFIED / VERSION_AND_SURFACE_SENSITIVE`

The test proved Codex could reach the authenticated Library UI, locate the exact Library-only object, download it, and independently reproduce the undisclosed expected size, SHA-256 and exact text without using GitHub or the receipt file.

This remains browser/UI mediation, not a native Library mount.

### Plugin path

Codex supports plugins/apps in supported task views, but no first-party native ChatGPT Library connector was discovered in this review. External stores such as Drive/Box/SharePoint would change the architecture and are not Library-only.

## Security/privacy interpretation

`not in GitHub` is not equivalent to `local-only` or `zero-cloud`.

Library content is stored in the user's/workspace's ChatGPT account and follows OpenAI's applicable storage, retention and data-control rules. Library is acceptable only when ChatGPT Library itself is an approved storage location for the project's classification.

If material is prohibited from both GitHub and ChatGPT cloud storage, R017 does not authorize Library as a destination.

## Capability matrix

| Capability | Status |
| --- | --- |
| persistent documentary storage in Library | VERIFIED / DOCUMENTED |
| folders/search/retrieval | VERIFIED / DOCUMENTED |
| materialize exact current object | VERIFIED |
| runtime SHA-256 verification | VERIFIED |
| same-path overwrite | VERIFIED; unsuitable as audit history |
| usable native historical version chain | NOT VERIFIED / NOT EXPOSED IN TEST |
| CAS replacement via expected Library version | NOT QUALIFIED |
| create-if-absent path as mutex | NOT SUPPORTED |
| strict Library-only cross-chat lock | NOT QUALIFIED |
| immutable object + append-only receipt model | PROPOSED / FEASIBLE |
| fork detection from parent hashes | PROPOSED / FEASIBLE |
| Codex native ChatGPT Library mount/source | NOT DOCUMENTED / NOT DISCOVERED |
| manual Library -> Codex local bridge | SUPPORTED COMPOSITION |
| Codex browser -> Library -> local download | EMPIRICALLY VERIFIED / VERSION_AND_SURFACE_SENSITIVE |
| Codex -> Library immutable upload-back | NOT VERIFIED |

## Recommended bounded architecture

```text
ChatGPT Library = canonical immutable documentary artifact store
ChatGPT Orchestrator = governance / promotion / reconciliation authority
SHA-256 = content identity
append-only promotion receipts = history/DAG
unique work-unit folders = workspace isolation
Codex = optional worker through explicit browser/manual bridge, not native Library reader
```

Concurrency:

```text
single active canonical writer
OR
optimistic isolated writers + fork detection
OR
approved non-content coordination authority
```

Do not claim strict multi-chat locking using Library alone.

## Remaining high-value qualifications

1. Codex local -> Library immutable upload-back:
   - create a new local revision;
   - compute SHA-256;
   - upload through authenticated Library UI as a **new uniquely named object**;
   - Orchestrator independently discovers/materializes and verifies it;
   - original promoted object remains unchanged.

2. Two-chat Library-only fork test:
   - both read same parent;
   - each writes unique immutable candidate + promotion record;
   - both survive;
   - reconstruction reports `FORK_DETECTED` instead of silently selecting a winner.

3. Cross-chat resume from exact receipt/hash.

4. Storage/GC behavior under quota pressure for immutable documentary history.

## Disposition

R017 is:

```text
Research-State: COMPLETE
Decision-State: NOT_REQUIRED
```

The research supports a bounded Library-only documentary architecture, but no normative Agent Governance adapter is adopted by this artifact.