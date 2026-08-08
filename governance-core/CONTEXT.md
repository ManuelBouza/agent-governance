# Progressive Context Loading

Context-Version: 1.1.0

Load information by relevance, not by repository size. Use a small stable bootstrap plus direct navigation to focused context.

## Tiers

- **T0 Bootstrap** — STATE + GOVERNANCE + native repository adapter.
- **T1 Routing** — GOVERNANCE identifies the next files.
- **T2 Focused context** — only the lifecycle module, current task, Skill, mission context or decision needed now.
- **T3 Evidence/history** — EXCHANGE delta, commits, logs or code only when required.

Never load T2/T3 material preemptively.

## File Creation Rule

Create a separate document only when it forms a coherent unit of context loadable independently. Each persistent file needs one primary responsibility and a discoverable path from GOVERNANCE, WORKPLAN, STATE or another direct index.

## Guardrail Budgets

Project-design budgets, not vendor hard limits:
- always-loaded file target <= 1,000 tokens;
- total governance/bootstrap instructions target <= 2,000 tokens excluding native system instructions;
- focused Governance module target <= 1,500 tokens;
- atomic task record target <= 800 tokens;
- STATE target <= 500 tokens and approximately constant size;
- Decision Record target <= 1,000 tokens;
- Governance `SKILL.md` target < 2,500 tokens unless measured use proves more is required.

Exceeding a budget requires justified cohesion or refactoring; never remove required authority/safety information just to meet a budget.

## STATE Frontier Rule

STATE answers: where are we, what controls the frontier, and what can happen next. Do not store full task inventories, decision history, debate, logs or repeated MISSION/WORKPLAN content.

Freshness is primarily checked through `exchange_q`; later EXCHANGE events require replay/reconstruction.

## WORKPLAN Index Rule

WORKPLAN contains gates, approved Skill frontier, deterministic execution order, dependency/status metadata and pointers to task records. It MUST NOT expose future task objective/scope/acceptance content.

During implementation the agent MAY inspect the metadata index to choose the next eligible ID, but loads exactly one task record at a time.

## Sequential Disclosure Rule

Future task records are sealed by protocol, not encryption.

The Implementation Agent MUST NOT open a future task record while another task is READY, IN_PROGRESS or BLOCKED. After the current task reaches DONE, the agent may identify the next eligible task from WORKPLAN metadata and only then load that task record.

Do not preload, summarize, search across, or infer detailed future task contents. Product adapters should avoid automatic inclusion of task directories.

## Decision Records

Use a Decision Record only when rationale, alternatives or consequences materially affect future choices. Routine point decisions remain compact EXCHANGE events. STATE may identify controlling IDs without reproducing rationale.

## EXCHANGE

Physical growth is acceptable while logical reads stay bounded. Normal handoff reads only events with `q > STATE.exchange_q`. During a continuous implementation sequence multiple task events may accumulate before STATE refresh.

## Reference Discipline

Prefer direct references from an index/router to the target file. Avoid deep chains and duplicated normative rules.
