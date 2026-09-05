# Portability Manifest

Status: SOURCE-SIDE EXTRACTION INVENTORY  
Source repository: `ManuelBouza/agent-governance`  
Source extraction baseline: `0e2edbca2cb0e620db7cdb7b93945bef8985fdfd`

This manifest classifies every source artifact and semantic rule selected into the dependency closure. Each entry has exactly one portability class.

Allowed classes:

- `PORTABLE`
- `ADAPT_REQUIRED`
- `SOURCE_ONLY`
- `EVIDENCE_ONLY`
- `DO_NOT_COPY`

Artifact classification describes how to treat the **source artifact itself**. Rule classification describes how to treat the **semantic rule extracted from source authority**. A source Decision document can therefore be `SOURCE_ONLY` while an extracted rule it authorizes is `PORTABLE`.

## Machine-readable manifest

```yaml
schema: agent-governance-transfer-bundle/v1
source:
  repository: ManuelBouza/agent-governance
  branch: develop
  extraction_baseline: 0e2edbca2cb0e620db7cdb7b93945bef8985fdfd
  checkpoint_sequence: O218
bundle:
  root: docs/transfer/source-maintenance-operating-model/
  normative_asset: PORTABLE-OPERATING-MODEL.md
classes:
  - PORTABLE
  - ADAPT_REQUIRED
  - SOURCE_ONLY
  - EVIDENCE_ONLY
  - DO_NOT_COPY
frozen_source_state:
  task: T058
  classification: DO_NOT_COPY
  state: BLOCKED/FROZEN_BY_HUMAN
  branch: feat/t058-chatgpt-portable-workspace-adapter
  remote_head: 6ed319a1802cfd90d50d9dc95d969435c295a164
  implementation_review_anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
```

## Bundle assets

| Bundle asset | Classification | Target treatment |
| --- | --- | --- |
| `README.md` | `PORTABLE` | Carry as adoption guide/provenance or translate into target-native onboarding. |
| `PORTABLE-OPERATING-MODEL.md` | `PORTABLE` | Semantic candidate for target adoption; not authority until target accepts it. |
| `PORTABILITY-MANIFEST.md` | `PORTABLE` | Preserve provenance/classification with target adoption records. |
| `EVIDENCE-APPENDIX.md` | `EVIDENCE_ONLY` | Retain as supporting provenance; never promote directly to target authority. |
| `UNRESOLVED-GAPS.md` | `PORTABLE` | Preserve the non-claims/gaps unless target explicitly qualifies them. |
| `TARGET-ADOPTION-CHECKLIST.md` | `ADAPT_REQUIRED` | Apply procedure using target's provider, branch topology and governance carriers. |
| `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md` | `ADAPT_REQUIRED` | Bind exact target repository/head/frontier before successor mutation. |

## Source artifact dependency closure

