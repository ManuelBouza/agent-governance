# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O019  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

D032 deterministic verification is established by T003. The next authorized work unit is now planned as:

**T004 — D032 agent-facing capability eval foundation**

Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Planning branch:

`docs/t004-d032-agent-eval`

T004 is `READY` only after this Markdown planning branch is reviewed and merged into `develop`.

No executor may begin from a `develop` revision that predates the T004 contract.

## T004 Verification Decision

T004 covers model-dependent D032 behavior that T003 intentionally cannot prove mechanically.

The first baseline will:

- use realistic natural/technical/code-native user prompts;
- run repeated isolated agent sessions;
- preserve natural model responses rather than forcing JSON response schemas;
- use deterministic graders only for mechanical facts such as session isolation, zero tool calls, exact supplied-token preservation and record completeness;
- persist semantic-grading status as `PENDING_CHATGPT`;
- leave register fit, engineering-rigor equivalence, material-quality recognition/disclosure, diagram appropriateness/refresh and authority invariance to ChatGPT PD5 over persisted transcripts.

This is a capability baseline, not yet a stable-release numeric regression gate.

## T004 Primary Solution Diagram

Dominant design question: runtime interaction among corpus, eval harness, execution adapter, model and graders.

```text
T004 case corpus
     │
     ▼
Python eval harness
     │  creates clean trial + exact D032 system context
     ▼
Adapter boundary
     │
     ├─ OpenCode adapter (first execution adapter only)
     │    ├─ temporary config
     │    ├─ all agent tools DENY
     │    └─ explicit model + JSON event output
     │
     ▼
Fresh agent session ────────────────┐
     │                              │ multi-turn case only
     ▼                              │
User scenario                       │
     │                              │
     ▼                              │
Natural model response              │
     │                              │
     └──────── material redesign ───┘
                    │
                    ▼
         normalized trial record
         transcript + model/config
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
 mechanical graders    ChatGPT semantic PD5
 tokens/schema/tools   register/rigor/quality/
 session isolation     diagram/refresh/authority
```

OpenCode is only the first execution adapter. Case expectations and normalized records remain adapter-neutral.

## T004 Security Boundary

Security is `MATERIAL` because the eval invokes an external model through an authenticated agent host.

```text
                  TRUSTED SOURCE REPO
        D032 Core + T004 corpus (read-only input)
                         │
                         ▼
                Python eval harness
                         │
              copies only required text
                         ▼
┌──────────── DISPOSABLE TRIAL BOUNDARY ────────────┐
│ temp config + synthetic prompt                    │
│ OpenCode agent: all tools denied                  │
│ no repo writes · no shell · no web tools · no    │
│ Skills/plugins · no external-directory access     │
└───────────────────────┬───────────────────────────┘
                        │ model request
                        ▼
              EXTERNAL MODEL PROVIDER
              only synthetic eval content
                        │
                        ▼
                 response/events
                        │
                        ▼
              normalized JSONL evidence
                        │
                        ▼
                 source repo artifact
```

Child eval sessions must run outside the source worktree with deny-all agent tools and temporary configuration. Model-provider auth may be used only for model invocation; credentials/hidden reasoning must never be persisted.

## T004 Capability Corpus

Required families are persisted in the Task Contract:

- **A interaction-register invariance:** one avatar-upload scenario expressed as plain/domain, expert/architecture and code-native, with equivalent engineering controls/acceptance;
- **B silent baseline:** local draft-validation flow where non-material quality dimensions remain implicit instead of becoming checklist noise;
- **C material privacy/security:** sensitive customer CSV export crossing the platform boundary, expected to surface material implications and use a DFD with trust boundaries;
- **D diagram selection/refresh:** payment confirmation flow initially using dynamic/sequence, followed by a material redesign adding queue/worker that must invalidate stale readiness and refresh the diagram.

Run count: 3 independent trials per case/session, 18 independent sessions total and 21 user turns because D is multi-turn.

Semantic failures are evidence and must not be retried away.

## OpenCode Adapter Boundary

Current OpenCode documentation was checked during planning and supports the required shape: non-interactive `run`, JSON event output, explicit model/agent/directory/session options, custom agent prompts and deny permissions.

The executor must still preflight the installed version with read-only CLI help/version commands before implementation.

If current local OpenCode cannot provide explicit-model, clean-session, JSON-event, tool-denied execution without persistent global mutation, T004 stops `PARTIAL`; it must not update OpenCode or weaken isolation.

