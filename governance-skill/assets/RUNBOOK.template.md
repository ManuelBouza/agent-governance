# Runbook

Runbook-ID: `<runbook-id>`
Status: `DRAFT`
Revision: `<revision-or-git-identity>`
Owner: `<human|strategy|project-native>`

## Purpose

`<intended operational outcome>`

## Applicability and exclusions

- Applies when: `<conditions>`
- Excludes: `<conditions>`

## Authorization binding

- Required effect classes: `<D033-effect-classes>`
- Target constraints: `<target-class/identity constraints>`
- Privilege ceiling: `<maximum identity/role>`
- Credential class: `<reference class, never secret value>`
- Network scope: `<destinations/boundary>`
- Approval/Human gates: `<ALLOW_TASK|ALLOW_EXPLICIT|REQUIRE_HUMAN locations>`

This runbook states procedure requirements; it does not grant execution authority.

## Inputs

- `<parameter>` — `<type/constraint>`

## Preconditions

- `<observable condition that must hold before execution>`

## Semantic steps

### Step `<id>` — `<purpose>`

- Required effect: `<effect class>`
- Resource scope: `<scope>`
- Pre-step assertion: `<assertion>`
- Required state transition/effect: `<semantic effect, not terminal syntax>`
- Post-step assertion: `<assertion>`
- Evidence: `<sanitized evidence>`
- Retry/idempotency: `<rule>`
- Failure route: `<stop/recover/block>`
- Recovery/compensation: `<step/reference>`

## Checkpoints and Human gates

- `<checkpoint/gate and invalidation condition>`

## Postconditions

- `<final observable state>`

## Recovery

- Rollback/compensation: `<procedure/reference>`
- Unsafe/impossible rollback stop condition: `<condition>`
- Escalation: `<route>`

## Evidence

- `<runbook revision, target/principal, completed steps/checkpoints, postconditions, recovery and sanitized operation references>`

## Adapter recipes

Verified adapter syntax is stored separately under `runbooks/recipes/` and references this runbook/step. Adapter recipes are technical evidence and MUST NOT redefine this semantic procedure.