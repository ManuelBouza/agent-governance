# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O041  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T001, T002, T003, T005 and T007 are `ACCEPTED` and integrated. T004 remains terminal `CANCELLED_BY_HUMAN` under D037.

D039 — Evidence-Driven Governance Learning Loop (EGLL) — is `ACCEPTED`. T008 is `READY` but MUST wait until outstanding post-integration branch retirement is complete. T006 remains `READY` unchanged after T008; D036 remains after T006.

## Persisted executor-instruction invariant

PR #61 introduces `docs/OPERATION-CONTRACTS.md` and replaces the old chat-carried cleanup target model.

```text
prompt = bootstrap transport only
persisted contract + referenced Git policy = complete instruction
```

Every delegated executor action MUST be reconstructable from canonical Git without relying on operation-specific prompt text.

Use exactly one persisted contract pointer:

- normal executable/content work -> `docs/tasks/TNNN-*.md` Task Contract;
- bounded non-implementation repository operation -> `docs/operations/OPNNN-*.md` Operational Contract.

Prompts MUST NOT carry targets, branch names, SHAs, deletion decisions, exceptions, commands, acceptance semantics, or other concrete instructions absent from the persisted contract.

The canonical cleanup prompt in `docs/POST-INTEGRATION-CLEANUP-PROMPT.md` is now a pointer to exactly one integrated Operational Contract.

## OP001 — READY after PR #61 integration

Contract:

`docs/operations/OP001-pending-post-integration-branch-retirement.md`

OP001 persistently identifies the currently pending cleanup targets through merged PRs #53–#61, including the special resolved-review evidence for the post-merge advancement of `docs/t007-post-integration`/PR #55.

PR #61 is deliberately included in OP001 before merge so `docs/persisted-operational-contracts` can be retired by the same operation without recursive cleanup-contract creation.

After PR #61 is integrated, launch the executor with only the OP001 contract pointer. Do not put cleanup target IDs, branches, SHAs, or deletion instructions into chat.

## D039 / T008

D039 source-maintainer learning is controlled by:

- `docs/decisions/D039-evidence-driven-governance-learning-loop.md`
- `docs/ARCHITECTURE-GOVERNANCE-LEARNING-LOOP.md`
- `docs/GOVERNANCE-LEARNING.md`

T008 Task Contract:

`docs/tasks/T008-egll-deterministic-learning-detectors.md`

Expected branch: `test/egll-deterministic-learning-detectors`  
Expected handoff: `handoffs/T008-executor-handoff.json`

T008 remains deterministic/local: no live GitHub/network/model/provider/ruleset/Actions dependency and no Governance Core consumer semantics.

## T006 — READY AFTER T008

Task Contract:

`docs/tasks/T006-d035-deterministic-security-verification-contract.md`

Expected branch: `test/security-verification-contract`  
Expected handoff: `handoffs/T006-executor-handoff.json`

T006/D035 semantics remain unchanged. Do not fold T008 or D036 into T006.

## Branch lifecycle hardening

PR #58 established:

```text
merge -> freeze -> cleanup
new work -> new branch from current develop
```

A merged source branch MUST receive no further commits. Post-merge advancement becomes `REVIEW`; valid later work must be recovered through a fresh branch/PR before retirement.

## T007 procedural audit

Preserve the initial executor nonconformance: `eval/d032-agent-capability` was deleted before its missing-PR ambiguity was fully resolved, then restored at the exact original SHA. Persisted T007 R1 later authorized final exact-SHA deletion as cancelled T004 work.

## Orchestrator Direct-Write Audit History

Preserve; do not hide/rewrite without explicit Human authorization:

- T002-R1 placeholder: accidental `6a3bff4f12850bd701fea624815e955231082afa`; corrective `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
- architecture overview placeholder: accidental `a0e063344043fda53f55b8fcb5b03742a33a7185`; corrective `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.
- T004-R1 placeholder: accidental `197ce3fad02a69baf99238beb9859280a137a681`; corrective `52ae6fb5126517ea19c8d00918e7b148c17f146a`.
- D037 placeholder: accidental `71b62980c41b183dfb33ef3099c72fc827234606`; corrective `e5ee3c56cbd17f72f876987550bab34cde065b53`.
- T007-R1 review preparation: accidental temporary non-Markdown `noop` on `docs/t007-r1-branch-cleanup`; removed before integration.
- T007 post-integration prompt work: commits were appended to already-merged `docs/t007-post-integration` after PR #55; recovered through fresh PR #56; basis for merged-branch freeze.
- Operational Contract policy preparation: accidental direct write `46050487d3a066afd37cf340ccd58ab09daddfb9` created placeholder `docs/OPERATION-CONTRACTS.md` on `develop`; history is preserved. PR #61 replaces the placeholder with the intended policy through normal review and records the stronger persisted-instruction invariant.

## Next Action

1. Review and integrate PR #61; freeze `docs/persisted-operational-contracts` immediately after merge.
2. Launch OP001 using the canonical Operational Contract bootstrap prompt with exactly one pointer to `docs/operations/OP001-pending-post-integration-branch-retirement.md`.
3. Verify returned remote/local inventories independently against GitHub. No eligible OP001 target branch may remain remotely; inaccessible local checkouts remain explicitly unverified.
4. Then launch T008 using its normal Task Contract pointer.
5. Review/accept/integrate/clean T008; then resume T006 unchanged.
6. Do not start D036 until T006 closes.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if OP001 not complete, load `docs/OPERATION-CONTRACTS.md`, OP001, `docs/BRANCH-CLEANUP.md`, and `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`;
2. for T008 load its Task Contract, D039 and `docs/GOVERNANCE-LEARNING.md`;
3. load D037/test helpers only as needed for T008 review;
4. after T008 closes, load T006 + D035 + `governance-core/SECURITY.md`;
5. do not reload older task history absent regression/audit need.

## Do Not Load or Do

- Do not delete `main` or `develop`.
- Do not append commits to a merged topic branch.
- Do not place concrete executor instructions in chat when they are absent from the persisted contract.
- Do not let automatic learning components mutate Governance authority.
- Do not use model-based verification gates.
- Do not implement live GitHub enforcement/trend aggregation/consumer EGLL inside T008.
- Do not fold T008 into T006 or D036.
- Do not hide T007 or Orchestrator audit history.
- Do not declare the source product stable/release-ready.
