# Agent Module

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
   - **[Components](#components)**
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

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent and its Agent Instances operate. It contains the reusable view of the Agent's behavior, Skills, Rules, limits, responsibilities, capabilities, and boundaries, independent of the selected Agent Native.

### Purpose

The Module exists so the Human defines the Agent once instead of repeating the same expectations for Claude Code, Codex, Copilot, or another Runtime. It does not define the Target, the Implementation, or a vendor's files, commands, configuration format, or execution mechanism.

### How It Works

The Agent Module is composed of Components. Each Component owns one responsibility and has a Definition for its portable meaning and mandatory Principles, and a Preferences file for current selections, declarations, resources, explicit empty categories, and optional Native hints. Preferences never override Principles.

Agent Sync is the only bridge from the Module to the selected Agent Native. It reads the complete Module, learns the Native's own documentation and capabilities, and places the Module content into the Native's structures. It carries declarations as authored and restates them only when the Native's idiom requires it without changing scope or meaning. Every other Skill and Agent Instance uses the synchronized Runtime realization and does not read Module sources directly.

Each declared capability has one Capability Realization Kind. Constructed capabilities are realized from portable sources such as Skill Contracts, Prepared capabilities preserve a Human-authored artifact, and Installed capabilities are provisioned from an external provider. Agent Sync realizes and verifies these capabilities, reports approximation when the Native cannot reproduce a concept exactly, and never lets a Native artifact become a second authority.

The Agent Module is therefore the portable source of what the Agent is and must do; the Agent Native owns where and how that declaration is realized.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Agent Module** — the portable, Human-owned declaration of how an Agent and its capabilities operate.
- **Agent Native** — the selected Runtime mechanism that realizes the Agent Module.
- **Agent Sync** — the Agent Native Skill that reads the Agent Module and realizes it in the Native.
- **Capability Realization Kind** — whether a capability is Constructed, Prepared, or Installed.
- **Component** — one bounded part of the Agent Module with its own Definition and Preferences.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

### Components

The Module has ten Components: Runtime, Agent, Personality, Rule, Skill, Command, Tool, Permission, Connection, and Context. On 2026-09-17 the Human reduced the earlier seventeen to these ten so that every Component is a general capability any Agent must honor, rather than a mechanism of one particular Agent Native. Role and Coordination merged into Agent; Interaction, Observability, and Session merged into Rule; Integration and Extension merged into Connection; Hook merged into Permission; Settings dissolved into the common Preferences Schema (its general rules) and Runtime (its Claude-specific mechanics). Nothing was dropped: every absorbed Principle keeps its former number in a note, and every absorbed Preferences lives under a named key of its new Preferences. The Agent Native chooses how to realize each concept with its own mechanisms; where the Human knows a particular Native well, the Preferences may suggest a realization under `settings.native.<agent-native>` — a hint that narrows discovery, never an authority. This set is the Human's default structure — the set that was sufficient to hold every view the Human had about an Agent. It is not a requirement that every Agent Native supports every Component. Agent Sync takes the Understanding of each Component and places it into whatever the selected Agent Native actually offers; a Component the Native cannot realize exactly is realized through the nearest equivalent and reported as approximated, and an explicitly empty category stays empty.

```text
Agent Components
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

The complete Agent Module is read exclusively during an explicit Agent Native Skill invocation. Agent Sync first learns the selected Agent Native's own documentation, conventions, capabilities, and limitations, then reads every Module source and Interface-owned Skill Contract, and realizes each required Rule, Constructed Skill, Agent Instance, Command, Setting, Hook, permission, integration, and other capability as a self-contained Runtime artifact. the install mode of the Agent Native Skill resolves any optional prepared Skill file by exact declared stable key: a matching prepared Markdown file supplies that Skill's preserved native instruction content and is materialized as a Prepared Skill, and a Skill under an external provider declaration is provisioned as an Installed Skill; a Skill with neither follows its Contract-based realization path through Agent Sync. Every other Skill, supporting Agent Instance, coordinator, startup routine, and Understanding workflow is forbidden from entering, resolving, or using Agent Module sources and consumes only the last synchronized Runtime realization. A changed Agent Module declaration remains dormant until the Human explicitly invokes Agent Sync.

Each Agent Component below has its own Definition and Preferences. A Definition defines the Component's mandatory philosophy, responsibilities, rules, and boundaries; Preferences define its current selections, resources, portable realization requirements, default settings, and optional per-Native realization hints.

### Runtime

Runtime identity, provider, model, compatibility, and native capability mapping. Absorbs the former Settings Component (2026-09-17): Settings — Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation.

```yaml
name: Runtime
  definition: .interface/agent/runtime/definition.md
preferences: .interface/agent/runtime/preferences.yaml
responsibility: Runtime identity, provider, model, compatibility, and native capability mapping; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](runtime/definition.md)<br>
→ [Preferences](runtime/preferences.yaml)