| Source artifact | Classification | Why / extracted treatment |
| --- | --- | --- |
| `AGENTS.md` | `SOURCE_ONLY` | Source repository operating authority. Do not copy wholesale; extract compatible semantics and map into target-native instructions. |
| `docs/orchestrator/CHECKPOINT.md` | `SOURCE_ONLY` | Mutable source frontier; target must use or create its own frontier carrier. |
| `docs/decisions/D022-source-product-change-procedure.md` | `SOURCE_ONLY` | Historical/source lifecycle authority; later refinements were semantically extracted, not copied as a target decision. |
| `docs/decisions/D027-orchestrator-chat-checkpoints.md` | `SOURCE_ONLY` | Source checkpoint decision; objective/cold-start semantics extracted separately. |
| `docs/decisions/D033-execution-access-control-plane.md` | `SOURCE_ONLY` | Source Decision ID must not become target authority; effect/target authorization semantics are extracted as portable rules. |
| `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` | `SOURCE_ONLY` | Source Decision ID stays provenance; runbook/adapter separation is extracted. |
| `docs/decisions/D041-executor-process-autonomy.md` | `SOURCE_ONLY` | Source Decision artifact; WHAT/HOW boundary extracted. |
| `docs/decisions/D042-remote-baseline-freshness-before-contract-load.md` | `SOURCE_ONLY` | Source Decision artifact; freshness-before-authority-load rule extracted. |
| `docs/decisions/D052-specification-owned-conformance-test-authorship.md` | `SOURCE_ONLY` | Source Decision artifact; semantic-oracle ownership rule extracted. |
| `docs/decisions/D053-native-spec-driven-development.md` | `SOURCE_ONLY` | Source Decision artifact; single-owner/delta-first SDD rules extracted. |
| `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md` | `SOURCE_ONLY` | Source Decision artifact; operation-resolution boundary extracted. |
| `docs/decisions/D055-executor-launch-session-and-compute-profile.md` | `SOURCE_ONLY` | Source policy artifact. Generic minimum-sufficient-compute idea may inform target; source model mappings do not transfer. |
| `docs/decisions/D057-research-decision-traceability.md` | `SOURCE_ONLY` | Source Decision artifact; evidence/decision separation extracted. |
| `docs/decisions/D058-executor-coordinator-session-and-worktree-hygiene.md` | `SOURCE_ONLY` | Source Decision artifact; coordinator/workspace isolation semantics extracted. |
| `docs/decisions/D060-task-scoped-executor-coordinator-continuity.md` | `SOURCE_ONLY` | Source Decision artifact; one-work-unit/one-root semantics extracted. |
| `docs/decisions/D061-orchestrator-branch-target-write-guard.md` | `SOURCE_ONLY` | Source Decision artifact; fail-closed topic-target rule extracted. |
| `docs/decisions/D062-repository-long-lived-branch-protection-bootstrap.md` | `SOURCE_ONLY` | Source Decision artifact; provider-neutral protection bootstrap extracted. |
| `docs/decisions/D063-qualified-codex-read-only-child-measurement-surface.md` | `SOURCE_ONLY` | Source/provider qualification artifact; no unconditional target child-provenance claim transfers. |
| `docs/decisions/D065-semantic-executor-delegation-obligation.md` | `SOURCE_ONLY` | Source Decision artifact; semantic delegation gate extracted. |
| `docs/decisions/D066-chatgpt-portable-git-workspace-transport.md` | `SOURCE_ONLY` | Source adapter decision; accepted workspace/lock semantics extracted, helper implementation excluded. |
| `docs/decisions/D067-objective-scoped-orchestrator-chat-lifecycle.md` | `SOURCE_ONLY` | Source Decision artifact; objective-scoped lifecycle/bootstrap mismatch semantics extracted. |
| `docs/decisions/D068-library-first-candidate-materialization-executor-verification-boundary.md` | `SOURCE_ONLY` | Source Decision artifact; current Stage 5/6/7 overlay extracted without forcing target ownership mapping. |
| `docs/LIBRARY-FIRST-SOURCE-MAINTENANCE.md` | `ADAPT_REQUIRED` | Strong operational source for the current flow; target paths/provider/Library/branch conventions must be mapped. |
| `docs/OBJECTIVE-SCOPED-CHAT-HANDOFF.md` | `ADAPT_REQUIRED` | Procedure is reusable in shape but target must bind its own frontier and bootstrap fields. |
| `docs/BRANCHING.md` | `ADAPT_REQUIRED` | Branch isolation/retirement intent can be reused; exact target branch topology must be discovered. |
| `docs/BRANCH-CLEANUP.md` | `ADAPT_REQUIRED` | Safe cleanup semantics may be reused; commands/worktree topology remain target mechanics. |
| `docs/LONG-LIVED-BRANCH-PROTECTION-RUNBOOK.md` | `ADAPT_REQUIRED` | GitHub procedure is a provider adapter; preserve semantic control but map provider labels/API. |
| `docs/EXECUTOR-SESSION-WORKTREE-HYGIENE.md` | `ADAPT_REQUIRED` | Source/Codex operating procedure; map target executor and local workspace conventions. |
| `docs/EXECUTOR-LAUNCH-PROFILES.md` | `ADAPT_REQUIRED` | Host/model mapping is volatile adapter configuration, not portable correctness policy. |
| `docs/TASK-CONTRACTS.md` | `ADAPT_REQUIRED` | Target may reuse/adapt existing task carrier rather than copy source schema. |
| `docs/OPERATION-CONTRACTS.md` | `ADAPT_REQUIRED` | Target may reuse/adapt existing operational carrier. |
| `docs/EXECUTOR-HANDOFFS.md` | `ADAPT_REQUIRED` | Evidence/handoff semantics transfer; exact schema/path belongs to target. |
| `docs/ORCHESTRATOR-CHECKPOINTS.md` | `ADAPT_REQUIRED` | Checkpoint semantics transfer; target carrier/path may differ. |
| `docs/RESEARCH-TRACEABILITY.md` | `SOURCE_ONLY` | Canonical source research ledger; target creates its own evidence disposition and keeps source references as provenance. |
| `docs/SPEC-DRIVEN-DEVELOPMENT-RESEARCH.md` | `EVIDENCE_ONLY` | Supporting SDD research; no direct target authority. |
| `docs/research/CODEX-PERSISTENT-EXECUTOR-COORDINATOR-RESEARCH.md` (R006) | `EVIDENCE_ONLY` | Historical positive same-task continuity evidence; broader cross-task recommendation superseded. |
| `docs/research/ADAPTIVE-SUBAGENT-COMPUTE-ROUTING-RESEARCH.md` (R007) | `EVIDENCE_ONLY` | Complete/deferred; constrains against copying unqualified worker compute routing. |
| `docs/research/CODEX-CHILD-OBSERVABILITY-SURFACE-RESEARCH.md` (R008) | `EVIDENCE_ONLY` | Provider/version-sensitive measurement evidence only. |
| `docs/research/CODEX-CHILD-SANDBOX-INHERITANCE-RESEARCH.md` (R009) | `EVIDENCE_ONLY` | Provider/version-sensitive sandbox evidence only. |
| R010 launch-profile research from the source research registry | `EVIDENCE_ONLY` | Complete/deferred; no target model migration follows. |
| `docs/research/CODEX-COORDINATOR-IDENTITY-WORKTREE-HYGIENE-RESEARCH.md` (R011) | `EVIDENCE_ONLY` | Supports coordinator/worktree decision; vendor syntax remains volatile. |
| `docs/research/CODEX-COORDINATOR-DELEGATION-POLICY-RESEARCH.md` (R012) | `EVIDENCE_ONLY` | Supports semantic delegation; research is not itself authority. |
| `docs/research/CODEX-TASK-SCOPED-COORDINATOR-CONTINUITY-RESEARCH.md` (R013) | `EVIDENCE_ONLY` | Supports task-scoped root continuity. |
| `docs/research/CHATGPT-GIT-WORKSPACE-AND-GITHUB-TRANSPORT-RESEARCH.md` (R014) | `EVIDENCE_ONLY` | Empirical local-Git/Library/GitHub transport and lifecycle evidence. |
| `docs/research/CHATGPT-GIT-WORKSPACE-LIBRARY-SNAPSHOT-LIFECYCLE-APPENDIX.md` | `EVIDENCE_ONLY` | Detailed R014 lifecycle receipts; not normative. |
| `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-RESEARCH.md` (R015) | `EVIDENCE_ONLY` | Historical worktree-simulator feasibility evidence. |
| `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-LOCK-LIFECYCLE-APPENDIX.md` | `EVIDENCE_ONLY` | Reusable sentinel/release/GC qualification evidence. |
| `docs/research/CHATGPT-LIBRARY-WORKTREE-SIMULATOR-CROSS-CHAT-RACE-APPENDIX.md` | `EVIDENCE_ONLY` | Real two-chat CAS race evidence; version/surface sensitive. |
| `docs/tasks/T058-chatgpt-portable-workspace-adapter.md` | `DO_NOT_COPY` | Frozen/unaccepted implementation contract. |
| `handoffs/T058-executor-handoff.json` on frozen T058 branch | `DO_NOT_COPY` | Frozen implementation evidence; not production authority. |
| T058 helper/code/tests on `feat/t058-chatgpt-portable-workspace-adapter` | `DO_NOT_COPY` | Human-frozen unaccepted implementation. |

