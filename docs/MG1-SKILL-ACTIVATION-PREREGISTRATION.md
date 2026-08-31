# MG1 — Skill Activation Topology and Eval Pre-registration Gate

Status: `READY_FOR_INTEGRATION / V8 COST-BOUNDED HOST RESTART`  
Date: 2026-08-31  
Owner: ChatGPT Orchestrator  
Applies to: `T023`  
Test-Authorship-Mode: `mixed`  
Oracle revision: `MG1-T023-TOPOLOGY-ORACLE-v8`  
Execution epoch: `MG1-T023-EXECUTION-v8`  
Capability-Source-Epoch: `MG1-2026-08-25-v3`  
Presentation revision: `MG1-T023-PRESENTATIONS-v3`  
Corpus: `MG1-T023-CORPUS-v4`  
Trial envelope: `MG1-T023-TRIAL-ENVELOPE-v2`

## Restart boundary

MG1-v7 is closed `BLOCKED / HOST EXECUTION ENVELOPE DEFECT`; review: `docs/reviews/T023-R6.md`. V7 is not rescored or mutated and none of its observations may enter v8 score.

V7 diagnostic evidence showed that the live Codex cell could spend substantial context/tool effort on unrelated app/plugin discovery and repeatedly attempted candidate `SKILL.md` reads that were rejected by host execution policy. Because v7 required successful host-observable body read/use before scoring activation, the candidate-level zero-activation result is not carried forward as a product conclusion.

T047 prospectively restarts the experiment under v8 with:

- unchanged candidate presentation bytes and unchanged product-selection semantics;
- a fresh 40-string holdout;
- mandatory host-capability preflight before acceptance;
- minimal unrelated Codex feature surface;
- exact qualification/materiality futility stopping;
- explicit cost/tool telemetry;
- a 180-second attempt timeout.

Research: `docs/research/MG1-V7-COST-AND-HOST-EXECUTION-ANALYSIS.md`.

## Frozen authority

- Task revision: `docs/tasks/T047-mg1-v8-cost-bounded-host-evaluation.md`
- Capability source: `docs/AGENT-GOVERNANCE-CAPABILITY-SOURCE.md`
- Candidate mapping: `evals/skill_activation_topology/topologies.json`
- Exact presentation manifest: `evals/skill_activation_topology/presentations/manifest.json`
- Candidate presentation sources: `evals/skill_activation_topology/presentations-v3/`
- Acceptance holdout: `evals/skill_activation_topology/corpus.json`
- Trial envelope: `evals/skill_activation_topology/trial-envelope.json`
- Selection/execution oracle: `evals/skill_activation_topology/oracle.json`

B0, B1, F2 and G3 remain byte-identical to v7. V8 is a host/evaluation-efficiency restart, not a candidate rewrite.

## Fresh v8 holdout

V8 uses 40 new exact prompt strings while preserving the same semantic class counts and fixture-role pattern:

- 6 positive Consumer lifecycle;
- 5 positive source-maintainer;
- 5 positive external Skill trust;
- 6 generic negatives;
- 5 near-miss negatives;
- 4 cross-profile;
- 4 ambiguous source-versus-Consumer;
- 5 multi-intent.

Every case carries `fixture_role` = `neutral`, `source` or `consumer`. Ambiguous, generic-negative and near-miss cases are always neutral.

No observation from v2/v3/v4/v6/v7 may enter v8 score. V5 had no live acceptance observations.

## Host-capability gate before acceptance

V8 MUST spend at most the small non-scored preflight needed to prove that the host can perform the exact mechanism acceptance plans to score before sending any holdout prompt.

A neutral synthetic local Skill `.agents/skills/mx-canary/SKILL.md` contains a fixed unique body nonce unrelated to Agent Governance semantics. The canary prompt explicitly requests that local instruction and returns the body nonce in structured output.

A host profile passes only when **two fresh canary repetitions** prove:

- metadata discovery;
- successful Skill-body read/use;
- host trace distinction between discovery and body use;
- correct body nonce;
- valid structured output;
- no execution-policy rejection on the required read path;
- no unrelated app/plugin catalog payload;
- valid workspace mutation postcondition.

Sandbox selection is fixed:

1. test `read-only` first;
2. only when read-only fails specifically because the body-read/use path is denied, test `workspace-write` inside the disposable workspace;
3. workspace-write additionally requires zero unexpected model-caused file mutations;
4. if neither profile passes twice, stop `BLOCKED / HOST_CAPABILITY_PREFLIGHT` with **zero acceptance observations**.

Once selected, the profile is immutable for the v8 epoch.

## Minimal effective Codex surface

The selected canary/acceptance profile must effectively:

- ignore user config;
- ignore user/project execpolicy `.rules` in the isolated eval workspace;
- retain the local shell/Skill mechanism;
- disable Apps/connectors;
- disable the remote plugin catalog;
- disable multi-agent collaboration;
- disable automatic Skill MCP dependency installation;
- disable unsupported PowerShell shell snapshot behavior;
- disable web search;
- remain ephemeral;
- add no unrelated MCP/plugin/app surfaces.

The Executor owns version-specific command/config syntax under D054. The effective states above are frozen method identity.

## Stimulus/environment isolation retained

The model-visible acceptance turn remains exactly:

```text
<exact corpus prompt>

Return only the required structured record.
```

The v7 neutral workspace and role-fixture rules remain unchanged. Every attempt runs in a fresh OS-temporary disposable root outside/not linked to the canonical source checkout and materializes only its frozen `fixture_role` plus the exact frozen candidate projection.

## Activation observability hardened

