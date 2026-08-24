# Runbook Operation Resolution Contract

Status: DESIGN-APPROVED — STAGED  
Controlling decision: `docs/decisions/D054-executor-owned-operation-resolution-and-runbook-recipes.md`  
Activation: after T035 executable readiness and D040 Phase-B Core activation

## Purpose

Define the smallest portable contract for resolving and reusing Execution Adapter operations safely across CLI, API, SDK, PowerShell, Bash, remote-management and equivalent mechanisms.

This contract is staged source-product Design. Until D040 Phase-B activation it does not replace the currently routed Consumer Core semantics.

## Ownership boundary

```text
Human / Strategy
    -> operation intent + target/effect authority + semantic runbook

Implementation / Executor
    -> adapter selection + syntax/API realization + execution + verification
    -> verified operation recipe
```

Semantic runbooks remain procedure authority. Recipes remain technical realizations/evidence.

## Resolution algorithm

For every adapter operation:

1. **Resolve intent** — identify stable `operation_id`, actual target, resource scope, effect classes and current authorization context.
2. **Resolve procedure** — if the operation is material under D034, select the required semantic runbook/step. If none exists, stop for Strategy re-entry.
3. **Match recipe** — search only the relevant recipe registry for a `VERIFIED` recipe whose binding matches the current operation, adapter/tool/API identity/version, platform/shell context when material, target class and effect boundary.
4. **Reject stale trust** — `CANDIDATE`, `STALE`, `REVOKED` and `SUPERSEDED` recipes are not executable cached authority.
5. **Documentation fallback** — when no compatible verified recipe exists, inspect project-native authoritative procedure/help first, then installed/version-specific help/schema, then official vendor documentation for that version.
6. **Build candidate** — create a parameterized, secret-free candidate that preserves the semantic step and D033 envelope.
7. **Preflight** — verify target/principal/context and use preview/dry-run/plan where trustworthy and material.
8. **Authorize** — classify the bound invocation through D033. Approval is for the effect boundary, not the command string alone.
9. **Execute** — use least privilege and bounded credentials/network. Child processes may not expand authority.
10. **Verify** — establish the semantic postcondition and detect unexpected effects/context drift.
11. **Promote or stale** — promote to `VERIFIED` only after required evidence. Failure never promotes; failure of an already verified binding makes that recipe `STALE` pending diagnosis.

## Authoritative-source hierarchy

A newly resolved recipe must be supported by at least one authoritative source in this order of preference:

1. `project_native` — current owned project/platform procedure, generated interface or approved operational workflow;
2. `builtin_help` — installed tool/version help/introspection/schema;
3. `official_docs` — official vendor documentation bound to the installed tool/API version;
4. `official_api_schema` — current official API/SDK schema/reference bound to the invoked API version.

Current official docs without a version match may supplement but not override incompatible installed-version behavior.

Community/tutorial/search/model sources may be recorded as diagnostic context but cannot satisfy the authoritative source requirement.

## Native persistence layout

When no adequate project-native provider owns this capability, T035 prepares the native Consumer footprint:

```text
.agent-coordination/runbooks/
    RUNBOOK.template.md
    <runbook-id>.md
    recipes/
        RUNBOOK-RECIPE.template.json
        <recipe-id>.json
```

The registry is demand-driven. Do not generate a catalog of tools/commands during bootstrap.

### Semantic runbook identity

A native semantic runbook uses Markdown because it is Strategy/Human-owned procedure authority and benefits from reviewable natural-language semantics.

Required top-level metadata:

```text
Runbook-ID: <stable-id>
Status: DRAFT | READY | ACTIVE | SUPERSEDED | RETIRED
Revision: <revision-or-git-identity>
Owner: human | strategy | project-native
```

The runbook body must make purpose, applicability/exclusions, required effects, target constraints, inputs, preconditions, ordered semantic steps, checkpoints/Human gates, postconditions, recovery and evidence determinable.

### Recipe record

A native recipe is JSON with exactly these top-level fields unless a later accepted revision extends the schema:

```text
recipe_id
status
operation_id
runbook_id
runbook_step
adapter
binding
effect_classes
invocation
authoritative_sources
preconditions
preview
postconditions
verification
stale_triggers
supersedes
```

Required lifecycle states:

```text
CANDIDATE
VERIFIED
STALE
REVOKED
SUPERSEDED
```

#### `adapter`

```json
{
  "family": "cli | powershell | bash | api | sdk | ssh | remote | automation | other",
  "tool": "<canonical tool/API identity>",
  "version": "<exact installed/API version identity>",
  "platform": "<platform identity or any when provably irrelevant>",
  "shell": "<command environment or null>"
}
```

Exact version identity is the default trust binding. A later design may add compatible ranges only when compatibility can be proven deterministically rather than guessed.

#### `binding`

```json
{
  "target_class": "<semantic target class>",
  "resource_scope": "<bounded resource pattern/description>",
  "privilege": "<maximum identity/role class>",
  "credential_class": "<reference class, never secret value>",
  "network_scope": ["<destination class/reference>"]
}
```

#### `effect_classes`

