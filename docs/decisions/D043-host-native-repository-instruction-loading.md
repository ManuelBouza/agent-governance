# D043 — Host-native repository instruction loading

Status: ACCEPTED

## Context

D042 requires executor launches to establish a current canonical remote baseline before loading the persisted Task/Operational Contract. The canonical launch prompts also explicitly instructed the executor to read `AGENTS.md` on every launch.

Compatible coding-agent hosts such as OpenCode, Codex and Claude Code normally load repository-level agent instructions as part of their native session/repository bootstrap. Repeating an unconditional `read AGENTS.md` instruction in every Agent Governance launch prompt is therefore redundant and can distort the executor's own orchestration by turning host bootstrap into task work.

Agent Governance should preserve `AGENTS.md` authority without duplicating host-native repository-instruction loading.

## Decision

A compatible Agente de IA Ejecutor host is expected to load applicable repository instructions, including `AGENTS.md`, through its native session/repository bootstrap mechanism.

Agent Governance launch prompts MUST NOT instruct the executor to read/re-read `AGENTS.md` by default.

ChatGPT adds an explicit `AGENTS.md` reload instruction only when the integrated change immediately governing the next delegated execution modified `AGENTS.md` and the executor session may therefore hold a pre-change instruction snapshot.

```text
normal launch:
canonical remote freshness
    -> persisted contract
    -> execution

launch after AGENTS.md change:
canonical remote freshness
    -> reload current AGENTS.md
    -> persisted contract
    -> execution
```

The reload condition is determined by canonical Git diff/history, not by executor guesswork.

## Compatibility rule

If an executor host does not natively load repository instructions, its adapter/session bootstrap must provide equivalent repository-instruction loading before it is treated as a compatible executor. Agent Governance MUST NOT compensate by reintroducing unconditional `AGENTS.md` reads into every Task/Operational launch prompt.

## Authority boundary

This decision changes instruction transport only.

It does not:

- weaken or remove `AGENTS.md` authority;
- change Markdown/non-Markdown ownership;
- alter D041 executor process autonomy;
- alter D042 canonical-remote freshness;
- make private executor orchestration acceptance evidence;
- add task-specific semantics to launch prompts.

## Invariant

```text
repository instruction authority != repeated prompt instruction
host-native load + conditional reload on change = sufficient bootstrap
```

A launch is nonconforming if ChatGPT omits the conditional reload after a governing `AGENTS.md` change, or if it adds an unconditional `read AGENTS.md` directive when no such change requires reload.
