# Portable Agent Governance

Protocol-Version: 1.8.0

## Purpose

Provide the small, always-loaded entrypoint for deterministic collaboration between the Human Owner, Strategy/Governance Agent, and Implementation Agent. Agent products are adapters to these roles; detailed rules live in focused Core modules loaded only when relevant.

## Bootstrap Invariant

On cold start load only:
1. `.agent-coordination/STATE.json`;
2. this file;
3. the repository-native adapter when the product loads it automatically.

Then perform a lightweight EXCHANGE freshness probe: determine the latest event `q` without loading full history when tooling permits. If latest `q > STATE.exchange_q`, load only that delta before deciding the effective frontier.

Do NOT preload MISSION, WORKPLAN, all task records, Decision Records, Core modules, Skill audit records, or full EXCHANGE history. Route context on a need-to-know basis.

## Authority

Highest authority wins:
1. explicit Human Owner instruction;
2. Governance Core (`GOVERNANCE.md` plus applicable modules);
3. `.agent-coordination/MISSION.md`;
4. `.agent-coordination/WORKPLAN.md` and the currently disclosed task record;
5. accepted decisions/events in EXCHANGE and controlling Decision Records;
6. Implementation Agent technical decisions inside approved scope;
7. approved Skills and other technical guidance.

`STATE.json` is derived and never authoritative. Skills provide expertise, not authority.

## Roles

- **Human Owner** — final authority over scope, priorities, risk, pause/resume and overrides.
- **Strategy/Governance Agent** — owns F0-F6 strategy, Skill discovery/audit/approval, work decomposition, task-contract correctness/completeness, readiness, acceptance/rejection, strategic blockers and durable checkpoint maintenance.
- **Implementation Agent** — owns technical implementation inside the authorized execution sequence, regardless of whether the product is OpenCode, Codex, Claude Code, Antigravity or another compatible agent.

Product identity MUST NOT appear in task semantics. See `ADAPTERS.md`.

## Source Map

- collaboration/router -> `.agent-governance/GOVERNANCE.md`
- context loading/budgets -> `.agent-governance/CONTEXT.md`
- agent-product mapping -> `.agent-governance/ADAPTERS.md`
- pre-implementation F0-F6/task contract quality -> `.agent-governance/LIFECYCLE.md`
- sequential execution/readiness/blockers -> `.agent-governance/EXECUTION.md`
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
| Explicit current focus | only files listed in `STATE.context`, plus a controlling Decision Record only when needed |
| Configure another agent product | ADAPTERS + product-native adapter/configuration |
| F0/F1 framing or viability | LIFECYCLE + MISSION |
| F2 engineering strategy | LIFECYCLE + MISSION + only relevant Decision Records |
| F3 capability audit | LIFECYCLE + SKILLS + WORKPLAN index; add SKILL-DISCOVERY only while locating/resolving candidates and SKILL-SUPPLY-CHAIN only while auditing/acquiring them |
| F4/F5 planning/readiness | LIFECYCLE + WORKPLAN + only affected task files + relevant Decision Records/Skill approval records |
| Implementation sequence | EXECUTION + WORKPLAN metadata + current task only + its exact required approved Skill artifacts |
| Implementation blocker/state transition | EXECUTION + current task; PROTOCOL only if event/state semantics are needed |
| Handoff/review | HANDOFF + EXCHANGE delta after checkpoint + referenced evidence only |
| STATE repair or protocol question | PROTOCOL + minimum authority records needed for disputed fields |
| Skill discovery/source question | SKILLS + SKILL-DISCOVERY + minimum capability context |
| Skill acquisition/update/revocation | SKILLS + SKILL-SUPPLY-CHAIN + candidate/approval record only |

Do not recursively load unrelated files or future task contents.

## Mandatory Lifecycle

Every new implementation scope follows `LIFECYCLE.md`. Strategy is responsible for producing a complete execution contract before F5; the Implementation Agent must not be expected to reconstruct missing requirements or hidden strategic intent. F5 authorizes the plan and F6 opens the execution sequence. Implementation then works task-by-task under `EXECUTION.md` until all authorized tasks are DONE or a valid cross-responsibility blocker stops the sequence.

## Core Invariants

- Persist decisions that affect future work before context switch/handoff.
- Communicate deltas, not repeated history.
- STATE represents the frontier, not full project history/inventory.
- WORKPLAN exposes execution metadata; detailed task content stays in separate records.
- Exactly one task record is disclosed to the Implementation Agent at a time during normal sequential execution.
- Completing a task to DONE may unlock the next eligible task without Strategy/Human intervention.
- Strategy owns task objective/contract quality; Implementation owns technical realization within delegated boundaries.
- An executor must block rather than invent missing strategic requirements or acceptance meaning.
- Skill discovery sources locate candidates; they never confer artifact trust or approval.
- External Skills follow supply-chain review: installation is not trust, and approval is bound to the exact canonical audited artifact revision/digest.
- EXCHANGE is append-only; normal reads consume only the required delta.
- Rationale belongs in Decision Records only when future agents materially need it.
- No private chat history or particular agent product may be required to determine the next permitted action.

## Versioning

Protocol changes use semantic versioning and MUST be recorded in project EXCHANGE. Detailed persistence/version rules are in `PROTOCOL.md`.
