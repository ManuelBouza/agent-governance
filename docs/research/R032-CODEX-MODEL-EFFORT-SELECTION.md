# R032 — Codex Model and Effort Selection by Determinism, Technical Branching, and Verifiability

Research-ID: R032  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-17  
Last-Reviewed: 2026-09-17  
Owner: ChatGPT Orchestrator  
Scope: Human-visible Codex Executor root model/reasoning selection under D055; no child-routing adoption, no T066/T068/T069 mutation  
Question: How should Agent Governance choose the minimum-sufficient Codex model and reasoning effort from the technical shape of the work rather than treating Sol/Medium as an undifferentiated default?  
Evaluation-Refs: D055; R007/T063; R010; no new provider trial in R032  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Context

D055 already establishes the correct governing objective: recommend the lowest-cost/lowest-effort Executor configuration that retains a reasonable quality margin for the actual technical risk. `docs/EXECUTOR-LAUNCH-PROFILES.md` currently maps read-only/repetitive work to Luna/Low, narrow mechanical implementation to Terra/Low, ordinary Agent Governance implementation/rework to Sol/Medium, and complex/high-risk work to Sol/High.

The open question is not whether proportional compute is desirable. The question is how to classify a concrete work unit before launch so that `Sol / Medium` does not become a habitual default when the Orchestrator has already removed most semantic uncertainty and strong deterministic verification exists.

This research therefore distinguishes:

- **authority/specification completeness**, which is an Orchestrator gate and cannot be repaired with more model compute;
- **technical search burden**, which should drive model capability and reasoning effort;
- **verification strength**, which changes the cost of trying a lower tier safely;
- **risk/blast radius**, which can raise the minimum profile even when the implementation appears mechanically small.

## Current external evidence

### Official OpenAI evidence reviewed 2026-09-17

1. OpenAI, **Managing usage with GPT-6 Astra in Work and Codex**  
   `https://help.openai.com/en/articles/20001516`

   Current guidance explicitly says to choose model by task/capability needs and reasoning separately. It describes Astra as the most capable option for especially demanding work, Sol as a strong capability/efficiency balance, Terra as the everyday balanced option, and Luna as a fast economical option for focused or repetitive work. It also states that higher reasoning consumes more allowance and does not always produce a better result. The current article gives the important counterexample that a stronger model at lower effort can outperform a weaker model at higher effort; therefore model family and reasoning effort are not one scalar quality knob.

2. OpenAI, **The builder’s guide to GPT-5.6**  
   `https://openai.com/index/builders-guide-to-gpt-5-6/`

   The guide reports materially stronger price/performance at lower reasoning settings and gives production examples where Luna is effective for extraction, code retrieval/exploration, and repeated agentic steps. It also explicitly recommends moving deterministic filtering/aggregation/orchestration into code so model tokens are reserved for judgment. The durable implication is that deterministic work should not automatically inherit frontier reasoning capacity.

3. OpenAI, **A practical guide to building agents**  
   `https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/`

   The model-selection method is evidence driven: establish a capable quality baseline, then substitute smaller/faster models where evals show that the acceptance target remains satisfied. This directly supports a ratcheting policy rather than a fixed all-frontier default.

4. OpenAI API, **Models** and **Model guidance**  
   `https://developers.openai.com/api/docs/models`  
   `https://developers.openai.com/api/docs/guides/latest-model`

   Current model guidance treats `low` as efficient reasoning, `medium` as the balanced latency/performance point, `high` as appropriate for complex agentic work needing hard reasoning, and the highest modes as exceptional. The current catalog continues to separate Astra, Sol, Terra, and Luna by capability/cost role.

5. OpenAI Help Center, **GPT-5.6 and GPT-6 Pro in ChatGPT**  
   `https://help.openai.com/en/articles/20001354-gpt-5-6`

   Current guidance confirms GPT-5.6 availability in Codex from Codex CLI `0.144.0+` and Astra from `0.153.0+`, subject to account/workspace availability.

### D077 version-sensitive revalidation

The D055/R010 provider mapping was written before the current Codex stable release. Official `openai/codex` GitHub release metadata reviewed on 2026-09-17 reports:

```text
reference qualified/previously inspected surface: 0.153.x lineage
current stable:                            0.154.0
higher relevant prerelease observed:       0.155.0-alpha.16
```

Current OpenAI product/model documentation still exposes the same material selection dimensions used here: model family plus reasoning effort. No reviewed release evidence makes a specific Codex version a prerequisite for the classifier itself beyond the documented minimum model-availability floors.

D077 disposition for this research: **NO_MATERIAL_CHANGE** to the selection abstraction. Availability remains host/account/version checked at launch; R032 does not extend any D063-qualified measurement surface to newer Codex versions.

## Existing Agent Governance evidence

### D055 already supplies the normative principle

D055 says higher reasoning is not a remedy for incomplete specification and requires the minimum sufficient compute for accepted quality. R032 therefore does not need a new principle such as “always use smaller models first.” The missing layer is a more explicit classifier for when downshift is justified.

