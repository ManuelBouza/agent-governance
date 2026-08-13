# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O057  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Frontier

T006, T008, T009 and T010 are `ACCEPTED`, integrated and post-integration-cleaned. L002 remains `ANALYZED` and separate.

D036 — Existing-System Assurance Audit Mode — is `ACCEPTED` and staged. D040 controls atomic protocol migration/single-version authority. D041 executor-process autonomy is integrated and OP008 cleanup is complete.

D042 remote-baseline freshness is integrated by PR #78. OP010 remains pending to retire the PR #78 source branch.

D043 — Host-native repository instruction loading — is carried by PR #79. It removes unconditional `read AGENTS.md` instructions from normal Task/Operational launch prompts while preserving `AGENTS.md` authority and D042 remote freshness.

## D043 — conditional AGENTS reload

Decision:

`docs/decisions/D043-host-native-repository-instruction-loading.md`

Core rule:

```text
normal launch:
canonical remote freshness
    -> persisted contract
    -> execution

launch after governing AGENTS.md change:
canonical remote freshness
    -> reload current AGENTS.md
    -> persisted contract
    -> execution
```

Compatible executor hosts are expected to load repository-level instructions through their native session/repository bootstrap. If a host lacks that capability, its adapter/session bootstrap must provide equivalent loading; Agent Governance does not compensate by repeating `read AGENTS.md` in every delegated prompt.

The reload condition is based on canonical Git history and is included only when the integrated change governing the next delegated execution modified `AGENTS.md`.

Updated policy surfaces:

- `docs/TASK-CONTRACTS.md`;
- `docs/OPERATION-CONTRACTS.md`;
- `docs/POST-INTEGRATION-CLEANUP-PROMPT.md`.

`AGENTS.md` itself is not modified by D043.

## D040 / D036 staged state

Canonical Protocol remains `1.12.0`.

`governance-core/ASSURANCE.md` remains version `1.0.0`, `Activation-State: STAGED`, and is not yet routed as an active required Core module.

L001 remains `CONTROL_FAILURE` until post-T010 D040 Phase-B activation to Protocol `1.13.0` proves the stronger single-authority control end-to-end.

## Cleanup state

Completed:

- OP009 — T010 acceptance/implementation/cleanup branches retired;
- OP008 — D041 planning branch retired.

Pending:

- OP010 — retire PR #78 / D042 planning branch;
- OP011 — `READY`; after PR #79 is integrated, retire only the merged PR #79 source branch.

## Executor process autonomy

D041 remains active:

```text
Governance owns requested outcome + boundaries + acceptance
Executor owns implementation process + internal orchestration
```

D043 changes only redundant repository-instruction transport. It does not prescribe SDD, General Task, workers, Skills, CodeGraph or executor-internal topology.

## Learning state

L001 — `verification.regression.protocol_version_drift` — `CONTROL_FAILURE`; T010 implemented the stronger D040 Phase-A control, but full re-verification awaits Phase-B activation.

L002 — `task.handoff.identity_mismatch` — `ANALYZED`, non-blocking and separate.

## Next Action

1. Review/integrate PR #79 and freeze its source branch.
2. Execute OP010 using the D043 normal launch form: D042 remote freshness + OP010 pointer, with no explicit `AGENTS.md` read because PR #79 does not modify `AGENTS.md`.
3. Execute OP011 to retire the PR #79 planning branch.
4. Verify remote branches reduce to `develop` and `main`.
5. Then perform D040 Phase-B Markdown activation to Protocol `1.13.0` and re-evaluate L001.
6. Treat CodeGraph project initialization as a separate capability/repository-state operation.

## Next Chat Minimum Load

After repository bootstrap and this checkpoint:

1. if PR #79 is not integrated, load D043 plus Task/Operational bootstrap policy;
2. if OP010 is pending, load `docs/operations/OP010-retire-bootstrap-freshness-branch.md` plus branch-cleanup policy;
3. if OP011 is pending, load its Operational Contract plus branch-cleanup policy;
4. after cleanup, load D040 + T010-R1 + staged `ASSURANCE.md` for Phase-B activation;
5. load L002 only on a concrete handoff-identity conflict or explicit separate control-selection work.

## Do Not

- Do not write directly to `develop` or `main`.
- Do not launch a Task/Operation from stale local repository state; establish current canonical remote baseline before contract load.
- Do not add an unconditional `read AGENTS.md` directive to normal launch prompts.
- Add the D043 reload line only when the governing integrated change modified `AGENTS.md`.
- Do not destructively discard local/uncommitted work merely to establish freshness.
- Do not merge Protocol `1.13.0` activation before pending cleanup closes.
- Do not prescribe executor-internal methodology/tool routing.
- Do not infer intrusive/live assessment authorization from D036/T010.
- Do not add scanner/provider/model/network dependencies to D040 Phase B.
- Do not fold L002 into D036/T010.
- Preserve prior procedural audit history.
