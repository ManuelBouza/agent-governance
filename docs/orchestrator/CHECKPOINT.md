# Current ChatGPT Orchestrator Checkpoint

Checkpoint-State: CURRENT  
Checkpoint-Sequence: O020  
Canonical-Branch: `develop`  
Chat-Closure: CONTINUE_ALLOWED

## Current Work Unit

T001, T002 and T003 remain `ACCEPTED` and integrated.

T004 — D032 agent-facing capability eval foundation — is `READY` on `develop` and has been launched to the Agente de IA Ejecutor. No final T004 executor handoff has been received yet.

T004 Task Contract:

`docs/tasks/T004-d032-agent-facing-capability-eval.md`

Expected T004 executor branch:

`eval/d032-agent-capability`

Expected T004 handoff:

`handoffs/T004-executor-handoff.json`

T004 remains governed by its existing contract. Later architecture work MUST NOT retroactively broaden or alter its running execution semantics.

## Newly Accepted Architecture — D033

The Human Owner identified a product requirement for AI-controlled terminal/system access with strict authorization over what the AI may and may not do locally or remotely.

ChatGPT researched and persisted:

- `docs/decisions/D033-execution-access-control-plane.md`;
- `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`.

D033 is `ACCEPTED` architecture but is not yet integrated into the Governance Core protocol.

The central invariant is:

```text
transport or credential possession != execution authority
```

An open terminal, shell, SSH connection, authenticated CLI, cloud token, private key or privilege mechanism is only a transport/capability mechanism. It does not authorize effects beyond the current **Execution Capability Envelope**.

## D033 Execution Capability Envelope

For material terminal/process/system access, authorization is defined by the applicable subset of:

- actor/execution role;
- exact target identity/environment/account/resource;
- effect classes;
- resource scope;
- privilege ceiling;
- credential source/use;
- network destinations/path;
- task/time/operation lifetime;
- rollback/recovery expectation;
- approval mode;
- audit/evidence requirement.

Authorization is effect-oriented rather than executable-name-oriented. Shells, scripts, `ssh`, cloud/database/cluster CLIs and child processes must not become routes to expand authority.

Child/nested execution may inherit only a subset of the parent envelope.

## D033 Approval Modes

### `ALLOW_TASK`

Routine local effects already inside the approved task boundary, such as repository inspection, task-owned branch mutation, repository-native verification and disposable synthetic state.

### `ALLOW_EXPLICIT`

Non-baseline effects that a persisted task/decision explicitly bounds by target, effect and privilege. The AI may choose technical commands autonomously inside that envelope.

### `REQUIRE_HUMAN`

Human approval is required by default for bounded operations materially involving:

- production mutation/deployment;
- root/administrator or equivalent high-impact privilege;
- workstation/system-global configuration;
- firewall/SSH/IAM/security-control changes;
- credential creation/rotation/revocation or broadened scope;
- destructive/irreversible actions;
- material production data/schema migrations;
- uncertain target/effect.

Approval is normally for a coherent bounded operation rather than every shell line. After approval, the AI still owns execution inside the approved envelope.

### `DENY`

Fail closed under the current authorization for conditions such as:

- unknown/mismatched target identity;
- bypassing host/service identity verification for convenience;
- unbounded privilege when only narrow privilege is justified;
- credential discovery/exfiltration/persistence outside approved sources;
- disabling security/audit/access controls merely to unblock execution;
- clone/project-local authority expanding into global workstation mutation;
- unapproved forwarding/pivot/multi-hop access;
- dynamically obtained executable content whose effects cannot be bounded;
- hiding required execution evidence.

## D033 Primary Solution Diagram

Dominant question: security-sensitive execution/control flow across local and remote trust boundaries.

Preferred primary view: DFD with trust boundaries.

```text
Human Owner
   │ approves scope/risk
   ▼
Strategy / Task Contract
   │
   │  Execution Capability Envelope
   ▼
┌──────── POLICY / AUTHORIZATION BOUNDARY ────────┐
│ target identity + effect + privilege + auth     │
│ ALLOW_TASK / ALLOW_EXPLICIT / HUMAN / DENY     │
└───────────────────┬─────────────────────────────┘
                    │ allowed
                    ▼
            Executor / Terminal
         ┌──────────┼───────────┐
         ▼          ▼           ▼
    local process   ssh/API    privileged op
         │          │           │
         └──────────┴─────┬─────┘
                          ▼
             OS/native enforcement
      sandbox · privilege · SSH/IAM controls
                          │
                          ▼
                 Local/Remote Resource
                          │
                          ▼
               sanitized audit evidence
                          │
                          ▼
                    Handoff/review
```

## D033 Security / Research Basis

D033 was informed by primary technical/security sources including:

