# Portable Agent Governance

Protocol-Version: 1.13.0

## Purpose

Provide the small, always-loaded entrypoint for deterministic collaboration between the Human Owner, Strategy/Governance Agent, and Implementation Agent. Agent products are adapters to these roles; detailed rules live in focused Core modules loaded only when relevant.

Agent Governance also acts as a bidirectional proxy between Human Owner intent and implementation-grade engineering: communication adapts to the Human Owner's current technical register while engineering rigor remains invariant. Detailed interaction and quality rules are progressively loaded from `INTERACTION.md` and `QUALITY.md`.

Material security is governed by current/versioned authority, freshness, known-bad state, independent verification, bounded Human exceptions and temporal posture invalidation from `SECURITY.md`. Model output is never security authority, and historical task acceptance does not imply permanent current security posture.

Existing-system assurance is governed by evidence-first scope, assessment-profile ceilings, explicit finding states, provenance-bearing evidence, coverage accounting and audit/remediation separation from `ASSURANCE.md`. Model opinion, tool success, unassessed areas and missing evidence never silently become assurance.

Material local/remote/system execution is governed by effect- and target-oriented authorization plus runbook-first terminal-neutral procedure semantics from `EXECUTION-CONTROL.md`. Availability of a terminal, credential, CLI, API, remote connection or privileged identity never creates Governance authority by itself.

## Bootstrap Invariant

On cold start load only:
1. `.agent-coordination/STATE.json`;
2. this file;
3. the repository-native adapter when the product loads it automatically.

Then perform a lightweight EXCHANGE freshness probe: determine the latest event `q` without loading full history when tooling permits. If latest `q > STATE.exchange_q`, load only that delta before deciding the effective frontier.

Do NOT preload MISSION, WORKPLAN, all task records, Decision Records, Core modules, Skill audit records, ecosystem inventories, or full EXCHANGE history. Route context on a need-to-know basis.

## Authority

Highest authority wins:
1. explicit Human Owner instruction;
2. Governance Core (`GOVERNANCE.md` plus applicable modules);
3. `.agent-coordination/MISSION.md`;
4. `.agent-coordination/WORKPLAN.md` and the currently disclosed task record;
5. accepted decisions/events in EXCHANGE and controlling Decision Records;
6. Implementation Agent technical decisions inside approved scope;
7. approved Skills and other technical guidance.

`STATE.json` is derived and never authoritative. Skills provide expertise, not authority. Existing SDD/specification artifacts become controlling for a scope only when Strategy/Human authority binds them by reference from the applicable mission/decision/task contract; they do not create a parallel Governance authority tier.

## Roles

- **Human Owner** — final authority over scope, priorities, risk, pause/resume and overrides.
- **Strategy/Governance Agent** — owns F0-F6 strategy, Human-intent/engineering translation, ecosystem/capability boundary decisions, implicit quality review, Skill discovery/audit/approval, graphical solution presentation, work decomposition, task-contract correctness/completeness, readiness, acceptance/rejection, strategic blockers and durable checkpoint maintenance.
- **Implementation Agent** — owns technical implementation inside the authorized execution sequence and applicable execution-capability envelope, regardless of whether the product is OpenCode, Codex, Claude Code, Antigravity or another compatible agent.

Product identity MUST NOT appear in task semantics. See `ADAPTERS.md`.

## Source Map

