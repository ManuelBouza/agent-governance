# R029 — AGENTS.md / Skill Architecture Refactor Research

Research-ID: R029  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Opened: 2026-09-13  
Last-Reviewed: 2026-09-13  
Owner: ChatGPT Orchestrator  
Scope: source-product instruction/context architecture; root `AGENTS.md`, source Maintainer Skill, reusable transverse Agent Skills, and ChatGPT/Codex host adaptation  
Question: How should the current overloaded root `AGENTS.md` be decomposed so always-on governance remains safe while domain workflows and genuinely reusable cross-project capabilities use progressive-disclosure Skills without creating routing sprawl?  
Evaluation-Refs: none yet; this research defines the candidate decomposition and pre-decision evaluation requirements  
Decision-Ref: none  
Supersedes: none  
Superseded-By: none

## Status and authority boundary

This memo is research evidence only. It does **not** authorize:

- rewriting or slimming `AGENTS.md`;
- creating, renaming, packaging, installing, or releasing any new Skill;
- splitting the approved Maintainer Skill into role-named top-level Skills;
- changing D053/D068 stage ownership, D052 oracle ownership, D054 execution-mechanics ownership, D055 launch policy, D065 delegation semantics, D066 transport policy, or any other accepted decision;
- changing ChatGPT/Executor Markdown or source-code write ownership;
- launching Codex/an Executor, consuming provider/model calls, or beginning a qualification run.

The purpose is to establish a durable classification and a testable candidate architecture before any normative decision or implementation.

## Executive finding

The current root `AGENTS.md` mixes four different kinds of material:

1. **always-on authority and safety invariants** that must be visible before any Skill is selected;
2. **Agent Governance source-maintenance domain workflows** that belong to the Maintainer capability and can be progressively routed;
3. **cross-project operational workflows** whose intent is not specific to Agent Governance and are candidates for reusable transverse Skills;
4. **deterministic mechanics/reference detail** better represented by scripts, narrow references, CI, or host-specific adapters instead of repeated prose.

The evidence supports investigating this target shape:

```text
root AGENTS.md
  = repository identity
  + authority / ownership
  + hard safety invariants
  + cold-start bootstrap
  + short conditional routing rules

Maintainer Skill
  = Agent-Governance-specific source-maintenance dispatcher
  + Orchestrator/Executor role routes already approved by contract
  + domain-specific SDD / Task Contract / acceptance semantics

small transverse Skill set
  = only reusable capabilities with distinct intent and trigger boundaries
  + host-neutral semantic contract where possible
  + ChatGPT/Codex adapter/reference only where mechanics differ

references / scripts / CI
  = detailed procedures
  + deterministic checks
  + host/tool syntax
```

This is a **candidate architecture**, not an accepted design.

## Canonical repository baseline reviewed

Research baseline:

- `develop@35367824dd22b714bc07ce873656856788d85519`;
- root `AGENTS.md` at blob `dd2e2d814aee8f682bde54f6d5d0d462d7e1de87`;
- `docs/MAINTAINER-SKILL-CONTRACT.md`;
- `maintainer-skill/STATUS.md`;
- `docs/GOVERNANCE-SKILL-CONTRACT.md`;
- D057 research traceability;
- D066 ChatGPT portable Git workspace/transport;
- current O291 checkpoint.

The current Maintainer Skill contract is important: it intentionally defines **one top-level source-maintenance Skill with internal Orchestrator and Executor routes**. A new top-level source-maintenance Skill is permitted only after evidence demonstrates a distinct non-overlapping intent, measurable routing benefit, acceptable trigger separation, and an explicit architecture decision. R029 therefore does not propose top-level Skills merely because ChatGPT and Codex occupy different roles.

## External evidence reviewed

### E1 — OpenAI: Using skills to accelerate OSS maintenance

Source: https://developers.openai.com/blog/skills-agents-sdk  
Published: 2026-03-09; reviewed 2026-09-13.

Material findings:

- OpenAI's Agents SDK repositories keep repository policy in `AGENTS.md`, recurring workflows in repo-local Skills, and deterministic/supporting material in scripts/references or GitHub Actions.
- Skills use progressive disclosure: metadata first, full `SKILL.md` only after routing, then references/scripts only when needed.
- OpenAI explicitly recommends keeping `AGENTS.md` small and using it for rules that apply every time plus short conditional Skill triggers.
- Each Skill should have a narrow contract, clear trigger, and concrete output.
- `description` is part of the routing contract.

