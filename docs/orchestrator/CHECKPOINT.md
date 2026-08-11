# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O025  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — remains `PARTIAL` after a second executor return.

Latest reviewed executor return:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: 1c11fb838ca228e9a1c5b465d5bce41cf380d36b
```

Remote branch HEAD exactly matched the visible HEAD.

T004 Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Historical R1 directive:

`docs/reviews/T004-R1.md`

Active R2 directive:

`docs/reviews/T004-R2.md`

Expected executor branch remains:

`eval/d032-agent-capability`

Expected handoff remains:

`handoffs/T004-executor-handoff.json`

T004 is **not accepted** and no implementation PR is authorized.

## T004 Second-Return Identity / Scope

D029 identity is valid:

- controlling T004 base remains `f7182fe06d0324be424617fc4764528704f51e4c`;
- latest implementation anchor: `dc5ddacec697947c311013ec0b5fb6f23daf426b`;
- final pushed branch HEAD: `1c11fb838ca228e9a1c5b465d5bce41cf380d36b`;
- the only commit after the implementation anchor changes only `handoffs/T004-executor-handoff.json`.

R1 implementation stayed within authorized eval/test/handoff surfaces:

- `evals/d032/adapters/opencode.py`;
- `evals/d032/cases.json`;
- `evals/d032/runner.py`;
- `tests/test_d032_agent_eval_harness.py`;
- `handoffs/T004-executor-handoff.json`.

No executor Markdown/dependency/toolchain configuration drift was found.

## T004 R1 Progress Accepted

R1 corrected the concrete custom-agent configuration defect:

- `d032-eval` now has a non-empty `description`;
- mode is explicitly `primary`;
- model is explicitly `openai/gpt-5.6-terra`;
- global and agent permissions remain deny-all;
- legacy per-tool disables remain defense in depth;
- disposable workspace/config/database isolation remains in place.

The exact temporary configuration now passes a no-model-call preflight through installed OpenCode `1.18.16`.

Reported verification:

- focused harness: `34 passed`;
- canonical suite: `148 passed`;
- Ruff check/format green;
- Python `3.13.14`;
- uv `0.11.33`;
- pytest `9.1.1`;
- Ruff `0.16.2`;
- OpenCode `1.18.16`.

No dependencies or global OpenCode/Gentle-AI/provider configuration changed.

## Remaining T004 Blocker

The required baseline still has:

- required independent sessions: `18`;
- required turns: `21`;
- completed sessions: `0`;
- completed turns: `0`;
- result artifact: none.

After successful R1 preflight, the first exact real child observed:

- process exit: non-zero (`1`);
- JSON events: exactly `1`;
- user-visible response: none;
- tool calls: zero.

A bounded diagnostic also failed without a response. No provider/model substitution or isolation weakening occurred.

The executor correctly failed closed; semantic D032 PD5 remains unavailable.

## T004 R2 Finding

The OpenCode adapter currently parses JSON events but does not preserve/classify the structured OpenCode `error` event before reducing the failure to event counts and heuristic stderr categories.

OpenCode `run --format json` emits session failures as JSON error events. R2 requires the adapter to extract only safe structured error identity before any provider/model/adapter decision.

Recent upstream OpenCode history contains GPT-5.6-family OAuth/model-transport compatibility defects, but this is only a hypothesis until the exact Terra error event is observed.

## T004 R2 Required Sequence

1. Keep the existing R1 preflight and isolation unchanged.
2. Add structured JSON error-event extraction/redaction with deterministic tests.
3. Establish only safe read-only metadata: OpenAI auth entry present/not present and exact Terra model advertised/resolvable.
4. Re-run exactly `A-plain` trial 1 first.
5. If the structured error identifies provider/model/auth/network/transport failure, stop `PARTIAL` and report it.
6. If still inconclusive, at most one minimal disposable deny-all control probe may distinguish provider path from eval-agent/context path.
7. No iterative diagnostic matrix.
8. Do not switch provider/model or OpenCode version and do not weaken isolation.
9. Only if the exact eval child succeeds may the complete 18-session / 21-turn baseline run.
10. Semantic fields remain `PENDING_CHATGPT` until ChatGPT PD5.

## Accepted Architecture Frontier — D033 through D036

Accepted architecture, not yet integrated into Governance Core/protocol:

- `docs/decisions/D033-execution-access-control-plane.md` — bounded execution authority;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — runbook-first platform/terminal-neutral execution;
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md` — current security authority, freshness, known-bad regression and independent verification;
- `docs/decisions/D036-existing-system-assurance-audit-mode.md` — evidence-first assurance audits of existing systems.

