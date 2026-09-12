# Agent Interface Skill policy

These shared rules apply to every Agent Interface Skill and supporting agent, including one written later. Each of them reads these rules at the start of its own Workflow, located through the Interface document, and none of them copies any part of them into its own instructions: a copied rule is a second version that drifts, and changing the rule would then mean editing every Skill that holds a copy.

The Agent Component Principles and Profiles located by the Interface document are the authorities for the common Agent contract and selected Agent Profile. This Rule applies those contracts to the current Agent Runtime and adds only the project restrictions stated below.

## Root project README

Skills and supporting agents must never read the content of the `README.md` located at the project root. This restriction applies only to that root project README, including for discovery, setup, understanding, documentation, or supporting evidence. README files inside Components, packages, or other subdirectories may be read and used as documentation for their own scope.

## Interface protection

The complete `.interface/` tree is read-only to every Skill and supporting agent by default. This protection applies to current and future files and directories without requiring a path list.

The only mutable exception is `.interface/foundation/config/`. A Skill may change an exact Config record there only when the Interface gives that Skill write authority and the record's owning Component permits the change. The exception never grants general Config write access and never reaches a sibling, parent, or other Interface path.

Never edit, overwrite, rename, move, truncate, replace, or delete a protected Interface path. Do not run a command, script, formatter, generator, reset, cleanup, or bulk operation whose resolved write targets could include one. Exclude protected paths before execution and verify them afterward when a broader operation could reach them. When a protected-source change appears necessary, report it and leave the source unchanged for direct Human authorship.

## Project-scoped capabilities

Install or configure every Skill, plugin, MCP integration, agent, or other project-specific Agent capability at project scope, with its required files stored in or declared by the repository so it travels with the project. Never use user scope for a project capability. If the current environment cannot provide a project-scoped installation, report that limitation and do not substitute a machine-local or user-scoped installation.

## Related capabilities

Check the Skills and capabilities already available in the environment for relevance to the current work. When applicable, read their instructions and use them within the active role and requested scope, respecting the project's resolved decisions and the current write boundaries.

A capability counts as available only when the active Agent can discover and use it in the current project. Files on disk, an installation receipt, or a configuration entry alone are not evidence that a Skill is loadable, a plugin is enabled, or an MCP server is connected. When activation, trust, authentication, reload, or restart is still required, report that condition rather than claiming the capability is ready.

When a relevant Skill recommends an alternative to the project's current choice, briefly explain the current choice, the proposed alternative, which Skill recommends it, and the reason for the recommendation. Ask the human whether to keep the current choice or adopt the alternative. Do not change the choice or proceed with work that depends on that decision until the human answers; independent work may continue. Apply an accepted alternative within the current role and write boundaries, reporting any required changes to human-owned sources.

## Decision policy

- Explicit project decisions, the applicable Principles, the declared interfaces between Components, permissions, and write boundaries are binding. They constrain professional judgment rather than being weighed against it: judgment settles what is undecided, never whether a decided thing still applies.
- When a necessary detail is not defined, choose the approach that best fits what is already binding, using the current role sources, available evidence, and professional judgment, then continue without asking. Record a choice that another operation would have to live with — a resolved technology, an interface shape, a stored structure — where that operation will find it, so that a decision made in passing does not later read as something the project always intended.
- A differing Skill recommendation requires the human decision described above. Otherwise, stop only when no safe choice can be made without materially affecting project intent, core architecture, security, data integrity, permissions, a declared interface, or an irreversible action. Always report the reason for stopping. When recording it is within the active role's write authority, also store it in the appropriate operational record under the owning Component's rules, so it remains available to later runs. When the role has no authority to record it, reporting is sufficient; this rule grants no additional write authority.
- Discretion never expands the active role, requested scope, or write authority. All three are fixed at invocation — the role by the Skill selected, the scope by what was asked for, the authority by the Component that owns the record — so none of them is something an operation discovers midway and grants itself. Work that turns out to be necessary but lies outside them is reported as necessary, not performed.
