# Developer Guide

This guide defines the Developer's shared defaults for `my-interface-interpreter`. The Skill's live authorities and safety boundaries remain controlling.

## Understand the Interface

- At the start of every invocation, read the repository `README.md` completely to understand Agent Interface, its workflow, and this Skill's role. Treat it as Interface context, not as a source of target-project facts.
- Then read `.interface/root.yaml` as the Interface entry point and current map. Resolve every other path, read order, policy, authority, and boundary from the files currently named by that map.
- Re-read every required source from disk on every invocation. Do not rely on remembered paths, values, state, configuration, or conclusions from an earlier run.

## Project Knowledge Boundary

- This is the only workflow Skill authorized to read the human-managed project-definition file. Resolve that file from the live map and read it completely on every invocation.
- Treat the current human-managed definition as the source of target-project intent and facts. Use Schemas, policies, authorities, and existing generated files only for structure, validation, preservation, reconciliation, and permitted state behavior.
- Do not let implementation files, prior generated output, or remembered context silently add to or replace the Developer's definition.

## Role Discipline

- Perform only this Skill's interpretation responsibility. Do not silently plan, develop, review, clear, or invoke another Skill's role.
- Treat the Developer's invocation as authority only for the operation and exact scope defined by the Skill and live Interface.
- Apply this guide as interpretation guidance, never as permission to widen a write boundary or authority.
- If this guide conflicts with a live policy, authority, Schema, or safety boundary, stop and report the conflict instead of guessing.

## Working Defaults

- Prefer current source evidence over memory or inference.
- Read and write only the smallest scope required for a complete authorized interpretation.
- Preserve ambiguity as a recorded gap; do not convert it into an invented project decision.

## Reporting

- Ground the result in current mapped sources and validation outcomes.
- Distinguish generated, preserved, blocked, and unresolved content, and identify any decision that remains with the Developer.
