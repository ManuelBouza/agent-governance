# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O016  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001 and T002 are `ACCEPTED` and integrated.

D032 is `ACCEPTED` and integrated, but its dedicated verification is incomplete. During post-T002 planning ChatGPT found a concrete deterministic regression caused by D032-era protocol evolution: `governance-core/GOVERNANCE.md` is now protocol `1.10.0`, while `tests/_helpers.py` still declares `SOURCE_PROTOCOL_VERSION = "1.9.0"`; the helper's `CORE_REQUIRED_MODULES` also omits new Core modules `INTERACTION.md` and `QUALITY.md`.

The next planned work unit is T003 — D032 deterministic policy-contract foundation — persisted on Markdown branch `docs/t003-d032-deterministic-contract` at `docs/tasks/T003-d032-deterministic-policy-contract.md`.

T003 is not an agent-behavior eval. It restores deterministic harness alignment and encodes only D032 properties that can be verified mechanically without model interpretation.

## Completed

- T001 remains `ACCEPTED` and integrated.
- T002 PD5 R2 remains `ACCEPTED` and integrated.
- T002 implementation merge: `7ef62bbea5b3d0030bcc715d4b973538114c746e`.
- Post-T002 checkpoint merge: `bcf7899b01a1fb668c16a95ef6d83c053f398277`.
- D030 remains controlling for clone-local Gentle-AI RDD opt-out.
- D031 remains controlling for normal local Gentle-AI Skill Registry `.atl/` coexistence.
- D032 remains controlling for the Human-intent ↔ engineering proxy, invariant engineering quality, implicit quality envelope and Primary Solution Diagram readiness.
- D032 architecture overview: `docs/ARCHITECTURE-INTENT-ENGINEERING-PROXY.md`.
- Current D032 Core modules: `governance-core/INTERACTION.md` and `governance-core/QUALITY.md`.

## T003 Planning Decision

`docs/TESTING-AND-EVALUATION.md` requires the least probabilistic verifier that can correctly prove a property.

The D032 verification frontier is therefore decomposed:

1. **T003 deterministic policy-contract foundation** — current planned task;
2. **future agent-facing D032 eval increment** — only after T003, for actual model interpretation/interaction behavior.

This avoids using model-based evals to prove mechanical properties and avoids overclaiming that a fixture classifier demonstrates real LLM behavior.

## T003 Primary Solution Diagram

Dominant design question: local verification workflow/dependency change.

```text
D032 Core (read-only)
INTERACTION + QUALITY + LIFECYCLE
              │
              ▼
     Synthetic D032 cases (JSON)
     ┌────────┼─────────┬──────────┐
     │        │         │          │
 register   quality   diagram    refresh
 variants   routing   selection   invalidation
     │        │         │          │
     └────────┴────┬────┴──────────┘
                   ▼
        Deterministic test-local model
                   │
      ┌────────────┼──────────────┐
      ▼            ▼              ▼
 engineering   material-only   correct diagram/
 invariance     disclosure      stale-on-change
      │            │              │
      └────────────┴──────┬───────┘
                          ▼
       protocol/module drift checks
       1.10.0 + INTERACTION + QUALITY
                          │
                          ▼
              canonical locked gate
              pytest + Ruff + no network
```

The diagram is persisted in T003 and is the current D032 graphical-readiness evidence for this implementation scope.

## T003 Scope Summary

Expected executor branch:

`test/d032-deterministic-contract`

Expected handoff:

`handoffs/T003-executor-handoff.json`

Expected non-Markdown surfaces include only the smallest needed subset of:

- `tests/_helpers.py`;
- `tests/fixtures/d032/` non-Markdown fixture data;
- one focused D032 deterministic Python test module;
- small existing Python test alignment only when necessary;
- T003 handoff JSON.

No new dependency, production runtime policy engine, LLM call, agent session, transcript grader, Hypothesis layer, external SDD runtime or executor-authored Markdown is authorized.

## Known Pre-Mutation Regression

Current source bytes imply that the exact protocol-version test is stale/failing:

- canonical Core: `Protocol-Version: 1.10.0`;
- deterministic helper expectation: `SOURCE_PROTOCOL_VERSION = "1.9.0"`.

