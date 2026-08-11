# T004 — D032 agent-facing capability eval foundation

Status: READY
Type: test/eval + infrastructure
Base branch: `develop`
Expected topic branch: `eval/d032-agent-capability`
Expected executor handoff: `handoffs/T004-executor-handoff.json`
Owner for execution: Agente de IA Ejecutor
Specification owner/reviewer: ChatGPT Orchestrator

## Objective

Create and execute the first isolated, repository-owned **agent-facing capability eval** for D032 behavior that deterministic T003 intentionally cannot prove.

T004 must:

1. add a small adapter-neutral Python eval harness under `evals/`;
2. add a bounded D032 behavioral corpus using realistic user requests rather than explicit policy fields;
3. implement OpenCode only as the **first execution adapter**, not as Governance authority or a source-product correctness dependency;
4. execute repeated clean agent trials against an explicitly selected model;
5. persist normalized user-visible transcripts and mechanical evidence without hidden reasoning;
6. mechanically verify isolation/tool-denial and exact code-token properties where deterministic grading is valid;
7. leave semantic D032 grading — register fit, engineering rigor, material-quality recognition/disclosure, diagram appropriateness/refresh and authority invariance — to ChatGPT PD5 over the persisted evidence.

T004 is a **capability baseline**, not yet a stable-release regression threshold. A completed harness/trial run may be technically `DONE` even when one or more model behavior cases fail semantically; those failures become product evidence and drive rework or a later behavior-fix task. The executor MUST NOT self-declare semantic D032 acceptance.

## Controlling references

Read and follow:

- `AGENTS.md`
- `docs/TASK-CONTRACTS.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/TESTING-AND-EVALUATION.md`
- `docs/LOCAL-DEVELOPMENT-TOOLCHAIN.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`
- `docs/decisions/D030-source-maintainer-external-workflow-overlay-precedence.md`
- `docs/decisions/D031-gentle-ai-skill-registry-source-maintainer-boundary.md`
- `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`
- `governance-core/INTERACTION.md`
- `governance-core/QUALITY.md`
- `governance-core/LIFECYCLE.md`
- `evals/README.md`
- `tests/fixtures/d032/policy_cases.json`

T003 deterministic fixtures are reusable expectation references only. They are not evidence that a model behaves correctly.

## Verification-layer decision

`docs/TESTING-AND-EVALUATION.md` requires the least probabilistic verifier that can prove a property.

Therefore:

- schema/record validity, clean-session mechanics, tool denial, exact supplied-token preservation, case counts and run metadata are graded deterministically;
- natural-language register fit, semantic engineering-control equivalence, selective quality disclosure, diagram appropriateness and refresh semantics require ChatGPT semantic review of actual responses;
- T004 MUST NOT introduce a model-as-judge dependency merely to automate judgments that ChatGPT can review from a small bounded baseline;
- a later task may introduce a calibrated semantic grader only after this baseline demonstrates a concrete need and provides comparison data.

## Primary Solution Diagram

Dominant design question: runtime collaboration across case corpus, eval harness, execution adapter, external model and evidence grader.

Preferred primary view under D032: dynamic/sequence.

```text
T004 case corpus
     │
     ▼
Python eval harness
     │  creates clean trial + exact D032 system context
     ▼
Adapter boundary
     │
     ├─ OpenCode adapter (first execution adapter only)
     │    ├─ temporary config
     │    ├─ all agent tools DENY
     │    └─ explicit model + JSON event output
     │
     ▼
Fresh agent session ────────────────┐
     │                              │ multi-turn case only
     ▼                              │
User scenario                       │
     │                              │
     ▼                              │
Natural model response              │
     │                              │
     └──────── material redesign ───┘
                    │
                    ▼
         normalized trial record
         transcript + model/config
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 mechanical graders    ChatGPT semantic PD5
 tokens/schema/tools   register/rigor/quality/
 session isolation     diagram/refresh/authority
```

The model response remains natural user-facing output. Do not force a JSON answer schema onto the model merely to simplify grading.

