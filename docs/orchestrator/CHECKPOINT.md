# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O033  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003 and T005 are `ACCEPTED` and integrated.

T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

T006 is now `READY` and its controlling Core/Task Contract are integrated into `develop` through PR #45.

Current deterministic verification policy remains:

```text
probabilistic implementation assistant != verification authority
source-product acceptance = deterministic evidence + authorized Human/Orchestrator judgment
```

No live LLM/model reviewer may become a required repository verification/release gate without a new explicit Human Owner decision superseding D037.

## T006 — READY FOR EXECUTOR

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Planning/Core integration PR #45:

`d2730f2054a5a0639db28eae4564a47bf6051714`

Required executor branch:

`test/security-verification-contract`

Expected handoff:

`handoffs/T006-executor-handoff.json`

Executor implementation MUST start from a `develop` revision containing the exact T006 Task Contract. The PR #45 squash above is the first such canonical revision.

Do not launch from an older base.

## Canonical executor launch-prompt invariant

`docs/TASK-CONTRACTS.md` now defines the mandatory normal executor launch structure.

Every normal launch prompt is transport/bootstrap only and contains these semantic parts:

```text
role
+ repository/base
+ AGENTS.md bootstrap
+ exactly one authoritative Task Contract pointer
+ completion/return contract
```

Do not duplicate objective, acceptance criteria, scope/files, exclusions, architecture, tests, branch/handoff details, provider-specific rules, safety/security restrictions or protocol versions into the launch prompt when they are already controlled by Git.

If a required task fact is missing, incomplete or stale, persist/fix the Task Contract or controlling repository policy before launch. Do not compensate with chat-only launch instructions.

## D035 Core state

Integrated:

- `governance-core/SECURITY.md` — Security-Verification-Version `1.0.0`;
- `governance-core/GOVERNANCE.md` — Protocol-Version `1.12.0`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md` — T006 implementation boundary;
- T006 deterministic Task Contract.

Core security invariants:

```text
model output != security authority
security guidance freshness != model training freshness
security acceptance = applicable current controls + independent evidence
past task acceptance != permanent security posture
security PASS != execution authorization
execution authorization != security PASS
```

Security outcomes:

`PASS | BLOCK | HUMAN_EXCEPTION`

Freshness states:

`CURRENT | STALE | UNKNOWN | CONFLICT | SUPERSEDED`

Freshness classes:

`THREAT_LIVE | PRODUCT_VERSION | STANDARD_PINNED | PROJECT_DECISION`

Known-bad states are scoped/versioned and include active, mitigated, superseded, not-applicable and bounded-exception disposition.

## T006 deterministic verification boundary

T006 executor work is non-Markdown test scaffolding only.

It must mechanically prove at least:

- authoritative source/applicability/conflict behavior;
- class-aware freshness without wall-clock/network dependence;
- applicable active known-bad state blocks even when model/statistical metadata favors it;
- independent evidence is required for `PASS`;
- Human exceptions are exact-scope, independently supported and expiry-sensitive;
- temporal invalidation changes current posture without rewriting historical acceptance;
- security and D033/D034 execution control cannot grant each other's authority;
- Protocol `1.12.0` and `SECURITY.md` module alignment;
- provider/SDD/model/network/dependency neutrality.

Required verification is defined in the Task Contract and includes focused pytest, full pytest and Ruff check/format in the locked uv environment.

## Provider / SDD separation invariant

Portable Governance Core remains provider-neutral.

`governance-core/SECURITY.md` does not depend on Gentle-AI, GitHub Spec Kit, OpenSpec or another SDD/security/review provider.

Provider-specific lifecycle, commands, paths, schemas, receipts and integration behavior remain outside portable Core semantics and are loaded/implemented only when a concrete provider integration is separately governed.

`COEXISTENCE.md` may name known systems as compatibility examples; those names are not required branches/dependencies in portable Core behavior.

D038/D030 remain relevant only if external-provider evidence/integrity behavior actually affects a future task. They are not implementation dependencies for T006.

## D033/D034 preservation

T006 does not modify `governance-core/EXECUTION-CONTROL.md`.

Security and execution control compose as independent planes:

```text
security evaluation may narrow/block
but cannot expand execution authority

execution authorization/procedure success
cannot manufacture security PASS
```

Do not reinterpret T006 as authorization/runtime/runbook adapter work.

## D036 boundary

D036 remains the next planned architecture layer after T006 closes.

Do not implement D036 audit mode, findings/evidence graph, assurance reporting or coverage semantics inside T006.

## D038 — External provider boundary remains accepted

D038 remains integrated and continues to specialize D030 only for Gentle-AI RDD capability classification.

Relevant invariant if provider work later becomes material:

```text
external evidence != Governance acceptance
external provider lifecycle != Governance task lifecycle
external PASS = evidence, never acceptance authority
external native enforcement may narrow/block but cannot expand authorization
```

Do not load D038/D030 during normal T006 execution/review unless an actual provider/coexistence conflict appears.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.

## Next Action

1. Launch the Agente de IA Ejecutor for T006 using the canonical minimal launch-prompt contract in `docs/TASK-CONTRACTS.md` and exactly one Task Contract pointer.
2. Executor creates/uses `test/security-verification-contract` from current `develop`, implements only authorized non-Markdown scope, runs required deterministic verification, persists/pushes the D029-compliant handoff and returns status/path/branch/HEAD only.
3. ChatGPT reviews remote base/head identity, Task Contract, handoff, complete diff and verification evidence before acceptance.
4. Do not start D036 until T006 is accepted/integrated.

Canonical T006 launch prompt:

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Start from current develop and read AGENTS.md first.

Then load and execute the authoritative Task Contract:
docs/tasks/T006-d035-deterministic-security-verification-contract.md

Treat that Task Contract and its referenced repository policies as the complete execution specification. Do not infer or expand task scope from this prompt.

Complete the required verification and executor handoff, commit and push all authorized work, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. for T006 execution/review load `docs/tasks/T006-d035-deterministic-security-verification-contract.md`;
2. load D035 and `governance-core/SECURITY.md` as the normative security semantics;
3. load `governance-core/GOVERNANCE.md`, D037 and current deterministic test helpers as needed for contract/review;
4. load `governance-core/EXECUTION-CONTROL.md` / D033/D034 only when evaluating the explicit security-vs-execution composition cases;
5. load D038/D030 only if a concrete external-provider conflict appears;
6. load D036 only after T006 closes or if a concrete boundary conflict requires it;
7. do not reload T001–T005 implementation details absent regression/audit need.

## Do Not Load or Do

- Do not reopen T001–T005 absent a concrete regression or explicit Human decision.
- Do not add live LLM/model reviewer output as a required source-product gate.
- Do not fetch live vulnerability/advisory data in T006 deterministic tests.
- Do not add an external security/SDD/review provider dependency to T006 or portable Core.
- Do not couple portable Core semantics to Gentle-AI or another named SDD/provider.
- Do not treat security `PASS` as execution authorization or D033/D034 success as security `PASS`.
- Do not let an implementation/model invent security exceptions.
- Do not use wall-clock/network state as hidden freshness inputs in deterministic tests.
- Do not implement D036 inside T006.
- Do not start an RDD/external-provider executable integration without a separate Task Contract.
- Do not declare the source product stable/release-ready.
