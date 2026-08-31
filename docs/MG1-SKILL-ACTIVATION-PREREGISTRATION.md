# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION / V9 WINDOWS-SANDBOX-BOUND RESTART`  
Date: 2026-08-31  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v9`  
Execution epoch: `MG1-T023-EXECUTION-v9`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v4`  
Trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`

## Restart boundary

MG1-v8 is closed `BLOCKED / HOST_CAPABILITY_PREFLIGHT`; review: `docs/reviews/T023-R7.md`. V8 is not rescored or mutated.

V8 issued **zero acceptance prompts and zero scored observations**. Its two synthetic canaries are diagnostic only and cannot enter v9 score.

Research in `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md` identifies the blocker as an Execution Adapter configuration defect:

- `codex exec` headless defaults approvals to Never;
- V8 correctly used `--ignore-user-config` for isolation;
- V8 did not explicitly restore a native Windows sandbox backend after ignoring that configuration;
- exact Codex 0.149.0 source/tests show that unmatched PowerShell/file reads are forbidden when the Windows backend is disabled and approvals cannot be surfaced;
- those same tests permit unmatched commands to execute under the native RestrictedToken/Elevated sandbox backends.

T048 prospectively restarts the experiment under v9 with the same product/eval semantics but an explicitly bound native Windows sandbox backend.

## Frozen authority

- Task revision: `docs/tasks/T048-mg1-v9-native-windows-sandbox-bound-restart.md`
- Root-cause research: `docs/research/MG1-V8-WINDOWS-SANDBOX-ROOT-CAUSE.md`
- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate presentation sources: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Trial envelope: `evals/skill_activation_topology/trial-envelope.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

B0, B1, F2 and G3 remain byte-identical to v8. The holdout and trial envelope remain byte-identical to v8.

## Holdout reuse is allowed

V9 reuses `MG1-T023-CORPUS-v4` unchanged because v8 stopped before any acceptance prompt was sent. The v8 canaries contained neither holdout prompt text nor candidate/reference bodies.

No observation from v2/v3/v4/v6/v7/v8 may enter v9 score. V5 had no live acceptance observations.

## Execution identity correction

The v9 complete host profile consists of:

```text
Codex CLI version
+ native Windows sandbox backend
+ logical sandbox mode
+ model
+ effort
+ ignored user-config/rules state
+ minimal feature-surface identity
```

V9 requires the native Windows backend to be selected explicitly through the hermetic invocation/configuration surface even while user config remains ignored.

### Backend order

1. prefer native Windows `elevated`;
2. use `unelevated` / restricted-token only as the preregistered fallback when elevated cannot initialize, is unavailable under supported host requirements, or fails the unchanged canary for a backend-specific envelope reason;
3. a disabled backend is never permitted;
4. acceptance never relies implicitly on `$CODEX_HOME/config.toml`.

Exact version-specific syntax remains Executor-owned under D054.

## CLI-version isolation

The first v9 epoch targets the same Codex CLI baseline as v8: `0.149.0`.

If 0.149.0 cannot explicitly realize a permitted non-disabled backend, stop before any live canary or acceptance call with `BLOCKED / WINDOWS_SANDBOX_BACKEND_UNAVAILABLE`.

Do not upgrade Codex inside v9. A host-version change requires a separate prospective revision so backend binding and CLI-version effects are not confounded.

## Pre-model backend resolution gate

Before spending a model call, persist enough resolved host evidence to establish:

- Codex CLI version;
- native Windows platform;
- requested non-disabled backend;
- user config ignored;
- user/project execpolicy rules ignored;
- requested logical sandbox;
- v8 minimal unrelated feature surface;
- dangerous approval/sandbox bypass absent.

If the requested backend cannot be established, stop before canary.

## Synthetic host-capability canary retained

Use the same v8 neutral synthetic Skill semantics:

- `.agents/skills/mx-canary/SKILL.md`;
- unique full body nonce not inferable from metadata;
- neutral prompt explicitly requesting use of the local instruction;
- no holdout or candidate content;
- structured nonce result.

A complete profile passes only when **two fresh repetitions** both prove:

