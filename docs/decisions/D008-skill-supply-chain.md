# D008 — Skill supply-chain verification

Status: ACCEPTED
Authority: Human Owner
Origin: migrated from the original `script-uh` governance testbed.

## Decision
External Skills must be discovered before installation, acquired from the strongest available canonical provenance source, audited in quarantine, and approved only for an exact immutable revision/content digest before installation or normative use.

## Rationale
Skills may contain instructions, scripts, dependencies and privileged behavior. Source reputation or platform scanning alone is insufficient to establish project trust.

## Consequences
- Classify trust from the canonical artifact, not the discovery directory.
- Persist per-Skill approval records in the adopting project instance.
- Audit all content, scripts/config, permissions, dependencies, network/filesystem/process/secret behavior and maintenance/compatibility.
- High-risk Skills require explicit Human Owner approval.
- Any artifact, dependency or permission change requires re-audit before update/use.
- Revoked/superseded Skills cannot satisfy F3 or task requirements.

Current detailed semantics are defined by `governance-core/SKILL-SUPPLY-CHAIN.md` and refined by D009.
