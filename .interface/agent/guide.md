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

The Module has ten Components: Runtime, Agent, Personality, Rule, Skill, Command, Tool, Permission, Connection, and Context. On 2026-09-17 the Human reduced the earlier seventeen to these ten so that every Component is a general capability any Agent must honor, rather than a mechanism of one particular Agent Native. Role and Coordination merged into Agent; Interaction, Observability, and Session merged into Rule; Integration and Extension merged into Connection; Hook merged into Permission; Settings dissolved into the Agent Profile Schema (its general rules) and Runtime (its Claude-specific mechanics). Nothing was dropped: every absorbed Principle keeps its former number in a note, and every absorbed Profile lives under a named key of its new Profile. The Agent Native chooses how to realize each concept with its own mechanisms; where the Human knows a particular Native well, the Profile may suggest a realization under `settings.native.<agent-native>` — a hint that narrows discovery, never an authority. This set is the Human's default structure — the set that was sufficient to hold every view the Human had about an Agent. It is not a requirement that every Agent Native supports every Component. Agent Sync takes the Understanding of each Component and places it into whatever the selected Agent Native actually offers; a Component the Native cannot realize exactly is realized through the nearest equivalent and reported as approximated, and an explicitly empty category stays empty.

```text
Agent Components
├── Runtime
│   ├── Principles  → .interface/agent/runtime/principles.md
│   └── Profile     → .interface/agent/runtime/profile.yaml
├── Agent
│   ├── Principles  → .interface/agent/agent/principles.md
│   └── Profile     → .interface/agent/agent/profile.yaml
├── Personality
│   ├── Principles  → .interface/agent/personality/principles.md
│   ├── Profile     → .interface/agent/personality/profile.yaml
│   └── Definitions → .interface/agent/personality/definitions/<personality>.md
├── Rule
│   ├── Principles  → .interface/agent/rule/principles.md
│   └── Profile     → .interface/agent/rule/profile.yaml
├── Skill
│   ├── Principles  → .interface/agent/skill/principles.md
│   ├── Profile     → .interface/agent/skill/profile.yaml
│   ├── Contracts   → .interface/agent/skill/contracts/<interface-owned-skill>.md
│   └── Files       → .interface/agent/skill/files/<declared-skill-stable-key>[.md | /]
├── Command
│   ├── Principles  → .interface/agent/command/principles.md
│   └── Profile     → .interface/agent/command/profile.yaml
├── Tool
│   ├── Principles  → .interface/agent/tool/principles.md
│   └── Profile     → .interface/agent/tool/profile.yaml
├── Permission
│   ├── Principles  → .interface/agent/permission/principles.md
│   └── Profile     → .interface/agent/permission/profile.yaml
├── Connection
│   ├── Principles  → .interface/agent/connection/principles.md
│   └── Profile     → .interface/agent/connection/profile.yaml
└── Context
    ├── Principles  → .interface/agent/context/principles.md
    └── Profile     → .interface/agent/context/profile.yaml
```

The complete Agent Module is read exclusively during an explicit Agent Native Skill invocation. Agent Sync first learns the selected Agent Native's own documentation, conventions, capabilities, and limitations, then reads every Module source and Interface-owned Skill Contract, and realizes each required Rule, Constructed Skill, Agent Instance, Command, Setting, Hook, permission, integration, and other capability as a self-contained Runtime artifact. the install mode of the Agent Native Skill resolves any optional prepared Skill file by exact declared stable key: a matching prepared Markdown file supplies that Skill's preserved native instruction content and is materialized as a Prepared Skill, and a Skill under an external provider declaration is provisioned as an Installed Skill; a Skill with neither follows its Contract-based realization path through Agent Sync. Every other Skill, supporting Agent Instance, coordinator, startup routine, and Understanding workflow is forbidden from entering, resolving, or using Agent Module sources and consumes only the last synchronized Runtime realization. A changed Agent Module declaration remains dormant until the Human explicitly invokes Agent Sync.

