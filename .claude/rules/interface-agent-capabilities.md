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
| `project_skills.supporting.skill-installer` | `/my-interface-skill-installer` | Explicit Human only |
| `project_skills.supporting.agent-sync` | `/my-interface-agent-sync <self \| module>` | Explicit Human only; sole Agent Module reader |

## Contextual Skills

The Agent Module currently declares none. Implementation Preferences name an associated Skill directly (for example `pydantic`, `fastapi`, `typer`), and operations resolve that name against the Skills currently discoverable and usable in this Runtime — whether project-scoped, plugin-provided, or runtime-provided.
