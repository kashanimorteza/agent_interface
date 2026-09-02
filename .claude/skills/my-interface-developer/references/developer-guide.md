# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-developer`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Inspect the repository root and the top-level structure of `.interface/` to understand how the Interface, generated Config, and mapped target-project locations relate. This structural inspection does not make unrelated repository contents a source of project knowledge.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, task state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Do not read the human-managed project-definition file. Only `my-interface-interpreter` may read and interpret it.
- Use the current generated Understanding and authorized Task plan as the project sources for development. Target files may confirm implementation facts only where the task and live authority permit; they do not authorize reinterpretation or expansion of project intent.

## Execution Understanding

- Use the current Task plan as the execution queue and source of the exact work requested; do not derive additional work from nearby code or general project goals.
- Use the generated Understanding to interpret the requested item's responsibility and the task's intended result.
- Use the selected item's current Policy, resolved configuration, and contracts to resolve implementation constraints, code location, environment, and verification context.
- Use the live State contract and file policies to determine scope, transitions, writable content, and how outcomes, blockers, and questions are recorded.
- Use target-project code as evidence of the current implementation only within the selected task's scope. A mismatch that requires changing the plan remains a planning issue rather than permission to reshape the task.

## Role Discipline

- Perform only this Skill's development responsibility. Do not silently plan, review, reinterpret, or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by the Skill, current Task plan, and live Interface.
- Apply this guide as execution guidance, never as permission to widen a task, write boundary, or authority.
- If this guide conflicts with a live policy, authority, contract, or safety boundary, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current file evidence over memory or inference.
- Inspect and change only the smallest scope required by the selected task.
- Keep execution within the item named by the Developer, even when another item's task is eligible.
- Persist coordination and progress records before relying on them, and leave every claimed task with an accurate outcome under the live protocols.
- Do not invent missing requirements, destinations, permissions, verification, or acceptance criteria.

## Reporting

- Ground the result in current paths, task records, and observable verification.
- Distinguish completed, skipped, blocked, and unresolved work, and identify any decision that remains with the Developer.
