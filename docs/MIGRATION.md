# Product Extraction Record

Date: 2026-08-08

## Source

Original testbed repository: `ManuelBouza/script-uh`

Last source-tree commit before extraction cleanup:
`e52865e11020917ebae0fa7b91722b87f87d7e44`

Extraction cleanup commit in `script-uh`:
`31ca041bde71f9254c7238d64e8cf06518423ab1`

## Destination

Canonical product repository:
`ManuelBouza/agent-governance`

## Migrated product material

- the complete protocol 1.8.0 Governance Core;
- Governance Skill functional contract;
- Governance Skill package design;
- accepted product decisions D001-D009, normalized as product-history records;
- D010 establishing Governance/Skill-only testing scope;
- D011 establishing this dedicated repository as canonical product source;
- explicit source-repository boundaries for deterministic tests and agent evals.

## Deliberately not migrated

- application mission/task/workplan/state from `script-uh`;
- consumer-specific OpenCode configuration;
- consumer-specific repository safety/development rules;
- application code or business-domain state.

The original Git history remains available in `script-uh`, but its current tree is no longer a Governance product source or active Governance consumer.
