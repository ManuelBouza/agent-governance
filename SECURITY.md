# Security Policy

Agent Governance treats governance bypasses, unsafe Skill handling, authority-confusion defects, provenance failures, and unintended disclosure of protected task context as security-relevant defects.

## Reporting

Do not include credentials, private repository content, personal data, production secrets, or live exploit material in public reports.

When GitHub private vulnerability reporting is available for this repository, prefer that channel for issues whose disclosure could materially enable abuse before a fix exists. Otherwise, open a public issue containing only the minimum non-sensitive description needed to identify the affected component and state that security-sensitive details are being withheld.

## In scope

Examples include:
- Governance or adapter behavior that permits unauthorized mutation of authoritative records;
- bypass of lifecycle/readiness or sequential-disclosure rules;
- Skill provenance, digest, approval, revocation, or permission-envelope validation defects;
- malicious Skill content being treated as trusted without the required audit;
- state reconstruction that silently accepts conflicting authority or forged events;
- bootstrap/install behavior that overwrites existing project state unexpectedly.

## Out of scope

General model quality, application-specific coding bugs, and security defects in unrelated consumer applications are outside this repository unless caused by the governance product itself.

## Disclosure and fixes

Security fixes should preserve auditability, add regression coverage, and document protocol compatibility impact. A vulnerability that changes governance guarantees may require a protocol version change and an explicit Decision Record.
