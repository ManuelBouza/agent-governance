---
name: source-maintainer
description: Use only for maintenance of the canonical Agent Governance source repository identified as the source product. Do not use in governed Consumer repositories, for generic source-code maintenance, for generic releases, or for external Skill installation/approval. If the repository is not clearly the canonical Agent Governance source, do not activate this peer.
---

# Source Maintainer peer

Read only `references/source-maintainer.md`.

Use source-maintainer capability only within the explicit source-product boundary. Never initialize Consumer Governance state at the source root. Never use source authority to perform Consumer lifecycle operations or external Skill approval/installation. Cross-profile requests must return bounded rejection without granting the forbidden capability.