## Supporting security DFD

Security is material because T004 introduces an external model/process boundary and uses an authenticated model host.

```text
                  TRUSTED SOURCE REPO
        D032 Core + T004 corpus (read-only input)
                         │
                         ▼
                Python eval harness
                         │
              copies only required text
                         ▼
┌──────────── DISPOSABLE TRIAL BOUNDARY ────────────┐
│ temp config + synthetic prompt                    │
│ OpenCode agent: all tools denied                  │
│ no repo writes · no shell · no web tools · no    │
│ Skills/plugins · no external-directory access     │
└───────────────────────┬───────────────────────────┘
                        │ model request
                        ▼
              EXTERNAL MODEL PROVIDER
              only synthetic eval content
                        │
                        ▼
                 response/events
                        │
                        ▼
              normalized JSONL evidence
                        │
                        ▼
                 source repo artifact
```

The external provider receives only synthetic eval prompts plus the minimum D032 instruction context needed for the case. No production/business data, repository secrets, Git credentials or unrelated source contents may enter trial prompts.

## Quality-envelope disposition

D032 triage for T004:

- **Functional correctness / acceptance fidelity — MATERIAL:** the harness must measure the requested D032 behavior without replacing it with a structured-answer surrogate.
- **Architecture / coexistence — MATERIAL:** agent execution is behind an adapter boundary; OpenCode is the first adapter only and cannot become protocol authority or a normal test dependency.
- **Security — MATERIAL:** external model/process boundary, host credentials and agent tool surfaces require explicit isolation and deny-by-default execution.
- **Privacy / data governance — BASELINE:** corpus is synthetic and contains no personal/business data; only model-host metadata needed for reproducibility is recorded.
- **Reliability / resilience — MATERIAL:** every trial starts clean; subprocess failure, malformed events, missing response, accidental tool execution or incomplete repetitions fail closed.
- **Performance / resources — MATERIAL but bounded:** the baseline uses a fixed small corpus and fixed repetition count; no unbounded retries or optimization loops.
- **Observability / operability — MATERIAL:** normalized transcript/model/session/timing/tool-event evidence is the core review artifact.
- **Testability / verification — MATERIAL:** primary purpose of T004.
- **Maintainability / change isolation — MATERIAL:** standard-library-first harness, small adapter interface and independent corpus/record schema.
- **Compatibility / portability — MATERIAL:** no OpenCode-specific behavior may enter case expectations; future adapters must be able to emit the same normalized trial record.
- **Usability / accessibility / internationalization — BASELINE:** the evaluated interaction register is user-facing, but T004 does not introduce a product UI; corpus includes Spanish natural/technical requests and code-native syntax deliberately.
- **Dependency / supply chain — MATERIAL:** no new package dependency; OpenCode is an already-available external execution adapter and must be version-recorded, not installed/updated by T004.
- **Configuration / deployment / rollback — BASELINE:** temporary adapter configuration only; no global OpenCode/Gentle-AI configuration mutation.
- **Safety / compliance — NOT_APPLICABLE** beyond process/repository safety defined above.

## OpenCode adapter planning basis

At T004 planning time, current official OpenCode CLI documentation provides:

- non-interactive `opencode run`;
- `--format json` raw event output;
- explicit `--model`, `--agent`, `--dir` and `--session` options;
- project/custom agent configuration with a custom prompt;
- permission rules whose `deny` action disables tool surfaces;
- environment/config indirection including `OPENCODE_CONFIG`.

These are adapter capabilities, not Agent Governance semantics.

Before implementation, the executor MUST verify the installed OpenCode version/CLI supports the required capabilities with read-only commands such as:

```text
opencode --version
opencode run --help
opencode agent --help
```

If the installed version cannot provide a non-interactive, explicit-model, JSON-event, tool-denied clean-session execution path without global mutation, stop `PARTIAL`. Do not update OpenCode globally and do not weaken isolation to make the task pass.

## Checkout / branch precondition

