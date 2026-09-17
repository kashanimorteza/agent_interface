# Synchronized Agent capability catalog

Scope: global — this synchronized Runtime Rule loads for all work in this project.

This file is the project-scoped Claude Runtime projection produced by explicit Agent Sync. It records the Skills the Agent Module declares and their native mappings, so the active Agent Native and its Agent Instances never inspect `.interface/agent/` during ordinary operation.

It is a reference projection, not a gate: a Skill is resolved against whatever is currently discoverable and usable in this Runtime, and this file never restricts which Skills an operation may use. A missing or unusable required entry is Runtime drift and must be reported; it never authorizes an Agent Module read or an automatic `/my-interface-agent-native` invocation.

## Interface-owned workflow Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.core_workflow.configure` | `/my-interface-configure` | Human or declared coordinator |
| `project_skills.core_workflow.planning` | `/my-interface-planning [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.developing` | `/my-interface-developing [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.reviewing` | `/my-interface-reviewer [phase-number ...]` | Human or declared coordinator; records Findings with their owning operation and invokes no other Skill |
| `project_skills.core_workflow.launch` | `/my-interface-launch` | Human or declared coordinator |

Core workflow Skills never activate autonomously merely because a request looks relevant. A coordinator invokes one only through Claude Code's own `Skill` tool, so the invoked Skill loads and executes its own definition; reading its file and running it inline, or handing it to a forked or subordinate agent, is never an invocation. Coordinator invocation never expands the invoked Skill's scope, authority, or stopping conditions.

## Interface-owned supporting Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.supporting.implement` | `/my-interface-implement [phase-number ...]` | Explicit Human only. The selected implementation coordinator and the only declared coordinator: it owns the Planning → Developing → Reviewing loop and may invoke Configure, Planning, Developing, Reviewing, and Launch, each retaining ownership of its own records and outputs |
| `project_skills.supporting.reset` | `/my-interface-reset [phase-number ... \| config \| complete]` | Explicit Human only |
| `project_skills.supporting.agent-native` | `/my-interface-agent-native <1=sync self \| 2=sync component \| 3=install>` | Direct explicit Human only — never by a model, Skill, coordinator, Hook, or automation. The only Agent Module reader: modes `1` and `2` are Agent Sync and the only path that repairs Runtime drift; mode `3` installs Prepared and Installed capabilities and never repairs drift |

Implement's coordination scope: Configure once when no phase was selected or when a Finding names it; Planning, Developing, and Reviewing per selected phase, repeated while Review records Findings and progress continues; Launch when every enabled and ready phase is assured.

## Agent Instances

| Agent Instance | Native realization | Role and capabilities |
|---|---|---|
| `general` | The Claude Code primary agent (runtime-provided) | Primary execution Role; accountable to the Human for the complete authorized request |
| `interface-reader` | Project agent `interface-reader` | Read-only Interface status reporting; tools Read, Grep, Glob; no write authority |

## Installed provider Skills

Installed Skills are provider-owned and provisioned only by `/my-interface-agent-native 3`. Their presence here is not proof that they are currently usable; resolve them against the Skills discoverable in this Runtime, matching the declared name within a namespaced identifier.

| Capability identifier | Skill name | Provider | Activation | Required |
|---|---|---|---|---|
| `project_skills.installed.pydantic` | `pydantic` (discoverable as `pydantic:pydantic`) | plugin `pydantic@pydantic-skills` | implicit when relevant | no |

No Prepared Skill is currently declared.

## Skills named by Implementation Preferences

Implementation Preferences may name an associated Skill directly on the technical option that requires it. Those names and their requirement levels belong to the Preferences, not to this catalog: read them from the current Implementation authorities and resolve each against the Skills currently discoverable and usable in this Runtime — project-scoped, plugin-provided, or runtime-provided.