### E2 — OpenAI: Rethinking skills and prompts for GPT-6 Astra

Source: https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra  
Published: 2026-09-11; reviewed 2026-09-13.

Material findings:

- accumulated instructions in Skills, `AGENTS.md`, and task prompts should be re-audited as models improve;
- too many Skills and long descriptions consume the initial routing budget; Codex may shorten descriptions, which can reduce routing quality;
- overlapping or over-broad descriptions can cause incorrect Skill activation;
- a Skill with multiple workflows should use a minimal root router to supporting docs/scripts;
- always requiring broad documentation reads burns context and should be replaced by contextual routing;
- guidance must account for multiple models rather than overfitting one model generation.

### E3 — OpenAI: Build skills

Source: https://learn.chatgpt.com/docs/build-skills  
Reviewed: 2026-09-13.

Material findings:

- the same Agent Skill authoring format is supported by ChatGPT and Codex;
- both products begin with Skill `name` + `description` and load the full `SKILL.md` only after activation;
- Codex limits the initial Skill list to at most 2% of the model context window, or 8,000 characters when the context window is unknown; descriptions are shortened first and large catalogs may omit Skills from the initial list;
- implicit invocation depends on the Skill description, so descriptions require concise scope and trigger boundaries;
- OpenAI's current best practices say to keep each Skill focused on one job, prefer instructions over scripts unless deterministic behavior/external tooling is needed, and test prompts against descriptions.

### E4 — OpenAI: Custom instructions with AGENTS.md

Source: https://learn.chatgpt.com/docs/agent-configuration/agents-md  
Reviewed: 2026-09-13.

Material findings:

- Codex reads `AGENTS.md` before doing work;
- project instructions are concatenated through the directory hierarchy and are subject to a combined byte limit (`project_doc_max_bytes`, 32 KiB by default in the reviewed documentation);
- closer nested instructions override broader ones;
- OpenAI recommends concise rules and moving formatting/lint checks to CI where appropriate.

This supports keeping hard authority/safety constraints in the always-loaded chain while moving conditional workflow detail out of it.

### E5 — Agent Skills open specification

Source: https://agentskills.io/specification  
Reviewed: 2026-09-13.

Material findings:

- `name` and `description` are required discovery metadata;
- the full Skill body is loaded only after activation;
- supporting `scripts/`, `references/`, and `assets/` are on-demand resources;
- the specification recommends splitting long `SKILL.md` content into focused references, keeping the main Skill under 500 lines, and avoiding deep reference chains.

### E6 — AGENTS.md open format

Source: https://agents.md/  
Reviewed: 2026-09-13.

Material findings:

- `AGENTS.md` is intended as predictable repository guidance for agents;
- common content includes project overview, build/test guidance, conventions, and security considerations;
- nested `AGENTS.md` files are supported for narrower scopes;
- it is living project documentation, not a requirement to centralize every workflow in one root file.

### E7 — Martin Fowler / Thoughtworks: Context Engineering for Coding Agents

Source: https://martinfowler.com/articles/exploring-gen-ai/context-engineering-coding-agents.html  
Published: 2026-02-05; reviewed 2026-09-13.

Material findings:

- context engineering is the deliberate curation of what the model sees;
- Skills are a lazy-loaded context interface;
- excessive context can lower effectiveness and increase cost;
- always-loaded rules are best reserved for frequently repeated general conventions, while task-specific instructions/guidance can be loaded conditionally.

This is supporting specialized-industry evidence, not normative authority for Agent Governance.

## Durable synthesis

### Finding 1 — `AGENTS.md` cannot become only a pointer file

Some current root content defines authority before any Skill can safely run: repository identity, source-vs-consumer boundary, role/ownership boundaries, protected-branch behavior, cold-start authority, fail-closed rules, and the fact that Skills do not create governance authority.

If these are removed entirely from the always-loaded surface, correct behavior becomes dependent on successful Skill routing. That would invert the authority model and is not supported by the repository's existing invariants.

The target therefore is **lean root**, not **empty root**.

### Finding 2 — the Maintainer Skill remains the domain capability

The existing contract already contains the correct abstraction for work whose intent is “maintain the Agent Governance source product”. Its Orchestrator/Executor routes are role-aware progressive routing inside one domain Skill; they are not separate governance roles.

