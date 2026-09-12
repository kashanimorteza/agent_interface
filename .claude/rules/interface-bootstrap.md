# Agent Interface bootstrap

The Interface structure and native Agent implementations are independent of a particular Runtime layout. Portable Contracts for `my-interface-*` Skills belong to the Interface; their native Skills realize them as runtime adapters. External Skills remain provider-owned resources declared by the Profile. A Contract change may require adapter reconciliation, but never a redesign of Interface structure or a dependency on one vendor's implementation.

## Entry points

- `.interface/foundation/interface.md` is the canonical Interface document and file map, and the single entry point every Skill and supporting Agent starts from. Everything else — including these rules — is located through it.

Establish Interface Understanding from the Interface document alone. Then follow the routes and Agent Component read order it defines for the active role. Read every routed Principles and Profile source required to apply the Agent Profile; empty categories are declarations and must not be treated as missing. Use that Profile to locate the current native Rules, role instructions, and capabilities applicable to the work.

Use the Interface document to locate the current resources required by the active role. Do not assume that a resource exists merely because it existed in an earlier version of the Interface.

Read a located resource before relying on it. A resource that still exists may have changed its content, its fields, or its meaning since it was last read, and what an earlier run knew about it is not evidence about the current version.

## Separation

- Do not hardcode or copy Interface structure, values, fields, defaults, Policies, or project facts into a Skill. Read them from their current owners using the shared entry points. The same applies to an external capability a Skill uses: name what it must achieve and how to discover the current way of achieving it, rather than freezing one tool's commands, options, or catalog names into the Skill.
- The Agent Skill Component owns one portable Contract for every Interface-owned `my-interface-*` Skill. The catalog maps that Contract to a native implementation; it is a pointer and never a second copy. A native Interface Skill is a runtime adapter: it may define runtime-specific execution details but never override the Contract's responsibility, invariants, authority, verification, stopping conditions, or output obligations. When a native implementation disagrees with its Contract, the Contract is correct and the adapter is drifted. External Skills have no Interface-owned Contract and are used from their declared provider resource under the active Role and applicable Agent Principles.
- Change a Skill only when its own role or Workflow changes. A change to the Interface structure or target project must not require a Skill change. When one does, the Skill was holding a copy of something it should have been reading: treat the forced edit as the symptom, and remove the copy rather than only updating it.
