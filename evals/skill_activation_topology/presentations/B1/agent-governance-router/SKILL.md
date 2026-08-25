---
name: agent-governance-router
description: Route explicit Agent Governance requests to Consumer lifecycle, canonical source-maintainer, or external-Skill-trust guidance. Do not activate for generic coding, testing, Git, SDD/tooling, releases, documentation, or generic Skill installation.
---

# Agent Governance Router

Identify the minimum required Agent Governance capability and load only its reference:

- Consumer repository governance -> `references/consumer-lifecycle.md`
- canonical Agent Governance source maintenance -> `references/source-maintainer.md`
- external Agent Skill trust/audit -> `references/external-skill-trust.md`

For valid multi-intent work, load only the required union in the listed order. If Consumer/source context is ambiguous, request context rather than broadening permissions.

This router does not change Core, engine, profile, authority, or mutation semantics.
