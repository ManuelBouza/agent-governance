# Progressive Context Loading

Context-Version: 1.2.0

Load information by relevance, not by repository size. Use a small stable bootstrap plus direct navigation to focused context.

## Tiers

- **T0 Bootstrap** — STATE + GOVERNANCE + native repository adapter.
- **T1 Routing** — GOVERNANCE identifies the next files.
- **T2 Focused context** — only the lifecycle/coexistence module, current task, exact referenced project-native artifact, Skill, mission context or decision needed now.
- **T3 Evidence/history** — EXCHANGE delta, commits, logs or code only when required.

Never load T2/T3 material preemptively. Existing SDD/specification systems do not create an exception: load only the native artifacts explicitly required for the current frame/task, not their whole workspace/backlog.

## File Creation Rule

Create a separate document only when it forms a coherent unit of context loadable independently. Each persistent file needs one primary responsibility and a discoverable path from GOVERNANCE, WORKPLAN, STATE or another direct index.

## Guardrail Budgets

Project-design budgets, not vendor hard limits:
- always-loaded file target <= 1,000 tokens;
- total governance/bootstrap instructions target <= 2,000 tokens excluding native system instructions;
- focused Governance module target <= 1,500 tokens;
- atomic task record target <= 800 tokens excluding directly referenced native requirement/spec artifacts;
- STATE target <= 500 tokens and approximately constant size;
- Decision Record target <= 1,000 tokens;
- Governance `SKILL.md` target < 2,500 tokens unless measured use proves more is required.

Exceeding a budget requires justified cohesion or refactoring; never remove required authority/safety information just to meet a budget. Do not evade task budgets by duplicating large external SDD artifacts into Governance records; reference them instead.

## STATE Frontier Rule

STATE answers: where are we, what controls the frontier, and what can happen next. Do not store full task inventories, capability inventories, external SDD inventories, decision history, debate, logs or repeated MISSION/WORKPLAN content.

Freshness is primarily checked through `exchange_q`; later EXCHANGE events require replay/reconstruction.

Material ecosystem/provider classifications live in the compact CAPABILITIES record under PROTOCOL/COEXISTENCE, not STATE.

## WORKPLAN Index Rule

WORKPLAN contains gates, approved Skill frontier, deterministic execution order, dependency/status metadata and pointers to task records. It MUST NOT expose future task objective/scope/acceptance content or copy future native-SDD task artifacts.

During implementation the agent MAY inspect the metadata index to choose the next eligible ID, but loads exactly one task record at a time. That task may then route to the exact native project/SDD artifacts required for its execution.

## Sequential Disclosure Rule

Future task records are sealed by protocol, not encryption.

The Implementation Agent MUST NOT open a future task record while another task is READY, IN_PROGRESS or BLOCKED. The same rule applies to native SDD/spec/task artifacts that reveal future-task objective/scope/acceptance content. After the current task reaches DONE, the agent may identify the next eligible task from WORKPLAN metadata and only then load that task record and its exact referenced native artifacts.

Do not preload, summarize, search across, or infer detailed future task contents. Product adapters should avoid automatic inclusion of task directories or external SDD backlog directories.

## Decision Records

Use a Decision Record only when rationale, alternatives or consequences materially affect future choices. Routine point decisions remain compact EXCHANGE events. STATE may identify controlling IDs without reproducing rationale.

## EXCHANGE

Physical growth is acceptable while logical reads stay bounded. Normal handoff reads only events with `q > STATE.exchange_q`. During a continuous implementation sequence multiple task events may accumulate before STATE refresh.

## Reference Discipline

Prefer direct references from an index/router to the target file. Avoid deep chains and duplicated normative rules.

For project-native SDD/specification artifacts, reference the canonical native path/source. Do not create Governance mirror copies unless a deliberate migration decision transfers ownership.
