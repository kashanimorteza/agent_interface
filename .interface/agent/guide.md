# Agent Module

This document explains the Agent Module: what it is, why it exists, how its parts relate, how it changes, and how its success is judged. It is Human-owned and records the Human's stated understanding so that this understanding is not lost between sessions or Agent Runtimes. The canonical Interface definition remains `.interface/interface.md`; this document explains, it does not redefine. Where the two disagree, the Interface file and each Component's Principles are correct.

<br>

## Purpose

Agent Interface is the interface between a developer and an AI Agent. The Agent Module is the layer inside it that holds everything about the Agent itself: its behaviors, skills, rules, restrictions, responsibilities, and view of the world. It is written once, independently of which Agent Native will run it — Claude Code, Codex, Copilot, or any other engine.

The Module does not know the Agent Native. A separate Skill, Agent Sync, establishes an Understanding of the complete Module and configures the Agent Native's own structure from that Understanding — Agent Sync is, in effect, the Native configuring itself, since it runs inside the Native. Because Agent Sync itself runs inside the Agent Native, the Native already knows where a rule belongs, where a skill belongs, and what documentation a skill must be built with. The Module owns *what* the Agent is; the Agent Native, through Agent Sync, owns *where and how* that is realized.


The Agent Module is the Human-owned, Runtime-independent home for the complete reusable view of how an Agent Native and its Agent Instances should operate. The Human declares that view once through its Components—including the Agent Native, Agent Instance identities, Roles, Rules, Skills, settings, capabilities, boundaries, and every other supported mechanism—rather than explaining the same expectations separately to Claude Code, Codex, or each later Agent Runtime. Each Agent Component owns one responsibility and has Principles for its mandatory portable contract and a Profile for its current choices, resources, portable realization requirements, and explicit empty categories.

The Agent Module expresses our general understanding, philosophy, rules, responsibilities, boundaries, and desired behavior for an Agent. It is an independent declaration and is not written for Claude Code, Codex, or any other specific Agent Native. It does not define the Target and does not prescribe a vendor's files, directories, command names, configuration format, or implementation mechanism. An Agent Native reads this portable Module through explicit Agent Sync, understands its own runtime documentation and capabilities, and translates the Module into the native structures it supports. The meaning and authority come from the Agent Module; the concrete runtime form comes from the Agent Native.

Every capability the Module declares has exactly one Capability Realization Kind, and that Kind decides what Agent Sync does with it. A Constructed capability is built by the Agent Native from a portable specification such as a Skill Contract. A Prepared capability is transferred into the Runtime unchanged from a complete Human-authored artifact. An Installed capability is provisioned by the Agent Native through its own native mechanism from an external source such as a marketplace, package registry, or MCP server, and is never built or transferred. This distinction applies to every Component, not only to Skills, so a newly declared capability of any kind has a defined place and a defined realization path. Because external sources differ by Agent Native, a declaration may carry optional per-Agent-Native identity for an Installed capability so the selected Native can locate and provision it. That identity helps the Native find an external artifact; it never prescribes the Native's own structure, format, or mechanism, and Agent Sync treats it as an aid rather than an authority.

Together, these Components form the Agent Profile within the complete Agent Module. Explicit Agent Sync is the only bridge from that reusable declaration to the currently selected compatible Runtime: it understands the complete Agent Module, learns the Native Runtime's own conventions, realizes the Module through that Runtime's Agent Native, Agent Instances, Rules, Skills, settings, and other capabilities, and verifies the result. The active Agent Native and its Agent Instances then operate from the synchronized Runtime realization without requiring the Human to restate the Agent philosophy.
<br>

## What belongs here

Every view, rule, limit, and responsibility that concerns the Agent, and would remain true if the Target or the Implementation were replaced. A rule such as "never commit or push until the Human explicitly asks" is an Agent rule: it is a rule between the Human and the Agent, not a property of any project. The Module records it, and the Agent Native enforces it through whichever native mechanism it has (a permission rule, a hook, a persistent instruction).

