# T068 — ChatGPT Skill Host Materialization and Qualification

## Identity

- Task ID: `T068`
- Status: `READY`
- Type: `mixed`
- SDD profile: `STANDARD`
- Base branch: `develop`
- Base SHA: `5bed8b952a3c552e3af0abfdbe07895864319696`
- Topic branch: `feat/t068-chatgpt-skill-host-activation`
- Expected Executor handoff: `handoffs/T068-executor-handoff.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: `ChatGPT Orchestrator / Agente de IA Ejecutor / Human Owner`
- ChatGPT Effort: `MEDIUM`
- Execution Shape: `MULTI_EXECUTION`

## Objective

Materialize the adopted R029/D082 Agent Governance Skill architecture as reproducible ChatGPT-loadable Skill bundles without semantic forking, cross the explicit Human/workspace installation gate, and qualify observable ChatGPT activation/routing behavior before claiming host activation.

This task does not reopen D082/T067 and does not start or modify T066.

## Controlling references

- `AGENTS.md`
- `docs/research/R031-CHATGPT-SKILL-HOST-MATERIALIZATION.md`
- `docs/RESEARCH-TRACEABILITY.md`
- `docs/decisions/D082-r029-lean-root-and-transverse-skill-architecture.md`
- `maintainer-skill/SKILL.md`
- `repository-change-control-skill/SKILL.md`
- `upstream-version-revalidation-skill/SKILL.md`
- `research-evidence-traceability-skill/SKILL.md`
- `durable-work-checkpoint-skill/SKILL.md`
- `executor-launch-handoff-skill/SKILL.md`
- `docs/TASK-CONTRACTS.md`
- `docs/ORCHESTRATOR-CHECKPOINTS.md`

R031 is the current host-evidence carrier. OpenAI Skills behavior is version-sensitive and must be refreshed before consequential later reliance when material drift is observed.

## Requirement / specification delta

### ADDED

- **REQ-T068-1 — Packaging:** reproducibly materialize exactly six top-level ChatGPT Skill bundles: `source-maintainer` plus the five D082 transverse Skills.
- **REQ-T068-2 — Resource completeness:** preserve each root `SKILL.md` and all required Skill-local references/resources with relative paths intact.
- **REQ-T068-3 — Provenance:** bind generated packages to a canonical source revision without making generated host artifacts authoritative over Git.
- **REQ-T068-4 — Deterministic validation:** reject missing/extra top-level Skills, missing `SKILL.md`, missing required Skill-local resources, duplicate Skill names, escaping references, contaminated output, and any top-level promotion of `workspace-isolation`.
- **REQ-T068-5 — Human install gate:** distinguish `PACKAGED` from `INSTALLED`; fail closed when the ChatGPT Skills surface, upload permission, scan, or installation is unavailable or blocked.
- **REQ-T068-6 — Post-install qualification:** qualify observable explicit invocation, automatic routing, anti-trigger behavior, Maintainer internal routing, and transverse composition after installation.
- **REQ-T068-7 — No semantic host fork:** ChatGPT adaptation is limited to packaging, provenance, narrow host adapters, and qualification assets unless durable Orchestrator authority explicitly re-enters Design.

### PRESERVED

- **REQ-T068-P1:** one Maintainer domain Skill with Orchestrator/Executor internal routes; exactly five transverse Skills; `workspace-isolation` remains subordinate under `executor-launch-handoff`.
- **REQ-T068-P2:** Git remains canonical authority over installed Skill snapshots/host state.
- **REQ-T068-P3:** authority, ownership, cold-start and fail-closed correctness remain valid with Skills absent/disabled.
- **REQ-T068-P4:** D068 ownership boundaries remain unchanged.
- **REQ-T068-P5:** T066 remains untouched and unstarted.
- **REQ-T068-P6:** ChatGPT/Codex empirical parity remains `NOT_ESTABLISHED` unless separately authorized and demonstrated.

## Controlling Design

### Host architecture

```text
canonical Git Skill directories
    -> deterministic package/validation layer
    -> six independent ChatGPT Skill bundles
    -> Human/workspace upload + OpenAI scan
    -> installed ChatGPT Skill set
    -> explicit + automatic-routing qualification
