# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O181  
Canonical-Branch: `develop`  
Current-Work-Unit: T046/MG1-v7 stimulus-isolated evaluation is integrated and controlling; T023 is ready for a fresh v7 acceptance epoch  
Chat-Closure: CONTINUE_CURRENT_CHAT  
Active-Executor: none  
Active-Executor-Surface: ChatGPT Orchestrator

## Durable frontier

- D053, D054, D040, D042, D048, D050, D051, D052, D055 and D056 remain controlling. Core protocol remains `1.15.0`.
- T021 and T022 are `ACCEPTED`.
- T023 v2: closed `BLOCKED / EXPERIMENT CLOSED`; review `docs/reviews/T023-R1.md`.
- T023 v3: closed `BLOCKED / EXECUTION-INCOMPLETE`; review `docs/reviews/T023-R2.md`.
- T023 v4: closed `BLOCKED / EXTERNAL CAPACITY`; review `docs/reviews/T023-R3.md`.
- T023 v5: `SUPERSEDED_PRE_EXECUTION`; review `docs/reviews/T023-R4.md`.
- T023 v6: closed `BLOCKED / NO QUALIFYING SINGLE-FAMILY REFERENCE / EXPERIMENT CLOSED`; review `docs/reviews/T023-R5.md`.
- V6 submitted HEAD `6fae8c8d7b15979895cf951b87e9145368e86daf`; evidence PR `#240`, merge `15aa0831dd10faa8736ec219f1b847c600f71167`.
- V6 observations remain diagnostic only and MUST NOT enter v7 scoring.
- Post-close analysis `docs/research/MG1-V6-CONFOUND-ANALYSIS.md` identified evaluator-prose activation induction and canonical-source workspace-path leakage as method confounds requiring prospective isolation before candidate presentation redesign.
- T046/MG1-v7 is integrated by PR `#242`, merge `c553cafaa9867e9e2cfaf27f954406d926795930`.

## T046 / MG1-v7 controlling identity

```text
Task: T046
Status: INTEGRATED / CONTROLLING
Task Contract: docs/tasks/T046-mg1-v7-stimulus-isolated-evaluation.md
Research: docs/research/MG1-V6-CONFOUND-ANALYSIS.md
Integration PR: #242
Integration merge: c553cafaa9867e9e2cfaf27f954406d926795930
Oracle: MG1-T023-TOPOLOGY-ORACLE-v7
Execution epoch: MG1-T023-EXECUTION-v7
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3
Corpus: MG1-T023-CORPUS-v3
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
```

V7 preserves B0/B1/F2/G3 presentation and reference bytes from v6. It changes only the prospective holdout/evaluation method required to remove identified measurement confounds.

## V7 execution invariants

- The model-visible natural-language turn is exactly the fresh corpus prompt, two newlines, and `Return only the required structured record.`
- No added domain-bearing evaluator prose may name Agent Governance, candidate/profile/capability identities, Agent Skills, activation/routing evaluation, Consumer or source-maintainer semantics.
- Read-only and safety enforcement are host-side/out-of-band.
- Every attempt uses a fresh OS-temporary disposable workspace outside and not linked to the canonical source checkout; the neutral root must satisfy the forbidden-substring/path-leak rules in `trial-envelope.json`.
- Every case materializes only its frozen `fixture_role`: `neutral`, `source`, or `consumer`. Ambiguous, generic-negative and near-miss cases are neutral.
- Scored `activated_entrypoints` comes from host-observable successful candidate `SKILL.md` body read/use after discovery. Metadata discovery and model self-report alone are not scored activation.
- If the required host cell cannot distinguish metadata discovery from candidate-body activation reproducibly, stop `BLOCKED` before acceptance scoring.
- Paired 2+1 case scoring remains controlling: two mandatory valid repetitions, one conditional third on frozen-field/context disagreement, no fourth valid repetition.
- Stage R evaluates B0/B1 first: 160–240 valid observations. If neither qualifies, stop `BLOCKED` and do not execute F2/G3.
- Stage C evaluates F2/G3 only when a single-family reference exists: another 160–240 valid observations.
- Numeric thresholds, mandatory zero-tolerance safety gates, D050 selection percentages/tie-breaks and `observed_context_bytes` selection meaning remain unchanged.
- Explicit usage-limit/quota events remain non-attempt capacity pauses. Each scheduled repetition retains a 600-second timeout, fresh thread/workspace and at most two non-capacity model attempts.
- Same-epoch v7 resume preserves already valid v7 observations after exact identity/integrity verification.

## T023 next executable identity

```text
Task: T023
Status: READY / FRESH V7 EPOCH
Task Contract: docs/tasks/T023-unified-skill-profile-activation-evals.md
Controlling revision: docs/tasks/T046-mg1-v7-stimulus-isolated-evaluation.md
Expected handoff: handoffs/T023-executor-handoff.json
Required live cell: Codex / native Windows / GPT-5.6 Sol / Medium
Prior v2/v3/v4/v6 observations allowed in v7 score: 0
Prior v5 live observations: 0
```

No v7 live acceptance call has occurred yet.

## Next action

1. Integrate this O181 checkpoint branch through PR and refresh canonical `develop`.
2. Show D055 for T023: Codex `NEW`, GPT-5.6 Sol, High.
3. Relaunch T023 from fresh canonical `develop` using only the pointer to `docs/tasks/T023-unified-skill-profile-activation-evals.md` plus D042 freshness.
4. Executor mechanically implements the frozen v7 neutral-envelope, neutral-workspace, fixture and host-observable activation method and performs Code Review & Verify; it MUST NOT change candidate presentation/reference bytes or Orchestrator-owned acceptance semantics.
5. Orchestrator independently reviews the submitted v7 evidence and applies the frozen selection rule.
6. If v7 again yields no qualifying B0/B1 reference after confound removal, re-enter Specify for candidate presentation/topology redesign. Do not tune candidates during the v7 epoch.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not relaunch v6; do not import prior observations into v7 score; do not change B0/B1/F2/G3 presentation/reference bytes during v7; do not append domain-bearing evaluator prose; do not run neutral/ambiguous/negative trials inside or beneath the canonical source checkout; do not treat metadata discovery or model self-report alone as scored activation; do not execute F2/G3 if Stage R yields no qualifying reference; do not weaken thresholds or selection rules; do not write directly to `main`/`develop`.
