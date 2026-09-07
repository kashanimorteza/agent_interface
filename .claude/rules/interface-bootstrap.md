# Agent Interface bootstrap

Agent Interface Skills and the Interface structure are independent. Changing either one must not require changing the other. This independence is what lets the Interface be handed to a different Agent, and a Skill to a different project, without either being rewritten.

## Entry points

- `.interface/interface.md` is the canonical Interface document and file map, and the single entry point every Skill and supporting Agent starts from. Everything else — including these rules — is located through it.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read a located resource before relying on it. A resource that still exists may have changed its content, its fields, or its meaning since it was last read, and what an earlier run knew about it is not evidence about the current version.

## Separation

- Do not hardcode or copy Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Read them from their current owners using the shared entry points. The same applies to an external capability a Skill uses: name what it must achieve and how to discover the current way of achieving it, rather than freezing one tool's commands, options, or catalog names into the Skill.
- The Interface may catalog Skill metadata: a Skill's name, path, invocation, the Workflow Mode it executes, and a short statement of what it is for. The catalog exists so that the Interface can route work to a Skill without knowing how that Skill works, which is why the traffic runs one way — the Interface may describe a Skill, while a Skill stores nothing about the Interface. The catalog is a pointer, never a second copy: it carries no part of a Skill's Workflow, boundaries, or report format, and when the catalog and the Skill disagree, the Skill is correct.
- Change a Skill only when its own role or Workflow changes. A change to the Interface structure or target project must not require a Skill change. When one does, the Skill was holding a copy of something it should have been reading: treat the forced edit as the symptom, and remove the copy rather than only updating it.
