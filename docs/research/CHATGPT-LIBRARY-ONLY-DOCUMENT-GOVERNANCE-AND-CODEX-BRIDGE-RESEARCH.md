# R016 — ChatGPT Library-only document governance and Codex bridge research

Research-ID: R016  
Research-State: COMPLETE  
Decision-State: NOT_REQUIRED  
Opened: 2026-09-06  
Last-Reviewed: 2026-09-06  
Owner: ChatGPT Orchestrator  
Decision-Ref: none  
Related-Research: R014, R015  
Related-Decision: D066 (Git-backed source-maintenance path only; does not govern Library-only document projects)

## Question

Can some projects intentionally keep documentary/project content in ChatGPT Library and avoid GitHub entirely when publication to GitHub is undesirable, while retaining enough control over canonical state, revisions, concurrency and recovery? Separately, can Codex directly or indirectly consume that Library-resident content?

## Scope

This research is limited to projects whose authoritative payload is documentary/content-oriented rather than a normal Git source repository. Examples include private research notes, internal dossiers, reports, specifications, collected evidence and other artifacts that may appropriately live inside ChatGPT Library but should not be published to GitHub.

This research does **not** alter D066. D066 remains the authority for the existing Git-backed ChatGPT Orchestrator source-maintenance adapter. R016 evaluates a separate Library-only content model.

## Sources checked on 2026-09-06

Official OpenAI sources:

- File storage and Library in ChatGPT: `https://help.openai.com/en/articles/20001052-file-storage-and-library`
- Chat/file retention: `https://help.openai.com/en/articles/8983778-how-are-files-vs-chats-retained`
- ChatGPT Work and Codex: `https://help.openai.com/en/articles/20001275`
- Using Codex with your ChatGPT plan: `https://help.openai.com/en/articles/11369540`
- Plugins in ChatGPT and Codex: `https://help.openai.com/en/articles/20001256/`
- Built-in browser in the ChatGPT desktop app: `https://help.openai.com/en/articles/20001277-using-the-built-in-browser-in-the-chatgpt-desktop-app`

Current official documentation states that Library files are saved for reuse, Library is available on web, files can be searched/browsed and added back to chats, and Library storage is independent of daily attachment/chat limits. Library itself does not add real-time external collaboration. Official documentation also states that supported Codex task views can use plugins, Codex can work with local folders/repositories/developer tools, and the desktop built-in browser can sign in to websites and download files with approval.

No official documentation found in this review states that Codex has a native first-party `ChatGPT Library` filesystem/source connector.

A Plugin Directory search for `ChatGPT Library files Codex` and `OpenAI files storage Library` did not expose a first-party plugin whose function is to mount or search the user's native ChatGPT Library from Codex. This is evidence about the discoverable surface on 2026-09-06, not a universal claim that no future/private integration can exist.

## Empirical Library-only control experiment

A disposable Library namespace was used:

`/library-only-control-research-20260906/`

It was deleted after the experiment.

### Initial object

Uploaded:

`/library-only-control-research-20260906/control.txt`

Initial bytes:

```text
version: 1
content: alpha
```

Initial SHA-256 computed before upload:

`a5ccec54d5758688e6591efbcb6b1846732950acb2ec63bcea154cc569449cb0`

Initial Library identities:

```text
file_id:         file_00000000a06881f4be1f3f3d5bbdef04
library_file_id: libfile_fdfd6b1e90348191bccd35d3a70c710a
visible version_id from search: 1
```

### Same-path overwrite

The same path was overwritten with:

```text
version: 2
content: beta
```

SHA-256 before upload:

`31a3c59ccc97619d2d06a5e244b2c47882983b96446c125d99f60410f9ddbd93`

Library reported `File overwritten`.

After overwrite:

```text
library_file_id: remained libfile_fdfd6b1e90348191bccd35d3a70c710a
new file_id:      file_00000000c0fc81f49cc28406d9293f07
visible version_id from search: still 1
```

A read through the current result returned exactly the v2 content.

The earlier result reference for the v1 backing object was no longer resolvable through the active Library surface.

Bounded conclusion:

- a stable `library_file_id` is a logical Library-item identity, not a content-version identity;
- a backing `file_id` may change when the logical item is overwritten;
- the tested surface did not expose a usable Git-like historical version chain for prior content;
- same-path overwrite therefore must not be used as the sole audit/history mechanism for a governed Library-only project.

### Tested optimistic version replacement path

The exposed Library-management schema advertises an `expected_current_version` field for replacement by `library_file_id` in some flows. In this experiment, attempting replacement by `library_file_id` + expected version returned:

`Shared-file replacement is not available.`

Therefore optimistic version/CAS replacement through that path is **not qualified** for the tested Library item/runtime.

Do not design a Library-only concurrency protocol that assumes this field is generally available until separately qualified.

### Duplicate-name collision

A second upload targeted the already occupied path with `overwrite=false`.

Instead of rejecting the create as an ownership collision, Library succeeded by assigning a duplicate-safe name:

`control(1).txt`

Bounded conclusion:

```text
same requested Library pathname
!= atomic create-if-absent mutex
```

A Library filename/path cannot currently substitute for the GitHub create/CAS lock qualified in R015/D066.

## Library-only control model

### Core design principle

Library can be the authoritative **artifact store**, but it should not be treated as a Git repository or as a transactional key-value store.

The safer model is:

```text
immutable content objects
+ append-only receipts/manifests
+ explicit canonical-promotion records
+ hash-based identity
+ fork detection
```

rather than:

```text
one mutable current.docx/current.md
+ overwrite in place
```

### Proposed namespace

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

### Content identity

Every governed artifact should have an explicit receipt containing at least:

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

`library_file_id` alone must not be treated as immutable content identity because the experiment showed that the same Library logical item can acquire a new backing `file_id` after overwrite.

### Versioning

Recommended rule:

```text
never overwrite a promoted content object
```

A new revision is a new Library object with a unique filename containing either a monotonic revision number plus hash prefix, or a timestamp/nonce plus hash prefix.

A promotion record links:

```text
parent promoted SHA
-> candidate SHA
-> new promoted SHA
```

This produces an application-level history even though Library does not expose a qualified native Git-like version history.

### Canonical head

A mutable `current` pointer is convenient but introduces last-writer-wins risk. Therefore two modes should be distinguished.

#### Mode S — single active writer

For projects that guarantee one active Orchestrator/writer at a time, a compact mutable `project.json`/`HEAD.json` may point to the current promoted SHA, provided every promoted object and prior promotion receipt remains immutable.

Even in this mode, destructive overwrite of the promoted artifact itself is prohibited.

#### Mode M — potentially multiple writers/chats

Pure Library currently lacks a qualified atomic mutex/CAS primitive.

Therefore do **not** allow multiple chats to silently update one mutable canonical pointer.

Use append-only promotion records instead. Every promotion states its parent SHA. Reconstruction computes the promotion DAG.

Expected healthy state:

```text
exactly one reachable head
```

If two promotions name the same parent but different child SHAs:

```text
FORK_DETECTED
-> fail closed
-> no automatic winner
-> require reconciliation / Human or explicit merge procedure
```

This does not prevent concurrent drafts; it prevents concurrency from being silently mistaken for a single linear history.

### Workspaces without GitHub

Multiple chats may safely create **separate immutable candidate namespaces** because collision-free unique names do not require shared mutation:

```text
/work/<work-unit-A>/...
/work/<work-unit-B>/...
```

They may work independently on separate candidate artifacts.

What Library-only does not currently provide is the R015/D066 equivalent of an atomic exclusive-writer lock over one shared logical workspace.

Therefore a Library-only project should choose one of:

1. **single-writer canonical mode** — one active canonical writer; other chats read or create isolated candidates;
2. **optimistic multi-writer mode** — isolated candidates and append-only promotions; competing promotions create a detected fork that must be reconciled;
3. **hybrid coordination mode** — content remains only in Library, while a separate non-content authority provides atomic locking/CAS. The separate authority must itself be explicitly approved for the project.

Pure Library alone should not claim strict cross-chat mutex semantics on the currently qualified surface.

## Integrity and recovery

### Write protocol