Each Agent Component below has its own Principles and Profile. Principles define the Component's mandatory philosophy, responsibilities, rules, and boundaries; Profiles define its current selections, resources, portable realization requirements, default settings, and optional per-Native realization hints.

### Runtime

Runtime identity, provider, model, compatibility, and native capability mapping. Absorbs the former Settings Component (2026-09-17): Settings — Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation.

- [Principles](runtime/principles.md)
- [Profile](runtime/profile.yaml)

### Agent

The selected Agent Native and its General and Specialized Agent Instances. Absorbs the former Role, Coordination Components (2026-09-17): Role — Primary and specialized Agent Role contracts. Coordination — Delegation, teams, tasks, messaging, concurrency, and worktree isolation.

- [Principles](agent/principles.md)
- [Profile](agent/profile.yaml)

### Personality

The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order.

- [Principles](personality/principles.md)
- [Profile](personality/profile.yaml)
- [Definitions directory](personality/definitions/)

### Rule

Persistent global and scoped behavioral instructions. Absorbs the former Interaction, Observability, Session Components (2026-09-17): Interaction — Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior. Observability — Validation, status, diagnostics, evidence, logs, telemetry, health, and usage. Session — Lifecycle, resume, history, background work, isolation, checkpoints, and termination.

- [Principles](rule/principles.md)
- [Profile](rule/profile.yaml)

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

### Tool

Atomic built-in and externally provided executable capabilities.

- [Principles](tool/principles.md)
- [Profile](tool/profile.yaml)

### Permission

Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets. Absorbs the former Hook Component (2026-09-17): Hook — Deterministic event-driven lifecycle automation.

- [Principles](permission/principles.md)
- [Profile](permission/profile.yaml)

### Connection

External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle. Absorbs the former Integration, Extension Components (2026-09-17): Integration — MCP, LSP, channels, application connectors, and external services. Extension — Plugins, marketplaces, capability packages, monitors, and extension lifecycle.

- [Principles](connection/principles.md)
- [Profile](connection/profile.yaml)

### Context

Persistent instructions, Understanding, Memory, imports, loading, and compaction.

- [Principles](context/principles.md)
- [Profile](context/profile.yaml)

Every Agent Component's Principles and Profile are authoritative for that Component only. A runtime artifact not declared in the owning Profile is an optional runtime capability; a required declaration not usable by the selected runtime is an Agent Profile gap.

<br>

## How the Module changes

Every decision about the Agent is first written into the Agent Module, in the Component that owns it. Nothing is written into the Agent Native by hand. Once the Module is updated, the Human invokes Agent Sync — `self` to let the Agent Sync adapter realize itself from its current Contract, then `module` to realize every other declaration — and the Agent Native is brought into conformance.

There is exactly one exception. The native Agent Sync adapter must exist before Agent Sync can run at all, so the first time — and only the first time — it is written by hand from its Contract. After that bootstrap, Agent Sync updates its own adapter and every other native artifact; no further manual native change is made.

Agent Sync leaves two traces in the Agent Native so that later runs and later readers can tell where synchronization stands: every realized Skill carries a fingerprint of the Module source it was built from, and one project-scoped synchronization record lists every declaration with its source, fingerprint, native artifact, status, mode, and time. A changed fingerprint proves that a realization is stale; an unchanged one never proves that it conforms — only a full comparison of source and realization does. Where those traces live and how they are written is a native detail owned by the Agent Sync adapter, not a Module declaration.

Only the Agent Native Skill reads this Module. Every other Skill, Agent Instance, coordinator, and startup routine consumes the last synchronized native realization and never enters `.interface/agent/`.

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

**Are the sixteen Components required for every Agent?** *(sixteen at the time of the answer; Personality became the seventeenth later the same day, and the set was then reduced to ten — see Components)*
No. They are the structure that was sufficient to hold every view the Human had. Agent Sync places the Understanding into whatever the selected Agent Native offers; the sixteen are a default, not an obligation on every Native.