What does not belong here: the meaning of the Target, the engineering philosophy of the Implementation, the shape of generated Config, and any vendor's file layout, command names, or configuration format.

<br>

## Principles and Profiles

Each Agent Component has two files.

- `principles.md` states the Human's view and philosophy of that Component. It contains no technology, package, provider, or Agent Native. It is portable: the same file can be handed to another project or another Agent unchanged.
- `profile.yaml` holds the parameters that support that view: current selections, declared resources, explicit empty categories, and — when a view needs a helper for one Agent Native — a block declared for that Native only (for example `native.claude`). A Profile is in effect a preferences file; it never weakens a Principle.

When the Agent Native changes, Principles stay as they are. Only the Native-specific helper blocks in Profiles may change.

<br>

## Components

The Module currently has seventeen Components: Runtime, Settings, Context, Role, Agent, Coordination, Skill, Command, Rule, Tool, Hook, Integration, Extension, Interaction, Permission, Observability, and Personality. Personality was added on 2026-09-17; it absorbs what were briefly separate Action and Route ideas: each personality declares who it is, the Actions it performs, and the models it prefers in priority order. This set is the Human's default structure — the set that was sufficient to hold every view the Human had about an Agent. It is not a requirement that every Agent Native supports every Component. Agent Sync takes the Understanding of each Component and places it into whatever the selected Agent Native actually offers; a Component the Native cannot realize is reported, and an explicitly empty category stays empty.

```text
Agent Components
├── Runtime
│   ├── Principles  → .interface/agent/runtime/principles.md
│   └── Profile     → .interface/agent/runtime/profile.yaml
├── Settings
│   ├── Principles  → .interface/agent/settings/principles.md
│   └── Profile     → .interface/agent/settings/profile.yaml
├── Context
│   ├── Principles  → .interface/agent/context/principles.md
│   └── Profile     → .interface/agent/context/profile.yaml
├── Role
│   ├── Principles  → .interface/agent/role/principles.md
│   └── Profile     → .interface/agent/role/profile.yaml
├── Agent
│   ├── Principles  → .interface/agent/agent/principles.md
│   └── Profile     → .interface/agent/agent/profile.yaml
├── Coordination
│   ├── Principles  → .interface/agent/coordination/principles.md
│   └── Profile     → .interface/agent/coordination/profile.yaml
├── Skill
│   ├── Principles  → .interface/agent/skill/principles.md
│   ├── Profile     → .interface/agent/skill/profile.yaml
│   ├── Contracts   → .interface/agent/skill/contracts/<interface-owned-skill>.md
│   └── Files       → .interface/agent/skill/files/<declared-skill-stable-key>[.md | /]
├── Command
│   ├── Principles  → .interface/agent/command/principles.md
│   └── Profile     → .interface/agent/command/profile.yaml
├── Rule
│   ├── Principles  → .interface/agent/rule/principles.md
│   └── Profile     → .interface/agent/rule/profile.yaml
├── Tool
│   ├── Principles  → .interface/agent/tool/principles.md
│   └── Profile     → .interface/agent/tool/profile.yaml
├── Hook
│   ├── Principles  → .interface/agent/hook/principles.md
│   └── Profile     → .interface/agent/hook/profile.yaml
├── Integration
│   ├── Principles  → .interface/agent/integration/principles.md
│   └── Profile     → .interface/agent/integration/profile.yaml
├── Extension
│   ├── Principles  → .interface/agent/extension/principles.md
│   └── Profile     → .interface/agent/extension/profile.yaml
├── Interaction
│   ├── Principles  → .interface/agent/interaction/principles.md
│   └── Profile     → .interface/agent/interaction/profile.yaml
├── Permission
│   ├── Principles  → .interface/agent/permission/principles.md
│   └── Profile     → .interface/agent/permission/profile.yaml
├── Session
│   ├── Principles  → .interface/agent/session/principles.md
│   └── Profile     → .interface/agent/session/profile.yaml
├── Observability
│   ├── Principles  → .interface/agent/observability/principles.md
│   └── Profile     → .interface/agent/observability/profile.yaml
└── Personality
    ├── Principles  → .interface/agent/personality/principles.md
    ├── Profile     → .interface/agent/personality/profile.yaml
    └── Definitions → .interface/agent/personality/definitions/<personality>.md
```

