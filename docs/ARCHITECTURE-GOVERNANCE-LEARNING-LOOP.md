# Architecture — Evidence-Driven Governance Learning Loop

Status: PROPOSED  
Decision candidate: D039  
Scope: Agent Governance source-maintenance learning first; future consumer-product applicability only after explicit architecture approval

## Problem

Agent Governance already persists tasks, reviews, handoffs, decisions, checkpoints and deterministic verification. However, the source-maintenance workflow still depends on Humans/agents noticing when a failure or near miss reveals a missing invariant, then manually deciding whether to convert that experience into a durable preventive control.

The T007 sequence exposed two representative classes:

- an executor performed a destructive branch operation before an ambiguity had been fully resolved, then recovered the exact original ref;
- the Orchestrator later appended new commits to a topic branch whose PR had already merged, forcing recovery through a new branch/PR and motivating the merged-branch freeze invariant.

The immediate incidents were recovered and policy was hardened, but the learning process itself was ad hoc. A repeatable system needs to detect comparable signals, force causal analysis, promote useful lessons into enforceable controls, and verify that the original failure mode is no longer silently possible.

## Research synthesis

### Google SRE postmortem/CAPA model

Google SRE treats postmortems as a formal mechanism for preventing recurrence, recommends defining objective postmortem triggers before incidents occur, and emphasizes preventive action items rather than merely documenting what happened. Google also describes automating postmortem creation/metadata extraction and aggregating postmortem data to identify recurring themes and weaknesses.

Adopted principles:

- define learning triggers before the next incident;
- capture evidence and contributing causes, not blame;
- require preventive actions where the incident reveals a systemic gap;
- aggregate structured incident metadata to detect recurrence/trends;
- treat recurrence after a supposed fix as evidence that the control was ineffective.

Primary sources:

- Google SRE, Postmortem Culture: Learning from Failure: `https://sre.google/sre-book/postmortem-culture/`
- Google SRE Workbook, Postmortem Culture: `https://sre.google/workbook/postmortem-culture/`
- Google SRE, Lessons Learned from Other Industries / CAPA: `https://sre.google/sre-book/lessons-learned/`

### NIST SSDF root-cause recurrence prevention

NIST SP 800-218 frames secure software improvement partly as addressing root causes so vulnerabilities do not recur. This supports a general source-maintenance rule: a failure should not be considered fully resolved merely because its immediate symptom was repaired.

Adopted principle:

```text
symptom repair != recurrence prevention
```

Primary source:

- NIST SP 800-218 SSDF: `https://csrc.nist.gov/pubs/sp/800/218/final`

### Policy-as-code and decision telemetry

Open Policy Agent separates policy decision-making from enforcement, treats policy as versionable knowledge, and supports decision logs containing the policy queried, inputs, policy/bundle metadata and related audit information. Agent Governance does not need to adopt OPA as a dependency, but the architecture is useful: separate detection facts, policy authority, enforcement, and audit telemetry.

Adopted principles:

- policy knowledge is explicit/versioned rather than hidden in application/model behavior;
- detectors/enforcers consume structured state;
- policy decisions produce auditable evidence;
- policy changes and policy enforcement are separable responsibilities.

Primary sources:

- OPA documentation: `https://www.openpolicyagent.org/docs`
- OPA integration/management: `https://www.openpolicyagent.org/docs/integration`
- OPA decision logs: `https://www.openpolicyagent.org/docs/management-decision-logs`

### Repository-native enforcement

GitHub rulesets and required status checks can mechanically prevent or block classes of repository mutation. Multiple rulesets can layer, and required checks can make deterministic verifiers part of merge eligibility.

Adopted principles:

- a lesson that can be enforced mechanically should preferentially become a deterministic repository control;
- enforcement should be layered rather than relying on one agent remembering a rule;
- monitor/evaluate controls before or alongside enforcement where rollout risk exists.

Primary sources:

- GitHub rulesets: `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets`
- GitHub ruleset rules: `https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets`

### LLM reflection literature

Reflexion and Self-Refine show that linguistic feedback/reflection can improve subsequent model behavior without necessarily changing model weights. This is useful as a hypothesis-generation technique, but D037 already prohibits probabilistic model behavior from becoming source-product verification authority.

