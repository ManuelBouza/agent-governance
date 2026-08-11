# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O024  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — has returned `PARTIAL` from the Agente de IA Ejecutor.

Executor return reviewed:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: d3b8fbfe71467e19a2225bb5fd779c82930214bd
```

Remote branch HEAD exactly matched the visible HEAD.

T004 Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Active rework directive:

`docs/reviews/T004-R1.md`

Expected executor branch remains:

`eval/d032-agent-capability`

Expected handoff remains:

`handoffs/T004-executor-handoff.json`

T004 is **not accepted** and no implementation PR is authorized.

## T004 PD5 R1 Findings

D029 identity is valid for the reviewed return:

- `base_sha`: `f7182fe06d0324be424617fc4764528704f51e4c`;
- implementation anchor: `d1961944e2a6c00ff5c35f2eb7dc11c3d151535a`;
- final pushed branch HEAD: `d3b8fbfe71467e19a2225bb5fd779c82930214bd`;
- the only commit after the implementation anchor changes only `handoffs/T004-executor-handoff.json`.

Branch delta from the controlling T004 base is limited to:

- `evals/d032/adapters/opencode.py`;
- `evals/d032/cases.json`;
- `evals/d032/runner.py`;
- `tests/test_d032_agent_eval_harness.py`;
- `handoffs/T004-executor-handoff.json`.

No Markdown, dependency or toolchain configuration drift is present on the executor branch.

Reported deterministic verification is green:

- pre-mutation baseline: `114 passed`;
- focused harness: `22 passed`;
- final canonical suite: `136 passed`;
- Ruff check/format green.

However the required real model baseline did not execute successfully:

- required independent sessions: 18;
- required turns: 21;
- completed sessions: 0;
- completed turns: 0;
- persisted result artifact: none.

The executor correctly failed closed and did not fabricate transcripts or weaken isolation.

## Concrete T004 Adapter Defect

The reviewed OpenCode adapter creates the temporary custom agent `d032-eval` without a `description`.

Current OpenCode agent documentation for the installed-era interface declares `description` a required custom-agent option. The implementation therefore has a concrete adapter-configuration defect that must be corrected before the remaining child failure can be attributed to the host/provider/model.

The existing focused tests verify record/corpus/security invariants but do not prove that the generated temporary custom-agent configuration resolves a runnable `d032-eval` before the provider call.

T004-R1 therefore requires:

1. add a non-empty custom-agent `description`;
2. explicitly make the eval agent `primary` unless the installed interface proves another mode is required;
3. preserve deny-all isolation;
4. add a read-only adapter configuration smoke/preflight under the exact temporary environment, using a documented capability such as `opencode agent list`;
5. improve sanitized fail-closed diagnostic classification;
6. rerun the full 18-session / 21-turn real baseline only after adapter preflight passes;
7. if the corrected adapter still cannot produce a response, return `PARTIAL` with exact sanitized failure evidence rather than weakening isolation or silently changing provider/model.

Semantic D032 grading remains unavailable until real transcripts exist.

## Accepted Architecture Frontier — D033 through D036

Architecture work accepted while T004 was running remains non-retroactive to T004:

- `docs/decisions/D033-execution-access-control-plane.md` — execution authorization by actor/target/effect/privilege/credential/resource scope;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — reusable runbooks + terminal/platform-neutral execution adapters;
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md` — current/versioned security authority, known-bad anti-regression and independent verification;
- `docs/decisions/D036-existing-system-assurance-audit-mode.md` — evidence-first audits of existing systems across implementation quality, security, configuration and applicable practices.

Consolidated overviews:

- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`;
- `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`.

D033–D036 are accepted architecture only; they are not yet integrated into Governance Core/protocol and MUST NOT broaden the running T004 contract.

Combined future stack:

```text
D032 quality/interaction
        ↓
D035 security authority/freshness
        ↓
D036 assessment / independent verification
        ↕
D033 execution authorization
        ↓
D034 runbook + terminal-neutral adapter
```

## Orchestrator Direct-Write Incident During T004-R1 Persistence

While preparing this R1 review, ChatGPT accidentally created `docs/reviews/T004-R1.md` with content `placeholder` directly on `develop`.

Unauthorized direct-write commit:

`197ce3fad02a69baf99238beb9859280a137a681`

It was immediately corrected by deleting the placeholder directly from `develop`:

`52ae6fb5126517ea19c8d00918e7b148c17f146a`

The corrective commit removes exactly the accidental placeholder. No T004/Core/runtime/configuration content was intentionally changed by the incident. Preserve this history for audit; do not rewrite it unless the Human Owner explicitly authorizes history repair.

The proper T004-R1 persistence uses the Markdown topic branch:

`docs/t004-r1-opencode-adapter-preflight`

## Open Questions / Blockers

Active blocker: T004 cannot reach semantic PD5 because its OpenCode child execution produced no valid response/event stream.

First required correction is the documented custom-agent configuration defect and adapter preflight defined by T004-R1.

If corrected/preflighted OpenCode still fails, Strategy must decide from sanitized evidence whether the next step is:

- a bounded OpenCode/provider compatibility diagnosis; or
- another execution adapter behind the same adapter-neutral T004 contract.

Do not make that decision before R1 evidence exists.

The source product remains not stable/release-ready.

## Next Action

1. Integrate this T004-R1 Markdown review/checkpoint through the normal Markdown PR flow if its diff is limited to `docs/reviews/T004-R1.md` + this checkpoint.
2. Send the executor a minimal prompt to continue the existing `eval/d032-agent-capability` branch and apply only T004-R1.
3. On the next executor return, validate remote HEAD and D029 identity.
4. If a complete 21-record baseline exists, perform semantic PD5 over every persisted response and verify the 18-session cardinality/isolation evidence.
5. If still `PARTIAL`, review exact sanitized diagnostics before authorizing any provider/model/adapter change.
6. Only after T004 is resolved, design the D033–D036 Core-integration frontier with a fresh D032 Primary Solution Diagram and quality/security triage.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
2. load `docs/reviews/T004-R1.md`;
3. if the executor has returned again, fetch `handoffs/T004-executor-handoff.json` and the exact remote branch/results at the reported final HEAD;
4. load D029 for handoff identity review if needed;
5. load D032 Core files only when semantic transcript grading is possible;
6. load D033–D036 only if execution/security/audit architecture planning becomes the active work after T004.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not accept T004 without the real 18-session / 21-turn baseline and ChatGPT semantic PD5.
- Do not fabricate/massage transcripts or use model self-grading to complete T004.
- Do not weaken tool denial, disposable-environment isolation or source-worktree immutability to make OpenCode run.
- Do not silently switch provider/model on R1.
- Do not retroactively apply D033–D036 to change T004 scope.
- Do not open/merge a T004 implementation PR while T004 remains `PARTIAL`.
- Do not modify Core/protocol for D033–D036 until T004 is resolved and a separate READY Task Contract aligns semantics/code/tests.
- Do not hide or rewrite the direct-write incident without explicit Human authorization.
- Do not declare the source product stable/release-ready.