The complete Agent Module is read exclusively during an explicit Agent Sync or Skill Installer invocation. Agent Sync first learns the selected Agent Native's own documentation, conventions, capabilities, and limitations, then reads every Module source and Interface-owned Skill Contract, and realizes each required Rule, Constructed Skill, Agent Instance, Command, Setting, Hook, permission, integration, and other capability as a self-contained Runtime artifact. Skill Installer resolves any optional prepared Skill file by exact declared stable key: a matching prepared Markdown file supplies that Skill's preserved native instruction content and is materialized as a Prepared Skill, and a Skill under an external provider declaration is provisioned as an Installed Skill; a Skill with neither follows its Contract-based realization path through Agent Sync. Every other Skill, supporting Agent Instance, coordinator, startup routine, and Understanding workflow is forbidden from entering, resolving, or using Agent Module sources and consumes only the last synchronized Runtime realization. A changed Agent Module declaration remains dormant until the Human explicitly invokes Agent Sync.

Each Agent Component below has its own Principles and Profile. Principles define the Component's mandatory philosophy, responsibilities, rules, and boundaries; Profiles define its current selections, resources, portable realization requirements, and default settings.

### Runtime

Runtime identity, provider, model, compatibility, and native capability mapping.

- [Principles](runtime/principles.md)
- [Profile](runtime/profile.yaml)

### Settings

Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation.

- [Principles](settings/principles.md)
- [Profile](settings/profile.yaml)

### Context

Persistent instructions, Understanding, Memory, imports, loading, and compaction.

- [Principles](context/principles.md)
- [Profile](context/profile.yaml)

### Role

Primary and specialized Agent Role contracts.

- [Principles](role/principles.md)
- [Profile](role/profile.yaml)

### Agent

The selected Agent Native and its General and Specialized Agent Instances.

- [Principles](agent/principles.md)
- [Profile](agent/profile.yaml)

### Coordination

Delegation, teams, tasks, messaging, concurrency, and worktree isolation.

- [Principles](coordination/principles.md)
- [Profile](coordination/profile.yaml)

### Skill

Reusable knowledge and workflows, including core, supporting, and contextual Skills.

- [Principles](skill/principles.md)
- [Profile](skill/profile.yaml)
- [Contracts directory](skill/contracts/)
- [Files directory](skill/files/)

### Command

Named and slash invocation entry points, arguments, aliases, and routing.

- [Principles](command/principles.md)
- [Profile](command/profile.yaml)

### Rule

Persistent global and scoped behavioral instructions.

- [Principles](rule/principles.md)
- [Profile](rule/profile.yaml)

### Tool

Atomic built-in and externally provided executable capabilities.

- [Principles](tool/principles.md)
- [Profile](tool/profile.yaml)

### Hook

Deterministic event-driven lifecycle automation.

- [Principles](hook/principles.md)
- [Profile](hook/profile.yaml)

### Integration

MCP, LSP, channels, application connectors, and external services.

- [Principles](integration/principles.md)
- [Profile](integration/profile.yaml)

### Extension

Plugins, marketplaces, capability packages, monitors, and extension lifecycle.

- [Principles](extension/principles.md)
- [Profile](extension/profile.yaml)

### Interaction

Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior.

- [Principles](interaction/principles.md)
- [Profile](interaction/profile.yaml)

### Permission

Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets.

- [Principles](permission/principles.md)
- [Profile](permission/profile.yaml)

### Session

Lifecycle, resume, history, background work, isolation, checkpoints, and termination.

- [Principles](session/principles.md)
- [Profile](session/profile.yaml)

### Observability

Validation, status, diagnostics, evidence, logs, telemetry, health, and usage.

- [Principles](observability/principles.md)
- [Profile](observability/profile.yaml)

### Personality

The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order.

- [Principles](personality/principles.md)
- [Profile](personality/profile.yaml)
- [Definitions directory](personality/definitions/)

