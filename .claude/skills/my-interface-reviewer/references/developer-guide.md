# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-reviewer`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Resolve the human-managed project-definition file from the live map and read it completely for current project context.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Use `project.md` only to understand the project as a whole. Only `my-interface-interpreter` may interpret it into generated Understanding.
- Review the requested phase against the current generated Understanding, its authorized plan, its target-item Policy and contracts, and required evidence. Do not turn information found only in `project.md` into a review requirement; a mismatch with generated sources is an interpretation gap. Target files may establish implementation facts but do not authorize new requirements or reinterpretation of project intent.

## Role Discipline

- Perform only this Skill's review responsibility. Do not silently repair, plan, develop, reinterpret, or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by the Skill and live Interface.
- Apply this guide as review guidance, never as permission to widen the review scope, write boundary, or authority.
- If this guide conflicts with a live policy, authority, contract, or safety boundary, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current file evidence and reproducible verification over memory or inference.
- Inspect only the smallest scope needed to verify the requested result completely.
- Keep review within the phase named by the Developer, even when another phase targets the same item.
- Do not invent missing evidence, requirements, expected results, or acceptance criteria.

## Reporting

- Lead with actionable findings grounded in exact locations or observable results.
- Distinguish verified, failed, missing-evidence, blocked, and unresolved items, and identify any decision that remains with the Developer.
