# D063 — Qualified Codex Read-Only Child Measurement Surface

Status: ACCEPTED  
Date: 2026-09-05  
Authority: Human Owner / ChatGPT Orchestrator  
Research: R008, R009  
Evaluation: `docs/tasks/T055-codex-child-observability-qualification.md`, `docs/tasks/T056-codex-read-only-child-requalification.md`, `docs/tasks/T057-codex-read-only-child-requalification-v2.md`  
Acceptance: `docs/reviews/T057-R1.md`

## Decision

Agent Governance accepts the Codex App Server read-only child observability surface exercised by T057 as a **qualified measurement substrate** for future bounded child-routing/evaluation work, subject to the version/capability and interpretation limits below.

The accepted surface is not a blanket statement about all Codex versions or every provider execution path. It is the supported protocol combination demonstrated on Codex/App Server 0.153.4 and revalidated by native schema/capability preflight at execution time.

## Qualified receipt set

A future evaluation may treat the measurement substrate as qualified only when the installed native surface provides and the run captures the semantic equivalent of all of the following for the same exact child:

```text
real parent/child correlation
parent activePermissionProfile.id == ":read-only"
continuous loaded-parent residency through child reattachment
child activePermissionProfile.id == ":read-only"
no contradictory broader supported legacy permission projection
requested child model/reasoning
resolved configured child model/reasoning
exact non-estimated child/turn token usage
exact child-turn duration
exact-child reroute signal/event observation
no tracked/global mutation attributable to the measurement procedure
```

The preferred permission provenance field is `activePermissionProfile`. Legacy `sandbox` remains a compatibility cross-check and must not contradict the qualified read-only profile.

## Parent-owned child reattachment invariant

For a parent-owned Multi-Agent V2 child, qualification depends on owner-controlled reattachment while the actual parent remains loaded in the same live App Server process.

The measurement harness must:

1. resolve the installed native `thread/loaded/list` response shape before provider-backed work;
2. verify the real parent ID remains loaded immediately before child reattachment;
3. reattach the exact child without permissions/sandbox/model/reasoning/cwd/approval/environment overrides;
4. preserve the actual parent-owned reload semantics of the installed supported surface.

Loss of parent residency or ambiguous child identity fails closed for the affected evaluation.

## Model/reasoning interpretation boundary

The accepted model/reasoning receipt is a **configured/resolved thread-state receipt**, not an authoritative provider-signed per-turn backend execution receipt.

Future evidence must distinguish:

```text
requested_profile
resolved_thread_profile
reroute_observed
backend_served_profile_verified
```

Unless a stronger supported provider receipt exists and is explicitly qualified later:

```text
backend_served_profile_verified = false
```

A matching resolved thread profile plus absence of `model/rerouted` may support a controlled claim about configured compute allocation. It must not be restated as proof that every token was served by that exact backend model/effort.

## Usage and duration boundary

Only server-reported, non-estimated usage attributable to the exact child thread/turn is accepted for quantitative evaluation.

Do not substitute:

- parent/root aggregate usage;
- estimated token counts;
- controller wall-clock timing;
- unrelated thread/turn timing;
- private SQLite/JSONL/rollout reconstruction as the primary passing receipt.

Repeated identical snapshots for the same exact child/turn are snapshots, not additive usage.

## Permission safety boundary

Qualification of the measurement substrate does not authorize write probing merely to prove denial.

For read-only child evaluation:

- select the parent with the supported built-in read-only permission profile;
- require the supported child `activePermissionProfile` provenance receipt;
- fail closed on missing/different profile identity or contradictory broader supported projection;
- verify no tracked mutation;
- do not intentionally attempt a write unless a separate security test explicitly authorizes that risk.

## Version/capability revalidation

This decision is version-sensitive.

Before relying on D063 in a future empirical evaluation, revalidate the installed host's native schema/help and required capabilities. Codex 0.153.4 is the qualified reference floor, not timeless schema authority.

Requalification or explicit review is required when a material change affects any of:

- permission-profile selection or `activePermissionProfile` lifecycle responses;
- parent-owned Multi-Agent V2 child reload/reattachment semantics;
- loaded-thread identity surface;
- child relationship discovery;
- token-usage attribution;
- exact turn timing;
- model/reasoning fields;
- reroute notification semantics.

If a later version removes or materially changes a mandatory surface, the evaluation must stop rather than silently relying on D063.

## Research disposition

D063 adopts the evaluated conclusions of R008 and R009:

```text
R008 Research-State: COMPLETE
R008 Decision-State: DECIDED

R009 Research-State: COMPLETE
R009 Decision-State: DECIDED
```

The canonical transition is recorded in `docs/RESEARCH-TRACEABILITY.md`.

Historical R008/R009 research bodies remain evidence of the questions and version-pinned analysis that led here; D063 and the registry carry the accepted current disposition.

## Relationship to R007

D063 clears the **measurement-substrate blocker** that prevented a corrected adaptive-subagent compute-routing evaluation.

It does not adopt routing policy and does not automatically reactivate R007.

R007 remains `DEFERRED` until ChatGPT Orchestrator persists a corrected successor evaluation that, at minimum:

- removes the T054 P2 shared task/oracle-semantics confound;
- uses a first-attempt-qualified requested->resolved child mapping;
- uses the D063-qualified measurement surface;
- preserves configured-vs-backend identity boundaries;
- defines its own acceptance and quantitative-claim limits;
- explicitly transitions R007 under D057 before execution.

## Relationship to D055 and model selection

D063 does not change D055 or the Human-visible Executor launch-profile policy.

T057's Sol/Medium root and Terra/Low child were experimental controls. Their successful observability is not a global recommendation that every future task or child use those profiles.

## No savings/cost decision

T057 established exact tokens and duration for one synthetic child turn. It did not establish a baseline comparison, cost model, quality tradeoff or savings estimate.

Therefore D063 adopts **no quantitative savings claim** and no routing-efficiency conclusion.

## Effective rule

```text
future child-routing evaluation
AND installed Codex native surface revalidates D063 mandatory receipts
AND exact child read-only/identity/usage/duration/reroute evidence is captured
=> measurement substrate may be treated as QUALIFIED

otherwise
=> fail closed / requalify before quantitative routing conclusions
```
