# Portable Agent Governance

Protocol-Version: 1.15.0

## Purpose

Provide the small, always-loaded entrypoint for deterministic collaboration between the Human Owner, Strategy/Governance Agent, and Implementation Agent. Agent products are adapters to these roles; detailed rules live in focused Core modules loaded only when relevant.

Agent Governance also acts as a bidirectional proxy between Human Owner intent and implementation-grade engineering: communication adapts to the Human Owner's current technical register while engineering rigor remains invariant. Detailed interaction and quality rules are progressively loaded from `INTERACTION.md` and `QUALITY.md`.

Native Spec-Driven Development is a built-in Governance capability. `SDD.md` defines the tool-neutral, spec-anchored, delta-first method and the single-owner stage model. Existing project-native SDD/specification systems may be reused/adapted through `COEXISTENCE.md`, but absence of an external SDD provider never removes SDD discipline.

Material security is governed by current/versioned authority, freshness, known-bad state, independent verification, bounded Human exceptions and temporal posture invalidation from `SECURITY.md`. Model output is never security authority, and historical task acceptance does not imply permanent current security posture.

Existing-system assurance is governed by explicit scope/authorization, evidence provenance, coverage accounting, bounded finding states, severity/confidence separation and temporal posture from `ASSURANCE.md`. Model opinion, missing evidence, scanner/tool success and historical reports do not become assurance authority.

Material local/remote/system execution is governed by effect- and target-oriented authorization plus runbook-first terminal-neutral procedure semantics and Executor-owned adapter-operation resolution from `EXECUTION-CONTROL.md`. Availability of a terminal, credential, CLI, API, remote connection, privileged identity or cached operation recipe never creates Governance authority by itself.

## Bootstrap Invariant

On cold start load only:
1. `.agent-coordination/STATE.json`;
2. this file;
3. the repository-native adapter when the product loads it automatically.

Then perform a lightweight EXCHANGE freshness probe: determine the latest event `q` without loading full history when tooling permits. If latest `q > STATE.exchange_q`, load only that delta before deciding the effective frontier.

Do NOT preload MISSION, WORKPLAN, all task records, Decision Records, Core modules, Skill audit records, ecosystem inventories, runbook/recipe registries, SDD histories/workspaces, or full EXCHANGE history. Route context on a need-to-know basis.

## Authority

Highest authority wins:
1. explicit Human Owner instruction;
2. Governance Core (`GOVERNANCE.md` plus applicable modules, including `SDD.md` when development work is governed);
3. `.agent-coordination/MISSION.md`;
4. `.agent-coordination/WORKPLAN.md` and the currently disclosed task record;
5. accepted decisions/events in EXCHANGE and controlling Decision Records;
6. Implementation Agent local technical decisions inside approved scope and Design;
7. approved Skills and other technical guidance.

`STATE.json` is derived and never authoritative. Skills provide expertise, not authority. Existing SDD/specification artifacts become controlling for a scope only when Strategy/Human authority binds them by reference from the applicable mission/decision/task contract; they do not create a parallel Governance authority tier.

## Roles

- **Human Owner** — final authority over scope, priorities, risk, pause/resume and overrides.
- **Strategy/Governance Agent** — owns native SDD Explore/Frame, Specify, Design, Plan & Trace, and Converge/Accept/Evolve; F0-F6 strategy; Human-intent/engineering translation; ecosystem/capability boundary decisions; implicit quality review; Skill discovery/audit/approval; graphical solution presentation; work decomposition; task-contract correctness/completeness; readiness; acceptance/rejection; strategic blockers; and durable checkpoint maintenance.
- **Implementation Agent** — owns native SDD Implement plus Code Review & Verify for authorized technical work inside the execution sequence and applicable execution-capability envelope, including adapter/CLI/API/SDK/shell mechanics and bounded operation resolution, regardless of whether the product is OpenCode, Codex, Claude Code, Antigravity or another compatible agent.

No SDD stage is dual-owned. Implementation-local coding choices are not a second Design authority. If implementation/review exposes a material requirement, Design, Plan or acceptance defect, Implementation blocks and returns that concern to Strategy for re-entry under `SDD.md`.

Product identity MUST NOT appear in task semantics. See `ADAPTERS.md`.

## Source Map