- local Skill metadata discovery;
- successful Skill-body read/use;
- host trace distinction between metadata discovery and body use;
- exact full nonce;
- valid structured output;
- no execution-policy rejection affecting the required body path;
- no unrelated app/plugin catalog material;
- correct workspace mutation postcondition;
- identical non-disabled native Windows backend identity.

Do not spend a second repetition after the first repetition proves a profile has a terminal, repetition-independent failure. Two repetitions are required to establish PASS, not to reconfirm failure.

## Logical sandbox order retained inside each backend

1. logical `read-only` first;
2. logical `workspace-write` only when read-only cannot support the body-read/use path;
3. workspace-write requires zero unexpected model-caused file mutation.

If no backend/logical-sandbox profile passes, stop `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with zero acceptance prompts.

## Acceptance binding

Once a complete profile passes 2/2, freeze it for the entire v9 epoch.

Every acceptance attempt/resume must preserve:

- exact Codex version;
- exact native Windows backend;
- exact logical sandbox;
- GPT-5.6 Sol / Medium;
- ignored config/rules state;
- minimal feature-surface identity.

A disabled/different backend, logical-sandbox drift, required Skill-body policy rejection, or reappearance of unrelated app/plugin material is `HOST_SURFACE_DRIFT`. The affected observation is not scored and new scheduling stops immediately.

## Explicit Skill is not a substitute

Codex supports explicit Skill selection and can host-read explicitly selected Skill contents into prompt fragments. T023, however, evaluates **implicit** activation from ordinary user turns.

Therefore v9 MUST NOT replace acceptance routing with `$skill`, `/skills`, or any preselected Skill invocation. That would change the claim under test.

## Activation observability retained

Scored activation remains actual candidate-body read/use proved by host evidence after metadata discovery.

Model self-report and metadata alone do not score activation.

The harness may recognize a first-party Codex event that unambiguously proves equivalent body load/use; the acceptance semantic is the event's meaning, not a hard-coded `Get-Content` spelling. Any added event extractor remains Executor-owned technical implementation and must be deterministic/tested.

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

V9 adds only the explicit Windows backend identity.

## Dangerous shortcuts forbidden

V9 does not permit:

- `--dangerously-bypass-approvals-and-sandbox` / `--yolo`;
- interactive approvals inside the acceptance cell;
- explicit `$skill` substitution;
- candidate-body injection into the user prompt;
- evaluator-specific manual read grants used only to bypass the normal supported Skill path;
- OS/model/effort substitution;
- silent Codex upgrade.

## Stimulus/environment isolation retained

The model-visible acceptance turn remains exactly:

```text
<exact corpus prompt>

Return only the required structured record.
```

Every attempt uses a fresh OS-temporary disposable root outside/not linked to the canonical checkout and materializes only the frozen role fixture plus exact candidate projection.

## Cost-bounded scheduling retained

V9 preserves the v8 consequence-first order:

1. cross-profile;
2. ambiguous;
3. generic negative;
4. near-miss;
5. positive Consumer;
6. positive source-maintainer;
7. positive external Skill trust;
8. multi-intent.

Paired 2+1 remains unchanged for work still required.

Immediate zero-tolerance failures and optimistic-completion futility stop a candidate exactly as in v8. Stage C begins only after a qualifying B0/B1 reference exists and challengers stop when qualification/material advantage becomes impossible.

The 480-observation matrix remains a **worst-case ceiling**, not a target.

## Thresholds and selection unchanged

V9 retains:

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
- same-epoch resume preserves valid observations and futility states after exact host-profile verification.

Persist available input/cached/reasoning/output/total tokens, tool calls, rejected calls, unrelated-resource counts/bytes, duration, capacity state, Codex version, native backend, logical sandbox and full profile identity.

## Ownership boundary

The v9 oracle and this preregistration are Orchestrator-owned D052/Markdown assets.

The Executor owns mechanical provider/harness implementation, installed-version adapter syntax, backend identity extraction, host-event extraction, scheduling, evidence, metric computation, implementation tests and Code Review & Verify.

No v9 canary/acceptance call may occur before T048 and the v9 oracle are integrated into canonical `develop`.
