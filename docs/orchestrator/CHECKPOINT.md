# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O146  
Canonical-Branch: `develop`  
Current-Work-Unit: T034-R1 Design/Plan re-entry integrated; resume existing T034 branch  
Chat-Closure: KEEP_CURRENT_CHAT

## Durable frontier

- D053 native SDD remains accepted with single-owner stages.
- D054 Executor-owned execution mechanics and RB001 source bootstrap remain integrated and controlling.
- T035 remains `BLOCKED` until T034 is accepted/integrated on a green canonical baseline and a later T035 oracle gate is frozen.
- T021/T022 remain paused.
- T034 first execution returned terminal `BLOCKED` on the expected branch rather than expanding scope.
- Submitted terminal pointer:
  - branch: `feat/t034-native-sdd-executable-materialization`;
  - HEAD: `83abcafc60c943040fa4aa70f242950220851981`;
  - implementation anchor: `3c85675394f4764f7436bbbb12e75de64a505f68`;
  - handoff: `handoffs/T034-executor-handoff.json`.
- The submitted implementation preserved the frozen oracle and committed no Markdown.
- T034-R1 review is integrated at `docs/reviews/T034-R1.md` with disposition `REWORK_REQUIRED` and authoritative Design/Plan re-entry scope.

## Current remote state

```text
last verified develop              = 332baa9db5c030ffc007a72ac1d0f28225cfabd6
T034 R1 review PR                  = #191 — MERGED
T034 review                        = docs/reviews/T034-R1.md
T034 task                          = docs/tasks/T034-native-sdd-executable-materialization.md
T034 oracle                        = tests/test_t034_native_sdd_conformance.py
T034 oracle revision               = T034-A2-v1 — FROZEN / unchanged
T034 branch                        = feat/t034-native-sdd-executable-materialization
T034 submitted terminal HEAD       = 83abcafc60c943040fa4aa70f242950220851981
T034 implementation anchor         = 3c85675394f4764f7436bbbb12e75de64a505f68
T034 handoff                       = handoffs/T034-executor-handoff.json
T034 branch relation               = ahead 2 / behind 1 vs current develop at last check
T035                               = BLOCKED
T021/T022                          = PAUSED
```

Re-resolve canonical `develop` and the T034 branch immediately before resume. After this checkpoint itself is integrated, the T034 branch will be further behind and must be reconciled without rewriting represented history.

## T034-R1 accepted preservation

Preserve the submitted T034 implementation unless an R1 correction mechanically requires adjustment:

- closed Core inventory now contains `SDD.md` / `SDD-Version`;
- the no-external-SDD corpus/grader semantics use the frozen native fallback vocabulary;
- authorized artifact protocol expectations use `1.14.0`;
- no second SDD runtime/lifecycle, external SDD dependency, task parser/schema, handoff schema or CLI-surface expansion was introduced.

The frozen T034 oracle must remain unchanged.

## T034-R1 required corrections

`docs/reviews/T034-R1.md` is the authoritative revision to the original Task Contract for these exact additions:

1. mechanically change only `protocol_version` to `1.14.0` in:
   - `governance-skill/assets/CAPABILITIES.template.json`;
   - `governance-skill/assets/STATE.template.json`;
2. update `src/agent_governance/artifact.py` only so the existing `governance-skill/assets/RUNBOOK.template.md` participates in the current explicit self-contained artifact allowlist/parity; corresponding mechanical artifact-test expectations are allowed;
3. narrowly correct reference-integrity path/prose classification in `tests/_helpers.py` plus focused regressions in `tests/test_reference_integrity.py` so accepted slash-separated SDD taxonomy is not treated as a path while concrete relative paths, dotfiles, missing paths, traversal protection and existing fail-closed reference checks remain effective.

The reference review identifies representative taxonomy forms. Do not broadly exempt slash-containing tokens.

These additions do not activate D054 Consumer runtime semantics, create native runbook/recipe directories, change routed Core protocol, or absorb T035 into T034.

## Resume procedure

Resume on the existing represented T034 branch. Do not recreate it, reset it to `develop`, rebase/force-push represented commits, or discard the submitted handoff/history.

The Executor must:

