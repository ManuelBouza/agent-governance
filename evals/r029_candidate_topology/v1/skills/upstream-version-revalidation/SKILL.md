---
name: upstream-version-revalidation
description: Use when a consequential design, launch, workaround, evaluation or compatibility conclusion relies on version-specific behavior of an external runtime, library, tool or provider and the relied-on version may be stale. Do not use for routine update checks, install commands or descriptive version mentions.
---

# Upstream version revalidation — evaluation fixture

Intent: identify the exact relied-on version and material behavior surface, establish current relevant upstream state, compare relevant releases, and return bounded evidence about whether the historical assumption remains valid.

Required behavior:
- inspect the reference/pinned version and current stable upstream state;
- inspect higher relevant releases and relevant prereleases only when they materially inform an unresolved surface;
- compare the exact relied-on API/schema/source/behavior where practical;
- preserve evidence provenance/freshness;
- distinguish upstream evidence from project authority to upgrade, requalify, launch or accept.

Anti-triggers: a newer package exists with no consequential version-specific reliance, ordinary dependency commands, general research without a version-sensitive controlling assumption, or an already-authoritative simple latest-version policy.

Postcondition: evidence-backed material-change/revalidation status. The calling domain retains upgrade, qualification, launch and acceptance authority.