Every Agent Component's Principles and Profile are authoritative for that Component only. A runtime artifact not declared in the owning Profile is an optional runtime capability; a required declaration not usable by the selected runtime is an Agent Profile gap.

<br>

## How the Module changes

Every decision about the Agent is first written into the Agent Module, in the Component that owns it. Nothing is written into the Agent Native by hand. Once the Module is updated, the Human invokes Agent Sync — `self` to let the Agent Sync adapter realize itself from its current Contract, then `module` to realize every other declaration — and the Agent Native is brought into conformance.

There is exactly one exception. The native Agent Sync adapter must exist before Agent Sync can run at all, so the first time — and only the first time — it is written by hand from its Contract. After that bootstrap, Agent Sync updates its own adapter and every other native artifact; no further manual native change is made.

Agent Sync leaves two traces in the Agent Native so that later runs and later readers can tell where synchronization stands: every realized Skill carries a fingerprint of the Module source it was built from, and one project-scoped synchronization record lists every declaration with its source, fingerprint, native artifact, status, mode, and time. A changed fingerprint proves that a realization is stale; an unchanged one never proves that it conforms — only a full comparison of source and realization does. Where those traces live and how they are written is a native detail owned by the Agent Sync adapter, not a Module declaration.

Only Agent Sync and Skill Installer read this Module. Every other Skill, Agent Instance, coordinator, and startup routine consumes the last synchronized native realization and never enters `.interface/agent/`.

<br>

## What success means

Agent Sync has succeeded when three things are true together:

1. it established a precise Understanding of the complete Module;
2. it transferred that Understanding into the Agent Native's configuration and mechanisms — the declared Skills exist there, the rules and limits are in force there, and the concept and view the Module expresses reached the Native in the best form the Native allows; and
3. the Agent then works the way the Human intended: it has understood how it must be configured and behaves accordingly.

The third condition is about behavior, not only about artifacts. A file that exists and a rule that is loaded are evidence for the second condition; only observed conduct is evidence for the third.

<br>

## Understanding record

The following questions were put to the Human and answered on 2026-09-17. They are recorded so that a later reader — Human or Agent Sync — can recover the intent behind the Module without reconstructing it.

**What is the Agent Module and why does it exist?**
The project is an interface between developer and Agent. A layer named Agent holds all behaviors, skills, and everything that concerns an Agent, so that no matter which Agent Native runs it, every view, rule, limit, and responsibility lives in one place. Agent Sync takes an Understanding of this Module and configures the Native's own structure from it; because Agent Sync runs inside the Native, the Native itself knows where each thing goes and how to build it.

**Where does a rule such as "never commit or push without an explicit request" belong?**
It is a rule between the Human and the Agent, and it can also be a rule inside the Agent Module so that no Skill or Instance commits or pushes until the Human directly asks.

**What is the difference between Principles and Profile?**
Principles express the view and philosophy of a Component and say nothing about technology, packages, or the kind of Agent. Profiles hold supporting parameters, including helpers for a specific Agent Native such as Claude, Copilot, or Codex; they are in effect preferences. The Human noted that the Implementation Module calls the equivalent file `preferences.yaml` and that the name `profile.yaml` is historical.

**Are the sixteen Components required for every Agent?** *(sixteen at the time of the answer; Personality became the seventeenth later the same day)*
No. They are the structure that was sufficient to hold every view the Human had. Agent Sync places the Understanding into whatever the selected Agent Native offers; the sixteen are a default, not an obligation on every Native.

**What does "Agent Sync succeeded" mean?**
That Agent Sync, from a precise Understanding of the Module, transferred everything into the Native's configuration and mechanisms as well as that Native allows — the Skills exist there, the concept and view reached it — and that in the end the Agent works the way the Human wants and has understood how it must be configured.

<br>

## Decisions taken

Recorded on 2026-09-17. Each was discussed with the Human, confirmed, and then written into the Module in the Component that owns it; the Agent Native was changed only through Agent Sync, except for the one-time hand bootstrap of the Agent Sync adapter.

