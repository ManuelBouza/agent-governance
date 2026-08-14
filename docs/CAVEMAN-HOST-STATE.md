# Caveman host state

State: ACCEPTED_WITH_LEGACY_INTEGRATION

## Current accepted state

Caveman is accepted on the Human Owner workstation as an optional user-scoped Skill at the approved v2.0.0 content, discoverable by Gentle AI, with no same-name project Skill shadowing it and with `gentle-orchestrator` preserved.

Two legacy Caveman integration fragments remain present:

- the Caveman plugin entry in `/home/manuel/.config/opencode/opencode.json`;
- the mechanically delimited Caveman block in `/home/manuel/.config/opencode/AGENTS.md`.

These fragments are retained as an accepted host-configuration exception. Their presence does not make Caveman, Gentle AI, or either legacy integration a dependency or authority source for Agent Governance.

## Evidence and disposition

OP039 established the approved Caveman v2.0.0 Skill and Gentle discovery state. OP041 and OP043 confirmed the two legacy fragments and no partial mutation. OP044 classified the blocking edit policy as USER_CONTROLLED. The Human Owner authorized a narrow ephemeral cleanup attempt through OP046. OP046 returned BLOCKED because OpenCode denied both exact process-local edit exceptions, while preserving the Skill, Gentle discovery, `gentle-orchestrator`, persistent policy, and repository state.

After that result, the Human Owner explicitly accepted retaining the two legacy fragments rather than continuing permission work solely to remove them.

## Operational consequence

OP046 is closed as BLOCKED / NOT REQUIRED FOR CURRENT ACCEPTANCE. Do not retry OP046 or introduce broader/persistent edit permissions merely to remove these fragments.

Reopen this host-cleanup line only if concrete evidence shows that either retained fragment causes a real conflict, such as duplicate Caveman activation, unintended provider/runtime routing, Gentle AI interference, `gentle-orchestrator` modification, or another materially observable host behavior.

Until such evidence exists:

- Caveman remains optional and recommended where appropriate, not required;
- Gentle AI remains optional and recommended where appropriate, not required;
- the approved Caveman Skill remains the preferred integration surface;
- the retained legacy fragments are accepted configuration debt, not an active blocker;
- Agent Governance correctness, bootstrap, validation, task execution, verification, and release acceptance must not depend on Caveman or Gentle AI.
