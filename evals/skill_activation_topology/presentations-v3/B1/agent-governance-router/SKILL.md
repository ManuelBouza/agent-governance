---
name: agent-governance-router
description: Thin router for explicit Agent Governance product work only. Activate when the request clearly concerns an installed governed Consumer repository, the canonical Agent Governance source product, or Governance-scoped external Agent Skill trust. Do not activate for generic coding/SDD/Git/release/corporate-governance/source-maintenance/Skill-installation requests. If Agent Governance is explicit but source-versus-Consumer context is missing, activate only to ask for that context and load no capability reference.
---

# Agent Governance thin router

Do not preload capability references.

Route by explicit context and intent:

- governed Consumer repository -> read only `references/consumer-lifecycle.md`;
- canonical Agent Governance source product -> read only `references/source-maintainer.md`;
- Governance-scoped external Agent Skill trust -> read only `references/external-skill-trust.md`;
- legitimate multi-intent -> read only the references required by those intents;
- ambiguous source-versus-Consumer request -> ask for context without granting a profile or reading capability references.

For cross-profile requests, route only to the legitimate current-context capability and return a bounded rejection of the forbidden operation.
