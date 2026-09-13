---
name: repository-change-control
description: Control an authorized tracked repository mutation path: resolve repository-local base/target/branch/review policy, avoid protected direct writes, preserve durable provenance, and fail closed on ambiguous authority or stale change-path state. Do not use for read-only inspection, generic Git syntax/history questions, ordinary editing after a safe path is already established, release strategy, or task/acceptance authority.
---

# Repository Change Control

Use when tracked repository mutation requires change-path resolution or verification. Repository-local policy is always authoritative.

## Trigger

Activate for work that must resolve or verify an authorized mutation base, change/topic branch, protected-target restriction, review/integration target, freshness relationship, or durable branch/ref provenance.

Do not activate for read-only inspection, generic Git commands/history/diff help, local scratch work outside governed mutation, ordinary editing after the change path is already safely established, release planning as the primary intent, or specification/Design/acceptance decisions.

## Workflow

1. Identify repository identity and caller authority envelope.
2. Load repository-local branch/change policy.
3. Establish current durable base/target/branch state.
4. Select only an already-authorized change-path class.
5. Fail closed on unknown/conflicting base, target, permissions, freshness, or protected-target restrictions.
6. Preserve a bounded reviewable mutation unit and durable branch/ref provenance.
7. Verify the relevant remote/durable postcondition after authorized repository actions.

## Postcondition

Return the resolved authorized base, integration target, change-path/branch identity, protected-write disposition, reviewable durable state, and any blocked conflict. Successful mechanics never imply semantic acceptance.

## Authority boundary

This Skill cannot create mutation permission, redefine repository branch/release policy, alter task scope/specification/Design/ownership/acceptance, weaken protection, or make host identity authoritative.

For Agent Governance, `docs/BRANCHING.md`, D061/D062, D068 publication, write ownership, release policy, and the Maintainer adapter remain controlling.