Consolidated overviews:

- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`;
- `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`.

These decisions MUST NOT retroactively broaden T004.

Future combined stack:

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

After T004 is resolved, design the first D033–D036 Core integration with a fresh D032 Primary Solution Diagram and quality/security triage before implementation.

## Orchestrator Direct-Write Audit History

Preserve these known accidental direct-write incidents; do not hide/rewrite them without explicit Human authorization.

### T002-R1 placeholder incident

- accidental direct `develop` commit: `6a3bff4f12850bd701fea624815e955231082afa`;
- corrective commit: `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.

### Architecture overview placeholder incident

- accidental direct `develop` commit: `a0e063344043fda53f55b8fcb5b03742a33a7185`;
- corrective commit: `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.

### T004-R1 placeholder incident

- accidental direct `develop` commit: `197ce3fad02a69baf99238beb9859280a137a681`;
- corrective commit: `52ae6fb5126517ea19c8d00918e7b148c17f146a`.

The proper T004-R1 review was later integrated through the Markdown PR flow.

## Open Questions / Blockers

Primary blocker: exact structured OpenCode child error is not yet preserved, so provider/model/auth/transport versus eval-agent/context failure is not yet proven.

Do not authorize a provider/model/OpenCode-version/adapter change until R2 structured evidence is reviewed.

The source product remains not stable/release-ready.

## Next Action

1. Integrate T004-R2 + O025 through the normal Markdown PR flow if the diff is limited to those two files.
2. Send the executor a minimal prompt to continue `eval/d032-agent-capability` and apply only T004-R2.
3. On return, verify D029 and inspect the structured error/result evidence.
4. If the exact A-plain child succeeds and a complete 21-record baseline exists, perform semantic PD5 over all transcripts.
5. If provider/model/transport incompatibility is proven, Strategy/Human chooses a separately authorized remediation: alternate model, OpenCode version adjustment or alternate adapter.
6. Only after T004 resolution, design D033–D036 Core integration.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
2. load `docs/reviews/T004-R2.md` (R1 only if historical comparison is needed);
3. if the executor has returned, fetch `handoffs/T004-executor-handoff.json` and exact branch files/results at the reported final HEAD;
4. load D029 only if identity mechanics need re-checking;
5. load D032 Core files only when semantic transcript grading is possible;
6. load D033–D036 only when post-T004 architecture planning becomes active.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not accept T004 without the real 18-session / 21-turn baseline and ChatGPT semantic PD5.
- Do not fabricate transcripts or use model self-grading.
- Do not weaken deny-all, disposable isolation or source-worktree immutability.
- Do not silently switch provider/model or OpenCode version.
- Do not copy/persist credentials or raw secret-bearing diagnostics.
- Do not run an unbounded diagnostic matrix.
- Do not open/merge a T004 implementation PR while T004 remains `PARTIAL`.
- Do not retroactively apply D033–D036 to broaden T004.
- Do not modify Governance Core/protocol for D033–D036 until T004 is resolved and a separate READY Task Contract exists.
- Do not hide/rewrite direct-write incidents without explicit Human authorization.
- Do not declare the source product stable/release-ready.