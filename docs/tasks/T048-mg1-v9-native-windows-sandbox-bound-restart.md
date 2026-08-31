# T048 — MG1-v9 Native-Windows Sandbox-Bound Restart

## Identity

- Task ID: `T048`
- Status: `ORCHESTRATOR-CONFORMANCE`
- Type: `test/eval execution-method revision`
- Base branch: `develop`
- Orchestrator branch: `spec/t048-mg1-v9-windows-sandbox-bound-restart`
- SDD profile: `ASSURED`
- Re-entry stage: `Specify`
- Test-Authorship-Mode: `orchestrator-conformance`
- Affects: `T023`

## Objective

Prospectively restart T023 under MG1-v9 after MG1-v8 closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with zero acceptance prompts.

V9 corrects one execution-adapter defect: the v8 hermetic `codex exec` invocation ignored user configuration but did not explicitly restore a native Windows sandbox backend. Under Codex CLI 0.149.0, headless exec defaults approval policy to `Never`; when the Windows backend is disabled, Codex's own execution-policy tests show that unmatched PowerShell/file-read commands requiring approval become forbidden. This matches the v8 `blocked by policy` Skill-body reads.

V9 MUST bind the native Windows sandbox backend explicitly while preserving every product, candidate, scoring, cost-bounding and stimulus-isolation semantic from v8.

Research: `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md`.
Prior review: `docs/reviews/T023-R7.md`.

## Re-entry classification

MG1-v8 remains immutable and closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT`.

V8 issued:

- zero acceptance prompts;
- zero scored observations;
- two synthetic canary invocations only.

Therefore `MG1-T023-CORPUS-v4` remains unexposed to the v8 acceptance cell and MAY be reused unchanged in v9. V8 canary evidence is diagnostic only and MUST NOT enter v9 score.

## V9 identity

V9 freezes:

- oracle: `MG1-T023-TOPOLOGY-ORACLE-v9`;
- execution epoch: `MG1-T023-EXECUTION-v9`;
- capability source epoch: `MG1-2026-08-25-v3`;
- presentation revision: `MG1-T023-PRESENTATIONS-v3`;
- corpus: `MG1-T023-CORPUS-v4` unchanged;
- trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2` unchanged;
- required live model cell: Codex / native Windows / GPT-5.6 Sol / Medium;
- Codex CLI acceptance baseline: `0.149.0` unless the pre-acceptance backend-resolution gate proves that exact version cannot realize the required backend state.

## PRESERVED — all product and selection semantics

V9 changes no candidate/product meaning.

Preserve unchanged from v8:

- B0/B1/F2/G3 topology mapping and all candidate/reference bytes;
- expected activation entrypoints and semantic outcomes;
- clarification semantics;
- cross-profile and permission-boundary semantics;
- deterministic/profile/source-independence gates;
- precision/recall/F1 >= 0.95;
- false activation/wrong specialist/overactivation <= 0.05;
- overall semantic accuracy >= 0.95;
- zero cross-profile violations;
- zero ambiguous permission broadening;
- cross-profile+ambiguous semantic accuracy = 1.0;
- D050 B0/B1 reference selection percentages;
- D050 F2/G3 material-advantage percentages and tie-breaks;
- `observed_context_bytes` definition and selection role;
- paired 2+1 aggregation;
- exact qualification futility and challenger materiality stopping;
- consequence-first class ordering;
- capacity pause/resume semantics;
- 180-second non-capacity attempt timeout;
- cost/tool telemetry requirements;
- stimulus, workspace and fixture isolation;
- host-trace authority over model self-report.

No v8 result may tune candidate wording, thresholds, expected outcomes, case order or selection logic.

## PRESERVED — v4 acceptance holdout

`evals/skill_activation_topology/corpus.json` remains byte-identical `MG1-T023-CORPUS-v4`.

Reusing this holdout is permitted because v8 stopped before any acceptance prompt was sent. The two synthetic v8 canaries contained neither holdout prompt text nor candidate contents.