Adopted boundary:

```text
model reflection = candidate analysis aid
model reflection != incident fact
model reflection != policy authority
model reflection != verification gate
```

Primary sources:

- Reflexion, NeurIPS 2023 / arXiv 2303.11366
- Self-Refine, NeurIPS 2023 / arXiv 2303.17651

## Proposed architecture

Name: **Evidence-Driven Governance Learning Loop (EGLL)**.

```text
repository / workflow / verification events
                  │
                  ▼
       deterministic signal detectors
                  │
                  ▼
          LEARNING CANDIDATE
       evidence + stable fingerprint
                  │
                  ▼
        causal/systemic analysis
        Human / Orchestrator owned
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
  no systemic gap       systemic gap
  close with reason          │
                             ▼
                     CONTROL CANDIDATE
                 policy · test · schema · rule
                 workflow · tool · template
                             │
                             ▼
                     controlled change flow
                             │
                             ▼
                   regression/replay proof
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
            does not catch           catches
            original class        original class
                  │                     │
                  ▼                     ▼
               REWORK             VERIFIED LEARNING
                                        │
                                        ▼
                              recurrence monitoring
                                        │
                              same fingerprint recurs
                                        │
                                        ▼
                                  CONTROL_FAILURE
                              mandatory re-analysis
```

## Learning states

Each learning case has exactly one state:

- `DETECTED` — a qualifying signal exists with evidence;
- `TRIAGED` — scope/severity/fingerprint are resolved;
- `ANALYZED` — contributing/systemic causes are documented;
- `CONTROL_PLANNED` — a preventive/detective control is selected;
- `CONTROL_INTEGRATED` — the control exists in canonical Git/repository settings;
- `VERIFIED` — regression/replay evidence proves the control detects/prevents the original failure class;
- `CLOSED_NO_ACTION` — evidence demonstrates no systemic control change is warranted;
- `CONTROL_FAILURE` — a verified fingerprint recurred or the control failed its promised detection/prevention property;
- `SUPERSEDED` — a newer learning record explicitly replaces the prior control model.

`CLOSED` without either verification or a reasoned no-action disposition is not valid.

## Learning signal taxonomy

### Deterministic / automatically detectable

Initial source-maintenance detectors SHOULD cover:

1. **Verification regression** — required deterministic test/check changes from pass to fail.
2. **Workflow nonconformance** — persisted handoff/review reports a `procedural_nonconformance` or equivalent violation.
3. **Merged-branch advancement** — a merged PR source branch still exists and its current HEAD differs from the PR's reviewed `head_sha`.
4. **Branch-retirement backlog** — an eligible merged topic branch remains beyond the permitted closure window/state.
5. **Task/branch/handoff mismatch** — Task Contract expected branch/handoff identity disagrees with returned/persisted evidence.
6. **Acceptance rework** — a task produces a new formal rework round after an executor claims `DONE`; this is a learning candidate, not automatically a defect.
7. **Protection bypass/direct-write evidence** — canonical long-lived state changes outside the authorized PR flow where deterministically observable.
8. **Security verification failure/known-bad recurrence** — D035/D037 deterministic security control reports a failure class previously marked resolved.
9. **Repeated exception/override fingerprint** — the same explicit exception class occurs beyond a configured threshold.

### Human/Orchestrator-triggered

Some high-value signals cannot honestly be detected by code alone:

- Human correction that exposes a missing/incorrect process assumption;
- semantic architecture error discovered during review;
- unsafe but technically valid action not represented by existing deterministic state;
- recurring manual workaround/toil whose cost justifies automation.

These SHALL create the same learning case type, but the trigger evidence is a persisted review/decision/checkpoint reference rather than pretending the detector was automatic.

## Stable fingerprints

Trend analysis requires recurrence identity that does not depend on natural-language wording.

Examples:

- `git.branch.post_merge_advance`
- `git.branch.delete_before_review_resolution`
- `task.handoff.identity_mismatch`
- `task.done_requires_rework`
- `verification.regression.security_known_bad`
- `workflow.direct_write.long_lived_branch`

A fingerprint identifies the failure/control class, not a person or agent product.

