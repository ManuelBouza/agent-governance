# D077 — Version-Sensitive Upstream Revalidation

Status: ACCEPTED  
Date: 2026-09-10  
Authority: Human Owner / ChatGPT Orchestrator  
Trigger: T063 repair exposed a version-sensitive vendor/runtime blocker while a newer stable release and a later prerelease already existed  
Research: `docs/research/R021-T063-V3-CONFIG-AUTHORITATIVE-WORKER-RECEIPTS.md`  
Refines: D057, D063  
Preserves: D039, D055, D061, D062, D068, D071, D076

## Problem

A version-pinned evaluation can remain internally consistent while accidentally solving a defect that upstream has already fixed. Conversely, blindly moving to the newest release can invalidate a previously qualified measurement surface or introduce a new experimental variable.

Checking only the pinned version, only a changelog, or only the latest stable release is insufficient when the result materially depends on version-specific behavior.

## Decision

When Agent Governance research, design, evaluation, launch authority or acceptance materially depends on an external tool/runtime/library/provider version, the Orchestrator SHALL perform a **version-sensitive upstream revalidation** before relying on the pinned behavior.

The minimum comparison set is:

```text
1. pinned/reference version actually used by the project;
2. current stable upstream release;
3. every higher relevant release needed to determine whether the material behavior changed;
4. relevant higher prerelease(s) when the blocking capability is still unresolved and the prerelease touches, or plausibly contains changes to, that surface.
```

The purpose is not to maximize version number. The purpose is to determine whether a newer supported upstream state materially changes the design, workaround, qualification or launch decision.

## Required method

The revalidation SHALL:

- identify the exact pinned/reference version and the reason it is pinned;
- identify the current stable release from an official upstream source;
- inspect official release/source evidence for higher relevant versions;
- compare the exact behavior/API/schema/source path material to the project question, rather than relying on changelog wording alone when source or generated schema is available;
- record which versions were reviewed and the material conclusion;
- distinguish stable releases from prereleases;
- preserve any existing qualification boundary until a newer surface is actually requalified.

A prerelease is evidence about upstream direction, not automatic production/experiment authority.

## Disposition classes

A version-sensitive review should make one of these conclusions explicit:

```text
PIN_RETAINED
  newer relevant versions do not remove the blocker or otherwise justify changing the qualified baseline

UPGRADE_REQUIRED
  a newer supported version materially fixes the blocker or makes the existing workaround/design obsolete

REQUALIFICATION_REQUIRED
  a newer version is desirable or required, but a qualified project surface would materially change and must be requalified before execution

NO_MATERIAL_CHANGE
  version movement exists but does not affect the relied-on behavior
```

Equivalent wording is acceptable when the classification is unambiguous.

## Upgrade-fixes-blocker rule

If an official newer supported release removes the blocker that motivated a project workaround, the Orchestrator SHALL NOT silently perpetuate the workaround merely to preserve the older plan.

Required transition:

```text
newer supported release fixes material blocker
    -> stop old workaround launch
    -> re-enter specification/design as needed
    -> evaluate qualification impact
    -> adopt/requalify the newer surface before execution
```

This does not require adopting a prerelease solely because it contains a possible fix.

## Qualified-pin retention rule

A qualified older version may remain intentionally pinned when all are true:

- the pin has a concrete qualification/reproducibility reason;
- current stable and relevant higher versions have been checked;
- no reviewed newer supported version materially fixes the blocker or provides a sufficiently stronger surface;
- moving versions would add requalification cost or an uncontrolled experimental variable without compensating benefit;
- the retained pin is stated explicitly in the research/review/launch authority.

## Timing

Perform the revalidation at the decision point where version-dependent research is promoted into design/evaluation/launch authority.

Repeat it immediately before a consequential launch when the upstream release state may have changed since the earlier review. A materially new stable release between review and launch is a stop/re-entry condition until its relevance is classified.

## Relationship to D057

D057 already requires volatile vendor facts to be refreshed before decision promotion. D077 makes the **version range** explicit: a version-sensitive conclusion must not be based solely on the historical pinned version when higher relevant upstream versions exist.

The resulting research remains subject to the normal D057 Research -> Evaluation -> Decision traceability lifecycle.

## Relationship to D063

D063 remains the qualification authority for the Codex read-only child measurement substrate demonstrated on `0.153.4`.

D077 does not automatically extend D063 to later Codex versions. It requires inspecting later relevant versions before choosing whether to retain the qualified pin, upgrade and requalify, or stop.

## T063 application

R021 reviewed:

```text
0.153.4            qualified T063 reference
0.154.0            current stable at 2026-09-10 review time
0.155.0-alpha.2    later relevant prerelease
```

The reviewed higher versions did not provide the public exact spawned-task receipt that had blocked T063 v2. T063 therefore classifies the result as `PIN_RETAINED`: `0.153.4` remains the deliberate D063-qualified runtime for v3 rather than carrying an obsolete workaround past an available upstream fix.

## Effective rule

```text
material result depends on version-specific behavior
    -> inspect pinned version
    -> inspect current stable
    -> inspect higher relevant versions, including relevant prerelease evidence when useful
    -> compare the exact relied-on surface
    -> explicitly retain pin, upgrade, requalify, or declare no material change
    -> only then authorize consequential execution
```
