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
- Owner: `ChatGPT Orchestrator (specification/Design/Plan/Stage 5/acceptance) / Agente de IA Ejecutor (authorized Stage 6 verification/repair) / Human Owner (final authority and ChatGPT workspace installation gate)`
- ChatGPT Effort: `MEDIUM`
- Execution Shape: `MULTI_EXECUTION`

## Objective

Materialize the already-adopted R029/D082 Agent Governance Skill architecture as reproducible ChatGPT-loadable Skill bundles without semantic forking, cross the explicit Human/workspace installation gate, and qualify observable ChatGPT activation/routing behavior before claiming host activation.

T068 does not reopen D082 architecture or T067 acceptance and does not start or modify T066.

## Current specification carrier / controlling references

Load only the smallest authoritative set needed for the active unit:

- `AGENTS.md`
- `docs/research/R030-CHATGPT-SKILL-HOST-MATERIALIZATION.md`
- `docs/decisions/D082-r029-lean-root-and-transverse-skill-architecture.md`
- `maintainer-skill/SKILL.md`
- `repository-change-control-skill/SKILL.md`
- `upstream-version-revalidation-skill/SKILL.md`
- `research-evidence-traceability-skill/SKILL.md`
- `durable-work-checkpoint-skill/SKILL.md`
- `executor-launch-handoff-skill/SKILL.md`
- `docs/TASK-CONTRACTS.md`
- `docs/ORCHESTRATOR-CHECKPOINTS.md`

Current upstream evidence is recorded in R030. OpenAI host behavior is version-sensitive; refresh consequential claims if materially changed before the installation/qualification gate.

## Requirement / specification delta

### ADDED

- **REQ-T068-1 — Deterministic ChatGPT Skill packaging.** The repository SHALL provide a reproducible way to materialize exactly six top-level ChatGPT Skill bundles from the adopted source directories:
  1. `source-maintainer` from `maintainer-skill/`;
  2. `repository-change-control`;
  3. `upstream-version-revalidation`;
  4. `research-evidence-traceability`;
  5. `durable-work-checkpoint`;
  6. `executor-launch-handoff`.
- **REQ-T068-2 — Complete relative resources.** Each bundle SHALL include its root `SKILL.md` and all required Skill-local references/resources while preserving relative paths.
- **REQ-T068-3 — Provenance.** Package generation SHALL be traceable to a canonical Git source revision and SHALL NOT make generated host artifacts a competing normative authority.
- **REQ-T068-4 — Deterministic topology validation.** Pre-upload checks SHALL reject a missing/extra top-level Skill, missing `SKILL.md`, missing required referenced resource, duplicate Skill name, or promotion of `workspace-isolation` to a sixth transverse/top-level Skill.
- **REQ-T068-5 — Human ChatGPT installation gate.** Host installation/upload is an explicit Human/workspace action. T068 SHALL distinguish `PACKAGED` from `INSTALLED` and fail closed if the ChatGPT Skills surface, upload permission, scan, or installation is unavailable/blocked.
- **REQ-T068-6 — Post-install ChatGPT qualification.** Observable ChatGPT behavior SHALL be qualified after installation; repository materialization alone cannot satisfy this requirement.
- **REQ-T068-7 — No semantic host fork.** ChatGPT adaptation SHALL be limited to packaging, provenance, narrow host adapters, and qualification assets unless a later durable design re-entry explicitly authorizes semantic changes.

### PRESERVED

- **REQ-T068-P1 — D082 topology.** One Maintainer domain Skill with two internal routes; exactly five transverse Skills; `workspace-isolation` subordinate under `executor-launch-handoff`.
- **REQ-T068-P2 — Git authority.** Canonical Git state remains authoritative over installed Skill snapshots/host state.
- **REQ-T068-P3 — Skill-independent safety.** Authority, ownership, cold-start and fail-closed correctness remain valid when Skills are absent/disabled.
- **REQ-T068-P4 — Role ownership.** ChatGPT Orchestrator retains specification/Design/Plan/semantic-oracle/Stage 5/Stage 7 ownership; Executor remains Stage 6 only.
- **REQ-T068-P5 — T066 isolation.** T066 remains untouched and unstarted.
- **REQ-T068-P6 — Empirical claim boundary.** ChatGPT/Codex parity remains `NOT_ESTABLISHED` unless separately authorized and demonstrated.

