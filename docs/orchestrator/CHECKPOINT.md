# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O027  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — is terminal:

`CANCELLED_BY_HUMAN`

Controlling closure:

- `docs/reviews/T004-CLOSURE.md`
- `docs/decisions/D037-deterministic-code-only-verification.md`

The Human Owner explicitly discarded model-based tests and selected code-based verification as the repository verification policy.

Do not continue T004 R1/R2/R3, do not run more LLM/provider/OpenCode trials, and do not integrate the partial T004 implementation branch.

Historical last T004 executor state before cancellation:

```text
STATUS: PARTIAL
HANDOFF: handoffs/T004-executor-handoff.json
BRANCH: eval/d032-agent-capability
HEAD: eb20dc0fed2674190a82ef40aa0e02436c02ced4
```

Latest T004 implementation anchor reported under D029:

`edc7fe186c0c84f6f30e3a2d8bbb4022ac609356`

No real T004 capability baseline was ever produced: 0/18 sessions, 0/21 turns, no baseline artifact.

T004 remains historical/audit evidence only. No implementation PR is authorized.

## D037 — Deterministic Code-Only Verification

D037 is accepted architecture/policy.

Core rules:

```text
probabilistic implementation assistant != verification authority

source-product acceptance = deterministic evidence + authorized Human/Orchestrator judgment
```

Repository-owned verification and release gates use deterministic/mechanically reproducible evidence such as:

- unit/contract/regression tests;
- JSON/JSONL fixtures;
- deterministic test-local policy models;
- property/state-machine tests where justified;
- schema/version/provenance/identity checks;
- synthetic coexistence fixtures;
- static/security/dependency/configuration verifiers;
- runbook precondition/postcondition checks;
- bounded deterministic technical probes under future D033–D036 authorization;
- Human/ChatGPT review only for genuinely irreducible qualitative judgment.

Repository verification SHALL NOT require live LLM calls, repeated stochastic agent trials, model-as-judge graders, generated transcript scoring, provider/model availability, agent-host compatibility or statistical model-behavior release thresholds.

D037 supersedes earlier testing-strategy/task language that required or permitted live model/agent evals as source-product verification or release gates.

T003 is the accepted deterministic D032 verification foundation. D032 remains accepted architecture, but Agent Governance does not claim that arbitrary models have been empirically certified to exhibit D032 behavior.

## Accepted Architecture Frontier — D033 through D036

Accepted and not yet integrated into Governance Core/protocol:

- `docs/decisions/D033-execution-access-control-plane.md` — bounded execution authority;
- `docs/decisions/D034-runbook-first-terminal-neutral-execution.md` — runbook-first platform/terminal-neutral execution;
- `docs/decisions/D035-security-authority-freshness-and-independent-verification.md` — current security authority, freshness, known-bad regression and independent verification;
- `docs/decisions/D036-existing-system-assurance-audit-mode.md` — evidence-first assurance audits of existing systems.

Consolidated overviews:

- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`;
- `docs/ARCHITECTURE-SECURITY-VERIFICATION.md`;
- `docs/ARCHITECTURE-ASSURANCE-AUDIT.md`.

Future combined stack:

```text
D032 interaction/quality contract
        ↓
D035 current security authority/freshness
        ↓
D036 assessment / independent verification
        ↕
D033 execution authorization
        ↓
D034 runbook + terminal-neutral adapter
        ↓
deterministic/bounded technical evidence under D037
```

## Next Product Frontier

With T004 closed, the next work is to design the first deterministic Core/test integration of D033–D036.

Before any implementation scope becomes READY:

1. decide whether D033–D036 should be one coherent task or intentionally decomposed increments;
2. present a fresh D032 Primary Solution Diagram at the smallest useful abstraction;
3. perform D032 quality/security triage;
4. define explicit deterministic contracts/fixtures and fail-closed acceptance behavior;
5. preserve terminal/platform neutrality and runbook semantics;
6. ensure D035 security freshness/known-bad verification and D036 audit evidence/coverage semantics are mechanically testable where possible;
7. use Human/ChatGPT review for semantics that cannot honestly be reduced to code rather than adding a model grader.

The source product remains not stable/release-ready.

## Orchestrator Direct-Write Audit History

Preserve these incidents; do not hide or rewrite them without explicit Human authorization.

### T002-R1 placeholder

- accidental direct `develop`: `6a3bff4f12850bd701fea624815e955231082afa`
- corrective: `67d8dc6de9679f833f3136c6a66ee7ad05283cb3`

### Architecture overview placeholder

- accidental direct `develop`: `a0e063344043fda53f55b8fcb5b03742a33a7185`
- corrective: `09fa91f6b3c829e6edc0719fcd636cf3cba8f879`

### T004-R1 placeholder

- accidental direct `develop`: `197ce3fad02a69baf99238beb9859280a137a681`
- corrective: `52ae6fb5126517ea19c8d00918e7b148c17f146a`

### D037 placeholder

While implementing the Human Owner's code-only verification decision, ChatGPT accidentally created `docs/decisions/D037-deterministic-code-only-verification.md` with `placeholder` directly on `develop`.

- accidental direct `develop`: `71b62980c41b183dfb33ef3099c72fc827234606`
- corrective deletion restoring the prior tree: `e5ee3c56cbd17f72f876987550bab34cde065b53`

The proper D037 persistence uses `docs/d037-deterministic-code-only-verification` and the normal Markdown PR flow.

## Next Action

1. Integrate D037 + T004 closure + O027 through normal Markdown PR flow if the diff is Markdown-only and contains no unexpected paths.
2. Do not send any further T004 prompt to the executor.
3. Begin Strategy design for deterministic D033–D036 Core integration.
4. Produce a new Task Contract only after the Primary Solution Diagram and quality/security triage are complete.
5. Execute that future task with ordinary code tests and no model-facing eval dependency.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. load `docs/decisions/D037-deterministic-code-only-verification.md`;
2. load D033–D036 and their architecture overviews;
3. load `governance-core/EXECUTION.md`, `governance-core/QUALITY.md` and applicable lifecycle/security Core only as needed for the new integration design;
4. load `docs/TESTING-AND-EVALUATION.md` only to reconcile deterministic sections with D037 when authoring the next Task Contract or a later consolidation;
5. do not load T004/R1/R2/R3 unless a concrete audit/history conflict requires it.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not resume T004 without a new explicit Human Owner decision superseding D037.
- Do not integrate `eval/d032-agent-capability` as T004 product work.
- Do not introduce live LLM calls, model graders or probabilistic agent trials into source-product release verification.
- Do not claim deterministic fixtures empirically certify arbitrary model behavior.
- Do not make OpenCode, another agent host, a provider or model identifier a source-product release dependency.
- Do not weaken D035 independent security verification; use current authoritative controls plus technical evidence.
- Do not modify Core for D033–D036 before a separate READY Task Contract aligns semantics/code/tests.
- Do not hide/rewrite direct-write incidents without explicit Human authorization.
- Do not declare the source product stable/release-ready.
