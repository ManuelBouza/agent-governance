# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O204  
Canonical-Branch: `develop`  
Current-Work-Unit: R009 child sandbox inheritance research is complete and under T056 evaluation; T056 is specified but execution is version-gated because the last observed installed Codex/App Server was 0.149.0 and the required parent-owned child reload fix is in 0.153.4+  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: none until installed Codex/App Server passes the T056 version gate

## Durable frontier

- D039, D041, D042, D053, D054, D055, D056 and D057 remain controlling. Core protocol remains `1.15.0`.
- D057 research-to-decision traceability: `docs/decisions/D057-research-decision-traceability.md`.
- Canonical research ledger: `docs/RESEARCH-TRACEABILITY.md`.
- T050 remains `ACCEPTED`; code-health/symbol-map boundary remains active.
- T023/MG1-v12 remains closed as valid `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE`; no MG1-v13 is authorized.
- D055 remains unchanged as the global Human-facing Executor launch-profile policy.
- T054 remains accepted with pilot outcome `NOT_QUALIFIED`; do not rerun it unchanged.
- T055 remains accepted with qualification outcome `PARTIAL_OBSERVABILITY`; do not rerun it unchanged on 0.149.0.

## T055 final boundary

Authoritative review: `docs/reviews/T055-R1.md`.

T055 proved on installed Codex/App Server 0.149.0:

- one real child and parent relationship;
- requested/resolved `gpt-5.6-terra / low` thread profile;
- exact non-estimated child/turn token usage;
- exact child-turn duration;
- reroute observability;
- no tracked mutation.

It failed the mandatory child sandbox receipt gate because the post-run child lifecycle response reported legacy compatibility sandbox `workspaceWrite` rather than an unambiguous non-write receipt.

That result remains `PARTIAL_OBSERVABILITY` and is not retroactively changed by R009.

## R009 — child sandbox inheritance / receipt research

```text
Research: docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: docs/tasks/T056-codex-read-only-child-requalification.md
Decision-Ref: none
```

### R009 causal findings

R009 inspected official OpenAI documentation/source across:

```text
Codex 0.149.0 release:
  758ef40f50c1a458425c7cfbf1eb12cbc07af0b0
  release date: 2026-08-20

Codex 0.153.4 release:
  3d2ee51ca2d5db578f328aa75e20aa22c0197c9a
  published: 2026-09-04

current source inspected:
  ddf04ad26789d040f9ef6a96736f76602e35a6cc
```

Key findings:

1. **Spawn-time permission inheritance already existed in 0.149.0.** `build_agent_spawn_config` / `apply_spawn_agent_runtime_overrides` copies the live parent turn permission-profile snapshot into the child config and reapplies it after role/model layering.
2. Direct `spawn_agent` does not expose a sandbox argument. Parent-derived permission inheritance is the intended control model.
3. App Server prefers experimental profile-ID selection through `permissions`; `:read-only` is the reserved built-in read-only profile ID.
4. `activePermissionProfile` is the supported lifecycle provenance field when profile identity is known. The legacy lifecycle `sandbox` field is a compatibility/display projection and must not be treated as the authoritative full profile.
5. T055 selected the parent through legacy `sandbox=readOnly`, not `permissions=":read-only"`; therefore it did not exercise the strongest profile-provenance path.
6. The decisive post-0.149 fix is:

```text
d21794d6ba794673f2f754cc01bdb7dabc538f8c
Reload Multi-Agent V2 children through their parent (#40477)
2026-08-24
```

It fixes direct cold child resume potentially rebuilding an unloaded child from caller-provided settings instead of parent authority. The new path reloads through the actual loaded parent, preserves child compute identity, and inherits the parent's execution policy.
7. This fix is included in Codex 0.153.4. Its App Server documentation explicitly states that parent-owned V2 child `thread/resume` ignores configuration overrides and reloads an unloaded child through its actual loaded parent using parent-derived configuration.

### R009 interpretation of T055

R009 does **not** say T055's frozen AC-T055-6 should have passed.

The 0.149.0 supported receipt was ambiguous/broader and T055 correctly failed closed.

R009 only narrows the causal interpretation:

```text
T055 proves: 0.149.0 post-run supported lifecycle evidence did not prove read-only child authority.
T055 does not prove: the original child spawn necessarily executed with workspace-write authority.
```

The known 0.149 child-reload gap plus legacy sandbox projection are sufficient reasons to require a new version-pinned qualification rather than reinterpret the old run.

## T056 executable identity

Task Contract: `docs/tasks/T056-codex-read-only-child-requalification.md`.

T056 is a new narrow read-only child observability requalification, not a T055 rerun and not a routing pilot.

