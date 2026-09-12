# Source maintainer reference

Use only for the canonical Agent Governance source product identified by the explicit supported source-product signal.

Allowed scope: validate source-maintainer context; locate live Core, Task Contracts, checkpoint, decisions, testing/eval and release records; reason about source-maintenance workflow; and resolve authorized source handoff JSON paths.

Never initialize or mutate Consumer `.agent-governance/` or `.agent-coordination/` state at the source root. Never use source-maintainer authority to approve/install external Skills into a Consumer project. If repository role is unclear, do not grant source-maintainer authority.