- collaboration/router -> `.agent-governance/GOVERNANCE.md`
- native Spec-Driven Development stages/spec delta/trace/convergence -> `.agent-governance/SDD.md`
- adaptive Human-intent/technical interaction -> `.agent-governance/INTERACTION.md`
- implicit engineering quality + graphical design readiness -> `.agent-governance/QUALITY.md`
- material security authority/freshness/verification/posture -> `.agent-governance/SECURITY.md`
- existing-system assurance scope/evidence/findings/coverage/posture -> `.agent-governance/ASSURANCE.md`
- context loading/budgets -> `.agent-governance/CONTEXT.md`
- agent-product mapping -> `.agent-governance/ADAPTERS.md`
- pre-implementation F0-F6/task contract quality -> `.agent-governance/LIFECYCLE.md`
- ecosystem/SDD/Skill/tool coexistence -> `.agent-governance/COEXISTENCE.md`
- sequential implementation/review/readiness/blockers -> `.agent-governance/EXECUTION.md`
- material execution authorization + runbook/adapter/verified-recipe semantics -> `.agent-governance/EXECUTION-CONTROL.md`
- STATE/EXCHANGE/Decision Records/versioning + native runbook/recipe persistence -> `.agent-governance/PROTOCOL.md`
- handoff/cold-start recovery -> `.agent-governance/HANDOFF.md`
- Skill capability governance -> `.agent-governance/SKILLS.md`
- Skill candidate discovery/source resolution -> `.agent-governance/SKILL-DISCOVERY.md`
- external Skill provenance/audit/install gate -> `.agent-governance/SKILL-SUPPLY-CHAIN.md`
- mission objective/scope -> `.agent-coordination/MISSION.md`
- work frontier/order/dependencies -> `.agent-coordination/WORKPLAN.md`
- task detail -> `.agent-coordination/tasks/<TASK-ID>.md`
- approved Skill artifact record -> `.agent-coordination/skills/<SKILL-ID>.json`
- Governance-owned semantic runbooks -> `.agent-coordination/runbooks/<runbook-id>.md`
- Governance-owned verified operation recipes -> `.agent-coordination/runbooks/recipes/<recipe-id>.json`
- durable current frontier -> `.agent-coordination/STATE.json`
- durable coordination delta -> `.agent-coordination/EXCHANGE.jsonl`
- rationale-bearing decisions -> `.agent-coordination/decisions/<DECISION-ID>-*.md`
- implementation -> repository code and Git history

## Context Router

| Situation | Load |
| --- | --- |
| Any cold start | STATE + GOVERNANCE + EXCHANGE freshness probe/delta if needed |
| Human-facing intent/response where register, abstraction or modality matters | INTERACTION + only the current request/domain context needed for translation |
| Explicit current focus | only files listed in `STATE.context`, plus a controlling Decision Record only when needed |
| Configure another agent product | ADAPTERS + product-native adapter/configuration |
| Bootstrap/adopt Governance where existing SDD/Skills/tooling may overlap | COEXISTENCE + only relevant project-native capability evidence; load SDD only when development-method ownership must be resolved |
| F0/F1 framing or viability | LIFECYCLE + SDD + MISSION; add INTERACTION when intent translation is non-trivial; add COEXISTENCE only when an existing methodology/capability boundary affects the frame |
| F2 engineering strategy | LIFECYCLE + SDD + QUALITY + MISSION + only relevant Decision Records; add SECURITY when security is material; add COEXISTENCE when selecting/reusing capability providers; add EXECUTION-CONTROL when material local/remote/system effects, privilege, credentials, deployment, persistent-data mutation or destructive/recovery-sensitive operations are part of the solution; add INTERACTION when presenting material tradeoffs/diagram at the Human Owner's register |
| F3 capability audit | LIFECYCLE + SKILLS + WORKPLAN index; add COEXISTENCE for existing Skill/registry overlap, SKILL-DISCOVERY only while locating/resolving candidates and SKILL-SUPPLY-CHAIN only while auditing/acquiring them |
| F4/F5 planning/readiness | LIFECYCLE + SDD + QUALITY + WORKPLAN + only affected task files + relevant Decision Records/Skill approval records; add SECURITY for security-material tasks; add EXECUTION-CONTROL for tasks with material execution effects/runbook/Human-gate requirements; add INTERACTION for Human-facing solution presentation; add only referenced native SDD artifacts needed to validate the current plan/task |
| Existing-system assurance/audit framing or evidence review | ASSURANCE + QUALITY + only declared subject/scope/evidence context; add SECURITY for security-material claims and EXECUTION-CONTROL only when the selected assessment method has material system effects or authorization/runbook requirements |
| Implementation sequence | EXECUTION + SDD + WORKPLAN metadata + current task only + its exact referenced native artifacts + exact required approved Skill artifacts; add SECURITY only when the disclosed task has material security controls/evidence; add EXECUTION-CONTROL only when the disclosed task/effect requires it; load only the selected runbook and compatible VERIFIED recipe for the active operation when applicable |
| Implementation blocker/state transition | EXECUTION + SDD + current task; add SECURITY for security-source freshness/known-bad/verifier/exception/posture blockers; add EXECUTION-CONTROL for authorization/target/runbook/recipe/adapter/recovery blockers; PROTOCOL only if event/state/persistence semantics are needed; COEXISTENCE only for a genuine provider/authority collision; QUALITY only if the blocker invalidates a material quality/design assumption |
| Handoff/review | HANDOFF + SDD + EXCHANGE delta after checkpoint + referenced evidence only; add SECURITY when reviewing material security evidence/posture; add ASSURANCE when reviewing an assurance report/finding/coverage claim; add EXECUTION-CONTROL when reviewing material execution/runbook/recipe evidence |
| STATE repair or protocol question | PROTOCOL + minimum authority records needed for disputed fields |
| Skill discovery/source question | SKILLS + SKILL-DISCOVERY + minimum capability context |
| Skill acquisition/update/revocation | SKILLS + SKILL-SUPPLY-CHAIN + candidate/approval record only |
| SDD/Skill/tool collision or shared managed-file question | COEXISTENCE + SDD + only the conflicting artifacts/configuration |
| Security/privacy/reliability/operability/quality question | QUALITY + only the affected design/task/evidence context; add SECURITY when security is material; add ASSURANCE when the question is an existing-system assessment claim; add EXECUTION-CONTROL when the concern involves system execution authority/procedure |