## Controlling Design

### Host architecture

```text
canonical Git source Skill directories
    -> deterministic package/validation layer
    -> six independent ChatGPT Skill bundles
    -> Human/workspace upload + OpenAI scan
    -> installed ChatGPT Skill set
    -> explicit + automatic-routing qualification
```

The ChatGPT host SHALL consume the same six D082 top-level semantic Skill boundaries. Do not create ChatGPT-specific semantic clones or combine them into one mega-Skill merely for convenience.

`source-maintainer` retains internal Orchestrator/Executor routes. `workspace-isolation` remains a reference/internal route under `executor-launch-handoff` and is never emitted as a top-level upload bundle.

### Packaging design

Stage 5 SHALL materialize a deterministic repository-owned packager/validator that:

- reads the six canonical Skill source directories;
- resolves the root Skill name from each `SKILL.md` front matter;
- recursively includes Skill-local files required for that package;
- validates internal relative references that are required to exist in-bundle;
- emits one archive per top-level Skill into a generated/untracked output location;
- emits a machine-readable manifest containing bundle name, source directory, source revision supplied/detected by the packaging invocation, file inventory, and content digest(s);
- produces byte-stable output when the same source tree, metadata inputs and tool version are used, to the extent practical for ZIP metadata normalization;
- does not vendor `AGENTS.md`, the current checkpoint, mutable Task Contracts, or other canonical repository authority into the Skill bundle unless a Skill-local resource is intentionally part of that source directory.

Generated archives are distribution artifacts, not canonical policy; the source directories and packaging code remain authoritative.

### Qualification design

Qualification has two planes:

1. **Deterministic pre-host conformance** — repository tests validate topology, package completeness, provenance manifest, forbidden sixth Skill, and semantic source identity/no rewritten Skill prose.
2. **Post-install ChatGPT behavioral qualification** — after the Human confirms installation, run a bounded corpus that records observable outcomes for:
   - explicit availability/invocation of each of six Skills;
   - positive auto-routing examples for each Skill;
   - negative/near-miss anti-trigger examples for each Skill;
   - Maintainer Orchestrator-route selection on source-planning work;
   - Maintainer Executor-route non-selection when ChatGPT Orchestrator owns the stage;
   - transverse composition on representative multi-capability source-maintenance cases;
   - absence of top-level `workspace-isolation`;
   - preservation of Git-bootstrap/fail-closed behavior.

Do not require hidden chain-of-thought or undocumented internal routing telemetry. Score only user-visible behavior, explicit Skill invocation surfaces when available, and durable test observations.

### Installation design

The Human installation gate is external to Git execution. The normal expected path on an eligible ChatGPT workspace is:

`Plugins -> Skills -> Create -> Upload from your computer`.

Upload/scan result for each bundle SHALL be recorded as `INSTALLED`, `NEEDS_REVIEW`, `BLOCKED`, or `UNAVAILABLE` (or a precise equivalent surfaced by ChatGPT). If archive upload form is rejected, do not silently rewrite the Skill semantics; record the host packaging incompatibility and re-enter Design/Stage 5 only for the narrow packaging adapter.

## Plan & Trace

| Unit | Requirement / Design ref | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| `E1` Research/authority freeze | R030; REQ-T068-* | R030 + this Task Contract + checkpoint | current OpenAI evidence, D082 preservation, Human objective recorded |
| `E2` Stage 5 package materialization | REQ-T068-1..4,7; P1..P4 | deterministic packager/validator, package manifest schema/output rules, tests, any narrow docs | deterministic tests prove six bundles, resources, provenance, no sixth Skill/no semantic rewrite |
| `E3` Stage 6 technical verification | E2 published candidate | candidate code/tests + `handoffs/T068-executor-handoff.json` | Executor runs/reviews candidate; bounded technical repair only; full relevant repo verification |
| `E4` Human ChatGPT installation gate | REQ-T068-5 | generated bundle set from accepted candidate | six host upload/scan/install outcomes; exact source/candidate provenance |
| `E5` ChatGPT behavioral qualification | REQ-T068-6; P1..P3,P6 | Orchestrator-owned qualification corpus/results | explicit/automatic/anti-trigger/composition results; no hidden-internal claims |
| `E6` Stage 7 convergence | all | acceptance/review/checkpoint/integration | Orchestrator accepts/rejects host activation and integrates only supported claims |

