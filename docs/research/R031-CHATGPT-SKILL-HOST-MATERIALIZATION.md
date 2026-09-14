# R031 — ChatGPT Skill Host Materialization

Status: COMPLETE  
Research-State: COMPLETE  
Decision-State: EVALUATING  
Owner: ChatGPT Orchestrator  
Observation-Date: 2026-09-14  
Canonical-Baseline: `develop@5bed8b952a3c552e3af0abfdbe07895864319696`

## Question

How should the R029/D082 Agent Governance Skill architecture be materialized in ChatGPT so that the canonical repository remains the semantic source of truth, host-specific packaging does not create a fork, and real ChatGPT activation can be qualified rather than inferred from repository structure alone?

## Scope

This research concerns ChatGPT host loading/installation and qualification of the already-adopted source-product architecture:

- one top-level `source-maintainer` Skill with internal Orchestrator/Executor routes;
- exactly five top-level transverse Skills:
  - `repository-change-control`;
  - `upstream-version-revalidation`;
  - `research-evidence-traceability`;
  - `durable-work-checkpoint`;
  - `executor-launch-handoff`;
- `workspace-isolation` remains subordinate under `executor-launch-handoff`.

It does not reopen D082 architecture, T067 acceptance, T066, or ChatGPT/Codex empirical parity.

## Sources and freshness

Primary current OpenAI sources reviewed on 2026-09-14:

1. OpenAI Help Center, **Skills in ChatGPT**, updated in September 2026: `https://help.openai.com/en/articles/20001066`.
2. OpenAI Academy, **Using skills**, published 2026-04-10 and current when reviewed: `https://openai.com/academy/skills/`.
3. OpenAI API Reference, **Skills / Create a new skill**: `https://developers.openai.com/api/reference/python/resources/skills/methods/create`.
4. OpenAI Help Center, **Plugins in ChatGPT and Codex**: `https://help.openai.com/en/articles/20001256/`.

Repository surfaces inspected at the same baseline:

- `maintainer-skill/SKILL.md` plus `maintainer-skill/references/`;
- `repository-change-control-skill/SKILL.md`;
- `upstream-version-revalidation-skill/SKILL.md`;
- `research-evidence-traceability-skill/SKILL.md`;
- `durable-work-checkpoint-skill/SKILL.md`;
- `executor-launch-handoff-skill/SKILL.md` plus its subordinate references.

## Observations

### O1 — ChatGPT now has a native Skill surface

Current OpenAI documentation describes Skills as reusable workflows containing instructions, examples/resources and optionally code. Once created and installed, ChatGPT can automatically use one or more relevant Skills; a Skill can also be selected explicitly.

This closes the historical host-capability question at the feature level: the Agent Governance source Skills no longer need to be simulated purely as project prompt text in an eligible ChatGPT workspace.

### O2 — ChatGPT supports direct Skill upload

The documented ChatGPT path is `Plugins -> Skills -> Create -> Upload from your computer`. Uploaded Skills are scanned before becoming available and may be accepted, marked `Needs Review`, or blocked.

Therefore installation is a host/workspace mutation and an explicit Human/workspace action. Git materialization alone cannot truthfully be called ChatGPT activation.

### O3 — Availability is account/workspace dependent

The current Help Center states that Skills are available to eligible ChatGPT Business, Enterprise, Healthcare and Edu users, subject to workspace settings and product availability. Workspace permissions may separately control Skill creation, upload, sharing and installation.

No repository artifact can override this host entitlement/configuration gate. The Human installation step must fail closed if the Skills surface or upload permission is unavailable.

### O4 — `SKILL.md` is the portable canonical playbook

OpenAI Academy documents `SKILL.md` as the Skill playbook and describes the format as portable/open-standard oriented. A Skill can include supporting resources and code. OpenAI recommends smaller composable building blocks rather than one monolithic Skill for complex workflows.

This is directly compatible with D082's one Maintainer domain Skill plus five composable transverse Skills. There is no evidence requiring these six semantic Skills to be collapsed into one ChatGPT-specific mega-Skill.

### O5 — Existing R029/D082 source layout is structurally aligned

All six adopted top-level Skills already have a root `SKILL.md`. The Maintainer Skill and `executor-launch-handoff` also contain required references; the remaining transverse Skills are currently single-file Skills.

No host-specific semantic fork is needed merely to make the source tree look like a ChatGPT Skill package.

### O6 — Packaging must preserve relative references

