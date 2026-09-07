# Agent Interface bootstrap

Agent Interface Skills and the Interface structure are independent. Changing either one must not require changing the other.

## Entry points

- `.interface/interface.md` is the canonical Interface document and file map.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

## Separation

- Do not hardcode or copy Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Read them from their current owners using the shared entry points.
- Each Skill contains only its own fixed role, specialized Workflow, and boundaries.
- The Interface may catalog Skill metadata, including a Skill's name, path, invocation, and short purpose.
- Change a Skill only when its own role or Workflow changes. A change to the Interface structure or target project must not require a Skill change.
