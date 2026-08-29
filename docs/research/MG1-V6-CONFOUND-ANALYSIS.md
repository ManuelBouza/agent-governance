# MG1-v6 Activation-Eval Confound Analysis

Status: `COMPLETE / INPUT TO T046`  
Date: 2026-08-29  
Owner: ChatGPT Orchestrator  
Applies to: closed T023/MG1-v6 evidence and prospective T046/MG1-v7

## Question

Did MG1-v6 primarily demonstrate defective B0/B1 presentation discrimination, or did the live-eval method itself introduce context that could cause the measured activation and ambiguous-profile failures?

## Closed-v6 boundary

MG1-v6 remains closed exactly as reviewed in `docs/reviews/T023-R5.md`: neither B0 nor B1 qualified under the frozen v6 method and no topology was selected. This analysis does not rescore, mutate, or invalidate that result. It identifies confounds that must be controlled before attributing the observed behavior to candidate wording/topology alone.

## Finding 1 — in-band evaluation text induced candidate inspection

The v6 live prompt appended a long evaluator wrapper to every corpus prompt. The wrapper repeatedly included domain-bearing terms such as Agent Governance, Agent Skill, activation, routing, Consumer and source context.

In `HN01--B0--r1`, whose underlying request was generic SQL optimization, the model explicitly stated that it was consulting the Agent Governance routing Skill **because the turn was an activation evaluation**. It then read B0 `SKILL.md` and all three references, even though its final semantic conclusion was that the generic SQL request did not belong to the product capability surface.

This is direct evidence that the measurement instruction could itself trigger the behavior being measured.

`HN02--B1--r1` shows the same mechanism more narrowly: the model first emitted a no-activation judgment for the generic GitFlow comparison, then read B1 `SKILL.md`, and only after that read reported the router entrypoint as activated while still classifying the underlying request as no-activation.

## Finding 2 — filesystem location leaked source-product identity

V6 disposable workspaces were created beneath the canonical Agent Governance source checkout. Their absolute paths therefore contained `agent-governance` and the source worktree identity.

`HA03--B1--r1` was intended to withhold whether the checkout was canonical source or installed Consumer. Despite that, the model asserted that the checkout was the canonical Agent Governance source product, selected `source-maintainer`, read the source-maintainer reference and returned `activate` rather than `clarify-context`.

The user stimulus did not supply that role. The host environment did.

Because ambiguous-role behavior is a zero-tolerance gate, a path-level role leak is a material confound.

## Finding 3 — v6 still contains useful candidate evidence

The confounds do not explain every observation and do not license a passing reinterpretation of v6. B0/B1 may still be too permissive after the method is cleaned up. V6 remains useful diagnostic evidence that:

- both candidates preserved recall under the tested method;
- B1 reduced context relative to B0;
- B0's preload design makes any body activation expensive;
- B1 can route correctly on cross-profile boundaries when current context is explicit;
- the current candidate descriptions alone did not prevent all evaluator-induced inspection.

The correct next step is therefore **method isolation before presentation tuning**.

## V7 design consequence

T046/MG1-v7 MUST:

1. keep all candidate presentation/reference bytes unchanged;
2. use a fresh holdout with new exact prompt strings;
3. make the corpus prompt the only domain-bearing in-band natural-language stimulus;
4. reduce the added suffix to the neutral sentence `Return only the required structured record.`;
5. enforce read-only behavior through host mechanics rather than domain-bearing evaluator prose;
6. execute from a neutral OS-temporary root outside the source checkout;
7. give ambiguous/negative/near-miss cases no source or Consumer role fixture;
8. treat host-observable candidate-body read/use as scored activation, with model self-report only as a diagnostic cross-check;
9. retain v6 paired 2+1 scoring, reference-first staging, thresholds and safety boundaries unchanged.

## Decision

Do not redesign B0/B1 presentation text yet. First run a stimulus-isolated v7 acceptance epoch. If the same no-reference result persists, the evidence will then support a presentation/topology redesign without the two identified measurement confounds.
