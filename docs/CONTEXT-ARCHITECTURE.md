# Source Repository Context Architecture

Status: ACTIVE
Controlling decision: `docs/decisions/D046-agent-capability-engineering-and-context-architecture.md`
Consumer precursor: `governance-core/CONTEXT.md`
RCAB v1 policy: `docs/decisions/D047-rcab-context-map-and-ratchet-policy.md`
RCAB snapshot/live refinement: `docs/decisions/D049-rcab-snapshot-live-separation.md`
Context map: `docs/CONTEXT-MAP.md`

## Purpose

Apply progressive context loading to the Agent Governance source repository without creating a second authority or copying Consumer lifecycle semantics into source maintenance.

The primary rule is:

> **Budget the load path, not just the file.**

A large on-demand evidence file can be healthy. A smaller file forced into every bootstrap can be expensive. Fragmenting one concern across many mandatory reads can be worse than keeping one cohesive file.

## Load classes

Agent-relevant source artifacts may be classified as:

- `bootstrap` — exposed in nearly every applicable source-maintenance session;
- `router` — identifies the current frontier or the next exact context to load;
- `focused` — authority/context for one concern;
- `task` — the current Task/Operational Contract or review authority;
- `evidence` — handoffs, receipts, eval results and history loaded only when needed;
- `generated-index` — reproducible discovery metadata, never authority;
- `generated-data` — machine-readable outputs/fixtures/reports not intended for unconditional model loading;
- `exempt-on-demand` — potentially large material whose normal load path is explicitly bounded.

Classification controls measurement and routing expectations. It MUST NOT transfer authority between files or roles.

## Measurement

Tokenizer-neutral physical baselines use UTF-8 bytes. Other deterministic diagnostics may include characters, lines, Markdown headings, reference counts, file type and content digests.

Token counts are valid measurements only when their tokenizer, host/model, or runtime observation source is identified. A bytes/characters heuristic MUST NOT be labelled as an exact token count.

Useful contextual metrics include:

- **Bootstrap Context Cost (BCC)** — repository context loaded before task-specific focused context is selected;
- **Task Minimum Context (TMC)** — unavoidable bootstrap/router context plus the current task and exact controlling references;
- **Retrieval Fan-Out (RFO)** — distinct repository artifacts actually loaded for a task;
- **Navigation Depth (ND)** — routing/reference hops from bootstrap/router to the target;
- **Context Amplification Ratio (CAR)** — compare observed load to an explicitly defined minimum/relevant baseline.

Static reference-graph fan-out is not the same as actual RFO. Do not claim actual load metrics without a load trace or an explicit deterministic load model.

## Budget adoption

The source repository begins with **measure -> accepted baseline -> warning/ratchet -> selective hard enforcement**.

No source-repository universal hard size budget is authorized before the baseline task establishes measurements. A later budget must identify its load class, metric, rationale and exception semantics.

The existing Consumer budgets in `governance-core/CONTEXT.md` remain unchanged and MUST NOT be silently reinterpreted as source-repository limits.

## RCAB v1 selected policy

D047 and T030-R2 establish the first source-repository warning/ratchet policy.

The mandatory source cold-start cohort is exactly the registered `bootstrap` + `router` surface in `docs/CONTEXT-MAP.md`. Its accepted T030-R2 physical reference is:

- `2` files;
- `21,471` UTF-8 bytes;
- `298` lines.

RCAB v1 always reports current delta from that reference. It emits a **non-blocking** bootstrap-growth warning when the cohort grows above two files or aggregate UTF-8 bytes exceed `105%` of the accepted reference.

The 5% band is a review-sensitivity margin, not a model-capacity claim, safety threshold or token estimate. Warning state alone MUST NOT fail a task, block a merge, or trigger an automatic split.

`focused`, `task`, `evidence`, `generated-data` and `exempt-on-demand` artifacts have no RCAB v1 absolute physical-size warning. Their size remains report-only evidence until observed load/routing evidence justifies a class-specific policy.

The allowed blocking RCAB checks are mechanically decidable integrity failures such as malformed/ambiguous map registry, duplicate/conflicting classifications, missing registered targets, non-reproducible canonical projections, explicit currentness failures when a workflow intentionally requests live comparison, and source/distribution leakage already covered by package-isolation verification.

A historical committed snapshot being older than current registered source is not, by itself, a generic blocking condition under D049.

The accepted reference does not silently ratchet. A lower observed footprint may be reported as a ratchet candidate, but changing the authoritative reference requires an Orchestrator-owned reviewed policy/baseline update.

## Discovery and indexes

The preferred lightweight architecture is:

