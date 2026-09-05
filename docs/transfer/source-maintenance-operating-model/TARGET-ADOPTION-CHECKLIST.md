# Target Adoption Checklist

Status: PORTABLE PROCEDURE / TARGET MUST ADOPT OR ADAPT

Use this checklist in the separate target-repository adoption chat. It is intentionally repository/provider neutral.

## Gate 0 — bind the target

Before any target mutation, establish:

- exact target repository;
- canonical provider/read surface;
- current default/stable branch;
- integration/development branch if one exists;
- current target governing instructions;
- current target durable frontier/state if any;
- active agent/connector identities and writable capabilities.

If target identity is missing or ambiguous, remain read-only.

## Gate 1 — target cold start

1. Read current canonical target branch identity.
2. Read target-local governing instructions (`AGENTS.md` or equivalent) from that exact revision.
3. Discover existing governance/specification/task/handoff/runbook/checkpoint systems.
4. Inspect current long-lived branch topology and server-side protection.
5. Inspect existing source-maintenance/executor/workspace conventions.
6. Do not create Agent Governance artifacts yet.

## Gate 2 — overlap classification

For each capability in the portable operating model, classify exactly one target disposition:

- `REUSE` — target already satisfies the semantic requirement;
- `ADAPT` — target has a compatible mechanism needing bounded extension/mapping;
- `COEXIST` — both mechanisms can remain without authority collision;
- `MISSING` — target lacks the capability and needs a target-native implementation;
- `CONFLICT` — existing authority collides materially; stop for Human resolution.

At minimum classify:

- canonical authority/cold-start;
- objective-scoped Orchestrator lifecycle;
- SDD/role stage ownership;
- spec delta/traceability;
- oracle/test ownership;
- execution access-control envelope;
- runbook/operation-resolution model;
- topic-branch write guard;
- long-lived branch protection;
- Task/Operational Contract carrier;
- Executor handoff/evidence carrier;
- coordinator continuity;
- coordinator-first delegation;
- worktree/workspace isolation;
- persistent local-Git/Library adapter if desired;
- lock/CAS/sentinel concurrency;
- publication freshness;
- Executor bounded repair;
- post-repair persistent-state re-sync;
- snapshot lifecycle/GC;
- checkpoint/bootstrap mismatch semantics;
- research-to-decision traceability.

## Gate 3 — preserve stronger controls

Before proposing a new target rule:

- identify stronger compatible project-native controls;
- preserve them;
- reference/adapt rather than duplicate existing current truth;
- do not reduce review counts, status checks, code-owner rules, signing, deployment gates, security controls or other stricter requirements merely to match the source baseline.

A source example is a floor for the extracted semantic property, not permission to weaken the target.

## Gate 4 — writable readiness

If the provider supports technical long-lived branch protection, normal agentic writable work remains blocked until effective protection is verified.

Verify:

- exact long-lived branch targets;
- PR/MR transport requirement;
- deletion restriction;
- force/non-fast-forward protection;
- no routine bypass for the normal automated write identity;
- active/enforced state.

If the active connector cannot administer required protection:

```text
REQUIRE_HUMAN
-> state exact missing control
-> Human/repository admin applies it
-> re-read effective provider state
-> only then clear writable readiness
```

Do not prove protection by deliberately attempting a destructive direct write when effective configuration is observable.

## Gate 5 — target-native design and authority

Create target-native artifacts for the chosen adoption. Do not reuse source `Dxxx`/`Rxxx` IDs as if already accepted by the target.

Persist:

- target adoption decision(s);
- target role/stage mapping;
- target branch/workspace mapping;
- target checkpoint/frontier carrier;
- target task/handoff schema or mapping;
- target runbook/operation adapter mapping when relevant;
- target safety-control receipt/ledger entry for branch protection;
- target research/evidence provenance;
- explicit unresolved-gap disposition.

The target decision should identify source provenance, for example:

```text
source_repository: ManuelBouza/agent-governance
source_bundle: docs/transfer/source-maintenance-operating-model/
source_extraction_baseline: 0e2edbca2cb0e620db7cdb7b93945bef8985fdfd
source_decision_ids: provenance only
```

## Gate 6 — adapt provider/host details

Resolve target-specific adapters without changing semantic authority:

- branch names and topic naming;
- GitHub/GitLab/other provider API operations;
- protected-branch configuration labels;
- local Git/worktree mechanics;
- persistent file-store choice and namespace;
- lock branch/sentinel representation;
- Executor host/session naming;
- model/effort mapping;
- worker roles and capabilities;
- shell/CLI/API recipes;
- CI/build/test commands;
- target file paths.

Volatile vendor behavior must be revalidated on the actual target surface.

## Gate 7 — materialize on a protected topic branch

For target changes:

```text
refresh canonical integration base
-> create target topic branch from exact base
-> verify branch/base
-> materialize complete target-native candidate
-> publish bounded checkpoint
-> verify complete delta
```

Never write the adoption directly to a protected long-lived branch.

## Gate 8 — technical verification

If target adoption includes executable/config/schema/automation changes, use the target's authorized Executor boundary.

The Executor:

- loads the exact persisted target contract/candidate from canonical target Git;
- maintains one coordinator root per work unit;
- delegates materially separable execution/diagnostic slices when safe;
- runs required tests/lint/build/evals/provider checks;
- repairs only defects inside approved target semantics/design;
- blocks and returns upstream semantic/design/acceptance defects;
- persists final handoff/evidence.

Orchestrator-owned text-only policy extraction does not require an Executor merely for ceremony, but target-native validation must still be proportionate.

## Gate 9 — convergence and integration

The Orchestrator verifies:

- completeness;
- correctness of evidence;
- coherence across target policy/design/implementation/evidence;
- containment/no unauthorized scope;
- persistence of accepted target current truth.

Then merge through the protected target PR/MR path and verify the resulting canonical target state.

## Gate 10 — portable workspace reconciliation

If the target adopted persistent snapshots:

- materialize the exact final canonical target state after Executor corrections;
- rebuild/validate replacement snapshot;
- promote only after round-trip validation;
- revalidate promoted current;
- retire merged/superseded snapshots only with positive evidence;
- release locks only with exact ownership proof.

If no persistent store is available or required, record that the protected canonical Git workflow is the active fallback. Do not emulate missing persistence semantics.

## Gate 11 — target independence

Before declaring adoption complete, prove that normal future target maintenance can bootstrap using only target-native state:

- target governing instructions;
- target current checkpoint/frontier;
- target decisions/specifications;
- target task/handoff/runbook carriers;
- target provider protection state;
- target workspace/lock receipts if used.

The source bundle may remain as provenance, but the target must not require live reads from `ManuelBouza/agent-governance` to operate.

## Gate 12 — closure

Update the target's durable frontier and generate the next objective bootstrap according to the adopted target lifecycle.

Any material mismatch during successor bootstrap must fail closed with expected/observed/source/blocker evidence rather than silent repair.
