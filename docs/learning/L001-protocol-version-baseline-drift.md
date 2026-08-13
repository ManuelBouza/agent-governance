# L001 — Protocol-version baseline drift

Learning ID: L001  
State: VERIFIED  
Fingerprint: `verification.regression.protocol_version_drift`

## Original detection

Detected during T008 executor verification at executor HEAD `59f0b8bc443636c5a7fbf5d417f185d528cc63e2` against base `bb1a2de8db622141fc975d1c341e82b9bdc4c3c6`.

At that base:

- `governance-core/GOVERNANCE.md` declared `Protocol-Version: 1.12.0`;
- `tests/_helpers.py` still declared `SOURCE_PROTOCOL_VERSION = "1.11.0"`;
- the deterministic suite was red independently of T008.

T009 corrected the test-side literal to `1.12.0`, removed a redundant fixed-literal assertion and restored the full suite. T008 subsequently replayed successfully on that corrected baseline, so L001 reached `VERIFIED`.

## Recurrence after VERIFIED

During D036/T010 planning on 2026-08-12, the Orchestrator prepared a Markdown-owned `GOVERNANCE.md` bump from `1.12.0` to `1.13.0` while the existing executor-owned helper still fixed `SOURCE_PROTOCOL_VERSION = "1.12.0"`.

The mismatching planning commit was:

`d1c584e2f1f73f08a3c6562afc362541e6b35873`

This reproduced the same failure class after L001 had reached `VERIFIED`.

The mismatch was detected during PR #73 review **before merge to `develop`**. The protocol bump/routing change was reverted on the planning branch in commit:

`b065fd5933243753204a3586a91b766bd495818a`

Canonical `develop` therefore remained green and stayed on Protocol `1.12.0`.

Under D039, same-fingerprint recurrence after `VERIFIED` is `CONTROL_FAILURE`. The historical T009 correction remains valid evidence for its specific incident, but its prevention control was not systemic enough.

## Revised causal/systemic analysis

The unstable element is not merely a missed literal update. It is the existence of a mutable current protocol version duplicated across two ownership domains:

```text
ChatGPT-owned Markdown Core current version
        +
executor-owned hard-coded current-version expectation
        ↓
manual cross-owner synchronization requirement
```

Because executable Task Contracts must be integrated before executor mutation and direct writes to `develop` are prohibited, an ordinary protocol bump can otherwise require a knowingly red intermediate canonical state.

That is a workflow/control-design defect, not a reason to normalize red `develop`.

## New selected control

D040 — `docs/decisions/D040-atomic-protocol-migration-and-single-version-authority.md` — supersedes literal synchronization as the systemic prevention model.

Core rule:

```text
Core Protocol-Version = single current-version authority

test helper = parser / validator / compatibility verifier
             != second current-version authority
```

Protocol changes crossing Markdown and executable ownership use a two-phase migration:

1. verification readiness while current protocol remains unchanged;
2. Markdown activation only after deterministic verification can consume the new state without a red intermediate baseline.

T010 was the first implementation of this stronger control while also establishing the D036 assurance-audit deterministic foundation. T011 completed active-routing readiness when the first Phase-B candidate exposed a remaining staged-only assumption.

## Containment and recovery execution

The first D040 Phase-B activation candidate, PR #81, was verified read-only by OP012 and correctly returned `BLOCKED` because focused/full pytest still encoded staged-only assurance routing assumptions. The candidate was not merged and no repository mutation was used to obtain PASS.

T011 then updated executor-owned deterministic verification without changing Markdown, Core semantics or the single current-version authority. Its accepted implementation derived required Assurance Core membership from Core routing and validated both historical STAGED state and ACTIVE Protocol `1.13.0+` state.

The clean Phase-B v2 candidate was rebuilt from current `develop` after T011 integration. OP017 verified exact candidate HEAD `43a783ff5e8f810eaa8cf62aedca482feedc71d3` with:

```text
MARKDOWN_ONLY: YES
FOCUSED_PYTEST: PASS
FULL_PYTEST: PASS
RUFF_CHECK: PASS
RUFF_FORMAT: PASS
REPO_MUTATION: NONE
```

PR #87 then merged exactly that tested candidate into `develop` as integration commit `85ccfac49e2e4a635f66c43fbedf95d54f7a6d29`.

The integrated state now has:

- `governance-core/GOVERNANCE.md` as the sole mutable current protocol-version authority;
- Protocol `1.13.0` active in Core;
- `governance-core/ASSURANCE.md` active/routed;
- deterministic verification green without an executor-side current-version synchronization edit;
- no second independently authored exact-current protocol-version authority.

## Recovery conclusion

The recovery requirements are satisfied:

1. D040 is integrated;
2. T010 removed the duplicated mutable current-version authority and introduced deterministic Core parsing/validation;
3. T010 passed focused/full/Ruff verification on staged Protocol `1.12.0`;
4. T010 was accepted, integrated and cleaned;
5. T011 corrected the remaining staged-only routing verifier and proved candidate composition without mutating the candidate;
6. OP017 proved the exact Markdown-only Protocol `1.13.0` activation candidate with all deterministic gates green and `REPO_MUTATION: NONE`;
7. PR #87 integrated exactly the tested candidate;
8. no second independent current-version authority was introduced.

Therefore L001 returns from `CONTROL_FAILURE` to `VERIFIED` under D039.

## Recurrence monitoring

Any later need to synchronize an independently authored exact-current protocol literal is the same control failure unless evidence establishes a materially different compatibility requirement.

A future protocol migration that cannot remain green under the D040 two-phase model must block and produce a new control/task correction rather than normalizing a red canonical intermediate state.
