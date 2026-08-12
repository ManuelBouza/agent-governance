# L001 — Protocol-version baseline drift

Learning ID: L001  
State: CONTROL_FAILURE  
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

T010 is the first implementation of this stronger control while also establishing the D036 assurance-audit deterministic foundation.

## Immediate containment

- Do not merge the transient `1.13.0` mismatch from PR #73.
- Keep `GOVERNANCE.md` at `1.12.0` during T010 readiness work.
- Stage `ASSURANCE.md` without routing it as an active required Core module yet.
- T010 must remove the independent mutable current-version literal and prove the assurance semantics deterministically.
- Only after T010 is accepted/integrated/clean may ChatGPT activate `ASSURANCE.md` and bump Protocol to `1.13.0` through a Markdown-only activation change.

## Verification requirement for recovery

L001 may return to `VERIFIED` only after all of the following are true:

1. D040 is integrated;
2. T010 replaces the duplicated mutable current-version authority with deterministic parsing/validation from Core;
3. T010 focused/full/Ruff gates pass on Protocol `1.12.0` with staged `ASSURANCE.md`;
4. T010 is accepted/integrated/clean;
5. the subsequent Markdown-only D036 activation bumps Core to `1.13.0` and routes `ASSURANCE.md` while the full deterministic suite remains green without any executor literal update;
6. no second independent current-version authority is introduced.

## Recurrence monitoring

Any later need to synchronize an independently authored exact-current protocol literal is the same control failure unless evidence establishes a materially different compatibility requirement.
