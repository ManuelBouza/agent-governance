# L003 — T020 DONE required acceptance rework

Learning ID: L003  
State: CONTROL_PLANNED  
Fingerprint: `task.done_requires_rework`

## Detection

Detected during Orchestrator review of T020 executor HEAD `a50b4bbb572c44e0715fda2b49955f36bbf043d2` after the executor reported `STATUS: DONE`.

T020-R1 recorded two bounded acceptance/verification gaps:

1. the artifact builder copied the complete `governance-skill/` source subtree and included source-product lifecycle/status `STATUS.md` in the Consumer distribution payload; and
2. artifact-only verification executed `bootstrap`, `validate`, and `state`, but used `--help` command enumeration instead of executing representative valid `event`, `skill`, `ecosystem`, and `archive` operations.

The defective candidate was not integrated. T020-R2 later accepted the corrected candidate and PR #127 integrated it into `develop`.

## Factual evidence

- Task Contract: `docs/tasks/T020-self-contained-build-artifact-and-identity.md`.
- Reviewed defective HEAD: `a50b4bbb572c44e0715fda2b49955f36bbf043d2`.
- Durable rework review: `docs/reviews/T020-R1.md`.
- Durable acceptance review: `docs/reviews/T020-R2.md`.
- Corrected accepted executor HEAD: `0aad8ce78b52a4bd2a4851663d675048215a539c`.
- Implementation PR: #127.
- Final executor handoff: `handoffs/T020-executor-handoff.json`.

## Immediate control integrated in T020

T020 itself now contains regression controls for the two concrete defects:

- positive Consumer artifact payload selection with source-only `STATUS.md` excluded; and
- direct artifact-only execution evidence for all seven Consumer v1 commands after source deletion.

These controls contain the observed T020 failure but do not by themselves close the broader systemic assurance gap.

## Causal/systemic analysis

Two reusable gaps were identified:

1. **distribution-boundary gap** — broad source-subtree selection can leak source-only/lifecycle material into distribution;
2. **acceptance-evidence traceability gap** — a `DONE` handoff can contain green tests while overstating which acceptance criterion those tests directly prove.

Contributing conditions included semantic rather than machine-explicit package boundaries, absence of acceptance-criterion-to-evidence mapping, and no structured evidence-type distinction between command visibility and successful execution.

These are system/process gaps, not agent-product or individual blame.

## Recurrence before control verification — T030-R1

T030 produced a second `task.done_requires_rework` occurrence before this systemic control reached `VERIFIED`.

The T030 executor handoff did use the new ICAE criterion-to-evidence structure: `AC-CTX-1` through `AC-CTX-5` were individually mapped to evidence types and exact tests. During Orchestrator review, however, `AC-CTX-1` was still found insufficiently proven: the canonical baseline embeds `git rev-parse HEAD`, but its repeated-run tests held `HEAD` fixed and did not exercise the final commit transition that persisted the baseline/handoff. The submitted baseline therefore recorded its implementation parent rather than the submitted final HEAD and would change on regeneration after finalization.

Canonical review: `docs/reviews/T030-R1.md`.

Under D039 this is a priority/escalation signal, **not** `CONTROL_FAILURE`, because L003 has not yet reached `VERIFIED`.

The recurrence refines the control model:

- criterion/evidence mapping materially improves auditability and defect localization;
- deterministic validation can check that mappings exist and reference recorded evidence;
- mapping presence and evidence-type labels cannot establish semantic sufficiency by themselves;
- Orchestrator review must still determine whether the cited test/evidence actually proves the full criterion boundary;
- reproducibility criteria involving commit identity must include the relevant finalization/identity transition in their regression evidence when that transition can change canonical output.

Do not introduce an LLM or heuristic proxy that claims to decide semantic evidence sufficiency automatically.

## Selected systemic control

D046/ICAE selects the prospective control direction:

- material acceptance criteria use stable identifiers when ambiguity is plausible;
- executor handoffs/reviews map each material criterion to exact supporting verification evidence;
- evidence type is explicit where weaker evidence could be mistaken for a stronger claim (`surface-present` vs `executed-successfully`, package/isolation, negative-control, reproducibility, etc.);
- package/distribution work uses positive boundaries/allowlists or an equivalent explicit boundary where broad copying could leak source-only material;
- deterministic validation should eventually expose missing/malformed required evidence mappings without pretending to judge semantic adequacy that belongs to Orchestrator review;
- live review/EGLL integration should emit `task.done_requires_rework` when a durable post-`DONE` review is `REWORK_REQUIRED`.

T021 and T030 apply criterion/evidence traceability prospectively in their contracts. T030-R1 demonstrates both the value and the limit of that structure. This is policy adoption/evidence, not completion of the systemic control.

## Verification / recurrence status

L003 is `CONTROL_PLANNED`, not `VERIFIED`.

`VERIFIED` requires the selected systemic control to be implemented and, for automatically detectable parts, replay evidence showing both:

1. a representative bad state produces the expected failure/fingerprint; and
2. a compliant state does not.

If the same failure class recurs after the systemic control reaches `VERIFIED`, evaluate the recurrence as potential `CONTROL_FAILURE` under D039.
