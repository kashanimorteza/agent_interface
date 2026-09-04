---
name: my-interface-developer
description: Execute eligible planned work for the one project phase named by the Developer. Implements and verifies only; never plans, reviews, or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Develop one project phase

Execute the unfinished eligible work for the project phase named in `$ARGUMENTS`.

## Bootstrap

Read `.interface/root.yaml`. This is the only Interface path this Skill may assume. Follow its current map and read order to discover every source, plan, authority, configuration, contract, code boundary, and verification context required for this run.

Re-read required sources on every invocation. Resolve the requested phase, executable work, destinations, permissions, coordination protocol, and completion rules only through current mapped files. Apply technology guidance supplied by the project Rules when relevant and available.

Do not rely on remembered paths, fields, task states, transitions, defaults, permissions, or decision rules. Use the human project definition for context only; the generated Understanding and authorized plan are the operational sources for implementation.

## Develop

Enter the required workflow state, select work, claim it, implement it, verify it, and record its actual outcome exactly as the live authorities and protocols require.

Inspect existing code within the authorized scope before editing. Apply technology guidance without widening the selected work. Derive all paths, allowed writes, required checks, and responses to ambiguity or failure from the current owning files.

Continue through eligible work in the requested phase while the live rules allow it. Never mark work complete without the verification required by its current contract.

## Boundaries

Develop only. Do not create or reshape plans, reinterpret project intent, review as another role, modify generated Understanding, or write outside the live code and record boundaries.

Report completed, skipped, and blocked work with observable verification and only the questions or blockers required by the current policies.
