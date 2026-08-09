# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O004  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001 has completed its first executor pass and returned `PARTIAL`. The implementation is largely complete and verified, but PD5 review found one procedural noncompliance, two focused technical rework items, and one defect in the executor-handoff SHA contract that is being corrected before rework continues.

## Completed

- Source-product foundation decisions D022-D028 remain accepted.
- T001 executor branch exists remotely: `test/governance-harness`.
- First visible executor HEAD reviewed: `a31b87f32b8004347e58521b01e3de4a7e55570b`.
- Reviewed implementation anchor: `e89e60cf1edd97975565870013229b1949f499f8`.
- First handoff reports 61 pytest tests passing plus Ruff/locked verification, but status is `PARTIAL`.
- PD5 review identified:
  - unauthorized workstation `uv self update 0.11.33` after discovering an out-of-range uv;
  - overly broad `.gitignore` boilerplate outside T001 scope;
  - reference-integrity logic that incorrectly skips all dot-prefixed paths;
  - an impossible self-referential handoff requirement requiring a JSON file to embed the SHA of the commit containing itself.
- D029 defines a non-self-referential executor handoff identity model.
- `docs/reviews/T001-R1.md` contains the durable first rework directive.

## Controlling References

For the immediate next action:

- `AGENTS.md`
- `docs/tasks/T001-deterministic-test-harness-foundation.md`
- `docs/reviews/T001-R1.md`
- `docs/EXECUTOR-HANDOFFS.md`
- `docs/decisions/D029-non-self-referential-executor-handoff-identity.md`

Do not reload the earlier decision history unless a concrete conflict requires it.

## Active Remote Artifacts

- Executor branch: `test/governance-harness`
- Current reviewed executor HEAD: `a31b87f32b8004347e58521b01e3de4a7e55570b`
- Persisted handoff: `handoffs/T001-executor-handoff.json`
- Review directive: `docs/reviews/T001-R1.md`
- T001 remains under active PD5 review/rework and is not accepted or merged.

## Open Questions or Blockers

No architecture decision blocker remains once D029/review R1 is integrated into `develop`.

The original `uv self update` remains a recorded procedural noncompliance. R1 does not retroactively authorize it; it permits remediation on the now-compliant workstation without requiring a second clean workstation.

## Next Action

1. Integrate the D029 + T001 R1 review-policy change into `develop`.
2. Ask the Agente de IA Ejecutor to fetch current `develop`, read `docs/reviews/T001-R1.md` and the revised handoff policy, and apply only the R1 rework on `test/governance-harness`.
3. Executor reruns the canonical locked verification, updates the handoff using `implementation_head_sha`, commits/pushes, and returns the minimal four-line pointer.
4. ChatGPT performs PD5 review again before any PR is opened.

Do not open or merge the T001 implementation PR yet.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T001-deterministic-test-harness-foundation.md`;
2. `docs/reviews/T001-R1.md`;
3. `docs/EXECUTOR-HANDOFFS.md`.

Load D029 directly only if the handoff identity rationale is needed.

## Do Not Load or Do

- Do not accept T001 from green tests alone.
- Do not erase or relabel the unauthorized workstation uv update as originally permitted.
- Do not require the handoff JSON to contain the SHA of its own containing commit.
- Do not open/merge the T001 PR before R1 rework is reviewed.
- Do not implement T001 rework as ChatGPT; non-Markdown rework belongs to the Agente de IA Ejecutor.
