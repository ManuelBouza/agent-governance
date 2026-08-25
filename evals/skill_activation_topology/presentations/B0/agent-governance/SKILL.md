---
name: agent-governance
description: Use for explicit Agent Governance work across governed Consumer repositories, canonical Agent Governance source maintenance, or external Agent Skill trust/audit. Route safely between Consumer lifecycle, source-maintainer, and external-skill-trust capabilities. Do not activate for generic coding, testing, Git, SDD/tooling, documentation, releases, or generic Skill installation without an Agent Governance intent.
---

# Agent Governance

This is the unified dispatcher baseline. Determine the requested Agent Governance capability before acting.

For governed adopting-repository lifecycle work, load `references/consumer-lifecycle.md`.

For canonical Agent Governance source-product maintenance, load `references/source-maintainer.md` only after exact source-product context is established.

For external Agent Skill discovery, provenance, approval eligibility, or supply-chain audit, load `references/external-skill-trust.md`.

For a legitimate multi-intent request, load the union of the required references in this order: Consumer Lifecycle, Source Maintainer, External Skill Trust. Do not load unrelated capability references.

If Consumer versus source-maintainer context is ambiguous, do not activate a broader permission surface; request the missing context. Do not activate merely because words such as governance, agent, skill, source, profile, task, or release appear.

All routes remain one Agent Governance product over one Core, one deterministic engine, and mutually isolated runtime profiles.
