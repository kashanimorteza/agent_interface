# Synchronized Agent capability catalog

Scope: global — this synchronized Runtime Rule loads for all work in this project.

This file is the project-scoped Claude Code projection that explicit Agent Sync derives from the Agent Module's Skill Preferences and Command Preferences. It records the Skills the Agent Module declares, their capability identifiers, their Commands, and their Claude Code mappings, so the active Agent Native and its Agent Instances never inspect `.interface/agent/` during ordinary operation.

It is a reference projection, not a gate: a Skill is resolved against whatever is currently discoverable and usable in this Runtime, and this file never restricts which Skills an operation may use. A missing or unusable required entry is Runtime drift and must be reported; it never authorizes an Agent Module read or an automatic invocation of the Agent Native Skill.

## Interface-owned workflow Skills (Constructed)

| Capability identifier | Portable name | Native Skill | Invocation |
|---|---|---|---|
| `skills.core_workflow.configure` | `configure` | `/my-interface-configure` | Human or declared coordinator |
| `skills.core_workflow.planning` | `planning` | `/my-interface-planning [phase-number ...]` | Human or declared coordinator |
| `skills.core_workflow.developing` | `developing` | `/my-interface-developing [phase-number ...]` | Human or declared coordinator |
| `skills.core_workflow.reviewing` | `reviewing` | `/my-interface-reviewer [phase-number ...]` | Human or declared coordinator; records Findings with their owning operation and invokes no other Skill |
| `skills.core_workflow.launch` | `launch` | `/my-interface-launch` | Human or declared coordinator |

Each core workflow Skill declares `human_invocation: enabled`, `coordinator_invocation: enabled for declared coordinators`, and `autonomous_invocation: disabled`. Core workflow Skills never activate autonomously merely because a request looks relevant. A coordinator invokes one only through Claude Code's own `Skill` tool, so the invoked Skill loads and executes its own definition; reading its file and running it inline, or handing it to a forked or subordinate agent, is never an invocation. Coordinator invocation never expands the invoked Skill's scope, authority, or stopping conditions. No core Skill currently names a Personality (`personality: null`).

## Interface-owned supporting Skills (Constructed)

| Capability identifier | Portable name | Native Skill | Invocation |
|---|---|---|---|
| `skills.supporting.implement` | `implement` | `/my-interface-implement [phase-number ...]` | Explicit Human only. The selected implementation coordinator and the only declared coordinator: it may invoke `skills.core_workflow.configure`, `planning`, `developing`, `reviewing`, and `launch`, each retaining ownership of its own records and outputs |
| `skills.supporting.reset` | `reset` | `/my-interface-reset [phase-number ... \| config \| complete]` | Explicit Human only |
| `skills.supporting.agent-native` | `agent-native` | `/my-interface-agent-native <1=sync self \| 2=sync component \| 3=install>` | Direct explicit Human only — model, delegated, and automated invocation disabled; never by a Skill, coordinator, Hook, or automation. The only Agent Module reader: modes `1` and `2` are Agent Sync and the only path that repairs Runtime drift; mode `3` installs Prepared and Installed capabilities and never repairs drift |

Implement's coordination scope, as declared: Configure once when no phase was selected or when a Finding names it; Planning, Developing, and Reviewing per selected phase, repeated while Review records Findings and progress continues; Launch when every enabled and ready phase is assured. Its authority: delegated invocation only through the Native's own Skill invocation mechanism; each Skill retains ownership of its records and outputs. Implement owns the Planning → Developing → Reviewing loop; Reviewing records Findings and invokes nothing.

## Prepared Skills

No Prepared Skill is currently declared (explicit empty category). The prepared-file directory `.interface/agent/skill/files/` is declared and currently absent, which is not an error.

## Installed provider Skills

Installed Skills are provider-owned and provisioned only by the Agent Native Skill's install mode (`/my-interface-agent-native 3`). Their presence here is not proof that they are currently usable; resolve them against the Skills discoverable in this Runtime, matching the declared name within a namespaced identifier.

| Capability identifier | Skill name | Provider | Activation | Required |
|---|---|---|---|---|
| `skills.installed.pydantic` | `pydantic` (discoverable as `pydantic:pydantic`) | plugin `pydantic@pydantic-skills` from marketplace `pydantic-skills` (github `pydantic/skills`) | implicit when relevant | no |

## Commands

A Command's portable identity is its key and its arguments; the slash form is Claude Code's realization. Each Command maps to exactly one owning Skill and adds no workflow of its own. No alias is declared (explicit empty category).

| Command | Arguments | Owner | Claude Code invocation |
|---|---|---|---|
| `configure` | (none) | `skill.skills.core_workflow.configure` | `/my-interface-configure` |
| `planning` | `[phase-number ...]` | `skill.skills.core_workflow.planning` | `/my-interface-planning [phase-number ...]` |
| `developing` | `[phase-number ...]` | `skill.skills.core_workflow.developing` | `/my-interface-developing [phase-number ...]` |
| `reviewing` | `[phase-number ...]` | `skill.skills.core_workflow.reviewing` | `/my-interface-reviewer [phase-number ...]` |
| `launch` | (none declared; the owning Contract accepts an optional Launch Scope `api \| logic \| presentation \| complete \| all`) | `skill.skills.core_workflow.launch` | `/my-interface-launch` |
| `implement` | `[phase-number ...]` | `skill.skills.supporting.implement` | `/my-interface-implement [phase-number ...]` |
| `reset` | `[phase-number ... \| config \| complete]` | `skill.skills.supporting.reset` | `/my-interface-reset [phase-number ... \| config \| complete]` |
| `agent-native` | `<1=sync self \| 2=sync component \| 3=install>` | `skill.skills.supporting.agent-native` | `/my-interface-agent-native <1=sync self \| 2=sync component \| 3=install>` |

## Skills named by Implementation Preferences

Implementation Preferences may name an associated Skill directly on the technical option that requires it. Those names and their requirement levels belong to the Preferences, not to this catalog: read them from the current Implementation authorities and resolve each against the Skills currently discoverable and usable in this Runtime — project-scoped, plugin-provided, or runtime-provided.
