# D056 — Orchestrator visible operation progress

Status: ACCEPTED  
Date: 2026-08-23  
Authority: Human Owner / ChatGPT Orchestrator  
Scope: Human-facing source-maintenance interaction visibility

## Problem

Remote repository and connected-system work can involve several observation, review and mutation steps. If those operations happen without visible phase markers, the Human Owner cannot easily tell whether the Orchestrator is reading canonical state, reviewing a diff, opening a PR, merging, or verifying the resulting state.

The required transparency is operational progress visibility, not disclosure of private model reasoning.

## Decision

When ChatGPT Orchestrator performs material GitHub or equivalent remote source-maintenance operations in an interactive Human-facing conversation, it SHALL emit concise visible **progress notes** around meaningful operation batches.

A progress note states what operational phase is being performed, for example:

```text
Voy a verificar el develop canónico y leer el checkpoint actual.
```

```text
El diff está limpio; ahora abriré el PR y comprobaré que sea mergeable.
```

```text
El PR está integrado; voy a revalidar el HEAD canónico y los archivos finales.
```

## Granularity

Progress notes SHOULD be grouped by meaningful phase rather than emitted mechanically before every individual API/tool call.

Use a new note when the externally observable purpose changes materially, such as:

- canonical-state/bootstrap reads;
- research or evidence gathering;
- diff/review validation;
- branch/file mutation;
- PR creation/review;
- merge/publication;
- postcondition/final-state verification.

For a trivial single read or single mutation, one short note is sufficient. Avoid noisy narration that adds no useful state information.

## Privacy and authority boundary

Progress notes expose **what operation is being attempted or verified**, not hidden chain-of-thought, internal deliberation, private scratch work, or token-by-token reasoning.

They are informational interaction telemetry only:

```text
visible progress note
    != Governance authority
    != Git state
    != acceptance evidence by itself
```

Git and persisted repository artifacts remain authoritative. A progress note must not claim success before the relevant remote postcondition is actually verified.

## Applicability

This decision applies to ChatGPT Orchestrator source-maintenance interaction with the Human Owner. It does not require the Agente de IA Ejecutor to expose its private reasoning or internal orchestration trace, and it does not modify D041 Executor process autonomy.

The same pattern MAY be used for other material connected-system operations when it helps the Human understand the current phase.

## Consequences

- the Human can follow repository-operation progress without needing access to private reasoning;
- GitHub work becomes visibly phase-oriented rather than opaque;
- progress narration is concise enough not to become a new context burden;
- success claims remain tied to verified remote state rather than narration.