```text
1. generate candidate bytes
2. compute SHA-256 locally/runtime-side
3. upload as unique immutable Library object
4. rediscover/materialize exact uploaded object
5. recompute SHA-256
6. compare expected == restored
7. create append-only receipt
8. only after validation create promotion record
9. reconstruct head(s)
10. if exactly one valid head -> canonical progression accepted
11. if multiple heads -> FORK_DETECTED / stop
```

### Read/resume protocol

```text
1. locate project namespace
2. load project metadata + promotion receipts
3. reconstruct valid promotion DAG
4. require one canonical head unless entering explicit reconciliation mode
5. locate exact content object from receipt
6. materialize
7. recompute SHA-256
8. compare receipt hash
9. only then use/edit content
```

### Garbage collection

R014's fail-closed GC principle still applies conceptually:

```text
new canonical state validated first
-> older state becomes retirement-eligible later
```

For documentary Library-only projects, retaining immutable historical revisions is usually preferable unless storage pressure requires cleanup.

Never remove the sole validated promoted copy. Never delete unresolved fork heads automatically.

## Codex access to ChatGPT Library

### Native direct access

Current status:

`NOT DOCUMENTED / NOT DISCOVERED`

The official Library article documents adding Library files to **ChatGPT chats**. The current Codex documentation describes local folders/repositories/developer tools, plugins/apps and browser use. During this review, no official first-party Codex source was found that mounts the user's native ChatGPT Library as a Codex filesystem or direct source.

The Plugin Directory search also did not discover a first-party `ChatGPT Library` connector/plugin for Codex.

Therefore do not instruct Codex as though `/ChatGPT Library/...` were a native path or mounted source.

### Bridge A — manual Library download -> Codex local workspace

Status:

`SUPPORTED COMPOSITION / MANUAL`

Official Library documentation supports downloading saved files. Official Codex documentation supports working with local folders/files.

Flow:

```text
Library
-> Human/download selected immutable object(s)
-> local controlled folder
-> Codex opens that folder
```

This is simple and auditable but manual.

For a governed flow, transfer a receipt alongside each file and have Codex verify SHA-256 before use.

### Bridge B — Codex desktop browser -> authenticated ChatGPT Library web UI

Status:

`TECHNICALLY PLAUSIBLE FROM DOCUMENTED COMPONENTS / NOT YET LIBRARY-SPECIFICALLY QUALIFIED`

Official documentation says:

- Library is available on the web;
- the desktop built-in browser can be opened from a Codex chat;
- the browser can sign in to websites;
- Codex/ChatGPT can navigate tabs and initiate downloads with approval.

Therefore a plausible controlled bridge is:

```text
Codex desktop
-> built-in browser or Codex Chrome extension
-> authenticated chatgpt.com Library
-> select exact Library object
-> download to Codex-controlled local workspace
-> verify receipt/hash
```

This is **not** native Library access. It is UI/browser automation over the Library web surface.

It must be treated as version-sensitive and permission-sensitive. Browser page content is untrusted input, and the Human should verify account/host before approval.

A dedicated empirical qualification is still required before making this an automatic Agent Governance adapter.

### Bridge C — Codex plugin/app

Codex officially supports plugins/apps in supported task views via `Sources -> Use plugins`.

Current status for native ChatGPT Library:

`NO FIRST-PARTY LIBRARY PLUGIN DISCOVERED`

External document stores such as Google Drive, Box or SharePoint can be exposed through plugins where enabled, but using them changes the storage architecture: the content no longer lives *only* in native ChatGPT Library.

A future first-party Library plugin or supported internal Files app would be the cleanest Codex bridge if OpenAI exposes one.

### Bridge D — Enterprise/Edu Compliance API

Official Library documentation states that Enterprise/Edu compliance administrators have Library-specific Compliance API endpoints for export/delete while files are active.

This is an administrative/compliance surface, not currently documented as a normal Plus/Pro member content API or as a Codex Library filesystem adapter.

Do not use it as the default R016 architecture without a separate Enterprise-specific design and authorization review.

## Security/privacy interpretation

Choosing Library instead of GitHub can be reasonable when GitHub publication/storage is inappropriate for a project's documentary payload. However, `not in GitHub` is not equivalent to `local-only` or `zero-cloud`.

