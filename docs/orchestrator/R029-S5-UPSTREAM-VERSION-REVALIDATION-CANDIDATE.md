# R029-S5 — `upstream-version-revalidation` Candidate Evaluation

Status: COMPLETE  
Parent: `R029 — AGENTS.md / Skill Architecture Refactor Research`  
Subtask: `R029-S5 — upstream-version-revalidation candidate`  
Baseline-Develop: `9ca112699712a229db9b04cd1b34b0c38d53f7db`  
Inputs: accepted R029-S1 through R029-S4 artifacts; `docs/decisions/D077-version-sensitive-upstream-revalidation.md`  
Decision-State: EVALUATING  
Normative-Effect: none  
Analytical-Disposition: `KEEP_CANDIDATE`

## Purpose

Evaluate whether the engineering pattern behind D077 is sufficiently reusable and non-overlapping to remain a transverse Skill candidate. This artifact separates host-neutral upstream/version revalidation semantics from Agent Governance-specific qualification, decision, launch and pin policy. It does not create or adopt a Skill.

## Reusable semantic intent

The reusable intent is:

> Before consequential reliance on version-sensitive external behavior, identify the exact relied-on version, establish the current relevant upstream state, compare the exact behavior surface across relevant releases, and produce a bounded evidence-backed disposition about whether prior reliance remains valid.

This intent survives removal of Agent Governance-specific Decision IDs, Task Contracts, Codex qualification rules, launch gates, project pins and research registry semantics.

The candidate is not generic “check for updates” or dependency upgrade automation. Its purpose is to detect when a historical version assumption has become stale or materially misleading before that assumption controls consequential work.

## Positive triggers

Activate/evaluate this capability when all or most of the following are true:

- a design, workaround, test, launch, evaluation or compatibility conclusion materially depends on behavior of an external versioned tool/runtime/library/provider;
- an older pinned/reference version is being used as evidence for a current decision;
- a blocker or workaround may have changed in later upstream releases;
- qualification/reproducibility requires deciding whether to retain an older baseline or revisit it;
- upstream release state may have changed since earlier research and the result is about to be relied on consequentially;
- exact API/schema/source/behavior comparison is needed rather than a generic changelog summary.

## Negative triggers / anti-triggers

Do not activate merely because:

- a package has a newer version and no consequential conclusion depends on version-specific behavior;
- the user asks for ordinary dependency installation/update commands;
- the task is routine vulnerability patching governed by a separate security/update policy;
- a version number is mentioned only descriptively;
- no external versioned dependency materially controls the decision;
- the required action is simply “use latest” under an already-authoritative policy with no revalidation question;
- the task is general web research without a version-sensitive relied-on surface.

## Input contract

Minimum semantic inputs:

1. external dependency/provider identity;
2. exact reference/pinned version or historical state actually relied on;
3. material behavior/API/schema/source surface that matters;
4. consequential question the version evidence must answer;
5. any repository/domain authority that constrains permitted version movement or qualification.

If the relied-on version or material surface cannot be identified, fail closed rather than inferring a compatibility conclusion.

## Reusable method

A host-neutral execution should:

1. identify the exact reference version and why it matters;
2. establish the current stable upstream state from authoritative upstream evidence;
3. identify higher relevant releases needed to determine whether the material behavior changed;
4. include relevant prerelease evidence only when it materially informs an unresolved surface, while keeping prerelease status explicit;
5. compare the exact relied-on behavior/API/schema/source surface rather than relying solely on release-note wording when stronger evidence is available;
6. record versions/evidence inspected and the material conclusion;
7. distinguish evidence about upstream change from authority to upgrade, requalify, launch or accept;
8. return a bounded disposition to the calling domain.

## Generic output/postcondition

The capability returns durable evidence sufficient for the caller to know:

- reference version inspected;
- current stable version inspected;
- additional relevant versions/prereleases inspected;
- exact material surface compared;
- whether a material change exists;
- whether the historical relied-on assumption remains supported, is invalidated, or requires caller-owned re-evaluation;
- evidence provenance and freshness date/state.

A generic candidate may use neutral disposition terms such as:

- `REFERENCE_STILL_SUPPORTED`
- `MATERIAL_UPSTREAM_CHANGE`
- `REVALIDATION_REQUIRED`
- `NO_MATERIAL_CHANGE`
- `INSUFFICIENT_EVIDENCE`