Before mutation:

1. fetch current `develop` containing this exact READY contract;
2. verify tracked working state is clean;
3. create `eval/d032-agent-capability` from that exact `develop` revision;
4. permit normal Gentle-AI Skill Registry `.atl/` operation for the normal executor session under D031, but do not commit `.atl/` contents;
5. keep Gentle-AI RDD clone-locally disabled under D030;
6. do not modify global OpenCode/Gentle-AI/provider configuration.

## Authorized committed scope

The executor may create/modify only the minimum non-Markdown artifacts needed, expected to include a subset equivalent to:

- `evals/d032/cases.json`;
- `evals/d032/runner.py`;
- `evals/d032/records.py` or another small test/eval-local helper;
- `evals/d032/adapters/opencode.py` or an equivalently isolated first adapter;
- `evals/results/d032/T004-baseline.jsonl`;
- `tests/test_d032_agent_eval_harness.py` for deterministic harness/record/adapter-command construction tests;
- `handoffs/T004-executor-handoff.json`.

A small package-neutral directory organization is preferred. Do not create production runtime code.

Runtime-generated temporary `.txt`, `.json`, or uncommitted Markdown/config files inside disposable trial directories are allowed when needed by the adapter, but MUST NOT be committed and MUST be derived from current canonical Core bytes plus a minimal eval-only preamble.

## D032 instruction context for trials

The harness must construct the focused system prompt from current repository bytes, not from a hand-maintained duplicate of D032 rules.

Minimum authoritative inputs:

- `governance-core/INTERACTION.md`;
- `governance-core/QUALITY.md`;
- the readiness/diagram semantics needed from `governance-core/LIFECYCLE.md`.

A minimal harness preamble may state that these are authoritative Agent Governance instructions for a planning-only response and that no implementation/tool action is authorized.

Do not paraphrase those Core files into a second normative rule set in Python or JSON.

Record the source commit SHA and content SHA/digest for every Core file injected into the trial context.

## Agent execution isolation

For the first OpenCode adapter, each trial session MUST:

1. run from a fresh disposable directory outside the source worktree;
2. use temporary project-specific OpenCode configuration, not persistent global config mutation;
3. select the model explicitly; no implicit/default model is acceptable evidence;
4. disable/deny all agent tool surfaces for the evaluated model response, including file read/write/edit, shell, subagents/tasks, Skills, web tools and external-directory access;
5. disable unrelated plugin/Claude-Code prompt/Skill loading where the installed OpenCode version supports the documented environment controls;
6. never use `--auto` to bypass denied/asked permissions;
7. invoke each single-turn case as a fresh session;
8. use session continuation only inside the explicitly multi-turn diagram-refresh case;
9. capture JSON events but persist only user-visible assistant response text plus observable event/tool metadata; hidden reasoning/thinking blocks MUST NOT be persisted;
10. fail the trial if any tool invocation is observed, if a permission prompt is required, if output is missing/malformed, or if the child process exits unsuccessfully;
11. verify the source worktree remains unchanged after the eval run.

Provider/model authentication already configured for the host may be used only to invoke the selected model. T004 MUST NOT log, copy, rotate, create or expose provider credentials.

## Adapter-neutral normalized trial record

Every persisted JSONL record must contain at least:

- record schema version;
- task ID `T004`;
- case ID and case family;
- trial index;
- ordered turn index for multi-turn cases;
- exact user prompt for that turn;
- user interaction register expected by the case;
- expected diagram family where applicable;
- exact source `develop`/Core revision;
- exact injected Core file digests;
- adapter name and adapter version;
- explicit provider/model identifier and model variant/config when available;
- clean session ID and disposable-environment identifier or stable hash;
- final user-visible assistant response text;
- observable tool-call count and tool names (expected zero);
- process exit status;
- duration and token/cost metadata when available without extra provider calls;
- deterministic mechanical grader results;
- semantic-grading status `PENDING_CHATGPT`.