If the same fingerprint recurs after a learning case reached `VERIFIED`, the new case MUST enter `CONTROL_FAILURE` unless evidence proves it is materially a different condition.

## Incident-to-control promotion matrix

A learning result is preferentially promoted to the strongest honest control layer:

| Failure class | Preferred control |
|---|---|
| mechanically invalid repository state | deterministic detector / status check / ruleset |
| protocol/state transition error | contract/state-machine regression test |
| ambiguous Task Contract/handoff field | schema + Task Contract/handoff policy |
| recurring workflow misuse | workflow invariant + automated precondition/check |
| security known-bad recurrence | security fixture/scanner/config verifier |
| qualitative architecture mistake | Decision/architecture rule + focused deterministic proxies only where meaning is preserved |
| human-facing ambiguity | interaction/Task Contract policy; no fake deterministic oracle |

The system MUST NOT create a weak proxy test merely to claim automation when the actual requirement is qualitative; D037 remains controlling.

## Authority and ownership

### Automatic components MAY

- detect deterministic signals;
- emit structured evidence/fingerprints;
- fail/annotate a check where an existing accepted invariant is violated;
- aggregate recurrence counts and trend summaries;
- replay deterministic regression cases.

### Automatic components MUST NOT

- create new Governance authority;
- silently change policy/architecture/Task Contracts;
- weaken acceptance criteria;
- auto-approve their own proposed preventive action;
- infer Human intent from a failure;
- use an LLM judgment as a PASS/FAIL gate.

### ChatGPT Orchestrator owns

- causal/systemic analysis;
- architecture/policy/control selection;
- committed Markdown learning records and Decisions;
- deciding whether a signal warrants a systemic change;
- acceptance of the resulting control and regression proof.

### Agente de IA Ejecutor owns

- authorized non-Markdown detectors;
- fixtures/replay cases/tests;
- CI/check implementation;
- structured non-authoritative telemetry artifacts where the Task Contract authorizes them;
- verification execution/evidence.

### Human Owner owns

- final architecture/risk decisions;
- exceptions/overrides;
- acceptance of material authority changes.

## Persistence model

For the source repository, Git remains authoritative.

Recommended surfaces:

- `docs/learning/` — Orchestrator-owned Markdown learning records for material cases;
- deterministic detector/test implementation under repository code/tests as selected by Task Contract;
- CI/check artifacts/logs — evidence transport, not authority;
- Decision Records — only for material architecture/policy changes;
- checkpoint — current unresolved learning/control frontier only, not full historical duplication.

Do not create a live consumer `.agent-governance/` or `.agent-coordination/` footprint in this source repository.

A future consumer EGLL may use a separate installed-state schema, but that is outside this source-maintainer proposal until explicitly approved.

## Material learning record schema

A source-maintainer learning Markdown record SHOULD include:

- Learning ID (`LNNN`);
- status/state;
- stable fingerprint;
- detection source and timestamp/revision;
- affected task/PR/decision/control;
- factual evidence references;
- immediate recovery/containment;
- contributing causes;
- systemic gap determination;
- selected control and owner;
- implementation Task/PR references;
- regression/replay acceptance evidence;
- recurrence links;
- closure or no-action rationale.

The record must separate facts from analysis and selected policy.

## Closure invariants

```text
failure observed != learning completed
written lesson != preventive control
control integrated != control effective

verified learning = evidence
                  + causal analysis
                  + selected control
                  + integrated control
                  + regression/replay proof
```

For an automatically detectable class:

```text
learning cannot reach VERIFIED
unless the original failure class is represented by a deterministic detector/replay
or a documented D037 limitation explains why that would change the requirement's meaning
```

## Automatic trend escalation

The detector/aggregator SHOULD compute recurrence counts by stable fingerprint.

Recommended default escalation semantics:

- first occurrence -> normal learning triage;
- second occurrence before a control is verified -> raise priority, but do not infer same root cause automatically;
- recurrence after `VERIFIED` -> `CONTROL_FAILURE`;
- multiple distinct fingerprints with a shared control surface -> architecture-level trend candidate.

Thresholds must be repository-configured and deterministic; an LLM does not decide that a statistical pattern exists.

## Source-maintenance MVP

A minimal executable implementation can be narrow and high-value:

