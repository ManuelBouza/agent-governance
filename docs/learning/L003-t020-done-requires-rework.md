# L003 — T020 DONE required acceptance rework

Learning ID: L003  
State: ANALYZED  
Fingerprint: `task.done_requires_rework`

## Detection

Detected during Orchestrator review of T020 executor HEAD `a50b4bbb572c44e0715fda2b49955f36bbf043d2` after the executor reported `STATUS: DONE`.

T020-R1 records two bounded acceptance/verification gaps:

1. the artifact builder copied the complete `governance-skill/` source subtree and therefore included source-product lifecycle/status metadata `STATUS.md` in the Consumer distribution payload; and
2. artifact-only verification executed `bootstrap`, `validate`, and `state`, but treated `--help` command enumeration as evidence for `event`, `skill`, `ecosystem`, and `archive` instead of executing representative valid operations from the isolated artifact.

The implementation was not integrated into `develop` before detection.

## Factual evidence

- Task Contract: `docs/tasks/T020-self-contained-build-artifact-and-identity.md`.
- Reviewed executor HEAD: `a50b4bbb572c44e0715fda2b49955f36bbf043d2`.
- Reviewed implementation commit: `9ba7c83595488e917ecfd9c6d53ae9cd4776d5ed`.
- Durable review: `docs/reviews/T020-R1.md`.
- Reviewed build implementation: `src/agent_governance/artifact.py` on the T020 branch.
- Reviewed isolation coverage: `tests/test_governance_artifact.py` on the T020 branch.
- Executor handoff: `handoffs/T020-executor-handoff.json` on the T020 branch.

## Immediate containment

T020 remains unaccepted and unintegrated.

T020-R1 authorizes only bounded correction of the packaging boundary and direct artifact-only execution evidence for all seven Consumer v1 commands. The existing T018/T019 baseline, T020 task scope, protocol semantics, Consumer behavior and Markdown ownership remain frozen.

The exact corrected tests required by T020-R1 become regression controls for these concrete failure modes.

## Causal/systemic analysis

### Observed facts

The handoff reported T020 `DONE` and summarized artifact-only operation coverage at a broader semantic level than the actual focused test demonstrated. Separately, the builder selected its Consumer distribution payload by copying an entire source subtree rather than by an explicit distribution allowlist/boundary.

### Contributing conditions

- The Task Contract defined the desired artifact boundary semantically but did not enumerate a machine-checkable Consumer payload allowlist.
- The handoff format records commands/results but does not require an explicit acceptance-criterion-to-evidence mapping.
- A parser/command-surface check could be summarized as if it were equivalent to successful command execution because the evidence taxonomy is not structurally encoded.
- T008's EGLL MVP can represent `task.done_requires_rework` once a normalized review outcome is supplied, but it is not wired into the live Task review/handoff path.

### Systemic gaps

Two reusable gaps are present:

1. **distribution-boundary gap** — packaging work can accidentally include source-only/lifecycle material when builders copy source subtrees rather than selecting the intended distributable payload;
2. **acceptance-evidence traceability gap** — a `DONE` handoff can contain green tests yet still overstate which acceptance criterion those tests directly prove.

These are process/assurance gaps, not agent-product or individual blame.

## Control decision boundary

Do not expand T020 retroactively beyond T020-R1. The immediate exact controls belong inside the existing T020 scope:

- explicit Consumer artifact payload selection with regression proof that `STATUS.md` is excluded; and
- representative artifact-only execution for all seven Consumer v1 commands after source removal.

Broader systemic controls require separate persisted design/Task authority after T020 is accepted. They should be coordinated with the planned ICAE methodology gate rather than smuggled into T020.

The future control should evaluate at least:

- stable acceptance-criterion identifiers in Task Contracts where useful;
- an explicit handoff/review evidence map from each material acceptance criterion to the exact verifier/test/eval that proves it;
- evidence-type distinction such as `surface-present`, `executed-successfully`, `negative-control`, `reproducibility`, and `review-only` so weaker evidence cannot silently satisfy a stronger claim;
- package/distribution tasks declaring a distributable allowlist or equivalent positive boundary when broad subtree copying could leak source-only material;
- deterministic validation that required evidence-map entries exist and reference actual recorded verification output;
- EGLL integration that automatically emits `task.done_requires_rework` when a durable review disposition is `REWORK_REQUIRED` after executor `DONE`.

Automation must not pretend to judge semantic adequacy that still requires Orchestrator review. It should make missing/overbroad evidence claims mechanically visible, while acceptance authority remains with Governance.

## Verification / recurrence status

L003 is `ANALYZED`, not `VERIFIED`.

The concrete T020 regression controls are not yet accepted/integrated, and the broader acceptance-evidence/EGLL integration control has not yet been contracted.

If the same `task.done_requires_rework` class recurs after a future systemic control reaches `VERIFIED`, recurrence must be evaluated under D039 as potential `CONTROL_FAILURE`.