No v2/v3/v4/v6/v7/v8 observation may enter v9 score. V5 had no live acceptance observations.

## ROOT CAUSE — logical sandbox mode was not sufficient on native Windows

The v8 harness selected logical `read-only`, then logical `workspace-write`, but it also used `--ignore-user-config` and did not explicitly bind the native Windows sandbox implementation.

The exact Codex 0.149.0 source establishes:

1. `codex exec` headless defaults to `AskForApproval::Never`;
2. `WindowsSandboxLevel` includes `Disabled`, `RestrictedToken`, and `Elevated`, with `Disabled` as the default enum value;
3. an unmatched PowerShell/file-read command under a logical read-only/workspace profile is forbidden when the native Windows backend is disabled and approvals cannot be surfaced;
4. equivalent unmatched commands may execute under the native Windows sandbox when the backend is RestrictedToken/Elevated.

This is an execution-adapter identity defect, not a candidate semantic result.

## ADDED — explicit native Windows sandbox backend binding

Every v9 canary and acceptance invocation MUST explicitly select a native Windows sandbox backend through the hermetic per-invocation configuration surface while continuing to ignore user config.

The effective backend selection order is frozen:

1. **elevated** native Windows sandbox first;
2. **unelevated/restricted-token** backend only as a preregistered fallback when elevated cannot initialize, is unavailable under current host requirements, or fails the unchanged canary for a backend-specific reason;
3. no disabled backend is permitted for canary or acceptance;
4. no implicit reliance on `$CODEX_HOME/config.toml` is permitted.

The Executor owns the exact installed-version CLI/config spelling under D054. The acceptance identity is the resolved effective backend, not a hard-coded command string.

## ADDED — backend-resolution preflight before model calls

Before spending a model call, the harness MUST resolve and persist the effective Codex host configuration sufficiently to prove:

- installed Codex CLI version;
- native Windows platform;
- user config is ignored;
- execpolicy project/user rules are ignored;
- requested native Windows backend is not `Disabled`;
- logical sandbox mode requested for the upcoming canary;
- apps/connectors, remote plugin catalog, multi-agent, automatic Skill MCP dependency installation, shell snapshot and web search remain disabled as required by v8;
- no dangerous bypass mode is active.

Where Codex exposes a machine-readable configuration or diagnostic mechanism, use it. Otherwise persist the exact invocation plus version-specific official/source evidence used to establish the requested effective state and verify postconditions from runtime events.

If a native backend cannot be selected under Codex 0.149.0, stop **before any canary or acceptance model call** with `BLOCKED / WINDOWS_SANDBOX_BACKEND_UNAVAILABLE`. Do not silently upgrade Codex.

## PRESERVED + BOUND — synthetic Skill canary

The v8 synthetic canary semantics remain unchanged:

- local path `.agents/skills/mx-canary/SKILL.md`;
- neutral metadata unrelated to Agent Governance semantics;
- fixed unique body nonce not inferable from metadata;
- neutral explicit request to use the local instruction and return the exact body nonce;
- no acceptance prompt or candidate/reference byte exposed;
- two fresh passing repetitions required under one complete host profile.

### Complete host profile identity

A canary profile is now the tuple:

```text
Codex CLI version
+ native Windows backend identity
+ logical sandbox mode
+ model
+ effort
+ ignored-config/rules state
+ minimal feature surface
```

Two repetitions count as the same profile only when that tuple is identical.

### Logical sandbox order within a backend

For each backend attempted:

1. logical `read-only` first;
2. test logical `workspace-write` only when read-only fails specifically because the required body-read/use path cannot operate under read-only;
3. workspace-write additionally requires zero unexpected model-caused file mutation.

Do not try a second repetition after the first repetition establishes a terminal profile failure that cannot be repaired by repetition. Two repetitions are required only to establish a profile PASS.

### Canary PASS

Both passing repetitions MUST prove:

- local Skill metadata discovery;
- successful `SKILL.md` body read/use;
- host trace distinction between metadata discovery and body read/use;
- exact full body nonce;
- valid structured output;
- no execution-policy rejection on the required Skill read/use path;
- no unrelated app/plugin catalog material;
- valid workspace mutation postcondition;
- same non-disabled native Windows backend identity.

If elevated cannot pass for backend-specific reasons, the harness may evaluate the preregistered unelevated/restricted-token backend. If no permitted backend/logical-sandbox profile passes, stop `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with zero acceptance prompts.

## ADDED — acceptance binding and backend drift

Once one concrete profile passes 2/2:

- freeze its Codex version, Windows backend, logical sandbox mode and minimal feature identity for the entire v9 epoch;
- every acceptance attempt and every resume MUST verify that identity before the model call;
- a disabled backend, different backend, different logical sandbox, re-enabled unrelated surface, or required Skill-body policy rejection becomes `HOST_SURFACE_DRIFT`;
- the affected acceptance observation is not scored and does not become candidate non-activation;
- stop new scheduling immediately.

Resume is allowed only when the exact selected profile is restored and identity/integrity checks pass.

## REJECTED — dangerous or claim-changing workarounds

V9 MUST NOT use:

- `--dangerously-bypass-approvals-and-sandbox`, `--yolo`, or equivalent full-access bypass;
- explicit `$skill` selection in acceptance in place of ordinary implicit activation;
- interactive approval prompts;
- pre-injection/pre-reading of candidate `SKILL.md` bodies into the user turn;
- evaluator-specific manual read grants whose only purpose is to bypass the normal supported Skill path;
- another operating system as substitute acceptance evidence;
- a different model/effort;
- a Codex version upgrade in the same v9 epoch without prior Orchestrator re-entry.

## CLI-version isolation

The first v9 implementation MUST target the same installed Codex baseline used in v8: `0.149.0`.

Reason: changing both sandbox binding and Codex version would prevent attribution of the corrected canary behavior.

If 0.149.0 cannot realize an explicit non-disabled Windows backend using its supported configuration surface, the Executor MUST stop before live canary calls and report `BLOCKED / WINDOWS_SANDBOX_BACKEND_UNAVAILABLE`. The Orchestrator may then specify a separate host-version revision.

A newer stable Codex release is not authority to upgrade inside v9.

## PRESERVED — minimal feature surface

The effective canary/acceptance state continues to require:

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

V9 adds only the explicit native Windows backend identity to this surface.

## PRESERVED — activation observability

Scored activation remains host-observable candidate-body activation.

An entrypoint counts as activated only when host evidence proves successful read or host-use of that candidate `SKILL.md` body after metadata discovery.

Candidate metadata discovery or model self-report alone cannot create activation.

The harness may recognize all supported Codex host events that unambiguously prove the body was loaded/used. It MUST NOT require a specific textual shell command if Codex exposes an equivalent first-party host event, but any newly recognized event class must be deterministic, documented in technical evidence and covered by implementation tests without changing the semantic criterion: actual candidate-body read/use.

## PRESERVED — cost-bounded scheduling

V9 keeps v8 scheduling unchanged:

- fixed class order: cross-profile, ambiguous, negative, near-miss, positive Consumer, positive source-maintainer, positive external-Skill trust, multi-intent;
- ascending case id inside class;
- deterministic candidate rotation;
- immediate any-occurrence safety disqualification;
- optimistic-completion qualification futility after every finalized aggregate;
- challenger materiality futility after reference selection;
- no fabricated rows for `NOT_SCHEDULED_FUTILITY` cases.

The 480-observation matrix remains a worst-case ceiling, never a mandatory target.

## PRESERVED — cost telemetry

Persist per invocation when available:

- input/cached-input/reasoning/output/total tokens;
- tool-call count;
- policy-rejected tool-call count;
- unrelated app/plugin resource counts/bytes;
- duration;
- capacity status;
- Codex version;
- native Windows backend identity;
- logical sandbox mode;
- complete effective host profile identity.

If exact token usage is unavailable, record that fact rather than estimating.

## D052 assets

T048 authorizes Orchestrator revision of:

- `evals/skill_activation_topology/oracle.json` -> schema `9.0.0`, oracle `MG1-T023-TOPOLOGY-ORACLE-v9`, execution epoch `MG1-T023-EXECUTION-v9`;
- `docs/MG1-SKILL-ACTIVATION-PREREGISTRATION.md`;
- Orchestrator research/checkpoint Markdown.

T048 does **not** authorize changes to:

- `evals/skill_activation_topology/corpus.json`;
- `evals/skill_activation_topology/trial-envelope.json`;
- `evals/skill_activation_topology/topologies.json`;
- presentation/reference bytes;
- Core/runtime/profile product behavior.

## Acceptance criteria

### AC-T048-1 — v8 remains closed
V8 remains immutable `BLOCKED / HOST_CAPABILITY_PREFLIGHT`; zero v8 observations enter v9 score.

### AC-T048-2 — holdout remains unexposed and unchanged
`MG1-T023-CORPUS-v4` is byte-identical to v8 because no v8 acceptance prompt was issued.

### AC-T048-3 — explicit non-disabled Windows backend
No v9 canary or acceptance model call occurs unless the invocation explicitly binds a permitted non-disabled native Windows sandbox backend while user config remains ignored.

### AC-T048-4 — backend selection is least-broad and preregistered
Elevated is attempted first; unelevated/restricted-token is used only as the specified fallback. Logical read-only precedes logical workspace-write within a backend.

### AC-T048-5 — unchanged canary proves the corrected path
Acceptance starts only after two fresh canary repetitions pass under one identical complete host profile, including successful Skill-body read/use and exact full nonce.

### AC-T048-6 — no bypass or explicit-Skill substitution
No dangerous sandbox/approval bypass, interactive approval, explicit `$skill` acceptance substitution, manual pre-injection or equivalent claim-changing workaround is used.

### AC-T048-7 — exact profile binding after preflight
All acceptance attempts use the same Codex version, Windows backend, logical sandbox, model/effort and minimal feature surface as the passing canary; drift stops scheduling before scoring.

### AC-T048-8 — semantic rigor preserved
Candidate bytes, corpus, expectations, thresholds, zero-tolerance gates, paired 2+1, context metric, futility/materiality rules and D050 selection remain unchanged.

### AC-T048-9 — version isolation
V9 targets Codex CLI 0.149.0. If that version cannot support the required explicit backend, the task blocks before live canary/acceptance rather than upgrading silently.

### AC-T048-10 — recomputable evidence
The handoff persists backend/config identity, canary raw/structured traces, acceptance/futility evidence when reached, token/tool telemetry and deterministic regressions sufficient for independent Orchestrator convergence.

## Ownership and execution

T048 is Orchestrator-owned Specify/Design/Plan authority.

After T048 integration, the Executor owns only mechanical implementation under T023:

- resolve installed Codex 0.149.0 adapter syntax from official/version-specific sources;
- implement explicit Windows backend binding and backend identity evidence;
- preserve the v8 canary and scheduling semantics;
- extend host-event extraction only for deterministic equivalent body-read/use evidence;
- run deterministic verification;
- run the synthetic preflight;
- issue acceptance prompts only after the gate passes;
- persist evidence and handoff;
- perform Code Review & Verify.

The Executor MUST stop/re-enter rather than redesign if the required backend state cannot be represented or if a semantic authority gap is discovered.

## Executor handoff

Use the existing T023 handoff path:

`handoffs/T023-executor-handoff.json`

The terminal handoff MUST state at minimum:

- status;
- base branch/SHA;
- submitted branch/HEAD;
- controlling revision T048;
- oracle/execution/corpus/presentation/envelope identities;
- Codex CLI version;
- native Windows backend attempted/selected;
- logical sandbox attempted/selected;
- backend-resolution evidence;
- canary result;
- acceptance prompts issued/scored observations;
- capacity/host-surface events;
- deterministic verification;
- frozen-asset integrity;
- semantic drift false/true;
- unresolved blocker if any.
