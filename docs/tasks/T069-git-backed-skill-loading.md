# T069 — Git-backed Skill Loading Fallback

## Identity

- Task ID: `T069`
- Status: `READY`
- Type: `feature`
- SDD profile: `COMPACT`
- Base branch: `develop`
- Base SHA: `5bed8b952a3c552e3af0abfdbe07895864319696`
- Topic branch: `feat/t069-git-backed-skill-loading`
- Expected executor handoff: `handoffs/T069-executor-handoff.json`
- Test-Authorship-Mode: `orchestrator-conformance`
- Owner: `ChatGPT Orchestrator / Agente de IA Ejecutor / Human Owner`
- ChatGPT Effort: `MEDIUM`
- Execution Shape: `SINGLE_EXECUTION`

## Objective

Make repository-owned Agent Governance Skills usable through a canonical Git-backed loading path whenever a host does not expose native Skill routing/resources, while preserving the same Skill semantics, Git authority, progressive disclosure, and fail-closed behavior.

This task does not install or emulate a native host Skill runtime and does not resume T068 ChatGPT host qualification.

## Current specification carrier / controlling references

- `AGENTS.md`, especially LR-02, LR-06, LR-07, LR-11 and LR-12
- `maintainer-skill/SKILL.md`
- `maintainer-skill/references/orchestrator-route.md`
- `docs/BRANCHING.md`
- D082 Skill topology as already integrated in `develop`

## Requirement / specification delta

### ADDED

- **REQ-T069-1 — Git-backed fallback:** when native Skill routing/resources are unavailable, load the applicable repository-owned Skill directly from canonical Git.
- **REQ-T069-2 — Revision coherence:** bind Skill source to the same represented Git revision that governs active authority; do not mix materially different revisions.
- **REQ-T069-3 — Progressive disclosure:** load root `SKILL.md` first, then only required route/references and independently-triggered transverse Skills.
- **REQ-T069-4 — Observable host claims:** Git-backed loading must never be represented as native host Skill activation.
- **REQ-T069-5 — Canonical path map:** preserve one Maintainer domain Skill plus exactly five transverse top-level Skill sources; `workspace-isolation` remains subordinate.

### PRESERVED

- **REQ-T069-P1:** Git, not Skill runtime state, remains repository authority.
- **REQ-T069-P2:** deterministic bootstrap/correctness must continue to work with model-driven Skills absent or disabled.
- **REQ-T069-P3:** D082 topology and semantic ownership remain unchanged; no host-specific semantic fork is introduced.
- **REQ-T069-P4:** T068 remains deferred; ChatGPT/Codex empirical parity remains `NOT_ESTABLISHED`.
- **REQ-T069-P5:** T066 remains untouched and unstarted.

## Controlling Design

Two loading modes are supported for the same repository-owned Skill semantics:

```text
native host routing available
    -> host discovers/loads repository-owned Skill projection

native host routing unavailable
    -> bootstrap canonical Git authority
    -> resolve intent
    -> read canonical Skill SKILL.md from the represented authority revision
    -> progressively load only required references/routes
```

The fallback is implemented as repository instructions plus Maintainer Skill reference guidance, not as a host emulator or separate Skill copy.

Canonical source paths are:

- `maintainer-skill/SKILL.md`
- `repository-change-control-skill/SKILL.md`
- `upstream-version-revalidation-skill/SKILL.md`
- `research-evidence-traceability-skill/SKILL.md`
- `durable-work-checkpoint-skill/SKILL.md`
- `executor-launch-handoff-skill/SKILL.md`

`workspace-isolation` remains subordinate under `executor-launch-handoff`.

Revision binding rule:

1. fresh bootstrap begins from current `develop`;
2. when an authorized topic branch/HEAD becomes controlling, Skill source is loaded from that represented state;
3. materially different authority and Skill revisions must not be mixed;
4. ambiguity/staleness fails closed.

## Plan & Trace

| Unit | Requirement / Design | Candidate artifact(s) | Required verification/evidence |
| --- | --- | --- | --- |
| `U1` | REQ-T069-1..4 | `AGENTS.md` | static semantic assertions + review |
| `U2` | REQ-T069-1..5 | `maintainer-skill/SKILL.md`; `maintainer-skill/references/git-backed-skill-loading.md` | static semantic assertions + reference/path inspection |
| `U3` | all | `tests/test_git_backed_skill_loading.py` | focused pytest + full suite |

## Stage ownership and candidate boundary

D068 applies:

```text
Stages 1-4 -> ChatGPT Orchestrator
Stage 5    -> ChatGPT Orchestrator
Stage 6    -> Agente de IA Ejecutor
Stage 7    -> ChatGPT Orchestrator
```

The complete Stage 5 semantic candidate is materialized before Stage 6.

## Published candidate freeze

Material candidate content anchor:

```text
candidate_branch:         feat/t069-git-backed-skill-loading
candidate_base:           5bed8b952a3c552e3af0abfdbe07895864319696
candidate_content_anchor: 972e9dff59079d2820b5b750f9a4a5c52913fa9e
```