No OpenCode-specific behavior is part of D032 correctness semantics.

## Expected Committed T004 Surfaces

Only the minimum non-Markdown subset is authorized, expected to include:

- `evals/d032/cases.json`;
- small Python harness/record helpers under `evals/d032/`;
- one isolated OpenCode adapter under `evals/d032/`;
- `evals/results/d032/T004-baseline.jsonl`;
- `tests/test_d032_agent_eval_harness.py`;
- `handoffs/T004-executor-handoff.json`.

No new package dependency, production runtime, model-provider SDK, hosted eval platform, Docker, Node, Hypothesis, external SDD runtime or executor-authored Markdown is authorized.

## Quality-Envelope Summary

Material for T004:

- functional/measurement fidelity;
- adapter architecture/coexistence;
- security/isolation;
- reliability/repeated clean trials;
- bounded model-call resource use;
- observability/evidence;
- verification;
- maintainability/change isolation;
- portability;
- dependency/supply-chain discipline.

Privacy is baseline because prompts are synthetic. No production/business data may enter model trials.

## Completed State Entering T004

- canonical `develop` at T004 planning start: `ed148902c9b1285bd3e92278b3a50b6e69e1a469`;
- T003 implementation integration: `f52d3fb2bd148c37f6a0c6896b2c20fdaabbaba1`;
- T003 post-integration checkpoint: `ed148902c9b1285bd3e92278b3a50b6e69e1a469`;
- deterministic full-suite evidence from T003: `114 passed, 0 failed, 0 skipped`;
- D030 controls clone-local Gentle-AI RDD opt-out;
- D031 controls normal `.atl/` Skill Registry coexistence;
- D032 controls adaptive interaction, invariant engineering quality and Primary Solution Diagram readiness.

## Open Questions or Blockers

No known design blocker remains for T004.

Actual execution depends on an already-authenticated model being available through the local OpenCode adapter. Lack of model/provider auth is an execution blocker and must produce `PARTIAL`/`BLOCKED`, not a mock transcript.

The source product remains not stable/release-ready. T004 is the first D032 model-behavior baseline; broader Governance/Skill behavioral, state-machine, trigger, security and multi-adapter release gates remain incomplete.

## Next Action

1. Review `docs/t004-d032-agent-eval` against current `develop`.
2. Confirm the planning diff contains only `docs/tasks/T004-d032-agent-facing-capability-eval.md` and this checkpoint.
3. Merge the planning PR into `develop` if clean.
4. Verify T004 is `READY` on resulting `develop`.
5. Launch the executor on `eval/d032-agent-capability` with only the Task Contract pointer and normal D030/D031 source-maintainer constraints.
6. On handoff, perform remote PD5 over code, results JSONL and **actual persisted user-visible transcripts** before any implementation PR.
7. During PD5 distinguish:
   - acceptance of the eval harness/evidence package;
   - semantic pass/fail findings for D032 product behavior.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint, load only:

1. `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
2. `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`;
3. `governance-core/INTERACTION.md`;
4. `governance-core/QUALITY.md`;
5. agent-eval/release-gate portions of `docs/TESTING-AND-EVALUATION.md`;
6. `evals/README.md`.

Load T003 history only if a concrete deterministic-regression question requires it.

## Orchestrator Branching Incidents

Two prior accidental direct Markdown writes remain audit history and are not policy-compliant precedent:

1. T002-R1 placeholder: `6a3bff4f12850bd701fea624815e955231082afa`, corrected by `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`.
2. Architecture-overview placeholder: `a0e063344043fda53f55b8fcb5b03742a33a7185`, corrected by `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`.

No placeholder remains. T004 planning correctly created its topic branch before Markdown mutation.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not treat T004 capability execution as self-accepting semantic evidence.
- Do not add a model-as-judge dependency inside T004.
- Do not force the evaluated model to emit JSON instead of natural user-facing responses.
- Do not permit evaluated child sessions to use file/shell/web/Skill/subagent tools.
- Do not execute child trials inside the source worktree.
- Do not commit hidden reasoning, credentials or real customer/business data.
- Do not update or globally reconfigure OpenCode/Gentle-AI/provider tooling.
- Do not commit `.atl/` contents or treat Skill registry selection as Governance trust/approval.
- Do not re-enable or globally alter Gentle-AI RDD.
- Do not erase recorded branching incidents.
- Do not declare the source product stable/release-ready from T004 alone.