```text
canonical Git + Markdown authority
        -> compact context map / direct routes
        -> generated machine-readable projection when useful
```

`docs/CONTEXT-MAP.md` is the selected compact human-readable routing registry. It deliberately registers only stable, high-value routes. The current exact frontier remains in `docs/orchestrator/CHECKPOINT.md`.

A generated manifest may project registered paths, classifications, metrics, hashes and route membership. It is discovery/evidence only.

Generated indexes/manifests:

- MUST be reproducible and canonically ordered for the inputs they represent;
- MUST identify a deterministic content epoch/identity sufficient to distinguish snapshot content;
- MAY remain as historical snapshot evidence after repository authority advances;
- MUST prove live currentness against the exact candidate state before being used as a live merge/release/currentness gate;
- MUST NOT duplicate or supersede normative authority;
- MUST NOT require embeddings/vector infrastructure for initial operation.

The RCAB manifest uses registered-content identity rather than requiring the Git SHA of the commit that contains the manifest itself, avoiding a D029-like self-reference problem.

Do not expand the context map into a repository-wide catalog merely because more files can be indexed. Add stable routes only when they reduce real discovery/load cost.

## Snapshot evidence vs live RCAB state

D049 separates two concerns that T031 initially coupled.

### Committed snapshot

`baselines/repository-context-manifest-v1.json` is a deterministic evidence snapshot for one registry/content epoch. Its stored metrics and hashes describe that epoch. The snapshot does not become normative authority and does not claim that mutable registered files have not changed since generation.

Normal accepted Markdown evolution may therefore make an older snapshot differ from live source without making the ordinary deterministic suite red solely for that reason.

### Live state

Current RCAB state must be derived from current authority:

```text
current docs/CONTEXT-MAP.md registry
        + current tracked registered files
        -> live integrity + current metrics + ratchet warning
```

Live status MUST NOT trust the committed snapshot as current.

### Explicit currentness comparison

A workflow may explicitly compare a snapshot against current registered content. That deterministic operation may report/fail stale or tampered state when currentness is the requirement being checked.

Fixture coverage must continue proving fresh/stale/tampered comparison. The ordinary full deterministic regression path, however, must not assume that every historical snapshot is required to equal today's mutable source state.

Snapshot refresh is an explicit RCAB maintenance action, not an incidental requirement attached to every registered Markdown change.

## Markdown decomposition

A budget warning triggers cohesion/retrieval review; it does not trigger an automatic split.

Split Markdown only when coherent responsibilities can be loaded independently and the resulting navigation remains direct. Prefer:

```text
stable-entry.md       -> concise authority/router for the concern
concern/
  focused-a.md
  focused-b.md
```

when preserving the stable path materially improves compatibility. Do not keep a full duplicate summary at the old path.

Normative Markdown MUST NOT be automatically split or rewritten solely from an LLM recommendation or numeric threshold. ChatGPT Orchestrator retains Markdown/authority review.

## Code and structured data

Code MUST NOT be split solely by LOC/bytes. Evaluate cohesion, responsibilities, complexity, coupling, public surface, change coupling, test boundaries and retrieval fan-out together.

JSON/JSONL/evidence/generated data MAY grow physically when normal reads are bounded. Append-only history should support delta/query reads instead of unconditional full-context loading.

## Deterministic context checks

Once their semantics are explicitly represented, suitable hard checks include broken registered references, forbidden recursive includes, duplicate canonical authority identities, non-reproducible generated projections, explicit live-currentness mismatch where a workflow intentionally requires currentness, and source/distribution boundary leaks.

Historical snapshot age alone is evidence, not a default hard failure.

Size, fan-out and navigation metrics start as evidence/warnings unless a later accepted baseline/decision makes a particular regression mechanically blocking.

Semantic duplication/responsibility analysis may use model assistance as advisory evidence only.

## Source/distribution boundary

Source context tooling and source indexes are source-only unless a later explicit distribution decision says otherwise.

In particular, repository-context measurement/lint tooling MUST NOT be placed inside a runtime path that T020 packages into the Consumer artifact. Context tooling must not alter the accepted self-contained Consumer payload or introduce source-maintenance overlays into distribution.

## EGLL

Material context regressions or incidents may become EGLL cases when they represent a reusable failure/control class. A warning alone is not automatically a learning incident.

Possible fingerprints must be selected from observed evidence, not predeclared as ceremony. Mechanically decidable context failures should eventually be promoted to deterministic controls with bad-case/good-case replay.

L006 records the T021-era discovery that continuously coupling a committed RCAB snapshot to mutable live registered Markdown can poison unrelated deterministic baselines. D049/T032 are the selected control path.
