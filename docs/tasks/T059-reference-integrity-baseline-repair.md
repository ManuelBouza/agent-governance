# T059 — Reference Integrity Baseline Repair

## Identity

- Task ID: `T059`
- Status: `READY`
- Type: `bugfix / deterministic test harness`
- Base branch: `develop`
- Expected implementation branch: `fix/t059-reference-integrity-baseline-repair`
- Expected executor handoff: `handoffs/T059-executor-handoff.json`
- SDD-Profile: `STANDARD`
- Test-Authorship-Mode: `executor-implementation`
- Blocking work: T058 final verification

## Explore / Frame

T058 was previously blocked because the repository-wide suite failed on two baseline defects outside T058 authority. Current `develop` has already eliminated the former governance-artifact failure, but the canonical Markdown reference-integrity test still misclassifies valid D058 prose in `AGENTS.md`.

The expression ``develop == origin/develop`` is a comparison/equivalence statement describing local/remote branch alignment. The current mechanical `looks_like_path()` heuristic sees the slash in `origin/develop` and classifies the whole expression as a repository path, producing a false unresolved-reference failure.

The repair must fix the classifier/harness semantics rather than rewriting valid governance prose merely to satisfy the test.

## Specify

### ADDED — T059-R1 comparison/equivalence prose classification

The reference classifier SHALL treat a backtick token as non-path prose when the token is structurally an inline comparison/equivalence expression rather than a concrete repository path.

At minimum, the existing canonical expression:

```text
develop == origin/develop
```

must not be classified as a repository path.

The rule must be narrow and deterministic. It MUST NOT create a broad exemption for arbitrary slash-containing strings.

### PRESERVED — T059-P1 concrete path detection

Existing concrete repository-path candidates must continue to classify as paths, including at least:

```text
docs/tasks/T034-native-sdd-executable-materialization.md
governance-core/SDD.md
src/agent_governance/artifact.py
.github/workflows/check.yml
../outside.md
```

### PRESERVED — T059-P2 existing taxonomy exemptions

Existing SDD taxonomy prose exemptions such as `ADDED/MODIFIED/REMOVED/PRESERVED` and `Converge/Accept/Evolve` must remain unchanged in meaning.

### PRESERVED — T059-P3 no governance semantic rewrite

Do not change `AGENTS.md` or other committed Markdown to work around the classifier defect.

## Design

Keep the change inside the deterministic reference-classification harness. The expected implementation surface is:

- `tests/_helpers.py`;
- `tests/test_reference_integrity.py` for focused regression coverage;
- `handoffs/T059-executor-handoff.json`.

Prefer a small explicit predicate or narrowly scoped extension of `looks_like_path()` that detects comparison/equivalence prose before slash-based path classification.

Do not introduce a new dependency, parser framework, or generalized Markdown semantic parser.

## Plan & Trace

1. Reproduce the current canonical failure on exact `develop`.
2. Add focused regression coverage proving the D058 comparison expression is prose.
3. Preserve existing concrete-path and taxonomy-path tests.
4. Implement the smallest classifier correction.
5. Run focused reference-integrity tests.
6. Run the full repository quality gate.
7. Persist handoff evidence and pushed implementation HEAD.

Trace:

- T059-R1 -> focused regression for comparison/equivalence expression + classifier implementation.
- T059-P1 -> existing and/or explicit concrete-path regression coverage.
- T059-P2 -> existing taxonomy regression coverage.
- T059-P3 -> changed-path verification: no committed Markdown changes from Executor.

## Authorized scope

Executor may modify only:

- `tests/_helpers.py`;
- `tests/test_reference_integrity.py`;
- `handoffs/T059-executor-handoff.json`.

Any need to change other files is a stop/re-entry condition.

## Explicit exclusions

Executor MUST NOT:

- edit committed Markdown;
- weaken canonical reference-integrity coverage;
- broadly ignore slash-containing prose;
- change unrelated test behavior;
- modify T058 implementation or handoff;
- add dependencies or configuration changes.

## Acceptance criteria

- **AC-T059-1:** `develop == origin/develop` is classified as prose/non-path.
- **AC-T059-2:** concrete path candidates remain classified as paths.
- **AC-T059-3:** existing SDD taxonomy exemptions remain correct.
- **AC-T059-4:** canonical `AGENTS.md` reference-integrity test passes without changing `AGENTS.md`.
- **AC-T059-5:** full repository quality gate passes.
- **AC-T059-6:** Executor-authored Markdown is absent and changed paths stay within authorized scope.

## Verification

Minimum final verification:

```text
uv run --locked python -m pytest tests/test_reference_integrity.py
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked python tools/code_health.py check
uv run --locked python -m pytest
git diff --check
```

The handoff must record the exact base SHA, implementation HEAD, focused/full-suite results, changed paths, and confirmation that no T058 files were modified.

## Stop / SDD re-entry conditions

Stop and report `BLOCKED` if:

- the failure cannot be corrected without changing governance Markdown semantics;
- the smallest correct fix requires a generalized parser or dependency change;
- focused correction causes concrete paths to become false negatives;
- another independent baseline failure remains after this repair.

## Expected handoff

Persist:

`handoffs/T059-executor-handoff.json`

Return only:

```text
STATUS: DONE | BLOCKED
HANDOFF: handoffs/T059-executor-handoff.json
BRANCH: <branch>
HEAD: <pushed-head>
```
