# T068 — ChatGPT Skill Host Materialization and Qualification

## Identity

- Task ID: `T068`
- Status: `READY`
- Type: `mixed`
- SDD profile: `STANDARD`
- Base branch: `develop`
- Base SHA at task creation: `5bed8b952a3c552e3af0abfdbe07895864319696`
- Expected topic branch: `feat/t068-chatgpt-skill-host-activation`
- Expected executor handoff: `handoffs/T068-executor-handoff.json`
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
- **REQ-T068-4 — Deterministic validation:** reject missing/extra top-level Skills, missing `SKILL.md`, missing required Skill-local resources, duplicate Skill names, and any top-level promotion of `workspace-isolation`.
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

Stage 5 SHALL materialize a deterministic packager/validator that:

- reads the six canonical Skill source directories;
- resolves Skill identity from each root `SKILL.md`;
- recursively includes Skill-local files;
- validates required internal relative references;
- emits one archive per top-level Skill to generated/untracked output;
- emits a machine-readable manifest with Skill name, source directory, source revision, file inventory and digests;
- normalizes archive metadata sufficiently for reproducible output from identical inputs;
- excludes `.git`, caches, secrets, generated local state and unrelated repository files;
- does not vendor mutable repository authority such as `AGENTS.md`, the current checkpoint or Task Contracts into Skill bundles unless such content is intentionally Skill-local source.

Generated archives are disposable distribution artifacts; canonical Skill directories and packaging code remain authoritative.

### Qualification design

Two evidence planes apply:

1. **Pre-host deterministic conformance:** topology, package completeness, provenance, no sixth Skill, no semantic source rewrite.
2. **Post-install ChatGPT behavioral qualification:** explicit availability, positive auto-routing, negative/near-miss anti-trigger cases, Maintainer Orchestrator/Executor route separation, transverse composition, absence of top-level `workspace-isolation`, and Git-bootstrap/fail-closed behavior.

Score only observable behavior and explicit Skill invocation surfaces. Do not require hidden chain-of-thought or undocumented routing telemetry.

### Installation design

Expected eligible-workspace path:

`Plugins -> Skills -> Create -> Upload from your computer`

Record each bundle outcome as `INSTALLED`, `NEEDS_REVIEW`, `BLOCKED`, `UNAVAILABLE`, or the precise equivalent surfaced by ChatGPT. If the UI rejects the candidate package form, preserve semantics and re-enter only the narrow packaging design needed to satisfy the host.

## Plan & Trace

| Unit | Requirement / Design | Candidate/evidence |
| --- | --- | --- |
| `E1` Research + authority freeze | R031; all REQ/PRESERVED | R031 + T068 + checkpoint |
| `E2` Stage 5 package materialization | REQ-T068-1..4,7 | packager/validator + tests + qualification corpus skeleton |
| `E3` Stage 6 technical verification | E2 candidate | Executor verification + `handoffs/T068-executor-handoff.json` |
| `E4` Human ChatGPT installation gate | REQ-T068-5 | six upload/scan/install outcomes tied to candidate provenance |
| `E5` ChatGPT behavioral qualification | REQ-T068-6; P1..P3,P6 | observable explicit/auto/anti-trigger/composition results |
| `E6` Stage 7 convergence | all | acceptance/integration/closure records |

## Execution geometry

`Execution Shape: MULTI_EXECUTION` because later work depends on an external Human/workspace installation gate and post-install host state.

Ordered units:

1. **Execution 1 — E1 + E2:** research/authority freeze and complete Stage 5 package candidate.
2. **Execution 2 — E3:** Executor technical verification.
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

## Published candidate freeze

Populate immediately before E3 launch:

```text
candidate_branch: feat/t068-chatgpt-skill-host-activation
candidate_head:   <exact published Stage 5 SHA>
candidate_base:   <exact authorized develop SHA>
```

## Authorized scope

Stage 5 may create/modify only packaging, validation, qualification, provenance, test/eval, research, Task Contract and checkpoint artifacts required by T068.

Stage 6 may execute the candidate, diagnose defects, perform bounded technical repairs that do not alter Skill semantics/topology/acceptance, run technical verification, and persist the authorized non-Markdown handoff.

## Explicit exclusions

Do not:

