# R009 — Codex Child Sandbox Inheritance / Receipt Research

Status: COMPLETE  
Research-State: `COMPLETE`  
Decision-State: `EVALUATING`  
Owner: ChatGPT Orchestrator  
Date: 2026-09-05  
Last-Reviewed: 2026-09-05  
Evaluation: `docs/tasks/T056-codex-read-only-child-requalification.md`  
Predecessor: `docs/reviews/T055-R1.md`  
Controlling traceability: `docs/decisions/D057-research-decision-traceability.md`

## Research question

T055 proved that the exercised Codex 0.149.0 App Server could correlate a real child to resolved model/reasoning, exact child/turn usage and duration, but failed the mandatory non-write child-sandbox receipt gate.

The narrow question for R009 is:

> Does a materially newer supported Codex surface provide a defensible parent-owned child sandbox inheritance and receipt path that can close T055's AC-T055-6 gap without direct per-spawn sandbox control, private persistence scraping, product dependency changes, or global configuration mutation?

## Scope

R009 is vendor-surface research. It does not test adaptive-routing quality, persistence efficiency, or compute savings.

It distinguishes:

1. **runtime inheritance** — what sandbox/permission state the child is built from;
2. **profile provenance** — whether the supported API exposes the identity of the permission profile producing that runtime state;
3. **legacy sandbox projection** — compatibility/display representation that may be lossy;
4. **cold/reload semantics** — whether inspecting/reloading a child can replace its parent-derived execution policy with caller/default settings;
5. **direct spawn override** — whether `spawn_agent` itself accepts a sandbox argument.

## Source priority

Primary sources:

- official OpenAI Codex App Server documentation in `openai/codex`;
- official `openai/codex` source and merged commit history;
- official OpenAI sandbox/security documentation.

Secondary issue/community evidence is not required for the core conclusion.

Volatile claims are pinned to the exact versions/commits below.

## Version identities

### Exercised T055 host

```text
Codex CLI:  0.149.0
App Server: 0.149.0
release commit: 758ef40f50c1a458425c7cfbf1eb12cbc07af0b0
release tag date: 2026-08-20
```

### R008 stable reference

```text
Codex: 0.153.4
release commit: 3d2ee51ca2d5db578f328aa75e20aa22c0197c9a
published: 2026-09-04
```

### Current source inspected

```text
openai/codex main:
ddf04ad26789d040f9ef6a96736f76602e35a6cc
```

## Finding 1 — T055's `workspaceWrite` receipt does not prove the child originally executed with widened write authority

T055 observed:

```text
parent lifecycle sandbox: readOnly
child resume sandbox: workspaceWrite
child writableRoots: []
```

Under the frozen T055 contract, that correctly failed the receipt gate: an explicit `workspaceWrite` compatibility value cannot be reinterpreted as `readOnly` merely because `writableRoots` was empty.

R009 adds an important causal boundary: the post-run 0.149.0 child `thread/resume` receipt is not sufficient evidence that the child **originally executed** under workspace-write.

Two official implementation facts support that boundary:

1. spawned children already inherited the live parent permission snapshot in 0.149.0;
2. a later change specifically fixed how unloaded Multi-Agent V2 children are reloaded/resumed so their runtime remains governed by the parent.

Therefore T055 remains a valid **observability failure**, but its receipt must not be upgraded into a claim that spawn-time child sandbox inheritance itself was unsafe.

## Finding 2 — 0.149.0 already copied the live parent permission profile into spawned children

Both the 0.149.0 source and current source implement the child spawn configuration through `build_agent_spawn_config` / `apply_spawn_agent_runtime_overrides`.

The implementation explicitly states that spawned child configuration refreshes runtime-owned fields including:

- approval policy;
- sandbox/permission state;
- cwd;
- model/reasoning state.

The core operation is a trusted snapshot copy from the parent turn:

```text
turn.config.permissions.permission_profile_state().snapshot()
  -> child config.permissions.set_permission_profile_from_session_snapshot(...)
```

This means the intended spawn-time model is parent-derived permission inheritance, not an independent child default.

Relevant official source:

- `openai/codex/codex-rs/core/src/tools/handlers/multi_agents_common.rs`
- 0.149.0 release commit `758ef40f...`
- current main `ddf04ad...`

Historical regression commit:

```text
7f571396c8819d7f4c4486ed1e967e40a2c9ffae
fix: sync split sandbox policies for spawned subagents (#14650)
2026-03-14
```

Its stated purpose was to reapply live filesystem/network sandbox policies when building spawned subagent configs and keep child sessions aligned with the parent turn after role-layer reloads.

## Finding 3 — direct `spawn_agent` sandbox override is not the intended surface

Current Multi-Agent V2 spawn arguments include task/message, role/type, model, reasoning effort and context-fork controls. They do not expose a direct sandbox argument.

