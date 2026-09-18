# Git-backed Skill loading fallback

Use this reference when a compatible host does not expose repository-owned Skills through a native Skill runtime, explicit `@` surface, or equivalent host routing mechanism.

## Principle

Git remains canonical. Native Skill installation is an optional host projection of the same repository-owned Skill source; lack of native host exposure must not prevent source-maintenance routing or correctness.

Do not claim or imply native Skill activation when using this fallback.

## Revision binding

Load Skill source from the same represented canonical Git revision that governs the active work.

1. At cold start, bootstrap from current `develop` as required by `AGENTS.md` and the current checkpoint.
2. If the checkpoint/Task Contract authorizes an active topic branch, revalidate that exact branch/HEAD before using Skill content from it.
3. Never mix a Skill body from one revision with repository authority from another when the difference could affect the task.
4. If the required Skill path is missing or the controlling revision is ambiguous/stale, fail closed rather than substituting chat memory or another branch.

## Loading workflow

1. Resolve intent from the Human objective plus current repository authority.
2. Select only the minimum applicable repository-owned Skill.
3. Read that Skill's root `SKILL.md` directly from the controlling Git revision.
4. Follow its progressive-disclosure links and load only the exact route/references required for the current stage or intent.
5. Compose transverse Skills only when their trigger is independently satisfied.
6. Apply repository policy, Task Contracts, Decisions, checkpoints, and handoffs as authority; Skill prose remains routing/operational guidance.
7. Record no host-native activation claim unless the host actually exposes observable native activation.

## Canonical source-maintenance paths

- Maintainer domain entry: `maintainer-skill/SKILL.md`
- Repository mutation control: `repository-change-control-skill/SKILL.md`
- Version-sensitive upstream reliance: `upstream-version-revalidation-skill/SKILL.md`
- Research evidence provenance/freshness: `research-evidence-traceability-skill/SKILL.md`
- Durable resumable frontier: `durable-work-checkpoint-skill/SKILL.md`
- Executor launch/handoff lifecycle: `executor-launch-handoff-skill/SKILL.md`

`workspace-isolation` remains an internal route/reference under `executor-launch-handoff`; never promote it to an independent top-level Skill merely because native routing is unavailable.

## Native/runtime coexistence

When the host does expose an applicable repository-owned Skill natively, prefer the native routing surface if it resolves to the same accepted repository-owned semantics. Host-native state cannot override Git authority.

When native exposure is unavailable, Git-backed loading is the compatibility fallback. The two modes must remain semantically equivalent at the repository-owned Skill layer; host adapters may differ only in discovery/loading mechanics.

## Non-goals

This fallback does not:

- install or emulate the host's native Skill runtime;
- create a host-specific Skill fork;
- grant repository mutation authority;
- replace deterministic bootstrap/tests/CI;
- turn chat history, Project Memory, or previously installed packages into canonical state;
- establish ChatGPT/Codex empirical parity or any host-activation qualification claim.