1. synchronize canonical remote state;
2. establish current `origin/develop` containing `docs/reviews/T034-R1.md` and this checkpoint;
3. safely reconcile current `develop` into the existing T034 branch with represented history preserved; if that cannot be done safely, return `BLOCKED`;
4. reload current `AGENTS.md` when required by the governing integrated history;
5. load the original T034 Task Contract plus `docs/reviews/T034-R1.md` as the complete revised execution authority;
6. follow D054/RB001 for Git/uv/PowerShell/shell mechanics and authoritative documentation fallback;
7. implement only the R1 corrections while preserving accepted T034 work;
8. rerun Code Review & Verify and the complete required verification matrix;
9. update `handoffs/T034-executor-handoff.json` with the new implementation anchor/evidence;
10. commit the complete R1 rework and perform one planned final push under D048;
11. verify remote branch HEAD and return only the canonical terminal fields.

## Required R1 verification

The terminal handoff must include green evidence for:

- frozen T034 oracle;
- complete Consumer trigger corpus/grader suite;
- focused bootstrap/validate and missing/tampered Core controls;
- complete Governance artifact/self-contained package suite including `RUNBOOK.template.md` parity;
- complete reference-integrity suite and focused taxonomy/concrete-path regression coverage;
- stable CLI v1 non-regression suite;
- native-Windows canonical:
  - `uv run --locked ruff check .`;
  - `uv run --locked ruff format --check .`;
  - `uv run --locked python -m pytest`.

No skip/xfail/deletion/weakening may be introduced merely to make the suite green.

## Canonical T034-R1 resume prompt

```text
Operate as the Agente de IA Ejecutor for ManuelBouza/agent-governance.

Synchronize the canonical remote and establish current origin/develop. Continue on the existing represented branch feat/t034-native-sdd-executable-materialization; preserve its submitted commits, handoff and history. Safely reconcile current develop into that existing branch. If this cannot be done without discard, branch recreation, force-push or represented-history rewrite, stop and report BLOCKED.

Reload current repository instructions from the reconciled baseline as required.

Then load and execute the authoritative T034 rework specification:
docs/tasks/T034-native-sdd-executable-materialization.md
docs/reviews/T034-R1.md

Treat those files and their referenced repository policies as the complete revised execution specification. Do not infer or expand rework scope from this prompt.

For source checkout/toolchain/bootstrap and other execution mechanics, follow D054 and the applicable semantic runbook including docs/runbooks/RB001-source-executor-checkout-bootstrap.md. Resolve missing adapter syntax from project-native or installed/version-specific help and official vendor/API documentation; do not delegate routine command execution to the Human.

Complete the required R1 implementation, Code Review & Verify, verification and updated executor handoff, commit and push all authorized rework, then return only:

STATUS: DONE | BLOCKED | PARTIAL
HANDOFF: <path>
BRANCH: <branch>
HEAD: <pushed-commit-sha>
```

## Next action

1. Integrate this O146 checkpoint through its short-lived Markdown PR.
2. Reverify canonical `develop` and exact remote T034 branch relation/HEAD after that integration.
3. Give the canonical T034-R1 resume prompt above to the Codex Executor, preferably in the existing T034 Codex chat so represented local context can be reused without becoming authority.
4. Await only the terminal pointer fields.
5. Perform remote D053 Converge/Accept from GitHub.
6. Do not resume T021/T022 and do not author/freeze the T035 oracle until T034 is accepted/integrated and canonical verification is green.

## Next chat minimum load

Until T034-R1 returns a terminal handoff, load only:

- current `develop` identity;
- `AGENTS.md`;
- this checkpoint;
- `docs/tasks/T034-native-sdd-executable-materialization.md`;
- `docs/reviews/T034-R1.md`;
- `tests/test_t034_native_sdd_conformance.py`;
- exact T034 branch/handoff state;
- RB001/D054 only when resolving an execution-boundary conflict.

## Do not

Do not merge submitted T034 HEAD `83abcafc60c943040fa4aa70f242950220851981`; do not discard/recreate/rebase-force the represented T034 branch; do not modify the frozen oracle; do not let the reference-integrity correction broadly suppress real path failures; do not activate D054 Consumer runtime or start T035; do not resume T021/T022; do not hand routine CLI/API/shell commands to the Human; and do not write directly to `main`/`develop`.
