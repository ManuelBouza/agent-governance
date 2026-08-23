# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O141  
Canonical-Branch: `develop`  
Current-Work-Unit: D053 native SDD A2/T034 executable-materialization gate under Orchestrator review/integration  
Chat-Closure: KEEP_CURRENT_CHAT

## Completed

- T033 native-Windows portability and its fresh-clone baseline remain closed/accepted.
- Human Owner approved D053 on 2026-08-23.
- D053 is `ACCEPTED`: native/tool-neutral, spec-anchored, brownfield delta-first SDD with proportional `COMPACT / STANDARD / ASSURED` coverage and `ADDED / MODIFIED / REMOVED / PRESERVED` deltas.
- D053 single-owner stage authority remains controlling:

```text
1 Explore / Frame           -> Orchestrator
2 Specify                   -> Orchestrator
3 Design                    -> Orchestrator
4 Plan & Trace              -> Orchestrator
5 Implement                 -> Executor for authorized technical implementation
6 Code Review & Verify      -> Executor for that technical implementation
7 Converge/Accept/Evolve    -> Orchestrator
```

- PR #184 integrated D053 acceptance plus `docs/SDD-ADOPTION-PLAN.md` at `0c0ecdcc8d19492bed9a0fbaa1751f845e7ddfa4`.
- A1 semantic protocol adoption was reviewed and integrated by PR #185 into `develop` as `6d5c24d9641177a6556c7b475e53c4716fb024b4`.
- A1 added `governance-core/SDD.md`, aligned source/consumer lifecycle ownership, Task Contracts/handoffs, coexistence, routing, trace/re-entry semantics and advanced the Core protocol to `1.14.0`.
- A1 changed only Markdown. No Executor was used.
- After A1 integration, A2 inspected current runtime/package/bootstrap/schema/test behavior and found executable work is required.
- A2 found the minimal required runtime/package gap: `src/agent_governance/engine.py` has a closed required-Core inventory that does not contain `SDD.md`, while integrated `GOVERNANCE.md` routes it and `_validate_core()` requires route/inventory equality.
- A2 confirmed the self-contained artifact builder already generically copies all `governance-core/*.md`; no special SDD package copier is needed.
- A2 confirmed current deterministic task mechanics do not require parsing the newly expanded SDD sections in `TASK.template.md`; task detail remains Markdown-native beyond existing identity/state metadata.
- A2 confirmed no current consumer/runtime handoff JSON schema exists and no new handoff schema is required merely because A1 added Code Review & Verify/trace semantics.
- A2 found the existing Consumer Governance eval still has obsolete missing-provider semantics: `no_sdd -> refuse_unsolicited_sdd`. D053 requires native SDD fallback while refusing unsolicited *external* SDD installation.
- A2 authored `docs/tasks/T034-native-sdd-executable-materialization.md` with `SDD-Profile: ASSURED` and `Test-Authorship-Mode: mixed`.
- A2 authored the D052 Orchestrator-owned conformance asset `tests/test_t034_native_sdd_conformance.py`, Oracle `T034-NATIVE-SDD-MATERIALIZATION`, revision `T034-A2-v1`.
- T034 freezes missing-provider behavior as `use_native_sdd` + `refuse_unsolicited_external_sdd`, with explicit `native_sdd_fallback` + `no_unsolicited_external_sdd` surface tags.
- T021/T022 remain paused and their represented contracts/history were not rewritten.

## Controlling References

For the current A2/T034 gate:

- `docs/decisions/D053-native-spec-driven-development.md`
- `docs/SDD-ADOPTION-PLAN.md`
- `governance-core/SDD.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/CONFORMANCE-ORACLE-CONTRACT.md`
- `docs/tasks/T034-native-sdd-executable-materialization.md`
- `tests/test_t034_native_sdd_conformance.py`

Do not preload T021.

## Active Remote Artifacts

