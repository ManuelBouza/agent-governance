# T049 — MG1-v10 Windows Workspace-ACL-Compatible Restart

## Identity

- Task ID: `T049`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval execution-method revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t049-mg1-v10-windows-workspace-acl-restart`
- SDD profile: `ASSURED`
- Re-entry stage: `Specify`
- Test-Authorship-Mode: `orchestrator-conformance`
- Affects: `T023`

## Objective

Prospectively restart T023 after MG1-v9 closed before acceptance because the Python 3.13 private ACL on `tempfile.TemporaryDirectory()` roots made the entire disposable workspace inaccessible to the Codex Windows restricted token.

MG1-v10 MUST correct only the disposable Windows workspace creation/accessibility layer while preserving the complete v9 product/evaluation semantics.

V10 MUST:

1. create each outer disposable Windows workspace with ordinary inherited ACL semantics compatible with the selected Codex sandbox, rather than Python private `0o700` temp-directory semantics;
2. prove workspace enumeration/readability through the selected native Windows sandbox without a provider/model call before any synthetic Skill canary;
3. issue the unchanged synthetic Skill canary only after the workspace-access gate passes;
4. keep the v9 backend selection, CLI version, host/model/effort, candidate bytes, holdout, semantic expectations, thresholds, selection and cost-bounded scheduling unchanged;
5. preserve enough evidence to distinguish workspace ACL failure, backend failure, Skill-body preflight failure, host-surface drift, model-attempt failure and external capacity.

## Evidence motivating re-entry

`docs/reviews/T023-R8.md` closes MG1-v9 as:

`BLOCKED / HOST_CAPABILITY_PREFLIGHT — EXECUTION ADAPTER WORKSPACE ACL CONFOUND`.

V9 facts:

- Codex CLI `0.149.0`;
- `elevated` backend probe timed out without provider/model use;
- `unelevated` backend initialized provider-free;
- one read-only and one workspace-write synthetic canary were issued;
- both failed because the sandboxed process could not read the Skill body **or enumerate the workspace root itself**;
- Python runtime `3.13.14`;
- harness workspace roots were created through `tempfile.TemporaryDirectory()` under `%TEMP%`;
- acceptance prompts: `0`;
- scored observations: `0`;
- topology selection: none.

Research: `docs/research/MG1-V9-WINDOWS-TEMP-ACL-ANALYSIS.md`.

## Preserved authority

V10 preserves unchanged:

- capability source epoch `MG1-2026-08-25-v3`;
- presentation revision `MG1-T023-PRESENTATIONS-v3` and every candidate/reference byte;
- candidate topology definitions B0/B1/F2/G3;
- corpus `MG1-T023-CORPUS-v4` byte-identically;
- trial envelope `MG1-T023-TRIAL-ENVELOPE-v2` byte-identically;
- semantic expectations and fixture roles;
- clarification, cross-profile and permission-boundary semantics;
- activation authority = actual host-observed candidate-body read/use after metadata discovery;
- deterministic/profile/source-independence gates;
- qualification thresholds: precision/recall/F1 >= 0.95, false/wrong/overactivation <= 0.05, overall semantic accuracy >= 0.95;
- zero cross-profile violations and zero ambiguous permission broadening;
- D050 B0/B1 reference and F2/G3 material-advantage/tie-break rules;
- paired 2+1 aggregation;
- consequence-first scheduling and exact qualification/materiality futility;
- 180-second non-capacity attempt timeout;
- capacity-aware pause/resume;
- required live cell: Codex / native Windows / GPT-5.6 Sol / Medium;
- Codex CLI baseline `0.149.0`;
- native Windows backend order: `elevated`, then `unelevated` fallback;
- user config/rules isolation and minimal feature surface;
- prohibition on explicit Skill substitution, dangerous bypass and interactive approval.

No v2/v3/v4/v6/v7/v8/v9 observation may enter v10 score. V5 had no acceptance observations. V8 and V9 both issued zero acceptance prompts, so corpus v4 remains unexposed to those acceptance epochs.

## MODIFIED — Windows disposable workspace creation

### Problem being corrected

V9 created canary and acceptance roots through Python `tempfile.TemporaryDirectory()` under `%TEMP%`. On Python 3.13 Windows, private `0o700` directory creation can apply a DACL that is not traversable/readable by the Codex restricted token.

### Required v10 outer-root semantics

Every backend probe workspace, synthetic canary workspace and acceptance-attempt workspace MUST be a fresh unique directory whose outer root:

- is under the OS temporary parent or another exact neutral disposable Windows parent already permitted by the frozen isolation rules;
- is outside and not linked to the canonical repository;
- contains no canonical `.git` metadata;
- satisfies the frozen forbidden-root-substring rules;
- is created with ordinary inherited Windows ACL semantics compatible with the selected sandbox token;
- is not created using Python `tempfile.TemporaryDirectory`, `tempfile.mkdtemp`, or another helper whose effective Windows root ACL is private `0o700`/equivalent;
- is not repaired by granting broad `Everyone`/world access;
- does not mutate the ACL of `%TEMP%` or another parent directory;
- does not use a candidate-specific or evaluator-only read grant;
- is removed host-side after the attempt when evidence retention no longer requires it.

Exact atomic unique-directory creation, ACL inspection and cleanup syntax/API are Executor-owned Execution Adapter mechanics under D054.

### ACL diagnostic evidence

For every live workspace, persist when available:

- absolute root path;
- creation method identity;
- Python runtime/version used by the harness;
- whether private Python-temp creation was avoided;
- inherited/explicit ACL diagnostic sufficient to troubleshoot access without exposing credentials;
- cleanup result.

ACL diagnostics are host evidence only and never enter candidate scoring.

## ADDED — provider-free workspace-access gate

Before any synthetic model canary for a native-backend/logical-sandbox profile, V10 MUST prove that the selected sandbox can access a neutral workspace created by the exact v10 workspace factory.

### Neutral probe material

The harness may create only neutral non-domain probe material, for example:

- one small fixed-name neutral file;
- one fixed nonce unrelated to Agent Governance, candidates, profiles or holdout semantics.

The probe contains no candidate/reference or holdout bytes.

### Provider-free execution

Invoke Codex's native Windows sandbox/command execution surface without provider/model access, under the requested:

- Codex CLI 0.149.0;
- native backend;
- logical sandbox;
- workspace root.

The probe MUST establish all of:

1. the sandboxed command starts with the exact workspace as CWD;
2. the workspace root can be enumerated/read;
3. the neutral probe file can be read exactly;
4. the exact nonce is returned;
5. no provider/model call was issued;
6. no dangerous bypass or interactive approval was used.

### Gate outcome

If the workspace-access probe fails for a native-backend/logical-sandbox profile, do not issue a synthetic model canary for that profile.

If no permitted profile has a readable workspace, stop:

`BLOCKED / WINDOWS_WORKSPACE_ACL_UNAVAILABLE`

with:

- synthetic model canary prompts = `0`;
- acceptance prompts = `0`;
- scored observations = `0`.

This failure is an Execution Adapter/host-workspace condition, not Skill behavior.

## PRESERVED + SEQUENCED — native Windows backend resolution

Backend resolution remains provider-free and precedes workspace/canary execution.

Order remains:

1. `elevated` first;
2. `unelevated` only when elevated cannot initialize/is unavailable or later fails for a preregistered backend/profile reason;
3. disabled backend forbidden.

V10 does not silently upgrade Codex.

For each backend/profile path, the sequence is:

```text
backend initialization
-> v10 workspace creation
-> provider-free workspace-access probe
-> unchanged synthetic Skill canary
-> acceptance only after 2/2 canary PASS
```

A profile that cannot pass the workspace-access gate never reaches the model canary.

## PRESERVED — synthetic Skill canary

The mx-canary semantics and body nonce are unchanged from v8/v9.

A complete host profile passes only when two fresh canary repetitions establish:

- local Skill metadata discovery;
- actual Skill-body read/use;
- host-trace distinction between metadata and body use;
- exact full nonce;
- valid structured output;
- no required-body policy/access rejection;
- no unrelated app/plugin catalog material entering the prohibited surface;
- correct workspace mutation postcondition;
- same non-disabled native backend/logical sandbox/minimal feature identity;
- v10 workspace-access gate PASS for the same workspace method/profile.

Two repetitions establish PASS; a terminal first-repetition failure need not be repeated when another repetition cannot repair it.

If workspace access passed but no complete profile passes the unchanged canary, stop:

`BLOCKED / HOST_CAPABILITY_PREFLIGHT`.

That distinction is mandatory: workspace ACL failure must not be reported as Skill preflight failure.

## Complete v10 host-profile identity

Persist and bind:

```text
Codex CLI version
+ native Windows backend
+ logical sandbox
+ workspace creation/ACL profile identity
+ model/effort
+ ignored user config/rules
+ minimal feature surface
```

Acceptance/resume must reproduce this complete identity.

## Acceptance workspace rule

Every acceptance attempt MUST use the same v10 workspace factory semantics that passed provider-free and synthetic preflight.

After the workspace is created and candidate/fixture materialized, host-side validation may confirm expected files/bytes before model execution. It MUST NOT pre-read candidate bodies into model context.

If an acceptance workspace unexpectedly becomes unreadable to the selected sandbox before/during required candidate-body access, classify `HOST_SURFACE_DRIFT`; do not score the affected observation.

## Explicitly forbidden shortcuts

V10 forbids:

- `--dangerously-bypass-approvals-and-sandbox`, `--yolo`, full-access mode;
- interactive approval to repair workspace access;
- broad `Everyone`/world ACL grants;
- mutation of the shared parent temporary-directory ACL;
- manual per-candidate/per-Skill read grants;
- explicit `$skill`/`/skills` substitution;
- pre-reading or injecting candidate bodies into the user prompt/model context;
- changing corpus/candidate bytes/thresholds/D050 rules;
- changing OS/model/effort;
- upgrading Codex within the v10 epoch.

## Evidence requirements

Persist machine-readable evidence sufficient to reconstruct:

- exact canonical base and frozen asset hashes;
- Python runtime;
- workspace factory implementation identity;
- each workspace path and ACL diagnostic;
- backend-resolution attempts/results;
- each provider-free workspace-access probe and explicit `provider_model_call_issued=false`;
- canary attempts/results only for profiles whose workspace probe passed;
- complete selected host-profile identity;
- all acceptance raw/structured observations if reached;
- capacity events separately from model attempts;
- host-surface drift separately from candidate behavior;
- futility/materiality certificates;
- deterministic regression evidence;
- completeness and final selection/blocker state.

## Test/verification requirements

Executor technical implementation MUST add deterministic tests proving at least:

1. v10 refuses Python-private outer workspace factories on Windows;
2. workspace-access probe runs before any synthetic model canary;
3. failed workspace-access probe causes zero canary/acceptance calls for that profile;
4. provider-free probe records exact nonce and no provider/model use;
5. canary is permitted only after workspace probe PASS;
6. acceptance is permitted only after canary 2/2 PASS;
7. workspace ACL failure and Skill-body preflight failure remain distinct terminal classes;
8. existing backend order, frozen assets, 2+1, futility and scoring semantics remain unchanged;
9. no unexpected workspace mutation is introduced;
10. deterministic/profile/Consumer-source regressions remain green.

## Acceptance criteria

### AC-T049-1 — v9 closed without semantic carryover
V9 evidence remains immutable; v9 acceptance prompts/scored observations are zero and no v9 result enters v10 score.

### AC-T049-2 — byte-identical experiment semantics
Corpus v4, trial envelope v2, presentations v3, topology semantics, expectations, thresholds, D050 rules, 2+1 and futility remain unchanged.

### AC-T049-3 — non-private Windows outer root
The live v10 outer workspace is not created through Python private `0o700` tempfile semantics and retains the existing isolation guarantees.

### AC-T049-4 — provider-free workspace readability
Before any synthetic model canary, the selected sandbox can enumerate/read the workspace and exact neutral probe file with zero provider/model calls.

### AC-T049-5 — fail before spend
If no permitted workspace/profile passes AC-T049-4, the run stops `WINDOWS_WORKSPACE_ACL_UNAVAILABLE` with zero synthetic model and acceptance calls.

### AC-T049-6 — unchanged Skill canary
Only after AC-T049-4 passes, the unchanged mx-canary is evaluated. Acceptance remains forbidden until a complete profile passes 2/2.

### AC-T049-7 — complete profile binding
Acceptance uses the exact Codex/backend/logical-sandbox/workspace-ACL/model/effort/config/feature profile selected by preflight.

### AC-T049-8 — no privilege broadening
No dangerous bypass, interactive approval, broad ACL grant, parent ACL mutation, explicit Skill substitution or manual candidate read grant is used.

### AC-T049-9 — cost-bounded acceptance unchanged
If acceptance is reached, v9 paired 2+1, consequence order, futility/materiality, timeout/capacity and selection rules remain controlling.

### AC-T049-10 — recomputable terminal evidence
Whether PASS, HOST_CAPABILITY_PREFLIGHT, WINDOWS_WORKSPACE_ACL_UNAVAILABLE, HOST_SURFACE_DRIFT, capacity pause or model-attempt failure, the handoff contains enough technical evidence for independent Orchestrator convergence.

## D052 assets

T049 authorizes Orchestrator revision of:

- `evals/skill_activation_topology/oracle.json` -> schema `10.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v10`, execution epoch `MG1-T023-EXECUTION-v10`;
- preregistration/review/research/checkpoint Markdown.

T049 does **not** authorize changes to:

- `evals/skill_activation_topology/corpus.json`;
- `trial-envelope.json`;
- `topologies.json`;
- presentation/reference bytes;
- product Core/runtime/profile semantics.

## Ownership and execution

T049 is Orchestrator-owned Specify/Design/Plan & Trace work. After integration, T023 may be relaunched from fresh canonical `develop`.

Executor owns only technical implementation and verification of:

- Windows workspace factory mechanics;
- ACL diagnostic extraction;
- provider-free workspace-access probe;
- existing backend/canary/acceptance harness adaptation;
- implementation tests;
- execution/evidence/handoff.

Executor MUST NOT edit committed Markdown or semantically alter the D052 oracle/corpus/presentations/thresholds/selection.