R029 finds no evidence for splitting that Skill into `chatgpt-orchestrator` and `codex-executor` top-level Skills solely by host/role. That would duplicate triggers around one domain intent and conflict with the existing contract absent new evidence.

### Finding 3 — transverse extraction must use capability intent, not host identity

OpenAI now uses one Skill format across ChatGPT and Codex. Therefore the default candidate pattern is:

```text
same intent + same semantic outcome
    -> one Skill
       -> host-specific reference/adapter only where mechanics differ

distinct intent / permission / trigger boundary
    -> separate Skill only after routing evidence
```

Portability does **not** grant authority. A Skill usable by both hosts remains constrained by the active repository role and persisted authority.

### Finding 4 — Skill count is itself a constrained resource

The extraction objective is not to maximize Skill count. Codex explicitly budgets the initial Skill catalog and may shorten or omit entries. Overlapping descriptions also damage routing.

Candidate transverse Skills therefore need all of:

- independent reusable intent outside Agent Governance;
- distinct trigger/anti-trigger boundary;
- useful output contract;
- measurable reduction in always-on/context duplication or operational error;
- no ownership ambiguity;
- no simpler representation as an internal reference/script of the Maintainer Skill.

### Finding 5 — deterministic mechanics should not become prose Skills by default

Where behavior can be implemented and verified deterministically, scripts/CI or narrow reference material are preferable to repeatedly loading procedural prose. The Skill should define when/why to invoke the mechanism and the required semantic postcondition.

This aligns with current repository policy: deterministic tests remain executable without Skill activation, and D054 keeps concrete execution mechanics on the Executor side.

## Complete semantic inventory of current root `AGENTS.md`

Classification vocabulary used below:

- `ROOT_INVARIANT` — must remain represented in the always-loaded root because it establishes authority/safety before routing.
- `ROOT_TRIGGER + DOMAIN_ROUTE` — keep a concise root invariant/trigger; route detail into the Agent-Governance Maintainer Skill or canonical domain references.
- `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` — keep the hard trigger/invariant at root; investigate a reusable cross-project Skill for the operational workflow.
- `DOMAIN_ROUTE` — detailed source-product workflow belongs to Maintainer/domain references; no independent transverse Skill is currently justified.
- `REFERENCE_OR_DETERMINISTIC` — detailed mechanics are better as references/scripts/CI and loaded only when required.

