# Workspace Isolation Internal Route

This is an internal route of `executor-launch-handoff`, not a top-level Skill.

Use before delegated writable execution when concurrent work units or ambiguous local state could create conflicting writers.

## Inputs

- delegated work-unit identity;
- selected executor/session;
- repository/resource identity;
- requested writable branch/resource when applicable;
- inventory of relevant writable surfaces;
- repository-local branch/base/cleanup policy;
- continuation or retirement state from the enclosing launch/handoff lifecycle.

## Workflow

1. Determine whether writable isolation is required.
2. Inventory relevant writable surfaces without treating age or naming as deletion authority.
3. Reuse an existing represented workspace only for safe same-work-unit continuation.
4. Otherwise allocate/select one exclusive writable surface only when no conflicting or ambiguous ownership exists.
5. Fail closed rather than reset/clean/delete unknown, unique, or unrepresented state.
6. Preserve work-unit/workspace attribution through execution and review.
7. At retirement, defer branch/integration safety to repository change-control/local cleanup policy and remove only evidence-safe obsolete surfaces.

## Postcondition

Before writable execution, one active writable work unit maps to one exclusive writable surface; represented authority/workspace/target agree; ambiguous state is preserved and reported.

At retirement, removal occurs only after repository-policy lifecycle permits it and no unique state is discarded.

## Authority boundary

This route cannot create mutation authority, choose branch/release policy independently, redefine Task Contract scope, decide semantic acceptance, delete ambiguous state for convenience, or make host-specific worktree syntax a semantic requirement.

For repository-backed work, branch/base/integration/retirement semantics come from `repository-change-control` or repository-local policy.