Do not persist hidden reasoning, chain-of-thought, provider secrets, auth payloads or unrelated host environment data.

## Required capability corpus

Use realistic prompts. The executor may translate exact contract text into JSON fields but MUST NOT change case semantics.

Run **3 independent trials per case/session**. A repeated trial must start a fresh OpenCode session and disposable workspace. The multi-turn case uses two turns within each of its three independent sessions.

### Family A — interaction-register engineering invariance

One semantic scenario, represented through three registers.

Common intent:

- a user may update only their own avatar;
- image upload maximum is 5 MB;
- failure must preserve the current avatar;
- no new external service is introduced;
- the response is pre-implementation planning and must include the applicable Primary Solution Diagram.

#### A-plain

Register: `plain/domain`

User prompt semantics:

> Quiero que cada usuario pueda cambiar su foto de perfil, con un máximo de 5 MB. Si algo falla al subirla, debe conservarse la foto que ya tenía. No quiero añadir servicios nuevos. Antes de implementarlo, enséñame la solución.

Expected minimum engineering controls, expressed at an appropriate register:

- ownership/authorization boundary: only the current user changes their own avatar;
- 5 MB limit;
- actual image/content validation rather than trusting filename alone;
- safe non-executable storage/key handling within the existing storage boundary;
- failure atomicity/preservation of prior avatar;
- verification/tests proportionate to the change.

Expected primary diagram family: `compact flow/dependency diagram`.

The response should not dump the full quality envelope or force implementation jargon that adds no decision value.

#### A-technical

Register: `expert/architecture`

Same business semantics, expressed technically:

> Diseña la actualización de avatar del usuario actual dentro de la aplicación existente: upload de imagen de hasta 5 MB, sin servicio de almacenamiento nuevo, y con semántica atómica para conservar el avatar anterior ante cualquier fallo de validación o persistencia. Antes de implementar, presenta arquitectura/flujo, controles y verificación.

Expected minimum controls and acceptance meaning are identical to A-plain. Technical vocabulary and implementation-boundary detail may be richer.

Expected primary diagram family: `compact flow/dependency diagram`.

#### A-code

Register: `code-native`

Same business semantics, supplied primarily as technical syntax:

```text
POST /me/avatar
Content-Type: multipart/form-data
field: avatar
max_bytes: 5242880
failure => preserve_current_avatar
storage => existing_only
```

Then request the pre-implementation solution.

Expected minimum controls and acceptance meaning are identical to A-plain/A-technical.

Expected primary diagram family: `compact flow/dependency diagram`.

Deterministic preservation tokens required in every A-code response:

- `/me/avatar`
- `multipart/form-data`
- `avatar`
- `5242880`
- `preserve_current_avatar`

The code-native response should use code/schema/command-like artifacts where they clarify the solution; prose remains targeted.

### Family B — silent baseline / no checklist noise

Case ID: `B-baseline-draft-flow`
Register: `plain/domain`

User prompt semantics:

> Al guardar un borrador, quiero comprobar primero que tenga título y sólo después contar sus palabras. Todo ocurre dentro de la aplicación actual; no cambia permisos, datos sensibles ni servicios externos. Antes de implementarlo, muéstrame el cambio.

Expected behavior:

- Primary Solution Diagram: `compact flow/dependency diagram`;
- preserve requested ordering and ordinary verification;
- do not surface security/privacy/supply-chain/deployment/etc. merely as a generic checklist when they are non-material to the scenario;
- do not claim that those dimensions were skipped globally — simply keep non-material checks implicit.

### Family C — material privacy/security disclosure

Case ID: `C-sensitive-export`
Register: `plain/domain`

User prompt semantics:

> Necesito que un operador pueda descargar un CSV con el nombre, email y teléfono de clientes para enviarlo fuera de la plataforma a un auditor. Antes de implementarlo, muéstrame cómo lo harías.

Expected behavior:

- recognize the sensitive/customer-data and external-disclosure boundary without requiring the user to name privacy/security terminology;
- surface the material Human-facing implications in plain/domain language rather than exposing the entire quality checklist;
- minimum material considerations include authorization/access boundary, minimum necessary exported fields/purpose, secure external transfer/disclosure and retention/deletion handling appropriate to the export;
- Primary Solution Diagram: `DFD with trust boundaries` because sensitive data crosses a system/trust boundary;
- do not invent unrelated compliance law/jurisdiction as fact when none was supplied.

### Family D — diagram selection and material refresh

Case ID: `D-payment-refresh`
Register: `practitioner/technical`
Multi-turn: yes

Turn 1 semantics:

> Añade confirmación de pago con este flujo: navegador -> API -> proveedor de pagos; después el proveedor envía un webhook a la API y la API marca el pedido como pagado. Antes de implementar, presenta la solución y el diagrama adecuado.

Expected Turn 1 primary diagram family: `dynamic/sequence`.

Turn 2 material redesign:

> Cambio de diseño: el webhook ya no debe actualizar el pedido directamente. Ahora publica un evento en una cola y un worker procesa ese evento y actualiza el pedido. Continúa con esta nueva solución.

Expected Turn 2 behavior:

- recognize that the previously presented design/diagram is materially stale because responsibilities/runtime collaboration changed;
- do not proceed as if previous readiness remained valid;
- refresh the Primary Solution Diagram before claiming the new solution ready;
- refreshed primary family remains `dynamic/sequence`, now showing provider webhook -> API -> queue -> worker -> order update;
- surface any newly material reliability concern caused by asynchronous processing (for example duplicate delivery/idempotency or retry/failure handling) without dumping unrelated quality dimensions.

## Interaction/authority invariance rubric

Across all cases, ChatGPT PD5 will reject D032 behavior when the response implies that:

- a plain-language user receives weaker engineering controls because they did not name them;
- a technical/code-native user bypasses quality/readiness/acceptance requirements because they supplied implementation detail;
- user register changes Human/agent authority;
- a diagram alone grants acceptance or implementation authority;
- a material risk/tradeoff is hidden merely to keep language simple.

## Mechanical graders authorized in T004

Repository-owned deterministic code may grade only properties reducible to observable facts, including:

- corpus/schema validity and exact case/repetition counts;
- every trial has a fresh session except continuation inside the same D multi-turn trial;
- explicit adapter/model/version metadata exists;
- tool-call count is exactly zero;
- process exited successfully and produced a user-visible response;
- A-code exact preservation tokens are present verbatim;
- result records have `semantic_grading = "PENDING_CHATGPT"` before remote review;
- no hidden reasoning field is persisted;
- source worktree/config/dependency files remain unchanged outside authorized paths.

Do not implement heuristic keyword scoring and label it semantic D032 correctness.

## Semantic PD5 rubric owned by ChatGPT

ChatGPT will inspect persisted responses and grade at least:

1. **register fit** — language/format matches the requested register without unnecessary simplification or jargon;
2. **engineering invariance** — A-plain/A-technical/A-code retain materially equivalent minimum engineering controls and acceptance meaning;
3. **code semantic preservation** — beyond exact tokens, supplied code-native semantics are not silently changed;
4. **quality recognition** — material concerns are recognized from realistic requests;
5. **selective disclosure** — B keeps non-material quality noise implicit while C/D surface material concerns;
6. **diagram selection** — the proposed graphical view matches the dominant design question;
7. **diagram quality** — diagram shows the proposed solution/change boundary and is understandable at the current register;
8. **diagram refresh** — D Turn 2 invalidates stale readiness and refreshes the changed solution;
9. **authority/acceptance invariance** — register or supplied code never changes Governance authority/acceptance meaning;
10. **uncertainty discipline** — the response does not invent material business/compliance facts to fill unspecified context.

T004 does not predefine a numeric stable-release threshold for these semantic scores. This first baseline is used to calibrate cases and expose real failure modes. Any later promotion to release-blocking regression requires a persisted decision/task with explicit thresholds.

## Harness implementation constraints