- collaboration/router -> `.agent-governance/GOVERNANCE.md`
- adaptive Human-intent/technical interaction -> `.agent-governance/INTERACTION.md`
- implicit engineering quality + graphical design readiness -> `.agent-governance/QUALITY.md`
- material security authority/freshness/verification/posture -> `.agent-governance/SECURITY.md`
- existing-system assurance scope/evidence/findings/coverage/reporting -> `.agent-governance/ASSURANCE.md`
- context loading/budgets -> `.agent-governance/CONTEXT.md`
- agent-product mapping -> `.agent-governance/ADAPTERS.md`
- pre-implementation F0-F6/task contract quality -> `.agent-governance/LIFECYCLE.md`
- ecosystem/SDD/Skill/tool coexistence -> `.agent-governance/COEXISTENCE.md`
- sequential execution/readiness/blockers -> `.agent-governance/EXECUTION.md`
- material execution authorization + runbook/adapter semantics -> `.agent-governance/EXECUTION-CONTROL.md`
- STATE/EXCHANGE/Decision Records/versioning -> `.agent-governance/PROTOCOL.md`
- handoff/cold-start recovery -> `.agent-governance/HANDOFF.md`
- Skill capability governance -> `.agent-governance/SKILLS.md`
- Skill candidate discovery/source resolution -> `.agent-governance/SKILL-DISCOVERY.md`
- external Skill provenance/audit/install gate -> `.agent-governance/SKILL-SUPPLY-CHAIN.md`
- mission objective/scope -> `.agent-coordination/MISSION.md`
- work frontier/order/dependencies -> `.agent-coordination/WORKPLAN.md`
- task detail -> `.agent-coordination/tasks/<TASK-ID>.md`
- approved Skill artifact record -> `.agent-coordination/skills/<SKILL-ID>.json`
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
| Bootstrap/adopt Governance where existing SDD/Skills/tooling may overlap | COEXISTENCE + only relevant project-native capability evidence |
| F0/F1 framing or viability | LIFECYCLE + MISSION; add INTERACTION when intent translation is non-trivial; add COEXISTENCE only when an existing methodology/capability boundary affects the frame |
| F2 engineering strategy | LIFECYCLE + QUALITY + MISSION + only relevant Decision Records; add SECURITY when security is material; add ASSURANCE when assessing an already-built subject rather than only designing a change; add COEXISTENCE when selecting/reusing capability providers; add EXECUTION-CONTROL when material local/remote/system effects, privilege, credentials, deployment, persistent-data mutation or destructive/recovery-sensitive operations are part of the solution; add INTERACTION when presenting material tradeoffs/diagram at the Human Owner's register |
| F3 capability audit | LIFECYCLE + SKILLS + WORKPLAN index; add COEXISTENCE for existing Skill/registry overlap, SKILL-DISCOVERY only while locating/resolving candidates and SKILL-SUPPLY-CHAIN only while auditing/acquiring them |
| F4/F5 planning/readiness | LIFECYCLE + QUALITY + WORKPLAN + only affected task files + relevant Decision Records/Skill approval records; add SECURITY for security-material tasks; add ASSURANCE for existing-system assessment scope/evidence/coverage/reporting; add EXECUTION-CONTROL for tasks with material execution effects/runbook/Human-gate requirements; add INTERACTION for Human-facing solution presentation; add only referenced native SDD artifacts needed to validate the current plan/task |
| Existing-system assurance audit | ASSURANCE + QUALITY + declared subject/scope/evidence context; add SECURITY for security-material claims; add EXECUTION-CONTROL before any live/read-only/active/intrusive assessment effect; add COEXISTENCE only for genuine provider/ownership overlap |
| Implementation sequence | EXECUTION + WORKPLAN metadata + current task only + its exact referenced native artifacts + exact required approved Skill artifacts; add SECURITY only when the disclosed task has material security controls/evidence; add ASSURANCE only when the disclosed task is part of an authorized existing-system assessment; add EXECUTION-CONTROL only when the disclosed task/effect requires it |
| Implementation blocker/state transition | EXECUTION + current task; add SECURITY for security-source freshness/known-bad/verifier/exception/posture blockers; add ASSURANCE for audit-scope/evidence/coverage blockers; add EXECUTION-CONTROL for authorization/target/runbook/adapter/recovery blockers; PROTOCOL only if event/state semantics are needed; COEXISTENCE only for a genuine provider/authority collision; QUALITY only if the blocker invalidates a material quality/design assumption |
| Handoff/review | HANDOFF + EXCHANGE delta after checkpoint + referenced evidence only; add SECURITY when reviewing material security evidence/posture; add ASSURANCE when reviewing an audit claim/report/coverage boundary; add EXECUTION-CONTROL when reviewing material execution/runbook evidence |
| STATE repair or protocol question | PROTOCOL + minimum authority records needed for disputed fields |
| Skill discovery/source question | SKILLS + SKILL-DISCOVERY + minimum capability context |
| Skill acquisition/update/revocation | SKILLS + SKILL-SUPPLY-CHAIN + candidate/approval record only |
| SDD/Skill/tool collision or shared managed-file question | COEXISTENCE + only the conflicting artifacts/configuration |
| Security/privacy/reliability/operability/quality question | QUALITY + only the affected design/task/evidence context; add SECURITY when security is material; add ASSURANCE when the request is an assessment of existing implemented state; add EXECUTION-CONTROL when the concern involves system execution authority/procedure |

Do not recursively load unrelated files, whole SDD histories, full Skill registries, or future task contents.

## Mandatory Lifecycle

Every new implementation scope follows `LIFECYCLE.md`. Strategy is responsible for producing a complete execution contract before F5; the Implementation Agent must not be expected to reconstruct missing requirements or hidden strategic intent. Existing SDD/specification systems may supply project-native requirements/plans/tasks when they satisfy the lifecycle contract; Governance validates/adapts those artifacts rather than duplicating them under `COEXISTENCE.md`.

Before F5 passes, Strategy also applies the implicit engineering quality envelope in `QUALITY.md` and presents the Primary Solution Diagram at the Human Owner's current interaction register under `INTERACTION.md`. Presentation complexity may vary; engineering quality may not.

When security is material under `QUALITY.md`, F5 additionally applies `SECURITY.md`: applicable authoritative controls and source freshness must be determinable, relevant known-bad state must be resolved, required independent verification must be defined, and any Human exception or temporal recheck/invalidation condition must be explicit. Security requirements exist before implementation; verifier success cannot compensate for missing security authority/applicability.