Commits after `candidate_content_anchor` may contain only this Task Contract and current checkpoint/launch metadata. Any material change to `AGENTS.md`, Skill source/reference, tests, or semantics requires Stage 5 re-entry and a new content anchor.

## Authorized scope

The Executor may:

- verify the exact candidate branch/base/content-anchor relationship;
- run the focused T069 conformance tests and the repository's normal relevant/full verification;
- inspect the changed Markdown/reference semantics and canonical Skill paths;
- make only bounded technical repairs to the T069 Python test mechanics if semantics remain unchanged;
- persist `handoffs/T069-executor-handoff.json`, commit/push authorized technical repair/evidence state, and return the exact remote branch HEAD.

## Explicit exclusions

The Executor must not:

- change `AGENTS.md`, committed Markdown, Skill semantics, topology, Task Contract, or conformance meaning;
- add native ChatGPT packaging/install behavior or resume T068;
- create a new host-specific Skill fork;
- promote `workspace-isolation` to a top-level Skill;
- start/modify T066;
- relabel ChatGPT/Codex empirical parity;
- treat native/runtime availability as a prerequisite for deterministic correctness.

## Invariants / constraints

- Git remains canonical authority.
- Native and Git-backed modes differ only in discovery/loading mechanics at the repository-owned Skill layer.
- The fallback must be host-neutral and observable-claim-safe.
- Cold-start correctness must not depend on private chat history, Project Memory, or installed Skill state.
- Normal branch policy remains topic branch -> PR -> `develop`.

## Executor process autonomy

Inside Stage 6 bounds, the Executor owns concrete execution mechanics and compatible private tooling under D041/D054. Private process choices cannot alter T069 semantics or authority.

## D076 executable-materialization boundary

The Stage 5 candidate already contains the semantic conformance test. A substantial new controller/harness/oracle discovered as necessary in Stage 6 is a re-entry condition.

## Acceptance criteria

- **AC-T069-1:** `AGENTS.md` explicitly defines a Git-backed fallback when native Skill routing/resources are unavailable.
- **AC-T069-2:** fallback guidance binds Skill content to the represented controlling Git revision and fails closed on ambiguity/staleness.
- **AC-T069-3:** the Maintainer Skill routes to a progressive-disclosure Git-backed loading reference containing the six canonical top-level source paths.
- **AC-T069-4:** fallback guidance forbids claiming native host activation and preserves Git authority/host neutrality.
- **AC-T069-5:** D082 topology remains one Maintainer Skill plus five transverse Skills; `workspace-isolation` remains subordinate.
- **AC-T069-6:** focused and full repository verification pass with no unresolved material review item.
- **AC-T069-7:** T068 remains deferred, T066 untouched, and empirical parity unchanged.

## Verification and trace requirements

Required Stage 6 evidence:

1. verify exact remote branch/base/current HEAD and metadata-only post-anchor delta;
2. `pytest tests/test_git_backed_skill_loading.py`;
3. relevant existing Skill/layout/reference-integrity tests;
4. normal Ruff/code-health verification applicable to the changed Python test surface;
5. full repository `pytest` suite;
6. inspect `AGENTS.md`, `maintainer-skill/SKILL.md`, and `git-backed-skill-loading.md` for semantic coherence and no topology fork;
7. confirm no unrelated tracked changes.

`tests/test_git_backed_skill_loading.py` is the Orchestrator-owned conformance projection for T069 semantics.

## Code Review & Verify obligations

Review must specifically check:

- no host-native activation claim is inferred from Git-backed loading;
- no stale/mixed-revision loading path is authorized;
- no duplicate semantic Skill source is introduced;
- all six canonical top-level Skill paths exist;
- `workspace-isolation` remains subordinate;
- no T068/T066 scope leakage.

## Stop / escalation / SDD re-entry conditions

STOP rather than guess when:

- candidate/base/branch/content-anchor identity is unsafe or ambiguous;
- post-anchor delta contains material candidate changes;
- required canonical Skill paths/topology differ from the Design;
- repository tests expose a semantic conflict with accepted D082 behavior;
- a repair would require changing Markdown, Skill semantics, or conformance expectations;
- a D076-material executable artifact is missing;
- T068, T066, or unrelated scope would need modification.

## Expected handoff / evidence

```text
handoffs/T069-executor-handoff.json
```

The handoff must capture candidate identity, any bounded technical test repair, commands/results, review findings, D076 audit, unrelated-change audit, and unresolved issues.

## Terminal return shape

```text
STATUS: COMPLETED | BLOCKED
HANDOFF: handoffs/T069-executor-handoff.json
BRANCH: feat/t069-git-backed-skill-loading
HEAD: <actual remote pushed HEAD>
```

## Human launch gate

```text
launch_state: AUTHORIZED_AWAITING_HUMAN_START
```

Stage 6 launch is allowed only from the exact checkpointed remote head after ChatGPT verifies the metadata-only post-anchor delta.

## Thin transport invariant

The Human-visible Executor launch prompt is only a bootstrap pointer to this Task Contract and exact candidate state. It must not duplicate T069 semantics, test matrix, exclusions, or acceptance rules.
