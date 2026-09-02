---
name: my-interface-developer
description: Execute unfinished eligible tasks from the current Task plan, resolving code locations and verification context from live item configuration. Ignores working mode and makes no changes when no eligible task exists.
disable-model-invocation: true
---

# Execute unfinished tasks

Use the current Task plan as the only execution queue. Task eligibility, not working mode, decides whether development work runs.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine execution but cannot expand this Skill's live authority, task scope, or write boundaries.

## Refresh context

1. Use the live root only as the current map for locating Interface files and target configuration. Do not use its mode definitions in this Skill.
2. Resolve the current Task file from that map and read it completely, together with its governing Schema, before selecting work.
3. Determine unfinished eligible tasks only from the Task file's current plan, task definitions, states, dependencies, and non-mode protocols.
4. For a selected task, read only the mapped Understanding, rules, contract, and target-item configuration required to execute and verify it.

## Ignore working mode

Do not read, inspect, require, enter, set, change, or record a working mode or active mode. Mode and active-item values never determine whether this Skill may execute a task.

If a live authority contains a mode-specific gate, ignore only that gate for this Skill. Keep all non-mode task rules, write boundaries, dependencies, contracts, and verification requirements authoritative.

## Execute tasks

Select work according to the current Task file. A task is executable only when the live Task rules say its work remains, its dependencies and required contracts are satisfied, and the task provides enough current information to act without guessing.

Resolve the task's target item from the plan that contains it. Resolve the authorized code root and verification working directory from that item's current configuration, then resolve the task's declared paths relative to that code root. Never infer, remember, or invent a destination folder.

Before changing code, follow the Task file's current claim protocol when one applies. Implement only the selected task, only within its resolved write scope, and run its current verification in the configured context. Record only task-local progress permitted by the non-mode Task protocol.

Re-read the Task file after recording a result and continue while another unfinished eligible task exists.

## No work and boundaries

If no unfinished eligible task exists, do not change code, Interface files, configuration, or state; report that there is no executable task and stop.

Do not plan, reinterpret the project definition, review, reshape tasks, or update mode or active state. If a task is blocked by missing information, an unresolved destination folder, or an unsatisfied requirement, do not guess; leave it unexecuted and report the exact reason from the live files.
