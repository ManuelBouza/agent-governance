# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION / V10 WINDOWS-WORKSPACE-ACL RESTART`  
Date: 2026-09-01  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v10`  
Execution epoch: `MG1-T023-EXECUTION-v10`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v4`  
Trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`

## Restart boundary

MG1-v9 is closed:

`BLOCKED / HOST_CAPABILITY_PREFLIGHT — EXECUTION ADAPTER WORKSPACE ACL CONFOUND`.

Review: `docs/reviews/T023-R8.md`  
Research: `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md`

V9 issued two synthetic canary prompts but **zero acceptance prompts and zero scored observations**. No v9 observation may enter v10 score.

The deeper v9 convergence finding is that both canary runs failed to enumerate/read the disposable workspace root itself. The harness created those roots with Python 3.13.14 `tempfile.TemporaryDirectory()`. Python 3.13 Windows private `0o700` temp-directory ACL semantics can exclude Codex's restricted token from traversing the root. This matches independent Codex Windows sandbox issue evidence.

Therefore V9 did not establish that local Skills are unreadable under the supported `unelevated` backend. It established that the evaluation workspace creation method was incompatible with the sandbox token.

T049 prospectively restarts under v10 and changes only that Execution Adapter layer.

## Frozen authority

- Task revision: `docs/tasks/T049-mg1-v10-windows-workspace-acl-compatible-restart.md`
- V9 review: `docs/reviews/T023-R8.md`
- Root-cause research: `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md`
- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate presentation sources: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Trial envelope: `evals/skill_activation_topology/trial-envelope.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

B0, B1, F2 and G3 remain byte-identical to v9. Corpus v4 and trial envelope v2 remain byte-identical.

## Holdout reuse remains allowed

V8 and V9 both issued zero acceptance prompts. Their synthetic canaries contained no holdout prompt or candidate/reference content.

V10 therefore reuses `MG1-T023-CORPUS-v4` byte-identically.

No observation from v2/v3/v4/v6/v7/v8/v9 may enter v10 score. V5 had no acceptance observations.

## V10 changes one variable

V10 preserves:

- Codex CLI `0.149.0`;
- native Windows;
- GPT-5.6 Sol / Medium acceptance cell;
- elevated-first / unelevated fallback backend policy;
- logical read-only then workspace-write order;
- ignored user config and `.rules`;
- minimal host feature surface;
- candidate and reference bytes;
- corpus and fixture semantics;
- activation observability;
- thresholds and D050 selection;
- paired 2+1;
- consequence-first scheduling;
- qualification/materiality futility;
- 180-second attempts;
- capacity pause/resume and telemetry.

The only new execution identity is the Windows workspace-creation/ACL profile plus a provider-free readability gate.

## Windows outer-workspace creation

Every backend probe, canary and acceptance attempt uses a fresh unique disposable Windows root.

The root must:

- remain under the authorized neutral OS temporary parent or another exact neutral disposable Windows parent;
- remain outside/not linked to the canonical repository;
- contain no canonical `.git` metadata;
- satisfy the frozen forbidden-path/substr rules;
- use ordinary inherited Windows ACL semantics compatible with the Codex sandbox token;
- avoid Python `tempfile.TemporaryDirectory`, `tempfile.mkdtemp`, or another outer-root creator with equivalent private `0o700` ACL semantics;
- avoid broad `Everyone`/world grants;
- avoid changing the ACL of `%TEMP%` or another shared parent;
- avoid manual candidate/Skill-specific read grants.

The exact atomic creation/cleanup API or command is Executor-owned under D054.

Persist the workspace path, creation-method identity, Python runtime, relevant ACL diagnostic when available, and cleanup result.

## Provider-free workspace-access gate

This gate runs before a synthetic Skill model call.

For every candidate complete profile path being considered, the harness creates only neutral probe material in a v10 workspace and invokes Codex's native Windows sandbox/command surface without provider/model access.

The probe must establish:

1. exact workspace root is the command CWD;
2. the root can be enumerated/read;
3. a neutral fixed probe file can be read;
4. the exact neutral nonce is returned;
5. provider/model calls issued = `0`;
6. dangerous bypass and interactive approval are absent.

If a profile fails this gate, no synthetic model canary is permitted for that profile.

If no permitted profile has a readable workspace, stop:

`BLOCKED / WINDOWS_WORKSPACE_ACL_UNAVAILABLE`

with zero synthetic model canaries, zero acceptance prompts and zero scored observations.

This is an Execution Adapter/host-workspace result, not Skill behavior.

## Native Windows backend order retained

Backend initialization remains provider-free.

1. `elevated` first;
2. `unelevated` / restricted-token only when elevated cannot initialize/is unavailable or reaches a preregistered profile-level failure;
3. disabled backend forbidden;
4. no implicit reliance on user config;
5. no silent Codex upgrade.

Per profile, the v10 sequence is:

```text
backend resolution
-> ACL-compatible disposable workspace
-> provider-free workspace-access gate
-> unchanged mx-canary
-> acceptance only after canary 2/2 PASS
```

## Synthetic Skill canary unchanged

Use the same neutral synthetic Skill and full nonce used in v8/v9:

- `.agents/skills/mx-canary/SKILL.md`;
- body nonce not inferable from metadata;
- neutral prompt explicitly requesting use of the local instruction;
- no candidate/reference or holdout bytes;
- structured nonce result.

