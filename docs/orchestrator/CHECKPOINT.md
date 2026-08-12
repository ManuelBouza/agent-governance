# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O042  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated. T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

OP001 post-integration branch retirement completed successfully and was independently verified remotely: canonical remote branches were reduced to `develop` and `main` before T008 launch. Local `develop`/`main` cleanup is executor-reported evidence; inaccessible external checkouts are not inferred clean.

D039 — Evidence-Driven Governance Learning Loop (EGLL) — is `ACCEPTED`.

T008 executor returned `PARTIAL` at HEAD `59f0b8bc443636c5a7fbf5d417f185d528cc63e2`. T008-R1 is `REWORK_REQUIRED` only because the required full-suite gate exposes a pre-existing protocol-version baseline drift outside T008 scope. The reviewed T008 implementation itself remains within its contract.

T009 is `READY` as the narrow prerequisite correction. After T009 is accepted/integrated/cleaned, T008 resumes on its existing task branch, incorporates current `develop`, reruns all original gates, refreshes the handoff, and returns for review. T006 remains `READY` unchanged after T008. D036 remains after T006.

## Persisted executor-instruction invariant

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
```

Use exactly one persisted contract pointer:

- normal executable/content work -> `docs/tasks/TNNN-*.md` Task Contract;
- bounded non-implementation repository operation -> `docs/operations/OPNNN-*.md` Operational Contract.

Prompts MUST NOT carry concrete targets, branches, SHAs, deletion decisions, exceptions, commands, acceptance semantics, or other task/operation instructions absent from the persisted contract.

## OP002 — READY after PR #62 integration

Operational Contract:

`docs/operations/OP002-retire-t008-r1-planning-branch.md`

OP002 persistently authorizes only retirement of the source branch of PR #62 after merge. It explicitly excludes the active T008 implementation branch and all executable work.

## L001 — CONTROL_PLANNED

Learning record:

`docs/learning/L001-protocol-version-baseline-drift.md`

Fingerprint:

`verification.regression.protocol_version_drift`

Observed at T008 verification base `bb1a2de8db622141fc975d1c341e82b9bdc4c3c6`:

- `governance-core/GOVERNANCE.md` declares `Protocol-Version: 1.12.0`;
- `tests/_helpers.py` still declares `SOURCE_PROTOCOL_VERSION = "1.11.0"`;
- `tests/test_execution_control_contract.py` still explicitly asserts `1.11.0`;
- full pytest therefore fails independently of the T008 implementation.

Immediate containment: T008 is not accepted and its executor correctly did not repair unrelated baseline tests outside scope.

Selected control: T009 restores deterministic version-alignment verification without changing Core semantics or creating a second protocol authority. L001 cannot become `VERIFIED` until T009 is accepted and T008 subsequently passes on the corrected baseline.

## T009 — READY

Task Contract:

`docs/tasks/T009-protocol-version-baseline-alignment.md`

Expected branch: `test/protocol-version-baseline-alignment`  
Expected handoff: `handoffs/T009-executor-handoff.json`

T009 may only correct the smallest necessary non-Markdown deterministic test/helper baseline. It MUST NOT edit Markdown/Core semantics, T008 implementation, T006/D035/D036, dependencies/configuration, or introduce network/model/provider scope.

Required gates include focused execution-control tests, full pytest, Ruff check, and Ruff format check.

## T008 — REWORK_REQUIRED after T009

Task Contract:

`docs/tasks/T008-egll-deterministic-learning-detectors.md`

Review:

`docs/reviews/T008-R1.md`

Executor branch: `test/egll-deterministic-learning-detectors`  
Reviewed HEAD: `59f0b8bc443636c5a7fbf5d417f185d528cc63e2`  
Implementation anchor: `6cf30513ef545fc276807a22272633f436b956bd`

Independent review confirms T008 changes only its three authorized test/fixture artifacts plus handoff, implements all five required fingerprints, and introduces no Markdown/Core/dependency/config/network/model/provider/ruleset/Actions/consumer-footprint scope expansion.

After T009 closes, T008 SHALL incorporate current `develop` into the existing task branch, rerun the original focused/full/Ruff gates, refresh the handoff, commit/push, and return the canonical T008 response. Do not change T008 detector semantics unless a new persisted review/revision explicitly authorizes it.

## D039 source-maintainer learning

Controlled by:

- `docs/decisions/D039-evidence-driven-governance-learning-loop.md`
- `docs/ARCHITECTURE-GOVERNANCE-LEARNING-LOOP.md`
- `docs/GOVERNANCE-LEARNING.md`

Automatic findings are evidence/learning candidates only; they do not create Governance authority or self-approve remediation.

## T006 — READY AFTER T008

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Expected branch: `test/security-verification-contract`  
Expected handoff: `handoffs/T006-executor-handoff.json`

T006/D035 semantics remain unchanged. Do not fold T008/T009 or D036 into T006.

## Branch lifecycle hardening

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

A merged source branch MUST receive no further commits. Post-merge advancement becomes `REVIEW`; valid later work must be recovered through a fresh branch/PR before retirement.

## Procedural audit history

Preserve; do not hide/rewrite without explicit Human authorization:

- T007 executor: `eval/d032-agent-capability` was initially deleted before missing-PR ambiguity was fully resolved, then restored at exact original SHA; persisted T007-R1 later authorized final deletion.
- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19e8b002eb6ee85281401`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.
- T007-R1 review preparation: accidental temporary non-Markdown `noop` on `docs/t007-r1-branch-cleanup`; removed before integration.
- T007 post-integration prompt work: commits were appended to already-merged `docs/t007-post-integration` after PR #55; recovered through PR #56; basis for merged-branch freeze and T008 regression fixture.
- Operational Contract policy preparation: accidental direct write `46050487d3a066afd37cf340ccd58ab09daddfb9` created placeholder `docs/OPERATION-CONTRACTS.md` on `develop`; PR #61 corrected it through normal review and preserved history.

