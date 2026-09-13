---
name: upstream-version-revalidation
description: Revalidate consequential reliance on version-sensitive external behavior by comparing the exact relied-on version with current stable and relevant higher releases, recording evidence about material change without authorizing upgrades or qualification extension. Do not use for routine update checks, installation commands, descriptive version mentions, ordinary security patching, or general research with no material version-specific reliance.
---

# Upstream Version Revalidation

Use only when a consequential conclusion depends materially on external version-specific behavior.

## Trigger

Activate when a design, workaround, compatibility claim, evaluation, launch, or reproducibility decision relies on an exact external runtime/library/tool/provider version and later upstream state may have changed the relied-on behavior.

Do not activate merely because a newer version exists, for routine install/update commands, descriptive version mentions, generic vulnerability patching governed elsewhere, "use latest" policies with no revalidation question, or general research unrelated to version-specific reliance.

## Workflow

1. Identify the exact reference/pinned version and consequential relied-on surface.
2. Establish current stable upstream state from authoritative evidence.
3. Inspect higher relevant releases; include relevant prerelease evidence only when it materially informs an unresolved surface.
4. Compare the exact API/schema/source/behavior surface, preferring stronger evidence over changelog wording alone.
5. Record versions, sources, freshness, material differences, and unresolved uncertainty.
6. Return evidence to the calling domain; do not decide project upgrade/qualification/launch authority.

## Postcondition

Produce an evidence-backed disposition such as `REFERENCE_STILL_SUPPORTED`, `MATERIAL_UPSTREAM_CHANGE`, `REVALIDATION_REQUIRED`, `NO_MATERIAL_CHANGE`, or `INSUFFICIENT_EVIDENCE`, plus exact versions/surfaces/provenance.

## Authority boundary

This Skill cannot require an upgrade, auto-extend qualification, treat prerelease state as production authority, redefine pins/compatibility/risk policy, or promote evidence into project policy.

For Agent Governance, D077 vocabulary, D063 qualification relationships, project pins, launch/re-entry consequences, and Decision authority remain in the Maintainer domain.
