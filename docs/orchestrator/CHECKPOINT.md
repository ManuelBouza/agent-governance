# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O026  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — remains `PARTIAL` after a third executor return.

Latest reviewed executor return:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: eb20dc0fed2674190a82ef40aa0e02436c02ced4
```

Remote branch HEAD exactly matched the visible HEAD.

T004 Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Historical rework directives:

- `docs/reviews/T004-R1.md` — temporary-agent conformance/preflight;
- `docs/reviews/T004-R2.md` — structured child error diagnosis.

Active directive:

`docs/reviews/T004-R3.md` — catalog-compatible model reselection.

Expected executor branch remains:

`eval/d032-agent-capability`

Expected handoff remains:

`handoffs/T004-executor-handoff.json`

T004 is **not accepted** and no implementation PR is authorized.

## Third-Return Identity / Scope

D029 identity is valid:

- controlling T004 base remains `f7182fe06d0324be424617fc4764528704f51e4c`;
- latest implementation anchor: `edc7fe186c0c84f6f30e3a2d8bbb4022ac609356`;
- final pushed branch HEAD: `eb20dc0fed2674190a82ef40aa0e02436c02ced4`;
- the only commit after the implementation anchor changes only `handoffs/T004-executor-handoff.json`.

Executor scope remains limited to the authorized eval/test/handoff surfaces. No Markdown, dependency or global toolchain configuration drift is reported.

## R1 / R2 Progress Accepted

R1 fixed the temporary custom-agent contract and added a no-provider preflight:

- non-empty `description`;
- explicit `primary` mode;
- explicit selected model;
- global + agent deny-all permissions;
- disposable workspace/config/database;
- project/default-plugin/external-Skill/Claude-Code loading disabled;
- `opencode agent list --pure` preflight passes under OpenCode `1.18.16`.

R2 added safe structured error extraction/redaction and bounded diagnosis:

- OpenCode JSON `error` event is inspected before stderr fallback;
- secret/token/auth/URL/path-like strings are redacted in deterministic tests;
- malformed JSONL does not destroy valid structured error siblings;
- raw error events, stderr, credentials and environment dumps are not persisted;
- focused harness: `59 passed`;
- canonical suite: `173 passed`;
- Ruff check/format green.

No real transcript/result artifact has been fabricated.

## R2 Runtime Evidence

Required T004 baseline:

- independent sessions: `18`;
- turns: `21`.

Current completed evidence:

- completed sessions: `0`;
- completed turns: `0`;
- result artifact: none.

Read-only provider metadata under the intended pure OpenCode environment established:

- OpenAI auth entry present: `true`;
- selected model: `openai/gpt-5.6-terra`;
- exact selected model advertised/resolved by `opencode models openai --pure`: `false`.

After unchanged adapter preflight, exact `A-plain` trial 1 returned:

- process exit: `1`;
- one structured JSON error event;
- `error_name`: `UnknownError`;
- category: `unknown-runtime`;
- sanitized message: `Unexpected server error. Check server logs for details.`;
- response: none;
- tool calls: zero.

The single R2-authorized minimal-context differential control reproduced the same structured error class under the same provider/model and deny-all disposable isolation.

Therefore:

- the exact provider backend root cause is not proven;
- the eval agent/context is no longer the leading blocker;
- `openai/gpt-5.6-terra` is invalidated as the T004 baseline target for installed OpenCode `1.18.16` because it is not present/resolvable in the effective model catalog and both exact/control calls fail identically.

## T004 R3 Strategy Decision

Prefer the smallest correction: **reselect the explicit model from the effective OpenAI catalog while keeping OpenCode `1.18.16`, the adapter, provider, corpus, context and isolation unchanged**.

Do not upgrade/downgrade OpenCode and do not introduce an alternate adapter yet.

R3 selection is deterministic and read-only. Run `opencode models openai --pure` and choose the first exact advertised ID from:

1. `openai/gpt-5.6-sol`
2. `openai/gpt-5`
3. `openai/gpt-5-codex`
4. `openai/gpt-4.1`

If none is advertised, stop `PARTIAL` without a provider call.

The list is a selection rule, **not a runtime retry ladder**.

After one model is selected:

1. keep existing tests/preflight green;
2. run exactly one fresh `A-plain` trial 1;
3. if it succeeds with valid text/zero tools/session evidence, run the complete original 18-session / 21-turn baseline with that same model;
4. if it fails, stop `PARTIAL` with the R2 structured sanitized error; do not try the next candidate;
5. persist baseline JSONL only if all 21 records validate;
6. semantic fields remain `PENDING_CHATGPT`.

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

## Open Questions / Blockers

Primary blocker: no catalog-resolvable model has yet produced the first real T004 response under the isolated OpenCode adapter.

R3 authorizes one deterministic catalog-compatible model selection and one smoke child before the complete baseline.

If the R3-selected advertised model also fails, Strategy/Human must choose between an OpenCode version adjustment and an alternate execution adapter. Do not continue model hopping.

The source product remains not stable/release-ready.

## Next Action

1. Integrate T004-R3 + O026 through normal Markdown PR flow if the diff is limited to those two files.
2. Send the executor a minimal prompt to continue `eval/d032-agent-capability` and apply only T004-R3.
3. On return, verify D029 and the deterministic catalog selection.
4. If a complete 21-record baseline exists, perform ChatGPT semantic PD5 over all transcripts and verify 18-session cardinality/isolation.
5. If R3 smoke fails, stop T004 execution and design a separately authorized OpenCode-version or alternate-adapter remediation.
6. Only after T004 resolution, design D033–D036 Core integration.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
2. load `docs/reviews/T004-R3.md` (R2 only if diagnostic history is needed);
3. if the executor has returned, fetch `handoffs/T004-executor-handoff.json` and exact branch/results at the reported final HEAD;
4. load D029 only if identity mechanics require re-checking;
5. load D032 Core files only when semantic transcript grading is possible;
6. load D033–D036 only when post-T004 architecture planning becomes active.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not accept T004 without the real 18-session / 21-turn baseline and ChatGPT semantic PD5.
- Do not fabricate transcripts or use model self-grading.
- Do not weaken deny-all, disposable isolation or source-worktree immutability.
- Do not retry `openai/gpt-5.6-terra` under OpenCode `1.18.16` for T004.
- Do not turn the R3 model preference list into iterative provider-call retries.
- Do not change provider/OpenCode version/adapter unless separately authorized after R3 evidence.
- Do not copy/persist credentials or raw secret-bearing diagnostics.
- Do not open/merge a T004 implementation PR while T004 remains `PARTIAL`.
- Do not retroactively apply D033–D036 to broaden T004.
- Do not modify Governance Core/protocol for D033–D036 until T004 is resolved and a separate READY Task Contract exists.
- Do not hide/rewrite direct-write incidents without explicit Human authorization.
- Do not declare the source product stable/release-ready.