## Next Action

1. Review/integrate PR #62 containing T008-R1, L001, T009, OP002, and this checkpoint; freeze its source branch immediately after merge.
2. Launch OP002 using only the canonical Operational Contract bootstrap prompt and pointer to `docs/operations/OP002-retire-t008-r1-planning-branch.md`; independently verify retirement.
3. Launch T009 using only the canonical Task Contract bootstrap prompt and pointer to `docs/tasks/T009-protocol-version-baseline-alignment.md`.
4. ChatGPT reviews T009 handoff/diff/evidence; after acceptance, integrate and post-integration-clean T009.
5. Resume T008 on its existing task branch exactly as specified by T008-R1; review again.
6. After T008 acceptance/integration/cleanup, resume T006 unchanged.
7. Do not start D036 until T006 closes.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if OP002 not complete, load `docs/operations/OP002-retire-t008-r1-planning-branch.md` plus branch-cleanup policy;
2. if T009 is not closed, load `docs/tasks/T009-protocol-version-baseline-alignment.md`, `docs/learning/L001-protocol-version-baseline-drift.md`, and `docs/reviews/T008-R1.md`;
3. for T008 re-review load its Task Contract, T008-R1, handoff, D039 and `docs/GOVERNANCE-LEARNING.md`;
4. load D037/test helpers only as needed;
5. after T008 closes, load T006 + D035 + `governance-core/SECURITY.md`;
6. do not reload older task history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not delete or repurpose the active T008 branch through OP002.
- Do not append commits to a merged topic branch.
- Do not place concrete executor instructions in chat when absent from the persisted contract.
- Do not accept T008 while its required full-suite gate is red.
- Do not fix the protocol baseline inside T008 by chat-only scope expansion.
- Do not let automatic learning components mutate Governance authority.
- Do not use model-based verification gates.
- Do not fold T008/T009 into T006 or D036.
- Do not hide procedural/audit history.
- Do not declare the source product stable/release-ready.