Human-visible launch profile **after the version gate is satisfied**:

```text
Executor: Codex
Session: NEW
Model: GPT-5.6 Sol
Effort: Medium
Expected evidence branch: test/t056-codex-read-only-child-requalification
```

### Hard version gate

T056 requires the **installed** Codex/App Server to be:

```text
>= 0.153.4
```

with native schema/help still exposing the required fields.

The last observed installed host during T055 was:

```text
0.149.0
```

Therefore T056 is currently **not ready to launch** unless the Human independently confirms that the normal installed Codex has since reached a qualifying version.

The Executor MUST NOT globally upgrade Codex, substitute a separate binary, build Codex from source, or mutate global configuration merely to satisfy the gate.

If launched while installed version is below 0.153.4, T056 must stop before any provider-backed synthetic probe with `BLOCKED_VERSION`.

### T056 frozen permission design

The parent is created with:

```text
permissions = ":read-only"
legacy sandbox request = omitted
```

Passing parent receipt requires:

```text
activePermissionProfile.id == ":read-only"
```

The parent remains loaded while exactly one real child is spawned and inspected.

The exact child is reattached/resumed without any config override. Passing child receipt requires:

```text
activePermissionProfile.id == ":read-only"
```

and no contradictory supported legacy sandbox projection showing broader authority.

T056 also reconfirms on the same version/run:

- real parent/child identity;
- requested/resolved child model/reasoning;
- exact non-estimated child/turn token usage;
- exact child-turn duration;
- reroute signal;
- no tracked mutation.

The child performs only a deterministic nonce return and no write attempt.

### T056 frozen decisions

Exactly one:

```text
QUALIFIED_READ_ONLY_CHILD_SURFACE
PARTIAL_OBSERVABILITY
BLOCKED_VERSION
BLOCKED_CAPABILITY
```

Even `QUALIFIED_READ_ONLY_CHILD_SURFACE` does not itself reactivate R007. Orchestrator convergence and explicit D057 transitions are required first.

## Research dispositions

### R006 — persistent Executor coordinator

```text
Research-State: COMPLETE
Decision-State: DEFERRED
```

No global D055 persistence-session change.

### R007 — adaptive subagent compute routing

```text
Research-State: COMPLETE
Decision-State: DEFERRED
```

No corrected routing pilot is authorized yet.

### R008 — child observability surface

```text
Research-State: COMPLETE
Decision-State: DEFERRED
```

R008 remains deferred pending T056. R009 provides the successor causal/version evidence but does not itself qualify the measurement surface.

### R009 — child sandbox inheritance / receipt

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Evaluation: T056 planned / version-gated
```

## Next action

1. Integrate the R009/T056 Markdown specification branch into `develop`.
2. Do **not** launch T056 while the installed Codex/App Server is known to be 0.149.0.
3. Human may update Codex through their normal installation/update channel outside the Executor task, or wait for the normal installation to advance. The Orchestrator does not prescribe a package-manager command because the installation method was not established by T055.
4. Before launching T056, establish that the normal installed Codex reports version `>= 0.153.4`.
5. Once that host gate is satisfied, use D055 launch profile: Codex / NEW / GPT-5.6 Sol / Medium.
6. Send pointer-only transport to current `docs/tasks/T056-codex-read-only-child-requalification.md` on canonical `develop`.
7. Executor runs T056 exactly and returns only terminal handoff fields.
8. Orchestrator converges T056 evidence from GitHub and transitions R009/R008 explicitly under D057.
9. Only after an accepted `QUALIFIED_READ_ONLY_CHILD_SURFACE` may the Orchestrator consider returning R007 to `EVALUATING` and specifying a corrected routing evaluation.
10. Do not launch MG1-v13 concurrently.

## Next chat minimum load

Load current `develop` identity, `AGENTS.md`, and this checkpoint.

Then follow `Next action`. Load R009/T056 only when the version gate is satisfied or when evaluating whether the gate changed. Load T055 review only if exact predecessor evidence is needed.

## Do not

Do not rerun T055 unchanged. Do not launch T056 on a known 0.149.0 host merely to obtain `BLOCKED_VERSION`. Do not globally upgrade Codex inside the Executor task. Do not infer child read-only authority from empty writable roots. Do not treat the legacy sandbox projection as the primary profile receipt. Do not claim `Thread.model` / `reasoningEffort` prove backend-served identity. Do not use private SQLite/JSONL to upgrade a result. Do not attempt child writes as a safety probe. Do not reactivate R007 without a passing T056 plus explicit D057 transition. Do not change D055, persistence policy, consumer policy or global routing policy. Do not rerun MG1-v12 or launch V13.