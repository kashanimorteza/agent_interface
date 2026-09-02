# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-clear`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project requirements.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, deletion sets, or conclusions from an earlier run.

## Project Knowledge Boundary

- Do not read the human-managed project-definition file. Only `my-interface-interpreter` may read and interpret it.
- When target-project knowledge is needed, consume the current generated Understanding through the live map. Target files may confirm operational facts only where this Skill explicitly permits; they do not authorize reinterpretation of project intent.

## Role Discipline

- Perform only this Skill's clear/reset responsibility. Do not silently perform or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by the Skill and live Interface.
- Apply this guide as execution guidance, never as permission to widen a deletion set, write boundary, or authority.
- If this guide conflicts with a live policy, authority, or safety boundary, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current file evidence over memory or inference.
- Inspect and affect only the smallest scope required by the live operation.
- Do not invent missing decisions, paths, permissions, or recovery guarantees.

## Reporting

- Ground the result in current paths and observable outcomes.
- Distinguish removed, skipped, blocked, and unresolved items, and identify any decision that remains with the Developer.
