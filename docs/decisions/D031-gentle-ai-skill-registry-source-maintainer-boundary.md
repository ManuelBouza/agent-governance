# D031 — Gentle-AI skill registry source-maintainer boundary

Status: ACCEPTED
Authority: Human Owner / ChatGPT Orchestrator under D026 and D030

## Problem

Agent Governance source maintenance currently uses OpenCode in a workstation where Gentle-AI is installed. T001 correctly resolved Gentle-AI RDD as an overlapping review/delivery authority under D030, but later task wording overgeneralized that conflict and treated Gentle-AI's project-local `.atl/` state as something the executor should not modify or refresh.

That boundary is too broad.

Gentle-AI's skill registry is a separate, non-authoritative capability from RDD. Current Gentle-AI documentation and implementation describe a project-local index at `.atl/skill-registry.md` plus `.atl/.skill-registry.cache.json`. Supported agent integrations including OpenCode refresh that registry from startup/plugin hooks. The registry records discovered Skill names, descriptions, scopes, and exact `SKILL.md` paths so the host orchestrator can resolve applicable Skills before delegation.

## Decision

For Agent Governance source maintenance, Gentle-AI's skill registry is classified `COEXIST` as an executor-host discovery/routing capability, subject to the following boundary:

- Gentle-AI MAY read, create, refresh, and cache its project-local `.atl/` skill-registry state during normal host operation.
- OpenCode/Gentle-AI MAY use that registry to discover and resolve Skills that assist executor work.
- Registry selection, project-vs-user precedence, or host activation MUST NOT become Agent Governance approval, trust, governance authority, Task Contract authority, or acceptance authority.
- Agent Governance tests, Task Contracts, and release correctness MUST remain executable without Gentle-AI or `.atl/` present.
- `.atl/` generated registry/cache state is local executor-host state and MUST NOT be committed as Agent Governance product state.
- RDD remains governed separately by D030 and stays disabled clone-locally for this source repository because its review/delivery authority conflicts with D022.

The source repository therefore distinguishes:

```text
Gentle-AI skill discovery / registry -> COEXIST
Gentle-AI RDD review/delivery authority -> CONFLICT, clone-local opt-out under D030
```

Disabling RDD MUST NOT be interpreted as disabling Gentle-AI generally.

## `.atl/` runtime state

The generated registry surface currently includes at least:

- `.atl/skill-registry.md`
- `.atl/.skill-registry.cache.json`

The registry may also inspect supported project Skill roots, including `.atl/skills/`, when such local state exists.

The generated registry is an index. The referenced `SKILL.md` remains the underlying Skill source of truth; the registry does not replace the Skill artifact itself.

Normal startup may refresh the registry when skill fingerprints change and may produce a cheap cache hit when they have not.

## `.gitignore` adaptation

Current Gentle-AI `skill-registry refresh` calls its `EnsureATLIgnored` behavior by default. If `.atl/` is absent from the repository root `.gitignore`, the normal refresh path may add a small local-runtime ignore block containing `.atl/`.

For this source repository, that exact ignore is an approved bounded `ADAPT` under D030 because it prevents legitimate executor-host cache/index state from polluting Git status while preserving all Agent Governance authority and correctness boundaries.

The approved canonical mutation is limited to ignoring `.atl/` as local AI runtime state. It does **not** authorize:

- committing `.atl/` contents;
- adding Gentle-AI to `pyproject.toml`, `uv.lock`, tests, or release dependencies;
- adding other Gentle-AI/SDD generated repository assets;
- initializing/migrating the source repository into Gentle-AI SDD;
- re-enabling Gentle-AI RDD;
- changing global/user Gentle-AI configuration.

If the host attempts broader tracked-file mutation, the executor must stop and report the exact delta.

## Skill trust boundary

The registry is discovery/selection evidence only.

For any Skill used normatively by Agent Governance itself, D026 and the applicable Skill supply-chain rules still distinguish:

```text
host discovers/selects an artifact != Agent Governance approves/trusts that artifact
```

An executor may use ordinary host-provided coding assistance where the Task Contract permits it, but host Skill availability cannot rewrite scope, acceptance criteria, Markdown ownership, or review authority.

## Relationship to D026 and D030

D026 defines the generic capability-first/reuse-before-install/no-authority-collision policy.

D030 applies that policy to executor-host overlays and specifically resolves RDD review/delivery authority.

D031 clarifies a different Gentle-AI capability boundary exposed by the same workstation:

- skill registry: non-authoritative discovery/routing, allowed to coexist;
- RDD: overlapping review/delivery authority, disabled clone-locally.

No Governance Core protocol change is introduced.

## Research basis

Gentle-AI public documentation and implementation reviewed on 2026-08-10:

- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/skill-registry.md`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/intended-usage.md`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/docs/usage.md`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/internal/skillregistry/registry.go`
- `https://github.com/Gentleman-Programming/gentle-ai/blob/main/internal/app/app.go`

Observed current behavior used by this decision:

- OpenCode is among the integrations whose startup/plugin hooks refresh the skill registry;
- the registry writes `.atl/skill-registry.md` and `.atl/.skill-registry.cache.json`;
- refresh is fingerprint-cached;
- project-local Skill candidates take precedence over same-name global candidates for host selection;
- `skill-registry list` provides a read-only inspection path;
- normal `refresh` ensures `.atl/` is ignored in `.gitignore` unless invoked with `--no-gitignore`;
- registry selection remains an index/delegation mechanism, not an Agent Governance trust or acceptance decision.

## Consequences

- T002 must not prohibit normal Gentle-AI skill-registry refresh/read/write behavior.
- T002 may authorize the minimal `.gitignore` `.atl/` compatibility entry if normal Gentle-AI operation adds it.
- T002 tests remain independent of Gentle-AI and must use synthetic fixtures rather than the live registry as test input.
- future source tasks should classify external host capabilities individually instead of treating all state from one product as one authority surface.
