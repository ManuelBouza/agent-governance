# MG1-v7 Cost and Host-Execution Analysis

Date: 2026-08-31  
Owner: ChatGPT Orchestrator  
Applies to: T023 successor method design

## Question

Why did MG1-v7 consume a disproportionate amount of Codex usage, and which prospective controls can reduce cost without weakening the frozen Agent Governance qualification or selection semantics?

## Evidence reviewed

Primary repository evidence:

- `handoffs/T023-executor-handoff.json` at submitted v7 HEAD `6e126d0a978a5ab1e306889f1f6333dbc98b21bb`;
- v7 raw attempt records and metrics under `evals/skill_activation_topology/evidence/mg1-v7-codex-windows-gpt-5.6-sol-medium/`;
- `docs/tasks/T046-mg1-v7-stimulus-isolated-evaluation.md`;
- `evals/skill_activation_topology/oracle.json` v7;
- `evals/skill_activation_topology/corpus.json` v3;
- Executor harness at the submitted v7 branch.

External documentation/research consulted:

- OpenAI Codex CLI developer commands: https://developers.openai.com/codex/cli/reference
- OpenAI Codex configuration reference: https://developers.openai.com/codex/config-reference
- OpenAI GPT-5.6 model guidance: https://developers.openai.com/api/docs/guides/latest-model
- GPT-5.6 Sol model reference: https://developers.openai.com/api/docs/models/gpt-5.6-sol
- Ofir Arviv et al., *Stop Guessing When to Stop Testing: Efficient Model Evaluation with Just Enough Data*, Findings of ACL 2026: https://aclanthology.org/2026.findings-acl.43/
- Shiyu Ji et al., *Seer Self-Consistency: Advance Budget Estimation for Adaptive Test-Time Scaling*, Findings of ACL 2026: https://aclanthology.org/2026.findings-acl.2120/
- *When More Thinking Hurts: Overthinking in LLM Test-Time Compute Scaling*, Findings of ACL 2026: https://aclanthology.org/2026.findings-acl.1199/

## V7 observed cost shape

The v7 handoff records:

- 171 valid acceptance repetitions;
- 11 explicit capacity events;
- 182 distinct Codex threads and 182 disposable workspaces;
- 160 mandatory Stage-R repetitions plus 11 conditional B1 thirds;
- zero non-capacity retries after a valid result;
- no Stage-C calls because no single-family reference qualified under the frozen v7 scoring result.

Therefore the dominant cost was not Executor conversational overhead or local deterministic testing. It was the repeated cost of bootstrapping a complete isolated Codex session for each model observation.

## Per-session amplification discovered in raw traces

Inspected raw v7 attempts show two avoidable cost amplifiers.

### 1. Unrelated app/plugin catalog material

Each inspected session began with Codex MCP resource discovery and received a substantial catalog of unrelated integrations/plugins such as Canva and default artifact templates. None of those tools were required by the activation-topology experiment.

Current Codex configuration documentation states:

- `features.apps` enables app/connector integrations and is on by default;
- `features.remote_plugin` enables the remote plugin catalog and is on by default;
- `features.multi_agent` enables collaboration tools and is on by default;
- `web_search` defaults to `cached` unless explicitly disabled;
- `features.skill_mcp_dependency_install` is on by default.

The v7 harness used `--ignore-user-config`, but that only suppresses `$CODEX_HOME/config.toml`; it does not by itself disable default runtime features.

### 2. Repeated policy-rejected Skill-body reads

Inspected v7 sessions show the model trying multiple ways to read the local candidate `SKILL.md` body (`Get-Content`, `rg`, `cmd /c type`, etc.), with those command executions rejected as `blocked by policy`.

This is important for both cost and validity:

- repeated failed tool attempts extend reasoning/tool loops and consume additional context/output;
- v7 scoring required successful host-observable candidate-body read/use before counting an activation;
- the harness continued the acceptance corpus without first proving that the required host-read path was operational under the selected execution policy.

The Codex CLI reference distinguishes two separate controls:

- `--ignore-user-config`: do not load `$CODEX_HOME/config.toml`;
- `--ignore-rules`: do not load user or project execpolicy `.rules` files.

