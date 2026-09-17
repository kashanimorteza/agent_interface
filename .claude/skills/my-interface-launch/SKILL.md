---
name: my-interface-launch
description: Bring the completed Target online and prove it is reachable, activated explicitly by the Human or a declared coordinator, or after end-to-end orchestration establishes every current launch prerequisite; verify readiness and report access points.
argument-hint: "[api|logic|presentation|complete|all]"
metadata:
  contract: ".interface/agent/skill/contracts/launch.md"
  contract_sha256: "sha256:ef7a88d86731cd7caa0500b3b58beb2a74a29ceb12f07252d376487ef9befd5c"
  synced_at: "2026-09-17T18:39:11Z"
---

# Launch the Target

This file is the self-contained Claude Code realization of the portable `launch` contract synchronized by Agent Sync. Follow this adapter and synchronized Runtime rules; never read or resolve Agent Module sources.

## Invocation

Run only when the Human invokes `/my-interface-launch` or a declared coordinator Skill invokes this Skill through Claude Code's own `Skill` tool. Never activate yourself because a request merely looks relevant, and never run from a startup, resume, or automation routine. When a coordinator invokes this Skill, that invocation loads and executes this file as the Skill's own definition; it is never satisfied by another Skill reading this file and executing these steps inline, and never by delegating this Skill to a forked or subordinate agent that inherits the caller's context.

## Role

Bring the completed Target online: verify the selected Environment, start and connect completed parts through the selected Launch definition, verify readiness, and record usable Access Points. Configure owns Environment preparation; Development owns product repair; Launch never performs either.

## Input

Accept one optional Launch Scope token from `$ARGUMENTS`: `api`, `logic`, `presentation`, or `complete` (`all` is an accepted alias of `complete`). `logic` prepares or verifies the reusable Logic Component; `api` starts the API executable. If `$ARGUMENTS` is empty, ask the Human to choose one of these values before starting instead of assuming a scope. Reject any other token by listing the accepted values and asking for a corrected one.

Consume the selected scope together with Target and Platform selections, Platform authorities, State, the developed parts and their public interfaces, and observable runtime state.

## Workflow

Establish Interface Understanding from the canonical Interface document. Follow its routes to the shared Skill rules, then establish current Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Read the Platform Principles and Preferences, the applicable Platform Component Runtime Requirements, the operational State, and the public boundaries of the developed parts.

Resolve the selected Environment and Launch from explicit Target decisions first and Platform defaults second; never invent a missing definition. If either selection has no valid or compatible definition, record the unresolved condition under State and stop instead of inventing a runtime method.

Resolve the phases currently both enabled and ready for implementation, and confirm from State that their Development is complete. Treat incomplete Development as a truthful launch stoppage rather than bypassing it. Use recorded Review outcomes as evidence when available, but only treat Review as a required prerequisite when the current Target, Platform, or the invoking coordinator explicitly requires it.

Apply the selected Launch definition:

1. Mark Launch as `launching` and append the corresponding State History Event before any mutation.
2. Verify that Configure prepared the selected Environment and inspect the developed parts before changing runtime state. Do not perform Environment preparation here; stop if preparation is unverified.
3. Perform the selected Launch stages and dependency order through each part's public boundary, in the order the Launch definition declares.
4. Preserve a part already running when it satisfies the required readiness check, changing only runtime elements that do not currently satisfy the selected Launch.
5. Deliver every required binding through the parts' public boundaries only, without recording secrets.
6. Verify the complete composed result and every reported Access Point; report only independently verified Access Points.
7. Record `launched` with its selections and Access Points on success, or `failed` on failure, and append the outcome to State History.

Stop dependent startup after a failed prerequisite or failed readiness check. Preserve truthful runtime and State, and record Blockers or Open Questions under their owners when applicable.

## Boundaries

Perform only Launch's role: project runtime startup, connection, readiness, and shutdown actions required by the selected Launch Scope and Launch definition, writing only Launch-owned State and History. Do not perform another Interface Operation, prepare Environment or other runtime requirements, define or modify Target intent, repair product code, redefine a part's internals, edit human-owned Interface sources, or exercise authority over another Component's internal implementation.

Stop instead of proceeding when: the selected Environment or Launch is unresolved or incompatible; Environment preparation is unverified; required Development is incomplete; a prerequisite startup or readiness check fails; or a required binding cannot be delivered safely.

## Report

Report the selected Environment and Launch, environment verification, the startup-or-preservation outcome for each part, readiness evidence, verified Access Points, and unresolved Blockers or Open Questions under their owners.
