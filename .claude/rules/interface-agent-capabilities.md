<!-- managed by /my-interface-native-implement: Rule `interface-agent-capabilities` (scope: global — no paths frontmatter, applies to all work); contract: derived from the Executor Module Skill Definition, Skill Contracts, and Provider Skills — regenerated on every run, do not edit by hand -->

# Agent Interface capabilities

The realized Runtime capabilities of this project. Use these identifiers and Native mappings; never consult the Executor Module to resolve them. If one is missing or unusable, report Runtime drift with its Capability Status and ask the Human to run `/my-interface-native-implement`.

## Core Skills

Each Core Skill is a project Skill in `.claude/skills/<skill-name>/SKILL.md`, invoked as `/<skill-name>` or through the Skill tool.

| Stable key | Skill name | Inputs | Invocation |
|---|---|---|---|
| `configure` | `my-interface-configure` | request | Human or Agent |
| `plan` | `my-interface-plan` | request, optional phases | Human or Agent |
| `develop` | `my-interface-develop` | request, optional phases | Human or Agent |
| `review` | `my-interface-review` | request, optional phases | Human or Agent |
| `implement` | `my-interface-implement` | request, optional phases | Human or Agent — the coordinating Skill |
| `launch` | `my-interface-launch` | request, optional scope | Human or Agent |
| `reset` | `my-interface-reset` | request, exactly one scope | Human only (model invocation disabled) |

- Only Implement coordinates Core Skills, and it invokes only Configure, Plan, Develop, and Review. No Core Skill invokes another Core Skill otherwise. Every Core Skill may use any Provider Skill or other available Skill.
- Every Core Skill execution creates one Log Entry in State with its ID and Skill and updates that same Entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.
- State is an Operation Component, not a Skill.

## Provider Skills

Ready-made Skills copied unchanged into `.claude/skills/<name>/`; their content is taken as the provider supplies it and their requirements are realized only within Permission.

| Skill name | Use |
|---|---|
| `fastapi` | FastAPI APIs, Pydantic models, dependencies, streaming/SSE, serving frontend apps |
| `sqlmodel` | SQLModel models, sessions, queries, FastAPI integration, relationships, link models, CRUD |

## Agent Native Implement

`/my-interface-native-implement` realizes the Executor Module in Claude Code. Only the Human invokes it directly; no Agent, Skill, coordinator, hook, or automation may invoke it.