| Current semantic unit | Classification | Candidate disposition if later adopted | Rationale |
| --- | --- | --- | --- |
| Repository role / source-product vs consumer separation | `ROOT_INVARIANT` | Keep concise identity, allowed artifact classes, and prohibition on live consumer footprints at root | Must be known before any source mutation or Skill selection |
| Canonical product paths | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep only bootstrap-critical paths at root; full path catalog can move to Maintainer reference/router | Large path inventory is navigation context, not all-task authority |
| Binary operating model / Human + Orchestrator + Executor | `ROOT_INVARIANT` | Keep | Establishes authority independent of host product |
| D053 native SDD stage ownership | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep concise stage ownership and stop/re-entry rule; route profile/delta detail | Ownership must be always visible; workflow detail is domain context |
| D068 source-maintenance refinement | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep concise Stage 5/6/7 ownership boundary; route publication/detail | Critical ownership invariant, but current multi-paragraph procedure is conditional |
| D076 ephemeral executable materialization boundary | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep short material-vs-mechanical stop rule; route classification/evidence detail | Prevents authority loophole before Stage 6 tooling runs |
| D077 version-sensitive upstream revalidation | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` | Keep one trigger sentence; evaluate reusable `upstream-version-revalidation` capability | Method is broadly reusable beyond Agent Governance |
| D052 semantic oracle/test authorship boundary | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep ownership essence; route test/eval workflow detail | Authority must remain visible; mechanics are conditional |
| Human Owner authority | `ROOT_INVARIANT` | Keep | Ultimate authority cannot depend on Skill routing |
| ChatGPT Orchestrator / Markdown ownership | `ROOT_INVARIANT` | Keep, possibly compressed | Defines write authority and cold-start responsibility |
| Executor product-agnostic role and prohibitions | `ROOT_INVARIANT` plus `DOMAIN_ROUTE` | Keep authority/prohibitions; route enumerated Stage 6 workflow details | Prevents host identity from redefining role |
| D054 execution-mechanics ownership | `ROOT_TRIGGER + DOMAIN_ROUTE` with possible reusable adapter reference | Keep semantic-vs-mechanics split; route runbook resolution and syntax detail | Core authority is always-on; mechanics vary by task/host |
| D055 Executor launch profile | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` | Keep requirement that a launch profile exists; evaluate `executor-launch-handoff` workflow | Launch/session/model/effort preparation is reusable, but Agent Governance authority remains an adapter |
| D058 coordinator identity/worktree hygiene | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` / `REFERENCE_OR_DETERMINISTIC` | Keep collision/isolation invariant; evaluate whether workspace mechanics are a sub-route of repository change control rather than a separate Skill | Separate top-level Skill is not yet justified |
| Source-change procedure invariant | `ROOT_TRIGGER + DOMAIN_ROUTE` | Root keeps branch/PR and stage ownership summary; Maintainer route owns full Markdown/executable sequences | Source-maintenance-specific workflow |
| Persisted Task Contract / handoff invariant | `ROOT_TRIGGER + DOMAIN_ROUTE` with reusable handoff concepts | Keep persisted Git authority over chat and mandatory durable completion evidence; route full lifecycle/templates | Task Contract semantics are product-specific even if some handoff mechanics generalize |
| Orchestrator chat continuity invariant | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` | Keep cold bootstrap `develop -> AGENTS.md -> CHECKPOINT`; evaluate a generic durable-checkpoint capability with Agent Governance adapter | Durable work-frontier pattern can be reusable, exact checkpoint semantics are domain-specific |
| Research traceability invariant | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` | Keep `research != decision` and persist-before-rely; evaluate reusable research-evidence workflow | Generalizable provenance discipline, but current Rxxx/Dxxx registry is an Agent Governance adapter |
| Testing Skill/capability invariant | `ROOT_TRIGGER + DOMAIN_ROUTE` / `REFERENCE_OR_DETERMINISTIC` | Keep no-Skill correctness and Maintainer ownership boundaries; continue routing testing internally rather than creating generic testing Skills | Existing contract already rejects overlapping pytest/TDD Skill sprawl |
| Local development toolchain invariant | `REFERENCE_OR_DETERMINISTIC` plus minimal root safety | Keep only canonical toolchain/Markdown protection facts needed before execution; route detailed commands to Maintainer references | Tool syntax is task-specific and deterministic |
| File ownership invariant | `ROOT_INVARIANT` | Keep | Direct mutation authority cannot depend on Skill activation |
| Branching invariant | `ROOT_TRIGGER + TRANSVERSE_CANDIDATE` | Keep `main/develop` roles, no direct long-lived writes, topic branch + PR; evaluate reusable repository change-control workflow | Generic Git/provider safety workflow is strongly reusable |
| Product boundaries | `ROOT_INVARIANT` plus `DOMAIN_ROUTE` | Keep Core neutrality, source/consumer separation, Skills-not-authority, release-gate constraints; route detailed testing/supply-chain references | Product identity and authority boundaries must always apply |
| Change discipline | `ROOT_TRIGGER + DOMAIN_ROUTE` | Keep one-coherent-change / no mixed unrelated cleanup principle; route refactor characterization and D068 procedure | Detailed refactor workflow is source-product context |
| Progressive-context / no-duplication directive | `ROOT_INVARIANT` | Keep and make it architectural | It directly governs the desired instruction architecture |

### Inventory conclusion

No current major semantic unit is classified as “delete without replacement”. The refactor hypothesis is a **representation/routing change**, not a behavior-removal exercise.

The highest-value reduction comes from compressing root invariants to their decision-relevant core and replacing embedded procedures with conditional routes to canonical domain or transverse capabilities.

## Candidate transverse capability map

These are research candidates only. Names are provisional.

### 1. `repository-change-control` — strongest candidate

Reusable intent:

- establish repository and intended target identity;
- classify protected/long-lived vs topic branches;
- require freshness before mutation/publication;
- isolate writable work units;
- publish coherently and verify the remote result;
- fail closed on ambiguous target/ownership/freshness.

Potential adapters/references:

- ChatGPT/GitHub connector and portable-workspace semantics where qualified;
- Codex/native Git/worktree/CLI execution mechanics;
- provider-specific protection/PR mechanics only when relevant.

Why it should not become two host Skills by default: the semantic outcome is shared; only mechanics differ.

### 2. `upstream-version-revalidation` — strong candidate

Reusable intent:

- distinguish pinned/reference behavior from current stable upstream;
- inspect higher relevant releases/prereleases when necessary;
- record explicit retain/upgrade/requalify/no-material-change disposition before consequential reliance.

D077 is an Agent Governance instance of a broadly reusable engineering/research capability.

### 3. `research-evidence-traceability` — candidate

Reusable intent:

- assign stable research identity;
- separate research state from decision state;
- persist evidence before downstream reliance;
- preserve supersession history;
- revalidate volatile facts before promotion.

Agent Governance's `Rxxx`, `Dxxx`, registry and checkpoint formats would remain a project adapter/reference, not universal Skill semantics.

### 4. `durable-work-checkpoint` — candidate with a strong adapter boundary

Reusable intent:

- make a fresh session reconstruct the live work frontier from canonical state;
- record blockers, next permitted action and minimal next-session load;
- avoid private-chat history as authority.

The exact `docs/orchestrator/CHECKPOINT.md` schema and D027/D069/D080 rules remain Agent Governance-specific.

### 5. `executor-launch-handoff` — mixed candidate

Reusable intent:

- select new/continue session state;
- present model/reasoning configuration when applicable;
- transport only the minimal durable task authority;
- require durable terminal evidence.

The current Task Contract, ownership boundaries, launch-profile policy, and acceptance semantics are domain policy. A future transverse Skill must therefore expose adapter hooks rather than absorb those rules as universal semantics.

### 6. Workspace isolation as a separate Skill — not yet justified

D058/D066 worktree/lock/snapshot mechanics are reusable, but R029 finds insufficient evidence that users express a distinct intent that should route to an independent top-level Skill. Initial evaluation should treat workspace isolation as a route/reference inside `repository-change-control` or `executor-launch-handoff` and split it only if trigger/eval evidence demonstrates a distinct job.

## Capabilities that should remain internal/reference-first

R029 does **not** currently support top-level generic Skills for:

- `coding`;
- `testing` / `pytest` / `TDD`;
- `git-commands`;
- `markdown`;
- `branching` as a separate duplicate of repository change control;
- `code-health` merely because maintainability guidance is substantial;
- separate `chatgpt-orchestrator` and `codex-executor` Maintainer Skills.

These would be broad, overlapping, mechanically narrow, or already represented by Maintainer internal routes/references. The current Maintainer contract's testing and code-health approach remains the better baseline until trigger evidence says otherwise.

## ChatGPT / Codex duality

### Shared Skill contract

Current OpenAI documentation supports one Skill authoring format across ChatGPT and Codex. Therefore, the candidate design should define host-neutral semantics first.

Example:

```text
repository-change-control/SKILL.md
  minimal intent + trigger + semantic invariants + routing