- NIST SP 800-207 Zero Trust Architecture — no implicit trust based only on network location; authentication/authorization before resource access;
- NIST least-privilege and privileged-command definitions / SP 800-53 lineage;
- NIST Audit and Accountability concepts;
- OpenSSH native restrictions such as forced commands, user/principal restrictions, forwarding/destination restrictions and host-key verification;
- Linux `no_new_privs`;
- Linux seccomp filtering, with the explicit boundary that seccomp alone is not a complete sandbox.

D033 remains platform-neutral. It does not make OpenSSH, Linux, sudo, systemd, one cloud IAM system or one executor host a Governance dependency.

## D033 Native Enforcement Principle

For material risk, prefer platform-native enforcement over prompt-only trust when available.

Possible enforcement adapters include:

- restricted OS users/service accounts;
- narrow privilege policies;
- SSH forced/restricted commands/principals/forwarding;
- container/user-namespace/mount/network restrictions;
- `no_new_privs`/seccomp or other OS sandbox components;
- scoped cloud IAM roles;
- scoped database/cluster/deployment identities.

Governance defines authorization semantics; native systems enforce those semantics where practical.

## D033 Core-Integration Boundary

D033 deliberately does **not** modify `governance-core/` or the current protocol version while T004 is already running.

After T004 is reviewed, the leading planned architecture integration is a separate increment, tentatively T005, which should diagram and contract the smallest coherent change to add:

- `governance-core/EXECUTION-CONTROL.md`;
- progressive routing from `GOVERNANCE.md`;
- linkage from `EXECUTION.md` so READY does not imply unlimited terminal/system authority;
- Task Contract support for Execution Capability Envelopes;
- handoff evidence for material remote/privileged/system execution;
- deterministic policy/version/module tests;
- later adapter/dynamic security enforcement tests.

That task is not READY yet and must not be launched before T004 PD5 and its own D032 graphical/quality readiness work.

## T004 State

T004 remains the current executable frontier.

Its existing security boundary already provides a concrete narrow example of the D033 concept: child eval sessions run with tools denied, outside the source worktree, with synthetic prompts and bounded external model access. This is useful evidence but does not substitute for the general D033 Core integration.

T004 semantic grading remains `PENDING_CHATGPT` until its final handoff/transcripts are remotely reviewed.

## Active Remote Artifacts

- canonical `develop` at D033 planning start: `f7182fe06d0324be424617fc4764528704f51e4c`;
- T004 Task Contract: `docs/tasks/T004-d032-agent-facing-capability-eval.md`;
- D032 decision: `docs/decisions/D032-adaptive-intent-engineering-proxy-and-quality-envelope.md`;
- D033 decision branch: `docs/d033-execution-access-control`;
- D033 decision: `docs/decisions/D033-execution-access-control-plane.md`;
- D033 architecture overview: `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md`.

## Open Questions or Blockers

No D033 architecture blocker is currently known.

T004 still requires its executor result and PD5 before integration/semantic conclusions.

The source product remains not stable/release-ready. D033 Core integration, broader behavioral/security evals, property/state-machine coverage, Skill gates and release gates remain incomplete.

## Next Action

1. Review the D033 Markdown branch against current `develop`.
2. Confirm it changes only D033/architecture/checkpoint Markdown.
3. Merge the D033 Markdown PR into `develop` if clean.
4. Do not alter the running T004 contract.
5. When T004 returns, perform remote PD5 over its branch/handoff/results/transcripts.
6. After T004 is resolved, design the separate D033 Core-integration increment with a fresh Primary Solution Diagram, quality/security triage and Task Contract.

## Next Chat Minimum Load

After `AGENTS.md` and this checkpoint:

1. if T004 is still active/returned, load `docs/tasks/T004-d032-agent-facing-capability-eval.md` and its handoff/results as needed;
2. load `docs/decisions/D033-execution-access-control-plane.md` when terminal/local/remote execution control or the next Core-integration task is in scope;
3. load `docs/ARCHITECTURE-EXECUTION-ACCESS-CONTROL.md` only when a consolidated explanatory view is useful;
4. load D032/`QUALITY.md` only as needed for graphical/quality readiness or semantic T004 review.

## Do Not Load or Do

- Do not reopen T001/T002/T003 absent a concrete regression.
- Do not retroactively broaden or rewrite T004 because D033 was accepted while it was running.
- Do not interpret terminal/credential availability as authorization.
- Do not treat local execution as inherently trusted compared with remote execution.
- Do not authorize by executable name alone when target/effect/privilege changes meaning.
- Do not let child processes/scripts/SSH/CLIs expand beyond the parent capability envelope.
- Do not weaken project-native IAM/SSH/privilege/security/audit controls to simplify automation.
- Do not commit credentials, private keys, tokens, raw secret-bearing environment dumps or hidden reasoning.
- Do not update Core/protocol for D033 until a separate integrated Task Contract can also align deterministic verification.
- Do not declare the source product stable/release-ready from D033 or T004 alone.
