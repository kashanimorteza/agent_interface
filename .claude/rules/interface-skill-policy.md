# Agent Interface Skill policy

These shared rules apply to every Agent Interface Skill and supporting agent, including one written later. Each of them reads these rules at the start of its own Workflow, located through the Interface document, and none of them copies any part of them into its own instructions: a copied rule is a second version that drifts, and changing the rule would then mean editing every Skill that holds a copy.

## Human-owned files

Skills and supporting agents must never edit or delete a human-owned Interface source. The Interface document states which sources those are, and a YAML source additionally declares it in its own policy. Resolve the current set from there rather than from a list held here, because a list of paths goes stale the moment a source is renamed or added, and a stale list leaves a source unprotected without anyone noticing.

Only a human edits these sources. When a change appears necessary, report it and leave the source unchanged.

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
