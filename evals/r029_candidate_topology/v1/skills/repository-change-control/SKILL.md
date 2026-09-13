---
name: repository-change-control
description: Use when tracked repository content must be changed through an authorized mutation path and the task needs base/target/branch/review safety or durable repository provenance. Do not use for read-only inspection, generic Git syntax, or as authority to change repository policy.
---

# Repository change control — evaluation fixture

Intent: prepare and carry out a repository mutation through an already-authorized change path while preserving protected-target safety, reviewability, durable provenance and repository-local policy.

Required behavior:
- resolve repository-local policy, authorized base and integration target;
- fail closed if authority/base/target is missing or contradictory;
- use a bounded reviewable mutation path;
- verify the relevant durable/remote postcondition;
- never claim semantic acceptance merely because Git/provider mechanics succeeded.

Anti-triggers: read-only inspection, generic Git help, ordinary editing after a safe change path is already established, task/specification/acceptance decisions, or release strategy whose primary intent is not ordinary change-path control.

Postcondition: authorized base/target/change path plus reviewable durable state, or an explicit blocked state. Repository/domain policy remains authoritative.
