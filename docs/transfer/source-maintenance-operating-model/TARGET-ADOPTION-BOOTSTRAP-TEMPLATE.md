# Offline Target-Adoption Bootstrap Template

Status: TEMPLATE / TARGET IDENTITY REQUIRED BEFORE MUTATION

This bootstrap is intentionally **source-repository independent**. The target-adoption chat must be able to operate from the exported Transfer Bundle plus the target repository alone.

```text
TRANSFER PACKAGE
Package: Agent Governance source-maintenance Transfer Bundle
Package mode: OFFLINE / SELF-CONTAINED
Required local entrypoint: OFFLINE-START-HERE.md
Required receipt: EXPORT-RECEIPT.txt
Required checksums: SHA256SUMS.txt

TARGET
Target repository: <REQUIRED: owner/repository or exact local repository identity>
Target canonical branch: <DISCOVER FROM TARGET; DO NOT ASSUME develop>
Target expected HEAD: <READ/BIND AT LAUNCH>
Target checkpoint/frontier: <DISCOVER EXISTING TARGET CARRIER OR NONE>
Target provider: <DISCOVER>

OBJECTIVE
Adopt the portable source-maintenance operating model contained in this local
Transfer Bundle into the target repository as target-native governance.

The target must remain independently operable after adoption and MUST NOT
depend on access to ManuelBouza/agent-governance.

BOOTSTRAP FIRST — BEFORE TARGET MUTATION

A. VERIFY THE LOCAL TRANSFER PACKAGE
1. Read OFFLINE-START-HERE.md.
2. Read EXPORT-RECEIPT.txt and SHA256SUMS.txt.
3. Verify the declared package files/checksums that are available to the chat/runtime.
4. Read, in order:
   - PORTABLE-OPERATING-MODEL.md
   - PORTABILITY-MANIFEST.md
   - UNRESOLVED-GAPS.md
   - TARGET-ADOPTION-CHECKLIST.md
   - EVIDENCE-APPENDIX.md
   - OFFLINE-EXPORT-MANIFEST.md
5. Treat source-reference/* only as provenance/evidence. Do not promote source
   Dxxx/Rxxx/AGENTS wording to target authority automatically.
6. If a required package component is missing, inconsistent, corrupt, or its
   provenance cannot be established, fail closed before target mutation.

B. COLD-START THE TARGET
7. Read current target canonical branch identity from its repository provider.
8. Read target governing instructions (AGENTS.md or equivalent) from that exact revision.
9. Discover/read the target checkpoint/frontier/state carrier if one exists.
10. Inspect existing target governance, SDD, task/handoff, branch, runbook,
    Executor, workspace, protection and evidence mechanisms.
11. Classify every overlapping target capability as exactly one of:
    REUSE / ADAPT / COEXIST / MISSING / CONFLICT.
12. Preserve stronger compatible target-native controls.
13. Verify effective long-lived branch protection before normal writable automation.
14. Do not copy source AGENTS.md wholesale.
15. Do not copy source Decision/Research IDs as target decisions.
16. Do not copy or rely on frozen T058 implementation.
17. Revalidate provider/runtime/vendor-specific behavior on the actual target.

FAIL-CLOSED

If any material expected package or target state disagrees:

STATUS: BOOTSTRAP_MISMATCH
EXPECTED: <value>
OBSERVED: <value>
SOURCE: <local transfer artifact or target artifact>
BLOCKER: <why continuation is unsafe>

Do not overwrite, reinterpret, silently repair or bypass the discrepancy.
Return the discrepancy packet to the Human Owner.

IF BOOTSTRAP VERIFIES

Build target-native adoption authority that:
- preserves applicable portable semantic invariants;
- maps provider/host/path details to target reality;
- preserves stronger compatible existing controls;
- establishes protected topic-branch writable readiness;
- creates target-native decisions/receipts;
- uses target-native Task/Operational Contract + Executor boundaries for
  executable adoption work;
- keeps research/experiments as evidence only;
- carries unresolved gaps explicitly;
- verifies the integrated result;
- leaves future target maintenance independent of the source repository.

Use the target's own canonical Git/PR/MR path for all writes.
```

Source-repository access may be used later as optional provenance revalidation if it becomes available, but absence of that access is not a blocker when the offline package is complete and verified.