## Execution geometry

`Execution Shape: MULTI_EXECUTION` is mandatory for this objective because later work depends on an external Human/workspace installation gate and post-install host state.

Ordered execution units:

1. **Execution 1 — E1 + E2:** freeze host research/contract and materialize the complete deterministic package candidate.
2. **Execution 2 — E3:** Executor technical verification of the published Stage 5 candidate.
3. **Human gate — E4:** install/upload the accepted bundles in ChatGPT; no ChatGPT execution-shape label applies to this Human-only gate.
4. **Execution 3 — E5:** ChatGPT host behavioral qualification after confirmed installation.
5. **Execution 4 — E6:** Stage 7 semantic convergence/integration/closure.

A later execution MUST verify all preceding durable gates before proceeding. No wall-clock/minute/provider-session assumptions are part of this decomposition.

## Stage ownership and candidate boundary

```text
Stages 1-4  Explore / Specify / Design / Plan & Trace
            -> ChatGPT Orchestrator
Stage 5     Complete candidate materialization
            -> ChatGPT Orchestrator
Stage 6     Execute / diagnose / bounded repair / verify
            -> Agente de IA Ejecutor
Human gate  ChatGPT workspace upload/install
            -> Human Owner / authorized workspace actor
Stage 7     Converge / accept / integrate / evolve
            -> ChatGPT Orchestrator
```

Post-install behavioral qualification is an Orchestrator-owned semantic/eval activity because it determines whether ChatGPT host activation claims are accepted; it must not be delegated as if it were merely technical Stage 6 execution.

## Published candidate freeze

Populate immediately before E3 launch:

```text
candidate_branch: feat/t068-chatgpt-skill-host-activation
candidate_head:   <exact published candidate SHA>
candidate_base:   5bed8b952a3c552e3af0abfdbe07895864319696 or refreshed authorized base after revalidation
```

## Authorized scope

During Stage 5 the Orchestrator may create/modify only the artifacts required to package, validate, document, trace and qualify the six existing Skills, including deterministic scripts/tests/evals/manifests and this task's research/checkpoint/contract records.

During Stage 6 the Executor may:

- execute the published candidate;
- diagnose packaging/validator/test defects inside this Design;
- make bounded technical repairs that do not alter Skill semantics, topology, acceptance meaning or Orchestrator-owned qualification expectations;
- persist the authorized non-Markdown handoff/evidence.

## Explicit exclusions

Do not:

- change the D082 six-Skill topology or create a top-level `workspace-isolation` Skill;
- rewrite Skill semantics merely to satisfy ChatGPT packaging without Orchestrator Design re-entry;
- vendor mutable repository authority into installed bundles as a competing authority plane;
- claim ChatGPT installation from successful packaging alone;
- claim automatic routing from explicit `@` invocation alone;
- require or expose hidden chain-of-thought;
- start/modify T066;
- relabel ChatGPT/Codex parity;
- edit unrelated product surfaces;
- allow Executor Stage 6 to modify committed Markdown or Orchestrator-owned semantic qualification assets.

## Invariants / constraints

- Current upstream host evidence date: `2026-09-14`; revalidate if OpenAI Skills behavior materially changes before E4/E5.
- Current official eligibility statement: eligible ChatGPT Business, Enterprise, Healthcare and Edu users, subject to workspace/product controls. Account-specific entitlement is a Human gate, not a repository assumption.
- ChatGPT upload scanning/Needs Review/Blocked outcomes are authoritative host observations for E4.
- Git remains the source of truth for semantics and current maintenance frontier.
- Generated package artifacts must be reproducible and disposable/regenerable.

## Executor process autonomy

Inside E3, the Executor owns technical mechanics and private execution organization under D041/D054. It must not alter the approved host architecture, Skill boundaries, semantic oracle, or installation/qualification meaning.

## D076 executable-materialization boundary

All substantial packaging controllers, validators, fixtures and semantic qualification assets required for first-pass verification must exist by the end of E2/Stage 5. Discovery in E3 that a substantial new controller/harness/oracle is needed is an Orchestrator Stage 5 re-entry condition.

## Acceptance criteria

