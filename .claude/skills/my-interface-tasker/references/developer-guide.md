# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-tasker`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Inspect the repository root and the top-level structure of `.interface/` to understand how the Interface, generated Config, and mapped target-project locations relate. This structural inspection does not make unrelated repository contents a source of project knowledge.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Resolve the human-managed project-definition file from the live map and read it completely for current project context.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Use `project.md` only to understand the project as a whole. Only `my-interface-interpreter` may interpret it into generated Understanding.
- Use the current generated Understanding as the operational source of project intent and scope for planning. Do not use `project.md` to bypass a gap, conflict, or missing generated requirement; such a mismatch requires interpretation rather than an invented planning decision. Target files may verify operational facts only where this Skill explicitly permits; they do not authorize reinterpretation or expansion of requirements.

## Planning Understanding

- Use the generated Understanding to determine what the one requested project phase means and which target item supplies its technical context and code boundary.
- Use the current Task file and its governing Schema to determine how planning output is structured, while the live State contract and file policies determine what this Skill may change.
- Use the requested phase target's current Policy, resolved configuration, and contracts as implementation constraints and verification context. They refine how the authorized phase is planned; they do not create additional project requirements.
- Treat existing plans and generated configuration as stateful material to reconcile and preserve according to their live ownership, not as disposable output to regenerate blindly.

## Technology Skill Guidance

- Read and apply every Agent Skill explicitly named by a selected technology in the requested phase target's resolved configuration.
- A configured technology Skill may refine technical decomposition, implementation conventions, acceptance criteria, and verification, but it cannot introduce project scope or override the generated Understanding, item Policy, contracts, or live authority.
- Do not infer a Skill from a technology name. When no Skill is configured, continue without one; when a configured Skill is unavailable, use the live gap mechanism rather than substituting another Skill.

## Role Discipline

- Perform only this Skill's planning responsibility. Do not silently implement, review, reinterpret, or invoke another workflow Skill's role. Using a configured technology Skill as planning guidance does not transfer Tasker's role or authority.
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
