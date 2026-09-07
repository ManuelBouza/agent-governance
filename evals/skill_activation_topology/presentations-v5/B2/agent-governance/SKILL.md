---
name: agent-governance
description: Use only for a request to apply Agent Governance itself: operate a repository currently governed by Agent Governance, maintain the canonical Agent Governance product source, or apply Agent Governance trust policy to an external Agent Skill. Product applicability is required; topic similarity or incidental mention is insufficient.
---

# Agent Governance positive-anchor router

Do not preload capability references.

Route only after Agent Governance applicability is affirmative:

- governed Agent Governance Consumer repository -> read only `references/consumer-lifecycle.md`;
- canonical Agent Governance source product -> read only `references/source-maintainer.md`;
- Agent Governance-scoped external Agent Skill trust -> read only `references/external-skill-trust.md`;
- legitimate multi-intent -> read only the references required by those intents;
- affirmative Agent Governance applicability with unresolved source-versus-Consumer role -> ask for context without granting a profile or reading capability references.

Before granting `source-maintainer`, require the exact supported source-product signal.

For cross-profile requests, route only to the legitimate current-context capability and return a bounded rejection of the forbidden operation.
