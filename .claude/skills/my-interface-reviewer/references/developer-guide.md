# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-reviewer`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- Do not read the human-managed project-definition file. Only `my-interface-interpreter` may read and interpret it.
- Review the requested phase against the current generated Understanding, its authorized plan, its target-item Policy and contracts, and required evidence. Target files may establish implementation facts but do not authorize new requirements or reinterpretation of project intent.

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