- The `agent-sync` Skill Contract keeps the thirteen sections of the Skill Contract Schema in order; its former separate Understanding section was merged into Required Understanding.
- Prepared and Installed Skills belong to Skill Installer; Agent Sync realizes only Constructed Skills. The Interface file was aligned to say so.
- Every realized Skill carries a fingerprint of its source; a changed fingerprint proves staleness and an unchanged one never proves conformance (Agent Skill Principle 3, `agent-sync` Contract). The Agent Sync adapter may own a bounded helper that hashes, stamps, and writes the synchronization record but never judges conformance.
- Agent Sync records every run in one project-scoped synchronization record (`agent-sync` Contract, Outputs and Authority).
- The Agent Sync adapter carries each rule once; duplication inside the adapter is removed on the next `self` run.
- Rejected: a runtime-identity check in Agent Sync's Stopping Conditions, and declaring Codex as a second Runtime option now — both left for later.
- Personality is a Component of this Module (not of Foundation, not inside Runtime); it absorbs Action (what a personality does) and Route (which models it prefers, in order).
- Agent Sync, discussed in its own right (see `skill/guide.md`): Module Understanding starts from this guide; a declaration the Native cannot realize exactly is realized through the nearest equivalent, reported as `approximated`, and the run continues; unmanaged native capabilities are only reported; the restart notice is boxed; the two modes and the verify-until-converged loop stay.
- Hook Profile follows Permission on who may read the Module: the `agent-sync-read-grant` matcher and responsibility name both `agent-sync` and `skill-installer`. Confirmed; applied when the current review round is complete.

<br>

## Open decisions

Recorded on 2026-09-17 from the same review. Each is a Human decision that has not yet been taken; nothing here changes the Module until the Human decides.

- The boundary between Personality and Role: both name bounded execution identities (Role: `primary-execution`, `interface-reader`; Personality: `developer`, `planner`, `analyst`, `reviewer`, `architect`). Whether they are one concept or two is undecided.
- Personality, carried over from its first draft under Foundation: the full content and common structure of a definition file; whether every Personality pairs with one Action and whether the Interface-owned Skills (Planning, Developing, Reviewing, …) are the executors of Actions or something separate; the exact shape of a `models` entry (model identity, provider, fallback rule, conditions); whether routing is by Personality alone or by Personality and Action; and how Personality Model Preference relates to `runtime/profile.yaml` (`models`, `fallback_models`, `effort_levels`), which is currently empty. Who reads personalities is settled by placement: only Agent Sync, which realizes them in the Native.
- Whether `profile.yaml` keeps its name or becomes `preferences.yaml` to match the Implementation Module.
- Whether the third success condition — observed behavior — should become an explicit obligation in Agent Observability Principles or in the `agent-sync` Verification, with a stated form of evidence.
- Whether an explanatory Agent Rule about git commit and push should exist alongside the enforcing Permission `ask` rules.
- Native names that leaked into Profiles: `hook/profile.yaml` (event names, tool-name matchers, the `lifecycle_events` list), `agent/profile.yaml` (`allowed_tools` of `interface-reader`), and `settings/profile.yaml` (`source_precedence`). Either make them portable or move them under a `native.<agent-native>` block.
- Hook and Permission disagree about Skill Installer: Permission Principle 3 grants Agent Module reads to both `agent-sync` and `skill-installer`; the `agent-sync-read-grant` Hook declaration names only `agent-sync`. *Decided 2026-09-17 (see Decisions taken); pending application.*
- Permission Principle 3's At a Glance line names only `agent-sync`, while the Rule names both `agent-sync` and `skill-installer`.
- Output Style is selected in two places: `interaction/profile.yaml` selects `ADHD` as required, and `extension/profile.yaml` enables the `adhd-output-style` plugin that imposes its own style. One owner must be chosen.
- `context/profile.yaml` `target_precedence` does not state that the Technical Definition takes precedence on conflict, as `interface.md` does.
- `runtime/profile.yaml` `compatibility.required_profile_version: "1.0"` has no stated meaning while Profiles carry versions from 1.0 to 1.4.