## Extracted semantic rule classification

| Rule ID | Semantic rule | Classification | Target action |
| --- | --- | --- | --- |
| `P-AUTH-01` | Canonical remote Git/persisted target state outranks private chat/session memory. | `PORTABLE` | Adopt or map to target canonical authority. |
| `P-BOOT-01` | Successor cold-start verifies current canonical head, governing instructions, frontier and active work before mutation. | `PORTABLE` | Adopt with target-native paths. |
| `P-BOOT-02` | Material bootstrap mismatch fails closed; successor reports expected/observed/source/blocker and does not repair/reinterpret. | `PORTABLE` | Adopt. |
| `P-CHAT-01` | One Human-visible Orchestrator chat owns one explicit objective and does not execute the next material objective after closure. | `PORTABLE` | Adopt if target uses objective-scoped chat lifecycle. |
| `P-SDD-01` | Lifecycle stages have one accountable semantic owner; no dual-stage authority. | `PORTABLE` | Map target roles. |
| `P-SDD-02` | Brownfield specification is delta-first and reuses an adequate current spec carrier. | `PORTABLE` | Adopt/reuse target SDD. |
| `P-SDD-03` | Upstream requirement/design/acceptance defects cause Orchestrator re-entry rather than silent Executor redesign. | `PORTABLE` | Adopt. |
| `P-ORACLE-01` | Acceptance-oracle authorship follows semantic authority; tests/evals remain evidence. | `PORTABLE` | Map to target test ownership. |
| `P-EXEC-01` | Governance owns outcome/bounds/acceptance; Executor owns technical execution mechanics inside authority. | `PORTABLE` | Adopt. |
| `P-EXEC-02` | Operation syntax is resolved runbook/verified-recipe/authoritative-docs first and verified by semantic postconditions. | `PORTABLE` | Adopt; target adapter supplies commands/APIs. |
| `P-ACCESS-01` | Execution authorization is target/effect/privilege/credential/network oriented, not command-name based. | `PORTABLE` | Adopt or map to stronger target controls. |
| `P-BRANCH-01` | Normal automated mutation requires an exact verified short-lived topic branch; missing/stale target is STOP. | `PORTABLE` | Adopt with target branch topology. |
| `P-BRANCH-02` | A failed topic mutation must never fall back to a long-lived/default branch. | `PORTABLE` | Adopt. |
| `P-PROTECT-01` | Provider-supported long-lived branches require active PR/MR, deletion, non-FF/force-push and no-routine-agent-bypass protection before writable readiness. | `PORTABLE` | Reuse/adapt/establish target control. |
| `P-PROTECT-02` | Preserve stronger compatible target-native branch controls. | `PORTABLE` | Adopt. |
| `A-PROTECT-01` | GitHub ruleset labels/API/UI used by the source protection runbook. | `ADAPT_REQUIRED` | Replace with target provider implementation. |
| `P-COORD-01` | One complete Task/Operational Contract maps to one Human-visible Executor coordinator root; same task continues, new task starts new root. | `PORTABLE` | Adopt/map target work-unit carrier. |
| `A-COORD-01` | `AG | <repo> | <work-unit> | root-<n>` and host thread naming syntax. | `ADAPT_REQUIRED` | Use only if compatible with target host. |
| `P-DELEGATE-01` | Non-trivial coordinator evaluates semantic delegation triggers; eligible bounded work is delegated when no safety/overhead anti-trigger dominates. | `PORTABLE` | Adopt. |
| `A-DELEGATE-01` | Exact worker role names/count/model/spawn mechanics. | `ADAPT_REQUIRED` | Executor/target-host choice unless explicitly frozen. |
| `P-WORKSPACE-01` | Concurrent writable work units must have exclusive writable workspaces/topic branches. | `PORTABLE` | Adopt. |
| `P-WORKSPACE-02` | Unknown/unrepresented local work is preserved; cleanup does not destructively manufacture a clean state. | `PORTABLE` | Adopt. |
| `P-PORTABLE-01` | Canonical provider, local Git, persistent snapshot store and lock authority are distinct planes. | `PORTABLE` | Adopt if portable snapshots are used. |
| `A-LIBRARY-01` | ChatGPT Library as persistent snapshot store and its namespace/product operations. | `ADAPT_REQUIRED` | Revalidate or substitute target persistent store. |
| `P-LOCK-01` | Portable cross-chat ownership uses a coordination-only lock branch/namespace + expected-head CAS + owner sentinel. | `PORTABLE` | Adopt only with a target transport that qualifies equivalent semantics. |
| `P-LOCK-02` | Stale CAS failure is fail-closed and never an automatic retry-until-win loop. | `PORTABLE` | Adopt. |
| `P-LOCK-03` | Release requires exact current ownership/object identity and read-back proof of sentinel absence. | `PORTABLE` | Adopt. |
| `P-SNAPSHOT-01` | Portable snapshot is self-contained, includes real Git state and must pass integrity/identity/freshness/cleanliness validation before writable resume. | `PORTABLE` | Adopt if snapshots are used. |
| `P-SNAPSHOT-02` | Exact tree equality may verify represented content when connector-created commit identity intentionally differs. | `PORTABLE` | Use only when target transport exhibits equivalent commit-reconstruction behavior. |
| `P-PUBLISH-01` | Candidate publication rechecks exact remote topic freshness and verifies resulting head/tree/changed set. | `PORTABLE` | Adopt. |
| `P-PUBLISH-02` | Executor must load coherent authority/candidate from canonical Git, not chat-only/persistent-store-only state. | `PORTABLE` | Adopt. |
| `P-REPAIR-01` | Executor may diagnose/repair technical implementation defects inside approved semantics/design/plan. | `PORTABLE` | Adopt. |
| `P-REPAIR-02` | Requirement/public behavior/architecture/acceptance/new-risk/scope ambiguity is out of Executor repair authority and triggers durable re-entry. | `PORTABLE` | Adopt. |
| `P-RESYNC-01` | After Executor correction, retained persistent candidate must be rebuilt from exact canonical final state and validated before acceptance. | `PORTABLE` | Adopt when persistence is used. |
| `P-GC-01` | Snapshot deletion requires positive merge/integration + target refresh/promotion/revalidation; ambiguity retains prior state. | `PORTABLE` | Adopt when persistence is used. |
| `G-LOCK-01` | Crash/orphan recovery, TTL/heartbeat, automatic stale-lock reclamation and ownership transfer. | `DO_NOT_COPY` | No accepted automatic solution exists; target must design/qualify if needed. |
| `G-GC-01` | Automatic quota-pressure snapshot selection. | `DO_NOT_COPY` | Unqualified; target must not infer it. |
| `G-ROUTING-01` | Source-wide automatic child model/reasoning routing from deferred research. | `DO_NOT_COPY` | No adopted source rule exists. |
| `P-RESEARCH-01` | Research/experiment evidence never silently becomes normative authority; disposition is explicit and volatile facts are revalidated. | `PORTABLE` | Adopt. |
| `S-T058-01` | T058 implementation/helper as production workspace adapter. | `DO_NOT_COPY` | Frozen/unaccepted. |
| `S-SOURCE-01` | Source `AGENTS.md`, source checkpoint sequence, source D/R numbering and source branch names as target policy. | `SOURCE_ONLY` | Preserve only as provenance. |

## Provenance rule

The target may retain references such as:

```text
source_repository: ManuelBouza/agent-governance
source_extraction_baseline: 0e2edbca2cb0e620db7cdb7b93945bef8985fdfd
source_artifact: docs/decisions/D066-chatgpt-portable-git-workspace-transport.md
```

but must create its own authority identifier and acceptance record.

## Classification invariant

If an item appears both as a source artifact and as an extracted semantic rule, the two rows classify different objects:

- the **source artifact** remains source provenance;
- the **semantic rule** is the portable/adaptable candidate.

No source Decision or Research ID is promoted into target authority by this manifest.
