# Optional ecosystem integrations

Status: RECOMMENDED / OPTIONAL

Agent Governance is self-sufficient. Correctness, bootstrap, validation, execution, verification, state recovery, Skill approval, coexistence handling and release acceptance MUST NOT depend on Gentle AI, Caveman, or any other external orchestration/optimization product.

Optional ecosystem tools may improve ergonomics or efficiency when they are already present and compatible. They remain subordinate to repository Governance Core, project authority/state and host-native ownership.

## Gentle AI

Gentle AI is an optional and recommended orchestration integration when a project already uses it.

Recommended coexistence:

- keep `gentle-orchestrator` as the project's selected orchestration layer when that is the user's established workflow;
- let Gentle AI discover Agent Skills through its Skill Registry rather than rewriting their instructions;
- preserve project-local skill precedence and exact `SKILL.md` paths selected by the registry;
- use Agent Governance only for explicit governance operations, not as a replacement for Gentle AI's SDD/orchestration workflow;
- classify material overlap through `COEXISTENCE.md` and return `CONFLICT` rather than silently choosing an authority winner.

Gentle AI MUST NOT become a required adapter, authority source or correctness dependency for Agent Governance. Projects without Gentle AI remain fully supported.

## Caveman

Caveman is an optional and recommended token-efficiency Skill when its compression style is useful for the selected agent workflow.

When Gentle AI is present, the preferred integration is to expose Caveman as a discoverable Skill and allow Gentle AI to select it only when the task benefits from terse output. Do not require a Caveman proxy/runtime layer merely to use Agent Governance.

Recommended boundaries:

- Caveman activation is opportunistic, not mandatory;
- absence or deactivation of Caveman MUST NOT block Agent Governance work;
- Governance authority, Task/Operational Contracts, acceptance criteria, exact status fields, code, errors, numbers, negations and irreversible-operation warnings must retain their exact semantics;
- do not use Caveman compression as an authority, verification method or substitute for deterministic evidence;
- do not require Caveman for bootstrap, validation, state reconstruction, handoff processing, Skill audit, coexistence classification or release acceptance;
- persisted Governance artifacts should remain normal unambiguous prose unless an authoritative operation explicitly requires a different format.

Caveman may be recommended for analysis, exploration, review and other high-volume conversational output where it reduces token use without degrading task outcome. For already-small structured handoffs or exact completion shapes, loading Caveman may provide no net benefit and should remain optional.

## Integration rule

Optional ecosystem integration follows this order:

1. detect what the project already uses;
2. preserve native ownership and managed surfaces;
3. reuse or coexist before adding adapters;
4. recommend useful optional tooling without making it mandatory;
5. fail closed on unresolved authority or managed-file overlap.

A recommendation is not a dependency. A discovery registry is not approval authority. A model or optimization layer is not governance evidence.

## Upstream references

Current compatibility guidance was derived from:

- Gentle AI Skill Registry behavior, including project-first/global-second discovery and exact `SKILL.md` path delegation;
- Gentle AI OpenCode profiles where `gentle-orchestrator` is the canonical base conductor;
- Caveman's Skill-level terse-output contract and its explicit clarity exceptions.

These upstream products may evolve. Treat their current host behavior as ecosystem compatibility information, not as immutable Agent Governance protocol semantics.
