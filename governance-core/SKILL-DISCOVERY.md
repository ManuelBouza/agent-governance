# Skill Discovery Source Policy

Discovery-Version: 1.0.0

Load this module during lifecycle F3 when searching for external Skill candidates or evaluating a directory/marketplace/index as a discovery source.

## Core Invariant

`DISCOVERY TRUST != ARTIFACT TRUST`.

A directory, marketplace, leaderboard, registry or search engine helps locate candidates. It does NOT establish provenance, approval, safety or installability of the Skill artifact it lists.

Never install directly from a discovery result during F3. Resolve every candidate to its canonical upstream artifact first, then apply `SKILL-SUPPLY-CHAIN.md`.

## Discovery Priority

Search in this order unless the capability requires a narrower source:

1. already-approved/project-owned Skills and controlled internal registries;
2. the canonical repository/catalog of the upstream technology/vendor whose expertise is required;
3. official agent/platform repositories that actually publish/own the Skill artifact;
4. established public Agent Skill directories/marketplaces;
5. broader Git hosting/code search and third-party aggregators only when higher-priority discovery does not produce a suitable candidate.

Prefer the shortest provenance chain. A Skill listed by a public directory but owned by an upstream vendor is evaluated from the upstream repository, not from the directory copy/installation command.

## Known Public Discovery Sources

Known sources may change over time. Verify current ownership/status before relying on them; do not persist volatile ranking/count metrics as Governance authority.

- `skills.sh` — broad Agent Skills directory/leaderboard and multi-agent CLI ecosystem; primary public discovery source.
- `SkillsMP` (`skillsmp.com`) — large public Skill marketplace/index; secondary discovery source.
- `agent-skills.md` — independent Agent Skills directory; secondary discovery/cross-check source.
- `ClawHub` (`clawhub.ai`) — community directory with strong OpenClaw orientation; use when relevant to the capability/ecosystem.
- `skilldb` — meta-index aggregating multiple directories; useful for cross-checking/discovery, never canonical provenance.

Additional directories MAY be used when Strategy verifies what they index, who operates them and whether results can be resolved to inspectable canonical artifacts.

## Candidate Resolution

For every discovered candidate, Strategy MUST resolve and record before acquisition:

1. Skill name/id and capability fit;
2. directory/search source where discovered (informational only);
3. canonical artifact owner/organization;
4. canonical repository or immutable artifact origin;
5. exact Skill path within the source when applicable;
6. whether the canonical owner is project-owned, platform-official, upstream-author or third party;
7. latest candidate revision only as a discovery pointer, then an immutable commit/release/digest for audit.

If the directory cannot lead to an inspectable canonical source with established ownership, reject the candidate before acquisition.

## Directory Signals

The following MAY help prioritize candidates but MUST NOT be treated as approval evidence:

- install/download counts;
- stars/forks;
- leaderboard/trending rank;
- community reviews;
- automated marketplace security badges/scans;
- directory verification labels;
- presence in more than one directory.

These signals can change audit priority or provenance confidence only. They never replace inspection of the exact artifact.

## Cross-Checking

When practical, cross-check a promising candidate against another directory/search source and the canonical repository to detect:

- typosquatting or lookalike owners/names;
- stale/mirrored copies;
- mismatched Skill paths;
- unexpected forks;
- ownership changes;
- inconsistent descriptions or install commands.

A cross-check improves discovery confidence; it does not elevate the artifact's trust tier by itself.

## Installation Command Rule

Commands offered by directories/CLIs such as `add`, `install`, `use`, one-click installation or equivalent are discovery convenience only during F3.

Do NOT execute them against the active agent/project before audit. Acquisition must go to quarantine/review and be pinned to the exact canonical revision/digest approved under `SKILL-SUPPLY-CHAIN.md`.

## Discovery Failure

Classify the capability `MISSING` when no candidate with resolvable provenance and acceptable audit potential can be found. Do not lower supply-chain requirements merely to make F3 pass.

## Maintenance

Known discovery-source names are operational hints, not immutable trust anchors. Strategy MAY add/remove/update discovery sources as the ecosystem changes without changing artifact approval semantics. A directory becoming compromised, abandoned or misleading is grounds to stop using it for discovery immediately.