---
name: my-interface-developer
description: Development mode — execute the planned tasks for the project phase named by the Developer, following the current Config, Task standard, and verification gates. Use only after that phase has an authorized plan. Never plans or interprets the project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Execute one planned project phase

Implement the existing plan for the project phase named in `$ARGUMENTS`.

## Read before developing

1. Read `README.md` to understand Agent Interface, its workflow, and the Developer Skill's role. README content is system context only; never treat it as a target-project requirement.
2. Read `.interface/root.yaml` and follow its mappings, read order, mode boundaries, and authority references.
3. Read the live State contract before any state change or code write.
4. Read the current Task file and its governing Schema completely.
5. Resolve the requested phase from the generated Understanding and its existing plan, then read every mapped Config file required by that phase and its target.

Do not read `.interface/project.md`. The generated Config and existing plan are the complete sources for development.

## Phase scope

Exactly one project phase must be named. If it is missing, ambiguous, absent from the Understanding, or has no plan, stop and ask or use the configured gap mechanism. Do not select a phase or target implicitly and do not carry one over from an earlier run.

Enter development mode only as the live State contract authorizes for this invocation.

Execute tasks only from the requested project phase. Never continue into another phase merely because its tasks are ready. The phase is complete for this run when its own planned tasks are done or when its current Config and task protocols require the run to stop.

## Execution

Follow the Task file's current definitions for readiness, claiming, dependencies, contracts, permitted paths, status changes, logs, blockers, and completion. Follow the target Config for code location and verification context, and follow the project Rules for implementation boundaries.

Work on one task at a time. Claim it through the configured protocol before changing code, write only within the task's authorized scope, and run the task's own verification exactly where the Config requires. Record the result through the current Task and State mechanisms before selecting another task in the same phase.

Do not reproduce task fields, status values, transition identifiers, Config keys, file paths, or verification rules inside this Skill. Read them fresh from the files that own them.

If required information, authority, a contract, or a human decision is missing, do not guess or repair the plan. Record the gap as authorized and stop.

## Boundaries

Do not create, renumber, rewrite, or rescope plans or tasks. Do not enter another mode, implement another phase, alter a protected contract, or reinterpret the target project.

## Completion

Record the run outcome through the live State contract. Report the requested phase, tasks completed, verification results, and the exact blocker or remaining work that stopped the phase from completing.