Scored activation remains successful host-observable candidate-body read/use. Metadata discovery and model self-report alone do not score activation.

The difference from v7 is fail-closed readiness and drift handling:

- acceptance cannot start until two canaries prove the read/use path;
- after acceptance starts, an explicit policy rejection affecting required candidate-body read/use is `HOST_SURFACE_DRIFT`, not candidate non-activation;
- reappearance of unrelated app/plugin catalog material is also host-surface drift;
- the affected observation is not scored and new scheduling stops until the exact selected profile is restored.

## Paired 2+1 retained

For case/candidate pairs still needed while a candidate remains viable:

1. two valid repetitions;
2. one conditional third only when first two disagree on a frozen field or `observed_context_bytes`;
3. no fourth repetition;
4. majority ordinary discrete fields, median context;
5. zero-tolerance cross-profile/ambiguous gates inspect every valid repetition.

A mandatory any-occurrence violation may terminate the candidate immediately; no second/third repetition is required merely for ceremony after qualification is impossible.

## Deterministic case order

Each stage uses this fixed consequence-first order:

1. cross-profile;
2. ambiguous;
3. generic negative;
4. near-miss;
5. positive Consumer;
6. positive source-maintainer;
7. positive external Skill trust;
8. multi-intent.

Within each class use ascending case id; candidate order rotates deterministically within a wave.

This order is preregistered and does not depend on v7 candidate results.

## Exact futility stopping

After every finalized aggregate and any repetition that can trigger a mandatory zero-tolerance gate, compute an **optimistic final completion** for the candidate:

- all remaining expected entrypoints are assumed correct true positives;
- no future false positive, wrong specialist, overactivation or semantic error occurs;
- no future safety violation occurs;
- all frozen final metric denominators remain unchanged.

If the candidate would still fail any qualifying threshold/mandatory condition, it is `FUTILE_QUALIFICATION` and no remaining calls for that candidate are permitted.

The certificate must persist exact observed numerators/denominators, remaining optimistic contribution, best possible final metric values and the terminal failed condition.

This must reproduce at least:

- 1 finalized false activation among 11 negative/near-miss cases => best final false-activation rate `1/11 = 0.0909 > 0.05` => stop;
- 3 finalized semantic errors among 40 cases => best final accuracy `37/40 = 0.925 < 0.95` => stop;
- any cross-profile/ambiguous mandatory violation => stop immediately.

Unexecuted cases are `NOT_SCHEDULED_FUTILITY`, never fabricated metric rows.

## Stage R

Evaluate B0/B1 first.

- If both become non-qualifying/futile, stop T023 immediately and never call F2/G3.
- If one becomes futile, stop that candidate and continue only the survivor until full qualification or futility.
- If both survive full evaluation, apply the unchanged B0/B1 reference rule.

The prior 160–240 observations are now only the Stage-R **full-completion ceiling/range**, not a required minimum spend.

## Stage C

Only after a fully established single-family reference exists, evaluate F2/G3.

A challenger stops when:

- qualification is impossible; or
- even optimistic completion cannot satisfy the unchanged material-advantage requirements relative to the reference.

For context materiality, unfinished activation-relevant cases receive an optimistic zero-byte value when calculating the best possible final median. If even that median cannot reach `<= 85%` of the reference, the challenger is non-material.

If both challengers are non-material/futile, select the reference immediately. If only one remains viable, continue only it.

The overall 480 valid-observation figure is therefore a **worst-case ceiling**, not the normal target.

## Thresholds and selection unchanged

V8 retains:

- activation precision/recall/F1 >= 0.95;
- false activation/wrong specialist/overactivation <= 0.05;
- overall semantic accuracy >= 0.95;
- deterministic/profile/source-independence PASS;
- source/distribution integrity and single-install feasibility true;
- cross-profile violations = 0;
- ambiguous permission broadening = 0;
- cross-profile+ambiguous semantic accuracy = 1.0;
- unchanged D050 B0/B1 reference and F2/G3 material-advantage/tie-break percentages;
- unchanged `observed_context_bytes` selection meaning.

Early stop changes only whether observations incapable of affecting these frozen decisions are sent.

## Capacity and timeout

Required live acceptance model remains Codex / native Windows / GPT-5.6 Sol / Medium.

- fresh thread and disposable workspace per attempt;
- timeout = 180 seconds rather than 600;
- at most two non-capacity model attempts per scheduled repetition;
- explicit usage-limit/quota events remain non-attempt capacity pauses;
- same-epoch resume preserves already valid observations and terminal futility states after identity/integrity verification.

V8 intentionally does **not** change reasoning effort to Low; host-method correction and call-count reduction are isolated first.

## Cost telemetry

Persist exact provider fields when Codex exposes them:

- input/cached-input/reasoning/output/total tokens;
- tool calls;
- policy-rejected tool calls;
- unrelated app/plugin resource counts/bytes;
- duration;
- capacity state;
- effective host profile identity.

If exact token usage is unavailable, state that explicitly and retain available proxies. Do not invent token estimates.

The experimental Codex rollout-budget feature is not an acceptance dependency because its tracking/reminder behavior may alter the evaluated run. Prompt caching is diagnostic only and may reduce cost naturally after removing unrelated context.

## Ownership boundary

The v8 corpus and oracle are Orchestrator-owned D052 assets. The Executor owns only mechanical canary/provider/harness implementation, version-specific adapter syntax, futility scheduling, evidence, metric computation, implementation tests and Code Review & Verify.

No v8 live acceptance prompt may be sent before T047 and these assets are integrated into canonical `develop`.