references/chatgpt-github.md
  connector / GitHub / portable-workspace adapter where applicable

references/codex-git.md
  native Git/worktree/CLI adapter

scripts/
  deterministic validation only where portable and justified
```

The exact package layout is illustrative research, not implementation authority.

### Authority asymmetry remains

A shared Skill does not erase role boundaries:

- ChatGPT may use a capability during Orchestrator-owned work only within its repository authority;
- Codex/Executor may use the same capability only inside its authorized Executor envelope;
- a Skill may never turn a portable workflow into permission to edit Markdown, redesign requirements, accept work, bypass branch protection, or create consumer/source authority.

Thus **capability portability** and **governance authority** must stay separate dimensions.

## Proposed root `AGENTS.md` responsibility model for evaluation

A later candidate root should be tested against this responsibility set, not copied directly from this memo:

```text
1. repository identity / source-product boundary
2. canonical authority order (Git/GitHub; persisted authority over chat)
3. Human / Orchestrator / Executor role and write-ownership boundaries
4. concise D053/D068/D052/D076 stop/ownership rules
5. protected-branch / topic-branch / fail-closed mutation invariant
6. cold-start bootstrap from develop + AGENTS.md + checkpoint
7. Skills are operational tooling, never authority
8. short if/then routing table to Maintainer/transverse workflows
9. progressive-loading / no-duplication invariant
```

Everything omitted from this list is **not automatically removable**; it must remain reachable through the correct route/reference and be covered by preservation/eval gates.

## Pre-decision evaluation requirements

No architecture should be promoted from R029 directly. A later Human-selected evaluation/design objective should test at least:

### A. Preservation / authority

- every currently approved root invariant has an explicit retained location;
- no Skill becomes the sole source of normative authority;
- cold sessions still know enough to stop safely before any optional Skill activation;
- ChatGPT/Executor ownership remains unchanged;
- no D053/D068/D052/D054/D055/D065/D066 semantic migration occurs implicitly.

### B. Routing quality

For every proposed top-level Skill, create a trigger corpus with:

- explicit positive prompts;
- implicit positive prompts;
- negative prompts;
- near-miss prompts;
- overlap/collision prompts against other candidate Skills;
- host/role cases where the capability exists but authority forbids use.

Measure at minimum activation precision, activation recall, false-positive overlap and wrong-authority activation.

### C. Context efficiency

Compare baseline vs candidate:

- always-loaded root instruction size;
- initial Skill metadata catalog size;
- amount of task-irrelevant guidance loaded for representative workflows;
- number/depth of reference hops;
- whether Skill descriptions are shortened/omitted under realistic catalog size.

No fixed token target is established by R029. The goal is reduction without authority loss or routing degradation.

### D. Functional equivalence

Representative source-maintenance cases should prove that the candidate architecture can still correctly route:

- Markdown-only research/decision work;
- D068 Stage 5 materialization;
- Stage 6 Executor verification/repair;
- Task Contract/handoff creation and consumption;
- checkpoint/cold-start reconstruction;
- version-sensitive research;
- branch/protection/freshness-sensitive publication;
- testing/eval work without generic testing-Skill overlap.

### E. Cross-host behavior

Evaluate ChatGPT and Codex with the same semantic Skill where practical, while preserving their different execution surfaces and role authority. A host-specific top-level Skill requires evidence that a shared Skill plus adapters produces inferior or ambiguous routing.

### F. Deterministic validation

Before model-driven evaluation, use structural checks where possible for:

- Skill metadata/schema validity;
- duplicate/conflicting Skill names;
- reference existence and shallow routing;
- forbidden normative duplication;
- root-invariant coverage mapping;
- package inventory and supply-chain constraints.

Provider/model calls are not authorized by R029 and require a later selected evaluation objective.

## Candidate adoption gates

A later decision should require all of the following before implementation:

1. an explicit preserved-behavior map from every root semantic unit to root/domain/transverse/reference destination;
2. evidence that each new top-level Skill has a distinct trigger/job rather than merely a large body of prose;
3. a bounded Skill catalog whose metadata remains unambiguous under the documented Codex routing budget;
4. trigger/near-miss/collision evaluation for both relevant hosts/roles;
5. cold-start and wrong-authority safety evidence;
6. no-Skill fallback/bootstrap preservation where current contracts require it;
7. an explicit architecture decision identifying which candidates are adopted, rejected, merged, or kept as internal references;
8. only then, a separate implementation Task Contract/change set.

## D077 / volatility note

OpenAI Skill/AGENTS guidance is version-sensitive product documentation. R029 reviewed the current documentation on 2026-09-13, including the 2026-09-11 Astra guidance. No production decision is made here. Before a later consequential architecture decision relies on these vendor behaviors, D077 requires fresh relevance/version revalidation.

The durable parts of this memo are the classification method and repository analysis; numeric host limits, availability surfaces, and model-specific guidance are volatile facts.

## Research conclusion

R029 supports continued evaluation of a refactor from the current broad root instruction file toward:

```text
lean always-on AGENTS.md
+ one Agent-Governance-specific Maintainer Skill with existing role routes
+ a deliberately small set of capability-oriented transverse Skills
+ host-specific adapters/references only where mechanics differ
+ deterministic scripts/CI for deterministic behavior
```

The strongest first transverse candidate is repository change control; upstream version revalidation is also cleanly reusable. Research traceability, durable checkpointing and executor launch/handoff are plausible candidates but have stronger Agent Governance adapter boundaries and should be validated before promotion. Workspace isolation should initially be treated as a sub-route/reference rather than automatically becoming another top-level Skill.

The next permitted step is **evaluation/design selection**, not implementation. No Skill package or root `AGENTS.md` refactor is authorized by this research.