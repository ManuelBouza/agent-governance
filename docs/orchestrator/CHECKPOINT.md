# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O052  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T006, T008 and T009 are `ACCEPTED`, integrated and post-integration-cleaned. L002 remains `ANALYZED` and separate.

D036 — Existing-System Assurance Audit Mode — is `ACCEPTED`. PR #73 integrated the staged portable assurance module, D040 migration control and T010 readiness contract. OP007 then retired its planning branch.

T010 remains the next executable implementation task, but before launching it the Human identified an executor-host integration ambiguity: source-maintenance policy could be read as constraining the executor's proprietary orchestration methodology rather than only Governance authority/repository boundaries.

D041 resolves that ambiguity.

## D041 — executor process autonomy

Decision:

`docs/decisions/D041-executor-process-autonomy.md`

Core rule:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

The Agente de IA Ejecutor may independently choose and compose compatible direct work, planning, SDD/specification workflows, sub-agents/workers, Skills, code-graph/navigation tools, testing/review helpers or other executor-native mechanisms.

Agent Governance MUST NOT prescribe internal methodology, agent type, delegation topology or tool routing unless the method itself is material to an accepted product/safety/security/reproducibility/ownership invariant.

Worker topology and private orchestration traces are not Governance acceptance evidence by default. Review remains based on the persisted Task Contract, remote Git state, required verification and handoff.

D026/D030/D031 remain authority/coexistence boundaries; they do not prohibit executor-internal use of SDD or other host capabilities that operate without unauthorized tracked state or overlapping Governance authority.

## D040 / D036 staged state

Canonical Protocol remains `1.12.0`.

`governance-core/ASSURANCE.md` remains version `1.0.0`, `Activation-State: STAGED`, and is not yet routed as an active required Core module.

L001 remains `CONTROL_FAILURE` until T010 plus subsequent D040 Phase-B activation prove the stronger single-version-authority control end-to-end.

## T010 — NEXT EXECUTABLE AFTER D041 PLANNING CLEANUP

Task Contract:

`docs/tasks/T010-d036-deterministic-assurance-audit-contract.md`

Expected executor branch:

`test/d036-deterministic-assurance-audit-contract`

Expected handoff:

`handoffs/T010-executor-handoff.json`

T010 responsibilities remain unchanged:

1. deterministic synthetic D036 assurance semantics covering scope/authorization, profile ceilings, evidence/finding states, severity-confidence separation, coverage accounting, audit/remediation separation, temporal posture and D035/D033/D034 composition;
2. implement D040 by eliminating the independently authored mutable exact-current protocol literal as a second authority while preserving deterministic malformed/version/module validation.

T010 runs while authoritative Protocol remains `1.12.0` and `ASSURANCE.md` remains staged/not routed.

D041 changes only the executor-process boundary: the executor decides how to realize T010 using its available compatible tooling. Governance does not route it to SDD, General Task, particular workers, Skills or CodeGraph.

## OP008 — DRAFT UNTIL D041 PR IDENTITY IS PERSISTED

Operational Contract:

`docs/operations/OP008-retire-executor-process-autonomy-branch.md`

OP008 will retire only the merged D041 Markdown planning branch. Its integrating PR identity must be persisted before status becomes `READY`.

## Persisted executor-instruction invariant

`prompt = bootstrap transport only`; persisted Task/Operational Contract plus referenced Git policy is the complete external execution specification.

The prompt and contract MUST NOT prescribe executor-internal methodology/tool routing unless materially required by an accepted invariant.

## Learning state

L001 — `verification.regression.protocol_version_drift` — `CONTROL_FAILURE`; stronger control D040 selected, T010 + subsequent activation required for re-verification.

L002 — `task.handoff.identity_mismatch` — `ANALYZED`, non-blocking and separate. Do not fold it into D036/T010.

## Next Action

1. Review/integrate the D041 Markdown planning PR and freeze its source branch.
2. Execute OP008 using only its persisted Operational Contract pointer; independently verify remote/local inventories.
3. Launch T010 using only its persisted Task Contract pointer. Do not add instructions about SDD, workers, Skills, CodeGraph or internal orchestration.
4. Review/accept/integrate/clean T010.
5. Perform D040 Phase-B Markdown activation to Protocol `1.13.0`; prove the full deterministic suite remains green and then re-evaluate L001.
6. Treat CodeGraph project initialization as a separate capability/repository-state question; do not mix it into T010 unless separately authorized.
7. Do not start real-system audit adapters/providers until a later explicit decision/Task Contract authorizes them.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if the D041 planning PR is not integrated, load D041 and `docs/TASK-CONTRACTS.md`;
2. if OP008 is pending, load `docs/operations/OP008-retire-executor-process-autonomy-branch.md` plus branch-cleanup policy;
3. for T010 execution/review load T010, D041, D040, L001, D036/`ASSURANCE.md`, D035/`SECURITY.md`, D033/D034/`EXECUTION-CONTROL.md`, and D037 as required by the contract;
4. after T010 closes, load D040 + T010 acceptance evidence + staged `ASSURANCE.md` for Phase-B activation;
5. load L002 only on a concrete handoff-identity conflict or explicit separate control-selection work;
6. do not reload older task history absent regression/audit need.

## Do Not

- Do not write directly to `develop` or `main`.
- Do not prescribe SDD, General Task, a worker topology, Skill routing or CodeGraph use to the executor unless a future accepted invariant materially requires it.
- Do not inspect private executor orchestration as an acceptance requirement unless explicitly contracted.
- Do not merge a Protocol `1.13.0` bump before T010 readiness closes.
- Do not infer intrusive/live assessment authorization from D036/T010.
- Do not add scanner/provider/model/network dependencies to T010.
- Do not treat audit findings as remediation authority.
- Do not create another mutable exact-current protocol-version authority in tests.
- Do not fold L002 into D036/T010.
- Preserve prior procedural audit history.