### R007 supports heterogeneous compute but T063 blocks overclaiming

R007 found strong official and external support for task-adaptive child compute. The subsequent T063 experiment did **not** qualify its exact frozen adaptive child mapping. T063 accumulated useful observations, but its prospective global/per-probe qualification gate became impossible and the mapping was closed as not qualified.

That history matters here in two directions:

- it rejects a claim that Agent Governance has already empirically proven a broad Luna/Terra routing policy;
- it does **not** reject D055’s proportional-compute principle or the narrower proposition that highly deterministic, strongly verified work can safely start below Sol when the task class is already justified.

R032 therefore recommends conservative, observable gates and evidence-driven ratcheting rather than a universal downshift.

### R010 remains valid

R010 deferred global Astra adoption. Current OpenAI guidance strengthens the reason to keep model family and reasoning effort separate, but it does not justify replacing Sol with Astra globally. Astra can consume Work/Codex allowance faster than Sol and remains a capability escalation, not a default.

## Core finding: technical search burden, not task importance, should drive compute

A task can be operationally important while technically deterministic. Conversely, a one-line change can hide a difficult concurrency, security, compatibility, or history problem.

The launch decision should therefore be based on four observable dimensions.

### 1. Authority completeness — hard gate, not a score

Before model selection, the Executor must have complete persisted authority for the work it is allowed to do. Missing requirement, Design, acceptance, semantic oracle, branch authority, or material scope is a D053/D068 re-entry condition.

```text
material authority ambiguity
    -> STOP / Orchestrator re-entry
    -> do not compensate with Sol High, Astra, Max, or Ultra
```

Only after authority is complete does compute selection begin.

### 2. Execution determinism

`HIGH_DETERMINISM` means the technical action is substantially constrained by frozen authority and known repository mechanics: narrow metadata synchronization, exact schema/config projection, deterministic generation, read-only evidence collection, or a local change with an obvious implementation shape.

`LOWER_DETERMINISM` means the Executor must discover a materially non-obvious technical path, reconcile interacting invariants, or infer a solution from incomplete observability even though the semantic authority itself is complete.

Determinism is about technical execution, not whether the expected product behavior has been specified.

### 3. Technical branching factor

Technical branching is the number and plausibility of competing implementation/diagnostic paths the Executor must evaluate before it can converge.

Use qualitative classes rather than a pseudo-precise numeric score:

```text
LOW    one obvious path or tightly bounded choice
MEDIUM several plausible local approaches/causes
HIGH   multiple interacting hypotheses, non-local causes, architecture/history/security tradeoffs
```

This is **solution branching**, not Git branch count.

### 4. Verification strength

Verification changes the economics of a lower initial profile.

```text
STRONG
  fast deterministic tests/oracles directly cover the changed behavior and failures are attributable

MIXED
  useful tests exist but important behavior requires interpretation, integration evidence, or partial review

WEAK
  sparse/expensive/flaky/indirect observability, difficult environmental reproduction, or substantial judgment remains after tests pass
```

A strong oracle reduces the expected cost of trying a cheaper profile because insufficient work is discovered quickly and objectively. A weak oracle raises the model floor because silent false success is more expensive than an obvious failed test.

### Risk modifier

Regardless of the three dimensions above, raise the floor when the work contains a concrete high-risk modifier such as:

- subtle security or fail-closed bypass risk;
- concurrency/ordering/race behavior;
- difficult portability or environment interaction;
- repository-history reconciliation where represented work can be lost;
- wide blast radius across subsystems;
- weakly observable destructive/irreversible effects;
- difficult diagnosis with several surviving root causes.

“Important task” by itself is not a high-risk modifier.

## Proposed conservative launch classifier

This is a research recommendation, not yet accepted D055 policy.

| Work shape | Initial model | Effort | Reasoning |
| --- | --- | --- | --- |
| Read-only/repetitive; high determinism; low branching; strong verifier/postcondition | GPT-5.6 Luna | Low | The work mostly executes or checks a known procedure; failure is cheap and obvious. |
| Narrow tracked mutation; high determinism; low branching; strong deterministic verification; bounded/reversible blast radius | GPT-5.6 Terra | Low | A write deserves more margin than repetitive observation, but frontier search is unnecessary. |
| Bounded local implementation/refactor; high-to-medium determinism; low/medium branching; strong or mixed verification | GPT-5.6 Terra | Medium | Enough reasoning for ordinary implementation choices without paying the default Sol premium. |
| Ordinary multi-file implementation/rework; medium branching or mixed verifier; no exceptional risk | GPT-5.6 Sol | Medium | Preserve the existing D055 normal profile when the task is not clearly eligible for downshift. |
| High branching, weak verifier, non-local diagnosis, or any serious risk modifier | GPT-5.6 Sol | High | The technical search/assumption burden is the reason for additional reasoning. |
| Hardest end-to-end work where Sol/High has concrete insufficiency evidence, or capability rather than extra search depth is the limiting factor | GPT-6 Astra | Low/Medium initially | Escalate model capability before reflexively maximizing reasoning; raise effort further only with evidence. |
| Exceptional bound-testing / unresolved long-horizon work | strongest justified model | XHigh/Max/Ultra only when supported and evidenced | Highest modes remain exceptional and must identify the concrete marginal benefit sought. |

