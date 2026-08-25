---
name: agent-governance
description: Use only for explicit Agent Governance product work: an installed governed Consumer repository, the canonical Agent Governance source product, or Governance-scoped trust review of an external Agent Skill. Do not use for generic coding, generic SDD, Git, releases, corporate governance, unrelated source maintenance, or generic Skill installation. If Agent Governance is explicit but the repository role is unclear, activate only to ask whether the context is Consumer or canonical source; do not grant either profile yet.
---

# Agent Governance unified dispatcher

This B0 baseline exposes all three Agent Governance capability families through one Skill.

On activation, read all three local references before routing:

- `references/consumer-lifecycle.md`
- `references/source-maintainer.md`
- `references/external-skill-trust.md`

Then select only the capability required by the request. For ambiguous source-versus-Consumer context, return `clarify-context` and grant no profile/capability permission. For cross-profile requests, use the legitimate current-context capability only to return a bounded rejection; never grant or perform the forbidden capability.
