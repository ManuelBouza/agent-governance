# R029 E2 — Empirical Disposition

Status: `COMPLETE_WITH_CHATGPT_PARITY_WAIVER`  
Evaluation: `R029-E2-HOST-PARITY-v1`  
Date: 2026-09-13  
Decision-State: EVALUATING  
Normative-Effect: none

## Human disposition

The Human Owner determined that running 36 separate clean ChatGPT UI sessions is not operationally practical and that the existing Codex empirical evidence plus provider-free evaluation is sufficient for the current pre-decision objective.

Accordingly, the remaining ChatGPT empirical half is **waived**, not passed.

This changes the E2 acceptance meaning prospectively from full paired-host empirical parity to a bounded evidence package consisting of:

- provider-free static authority/routing/context evaluation;
- 36 clean Codex Desktop trials rescored under Freeze D;
- zero Codex authority/safety violations;
- retained domain-routing signal (`agent-governance-source-maintainer` observed in 21/36);
- explicit acknowledgement that equivalent ChatGPT empirical routing has not been demonstrated.

## Evidence retained

Codex transverse result under Freeze D:

```text
trials                    36
PASS                      36
ROUTE_MISMATCH             0
INVALID_TRIAL              0
AUTHORITY_FAILURE          0
authority/safety violations 0
```

Historical provider/model consumption remains 37 calls: 36 persisted trial attempts plus one unscored adapter preflight.

The ChatGPT half remains:

```text
executed trials: 0/36
empirical parity claim: NOT ESTABLISHED
waiver reason: Human determination that required UI transport is impractical for this objective
```

## Interpretation boundary

This disposition supports only the following conclusion:

> The candidate transverse routing topology survived provider-free evaluation and the full Codex Desktop empirical corpus without a scored transverse routing or authority/safety failure.

It does **not** support these stronger claims:

- ChatGPT/Codex empirical parity was demonstrated;
- ChatGPT would reproduce Codex's 36/36 result;
- domain-route behavior is qualified;
- the candidate architecture is adopted for production;
- production root or Skill changes are authorized.

A future single ChatGPT conversation covering all 36 cases may be used only as a correlated smoke test. It cannot be represented as equivalent to 36 clean independent trials because within-chat history can influence later answers.

## E3 consequence

E3 may now proceed using the bounded evidence package above, but must carry the missing ChatGPT empirical half as an explicit residual uncertainty when judging decision readiness.

If E3 determines that production adoption materially depends on cross-host empirical equivalence, a future dedicated evaluation may restore paired ChatGPT evidence as a separate objective. This waiver does not prohibit that later work; it merely closes it as non-required for the current pre-decision objective.

## Preserved boundaries

- Freeze D remains historical evaluation authority and is not rewritten.
- Existing Codex evidence remains immutable.
- No ChatGPT trial is simulated or backfilled.
- No API result is substituted for ChatGPT UI evidence.
- R029 remains research/evaluation only.
- No production root/Skill adoption is authorized.
- T066 Stage 5 remains untouched.
- R030 remains research-only and unimplemented.