### Important asymmetry for writes

R032 does **not** recommend Luna as a general implementation model. Luna is the economy floor for focused/repetitive/read-heavy work and possibly trivial writes only after a task class is separately validated. For ordinary bounded tracked mutation, Terra is the conservative low-cost floor.

This preserves margin while still creating a meaningful downshift from the current habit of using Sol/Medium for any delegated implementation.

## Model and effort are separate escalation axes

The evidence does not support this mental model:

```text
Luna Low < Terra Medium < Sol High < Astra Max
```

as a single monotonic ladder.

A stronger model at lower effort can outperform a weaker model at higher effort. Therefore the Orchestrator should classify **what is missing** when a result is insufficient:

```text
insufficient capability / poor abstraction / cannot handle task breadth
    -> raise model class

right model class but too little search, edge-case checking, or diagnosis depth
    -> raise reasoning effort

missing authority/context/files/permissions
    -> repair the missing input or re-enter governance; do not raise compute
```

This prevents spending high reasoning effort on a model that is the wrong capability tier and prevents using Astra to compensate for absent information.

## Expected-total-work rule

The cheapest first call is not necessarily the cheapest accepted result.

A useful qualitative objective is:

```text
expected total work
  = initial model/effort usage
  + verification usage
  + P(insufficient result) * (diagnosis + retry/rework + review churn)
```

Agent Governance should minimize **accepted-result cost**, not initial-call cost. A Luna/Terra retry cascade can be worse than one correct Sol execution; conversely, paying Sol/High for deterministic work with a strong oracle wastes allowance without improving acceptance.

No fixed numerical retry probabilities are adopted by this research.

## Ratcheting policy recommended for later adoption

Concrete model mappings should evolve from observed task classes rather than anecdote.

### Downshift

A class may be downshifted when repeated evidence shows that the lower profile:

- passes the same deterministic acceptance/verification;
- does not increase review findings or rework materially;
- does not increase root/coordinator workload enough to erase savings;
- remains stable across representative instances of that class.

### Upshift

Upshift when failures are credibly attributable to technical reasoning/capability rather than missing authority, stale state, broken tooling, or unavailable permissions. Signals include:

- repeated wrong implementation choice despite complete authority;
- unresolved multiple-cause diagnosis;
- verifier findings spanning several subsystems;
- missed edge cases not explained by missing tests/specification;
- non-local security/concurrency/portability behavior.

Do not repeat indefinitely at the same insufficient tier.

## What R032 does not establish

R032 does not establish any of the following:

- that Luna or Terra are globally qualified replacements for Sol on Agent Governance implementation;
- that T063’s failed adaptive mapping should be reused as root-routing policy;
- that Astra should replace Sol as the default;
- that higher reasoning always improves quality;
- that lower reasoning always reduces total accepted-result cost;
- fixed token, message, runtime, or monetary thresholds;
- a provider-independent permanent mapping from semantic task classes to current OpenAI model names.

## Recommended normative direction

If the Human chooses to adopt this research, the smallest compatible normative change is **not** to rewrite D055. A successor decision should refine D055 with an explicit pre-launch classifier:

```text
1. authority complete? otherwise re-enter
2. classify execution determinism
3. classify technical branching
4. classify verification strength
5. apply concrete risk modifiers
6. choose minimum-sufficient model
7. choose reasoning effort independently
8. verify; escalate the deficient axis only when evidence warrants it
9. ratchet task-class mappings from accumulated project evidence
```

The existing provider mapping can then be updated so `Sol / Medium` remains the safe unclassified/default profile while Terra/Low or Terra/Medium becomes an intentional first choice for clearly bounded, strongly verified implementation instead of an exceptional one-off.

A global claim that ordinary Agent Governance implementation should generally move from Sol to Terra still requires project-specific evaluation. The classifier itself can be adopted conservatively without making that stronger empirical claim.

## Disposition

```text
Research-State: COMPLETE
Decision-State: EVALUATING
Decision-Ref: none
```

R032 finds that D055’s minimum-sufficient-compute principle remains sound, but the current operational mapping should be refined around **execution determinism + technical branching + verification strength + concrete risk modifiers**, with model and reasoning effort treated as independent axes.

The evidence is sufficient to specify a conservative classifier that preserves Sol/Medium as the fallback and permits bounded downshift when explicit gates are met. It is not sufficient to claim a globally qualified Terra/Luna replacement for ordinary implementation without additional Agent Governance evidence.
