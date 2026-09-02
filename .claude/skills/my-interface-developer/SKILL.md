---
name: my-interface-developer
description: Execute unfinished eligible tasks for the one project phase named by the Developer, resolving its target item and code boundary from the generated Understanding. Implements only; never plans, reviews, or interprets the human project definition.
argument-hint: "[phase-id]"
disable-model-invocation: true
---

# Execute unfinished tasks

Use the requested phase's current Task plan as the only execution queue. The invocation and live State contract authorize that phase; its target item supplies configuration and the code boundary but does not widen the scope.

## Developer guide

Before performing any other step, read [references/developer-guide.md](references/developer-guide.md) completely and apply it throughout this invocation. The guide may refine execution but cannot expand this Skill's live authority, task scope, or write boundaries.

## Refresh context

1. Resolve the one requested phase id in `$ARGUMENTS` from the current generated Understanding. Refuse an omitted, additional, or unknown phase rather than choosing one.
2. Resolve the phase's target item from that phase, then follow the live map to read the current State contract, Task file and governing Schema, target-item Policy, mapped item configuration, and contracts required for this invocation.
3. Enter and record this Skill's working mode only as the live State contract permits, for the requested phase and no other.
4. Determine unfinished eligible tasks only from `content.plans.<phase-id>`, using the current task definitions, states, dependencies, contracts, and protocols.
5. For each selected task, read the mapped contract, target-item configuration, declared paths, and surrounding implementation context required to execute and verify it.

## Execute tasks

Select work according to the current Task file and only within the requested phase. A task is executable only when the live Task rules say its work remains, all earlier project phases are complete, its dependencies and required contracts are satisfied, and the task provides enough current information to act without guessing.

Resolve the authorized code root and verification working directory from the requested phase target's current configuration, then resolve the task's declared paths relative to that code root. Inspect the relevant existing implementation before editing, but do not treat it as permission to widen the task or invent a requirement. Never infer, remember, or invent a destination folder.

Before changing code, follow the current claim protocol and persist the claim as required so concurrent work cannot select the same task. Implement only the selected task, only within its resolved write scope, and run its current verification in the configured context.

Record the actual result through the current Task and State mechanisms. A failed or missing verification is not completion. Re-read the Task file and relevant State after recording the result, then continue only while another unfinished eligible task exists in the same requested phase.

## No work and boundaries

If the live State contract refuses the requested phase, or no unfinished eligible task exists within it, do not change product code or select work from another phase, including another phase with the same target. Record an outcome only as the current authorities permit, report the exact reason, and stop.

Do not plan, reinterpret the project definition, review, reshape tasks, or modify generated Understanding merely to make execution possible. If a task becomes blocked by missing information, an unresolved destination, an unsatisfied requirement, or a verification failure, do not guess or silently abandon a claim; use the current Task and State mechanisms to record only what the live authorities allow, then report the exact reason.