### Agent

The selected Agent Native and its General and Specialized Agent Instances. Absorbs the former Role, Coordination Components (2026-09-17): Role — Primary and specialized Agent Role contracts. Coordination — Delegation, teams, tasks, messaging, concurrency, and worktree isolation.

```yaml
name: Agent
  definition: .interface/agent/agent/definition.md
preferences: .interface/agent/agent/preferences.yaml
responsibility: The selected Agent Native and its General and Specialized Agent Instances; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](agent/definition.md)<br>
→ [Preferences](agent/preferences.yaml)

### Personality

The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order.

```yaml
name: Personality
  definition: .interface/agent/personality/definition.md
preferences: .interface/agent/personality/preferences.yaml
definitions: .interface/agent/personality/definitions/<personality>.md
definition_schema: .interface/foundation/schema/personality.md
responsibility: The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](personality/definition.md)<br>
→ [Preferences](personality/preferences.yaml)<br>
→ [Definitions](personality/definitions/)

### Rule

Persistent global and scoped behavioral instructions. Absorbs the former Interaction, Observability, Session Components (2026-09-17): Interaction — Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior. Observability — Validation, status, diagnostics, evidence, logs, telemetry, health, and usage. Session — Lifecycle, resume, history, background work, isolation, checkpoints, and termination.

```yaml
name: Rule
  definition: .interface/agent/rule/definition.md
preferences: .interface/agent/rule/preferences.yaml
definitions: .interface/agent/rule/definitions/<rule>.md
responsibility: Persistent global and scoped behavioral instructions; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](rule/definition.md)<br>
→ [Preferences](rule/preferences.yaml)<br>
→ [Definitions](rule/definitions/)

### Skill

Reusable knowledge and workflows, including core, supporting, and contextual Skills.

```yaml
name: Skill
  definition: .interface/agent/skill/definition.md
preferences: .interface/agent/skill/preferences.yaml
contracts: .interface/agent/skill/contracts/<interface-owned-skill>.md
files: .interface/agent/skill/files/<declared-skill-stable-key>[.md | /]
responsibility: Reusable knowledge and workflows, including core, supporting, and contextual Skills; the Definition and Process Component own the meaning, while Skill Preferences hold the Agent-side bridge to that Component
```

→ [Definition](skill/definition.md)<br>
→ [Preferences](skill/preferences.yaml)<br>
→ [Files](skill/files/)

The Skill directory in detail:

```text
skill/
├── definition.md       ← the shared Skill concept and guidance
├── preferences.yaml    ← Agent-side Skill declarations and Process bridges
└── files/               ← optional prepared Skill files, keyed by stable Skill key (declared; currently absent)
```

### Native

The Agent Native is the Agent's synchronization and Runtime mechanism, not a Skill. Its Contract is kept outside the Skill directory.

```yaml
name: Agent Native
  contract: .interface/agent/native/agent-native.md