Do not recursively load unrelated files, whole SDD histories, full Skill registries, full runbook/recipe registries, or future task contents.

## Mandatory Lifecycle

Every new implementation scope follows `LIFECYCLE.md` and `SDD.md`. Strategy is responsible for producing a complete execution contract before F5: current specification carrier where applicable, proportionate SDD profile, requirement/spec delta, controlling Design, atomic Plan/Trace, acceptance and verification obligations. The Implementation Agent must not be expected to reconstruct missing requirements, Design, Plan or hidden strategic intent.

Existing SDD/specification systems may supply project-native requirements/design/plan/task artifacts when they satisfy the lifecycle contract and can be mapped to the single-owner stage model. Governance validates/adapts those artifacts rather than duplicating them under `COEXISTENCE.md`. When no adequate project-native SDD provider exists, native `SDD.md` supplies the method; Governance does not install an external framework merely to obtain SDD.

Before F5 passes, Strategy also applies the implicit engineering quality envelope in `QUALITY.md` and presents the Primary Solution Diagram at the Human Owner's current interaction register under `INTERACTION.md`. Presentation complexity may vary; engineering quality may not.

When security is material under `QUALITY.md`, F5 additionally applies `SECURITY.md`: applicable authoritative controls and source freshness must be determinable, relevant known-bad state must be resolved, required independent verification must be defined, and any Human exception or temporal recheck/invalidation condition must be explicit. Security requirements exist before implementation; verifier success cannot compensate for missing security authority/applicability.

When the implementation scope includes material execution effects governed by `EXECUTION-CONTROL.md`, F5 additionally requires a determinable Execution Capability Envelope, explicit approval/Human-gate semantics, actual-target verification, and any required reusable/project-native runbook with preconditions, postconditions and recovery evidence. A runbook defines procedure but does not authorize a particular invocation. Exact adapter syntax need not be pre-authored by Strategy when Implementation can resolve it safely inside the approved semantic envelope.

F5 authorizes the complete SDD-anchored plan and F6 opens the execution sequence. Implementation then works task-by-task under `EXECUTION.md`, performing Implement and Code Review & Verify for each task, until all authorized tasks are DONE or a valid cross-responsibility/execution-control/security blocker stops the sequence. `DONE` is implementation/review evidence only. Strategy performs Converge/Accept/Evolve after handoff; general task readiness does not silently authorize production, privilege, credentials, global configuration, destructive effects or any target outside the applicable Execution Capability Envelope, and execution authorization does not establish security acceptance.

Existing-system assurance does not bypass the implementation lifecycle or create remediation authority. `ASSURANCE.md` governs assessment scope/evidence/findings; any resulting remediation is separately framed and authorized through the normal lifecycle, native SDD and execution-control planes.

## Core Invariants