The supported design instead derives the child's runtime permission policy from the parent turn and reapplies it after role/model layering.

R009 therefore rejects a successor design that attempts to add or emulate a direct per-spawn sandbox override.

The correct control point is the parent thread/turn permission profile.

## Finding 4 — profile IDs are the preferred receipt path; legacy `sandbox` is compatibility/display fallback

The App Server lifecycle API supports an experimental `permissions` selector by profile ID. Official documentation says to prefer this path over the legacy `sandbox` shorthand.

Reserved built-in IDs include:

```text
:read-only
:workspace
:danger-full-access
```

`ThreadStartResponse`, `ThreadResumeResponse` and `ThreadForkResponse` expose:

```text
activePermissionProfile
```

when a named or implicit built-in permission-profile identity is known.

The official implementation history explicitly warns that the lifecycle `sandbox` response is a compatibility/display fallback, not the full permission profile.

Relevant commit:

```text
83bbb4f32660c9246e90da92e664e2e69401c07b
app-server: stop returning thread permission profiles (#22792)
2026-05-15
```

Its rationale states that clients should round-trip active profile identity and that treating a response-derived legacy sandbox projection as a new local profile can lose restrictions and widen permissions.

Related commit:

```text
3fd79b7986b8019acb35a8e3a28ae32b67ca31ac
app-server: use profile ids in v2 permission params (#23360)
2026-05-18
```

The server owns profile resolution; clients select IDs and observe `activePermissionProfile` provenance.

Implication for T055:

- the parent was started with legacy `sandbox=readOnly` rather than `permissions=":read-only"`;
- a legacy selection can legitimately have no active profile ID;
- therefore T055 did not exercise the strongest supported provenance path available even in 0.149.0.

This does not invalidate T055. T055 followed its frozen contract and correctly failed on the receipt actually obtained.

## Finding 5 — 0.153.4 contains a material child reload/resume fix absent from the exercised 0.149.0 release

The decisive version delta is:

```text
d21794d6ba794673f2f754cc01bdb7dabc538f8c
Reload Multi-Agent V2 children through their parent (#40477)
2026-08-24
```

This commit is after the 0.149.0 release tag date (2026-08-20) and before the 0.153.4 release (2026-09-04).

Its stated motivation matches the T055 observability risk directly:

- Multi-Agent V2 children are parent-owned at runtime;
- directly resuming an unloaded child could rebuild it from caller-provided settings instead of the parent's current authority.

The fix:

- routes unloaded child reloads through the loaded immediate parent;
- rejects direct cold resume when the real parent cannot own the reload;
- preserves recorded child model/provider/reasoning/role;
- **inherits the parent's execution policy** and MCP extensions;
- validates/intersects permission/environment state;
- adds app-server child-resume coverage.

Official 0.153.4 App Server documentation now states:

```text
Parent-owned Multi-Agent V2 children are an exception:
thread/resume ignores configuration overrides and reattaches to the existing child.
An unloaded child is reloaded through its actual, currently loaded parent using parent-derived configuration.
```

The 0.149.0 App Server documentation inspected for R009 does not contain this parent-owned child exception.

This is a materially changed supported surface under O203's reconsideration rule.

## Finding 6 — why the 0.153.4+ combination is stronger than merely repeating T055

A valid successor qualification must combine **both** corrections:

```text
A. parent selection
   permissions = ":read-only"
   rather than legacy sandbox = readOnly

B. child inspection/reload semantics
   Codex >= 0.153.4 / includes #40477
   so an unloaded parent-owned V2 child is reloaded through its real parent
```

Using only A on 0.149.0 would leave the known child-resume authority gap in place.

Using only B while still selecting the parent via legacy sandbox would leave `activePermissionProfile` provenance potentially unavailable.

The paired design supplies:

- a stable, reserved read-only profile identity at the parent;
- parent-derived child permission state at spawn;
- parent-owned child reload semantics;
- a supported `activePermissionProfile` receipt after reattachment;
- the existing T055 child identity, usage and duration surfaces.

## Finding 7 — the parent must remain loaded during child reattachment

The 0.153.4+ contract deliberately rejects owner-controlled child cold resume when the actual parent is unavailable.

A successor qualification must therefore:

1. start the instrumented parent;
2. keep the parent loaded/alive;
3. spawn exactly one child;
4. discover the child;
5. inspect/reattach the child while the parent remains loaded;
6. capture the child lifecycle permission receipt;
7. only then close/dispose the synthetic topology.

This prevents a test harness from accidentally exercising an unsupported orphan-child reload path.

## Finding 8 — `activePermissionProfile=:read-only` is a provenance receipt, not provider inference

For the built-in profile, the official protocol defines `:read-only` as the reserved built-in read-only permission-profile identity.

A successor may therefore accept:

```text
activePermissionProfile.id == ":read-only"
```

