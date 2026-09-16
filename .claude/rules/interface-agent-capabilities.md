# Synchronized Agent capability catalog

This file is the project-scoped Claude Runtime projection produced by explicit Agent Sync. It records the Skills the Agent Module declares and their native mappings, so the active Agent Native and its Agent Instances never inspect `.interface/agent/` during ordinary operation.

It is a reference projection, not a gate: a Skill is resolved against whatever is currently discoverable and usable in this Runtime, and this file never restricts which Skills an operation may use. A missing or unusable required entry is Runtime drift and must be reported; it never authorizes an Agent Module read or automatic Agent Sync.

## Interface-owned workflow Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.core_workflow.configure` | `/my-interface-configure` | Human or declared coordinator |
| `project_skills.core_workflow.planning` | `/my-interface-planning [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.developing` | `/my-interface-developing [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.reviewing` | `/my-interface-reviewer [phase-number ...]` | Human or declared coordinator |
| `project_skills.core_workflow.launch` | `/my-interface-launch` | Human or declared coordinator |

## Interface-owned supporting Skills

| Capability identifier | Native Skill | Invocation |
|---|---|---|
| `project_skills.supporting.implement` | `/my-interface-implement [phase-number ...]` | Explicit Human only |
| `project_skills.supporting.reset` | `/my-interface-reset [phase-number ... \| config \| complete]` | Explicit Human only |
| `project_skills.supporting.skill-installer` | `/my-interface-skill-installer` | Explicit Human only; one of two Agent Module readers, scoped to resolving Prepared/Installed capabilities |
| `project_skills.supporting.agent-sync` | `/my-interface-agent-sync <self \| module>` | Explicit Human only; one of two Agent Module readers, and the only one that repairs Runtime drift |

## Contextual Skills

Implementation Preferences name an associated Skill directly on the technical option that requires it. This table is a reference only: operations resolve the name against the Skills currently discoverable and usable in this Runtime — whether project-scoped, plugin-provided, or runtime-provided — never through this catalog, and a listed name is not itself proof that its option is currently selected or that the Skill is currently usable.

| Skill name | Named by | Activates | Requirement |
|---|---|---|---|
| `pydantic` | `development` Preferences, Python `modeling` package | when the modeling package is selected | required |
| `fastapi` | `development` Preferences, Python `api` package | when the api package is selected | required |
| `typer` | `development` Preferences, Python `cli` package | when the cli package is selected | required |
