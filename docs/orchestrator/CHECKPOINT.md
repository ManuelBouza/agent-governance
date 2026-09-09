# Orchestrator Checkpoint

Checkpoint-ID: O260  
Date: 2026-09-09  
Current-Objective: T063 — adaptive worker routing requalification  
State: AUTHORIZED_AWAITING_HUMAN_CODEX_START  
Active-Executor: Codex  
Executor-Launch-State: AUTHORIZED / NOT_STARTED  
Coordinator-ID: `AG | agent-governance | T063 | root-1`  
Held-Work-Unit: T062 / T023 v15 Stage 6  
Held-State: HUMAN_HOLD_R32_UNCONSUMED  
Chat-Closure: KEEP_CURRENT_CHAT

## Canonical transition

Protected `develop` at launch-selection revalidation:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

O259 required an explicit selection between T063 and the held T062 line. After the alternatives were explained, the Human selected T063 (`correcto T063`).

That selection authorizes T063 launch preparation and execution. It does not resume T062.

Controlling launch authority:

```text
docs/reviews/T063-R2.md
```

Prelaunch interpretation correction remains:

```text
docs/reviews/T063-R1.md
```

## T063 launch profile

```text
Executor:        Codex
Surface:         Codex Local / native Windows
Session:         NEW
Coordinator-ID:  AG | agent-governance | T063 | root-1
Root model:      gpt-5.6-sol
Root effort:     medium
Codex CLI:       exactly 0.153.4
App Server:      exactly 0.153.4
Auth category:   chatgpt
```

Frozen scored matrix:

```text
P1 CONTROL:   gpt-5.6-sol   / medium
P1 ADAPTIVE:  gpt-5.6-luna  / medium
P2 CONTROL:   gpt-5.6-sol   / medium
P2 ADAPTIVE:  gpt-5.6-terra / medium
P3 CONTROL:   gpt-5.6-sol   / medium
P3 ADAPTIVE:  gpt-5.6-terra / high
```

No scored model/effort substitution is authorized.

The official stable Codex release and OpenAI model catalog were refreshed immediately before launch freeze. Stable remains 0.153.4 and the requested Sol/Terra/Luna model families support the frozen reasoning levels.

D071 prevents ChatGPT from directly interrogating or operating the Human's local Codex session. Therefore concrete host/account availability is checked as the Executor's first fail-closed preflight before any scored child. Missing D063 surface is `BLOCKED_MEASUREMENT_SURFACE`; requested/resolved mismatch is `BLOCKED_PROFILE_RESOLUTION`.

## Frozen evaluation baseline

T063 evaluates exactly:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

Expected evidence branch:

```text
test/t063-adaptive-worker-routing-requalification
```

At launch authorization this branch does not exist. Codex must create it from the exact frozen baseline after safe synchronization and use an exclusive T063 worktree.

Later launch Markdown on `origin/develop` is authority only and must not be merged/rebased/cherry-picked into the frozen evidence baseline merely to consume it.

## Frozen probe inputs

T063-R2 freezes all concrete inputs required by the Task Contract.

### P1

Six ordered Git paths at the frozen commit:

```text
.python-version
agent-governance-source.json
pyproject.toml
code-health.json
src/agent_governance/profile.py
src/agent_governance/source_adapter.py
```

Root computes Git-blob SHA and Git-object byte-size oracle independently before both arms.

### P2

Exact five-file package slice:

```text
src/agent_governance/__init__.py
src/agent_governance/artifact.py
src/agent_governance/engine.py
src/agent_governance/profile.py
src/agent_governance/source_adapter.py
```

Six ordered symbols:

```text
ArtifactBuildError
build_artifact
Profile
resolve_profile
SourceContext
_bootstrap
```

Dependency semantics remain static in-scope Python AST import edges only.

### P3

Seed source:

```text
src/agent_governance/profile.py
blob 1e3ae205b4350adc18a2f3f5d631dd739056ba34
```

Root creates a non-tracked ephemeral fixture with the single frozen fail-open mutation defined in T063-R2. Children receive only the fixture and generic review task, not the seed/oracle. Any oracle-authority read by a scored child invalidates the probe and stops the pilot.

## Experimental topology

T063-R1/R2 control:

```text
execution_target: CONTRACT_FIXED
underlying_delegation_eligibility: DELEGATED
```

Exactly six fresh children/turns form the normal scored set. First-attempt scores are immutable. Diagnostic escalation/rerun is allowed only exactly as T063 specifies and never rewrites the score.

Every measured App Server parent/child must satisfy D063 read-only/profile/identity/usage/duration/reroute receipts. The outer Coordinator may use only the minimum write authority needed to persist the two authorized JSON evidence files.

## Evidence and return

Normal committed delta from the frozen baseline is limited to:

```text
handoffs/T063-adaptive-worker-routing-telemetry.json
handoffs/T063-executor-handoff.json
```

No Executor-authored Markdown or product-source/config/test/schema mutation is authorized.

Terminal Human return shape:

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T063-executor-handoff.json
BRANCH: test/t063-adaptive-worker-routing-requalification
HEAD: <actual remote pushed HEAD>
```

Provider/model calls at checkpoint creation:

```text
0
```

## T062 held frontier

T023-R33 remains controlling. T062 is not resumed.

```text
scientific branch:               test/t023-skill-activation-topology-evals-v15
terminal Stage 5 HEAD:           3e0d0b71cf382db502e186622f40a23bcd915390
Candidate Freeze E:              5b025087bc7b6996f683a34fdd1ce441d3d6dd82
Holdout/oracle Freeze F:         5b8ac55980ecdbb6a2bf3784812b933647f2f13d
blocked Stage 6 evidence HEAD:   b9034e450f04fbc9736543425e531159d4b79d49
provider/model calls:            0
R32 continuation authority:      valid but unconsumed
R32 transport:                   PAUSED by T023-R33
```

Do not execute the old T062 R32 prompt while R33 controls.

## D061 / D062 authoring state

Launch authority was authored on:

```text
docs/t063-launch-authority
```

from exact protected base:

```text
69e910f329a2294c3b40df0f6ee983f9905f4677
```

Ruleset `22339910` was revalidated active for `main`/`develop`, with PR transport, deletion/non-fast-forward protection and no routine bypass actors.

## Other durable constraints

- T024 remains unauthorized until T023 selects a topology from valid evidence.
- T058 remains frozen by explicit Human decision.
- D066 intentional gaps remain unchanged.
- D071/D072/D073 control Human-mediated Codex transport/title handling.
- R007 remains `EVALUATING`; T063 execution cannot itself adopt global adaptive routing policy.

## Next Chat Minimum Load

After normal bootstrap (`develop`, `AGENTS.md`, this checkpoint), for T063 load only:

1. `docs/tasks/T063-adaptive-worker-routing-requalification.md`;
2. `docs/reviews/T063-R1.md`;
3. `docs/reviews/T063-R2.md`;
4. D063;
5. R018 only if a runtime/model-capability conflict appears.

For T062 resumption, instead follow the held-line instructions and revalidate R31/R32/R33 plus the scientific branch.

## Next Action

Human transport is next.

Start a **NEW** Codex session configured as specified above, use visible title:

```text
AG | agent-governance | T063 | root-1
```

and paste the complete T063 transport prompt emitted by ChatGPT with this launch authority.

After Codex terminates, return only its `STATUS / HANDOFF / BRANCH / HEAD` to ChatGPT for remote convergence.
