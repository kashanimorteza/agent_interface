# Synchronized Agent capability catalog

This file is the project-scoped Claude Runtime projection produced by explicit Agent Sync. It records the Skills the Agent Module declares and their native mappings, so the active Agent Native and its Agent Instances never inspect `.interface/agent/` during ordinary operation.

It is a reference projection, not a gate: a Skill is resolved against whatever is currently discoverable and usable in this Runtime, and this file never restricts which Skills an operation may use. A missing or unusable required entry is Runtime drift and must be reported; it never authorizes an Agent Module read or automatic Agent Sync.

## Interface-owned workflow Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.core_workflow.configure` | `/my-interface-configure` | Human or declared coordinator |
| `project_skills.core_workflow.planning` | `/my-interface-planning [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.developing` | `/my-interface-developing [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.reviewing` | `/my-interface-reviewer [phase-number ...]` | Human or declared coordinator; may itself invoke Configure, Planning, and Developing |
| `project_skills.core_workflow.launch` | `/my-interface-launch` | Human or declared coordinator |

Core workflow Skills never activate autonomously merely because a request looks relevant.

## Interface-owned supporting Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.supporting.implement` | `/my-interface-implement [phase-number ...]` | Explicit Human only; declared coordinator of Configure, Planning, Developing, Reviewing, and Launch |
| `project_skills.supporting.reset` | `/my-interface-reset [phase-number ... \| config \| complete]` | Explicit Human only |
| `project_skills.supporting.skill-installer` | `/my-interface-skill-installer` | Explicit Human only; one of two Agent Module readers, scoped to resolving Prepared/Installed capabilities |
| `project_skills.supporting.agent-sync` | `/my-interface-agent-sync <self \| module>` | Direct explicit Human only; one of two Agent Module readers, and the only one that repairs Runtime drift |

## Installed provider Skills

Installed Skills are provider-owned and provisioned only by Skill Installer. Their presence here is not proof that they are currently usable; resolve them against the Skills discoverable in this Runtime, matching the declared name within a namespaced identifier.

| Capability identifier | Skill name | Provider | Activation | Required |
|---|---|---|---|---|
| `project_skills.installed.pydantic` | `pydantic` (discoverable as `pydantic:pydantic`) | plugin `pydantic@pydantic-skills` | implicit when relevant | no |

## Skills named by Implementation Preferences

Implementation Preferences may name an associated Skill directly on the technical option that requires it. Those names and their requirement levels belong to the Preferences, not to this catalog: read them from the current Implementation authorities and resolve each against the Skills currently discoverable and usable in this Runtime — project-scoped, plugin-provided, or runtime-provided.