**What does "Agent Sync succeeded" mean?**
That Agent Sync, from a precise Understanding of the Module, transferred everything into the Native's configuration and mechanisms as well as that Native allows — the Skills exist there, the concept and view reached it — and that in the end the Agent works the way the Human wants and has understood how it must be configured.

<br>

## Decisions taken

Recorded on 2026-09-17. Each was discussed with the Human, confirmed, and then written into the Module in the Component that owns it; the Agent Native was changed only through Agent Sync, except for the one-time hand bootstrap of the Agent Sync adapter.

- The `agent-native` Skill Contract keeps the thirteen sections of the Skill Contract Schema in order; its former separate Understanding section was merged into Required Understanding.
- Prepared and Installed Skills belong to the install mode of the Agent Native Skill; its sync modes realize only Constructed Skills. The Interface file was aligned to say so.
- Every realized Skill carries a fingerprint of its source; a changed fingerprint proves staleness and an unchanged one never proves conformance (Agent Skill Principle 3, `agent-native` Contract). The Agent Sync adapter may own a bounded helper that hashes, stamps, and writes the synchronization record but never judges conformance.
- Agent Sync records every run in one project-scoped synchronization record (`agent-native` Contract, Outputs and Authority).
- The Agent Sync adapter carries each rule once; duplication inside the adapter is removed on the next `self` run.
- Rejected: a runtime-identity check in Agent Sync's Stopping Conditions, and declaring Codex as a second Runtime option now — both left for later.
- Personality is a Component of this Module (not of Foundation, not inside Runtime); it absorbs Action (what a personality does) and Route (which models it prefers, in order).
- Agent Sync, discussed in its own right (see `skill/guide.md`): Module Understanding starts from this guide; a declaration the Native cannot realize exactly is realized through the nearest equivalent, reported as `approximated`, and the run continues; unmanaged native capabilities are only reported; the restart notice is boxed; the two modes and the verify-until-converged loop stay.
- The Agent Module was restructured from seventeen to ten Components (see Components): a Component is a general capability; native mechanisms are Profile hints under `settings.native.<agent-native>` or left to the Native.
- The `agent-sync` Skill became `agent-native` with three numeric modes — `1` sync self, `2` sync component, `3` install — and the separate `skill-installer` Skill was merged into mode `3`. The Operation is named Agent Native; the activity of modes 1–2 is still called Agent Sync.
- Personality refers to models by the names declared in Runtime; an Agent Instance may name an optional `personality`.
- The former Hook `read-grant` follows Permission on who may read the Module: it names the single Agent Native Skill. Applied on 2026-09-17 within the Permission Component.

<br>

## Open decisions

Recorded on 2026-09-17 from the same review. Each is a Human decision that has not yet been taken; nothing here changes the Module until the Human decides.

- Personality, carried over from its first draft under Foundation: the full content and common structure of a definition file; whether every Personality pairs with one Action and whether the Interface-owned Skills (Planning, Developing, Reviewing, …) are the executors of Actions or something separate; the exact shape of a `models` entry (model identity, provider, fallback rule, conditions); whether routing is by Personality alone or by Personality and Action; and how Personality Model Preference relates to `runtime/profile.yaml` (`models`, `fallback_models`, `effort_levels`), which is currently empty. Who reads personalities is settled by placement: only Agent Sync, which realizes them in the Native.
- Whether `profile.yaml` keeps its name or becomes `preferences.yaml` to match the Implementation Module.
- Whether the third success condition — observed behavior — should become an explicit obligation in Agent Observability Principles or in the `agent-native` Verification, with a stated form of evidence.
- Whether an explanatory Agent Rule about git commit and push should exist alongside the enforcing Permission `ask` rules.
- Output Style is selected in two places: `interaction/profile.yaml` selects `ADHD` as required, and `extension/profile.yaml` enables the `adhd-output-style` plugin that imposes its own style. One owner must be chosen.
- `context/profile.yaml` `target_precedence` does not state that the Technical Definition takes precedence on conflict, as `interface.md` does.
- `runtime/profile.yaml` `compatibility.required_profile_version: "1.0"` has no stated meaning while Profiles carry versions from 1.0 to 1.4.