T003 requires the executor to characterize this mismatch before mutation. If current `develop` unexpectedly no longer exhibits it, the executor must stop `PARTIAL` rather than rewriting the premise.

T003 must align the harness forward to 1.10.0 and mechanically require `INTERACTION.md`/`QUALITY.md`; it must not downgrade Core or weaken exact assertions.

## D032 Deterministic Properties Planned for T003

- equivalent plain/technical/code-native fixture variants preserve an explicit engineering fingerprint, controls and acceptance facts;
- code-native fixtures preserve supplied identifiers/tokens mechanically;
- quality routing covers `BASELINE|MATERIAL|NOT_APPLICABLE`, material contract controls, Human-visible materiality, mandatory security triage and privacy independence;
- all eight D032 Primary Solution Diagram mapping families are covered from explicit dominant-question facts;
- none/cosmetic/material design changes map correctly to diagram-refresh requirements;
- test-local routing/classification never branches on product/user labels;
- no model behavior is claimed by this deterministic layer.

## Quality-Envelope Result for T003

Material dimensions:

- functional correctness / acceptance fidelity;
- verification;
- maintainability/change isolation;
- compatibility with accepted T001/T002 regression coverage.

Security is explicitly triaged as baseline because T003 introduces no trust boundary, secrets, untrusted executable content, network/public surface or production state. Privacy and end-user accessibility are not applicable to the synthetic local test assets. No additional threat model/DFD is required.

## Active Remote Artifacts

- canonical `develop`: `bcf7899b01a1fb668c16a95ef6d83c053f398277` at T003 planning start;
- T003 Markdown planning branch: `docs/t003-d032-deterministic-contract`;
- T003 Task Contract: `docs/tasks/T003-d032-deterministic-policy-contract.md`;
- D032 decision: `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`;
- D032 overview: `docs/ARCHITECTURE-INTENT-ENGINEERING-PROXY.md`.

## Orchestrator Branching Incidents

Two prior accidental direct Markdown writes remain audit history and are not policy-compliant precedent:

1. T002-R1 placeholder: `6a3bff4f12850bd701fea624815e955231082afa`, corrected by `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
2. Architecture-overview placeholder: `a0e063344043fda53f55b8fcb5b03742a33a7185`, corrected by `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.

T003 planning correctly created its topic branch before any Markdown contents mutation.

## Open Questions or Blockers

No architecture blocker is currently known for T003.

The source product is not stable/release-ready. After T003, model-dependent D032 behavior still needs agent-facing eval coverage, and other release gates in `docs/TESTING-AND-EVALUATION.md` remain incomplete.

## Next Action

1. Review `docs/t003-d032-deterministic-contract` against current `develop`.
2. Confirm the diff contains only `docs/tasks/T003-d032-deterministic-policy-contract.md` and this checkpoint update.
3. Merge the Markdown planning PR into `develop` if clean.
4. Verify resulting `develop` HEAD and T003 `READY` contract.
5. Launch an executor only after that merge, using the minimal Task Contract pointer.
6. After executor handoff, ChatGPT performs remote PD5 before any implementation PR.
7. If T003 is accepted/integrated, plan a separate agent-facing D032 eval increment; do not merge it into T003 retroactively.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T003-d032-deterministic-policy-contract.md`;
2. `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`;
3. `governance-core/INTERACTION.md`;
4. `governance-core/QUALITY.md`;
5. `docs/TESTING-AND-EVALUATION.md` only when interpreting verifier-layer boundaries.

## Do Not Load or Do

- Do not reopen T001/T002 absent a concrete regression.
- Do not claim current `develop` deterministic suite is green until the D032 protocol-version drift is repaired and verified.
- Do not broaden T003 into model/agent evals, a production policy engine, state-machine testing or new dependencies.
- Do not interpret fixture-level engineering invariance as proof of actual model behavior.
- Do not commit `.atl/` contents or treat Skill registry selection as Governance trust/approval.
- Do not re-enable or globally alter Gentle-AI RDD.
- Do not erase or normalize away recorded direct-write incidents.
- Do not declare the source product stable/release-ready from T003 alone.