V7 used the former but not the latter.

The configuration reference also states that `features.shell_snapshot` is on by default. V7 emitted a PowerShell shell-snapshot warning in inspected attempts because that snapshot mode was not supported in the observed Windows shell. Disabling an unsupported startup feature is a small but deterministic cleanup opportunity.

## Host-observability conclusion

V7 cannot be used to attribute zero host-observed activation to the candidate presentations alone.

The experiment intended to distinguish metadata discovery from candidate-body activation. Instead, the live cell was allowed to run while the required candidate-body read path was repeatedly rejected by host policy. A valid successor must fail closed before the acceptance corpus whenever it cannot prove the exact observability mechanism it plans to score.

This is classified in `docs/reviews/T023-R6.md` as `BLOCKED / HOST EXECUTION ENVELOPE DEFECT`, not a semantic oracle defect and not accepted evidence that B0/B1 intrinsically fail to activate.

## Decision-preserving session-count reduction

The v7/v6 selection method already made Stage C conditional on a qualifying B0/B1 reference. A further exact reduction is available: stop an individual candidate as soon as qualification or material-challenger status becomes mathematically impossible under the frozen thresholds.

This is not statistical guesswork. It is an optimistic-completion proof: assume every unscheduled remaining case is perfect for the candidate. If the final threshold still cannot be met, no future observation can change that candidate's admissibility.

### Exact examples under the 40-case design

The current semantic class distribution gives 11 negative/near-miss cases. With a false-activation maximum of 0.05, one finalized false-activation case implies `1 / 11 = 0.0909`, so qualification is already impossible.

Overall semantic accuracy must be at least 0.95 over 40 case aggregates. Three finalized semantic errors imply a best possible final accuracy of `37 / 40 = 0.925`, so qualification is already impossible.

Cross-profile violations and ambiguous permission broadening are mandatory zero-tolerance conditions. One valid repetition violating either boundary immediately disqualifies the candidate; remaining calls for that candidate cannot restore qualification.

Activation recall can be handled generically rather than by hard-coded counts: after each completed case aggregate, compute the maximum possible final recall by crediting every unscheduled expected entrypoint as a future true positive. If that optimistic recall is below 0.95, stop the candidate.

The same optimistic-completion method applies to precision, wrong-specialist rate, overactivation rate, and overall semantic accuracy using their frozen denominators.

For Stage C, once the reference metrics are final, a challenger may also stop when even optimistic completion cannot satisfy the frozen material-advantage requirements. Context can be bounded conservatively by treating every remaining activation-relevant case as zero bytes; if the best possible final median still exceeds the permitted reference ratio, material advantage is impossible.

### Literature support

Arviv et al. (ACL 2026) argue that fixed-size evaluation wastes compute when the decision is already resolved, and demonstrate sequential-testing designs that substantially reduce evaluation cost while maintaining a predeclared reliability criterion. MG1 can use an even stronger form for several gates because the relevant stopping rules are deterministic consequences of already-frozen thresholds rather than estimated significance boundaries.

## Prospective minimal Codex surface

A successor acceptance run should use a minimal effective host configuration while preserving the local Skill mechanism being tested.

Required effective controls proposed for v8:

- ignore user config;
- ignore execpolicy `.rules` for the isolated synthetic/acceptance workspace;
- keep the local shell/Skill mechanism enabled;
- disable Apps/connector integrations;
- disable the remote plugin catalog;
- disable multi-agent collaboration tools;
- disable automatic Skill MCP dependency installation;
- disable unsupported PowerShell shell snapshot behavior;
- disable web search;
- use ephemeral sessions and isolated OS-temporary workspaces as in v7.

The exact adapter syntax remains Executor-owned under D054, but the effective configuration is material to experiment reproducibility and therefore belongs in the persisted method authority.

## Mandatory host-capability canary

Before any acceptance prompt, v8 should run a non-scored synthetic Skill canary under the exact intended host/model/effort/configuration surface.

The canary must prove all of the following:

1. local Skill metadata is discoverable;
2. the synthetic `SKILL.md` body can be successfully read/used;
3. the host trace can distinguish that body read/use from metadata discovery;
4. structured output succeeds;
5. there is no execution-policy rejection affecting the required read path;
6. no unrelated app/plugin catalog content is materialized into the run;
7. the workspace remains within the intended mutation boundary.

Use the least-permissive viable sandbox:

- test `read-only` first;
- only if the read path fails for sandbox/policy reasons after rules isolation, test `workspace-write` inside the disposable workspace;
- `workspace-write` is acceptable only when the synthetic canary proves no unexpected model-caused writes and the harness verifies that postcondition after every acceptance attempt;
- if neither profile passes reproducibly, stop before the acceptance corpus.

The canary contains no acceptance holdout prompt and no candidate presentation content. Capacity events during canary readiness do not become acceptance attempts.

## Token and tool-cost observability

V8 should persist per invocation, when exposed by the current Codex event stream:

- input tokens;
- cached input tokens;
- reasoning tokens;
- output tokens;
- total tokens;
- tool-call count;
- policy-rejected tool-call count;
- unrelated app/plugin resource bytes or count;
- duration;
- capacity-event status.

If exact token fields are not exposed by the installed Codex version, the harness should record that absence explicitly and retain the available duration/tool-call/context proxies. Lack of token telemetry alone should not force substitution of a different host/model.

Current Codex documents an experimental rollout-budget feature, but it is off by default and can inject budget tracking/reminders. Because the experiment is sensitive to model-visible behavior, v8 should not depend on that experimental feature for acceptance. Cost control should instead come from minimal context, host preflight, exact early stopping, and a shorter fixed attempt timeout.

## Timeout

V7 allowed 600 seconds per model attempt. That ceiling permitted long tool-rejection loops in a classification/routing task whose required final output is small and structured.

V8 should prospectively reduce the timeout to 180 seconds per non-capacity model attempt. A host-observability/policy rejection detected by the harness should stop the epoch immediately rather than waiting for the timeout and should be classified as host-surface drift, not candidate behavior.

## Reasoning effort

OpenAI's current GPT-5.6 guidance recommends testing the current reasoning level and one level lower on representative workloads, and notes that `low` is appropriate for latency-sensitive workloads when tool use still matters.

However, changing the live-cell effort at the same time as host observability and sequential stopping would add another experimental variable. V8 therefore keeps GPT-5.6 Sol / Medium. A later independent non-acceptance calibration may evaluate Sol / Low before any future acceptance epoch if further savings are needed.

## Prompt caching

GPT-5.6 Sol supports discounted cached input. Disabling unrelated tools and stabilizing the fixed host prefix should improve cacheability naturally. V8 should record cached-input tokens if Codex exposes them, but prompt caching is treated as a secondary optimization, not as justification for retaining unnecessary context.

Priority order:

1. remove irrelevant context/tool surfaces;
2. prove the required host mechanism before acceptance;
3. stop exactly when the decision is mathematically irreversible;
4. then benefit from caching where available.

## Recommended v8 design

V8 should preserve:

- candidate presentation revision v3;
- B0/B1/F2/G3 topology semantics;
- zero-tolerance safety gates;
- numeric qualification thresholds;
- D050 reference/material-advantage selection percentages;
- case-level paired 2+1 aggregation;
- capacity pause/resume semantics;
- required live model GPT-5.6 Sol / Medium.

V8 should change prospectively:

- fresh holdout strings to avoid importing v7 observations;
- mandatory host-capability canary before acceptance;
- minimal effective Codex feature surface;
- 180-second attempt timeout;
- deterministic case-order groups chosen by decision consequence;
- qualification-impossibility and challenger-materiality-impossibility stopping;
- explicit cost/tool telemetry;
- immediate host-surface-drift stop when a required read path becomes blocked after a successful preflight.

The maximum theoretical observation count may remain the same as the paired 2+1 design, but it becomes a ceiling rather than a mandatory expenditure. When a candidate fails a decisive zero-tolerance or threshold-impossibility condition early, the remaining observations for that candidate are never scheduled.