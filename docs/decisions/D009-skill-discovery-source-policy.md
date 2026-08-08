# D009 — Skill Discovery Source Policy

Status: ACCEPTED
Authority: Human Owner
Protocol: 1.8.0
Origin: migrated from the original `script-uh` governance testbed.

## Context

Public Agent Skill directories are useful for finding candidates but can contain third-party, stale, mirrored, lookalike or malicious artifacts. Directory popularity/security signals do not establish ownership or project approval.

## Decision

- Treat discovery source and artifact trust as separate concepts.
- Search existing approved/project-owned and canonical upstream sources before broad public directories.
- Use public directories such as skills.sh, SkillsMP, agent-skills.md and ClawHub only to discover/cross-check candidates; meta-indexes such as skilldb are discovery aids only.
- Resolve every external candidate to canonical owner/repository/path before acquisition.
- Never execute directory/marketplace installation commands against the active project during F3.
- Apply quarantine and `SKILL-SUPPLY-CHAIN.md` audit only to the exact canonical artifact revision/digest.
- Rankings, installs, stars, badges, automated scans and multi-directory presence may prioritize review but never satisfy approval.
- Reject candidates whose canonical provenance cannot be established.

## Consequences

F3 has an explicit sequence: capability gap -> governed discovery -> canonical resolution -> quarantine/audit -> exact artifact approval. Known directories may evolve without changing this invariant.
