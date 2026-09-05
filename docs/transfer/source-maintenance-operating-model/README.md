# Agent Governance Source-Maintenance Transfer Bundle

Status: SOURCE-SIDE EXTRACTION COMPLETE  
Source repository: `ManuelBouza/agent-governance`  
Extraction baseline: `develop@0e2edbca2cb0e620db7cdb7b93945bef8985fdfd`  
Authority posture: extracted semantics only; this bundle is not itself a target-project adoption decision

## Purpose

This bundle packages the accepted operating logic needed to reproduce the current Agent Governance source-maintenance model in another similar repository without requiring the target project to depend on this source repository after adoption.

It is deliberately **not** a wholesale repository copy. It separates:

1. normative portable semantics;
2. source-product/provider adapter details that require target mapping;
3. historical research and experimental evidence;
4. unresolved gaps;
5. frozen or unaccepted implementation that must not be copied.

The target project must create its own native authority, decisions, receipts and paths. Source Decision/Research identifiers remain provenance only.

## Bundle contents

| File | Purpose |
| --- | --- |
| `PORTABLE-OPERATING-MODEL.md` | Self-contained semantic operating model to evaluate for target adoption. |
| `PORTABILITY-MANIFEST.md` | Artifact/rule classification and provenance inventory. |
| `EVIDENCE-APPENDIX.md` | Research/experiment evidence supporting the extracted controls without promoting research to authority. |
| `UNRESOLVED-GAPS.md` | Known limitations and explicit non-claims that must survive transfer. |
| `TARGET-ADOPTION-CHECKLIST.md` | Fail-closed target bootstrap and REUSE/ADAPT/COEXIST/MISSING/CONFLICT adoption procedure. |
| `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md` | D067-style successor prompt template; target repository identity must be bound before use. |

## Authority model

The bundle distinguishes **source authority** from **target authority**.

```text
source accepted decisions at extraction baseline
        -> semantic extraction + classification
        -> Transfer Bundle
        -> target repository inspection
        -> target-native REUSE / ADAPT / COEXIST / MISSING / CONFLICT decisions
        -> target-native receipts / policy / operating documents
```

The bundle does not make a source `Dxxx`, `Rxxx`, Task Contract, checkpoint, AGENTS file, branch name, model name, connector behavior or Library path authoritative in the target.

Research remains evidence. Experiments remain evidence. Target adoption requires an explicit target-native decision or already-controlling compatible target policy.

## Extraction principles

- GitHub is the canonical source repository authority.
- The extraction baseline is the exact source `develop` commit recorded above.
- Later source changes do not silently alter this bundle's provenance.
- Effective semantics were extracted from current accepted authority, including later refinements and overlays; earlier conflicting wording was not copied as if still controlling.
- `AGENTS.md` is not copied wholesale.
- The target must preserve stronger compatible native controls rather than replacing them with weaker Agent Governance examples.
- Provider-specific labels, branch names, model names, commands, file paths and connector capabilities are adapter details.
- The source repository's Consumer Governance Core is not installed by this bundle and is outside this source-maintenance transfer objective.

## Frozen implementation boundary

T058 is intentionally excluded from production transfer.

```text
source task: T058
source branch: feat/t058-chatgpt-portable-workspace-adapter
source remote head: 6ed319a1802cfd90d50d9dc95d969435c295a164
source implementation/review anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
state: BLOCKED / FROZEN_BY_HUMAN
classification: DO_NOT_COPY
```

The accepted workspace semantics come from current decisions and operating documents, not from the frozen helper implementation.

## Target adoption outcome

A successful target adoption should leave the target repository able to operate independently with:

- its own canonical branch and protection model;
- its own source-maintenance policy and checkpoint/frontier carrier;
- its own task/operation contract and handoff carriers where needed;
- its own workspace/Library/local-Git adapter or a documented compatible fallback;
- its own Executor coordinator/delegation configuration;
- its own target-native decisions/receipts proving how the portable semantics were reused, adapted, coexisted, or rejected.

The target should not need this source repository at runtime after those target-native artifacts are integrated.