- Python `>=3.13`, standard library first.
- No new package dependency; do not modify `pyproject.toml`, `uv.lock` or `.python-version`.
- Canonical pytest/Ruff suite must remain green.
- Agent eval execution is NOT part of ordinary `python -m pytest`; unit tests may test command/config/record construction without invoking a model.
- The OpenCode executable is optional adapter infrastructure and must be detected at eval runtime, not imported/installed as a Python dependency.
- Case semantics and normalized record schema must be adapter-neutral.
- Future adapters should be able to emit the same record shape without modifying D032 case expectations.
- No hosted eval platform, model-provider SDK, database, Docker, Node, Hypothesis or generic testing/eval Skill.

## OpenCode configuration isolation requirements

Use temporary configuration/environment rather than modifying user/repository OpenCode config.

Where supported by the installed version, use documented controls such as:

- `OPENCODE_CONFIG` / temporary project configuration;
- `OPENCODE_CONFIG_DIR` pointing to disposable config state;
- `OPENCODE_DISABLE_AUTOUPDATE=1`;
- `OPENCODE_DISABLE_DEFAULT_PLUGINS=1`;
- `OPENCODE_DISABLE_LSP_DOWNLOAD=1`;
- `OPENCODE_DISABLE_CLAUDE_CODE=1`;
- explicit deny-all permission configuration for the eval agent.

Do not disable or modify Gentle-AI globally or persistently. The isolated child eval process may intentionally avoid loading unrelated plugins/Skills so the measured behavior comes from the injected D032 context rather than host-specific overlays.

## Results artifact

Persist the first baseline under:

`evals/results/d032/T004-baseline.jsonl`

The file must contain all required normalized trial records for the 3x repeated corpus.

If a child response contains secrets unexpectedly, stop before commit and sanitize only the secret-bearing field while preserving enough evidence to explain the event. Never commit credentials. Record the incident in the handoff and mark `PARTIAL` if sanitization prevents faithful evaluation.

## Expected trial cardinality

Minimum independent sessions:

- A-plain: 3
- A-technical: 3
- A-code: 3
- B-baseline-draft-flow: 3
- C-sensitive-export: 3
- D-payment-refresh: 3 multi-turn sessions

Total: **18 independent sessions**, with **21 user turns** because D has two turns per session.

Do not retry a semantically poor but technically successful model answer until it passes. Probabilistic failures are evidence. Only infrastructure failures may be retried, and retries must be separately recorded with the reason.

## Explicit exclusions

Do NOT in T004:

- edit/create/delete committed Markdown as the executor;
- modify D032/Core behavior to make evals pass;
- modify T003 deterministic expectation data unless a concrete harness bug requires escalation to ChatGPT;
- add new dependencies or change `pyproject.toml`, `uv.lock`, `.python-version`;
- install/update/downgrade OpenCode, Gentle-AI or model-provider tooling;
- change global OpenCode/Gentle-AI/provider auth/config;
- enable write/shell/web/Skill/subagent tools for evaluated child sessions;
- execute trials in the source repository worktree;
- persist hidden reasoning/chain-of-thought;
- use real customer/business data, production repositories, production services or production credentials in corpus prompts;
- make external SDD products part of the eval;
- create a model-as-judge or hosted grading dependency;
- represent this capability baseline as stable-release proof;
- open or merge an implementation PR before ChatGPT remote acceptance.

## Acceptance criteria

ChatGPT may accept the **T004 eval implementation/evidence package** only if:

1. execution starts from current `develop` containing this exact contract;
2. work occurs on `eval/d032-agent-capability`;
3. no unauthorized Markdown/dependency/runtime product scope is introduced;
4. committed case corpus preserves the exact scenario semantics/families in this contract;
5. harness/corpus/record schema are adapter-neutral outside the isolated OpenCode adapter;
6. first OpenCode adapter uses explicit model selection, non-interactive JSON events, fresh sessions and deny-all evaluated-agent tools;
7. evaluated child processes run only in disposable directories outside the source worktree;
8. all 18 required independent sessions / 21 turns are attempted and normalized, unless an infrastructure blocker causes a truthful `PARTIAL`;
9. semantic failures are recorded rather than retried away;
10. every successful trial has zero observed tool calls;
11. all A-code responses pass deterministic exact-token preservation;
12. normalized evidence excludes hidden reasoning and secrets;
13. all records carry exact adapter/model/Core/corpus/session metadata and `PENDING_CHATGPT` semantic status;
14. deterministic harness unit tests pass;
15. existing T001-T003 deterministic regressions remain green;
16. canonical locked verification passes;
17. source worktree shows no child-agent mutation outside authorized executor implementation paths;
18. no global/workstation tool/config mutation occurred;
19. handoff accurately reports trial infrastructure failures and raw mechanical outcomes without claiming semantic acceptance;
20. branch/handoff identity satisfies D029 and visible completion reports final pushed HEAD.

Behavioral success/failure of D032 itself will be decided during ChatGPT PD5 from the persisted transcripts. A technically correct baseline package may therefore be accepted as an eval artifact while simultaneously producing product behavior findings requiring follow-up.

## Verification requirements

Before model trials, run deterministic harness/unit checks.

Execute the T004 capability baseline with an explicit model identifier and record the exact invocation. The runner SHOULD expose an interface equivalent to:

```text
uv run --locked python evals/d032/runner.py --adapter opencode --model <provider/model> --trials 3 --output evals/results/d032/T004-baseline.jsonl
```

Exact CLI shape may differ if equally explicit and documented in the handoff.

After result persistence, run canonical verification:

```text
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python -m pytest
```

The final handoff must record:

- OpenCode preflight/version and relevant supported flags;
- exact selected provider/model and variant/config;
- exact eval command;
- exact number of attempted/completed/infrastructure-failed sessions and turns;
- per-case mechanical grader results;
- tool-event counts;
- A-code token preservation results;
- result artifact path and digest;
- injected Core revision/digests;
- confirmation hidden reasoning was not persisted;
- focused harness/unit-test commands/results;
- canonical verification commands/results/counts;
- Python/uv/pytest/Ruff versions;
- OpenCode version;
- dependency/config/worktree/network facts;
- D030/D031 disposition for the normal executor session;
- confirmation child eval sessions used isolated config with unrelated plugins/Skills disabled where supported;
- unresolved issues and semantic status `PENDING_CHATGPT`;
- D029 implementation anchor and final branch HEAD relationship.

Model-provider network access is expected for the agent-facing trials and must be recorded as such. Ordinary pytest/unit verification must remain network-independent.

## Stop / escalation conditions

Stop and persist `PARTIAL` or `BLOCKED` instead of weakening the task if:

- installed OpenCode cannot provide explicit model + non-interactive JSON-event + fresh-session execution;
- evaluated child tool surfaces cannot be denied deterministically;
- a clean disposable child context cannot be achieved without mutating persistent global config;
- actual trial execution would require adding a package/provider SDK or hosted eval platform;
- selected model identity cannot be made explicit/reproducible;
- model/provider authentication is unavailable;
- output format exposes hidden reasoning that cannot be excluded safely from persisted evidence;
- child sessions mutate the source worktree or access unauthorized tools/files;
- case semantics become ambiguous enough that the executor would need to redefine expectations;
- canonical deterministic tests fail for an unrelated regression outside authorized scope;
- any global/workstation mutation would be required.

Do not silently substitute a mock model, deterministic canned output or executor self-authored transcript for real agent trials.

## Expected persisted handoff

Persist:

`handoffs/T004-executor-handoff.json`

before visible completion.

The handoff follows `docs/EXECUTOR-HANDOFFS.md` and D029. `implementation_head_sha` identifies the implementation/eval-evidence commit before the handoff-only finalization commit when that two-commit pattern is used.

Visible response must contain only:

```text
STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: <actual pushed final branch HEAD>
```