These are workflow outputs, not authority to mutate the caller's baseline.

## Authority boundary

The candidate MUST NOT:

- decide that a project must upgrade unless project/domain authority delegates that decision;
- extend an existing qualification to a newer version automatically;
- treat a prerelease as production/experiment authority;
- redefine project pinning, compatibility, launch, acceptance or risk policy;
- silently replace the calling repository's version-selection rules;
- convert upstream evidence into normative project policy.

Repository/domain policy remains authoritative over what to do with the evidence.

## Agent Governance adapter boundary

The following remain Agent Governance-specific and stay inside the Maintainer/domain adapter:

- D077's exact `PIN_RETAINED`, `UPGRADE_REQUIRED`, `REQUALIFICATION_REQUIRED`, `NO_MATERIAL_CHANGE` vocabulary;
- D063 qualification of specific Codex measurement surfaces and the rule that qualification does not auto-extend to later versions;
- project-specific version pins and their experimental/reproducibility reasons;
- D057 research-to-decision traceability integration;
- stop/re-entry rules before consequential launch;
- launch/acceptance authority and any Task Contract/checkpoint consequences;
- the exact rule for when a materially new stable release becomes a project stop condition.

Thus the transverse capability supplies structured revalidation evidence; Agent Governance decides its governance consequence.

## Host/adaptor boundary

The semantic contract is host-neutral. ChatGPT and Codex/Executor may differ in how they obtain evidence:

- browser/web search versus repository/vendor documentation lookup;
- API/CLI/package-index/source inspection mechanics;
- local schema/source comparison tooling;
- how evidence is persisted into the calling repository.

Those mechanics belong in host/tool adapters. They do not justify separate ChatGPT and Codex Skills because the intent, trigger, authority boundary and postcondition are the same.

## Non-overlap with nearby candidates

- `research-evidence-traceability` owns general provenance/persistence/freshness of research evidence; S5 is narrower and activated by version-sensitive upstream state.
- `repository-change-control` owns safe repository mutation paths, not upstream semantic revalidation.
- `durable-work-checkpoint` owns resumable frontier state, not external version comparison.
- `executor-launch-handoff` may consume the S5 result before launch but does not own the version analysis.

S10 may later define routing between general volatile-fact refresh and this version-specific capability. S5 does not resolve that topology.

## Evaluation against transverse-candidate criteria

### Distinct user/task intent

Pass. “Revalidate this version-sensitive external dependency before relying on the old assumption” is distinct from generic research, upgrading or package management.

### Reusable across repositories/domains

Pass. The pattern applies to SDKs, runtimes, APIs, providers, libraries and tools independent of Agent Governance vocabulary.

### Clear trigger/anti-trigger boundary

Pass. Material dependence on version-specific external behavior is the trigger; generic update checking is excluded.

### Concrete postcondition

Pass. The caller receives an evidence-backed comparison and explicit material-change/revalidation status.

### Authority safety

Pass, provided the capability remains evidence-producing and domain policy owns upgrade/qualification/launch decisions.

### Host portability

Pass. ChatGPT/Codex mechanics differ, semantic contract does not.

### Context-efficiency case

Pass. Detailed comparison procedure and evidence discipline need not remain always loaded; a concise root/domain trigger can route here only when version sensitivity is material.

## Analytical disposition

`KEEP_CANDIDATE`

Rationale: the candidate has a distinct reusable intent, narrow activation condition, concrete evidence/postcondition contract, strong authority boundary and host-neutral semantics. D077 demonstrates the pattern but does not need to travel wholesale: Agent Governance-specific dispositions, qualification relationships and launch consequences remain in the domain adapter.

This disposition is research/evaluation only. It does not authorize Skill implementation or architecture adoption.

## Completion assessment

S5 completion gate is satisfied:

- reusable semantics are explicitly separated from D077/Agent Governance policy;
- positive and negative triggers are defined;
- input/output/postcondition and fail-closed behavior are defined;
- authority and host-adapter boundaries are explicit;
- overlap with adjacent candidates is bounded;
- analytical disposition is `KEEP_CANDIDATE`;
- no root rewrite, Skill implementation, provider/model call, Executor launch or T066 mutation occurred.
