# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O145  
Canonical-Branch: `develop`  
Current-Work-Unit: T034 native SDD executable materialization READY for Executor launch under D054/RB001  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- PR #188 contained the two accidental direct-`develop` noop writes without rewriting history; L007 remains `CONTROL_PLANNED`.
- PR #189 integrated D054/T035 planning as `9bd77ee05db878dfc383b4628f563d17e89327de`.
- D054 is accepted architecture for Executor-owned execution mechanics: CLI/API/SDK/Git/uv/PowerShell/Bash/cloud/database/cluster/deployment/SSH/remote operations are selected and executed by the abstract Executor inside the current D033 envelope.
- Human/Orchestrator authority remains semantic: outcome, target/effect/resource/privilege/credential/network boundary, controlling Design/Plan, semantic runbooks/checkpoints, approval gates and acceptance evidence.
- `docs/runbooks/RB001-source-executor-checkout-bootstrap.md` is now the source-maintainer semantic runbook for safe checkout/toolchain bootstrap.
- Until T035 native recipe persistence exists, unknown adapter syntax is resolved from project-native or installed/version-specific help and official vendor/API documentation; successful newly resolved operations remain provisional handoff evidence rather than durable VERIFIED recipes.
- T035 remains `BLOCKED` until T034 is accepted/integrated on a green canonical baseline and a separate post-T034 Orchestrator-owned D052 oracle gate is integrated.
- The T035 oracle is intentionally not yet authored/frozen because integrating a deliberately red T035 oracle before T034 would invalidate T034's required full canonical pytest acceptance.
- T021/T022 remain paused.

## Current Remote State

```text
last verified develop             = 9bd77ee05db878dfc383b4628f563d17e89327de
D054/T035 planning PR              = #189 — MERGED
D054 decision                      = docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md
operation-resolution contract      = docs/RUNBOOK-OPERATION-RESOLUTION.md
source bootstrap runbook           = docs/runbooks/RB001-source-executor-checkout-bootstrap.md

T034 status                        = READY
T034 task                          = docs/tasks/T034-native-sdd-executable-materialization.md
T034 oracle                        = tests/test_t034_native_sdd_conformance.py
T034 oracle revision               = T034-A2-v1 — FROZEN
T034 expected branch               = feat/t034-native-sdd-executable-materialization
T034 remote branch                 = ABSENT at last check
T034 handoff                       = handoffs/T034-executor-handoff.json

T035 status                        = BLOCKED on T034 + future oracle gate
T035 task                          = docs/tasks/T035-runbook-operation-resolution-readiness.md
T035 oracle                        = NOT YET AUTHORED/FROZEN

T021/T022                          = PAUSED
```

Immediately before actual Executor launch, re-resolve canonical `develop` and the T034 branch state. A stale local branch named `develop` is not sufficient baseline evidence.

## T034 Execution Boundary

T034 remains exactly the integrated Task Contract; D054 changes execution mechanics ownership, not T034 product semantics.

Required implementation remains narrowly bounded to:

- add `SDD.md` / `SDD-Version` to the existing closed deterministic Core inventory;
- align deterministic Core/package expectations to integrated Protocol `1.14.0`;
- synchronize the existing T015 `no_sdd` corpus/grader/self-tests to frozen native fallback semantics:
  - `use_native_sdd`
  - `refuse_unsolicited_external_sdd`
  - `native_sdd_fallback`
  - `no_unsolicited_external_sdd`;
- preserve self-contained packaging/source independence and the stable CLI v1 surface;
- run the frozen T034 oracle, focused suites and complete native-Windows canonical Ruff/pytest verification;
- persist `handoffs/T034-executor-handoff.json`, perform Code Review & Verify, commit and make the one planned final push under D048.

Not authorized without SDD re-entry:

- edits to `tests/test_t034_native_sdd_conformance.py`;
- committed Markdown edits by the Executor;
- new SDD command/state/lifecycle/queue;
- external SDD dependency;
- new task-section parser/schema or handoff schema;
- T021/T022 changes;
- direct `develop`/`main` writes or force-push of represented history.

## D054 / RB001 Bootstrap Rule for T034

The Executor, not the Human, owns the concrete Git/uv/PowerShell/shell mechanics required to establish the safe native-Windows T034 baseline.

The Executor must:

1. follow `docs/runbooks/RB001-source-executor-checkout-bootstrap.md` semantically;
2. preserve any unrepresented local work and fail closed rather than destructively reset/overwrite it;
3. prove local base equals current canonical `origin/develop` containing the exact T034 contract/oracle;
4. reload current `AGENTS.md` because the governing integrated history changed `AGENTS.md`;
5. resolve unknown adapter syntax from installed/version-specific help or official documentation rather than model memory/chat snippets;
6. keep newly resolved operation evidence provisional until T035 exists;
7. use only D033-authorized target/effect/credential/network/privilege boundaries.

No Human command-by-command copy/paste is part of the normal launch path.

## Canonical Launch Prompt

Use the current `docs/TASK-CONTRACTS.md` minimal transport semantics:

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Synchronize the canonical remote and ensure the local develop baseline used for bootstrap is current with origin/develop. Preserve local/uncommitted work; if a safe current baseline cannot be established, stop and report BLOCKED rather than using stale repository state.

AGENTS.md changed in the governing integrated change; reload current AGENTS.md from this baseline before loading the Task Contract.

Then load and execute the authoritative Task Contract:
docs/tasks/T034-native-sdd-executable-materialization.md

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

For source checkout/toolchain bootstrap and other execution mechanics, follow the applicable semantic runbook, including docs/runbooks/RB001-source-executor-checkout-bootstrap.md. Resolve missing adapter syntax from project-native or installed/version-specific help and official vendor/API documentation under D054; do not delegate routine command execution to the Human.

Complete the required implementation, Code Review & Verify, verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

The runbook sentence is a routing pointer to integrated authority, not a duplicate command specification.

## Next Action

1. Integrate this O145 checkpoint refresh through its short-lived Markdown PR.
2. Reverify canonical `develop` after that merge and confirm `feat/t034-native-sdd-executable-materialization` is still absent/unstarted.
3. In the ChatGPT desktop app Codex Executor surface, open the safe native-Windows source project and send the canonical launch prompt above.
4. The Executor performs all routine Git/uv/PowerShell/shell operations itself under D054/RB001.
5. Await only the terminal pointer fields from the Executor.
6. Then perform remote D053 Converge/Accept review from GitHub.
7. Do not resume T021/T022 or author/freeze the T035 oracle until T034 is accepted/integrated and the canonical baseline is green.

## Next Chat Minimum Load

Until T034 returns a terminal handoff, load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint;
- `docs/tasks/T034-native-sdd-executable-materialization.md`;
- `tests/test_t034_native_sdd_conformance.py`;
- `docs/runbooks/RB001-source-executor-checkout-bootstrap.md`;
- exact T034 implementation/handoff branch state when it exists;
- D054 only when resolving a concrete execution-boundary conflict.

Do not reconstruct prior SDD adoption history or preload T021/T022 when these repository artifacts are sufficient.

## Do Not Load Or Do

Do not hand routine CLI/API/PowerShell/Bash commands to the Human as the default path; do not make recipe syntax execution authority; do not guess unknown commands from model memory; do not bypass target/identity/privilege/credential/network controls; do not disable TLS/host-key/security controls for convenience; do not modify the frozen T034 oracle; do not absorb T035 into T034; do not author/freeze the T035 oracle before T034 acceptance; do not resume T021/T022 automatically; do not write directly to `main`/`develop`; and do not treat L007 containment as verified prevention.