When an authorized scope assesses an already-built system, F5 additionally applies `ASSURANCE.md`: subject/environment/resource/data/access boundaries, authorized methods and profile ceiling, evidence provenance, finding-state semantics, coverage accounting, security-source freshness where applicable, and explicit audit-versus-remediation boundaries must be determinable before assessment claims are accepted. Unassessed or inconclusive areas cannot be silently reported as passing.

When the implementation scope includes material execution effects governed by `EXECUTION-CONTROL.md`, F5 additionally requires a determinable Execution Capability Envelope, explicit approval/Human-gate semantics, actual-target verification, and any required reusable/project-native runbook with preconditions, postconditions and recovery evidence. A runbook defines procedure but does not authorize a particular invocation.

F5 authorizes the plan and F6 opens the execution sequence. Implementation then works task-by-task under `EXECUTION.md` until all authorized tasks are DONE or a valid cross-responsibility/execution-control/security/assurance blocker stops the sequence. General task readiness does not silently authorize production, privilege, credentials, global configuration, destructive effects or any target outside the applicable Execution Capability Envelope, and execution authorization does not establish security or assurance acceptance.

## Core Invariants

- Persist decisions that affect future work before context switch/handoff.
- Communicate deltas, not repeated history.
- Adapt Human-facing vocabulary, abstraction and modality to the Human Owner's current register; do not permanently classify the person by technical level.
- Presentation complexity is never an engineering-quality setting: natural-language simplicity MUST NOT weaken architecture, security, testing, maintainability or any other applicable standard.
- Translate Human intent into technical execution constraints without inventing material business scope; translate technical results back without hiding material risks/tradeoffs.
- Apply the `QUALITY.md` cross-cutting quality envelope even when the Human Owner did not name its technical dimensions; surface only material concerns by default.
- Present an appropriate Primary Solution Diagram before an implementation scope becomes READY; refresh it when the solution boundary materially changes.
- When security is material, model output is never security authority; acceptance requires applicable current/versioned controls plus independent evidence under `SECURITY.md`.
- Historical task acceptance does not imply permanent current security posture; applicable advisories, vulnerabilities or drift may invalidate current posture without rewriting accepted history.
- Existing-system assurance is evidence-first and scope-bounded; model opinion, successful tool execution, absence of findings, `NOT_ASSESSED` and `INCONCLUSIVE` do not establish `PASS`.
- Audit severity and confidence are independent, and coverage gaps remain visible in bounded conclusions.
- An audit finding does not authorize remediation; assessment effects and remediation mutations each require their own applicable execution authority.
- Historical assurance reports remain historical; later drift/advisories may invalidate current posture without rewriting historical evidence.
- Security `PASS` does not grant execution authorization, audit `PASS` does not manufacture security `PASS`, and D033/D034 authorization/procedure success does not establish security or assurance `PASS`.
- A terminal, shell, CLI, API, credential, authenticated session, remote connection or privileged identity is a mechanism, not execution authority.
- Material execution is authorized by actor/target/effect/resource/privilege/credential/network scope and approval mode, not executable name alone.
- Procedure semantics are terminal/platform neutral; reusable/material operational work uses or references runbooks with preconditions, checkpoints, postconditions and recovery as required.
- An approved runbook does not authorize every invocation; actual target/context and approval are revalidated for the invocation.
- Authority may narrow through adapters/scripts/child processes but MUST NOT expand beyond the parent Execution Capability Envelope.
- STATE represents the frontier, not full project history/inventory.
- WORKPLAN exposes execution metadata; detailed task content stays in separate records or explicitly referenced project-native artifacts.
- Exactly one task record is disclosed to the Implementation Agent at a time during normal sequential execution.
- Completing a task to DONE may unlock the next eligible task without Strategy/Human intervention only while all task, security, assurance and execution-control eligibility conditions remain satisfied.
- Strategy owns task objective/contract quality; Implementation owns technical realization within delegated boundaries.
- An executor must block rather than invent missing strategic requirements, acceptance meaning, security authority/exception, assurance evidence/scope or execution authority.
- Detect relevant existing project capabilities before adding overlapping SDD/Skill/tooling/runbook/security-provider behavior; reuse/adapt compatible capabilities before installation or duplication.
- One system owns each overlapping artifact/capability boundary unless an explicit integration decision defines safe composition.
- Existing SDD/spec/task/runbook/security-control artifacts are referenced rather than mirrored when they remain the project's native source for that concern.
- Skill registries/discovery sources locate or select candidates; they never confer artifact trust or approval.
- External Skills follow supply-chain review: installation is not trust, and approval is bound to the exact canonical audited artifact revision/digest.
- EXCHANGE is append-only; normal reads consume only the required delta.
- Rationale belongs in Decision Records only when future agents materially need it.
- No private chat history, particular SDD product, Skill registry, security provider, audit/scanner provider, terminal/shell, execution adapter, or particular agent product may be required to determine the next permitted action.

## Versioning

Protocol changes use semantic versioning and MUST be recorded in project EXCHANGE. Detailed persistence/version rules are in `PROTOCOL.md`.