- **AC-T068-1:** Exactly six canonical top-level ChatGPT Skill packages are reproducibly materializable from the D082 source directories.
- **AC-T068-2:** Every package contains its root `SKILL.md` and required Skill-local resources with valid relative references.
- **AC-T068-3:** Deterministic validation rejects topology drift, missing resources, duplicate names and top-level `workspace-isolation`.
- **AC-T068-4:** Packaging/provenance does not rewrite or duplicate canonical Skill semantics into a host-specific fork.
- **AC-T068-5:** Stage 6 verification passes against the published candidate with no unresolved material review item.
- **AC-T068-6:** The Human installation gate records a usable installed state for all six Skills, or T068 remains explicitly blocked/partial without overstating host activation.
- **AC-T068-7:** Post-install qualification demonstrates explicit availability plus bounded positive/negative routing behavior for the installed Skills using observable evidence.
- **AC-T068-8:** Maintainer internal role routing and transverse composition remain consistent with D082; `workspace-isolation` is not exposed as a top-level Skill.
- **AC-T068-9:** Git-authority/cold-start/fail-closed independence is preserved.
- **AC-T068-10:** T066 remains untouched and ChatGPT/Codex parity remains `NOT_ESTABLISHED` unless separately authorized.

## Verification and trace requirements

Orchestrator-owned conformance assets SHALL include deterministic assertions for AC-T068-1..4 and the post-install ChatGPT qualification corpus for AC-T068-6..9.

Stage 6 SHALL run at minimum:

- package topology/resource/provenance tests;
- relevant repository reference-integrity and Skill tests;
- the repository's normal code-health/lint/test surface applicable to changed executable files;
- review of generated package manifests from a clean candidate state.

E5 SHALL persist a bounded machine-readable or Markdown-adjacent evidence record that records only observable prompts/scenario IDs, expected classification, actual visible outcome, explicit invocation/auto-routing mode, Skill availability and pass/fail disposition. Do not store hidden reasoning.

## Code Review & Verify obligations

E3 must review for:

- path traversal/archive safety;
- deterministic/reproducible archive metadata;
- accidental inclusion of secrets, `.git`, local caches, generated state or unrelated repository files;
- source-to-package identity;
- broken relative references;
- topology drift;
- generated artifact hygiene;
- tests sufficient to detect semantic source rewrite or omitted resources.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when:

- current base/branch identity cannot be established safely;
- OpenAI materially changes the Skills host contract relied upon here;
- ChatGPT requires a packaging structure incompatible with this Design;
- a Skill-local reference cannot be represented without changing semantics;
- a required host entitlement/permission is unavailable;
- upload scan blocks a Skill for a reason requiring source semantic change;
- automatic-routing qualification cannot be scored from observable behavior without inventing hidden telemetry;
- a D076-material executable artifact is discovered missing in Stage 6;
- T066 or unrelated scope would need to be touched.

## Version-sensitive launch gate

- reference evidence: OpenAI Skills/Plugins documentation reviewed `2026-09-14`
- disposition at task creation: `NO_MATERIAL_CHANGE` relative to R030 current evidence
- launch-time rule: before E4/E5, refresh official OpenAI Skills documentation if the surface/behavior appears changed or material time/version drift makes the relied-on claims stale; persist any consequential delta before qualification.

## Expected handoff / evidence

Stage 6 result:

```text
handoffs/T068-executor-handoff.json
```

The handoff must capture candidate/base/branch identity, Stage 6 repairs, package/test results, review findings, generated-manifest evidence, and D076 artifact audit.

Post-install host evidence is separate Orchestrator/Human-gate evidence and must not be fabricated into the Executor handoff before installation occurs.

## Terminal return shape

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T068-executor-handoff.json
BRANCH: feat/t068-chatgpt-skill-host-activation
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

For E3:

```text
launch_state: NOT_AUTHORIZED
```

E3 is not launchable until E2 Stage 5 candidate materialization is complete, reviewed and frozen at an exact remote head.

E4 is a distinct Human ChatGPT workspace installation gate and cannot be consumed by Executor completion.

## Thin transport invariant

Any later Executor prompt must contain only coordinator/session/bootstrap identity, canonical repository, this Task Contract pointer and exact authorized candidate identity. Detailed task semantics remain here.