responsibility: Synchronize the Agent Module with the selected Runtime and manage declared capability realization
```

→ [Contract](native/agent-native.md)

A Skill has exactly one Capability Realization Kind. A Process-backed Interface Skill is **Constructed** from its Process Component Definition, Process Preferences, and Agent Skill Preferences; Agent Sync builds the native Skill from those sources. A Skill with a matching prepared file is **Prepared** and a Skill from an external provider is **Installed**; both belong to the install mode of the Agent Native mechanism.

Three layers, each with one owner:

- **Definition** (`definition.md`) — the shared Skill concept and guidance: one bridge Contract per Process-backed Skill, proven availability, safe repeatability, one realization kind, and capability ownership.
- **Skill Preferences** (`preferences.yaml`) — the Agent-side bridge to the owning Process Component, including the Skill's invocation and Runtime boundary. Process meaning, behavior, inputs, outputs, authority, verification, idempotency, and stopping conditions are defined by that Component's Definition and Preferences.
- **Native adapter** (outside `.interface/`, for example `.claude/skills/<name>/SKILL.md`) — the synchronized, self-contained realization of the Contract in the selected Agent Native. It owns only runtime execution detail and never becomes a second authority.

When a conversation produces a new understanding of a Process-backed Skill, its durable meaning is recorded in the owning Process Component Definition or Preferences. The Agent Skill Preferences record only the bridge, invocation, and Runtime boundary. Optional prepared files live under `files/`; unmatched files are never installed by inference. External provider declarations belong to the provider that owns them. The adapter is brought into line by Agent Sync, never by hand — except for the Agent Native mechanism itself, once, at bootstrap.

Core Skills are Configure, Plan, Develop, Review, and Launch. They are available to the Human and declared coordinators, while autonomous activation is disabled. Implement is the explicit Human coordinator for that workflow and may invoke only those five Skills. Reset and Agent Native are explicit-Human-only and cannot be delegated or autonomously activated.

Prepared Skill content, when declared, is read from `.interface/agent/skill/files/<declared-skill-stable-key>.md` or the matching directory tree; an absent prepared artifact is not an error, and an unmatched artifact is never installed by inference. Optional external capabilities are Installed through their owning provider declaration; the current optional provider is `pydantic:pydantic`.

### Command

Named and slash invocation entry points, arguments, aliases, and routing.

```yaml
name: Command
  definition: .interface/agent/command/definition.md
preferences: .interface/agent/command/preferences.yaml
responsibility: Named and slash invocation entry points, arguments, aliases, and routing; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](command/definition.md)<br>
→ [Preferences](command/preferences.yaml)

### Tool

Atomic built-in and externally provided executable capabilities.

```yaml
name: Tool
  definition: .interface/agent/tool/definition.md
preferences: .interface/agent/tool/preferences.yaml
responsibility: Atomic built-in and externally provided executable capabilities; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](tool/definition.md)<br>
→ [Preferences](tool/preferences.yaml)

### Permission

Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets. Absorbs the former Hook Component (2026-09-17): Hook — Deterministic event-driven lifecycle automation.

```yaml
name: Permission
  definition: .interface/agent/permission/definition.md
preferences: .interface/agent/permission/preferences.yaml
responsibility: Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](permission/definition.md)<br>
→ [Preferences](permission/preferences.yaml)

### Connection

External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle. Absorbs the former Integration, Extension Components (2026-09-17): Integration — MCP, LSP, channels, application connectors, and external services. Extension — Plugins, marketplaces, capability packages, monitors, and extension lifecycle.

```yaml
name: Connection
  definition: .interface/agent/connection/definition.md
preferences: .interface/agent/connection/preferences.yaml
responsibility: External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](connection/definition.md)<br>
→ [Preferences](connection/preferences.yaml)

### Context

Persistent instructions, Understanding, Memory, imports, loading, and compaction.

```yaml
name: Context
  definition: .interface/agent/context/definition.md
