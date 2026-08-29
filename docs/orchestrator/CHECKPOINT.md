# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O180  
Canonical-Branch: `develop`  
Current-Work-Unit: T046/MG1-v7 stimulus-isolated evaluation revision ready for integration; no live v7 execution yet  
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
- V6 Stage R used 167 valid observations. B0/B1 both failed qualification; Stage C was correctly not executed.
- V6 remains immutable and its observations are diagnostic only for future design; none may enter v7 scoring.

## V6 post-close confound analysis

`docs/research/MG1-V6-CONFOUND-ANALYSIS.md` records two material measurement confounds discovered from closed v6 traces:

1. model-visible evaluation prose itself repeatedly named Agent Governance/Agent Skills/activation/routing and induced candidate inspection in negative cases; `HN01--B0--r1` explicitly consulted the Skill because the turn was an activation evaluation;
2. disposable workspaces were nested beneath the canonical `agent-governance` checkout, allowing ambiguous cases such as `HA03--B1--r1` to infer canonical source identity from host/environment context not supplied by the corpus prompt.

Therefore the next Specify revision isolates the method before changing candidate presentation semantics. This refines O179's provisional expectation of immediate presentation redesign: presentation v3 remains frozen for v7 so the confounds can be tested independently.

## T046 / MG1-v7 proposed authority

```text
Task: T046
Status: ORCHESTRATOR-CONFORMANCE / READY_FOR_INTEGRATION
Task Contract: docs/tasks/T046-mg1-v7-stimulus-isolated-evaluation.md
Research: docs/research/MG1-V6-CONFOUND-ANALYSIS.md
Oracle: MG1-T023-TOPOLOGY-ORACLE-v7
Execution epoch: MG1-T023-EXECUTION-v7
Capability source epoch: MG1-2026-08-25-v3
Presentation revision: MG1-T023-PRESENTATIONS-v3 (UNCHANGED)
Corpus: MG1-T023-CORPUS-v3 (fresh 40 prompts)
Trial envelope: MG1-T023-TRIAL-ENVELOPE-v2
```

V7 method changes:

- exact model-visible turn = fresh corpus prompt + blank line + `Return only the required structured record.`;
- no domain-bearing evaluator wrapper;
- read-only/safety enforcement out of band;
- fresh OS-temporary workspace outside and not linked to canonical source checkout;
- controlled per-case `fixture_role` = neutral/source/consumer;
- ambiguous/negative/near-miss cases always neutral;
- scored activation comes from host-observable candidate `SKILL.md` body read/use; metadata discovery and model self-report alone do not count;
- fresh 40-case holdout with unchanged semantic class counts;
- B0/B1/F2/G3 presentation/reference bytes unchanged.

Preserved from v6:

- paired 2+1 case scoring;
- Stage R B0/B1 first: 160–240 valid observations;
- Stage C F2/G3 only if a reference exists;
- all numeric qualification thresholds and D050 selection percentages;
- zero-tolerance cross-profile/ambiguous safety boundaries;
- capacity-aware pause/resume, 600-second timeout, fresh thread/workspace and two non-capacity attempts;
- required live cell Codex / native Windows / GPT-5.6 Sol / Medium.

## Next action

1. Review the full `spec/t046-mg1-v7-stimulus-isolated-eval` diff against canonical `develop@a8e289faf9fafb659087c2851b22bcbdae68caa0`.
2. Confirm only Orchestrator Markdown plus authorized D052 corpus/oracle/envelope assets changed; confirm presentation/topology/reference bytes did not change.
3. Integrate T046/MG1-v7 through PR.
4. Refresh canonical `develop` and checkpoint v7 as `INTEGRATED / CONTROLLING`.
5. Only then show D055 and relaunch T023 from fresh canonical develop.
6. Executor mechanically implements the frozen neutral-envelope, neutral-workspace, fixture and host-observable activation method; it must not change presentation bytes or acceptance semantics.
7. Orchestrator independently reviews v7 evidence. If no reference still exists, only then re-enter Specify for presentation/topology redesign.

## Next chat minimum load

Load only current `develop` identity, `AGENTS.md`, and this checkpoint; then follow `Next action`.

## Do not

Do not relaunch v6; do not import any prior observation into v7 score; do not change B0/B1/F2/G3 presentation/reference bytes in v7; do not append domain-bearing evaluator prose; do not run neutral/ambiguous/negative trials inside or beneath the canonical source checkout; do not treat metadata discovery or model self-report alone as scored activation; do not weaken thresholds/selection rules; do not write directly to `main`/`develop`.