as the server-authored provenance receipt for the active permission profile, provided:

- the parent was explicitly started with that ID;
- the child is real and parent-owned;
- the version includes #40477 semantics;
- the child receipt is obtained through the supported App Server lifecycle path;
- no contradictory supported permission receipt indicates broader authority.

The legacy `sandbox` projection should be recorded as a compatibility cross-check, not treated as the primary provenance field.

If `activePermissionProfile` is null, differs from `:read-only`, or the legacy sandbox explicitly contradicts the profile in a way that cannot be explained by documented projection semantics, the successor must fail closed.

## Finding 9 — runtime write probing is unnecessary for qualification

R009 does not recommend intentionally attempting a write from the child merely to prove denial.

Reasons:

- the target is observability/provenance, not destructive sandbox penetration testing;
- OS-specific write attempts add confounds;
- a supported server-authored active profile receipt plus version-pinned parent-owned inheritance is the appropriate protocol-level evidence;
- attempting a write could create side effects if the very mechanism under test regressed.

A successor should instead verify no tracked mutation and rely on the supported permission receipt.

## Finding 10 — 0.153.4 remains version-pinned, not timeless authority

Codex host semantics are volatile. T056 must not simply accept `>=0.153.4` forever without inspecting the installed native schema/help.

The evaluation should require:

- installed version at least 0.153.4 **or** a later stable/current version whose native App Server schema still exposes the required fields;
- native confirmation that `permissions`, `activePermissionProfile`, child relationship discovery and token usage surfaces are present;
- no assumption that later versions preserve exact field semantics if native schema/docs disagree.

If the installed host is still 0.149.0, T056 must stop before provider-backed probing. The Executor must not globally upgrade Codex to make the evaluation pass.

## Official OpenAI security boundary

OpenAI's public security guidance treats sandboxing as the technical execution boundary for where Codex can write and whether it can access the network. Official material distinguishes `read-only` and `workspace-write` modes and describes OS-enforced propagation of sandbox restrictions to descendant processes.

Relevant current public sources:

- https://openai.com/index/running-codex-safely/
- https://openai.com/index/building-codex-windows-sandbox/

These sources support the importance of preserving an explicit non-write sandbox boundary, but the child-specific inheritance conclusion rests on the version-pinned Codex implementation and App Server contract above.

## Research conclusion

R009 finds a **materially changed supported surface** that justifies one new narrow qualification.

The material change is not a new direct child sandbox override. It is the combination of:

1. preferred profile-ID selection and `activePermissionProfile` provenance;
2. existing spawn-time parent permission snapshot inheritance;
3. post-0.149 child reload fix #40477, included in 0.153.4, that forces parent-owned V2 child reattachment/reload through the actual parent and inherits parent execution policy.

Therefore:

```text
R009 Research-State: COMPLETE
R009 Decision-State: EVALUATING
Evaluation: T056
```

T056 is authorized as a **new, version-gated read-only child observability requalification**, not a rerun of T055.

## What R009 does not authorize

R009 does not:

- qualify the measurement surface by itself;
- reactivate R007;
- authorize a corrected routing pilot;
- authorize any child write-capable routing;
- change D055;
- authorize a global Codex upgrade by the Executor;
- treat legacy `sandbox` as equivalent to `activePermissionProfile`;
- claim backend-served model identity;
- claim token or cost savings.

Only an accepted T056 `QUALIFIED` result may close the R008/R009 measurement blocker and permit the Orchestrator to reconsider R007 under a separate persisted transition.

## Source ledger

Version-pinned official sources used in this research:

- `openai/codex@758ef40f50c1a458425c7cfbf1eb12cbc07af0b0` — Codex 0.149.0 release source;
- `openai/codex@3d2ee51ca2d5db578f328aa75e20aa22c0197c9a` — Codex 0.153.4 release source;
- `openai/codex@ddf04ad26789d040f9ef6a96736f76602e35a6cc` — current source inspected 2026-09-05;
- `7f571396c8819d7f4c4486ed1e967e40a2c9ffae` / PR #14650 — spawned sandbox sync;
- `83bbb4f32660c9246e90da92e664e2e69401c07b` / PR #22792 — legacy lifecycle sandbox as compatibility fallback / active profile identity boundary;
- `3fd79b7986b8019acb35a8e3a28ae32b67ca31ac` / PR #23360 — profile-ID client/server contract;
- `d21794d6ba794673f2f754cc01bdb7dabc538f8c` / PR #40477 — parent-owned V2 child reload fix;
- `codex-rs/core/src/tools/handlers/multi_agents_common.rs` — parent permission snapshot inheritance;
- `codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs` — current spawn argument/control surface;
- `codex-rs/app-server/README.md` — lifecycle permission and child-resume contract;
- `codex-rs/protocol/src/models.rs` — built-in profile identifiers and `ActivePermissionProfile` semantics.