preferences: .interface/agent/context/preferences.yaml
responsibility: Persistent instructions, Understanding, Memory, imports, loading, and compaction; the Principles are the authority, the Preferences hold selections, declarations, and optional native.<agent-native> realization hints
```

→ [Definition](context/definition.md)<br>
→ [Preferences](context/preferences.yaml)

Every Agent Component's Principles and Preferences are authoritative for that Component only. A runtime artifact not declared in the owning Preferences are an optional runtime capability; a required declaration not usable by the selected runtime is Agent Preferences gap.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- The Module consumes the selected Runtime, Target-independent Agent authorities, and the shared Interface sources required for realization.
- The Module is consumed by Agent Sync and by the synchronized Agent Runtime realization.
- [Interface](../interface.md) — canonical map and authority for the complete Agent Module.
- Agent Component Definitions and Preferences — the Module's mandatory meaning and current declarations, listed below.
- Component `definition.md` files — mandatory meaning and Principles for each Component.
- Component `preferences.yaml` files — current choices and declarations for each Component.
- [Agent Native Contract](native/agent-native.md) — the only Agent mechanism authorized to read the Agent Module directly.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Every view, rule, limit, and responsibility that concerns the Agent, and would remain true if the Target or the Implementation were replaced. A rule such as "never commit or push until the Human explicitly asks" is an Agent rule: it is a rule between the Human and the Agent, not a property of any project. The Module records it, and the Agent Native enforces it through whichever native mechanism it has (a permission rule, a hook, a persistent instruction).

What does not belong here: the meaning of the Target, the engineering philosophy of the Implementation, the shape of generated Config, and any vendor's file layout, command names, or configuration format. Such Native-specific hints belong only under `native.<agent-native>`.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Layering --->
## Layering

Each Agent Component has two files. `definition.md` states the portable view and philosophy; `preferences.yaml` holds current selections, declarations, and Native hints. Preferences never weaken a Principle. Definition files carry prose the Native must preserve, while Preferences point to them and hold generic categories and selections.

Three conventions keep Preferences ready for placement rather than rewriting: prose the Native must carry as written lives in its own Markdown file under the Component; declarations are grouped by capability kind rather than Native location; and a generic `selected` value carries any Native mechanism hint under `settings.native.<agent-native>`.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Authority --->
## Authority

### How the Module changes

Every decision about the Agent is first written into the Agent Module, in the Component that owns it. Nothing is written into the Agent Native by hand. Once the Module is updated, the Human invokes Agent Sync — `self` to let the Agent Sync adapter realize itself from its current Contract, then `module` to realize every other declaration — and the Agent Native is brought into conformance.

There is exactly one exception. The native Agent Sync adapter must exist before Agent Sync can run at all, so the first time — and only the first time — it is written by hand from its Contract. After that bootstrap, Agent Sync updates its own adapter and every other native artifact; no further manual native change is made.

Agent Sync leaves two traces in the Agent Native so that later runs and later readers can tell where synchronization stands: every realized Skill carries a fingerprint of the Module source it was built from, and one project-scoped synchronization record lists every declaration with its source, fingerprint, native artifact, status, mode, and time. A changed fingerprint proves that a realization is stale; an unchanged one never proves that it conforms — only a full comparison of source and realization does. Where those traces live and how they are written is a native detail owned by the Agent Sync adapter, not a Module declaration.

Only the Agent Native Skill reads this Module. Every other Skill, Agent Instance, coordinator, and startup routine consumes the last synchronized native realization and never enters `.interface/agent/`.

<br>





<br><br>
<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Component's Definition carries its mandatory Principles. The Guide records the shared success condition for realizing those Principles without replacing them.

### What success means

Agent Sync has succeeded when three things are true together:

1. it established a precise Understanding of the complete Module;
2. it transferred that Understanding into the Agent Native's configuration and mechanisms — the declared Skills exist there, the rules and limits are in force there, and the concept and view the Module expresses reached the Native in the best form the Native allows, placed as the Human wrote it and restated only where that served the Native, with any change of scope reported as approximated rather than hidden; and
3. the Agent then works the way the Human intended: it has understood how it must be configured and behaves accordingly.

The third condition is about behavior, not only about artifacts. A file that exists and a rule that is loaded are evidence for the second condition; only observed conduct is evidence for the third.

<br>





<br><br>
<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

- **Must** — keep portable Agent meaning in Component Definitions and current choices in Component Preferences.
- **Must** — enter the Agent Module through the authorized Agent Native Skill.
- **Must** — verify both realized artifacts and observed behavior.
- **Never** — let a Guide replace a Definition, Preferences file, or synchronized Runtime authority.

<br>
