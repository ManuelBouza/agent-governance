# R010 — GPT-6 Astra Executor Launch-Profile Research

Status: COMPLETE  
Research-State: `COMPLETE`  
Decision-State: `DEFERRED`  
Owner: ChatGPT Orchestrator  
Date: 2026-09-05  
Last-Reviewed: 2026-09-05  
Decision-Ref: none  
Controlling traceability: `docs/decisions/D057-research-decision-traceability.md`

## Research question

GPT-6 Astra became available during the T056 frontier. The narrow question is whether that vendor/model change should alter the already frozen Human-visible Executor launch profile for T056 or immediately replace GPT-5.6 Sol as the global D055 default/recommendation.

## Sources

Official OpenAI sources inspected on 2026-09-05:

- https://openai.com/products/release-notes/ — GPT-6 Astra release notes, 2026-09-03.
- https://openai.com/index/gpt-6-astra/ — launch/availability description.
- https://developers.openai.com/api/docs/models/gpt-6-astra — model capabilities and reasoning-effort support.
- https://developers.openai.com/api/docs/guides/latest-model — current model-selection/migration guidance.
- https://developers.openai.com/api/docs/models — current model catalog/selection guidance.
- official `openai/codex` source on current main, including explicit `gpt-6-astra` model support and bundled OpenAI-doc guidance.

Volatile availability/pricing/model-routing claims must be refreshed before a later normative adoption.

## Findings

### 1. Astra is an official current flagship model

OpenAI describes `gpt-6-astra` as its most capable model for the hardest end-to-end work, including complex reasoning, software engineering/coding, research and computer use.

Current API documentation exposes reasoning efforts:

```text
low
medium
high
xhigh
max
```

Astra does not support `none` reasoning effort.

### 2. Astra is not automatically the minimum-sufficient model for every Executor task

Current OpenAI model guidance still distinguishes task classes rather than prescribing uniform frontier allocation. Astra is the quality-first flagship; GPT-5.6 Terra remains the balanced quality/latency/cost option and Luna remains oriented toward faster/cost-sensitive work.

This is aligned with D055's existing minimum-sufficient-compute principle: a newly available stronger model does not itself justify raising every Executor task to that model.

### 3. Codex source has explicit Astra support

Current official `openai/codex` source contains explicit `gpt-6-astra` identifiers, model-catalog handling and migration guidance. Therefore Astra is a legitimate Codex-era model target where the installed Codex surface/account exposes it.

This source support is not equivalent to proving that every installed Codex version/account currently exposes Astra in its local model picker or provider catalog. Effective availability remains host/account specific.

### 4. T056 should not change from Sol to Astra

T056 is a narrow child-permission observability qualification. Its persisted Task Contract freezes the Human-visible root as:

```text
GPT-5.6 Sol / Medium
```

The root model is explicitly not an experimental variable.

Changing the root to Astra immediately before execution would add a model-family change to a qualification whose causal variable is the corrected child sandbox/profile surface. That would reduce comparability to T055 without improving the specific acceptance gate.

Therefore R010 supports **no T056 contract change**.

### 5. No global D055 Astra adoption is justified yet

Astra is materially more capable and may become the preferred model for some high-complexity Executor work. However, immediate global replacement of Sol would require a separate evaluation of at least:

- task success/quality at matched work units;
- latency and token/cost behavior;
- installed Codex availability and model-routing stability;
- whether Astra changes multi-agent behavior relevant to repository evaluations;
- which D055 risk classes actually benefit enough to justify higher compute/cost.

OpenAI's model guidance notes that Astra can sometimes complete difficult work with fewer output tokens despite higher per-token price, but that claim does not establish project-specific efficiency.

## Disposition

```text
Research-State: COMPLETE
Decision-State: DEFERRED
Decision-Ref: none
```

Current disposition:

1. Keep T056 at `GPT-5.6 Sol / Medium` exactly as persisted.
2. Do not amend D055 solely because Astra became available.
3. Astra may be selected prospectively for a future Task Contract when D055's minimum-sufficient-compute analysis justifies it.
4. A global/default migration from Sol to Astra requires a separate persisted evaluation or normative justification.

## Relationship to T056 version gate

Astra availability does not satisfy T056's host gate.

The Human reported on 2026-09-05 that the desktop ChatGPT surface is version `26.901.41600` and exposes Astra, while the normal PowerShell `codex --version` still reports:

```text
codex-cli 0.149.0
```

T056's installed Codex/App Server floor remains `>= 0.153.4`. The official latest stable `openai/codex` GitHub release inspected on 2026-09-05 is `0.153.4` (published 2026-09-04).

Desktop application build identity and Codex CLI/App Server version are separate facts; the former must not be used to bypass the latter's Task Contract gate.
