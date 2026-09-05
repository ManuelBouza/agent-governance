# Unresolved Gaps and Non-Claims

Status: EXTRACTED / MUST SURVIVE TARGET ADOPTION

These gaps are part of the portable model's safety boundary. A target must not silently fill them by assumption.

## Portable workspace / locking gaps

The accepted source semantics do not provide an automatic general solution for:

1. crash/orphan recovery after lock acquisition;
2. TTL or heartbeat semantics;
3. automatic abandoned-lock reclamation;
4. ownership transfer between chats/coordinators;
5. automatic resume of closed-but-unmerged work across chats;
6. provider-independent lock/topic ref retirement mechanics;
7. automatic persistent-store garbage-collection selection under real quota pressure;
8. unusual Git ref-name canonicalization/encoding at scale;
9. arbitrary provider ruleset/branch-protection interaction outside the qualified source envelope;
10. large-repository snapshot practicality near provider file-size/storage limits;
11. automatic conflict resolution after stale-write/CAS rejection.

A target that needs any of these must create explicit target-native authority and qualify the chosen mechanism before relying on it.

## Executor / worker gaps

- No source-wide adaptive child model/reasoning routing policy is adopted. Do not copy a vendor model mapping as portable governance.
- Exact child permission/sandbox provenance is provider/version sensitive. If acceptance depends on it, qualify the active target Executor surface rather than inferring it.
- Coordinator naming syntax and host thread identifiers are adapter details.
- A desired worker graph is not portable by default. Exact topology becomes authority only when the target explicitly makes topology an acceptance/safety/experiment variable.

## Vendor/runtime volatility

Revalidate before operational reliance:

- local Git availability;
- direct network transport availability;
- GitHub/GitLab/provider connector/API mutation semantics;
- expected-head/CAS behavior of the chosen write surface;
- persistent file-store materialize/upload/version/rename/delete behavior;
- file-size/storage/retention limits;
- model names and effort controls;
- session naming/continuation interfaces;
- worker/subagent permission and telemetry surfaces.

Historical source observations are evidence only.

## T058 frozen implementation

The source helper implementation associated with T058 is not accepted production logic.

```text
branch: feat/t058-chatgpt-portable-workspace-adapter
head: 6ed319a1802cfd90d50d9dc95d969435c295a164
implementation/review anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
state: BLOCKED / FROZEN_BY_HUMAN
```

Do not:

- copy its helper/code as an accepted implementation;
- claim its tests establish target readiness;
- resume or merge it as part of transfer;
- use it to close any gap listed above.

A target may implement its own adapter from the portable semantics, with target-native tests/evidence.

## Source legacy wording

Some source operating documents predate the latest objective-scoped/Library-first refinements. The Transfer Bundle is extracted from effective current authority, not from literal mechanical copying of all source text.

Therefore:

- legacy source wording is not an unresolved ambiguity to be copied;
- later accepted refinements control where there is direct conflict;
- target adoption should implement the extracted semantic model rather than reproduce historical inconsistencies.

## Target-specific unknowns

The source extraction intentionally does not assume:

- target repository identity;
- provider;
- default/integration branch topology;
- existing governance system;
- existing SDD/runbook/checkpoint mechanism;
- branch/ruleset configuration;
- target Executor/agent host;
- persistent workspace availability;
- target risk/approval policy;
- target release/CI requirements.

Those facts are resolved only in the target-adoption chat by inspecting target truth and classifying overlap.
