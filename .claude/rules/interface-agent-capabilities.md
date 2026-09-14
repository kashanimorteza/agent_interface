# Synchronized Agent capability catalog

This file is the project-scoped Claude Runtime projection produced by explicit Agent Sync. The active Agent Native and its Agent Instances resolve Agent capability identifiers here; they never inspect `.interface/agent/` during ordinary operation. A missing or unusable required entry is Runtime drift and must be reported; it never authorizes an Agent Module read or automatic Agent Sync.

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
| `project_skills.supporting.agent-sync` | `/my-interface-agent-sync` | Explicit Human only; sole Agent Module reader |

## Contextual Skills

| Capability identifier | Native Skill | Activation | Required |
|---|---|---|---|
| `project_skills.contextual.fastapi` | `fastapi` at `.claude/skills/fastapi/SKILL.md` | When a current Developer or Target choice selects FastAPI | Conditional: required when selected |
| `project_skills.contextual.typer` | `typer` at `.claude/skills/typer/SKILL.md` | When a current Developer or Target choice selects Typer | Conditional: required when selected |
| `project_skills.contextual.library-skills` | `library-skills` at `.claude/skills/library-skills/SKILL.md` | When package-provided Skill management is relevant | No |
