# Source Maintainer Reference

Use only for maintenance of the canonical Agent Governance source repository after exact source-product identification resolves the `source-maintainer` profile.

Activate this capability for explicit source-product work involving live Governance Core, Task Contracts, decisions, checkpoint, branching/release/testing policy, source verification records, or authorized handoff JSON paths.

Source-maintainer operation must remain fail-closed and isolated from Consumer state. Do not create or mutate `.agent-governance/` or `.agent-coordination/` at the source root. Do not infer source identity from directory names. Do not broaden source writes beyond accepted source adapters and authorized non-Markdown handoff paths.

Do not use this capability for ordinary Consumer Governance operation, generic coding, generic Git work, unrelated source repositories, or generic package/Skill installation.