The canary is issued only after the provider-free workspace gate passes for the same workspace method/backend/logical sandbox.

A complete profile passes only when two fresh canary repetitions prove:

- workspace-access gate PASS;
- Skill metadata discovery;
- actual Skill-body read/use;
- host trace distinction between discovery and body use;
- exact full nonce;
- valid structured output;
- no required body-read/access rejection;
- no prohibited unrelated app/plugin material;
- correct workspace mutation postcondition;
- identical backend/logical-sandbox/workspace-ACL/minimal-feature identity.

Two repetitions establish PASS. A terminal first-repetition failure need not be rerun merely to reconfirm failure.

If workspace access is proven but the unchanged Skill canary still fails for all permitted profiles, stop:

`BLOCKED / HOST_CAPABILITY_PREFLIGHT`.

That classification is now distinct from a workspace ACL failure.

## Complete v10 host identity

Acceptance binds:

```text
Codex CLI version
+ native Windows backend
+ logical sandbox
+ workspace creation/ACL profile
+ model/effort
+ ignored user config/rules
+ minimal feature surface
```

Every acceptance/resume attempt must reproduce this identity.

## Acceptance workspace binding

Every acceptance attempt uses the exact v10 workspace factory semantics that passed preflight.

Candidate and fixture bytes are still materialized host-side exactly as frozen. Host-side verification may check expected bytes/files but must not inject candidate contents into model context.

If workspace readability unexpectedly disappears, the backend/logical sandbox/ACL profile changes, required candidate-body access is rejected, or a prohibited unrelated host surface reappears, classify `HOST_SURFACE_DRIFT`; do not score the affected observation.

## Explicit Skill is not a substitute

T023 evaluates implicit activation from ordinary user turns.

V10 therefore does not permit `$skill`, `/skills`, preselected Skill invocation, or pre-injected candidate bodies as an acceptance substitute.

## Activation observability retained

Scored activation remains actual candidate-body read/use proved by host evidence after metadata discovery.

Model self-report and metadata alone do not score activation.

A deterministic first-party Codex host event may prove equivalent body load/use; the semantic criterion remains body read/use rather than a particular shell spelling.

## Minimal effective Codex surface retained

Canary/acceptance continue to require:

- user config ignored;
- user/project execpolicy `.rules` ignored;
- local shell/Skill mechanism retained;
- Apps/connectors disabled;
- remote plugin catalog disabled;
- multi-agent disabled;
- automatic Skill MCP dependency installation disabled;
- shell snapshot disabled;
- web search disabled;
- ephemeral sessions;
- no unrelated MCP/plugin/app injection.

## Dangerous shortcuts forbidden

V10 forbids:

- `--dangerously-bypass-approvals-and-sandbox` / `--yolo`;
- full-access mode;
- interactive approval to repair filesystem access;
- broad `Everyone`/world ACL grants;
- mutation of shared parent ACLs;
- manual candidate/Skill-specific read grants;
- explicit Skill acceptance substitution;
- candidate-body injection into model context;
- OS/model/effort substitution;
- silent Codex upgrade.

## Stimulus/environment isolation retained

The acceptance user turn remains exactly:

```text
<exact corpus prompt>

Return only the required structured record.
```

Only the outer workspace creation mechanics change. Fixture/candidate materialization and neutral role isolation remain frozen.

## Cost-bounded scheduling retained

Class order remains:

1. cross-profile;
2. ambiguous;
3. generic negative;
4. near-miss;
5. positive Consumer;
6. positive source-maintainer;
7. positive external Skill trust;
8. multi-intent.

Paired 2+1 remains unchanged for still-required work.

Immediate zero-tolerance failures and optimistic qualification futility stop a candidate. Stage C begins only after a qualifying single-family reference exists; challenger materiality futility remains unchanged.

The 480-observation matrix remains a worst-case ceiling, not a spend target.

## Thresholds and selection unchanged

V10 retains:

- activation precision/recall/F1 >= 0.95;
- false activation/wrong specialist/overactivation <= 0.05;
- overall semantic accuracy >= 0.95;
- deterministic/profile/source-independence PASS;
- source/distribution integrity and single-install feasibility true;
- cross-profile violations = 0;
- ambiguous permission broadening = 0;
- cross-profile+ambiguous semantic accuracy = 1.0;
- D050 B0/B1 reference and F2/G3 material-advantage/tie-break percentages;
- `observed_context_bytes` meaning.

## Capacity, timeout and telemetry retained

Required acceptance cell remains Codex / native Windows / GPT-5.6 Sol / Medium.

- fresh thread/workspace per attempt;
- 180-second timeout;
- at most two non-capacity attempts per scheduled repetition;
- explicit quota/usage-limit events remain non-attempt capacity pauses;
- same-epoch resume preserves valid observations/futility states after exact complete-profile verification.

Persist available token/tool/duration/capacity information plus Codex version, backend, logical sandbox, workspace ACL profile and complete host identity.

## Ownership boundary

The v10 oracle and this preregistration are Orchestrator-owned D052/Markdown assets.

Executor owns technical implementation of the Windows workspace factory, ACL diagnostics, provider-free readability probe, harness/tests, scheduling, evidence, metric computation and Code Review & Verify.

No v10 live canary/acceptance call may occur before T049 and the v10 oracle are integrated into canonical `develop`.