A ChatGPT upload can include supporting files. Therefore a host bundle must package each top-level Skill independently with its root `SKILL.md` and all files below that Skill directory while preserving relative paths.

For example, `source-maintainer` must include its `references/` files; uploading only `maintainer-skill/SKILL.md` would be incomplete because its Orchestrator/Executor routing explicitly loads Skill-local references.

### O7 — ZIP is explicitly supported by the Skills API; ChatGPT UI wording is less specific

The current OpenAI Skills API accepts either a directory upload or a single ZIP file. The ChatGPT Help Center says only `Upload from your computer` / upload a Skill and does not explicitly document the accepted archive/container shape.

A deterministic one-ZIP-per-Skill export is therefore a strong candidate distribution form, but ChatGPT UI ZIP acceptance remains a host gate to verify empirically rather than a fact to assume from the API alone.

### O8 — Canonical Git must remain authoritative after installation

An uploaded ChatGPT Skill is a workspace artifact and can drift from Git. Existing Agent Governance authority already states that Skills are routing/operational aids and that canonical Git state outranks host-native state.

Accordingly, the ChatGPT Skill package should carry provenance metadata and be reproducible from a specific Git commit, while source-maintenance runtime bootstrap continues to fetch current canonical `develop`, `AGENTS.md`, and `docs/orchestrator/CHECKPOINT.md` from GitHub. Installing a Skill must not snapshot repository authority into a competing authority plane.

### O9 — Installed availability and automatic routing are separate claims

Successful upload/scan proves only host availability. It does not prove automatic activation quality, anti-trigger behavior, internal route selection, transverse composition, or preservation of no-Skill fail-closed correctness.

Those claims require post-installation ChatGPT qualification using both explicit `@` invocation where supported and representative automatic-routing probes.

### O10 — This ChatGPT conversation does not currently expose the Agent Governance Skills as installed host Skills

The active environment exposes other installed plugin Skills, but the Agent Governance `source-maintainer` and five transverse Skills are not present in the installed Skill catalog available to this conversation. Repository reads in this chat are therefore not evidence of installed Skill activation.

## Analysis

The smallest host adaptation is packaging, not semantic rewriting:

```text
canonical source directories
    -> deterministic per-Skill bundle
    -> Human/workspace upload + scan
    -> installed ChatGPT Skills
    -> post-install qualification
```

The six top-level Skill boundaries should remain exactly the D082 boundaries. ChatGPT-specific mechanics should be limited to packaging/provenance and any narrowly necessary host adapter discovered during upload/qualification.

The Maintainer Skill must continue to treat GitHub/Git as authority. The transverse Skills should remain host-neutral semantic workflows. `workspace-isolation` must not emerge as a sixth upload package.

## Recommended implementation direction

1. Add deterministic packaging/validation for exactly six ChatGPT Skill bundles from the adopted source directories.
2. Preserve directory-relative resources and record source commit/provenance without rewriting Skill semantics.
3. Validate package topology deterministically before any host upload.
4. Use an explicit Human gate for ChatGPT upload/install because entitlement, permissions and scan outcome are host state.
5. After installation, run a bounded ChatGPT qualification covering:
   - each Skill explicit availability;
   - positive automatic-routing cases;
   - anti-trigger/near-miss cases;
   - Maintainer Orchestrator vs Executor route separation;
   - composition with the five transverse Skills;
   - confirmation that `workspace-isolation` is not a top-level Skill;
   - Git-authority/cold-start behavior;
   - no-Skill/fail-closed independence remains a repository invariant.
6. Do not relabel ChatGPT/Codex empirical parity from `NOT_ESTABLISHED` unless a separate authority explicitly defines and completes that comparison.

## Uncertainty / host gates

- The current user's exact ChatGPT workspace entitlement and Skill-upload permission are not observable from repository state and must be checked at installation time.
- The Help Center does not explicitly state whether ChatGPT UI accepts the same ZIP container accepted by the Skills API; verify rather than infer.
- Automatic Skill routing observability may differ by ChatGPT surface. Qualification must score observable behavior and explicit invocation where available, not hidden model internals.
- Host behavior is version-sensitive and should be revalidated before later consequential reuse if OpenAI materially changes Skills/plugin behavior.

## Disposition

Research is `COMPLETE`; normative/product adoption remains `EVALUATING` until T068 materializes reproducible bundles, passes deterministic package checks, crosses the Human ChatGPT-installation gate, and records post-installation qualification evidence.