```text
last verified develop       = 6d5c24d9641177a6556c7b475e53c4716fb024b4
A2/T034 gate branch         = test/t034-native-sdd-conformance-gate
T034 task                   = docs/tasks/T034-native-sdd-executable-materialization.md
T034 implementation branch = feat/t034-native-sdd-executable-materialization
T034 handoff                = handoffs/T034-executor-handoff.json
T034 oracle                 = tests/test_t034_native_sdd_conformance.py
T034 oracle revision        = T034-A2-v1
T034 oracle freeze          = DRAFT until integrated into canonical develop
D053                        = ACCEPTED

T033 status                 = ACCEPTED
T021 task                   = docs/tasks/T021-consumer-profile-abstraction-zero-drift.md
T021 review                 = docs/reviews/T021-R1.md
T021 branch                 = refactor/t021-consumer-profile-abstraction
T021 historical HEAD        = 969e2130ca9abb27c6ae5ad830923582f45b8a2f
```

Resolve the current A2 gate branch/PR head from GitHub immediately before integration. Do not treat the branch-local Task Contract/oracle as executable authority until the exact content is reachable from canonical `develop`.

## A2 Decision Boundary

T034 is intentionally narrow.

Required:

- extend the existing closed Core inventory/version map with `SDD.md` / `SDD-Version`;
- align deterministic Core/package Protocol 1.14.0 expectations;
- synchronize the existing T015 missing-provider corpus/grader/self-test semantics to the frozen T034 native-fallback oracle;
- prove source-layout bootstrap/validate, self-contained artifact behavior, trigger-corpus semantics and canonical native-Windows verification.

Not authorized without SDD re-entry:

- new SDD commands/state/lifecycle/queue;
- external SDD dependencies;
- a new deterministic parser/schema for SDD task sections;
- a new handoff JSON schema/validator;
- broader coexistence reclassification;
- D053 stage-ownership changes;
- T021/T022 changes.

## Executor Launch Boundary

No Executor may start while the T034 gate is only on the topic branch.

After integration:

1. reverify canonical `develop` and confirm T034 + exact oracle are reachable;
2. Oracle `T034-A2-v1` becomes `FROZEN` for execution;
3. establish a safe fresh/rematerialized native-Windows checkout; the stale pre-T033 CRLF checkout is prohibited;
4. because A1 modified `AGENTS.md`, the first T034 launch MUST use the D043 conditional reload line after synchronization and before the Task Contract pointer;
5. launch only the canonical minimal Task Contract prompt;
6. Executor may not edit the frozen T034 conformance asset or committed Markdown.

## Next Action

1. Reverify current `develop` immediately before PR/integration mutation.
2. Review the complete `test/t034-native-sdd-conformance-gate` diff against D053, D052, the A2 Design and oracle contract.
3. Open/integrate the T034 gate PR to `develop` only if the Task Contract and frozen oracle are coherent and no implementation changes leaked into the gate.
4. Reverify `develop` after integration.
5. Refresh this checkpoint to the post-integration T034 `READY` / oracle `FROZEN` frontier.
6. Establish the safe native-Windows Executor checkout and launch T034 with the required D043 `AGENTS.md` reload line.
7. Do not resume T021/T022 automatically.

## Next Chat Minimum Load

Until the T034 gate is integrated, load only:

- accepted D053;
- `docs/SDD-ADOPTION-PLAN.md` on the gate branch;
- `docs/tasks/T034-native-sdd-executable-materialization.md`;
- `tests/test_t034_native_sdd_conformance.py`;
- the gate PR diff/status;
- concrete runtime/test files only when required to resolve a review conflict.

After gate integration, a new chat should load only T034 plus its frozen oracle and exact implementation-surface files needed for Executor launch/review.

## Do Not Load Or Do

Do not restore dual SDD-stage ownership; let Executor-private planning/SDD become authoritative Design/Plan; install OpenSpec/Spec Kit/Kiro as a required dependency; create a parallel SDD lifecycle; perform full brownfield spec backfill; launch an Executor before T034/oracle integration; edit the frozen oracle during Executor work; invent task/handoff schemas without SDD re-entry; silently rewrite historical Task Contracts; resume T021/T022 automatically; use the stale CRLF checkout for executable work; write directly to `main`/`develop`; or allow the Executor to redefine normative specification/Design/acceptance semantics.