Values are the D033 effect classes from `EXECUTION-CONTROL.md`.

If any recipe contains one of these material classes, `runbook_id` and `runbook_step` are mandatory and must resolve to an existing semantic runbook:

```text
REMOTE_EXECUTE
PRIVILEGE_ELEVATE
SECRET_USE
DEPLOY_SERVICE_CHANGE
DATA_MUTATE
DESTRUCTIVE_IRREVERSIBLE
```

`INSTALL_CONFIGURE`, `NETWORK_CONNECT` and `MUTATE_SCOPED` may also require a semantic runbook when D034 applicability says the concrete operation is repeatable/material/risky/cross-system/recovery-sensitive. Static validation cannot infer every such project-level risk judgment; the governing task/runbook remains authoritative.

#### `invocation`

The invocation is parameterized and secret-free.

Supported initial kinds:

```text
argv
shell
api
sdk
remote
```

Examples are representations, not universal syntax:

```json
{"kind":"argv","template":["git","status","--short","--branch"]}
```

```json
{"kind":"shell","template":"<parameterized PowerShell/Bash expression>"}
```

```json
{"kind":"api","template":{"operation":"<provider operation>","parameters":"<non-secret parameter schema>"}}
```

Prefer structured argv/API forms over free-form shell text when equivalent because target/argument boundaries are easier to inspect. Shell text remains valid when shell semantics are genuinely required.

#### `authoritative_sources`

Non-empty array. Each item:

```json
{
  "source_class": "project_native | builtin_help | official_docs | official_api_schema",
  "reference": "<path/help topic/official URL/schema id>",
  "version": "<tool/API/doc version identity or null>"
}
```

A `VERIFIED` recipe must have at least one source that is current for the exact adapter binding.

#### Preconditions / preview / postconditions

These fields store concise observable checks or adapter operation references, not hidden reasoning.

- `preconditions`: non-empty for mutation/material operations;
- `preview`: null when unsupported/not useful, otherwise the safe preview operation/expectation;
- `postconditions`: non-empty for every `VERIFIED` recipe and must establish the semantic success state beyond client exit status when material.

#### `verification`

For `VERIFIED`:

```json
{
  "verified_at": "<RFC3339 timestamp>",
  "evidence": "<sanitized task/log/handoff reference>",
  "result": "pass"
}
```

Other states may set `verification` to null or retain historical evidence.

#### `stale_triggers`

Non-empty for `VERIFIED`. Must cover at least adapter/tool/API version drift and a failed postcondition/replay. Additional target/auth/default-context/security triggers are recorded where material.

## Matching semantics

The initial deterministic resolver is deliberately conservative.

A recipe matches only when:

- `status == VERIFIED`;
- `operation_id` matches exactly;
- adapter `family`, `tool`, `version`, `platform` and `shell` match exactly after canonical null/`any` handling defined by implementation;
- target class matches exactly;
- requested effect classes are equal to the recipe's recorded effect boundary;
- a material recipe's `runbook_id`/step resolves to the expected semantic runbook;
- recipe structure/provenance is valid.

No fuzzy matching, model similarity or command-name-only matching is part of the initial trusted path.

If several verified recipes match exactly, resolution must fail as ambiguous unless deterministic project-native precedence makes one uniquely current. The Executor must not pick one arbitrarily.

## Validation rules

T035 deterministic readiness must fail closed on at least:

- unknown top-level fields or lifecycle state;
- missing required identity/binding/provenance fields;
- a `VERIFIED` recipe without authoritative source, postcondition, verification evidence or stale triggers;
- a material effect recipe without a resolvable semantic runbook/step;
- duplicate `recipe_id` or duplicate exact VERIFIED match keys;
- a `SUPERSEDED` record without a replacement/supersession reference;
- unexpected symlink/junction traversal in native runbook/recipe paths;
- recipe/template content that attempts to embed a credential value in a designated credential field rather than a credential class/reference.

Validation proves structural/trust-record consistency. It does not authorize execution or prove a command is safe for every invocation.

## Source-maintainer bootstrap period

Before native Consumer recipe persistence is integrated, source tasks use D054's bootstrap-period rule:

- Executor owns all CLI/API mechanics;
- existing D033/D034 authorization/runbook rules still apply;
- no reusable recipe is assumed merely because a command appeared in chat/history;
- missing syntax is resolved from authoritative documentation;
- successful resolved operations are recorded as provisional handoff evidence;
- T035 may later materialize a durable recipe only after fresh validation against its exact tool/version/context.

## D040 activation boundary

T035 implements runtime/storage/validation/resolution readiness while current routed Protocol remains unchanged. It MUST NOT edit routed Core Markdown or advance `Protocol-Version`.

After T035 acceptance/integration, Orchestrator performs a separate Markdown activation to:

- incorporate D054 operation resolution into routed `EXECUTION-CONTROL.md`;
- describe the runbook/recipe registry in `PROTOCOL.md`;
- route focused lookup in `CONTEXT.md`;
- update Consumer Skill guidance and template references where required;
- advance current protocol/module semantic versions consistently.

This sequencing preserves D040's green-baseline migration invariant.