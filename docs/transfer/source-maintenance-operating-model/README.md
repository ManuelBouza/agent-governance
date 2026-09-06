# Agent Governance Source-Maintenance Transfer Bundle

Status: SOURCE-SIDE EXTRACTION / OFFLINE-PORTABLE

This bundle packages the accepted operating logic needed to reproduce the current Agent Governance source-maintenance model in another similar repository.

**The target project does not need access to this source repository.** A complete offline export carries the portable semantics, evidence/gaps, adoption procedure, bootstrap, integrity receipt and selected source-reference snapshots required for audit/clarification.

Start with `OFFLINE-START-HERE.md`.

## Bundle layers

1. **Portable adoption core** — semantic model, portability manifest, gaps, checklist and offline bootstrap.
2. **Evidence** — research/experiment synthesis supporting the controls without creating authority.
3. **Offline source-reference snapshots** — exact source wording for provenance/audit only; never automatic target authority.
4. **Explicit exclusions** — frozen/unaccepted implementation such as T058.

## Primary files

- `OFFLINE-START-HERE.md`
- `PORTABLE-OPERATING-MODEL.md`
- `PORTABILITY-MANIFEST.md`
- `EVIDENCE-APPENDIX.md`
- `UNRESOLVED-GAPS.md`
- `TARGET-ADOPTION-CHECKLIST.md`
- `TARGET-ADOPTION-BOOTSTRAP-TEMPLATE.md`
- `OFFLINE-EXPORT-MANIFEST.md`

## Authority model

```text
source accepted authority
-> semantic extraction
-> offline Transfer Bundle
-> target governance inspection
-> REUSE / ADAPT / COEXIST / MISSING / CONFLICT
-> target-native decisions/receipts/policy
-> independent target operation
```

The portable model is a candidate for adoption. Source `Dxxx`, `Rxxx`, `AGENTS.md`, branch names, model names, paths, connector behavior and Library product details remain provenance/adapter information unless the target explicitly adopts compatible semantics.

Research remains evidence. Experiments remain evidence. Preserve stronger compatible target-native controls.

## Frozen T058 boundary

T058 remains `BLOCKED / FROZEN_BY_HUMAN` and `DO_NOT_COPY`.

```text
branch: feat/t058-chatgpt-portable-workspace-adapter
remote head: 6ed319a1802cfd90d50d9dc95d969435c295a164
implementation/review anchor: 00134357e77f46d9cfcf82b03cedca3f386688f5
```

Its helper/code/tests are not portable accepted production logic and are excluded from the implementation package.

## Offline export integrity

A distributable archive should contain `EXPORT-RECEIPT.txt` and `SHA256SUMS.txt`. The target bootstrap fails closed on a missing/corrupt/inconsistent required package component.