- change D082 topology;
- create top-level `workspace-isolation`;
- rewrite Skill semantics merely to satisfy ChatGPT packaging;
- create a host-specific competing authority plane;
- infer installation from packaging;
- infer auto-routing from explicit `@` invocation alone;
- require/expose hidden reasoning;
- start/modify T066;
- relabel empirical parity;
- edit unrelated product surfaces;
- allow Stage 6 to edit committed Markdown or Orchestrator-owned semantic qualification assets.

## Invariants / constraints

- OpenAI host evidence baseline: `2026-09-14`.
- Current official eligibility statement: eligible ChatGPT Business, Enterprise, Healthcare and Edu users, subject to workspace/product controls.
- Account-specific entitlement and upload permissions are Human/host gates, not repository assumptions.
- OpenAI scan outcomes are authoritative observations for E4.
- Generated bundles must be reproducible and regenerable.

## D076 boundary

All substantial packaging controllers, validators, fixtures and semantic qualification assets required for first-pass verification must exist by the end of E2. Discovery in E3 of a material missing executable artifact requires Stage 5 re-entry.

## Acceptance criteria

- **AC-T068-1:** exactly six canonical ChatGPT Skill packages are reproducibly materializable.
- **AC-T068-2:** every package includes root `SKILL.md` plus required Skill-local resources.
- **AC-T068-3:** deterministic validation detects topology/resource/name/provenance violations including top-level `workspace-isolation`.
- **AC-T068-4:** package contents preserve canonical Skill semantics without host-specific semantic fork.
- **AC-T068-5:** Stage 6 verification passes with no unresolved material review item.
- **AC-T068-6:** all six Skills reach a recorded usable installed state, or T068 remains explicitly blocked/partial.
- **AC-T068-7:** post-install qualification demonstrates explicit availability and bounded positive/negative routing behavior with observable evidence.
- **AC-T068-8:** Maintainer internal routing and transverse composition remain D082-conformant.
- **AC-T068-9:** Git-authority/cold-start/fail-closed independence is preserved.
- **AC-T068-10:** T066 remains untouched; ChatGPT/Codex parity remains `NOT_ESTABLISHED` absent separate authority.

## Verification and trace requirements

Orchestrator-owned conformance assets must cover AC-T068-1..4 and the post-install corpus for AC-T068-6..9.

Stage 6 must execute:

- package topology/resource/provenance tests;
- relevant reference-integrity/Skill tests;
- applicable repository lint/code-health/full tests for changed executable surfaces;
- generated-manifest review from a clean candidate state.

E5 evidence records scenario ID/prompt class, expected visible classification, actual visible outcome, explicit-vs-auto mode, Skill availability and pass/fail disposition. Do not persist hidden reasoning.

## Code Review & Verify obligations

E3 reviews path-traversal/archive safety, reproducibility, accidental inclusion of secrets/local state, source-to-package identity, relative references, topology drift, generated artifact hygiene, and coverage sufficient to detect semantic rewrite/omission.

## Stop / escalation / SDD re-entry

STOP rather than guess when:

- base/branch/candidate identity is unsafe or ambiguous;
- OpenAI materially changes the Skills contract relied on by R031;
- ChatGPT requires an incompatible package structure;
- a Skill-local dependency cannot be represented without semantic change;
- required host entitlement/permission is unavailable;
- scan blocks a Skill for a reason requiring source semantic change;
- routing cannot be scored observably without inventing hidden telemetry;
- Stage 6 discovers a D076-material missing artifact;
- T066 or unrelated scope would need to be touched.

## Version-sensitive launch gate

- Reference evidence: OpenAI Skills/Plugins documentation reviewed `2026-09-14` in R031.
- Current disposition: `NO_MATERIAL_CHANGE` from the reviewed evidence baseline.
- Before E4/E5, refresh official OpenAI Skills documentation when material host drift is observed or freshness is insufficient for consequential qualification.

## Expected handoff

Stage 6 result:

```text
handoffs/T068-executor-handoff.json
```

It must capture candidate/base/branch identity, Stage 6 repairs, package/test/review results, generated-manifest evidence and D076 artifact audit.

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
launch_state: NOT_AUTHORIZED
```

E3 becomes launchable only after E2 is complete, reviewed and frozen at an exact remote head. E4 remains a distinct Human/workspace gate and cannot be consumed by Executor completion.

## Thin transport invariant

Any later Executor prompt carries only coordinator/session/bootstrap identity, canonical repository, this Task Contract pointer and exact candidate identity. Detailed semantics remain in canonical Git.
