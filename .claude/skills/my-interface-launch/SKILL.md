---
name: my-interface-launch
description: Bring the developed Target online through the selected Platform Launch, verify readiness, and report access points.
disable-model-invocation: true
---

# Launch the Target

This file is the Claude Code adapter for the portable `launch` Skill Contract. Resolve and read that Contract through Agent Skill Preferences before acting; the Contract is authoritative for behavior and this adapter supplies runtime execution details.

## Role

Bring the developed Target online according to the current Platform authorities. Configure owns Environment preparation; Launch verifies that preparation, then owns runtime startup, connection, readiness verification, and access reporting.

## Workflow

Establish Interface Understanding from the canonical Interface document. Follow its routes to the shared Skill rules, then establish Target Understanding from the Human and Technical Definitions it locates under their declared precedence. Read the Platform Principles and Preferences, the operational records, and the public boundaries of the developed parts.

Resolve the selected Environment and Launch from explicit Target decisions first and Platform defaults second. If either selection has no valid definition, record the unresolved condition under State instead of inventing a runtime method.

Resolve the phases currently both enabled and ready for implementation, and confirm from State that their Development is complete. Treat incomplete Development as a truthful launch stoppage rather than bypassing it. Use recorded Review outcomes as evidence when available, but do not make Review a prerequisite unless the current Target or Platform explicitly requires it.

Apply the selected Launch definition:

1. Mark Launch as `launching` and append the corresponding State History Event.
2. Verify that Configure prepared the selected Environment and inspect the developed parts before changing runtime state. Do not perform Environment preparation here.
3. Perform the selected Launch stages and dependency order through each part's public boundary.
4. Preserve a part already running when it satisfies the required readiness check.
5. Verify the complete result and collect every verified Access Point.
6. Record `launched` and its selections and Access Points on success, or `failed` on failure, and append the outcome to State History.

Stop dependent startup after a failed prerequisite or readiness check. Preserve truthful runtime and State, and record Blockers or Open Questions when applicable.

## Boundaries

Perform only Launch's role. Do not perform another Interface Operation, define or modify Target intent, repair product code, edit human-owned Interface sources, or exercise authority over another Component's internal implementation.

## Report

Report the selected Environment and Launch, environment verification, startup result for each part, readiness evidence, verified Access Points, and unresolved Blockers or Open Questions.