```

Do not combine the six semantic Skills into a ChatGPT-specific mega-Skill. `workspace-isolation` is never emitted as a top-level upload package.

### Packaging design

Stage 5 materializes a deterministic packager/validator that:

- reads the six canonical Skill source directories;
- resolves Skill identity from each root `SKILL.md`;
- recursively includes Skill-local files;
- validates required internal relative references and rejects escape attempts;
- rejects an independent root `workspace-isolation` / `workspace-isolation-skill` source;
- emits one archive per top-level Skill to generated/untracked output;
- emits a machine-readable manifest with Skill name, source directory, source revision, file inventory and digests;
- normalizes archive timestamps, permissions, ordering and compression inputs for reproducible output;
- refuses unrelated output-directory entries rather than deleting them;
- excludes `.git`, caches, local generated state and unrelated repository files from Skill sources;
- does not vendor mutable repository authority such as `AGENTS.md`, the checkpoint or Task Contracts into the bundle unless intentionally Skill-local source.

Generated archives are disposable distribution artifacts; canonical Skill directories and packaging code remain authoritative.

### Qualification design

Two evidence planes apply:

1. **Pre-host deterministic conformance:** topology, package completeness, provenance, reproducibility, no sixth Skill, no semantic source rewrite.
2. **Post-install ChatGPT behavioral qualification:** explicit availability, positive auto-routing, negative/near-miss anti-trigger cases, Maintainer Orchestrator/Executor route separation, transverse composition, absence of top-level `workspace-isolation`, and Git-bootstrap/fail-closed behavior.

The frozen Orchestrator-owned corpus is `evals/t068_chatgpt_skill_host/qualification-corpus.json` with 22 observable scenarios: six explicit, six auto-positive, six auto-negative, three transverse composition cases, and one Maintainer role-routing case.

Score only observable behavior and explicit Skill invocation surfaces. Do not require hidden chain-of-thought or undocumented routing telemetry.

### Installation design

Expected eligible-workspace path from current OpenAI documentation:

`Plugins -> Skills -> Create -> Upload from your computer`

Record each bundle outcome as `INSTALLED`, `NEEDS_REVIEW`, `BLOCKED`, `UNAVAILABLE`, or the precise equivalent surfaced by ChatGPT. If the UI rejects the candidate package form, preserve semantics and re-enter only the narrow packaging design needed to satisfy the host.

## Plan & Trace

| Unit | Requirement / Design | Candidate/evidence | State |
| --- | --- | --- | --- |
| `E1` Research + authority freeze | R031; all REQ/PRESERVED | R031 + T068 + O326 | COMPLETE |
| `E2` Stage 5 package materialization | REQ-T068-1..4,7 | packager/validator + tests + qualification corpus | COMPLETE |
| `E3` Stage 6 technical verification | E2 candidate | Executor verification + `handoffs/T068-executor-handoff.json` | AUTHORIZED |
| `E4` Human ChatGPT installation gate | REQ-T068-5 | six upload/scan/install outcomes tied to accepted candidate provenance | NOT_STARTED |
| `E5` ChatGPT behavioral qualification | REQ-T068-6; P1..P3,P6 | observable explicit/auto/anti-trigger/composition results | NOT_STARTED |
| `E6` Stage 7 convergence | all | acceptance/integration/closure records | NOT_STARTED |

## Execution geometry

`Execution Shape: MULTI_EXECUTION` because later work depends on an external Human/workspace installation gate and post-install host state.

Ordered units:

1. **Execution 1 — E1 + E2:** COMPLETE.
2. **Execution 2 — E3:** next; Executor technical verification.
3. **Human gate — E4:** install/upload accepted bundles in ChatGPT.
4. **Execution 3 — E5:** ChatGPT behavioral qualification after confirmed installation.
5. **Execution 4 — E6:** Stage 7 convergence/integration/closure.

Each later unit must verify all preceding durable gates. This decomposition has no wall-clock/minute/provider-session semantics.

## Stage ownership

```text
Stages 1-4 -> ChatGPT Orchestrator
Stage 5    -> ChatGPT Orchestrator
Stage 6    -> Agente de IA Ejecutor
Human gate -> Human Owner / authorized workspace actor
Stage 7    -> ChatGPT Orchestrator
```

Post-install behavioral qualification is Orchestrator-owned semantic/eval work because it determines the accepted host-activation claim.

## Stage 5 published candidate freeze

Stage 5 material candidate content is frozen at:

```text
candidate_branch:         feat/t068-chatgpt-skill-host-activation
candidate_base:           5bed8b952a3c552e3af0abfdbe07895864319696
candidate_content_anchor: 9707b41a1e0ac7f64c776318ca557bd3ceca263f
```

`candidate_content_anchor` is deliberately the last commit containing material E2 executable/eval content. Subsequent commits may only publish this Task Contract freeze and the Orchestrator checkpoint/launch routing. The Executor launch transport must carry the exact current remote branch HEAD after those metadata-only commits and must verify that the delta from `candidate_content_anchor` contains only the authorized freeze/checkpoint Markdown.

If any executable, test, eval corpus, Skill source, research conclusion or other material candidate surface changes after `candidate_content_anchor`, E3 authority is invalid until ChatGPT Orchestrator re-enters Stage 5 and publishes a new content anchor.

## Stage 5 materialized surfaces

- `tools/chatgpt_skill_package.py`
- `tests/test_chatgpt_skill_package.py`
- `tests/test_chatgpt_skill_package_safety.py`
- `tests/test_t068_chatgpt_skill_qualification.py`
- `evals/t068_chatgpt_skill_host/qualification-corpus.json`
- `docs/research/R031-CHATGPT-SKILL-HOST-MATERIALIZATION.md`
- `docs/RESEARCH-TRACEABILITY.md`
- this Task Contract and the T068 Orchestrator checkpoint

The Orchestrator sandbox could not execute the remote branch because its local execution environment had no DNS/network path to GitHub. That failed clone is not verification evidence and does not weaken E3. Stage 6 remains the required technical execution/review gate.

## Authorized Stage 6 scope

The Executor may:

- establish an isolated writable T068 workspace from the exact launch HEAD;
- verify base/branch/content-anchor identity and the metadata-only post-anchor delta;
- run the packager in validate and build modes using the exact launch HEAD as `source_revision` provenance input;
- inspect generated six ZIPs and manifest;
- run focused T068 tests, relevant reference-integrity/Skill tests, Ruff, code-health and the normal full repository test suite;
- review path traversal, archive safety, reproducibility, output preservation, source-to-package byte identity, relative resources, topology and generated-artifact hygiene;
- make bounded technical repairs to Stage 5 executable/test mechanics only when they do not alter Skill semantics, topology, acceptance meaning, R031 conclusions, the qualification corpus's semantic expectations, or committed Markdown;
- persist `handoffs/T068-executor-handoff.json`, commit/push the authorized state, and return the exact remote branch HEAD.

If a repair changes any Stage 5 executable/test file, the Executor must clearly identify it in the handoff. ChatGPT will determine whether the repair remains bounded or requires Stage 5 re-entry before acceptance.

## Explicit exclusions

Do not:

- change D082 topology;
- create top-level `workspace-isolation`;
- rewrite any canonical Skill semantics merely to satisfy ChatGPT packaging;
- edit committed Markdown during Stage 6;
- edit the qualification corpus semantic expectations during Stage 6;
- create a host-specific competing authority plane;
- infer installation from packaging;
- infer auto-routing from explicit `@` invocation alone;
- require/expose hidden reasoning;
- start/modify T066;
- relabel empirical parity;
- edit unrelated product surfaces.

## Invariants / constraints

- OpenAI host evidence baseline: `2026-09-14`.
- Current official eligibility statement: eligible ChatGPT Business, Enterprise, Healthcare and Edu users, subject to workspace/product controls.
- Account-specific entitlement and upload permissions are Human/host gates, not repository assumptions.
- OpenAI scan outcomes are authoritative observations for E4.
- Generated bundles must be reproducible and regenerable.
- Generated ZIPs/manifest are verification/distribution outputs and need not be committed unless later authority explicitly changes that disposition.

## D076 boundary

All substantial packaging controllers, validators, fixtures and semantic qualification assets required for first-pass verification exist by the end of E2. Discovery in E3 of a material missing executable artifact requires Stage 5 re-entry.

## Acceptance criteria

- **AC-T068-1:** exactly six canonical ChatGPT Skill packages are reproducibly materializable.
- **AC-T068-2:** every package includes root `SKILL.md` plus required Skill-local resources with source-identical bytes.
- **AC-T068-3:** deterministic validation detects topology/resource/name/provenance/path/output violations including top-level `workspace-isolation`.
- **AC-T068-4:** package contents preserve canonical Skill semantics without a host-specific semantic fork.
- **AC-T068-5:** Stage 6 verification passes with no unresolved material review item.
- **AC-T068-6:** all six Skills reach a recorded usable installed state, or T068 remains explicitly blocked/partial.
- **AC-T068-7:** post-install qualification demonstrates explicit availability and bounded positive/negative routing behavior with observable evidence.
- **AC-T068-8:** Maintainer internal routing and transverse composition remain D082-conformant.
- **AC-T068-9:** Git-authority/cold-start/fail-closed independence is preserved.
- **AC-T068-10:** T066 remains untouched; ChatGPT/Codex parity remains `NOT_ESTABLISHED` absent separate authority.

## Stage 6 required verification

At minimum:

1. `python tools/chatgpt_skill_package.py --root . --validate-only`
2. generate packages to a disposable clean directory with `--source-revision <exact launch HEAD>`;
3. run all three T068 test modules;
4. run relevant existing Skill/reference-integrity tests;
5. `ruff check` over changed Python surfaces (and repository-wide if normal project workflow does so);
6. repository code-health checker/tests;
7. full `pytest` suite;
8. inspect manifest and ZIP inventory/digests/source-byte identity;
9. confirm no generated archives/manifests or unrelated files are accidentally tracked;
10. audit D076 material completeness.

## Stop / escalation / SDD re-entry

STOP rather than guess when:

- base/branch/content-anchor/launch-HEAD identity is unsafe or ambiguous;
- the post-anchor delta is not metadata-only freeze/checkpoint Markdown;
- OpenAI materially changes the Skills contract relied on by R031;
- ChatGPT requires an incompatible package structure;
- a Skill-local dependency cannot be represented without semantic change;
- required host entitlement/permission is unavailable;
- scan blocks a Skill for a reason requiring source semantic change;
- routing cannot be scored observably without inventing hidden telemetry;
- Stage 6 discovers a D076-material missing artifact;
- T066 or unrelated scope would need to be touched.

## Version-sensitive gate

- Reference evidence: OpenAI Skills/Plugins documentation reviewed `2026-09-14` in R031.
- Current disposition: `NO_MATERIAL_CHANGE` at Stage 5 freeze.
- Before E4/E5, refresh official OpenAI Skills documentation when material host drift is observed or freshness is insufficient for consequential qualification.

## Expected handoff

```text
handoffs/T068-executor-handoff.json
```

It must capture candidate base/content anchor/launch HEAD, branch/worktree identity, Stage 6 repairs, exact commands/results, package manifest evidence, review findings, generated-artifact hygiene, D076 audit, and unresolved issues.

## Executor launch profile

```text
Executor: Codex
Session: NEW
Coordinator-ID: AG | agent-governance | T068 | root-1
Model: GPT-5.6 Sol
Effort: Medium
```

D055 rationale: bounded but consequential technical verification with archive/reproducibility/security review; Medium is the minimum sufficient profile. D060 requires a new task-scoped root because T068 is a new Task Contract.

## Terminal return shape

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T068-executor-handoff.json
BRANCH: feat/t068-chatgpt-skill-host-activation
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

E3 launch state:

```text
launch_state: AUTHORIZED
```

Authorization is conditional on the next Orchestrator checkpoint recording E2 complete / E3 next and on the Human launching the thin transport against the exact then-current remote branch HEAD. E4 remains a distinct Human/workspace gate and cannot be consumed by Executor completion.

## Thin transport invariant

The Executor prompt carries only coordinator/session/bootstrap identity, canonical repository, this Task Contract pointer, candidate content anchor, exact launch HEAD, and current base. Detailed semantics remain in canonical Git.
