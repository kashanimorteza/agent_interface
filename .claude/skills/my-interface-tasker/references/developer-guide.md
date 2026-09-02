# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-tasker`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Inspect the repository root and the top-level structure of `.interface/` to understand how the Interface, generated Config, and mapped target-project locations relate. This structural inspection does not make unrelated repository contents a source of project knowledge.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Do not read the human-managed project-definition file. Only `my-interface-interpreter` may read and interpret it.
- Use the current generated Understanding as the source of project intent and scope for planning. Target files may verify operational facts only where this Skill explicitly permits; they do not authorize reinterpretation or expansion of requirements.

## Planning Understanding

- Use the generated Understanding to determine what the one requested project phase means and which target item supplies its technical context and code boundary.
- Use the current Task file and its governing Schema to determine how planning output is structured, while the live State contract and file policies determine what this Skill may change.
- Use the requested phase target's current Policy, resolved configuration, and contracts as implementation constraints and verification context. They refine how the authorized phase is planned; they do not create additional project requirements.
- Treat existing plans and generated configuration as stateful material to reconcile and preserve according to their live ownership, not as disposable output to regenerate blindly.

## Role Discipline

- Perform only this Skill's planning responsibility. Do not silently implement, review, reinterpret, or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by the Skill and live Interface.
- Apply this guide as planning guidance, never as permission to widen the requested scope, write boundary, or authority.
- If this guide conflicts with a live policy, authority, Schema, contract, or safety boundary, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current mapped evidence over memory or inference.
- Produce the smallest complete plan that satisfies the authorized scope and current task standard.
- Plan only the phase id named by the invocation. Never widen the run to another phase, even when it has the same target item.
- Do not invent missing requirements, priorities, dependencies, contracts, verification, or acceptance criteria.

## Reporting

- Ground the plan and outcome in current mapped sources and validation results.
- Distinguish planned, preserved, blocked, and unresolved content, and identify any decision that remains with the Developer.
