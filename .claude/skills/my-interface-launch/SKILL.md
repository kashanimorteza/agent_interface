---
name: my-interface-launch
description: Bring the completed Target online and prove it is reachable, activated explicitly by the Human or a declared coordinator, or after end-to-end orchestration establishes every current launch prerequisite; prepare the selected Launch Item's project-scoped Environment, verify readiness, and report Access Points.
argument-hint: "[api|logic|presentation|complete|all]"
metadata:
  contract: ".interface/agent/skill/contracts/launch.md"
  contract_sha256: "sha256:c29168fd794dda6cb931cde443f02b0e1b29833ec14febac30b15989ee61107e"
  synced_at: "2026-09-18T13:46:48Z"
---

# Launch the Target

This file is the self-contained Claude Code realization of the portable `launch` Skill Contract, placed here by Agent Sync as the Human authored it. Follow this file and the synchronized Runtime Rules under `.claude/rules/`; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-launch` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Purpose

Bring the completed Target online and prove that it is reachable.

## Responsibility

Prepare and verify the selected Environment for the selected Launch Item, start and connect completed parts through the selected Launch definition, verify readiness, and record usable Access Points. Launch owns Environment preparation within project scope; a system-level requirement it cannot satisfy is a Blocker for the Human. Development owns product repair.

## Trigger

Activate explicitly or after end-to-end orchestration establishes every current launch prerequisite.

## Inputs

Accept one optional Launch Scope selection: `api`, `presentation`, `logic`, or `complete` (the alias `all` is equivalent to `complete`). `logic` prepares or verifies the reusable Logic Component and `api` starts the API executable. When no scope is supplied, ask the Human to choose one of these values before starting. Consume the selected scope together with Target and Platform selections, Platform authorities, State, developed parts and public interfaces, and observable runtime state.

Claude Code input handling: the scope arrives as a single token in `$ARGUMENTS`. If `$ARGUMENTS` is empty, ask the Human to choose one of the accepted values before starting instead of assuming a scope. Reject any other token by listing the accepted values and asking for a corrected one.

## Outputs

Produce runtime startup or preservation outcomes, readiness evidence, Launch State and History, verified Access Points, and Blockers or Open Questions under their owners.

## Required Understanding

Establish Interface Understanding and current Target Understanding. Read Platform Principles and Preferences, operational State, and public boundaries of developed parts.

Claude Code routes: establish Interface Understanding from `.interface/interface.md` and the Foundation section files it links, then Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Follow its routes to the Platform Principles and Preferences, the applicable Platform Component Runtime Requirements, the State Config, and the public boundaries of the developed parts.

## Authority

Control only project runtime startup, connection, readiness, and shutdown actions required by the selected Launch Scope and Launch definition. Read the applicable Platform Component Runtime Requirements and perform the declared launch actions in their required order. Write Launch-owned State and History. Prepare only the declared, project-scoped runtime requirements of the selected Launch Item; never repair code or redefine a part's internals.

## Workflow Invariants

- Resolve Environment and Launch from explicit Target decisions first and Platform defaults second; never invent a missing definition.
- Launch only the parts included by the selected Launch Scope: `api`, `presentation`, `logic`, or `complete`/`all`.
- Require Development completion for every phase currently enabled and ready.
- Review is an additional prerequisite only when Target, Platform, or the invoking coordinator requires it.
- Mark Launch as launching before mutation and record the final truthful state afterward.
- Inspect the Environment before startup, apply only the missing declared project-scoped requirements of the selected Launch Item, record a Blocker for any system-level requirement the Human must provide, and verify preparation before starting anything.
- Follow declared dependency order and stop dependent startup after a failed prerequisite.
- Preserve a running part that already satisfies readiness.
- Deliver required bindings through public boundaries without recording secrets.
- Report only independently verified Access Points.

Claude Code execution detail: if the Environment or Launch selection has no valid or compatible definition, record the unresolved condition under State and stop instead of inventing a runtime method. Confirm from State that Development is complete for every phase currently enabled and ready, and treat incomplete Development as a truthful launch stoppage rather than bypassing it. Append the `launching` State History Event before any mutation, perform the selected Launch stages through each part's public boundary in the order the Launch definition declares, and record `launched` with its selections and Access Points on success or `failed` on failure, appending the outcome to State History.

## Verification

- Observe readiness for every launched or preserved part and verify the composed result and every reported Access Point.

## Idempotency

Repeated Launch preserves healthy running parts and changes only runtime elements that do not satisfy the current selected Launch.

## Stopping Conditions

- Stop when Environment or Launch is unresolved or incompatible, a required system-level preparation is missing, preparation is unverified, required Development is incomplete, a prerequisite startup fails, readiness fails, or a required binding cannot be delivered safely.

## Runtime Realization

A native adapter resolves concrete startup, shutdown, process, service, and health-check mechanisms from Platform and Runtime mappings and reports selections, environment verification, per-part startup, readiness, Access Points, and unresolved conditions.

In Claude Code this adapter reports, in this order:

1. **Selections** — the selected Launch Scope, Environment, and Launch definition.
2. **Environment** — each declared project-scoped requirement of the selected Launch Item, whether it was already satisfied or applied during the run, its verification result, and every system-level requirement recorded as a Blocker for the Human.
3. **Parts** — the startup-or-preservation outcome and readiness evidence for each part.
4. **Access Points** — every independently verified Access Point.
5. **Unresolved conditions** — Blockers and Open Questions under their owners, and what each prevents.