Library content is stored in the user's/workspace's ChatGPT account and follows OpenAI's applicable storage/retention/data controls. Project classification must therefore evaluate whether ChatGPT Library itself is an approved storage location for the content.

If the material is prohibited from both GitHub and ChatGPT cloud storage, R016 does not make Library an acceptable destination.

## Capability matrix

| Capability | Status | Notes |
| --- | --- | --- |
| persistent documentary storage in Library | VERIFIED / DOCUMENTED | files remain available for reuse until deletion/retention policy applies |
| folders / search / retrieval | VERIFIED / DOCUMENTED | current Library and Files surfaces |
| materialize exact current object | VERIFIED | Files tooling |
| runtime SHA-256 verification | VERIFIED | materialize + local hashing |
| same-path overwrite | VERIFIED | changes backing file identity; not suitable as audit history |
| usable native historical version chain | NOT VERIFIED / NOT EXPOSED IN TEST | old result became unresolved; visible version_id remained `1` |
| CAS replacement via expected Library version | NOT QUALIFIED | tested path returned `Shared-file replacement is not available` |
| create-if-absent path as mutex | NOT SUPPORTED | duplicate-safe `control(1).txt` created instead of collision |
| strict Library-only cross-chat lock | NOT QUALIFIED | no atomic primitive established |
| immutable object + append-only receipt model | PROPOSED / FEASIBLE | uses only qualified create/read/materialize semantics |
| fork detection from parent hashes | PROPOSED / FEASIBLE | detects, does not prevent concurrent promotion |
| Codex native ChatGPT Library mount/source | NOT DOCUMENTED / NOT DISCOVERED | no first-party integration found in reviewed docs/plugins |
| Library download -> Codex local folder | SUPPORTED COMPOSITION | manual bridge |
| Codex browser -> ChatGPT Library web -> download | PLAUSIBLE / NEEDS EMPIRICAL QUALIFICATION | documented browser + Library components |
| Codex plugin to external document store | DOCUMENTED | not Library-only architecture |
| Enterprise Library Compliance API | DOCUMENTED ADMIN SURFACE | not default member/Codex bridge |

## Recommended bounded architecture

For projects where documentary payload should not be placed in GitHub but ChatGPT Library is an approved storage location:

```text
ChatGPT Library = canonical immutable artifact store
ChatGPT Orchestrator = governance/reconciliation authority
content SHA-256 = immutable content identity
append-only promotion receipts = history/DAG
unique per-work-unit Library namespace = workspace isolation
Codex = optional consumer/producer through explicit bridge, not native Library reader
```

Concurrency policy:

```text
single active canonical writer
OR
optimistic isolated writers + fork detection
```

Do not claim strict multi-chat exclusive locking using Library alone.

For Codex-heavy projects, a Library-only payload model is operationally viable only if one of the explicit bridges is acceptable. If automatic Codex access is a primary requirement, an approved plugin-accessible document system may currently be operationally stronger than native Library-only storage.

## Next empirical qualifications worth doing

1. Codex desktop/browser real round trip:
   - open authenticated ChatGPT Library;
   - locate exact test object;
   - download to Codex workspace;
   - verify SHA-256;
   - modify locally;
   - determine whether safe upload-back to Library can be performed without ambiguous replacement.

2. Library-only fork test with two independent chats:
   - both read same promoted parent;
   - each writes a unique immutable candidate and promotion receipt;
   - verify both survive without overwrite;
   - reconstruct two heads;
   - confirm system classifies `FORK_DETECTED` rather than choosing silently.

3. Closed-work-unit resume:
   - restore exact immutable candidate by receipt/hash in a new chat;
   - continue as a new candidate revision without overwriting history.

4. Storage/GC qualification for immutable documentary history under quota pressure.

## Disposition

R016 is `COMPLETE / NOT_REQUIRED` as research.

The research supports a bounded Library-only documentary architecture, but no normative Agent Governance adapter is adopted by this artifact.

Key conclusion:

```text
Library-only canonical document storage is feasible
if content objects are immutable and history is application-level;
Library alone is not currently qualified as an atomic multi-chat lock/version-control system;
Codex has no documented native Library source, but manual/local and browser-mediated bridges are viable candidates.
```