- Persist decisions that affect future work before context switch/handoff.
- Communicate deltas, not repeated history.
- Native SDD applies proportionately to every governed development change; lack of an external SDD provider does not disable it.
- Use one accountable owner per SDD stage: Strategy owns Explore/Specify/Design/Plan/Converge; Implementation owns technical Implement/Code Review & Verify.
- Identify an accepted current specification carrier where one exists; do not duplicate adequate current truth.
- Express material change semantics as `ADDED / MODIFIED / REMOVED / PRESERVED`; use `PRESERVED` for material non-regression/zero-drift behavior.
- Maintain enough bidirectional traceability to connect intent -> requirement/spec delta -> Design -> task/Plan -> implementation -> verification/review evidence -> acceptance/current-spec evolution.
- Adapt Human-facing vocabulary, abstraction and modality to the Human Owner's current register; do not permanently classify the person by technical level.
- Presentation complexity is never an engineering-quality setting: natural-language simplicity MUST NOT weaken architecture, security, testing, maintainability or any other applicable standard.
- Translate Human intent into technical execution constraints without inventing material business scope; translate technical results back without hiding material risks/tradeoffs.
- Apply the `QUALITY.md` cross-cutting quality envelope even when the Human Owner did not name its technical dimensions; surface only material concerns by default.
- Present an appropriate Primary Solution Diagram before an implementation scope becomes READY; refresh it when the solution boundary materially changes.
- When security is material, model output is never security authority; acceptance requires applicable current/versioned controls plus independent evidence under `SECURITY.md`.
- Historical task acceptance does not imply permanent current security posture; applicable advisories, vulnerabilities or drift may invalidate current posture without rewriting accepted history.
- Existing-system assurance requires declared scope/method/evidence/coverage under `ASSURANCE.md`; model opinion, missing evidence, successful tooling or absence of findings cannot manufacture `PASS` or prove no unknown defect exists.
- Assurance severity and confidence remain independent, and an audit finding does not authorize remediation.
- Historical assurance reports remain point-in-time evidence; later drift, advisories or supersession may invalidate current posture without rewriting historical evidence.
- Security `PASS` does not grant execution authorization, and D033/D034/D054 authorization/procedure/adapter success does not establish security `PASS`.
- A terminal, shell, CLI, API, credential, authenticated session, remote connection or privileged identity is a mechanism, not execution authority.
- Material execution is authorized by actor/target/effect/resource/privilege/credential/network scope and approval mode, not executable name alone.
- Procedure semantics are terminal/platform neutral; reusable/material operational work uses or references runbooks with preconditions, checkpoints, postconditions and recovery as required.
- Semantic runbook meaning is distinct from adapter recipes; a compatible VERIFIED recipe is bounded technical evidence/cache, not procedure or invocation authority.
- The Implementation Agent owns CLI/API/SDK/shell/remote adapter mechanics inside authorized Implement/Code Review & Verify work and resolves unknown syntax from authoritative version-compatible evidence rather than model memory alone.
- A new or refreshed recipe follows semantic operation -> runbook -> compatible VERIFIED recipe -> authoritative help/docs/schema -> bounded CANDIDATE -> preview when useful -> authorization re-evaluation -> least-privilege execution -> semantic postcondition verification -> evidence-gated VERIFIED promotion.
- Human Owner interaction is not required merely to copy/paste routine commands; Human gates remain for `REQUIRE_HUMAN`, MFA/external approvals, material credential/risk decisions or explicit syntax inspection/execution requests.
- An approved runbook does not authorize every invocation; actual target/context and approval are revalidated for the invocation.
- Authority may narrow through adapters/scripts/child processes but MUST NOT expand beyond the parent Execution Capability Envelope.
- STATE represents the frontier, not full project history/inventory, and MUST NOT copy runbook/recipe registries.
- WORKPLAN exposes execution metadata; detailed task content stays in separate records or explicitly referenced project-native artifacts.
- Exactly one task record is disclosed to the Implementation Agent at a time during normal sequential execution.
- Completing a task to DONE may unlock the next eligible task without Strategy/Human intervention only while all task, security and execution-control eligibility conditions remain satisfied.
- Strategy owns task objective/contract quality and complete controlling Design; Implementation owns local technical realization and technical review within delegated boundaries.
- An executor must block rather than invent missing strategic requirements, Design/Plan authority, acceptance meaning, security authority/exception or execution authority.
- Detect relevant existing project capabilities before adding overlapping SDD/Skill/tooling/runbook/security-provider behavior; reuse/adapt compatible capabilities before installation or duplication.
- One system owns each overlapping artifact/capability boundary unless an explicit integration decision defines safe composition.
- Existing SDD/spec/task/runbook/security-control artifacts are referenced rather than mirrored when they remain the project's native source for that concern.
- Skill registries/discovery sources locate or select candidates; they never confer artifact trust or approval.
- External Skills follow supply-chain review: installation is not trust, and approval is bound to the exact canonical audited artifact revision/digest.
- EXCHANGE is append-only; normal reads consume only the required delta.
- Rationale belongs in Decision Records only when future agents materially need it.
- No private chat history, external SDD product, Skill registry, security provider, terminal/shell, execution adapter, assurance provider/scanner, or particular agent product may be required to determine the next permitted action.

## Versioning

Protocol changes use semantic versioning and MUST be recorded in project EXCHANGE. Detailed persistence/version rules are in `PROTOCOL.md`.