1. define a deterministic learning-signal schema and fingerprint catalog in code/fixtures;
2. implement repository-state detectors for:
   - merged-branch advancement;
   - stale merged branch retirement;
   - Task Contract / handoff branch/path mismatch;
   - explicit executor `procedural_nonconformance` evidence;
3. provide deterministic replay fixtures for the T007 incidents;
4. emit machine-readable detector output suitable for CI/check presentation;
5. make detector failures/advisories visible before the next source-maintenance operation/merge as appropriate;
6. require Orchestrator learning triage for new fingerprints;
7. prove that the T007 post-merge branch-reuse fixture is caught without model/network dependency in the core test path.

A later phase can add GitHub API/Actions integration for live remote-state detection, with bounded network behavior and deterministic interpretation of returned facts.

## GitHub enforcement strategy

Repository controls should be layered:

1. existing protected-branch/PR controls prevent obvious long-lived-branch violations;
2. deterministic repository tests verify static/in-repository learning invariants;
3. a GitHub-aware detector checks remote lifecycle facts that cannot exist in a local fixture alone;
4. required status checks/rulesets enforce accepted invariants where GitHub supports the required state;
5. post-integration cleanup remains an operational detector because GitHub cannot encode every dynamic lifecycle condition as a static branch rule.

Do not make an external policy engine or service a required product dependency merely to implement EGLL. The OPA pattern informs separation of policy/decision/evidence; it does not imply adopting OPA.

## Relationship to existing decisions

- **D022** — EGLL uses the existing repository-native change procedure; learning does not bypass Task Contracts/PRs.
- **D027/D028** — unresolved learning/control state belongs in the durable checkpoint so cold-start orchestration does not forget it.
- **D029** — executor evidence identity remains independently auditable.
- **D032** — quality review can create learning candidates, but interaction adaptation is not learning authority.
- **D035** — security freshness/known-bad signals are valid learning inputs; historical PASS is never permanent authority.
- **D037** — all source-product learning gates remain deterministic/code-first. LLM reflection is advisory analysis only.
- **D038** — external review/provider evidence may contribute evidence but cannot gain Governance authority through EGLL.

## What EGLL explicitly does not do

- no model fine-tuning or weight updates;
- no hidden/private assistant memory as project authority;
- no autonomous policy mutation;
- no model-as-judge learning gate;
- no automatic blame attribution;
- no guarantee that every Human/semantic mistake is machine-detectable;
- no requirement to create a heavyweight postmortem for every ordinary test failure.

The goal is not zero mistakes. The goal is that meaningful failure classes become increasingly difficult to repeat silently.

## Adoption recommendation

Recommend adopting D039 with a staged implementation:

### Phase A — source-maintainer learning contract

Persist the learning lifecycle, trigger taxonomy, fingerprint semantics, closure gate and role boundaries. Seed the historical T007 incidents as learning examples, not as new active incidents.

### Phase B — deterministic MVP

Create a dedicated Task Contract for the executor to implement the signal schema, fixtures and local deterministic detectors. Keep model/network dependencies out of the core test path.

### Phase C — GitHub-aware remote detector

Add bounded GitHub-state checks for merged-branch advancement/retirement and other remote-only facts. Run as CI/maintenance verification where appropriate.

### Phase D — trend aggregation

Aggregate fingerprints and detect recurrence/control failure mechanically.

### Phase E — consumer-product decision

Only after source-maintainer evidence demonstrates value should a separate Decision determine whether/how EGLL becomes a Governance Core consumer capability.

## Acceptance criteria for the architecture

The architecture is acceptable only if:

1. learning authority remains Git/policy/evidence based, not model-memory based;
2. automatic detection cannot silently mutate authority;
3. every material learning case separates factual evidence, causal analysis and selected control;
4. `VERIFIED` requires regression/replay evidence or an explicit D037 irreducibility limitation;
5. recurrence after verified control is treated as control failure;
6. role ownership remains D016-compatible;
7. source/consumer repository boundaries remain intact;
8. the mechanism can start with deterministic local fixtures and does not require external services;
9. live GitHub detection, when added, has bounded deterministic interpretation;
10. removal of any optional LLM reflection aid does not change correctness or release-gating semantics.
