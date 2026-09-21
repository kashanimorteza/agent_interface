# Agent Module Guide

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent Native operates, realized only through explicit Agent Native Sync.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
   - **[Runtime](#runtime)**
   - **[Agent](#agent)**
   - **[Personality](#personality)**
   - **[Rule](#rule)**
   - **[Skill](#skill)**
   - **[Command](#command)**
   - **[Tool](#tool)**
   - **[Permission](#permission)**
   - **[Connection](#connection)**
   - **[Context](#context)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
   - **[What success means](#what-success-means)**
9. **[At a Glance](#at-a-glance)**





<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

The Agent Module is one of the three primary Interface Modules, alongside Target and Implementation. It is the Human-owned, Runtime-independent declaration of how an Agent operates: its behavior, Skills, Rules, limits, responsibilities, capabilities, and boundaries.

### Purpose

The Module exists so the Human defines the Agent once instead of creating a separate configuration for Claude, Codex, Copilot, or another Agent Native. The Human's complete view of Agent behavior is organized here through the Module's Components and can then be realized by different Native environments. The Module does not define the Target, the Implementation, or a Native vendor's files, commands, configuration format, or execution mechanism.

### How It Works

The Agent Module is composed of Components. Each Component has a Definition for its portable meaning and mandatory Principles, and a Preferences file for current selections and declarations. Preferences never override Principles.

Agent Sync is the only reader and bridge from the Module to the selected Agent Native. It reads the complete Module and realizes its meaning in the Native without changing its scope or authority. Other Skills and Agent Instances use the synchronized Native realization and do not read Module sources directly.

The Foundation File [Agent Native Sync](../foundation/agent-native-sync.md) instructs the selected Agent Native to create or update its Agent Native Sync Skill. In this project, that Skill is invoked through `/my-interface-agent-native`. When it runs, it reads this Module and realizes its current Components, declarations, and Principles in the Agent Native; therefore, changes made here take effect in a Native only through that synchronization.

To create or update the synchronization Skill, the Human tells the Agent:

```text
Read `.interface/foundation/agent-native-sync.md` completely and execute every instruction in it.

Use the selected Agent Native's official Agent Native Sync entry point. In this project, invoke `/my-interface-agent-native` according to the Foundation File. Preserve the authority and boundaries defined there. Do not read Target sources and do not modify `.interface/agent/`.

Report exactly what was done and whether synchronization completed successfully.
```

The Human invokes synchronization with `/my-interface-agent-native`; no mode or numeric argument is used.





<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Agent Module** — the portable, Human-owned declaration of how an Agent and its capabilities operate.
- **Agent Native** — the selected Runtime mechanism that realizes the Agent Module.
- **Agent Sync** — the Agent Native Sync Skill that reads the Agent Module and realizes it in the Native.
- **Component** — one bounded part of the Agent Module with its own Definition and Preferences.




<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The Agent Module is organized into bounded Components. Each Component has its own Definition and Preferences. Agent Sync transfers these Components to the selected Agent Native.

```text
Agent
└── Components
    ├── Runtime
    ├── Agent
    ├── Personality
    ├── Rule
    ├── Skill
    ├── Command
    ├── Tool
    ├── Permission
    ├── Connection
    └── Context
```

Agent Sync reads the complete Agent Module through its authorized Foundation instruction and realizes its Components in the selected Agent Native. Other operations use the synchronized Native realization and do not read Module sources directly.

Each Agent Component below has a Definition for meaning and Preferences for current declarations. Agent Native Sync is a Foundation File, not an Agent Component.

### Runtime

Runtime identity, provider, model, compatibility, and native capability mapping. Absorbs the former Settings Component (2026-09-17): Settings — Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation.

Responsibility: Runtime identity, provider, model, compatibility, and native capability mapping.

```yaml
definition: .interface/agent/runtime/definition.md
preferences: .interface/agent/runtime/preferences.yaml
```

→ [Definition](runtime/definition.md)<br>
→ [Preferences](runtime/preferences.yaml)

### Agent

The selected Agent Native and its General and Specialized Agent Instances. Absorbs the former Role, Coordination Components (2026-09-17): Role — Primary and specialized Agent Role contracts. Coordination — Delegation, teams, tasks, messaging, concurrency, and worktree isolation.

Responsibility: The selected Agent Native and its General and Specialized Agent Instances.

```yaml
definition: .interface/agent/agent/definition.md
preferences: .interface/agent/agent/preferences.yaml
```

→ [Definition](agent/definition.md)<br>
→ [Preferences](agent/preferences.yaml)

### Personality

The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order.

Responsibility: The personalities an Agent can take on, the Actions each performs, and the models each prefers in priority order.

```yaml
definition: .interface/agent/personality/definition.md
preferences: .interface/agent/personality/preferences.yaml
contracts: .interface/agent/personality/contracts/<personality>.md
```

→ [Definition](personality/definition.md)<br>
→ [Preferences](personality/preferences.yaml)<br>
→ [Contracts](personality/contracts/)

### Rule

Persistent global and scoped behavioral instructions. Absorbs the former Interaction, Observability, Session Components (2026-09-17): Interaction — Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior. Observability — Validation, status, diagnostics, evidence, logs, telemetry, health, and usage. Session — Lifecycle, resume, history, background work, isolation, checkpoints, and termination.

Responsibility: Persistent global and scoped behavioral instructions.

```yaml
definition: .interface/agent/rule/definition.md
preferences: .interface/agent/rule/preferences.yaml
contracts: .interface/agent/rule/contracts/<rule>.md
```

→ [Definition](rule/definition.md)<br>
→ [Preferences](rule/preferences.yaml)<br>
→ [Contracts](rule/contracts/)

### Skill

Reusable knowledge and workflows, including all declared Agent Skills.

Responsibility: Reusable knowledge and workflows, including all declared Agent Skills.

```yaml
definition: .interface/agent/skill/definition.md
preferences: .interface/agent/skill/preferences.yaml
```

→ [Definition](skill/definition.md)<br>
→ [Preferences](skill/preferences.yaml)<br>

### Command

Named and slash invocation entry points, arguments, aliases, and routing.

Responsibility: Named and slash invocation entry points, arguments, aliases, and routing.

```yaml
definition: .interface/agent/command/definition.md
preferences: .interface/agent/command/preferences.yaml
```

→ [Definition](command/definition.md)<br>
→ [Preferences](command/preferences.yaml)

### Tool

Atomic built-in and externally provided executable capabilities.

Responsibility: Atomic built-in and externally provided executable capabilities.

```yaml
definition: .interface/agent/tool/definition.md
preferences: .interface/agent/tool/preferences.yaml
```

→ [Definition](tool/definition.md)<br>
→ [Preferences](tool/preferences.yaml)

### Permission

Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets. Absorbs the former Hook Component (2026-09-17): Hook — Deterministic event-driven lifecycle automation.

Responsibility: Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets.

```yaml
definition: .interface/agent/permission/definition.md
preferences: .interface/agent/permission/preferences.yaml
```

→ [Definition](permission/definition.md)<br>
→ [Preferences](permission/preferences.yaml)

### Connection

External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle. Absorbs the former Integration, Extension Components (2026-09-17): Integration — MCP, LSP, channels, application connectors, and external services. Extension — Plugins, marketplaces, capability packages, monitors, and extension lifecycle.

Responsibility: External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle.

```yaml
definition: .interface/agent/connection/definition.md
preferences: .interface/agent/connection/preferences.yaml
```

→ [Definition](connection/definition.md)<br>
→ [Preferences](connection/preferences.yaml)

### Context

Persistent instructions, Understanding, Memory, imports, loading, and compaction.

Responsibility: Persistent instructions, Understanding, Memory, imports, loading, and compaction.

```yaml
definition: .interface/agent/context/definition.md
preferences: .interface/agent/context/preferences.yaml
```

→ [Definition](context/definition.md)<br>
→ [Preferences](context/preferences.yaml)

Every Agent Component's Principles and Preferences are authoritative for that Component only. A runtime artifact not declared in the owning Preferences are an optional runtime capability; a required declaration not usable by the selected runtime is Agent Preferences gap.





<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumed by the Foundation Module** — its [Agent Native Sync](../foundation/agent-native-sync.md) instruction is the only authorized reader of the Agent Module and realizes it in the selected Agent Native.
- **Provides Agent meaning** — the Module's Component Definitions and Preferences provide the portable meaning and current declarations that Agent Sync transfers.




<br><br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Target meaning** — belongs to Target, because it describes the project being built rather than how the Agent operates.
- **Implementation engineering philosophy** — belongs to Implementation, because it describes how the project is built rather than how the Agent operates.
- **Generated Config shape** — belongs to the owning Schema or Preferences, because it describes an output artifact rather than Agent meaning.
- **Agent Native layout, commands, and configuration format** — belongs to Agent Sync, because it describes Native realization rather than the portable Agent Module.




<br><br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Each Agent Component has two files. `definition.md` states the portable view and philosophy; `preferences.yaml` holds current selections and declarations. Preferences never weaken a Principle. Definition files carry the portable prose that Agent Sync must preserve, while Preferences point to them and hold generic categories and selections.

Two conventions keep Preferences ready for synchronization without duplicating the Module's meaning: prose that Agent Sync must carry as written lives in its own Markdown file under the Component, and declarations are grouped by capability kind rather than by Agent Native location. Agent Sync interprets these declarations for the selected Native without changing their scope or meaning.





<br><br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns the Agent Module and is the only actor allowed to change its files. Agent Sync reads the Module read-only and realizes its declarations in the selected Agent Native. No other Skill, Agent Instance, Runtime, or Context reads or changes the Module.

Every Principle in this Guide is mandatory. Agent Preferences can never override a Principle, and a Native realization may only preserve or strengthen the Module's meaning, never weaken it.




<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Component's Definition carries its mandatory Principles. The Guide records the shared success condition for realizing those Principles without replacing them.

### What success means

Agent Sync has succeeded when it has understood the complete Module, transferred its meaning to the Agent Native without changing its scope or authority, and the Agent behaves accordingly. Existing files and loaded rules are not sufficient evidence; observed behavior must also conform to the Human's intent.





<br><br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

- **Human-owned** — the Agent Module is the portable source of the Agent's meaning and declarations.
- **Read-only** — only Agent Sync reads the Module.
- **Synchronized** — Agent Sync transfers its meaning to the Agent Native without changing its scope or authority.
