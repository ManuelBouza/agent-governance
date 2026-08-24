# T040 — T038/T039 Convergence Sequencing Correction

## Identity

- Task ID: `T040`
- Status: `PLANNED`
- Type: `orchestrator-convergence`
- Base branch: `develop`
- Planning branch: `docs/o162-t040-convergence-sequencing`
- SDD-Profile: `STANDARD`
- Assurance-Class: `protocol-migration, convergence, verification-order`
- Verification-Planes: `deterministic, static, portability`
- Release-Impact: `removes a circular acceptance dependency between T038 and T039 without changing either product or oracle semantics`

## Objective

Correct the convergence order between T038 and T039 after independent T039 verification proved that the current persisted sequence is impossible to satisfy.

T039's oracle revision is already integrated into canonical `develop`, but canonical `develop` remains red until the separately implemented T038 Consumer asset repair is present. Requiring T039 full-suite acceptance before T038 can be re-verified therefore creates a circular dependency:

```text
T039 acceptance requires green canonical baseline
        -> green canonical baseline requires T038
        -> current checkpoint forbids T038 before T039 acceptance
```

T040 changes only sequencing/acceptance authority. It does not alter T038 implementation semantics, T039 oracle semantics, Core, runtime, templates, CLI behavior, T021, or T022.

## Trigger / evidence

Independent T039 verification at submitted HEAD `0197e1899cb0933c7345b373a5dfdbd015d078fc` used canonical base `develop@43641a0646baf5866c1cd0b58aa237d74f172e42` and made no implementation changes.

The T039 handoff reports:

- T039 oracle review itself is sound and narrow;
- focused T034 verification still fails during bootstrap because canonical source templates remain at pre-T038 protocol identity;
- the full suite is red for the same canonical T038 blocker;
- no runtime/template/Core/T038/T021/T022 change was made;
- T039 cannot converge until T038 is present.

The T038 submitted implementation at anchor `8aa32b32fb15e01bfbc56e327a910b82b3674c32` previously demonstrated its authorized focused surface green and was blocked only by the stale T034 live-current-version oracle that T039 has now corrected in canonical `develop`.

## Controlling references

- `AGENTS.md`
- `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md`
- `docs/decisions/D052-specification-owned-conformance-test-authorship.md`
- `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md`
- `handoffs/T038-executor-handoff.json`
- `docs/tasks/T039-t034-protocol-history-oracle-transition.md`
- `handoffs/T039-executor-handoff.json`
- `docs/orchestrator/CHECKPOINT.md`

## Requirement / specification delta

### MODIFIED — sequencing only

- **R-T040-1 — T039 integration precedes T038 acceptance**: the T039 oracle revision must be present in canonical `develop` before T038 terminal re-verification. This condition is already satisfied by `develop@43641a0646baf5866c1cd0b58aa237d74f172e42`.
- **R-T040-2 — T038 acceptance may precede T039 acceptance**: T038 does not require T039 to be formally `ACCEPTED`; it requires the T039 oracle revision to be integrated and controlling. T038 may therefore be reconciled/re-verified against current `develop` containing T039 and, if fully green, accepted and integrated.
- **R-T040-3 — T039 final acceptance follows T038 integration**: after T038 is accepted/integrated, T039 must receive a fresh independent verification from then-current canonical `develop`; only that post-T038 verification may satisfy T039's canonical full-suite gate.
- **R-T040-4 — T039 AC-T039-5 sequencing correction**: the phrase `canonical baseline green before T038 integration` is superseded. The intended requirement is `canonical baseline green after T038 acceptance/integration and before T039 final acceptance`.
- **R-T040-5 — no repeated impossible T039 launch**: the blocked T039 handoff at `0197e189...` is valid evidence of the circular baseline condition and must not be repeated until T038 has been accepted/integrated.

### PRESERVED

- **R-T040-P1** — T038 implementation semantics and authorized file scope remain exactly those in the T038 Task Contract.
- **R-T040-P2** — T039 oracle semantic revision remains exactly `T039-T034-PROTOCOL-HISTORY-TRANSITION-v1`; no other T034 oracle assertion changes.
- **R-T040-P3** — T038 represented history must be preserved; no force-push/recreation/discard of represented work.
- **R-T040-P4** — T039 verification remains read-only except its handoff JSON.
- **R-T040-P5** — T021 remains blocked until T038 acceptance; T022 remains blocked until T021 acceptance.
- **R-T040-P6** — no direct writes to `develop`/`main`.

## Corrected convergence sequence

```text
T039 oracle revision integrated in develop  [DONE]
        -> T038 represented branch re-enters from fresh current develop
        -> reconcile T039 into T038 history without discarding represented work
        -> run complete T038 verification matrix
        -> if green: Orchestrator reviews, accepts and integrates T038
        -> fresh T039 read-only verification from new canonical develop
        -> if focused/full verification green: accept T039
        -> resume T021-R1 on its represented branch
```

## T038 re-entry boundary

The next Executor action is T038, not T039.

The Executor must:

1. bootstrap from current canonical remote `develop` under D042/RB001;
2. verify the represented remote branch `fix/t038-protocol-derived-consumer-assets` and preserve its existing history;
3. reconcile current `develop` containing T039 into that represented branch without force-push/history rewrite;
4. make no semantic redesign unless the unchanged T038 Task Contract independently requires it;
5. run the complete T038 verification matrix including full locked pytest, Ruff check/format and `git diff --check`;
6. persist and push a new terminal T038 handoff/head under D048;
7. return only canonical completion fields.

If verification reveals a new independent defect after T039 is present, T038 stops for normal re-entry rather than expanding scope.

## T039 final-verification boundary

Do not relaunch T039 immediately after T040 integration.

T039 is relaunched only after T038 is accepted/integrated. That verification must start from fresh canonical `develop`, perform no product changes, and prove:

- focused T034 oracle green;
- complete locked pytest green;
- Ruff check/format green;
- `git diff --check` green;
- no T034 semantic drift beyond the already integrated T039 temporal correction.

## Acceptance criteria

### AC-T040-1 — circular dependency removed

The checkpoint and controlling authority no longer require T039 acceptance before T038 can be re-verified/accepted.

### AC-T040-2 — oracle-before-product ordering preserved

The T039 oracle revision remains integrated before any accepted T038 product integration.

### AC-T040-3 — final green baseline still mandatory

Neither T038 nor T039 may be finally accepted on a red relevant verification state. T038 must be green on its reconciled candidate; T039 must be green on canonical `develop` after T038 integration.

### AC-T040-4 — no semantic widening

No T038 product semantics, T039 oracle semantics, Core identity, CLI surface, T021/T022 work, or other program scope is changed by T040.

## Next action

After T040 planning/checkpoint integration, launch T038 from fresh canonical `develop` using pointer-only transport to `docs/tasks/T038-protocol-derived-consumer-asset-versioning.md`.

Do not launch T039 again until T038 is accepted/integrated.
