# Agent Module

This document explains the Agent Module: what it is, why it exists, how its parts relate, how it changes, and how its success is judged. It is Human-owned and records the Human's stated understanding so that this understanding is not lost between sessions or Agent Runtimes. The canonical Interface definition remains `.interface/interface.md`; this document explains, it does not redefine. Where the two disagree, the Interface file and each Component's Principles are correct.

<br>

## Purpose

Agent Interface is the interface between a developer and an AI Agent. The Agent Module is the layer inside it that holds everything about the Agent itself: its behaviors, skills, rules, restrictions, responsibilities, and view of the world. It is written once, independently of which Agent Native will run it — Claude Code, Codex, Copilot, or any other engine.

The Module does not know the Agent Native. A separate Skill, Agent Sync, establishes an Understanding of the complete Module and configures the Agent Native's own structure from that Understanding — Agent Sync is, in effect, the Native configuring itself, since it runs inside the Native. Because Agent Sync itself runs inside the Agent Native, the Native already knows where a rule belongs, where a skill belongs, and what documentation a skill must be built with. The Module owns *what* the Agent is; the Agent Native, through Agent Sync, owns *where and how* that is realized.


The Agent Module is the Human-owned, Runtime-independent home for the complete reusable view of how an Agent Native and its Agent Instances should operate. The Human declares that view once through its Components—including the Agent Native, Agent Instance identities, Roles, Rules, Skills, settings, capabilities, boundaries, and every other supported mechanism—rather than explaining the same expectations separately to Claude Code, Codex, or each later Agent Runtime. Each Agent Component owns one responsibility and has Principles for its mandatory portable contract and a Preferences file for its current choices, resources, portable realization requirements, and explicit empty categories.

The Agent Module expresses our general understanding, philosophy, rules, responsibilities, boundaries, and desired behavior for an Agent. It is an independent declaration and is not written for Claude Code, Codex, or any other specific Agent Native. It does not define the Target and does not prescribe a vendor's files, directories, command names, configuration format, or implementation mechanism. An Agent Native reads this portable Module through explicit Agent Sync, understands its own runtime documentation and capabilities, and translates the Module into the native structures it supports. The meaning and authority come from the Agent Module; the concrete runtime form comes from the Agent Native.

Every capability the Module declares has exactly one Capability Realization Kind, and that Kind decides what Agent Sync does with it. A Constructed capability is built by the Agent Native from a portable specification such as a Skill Contract. A Prepared capability is transferred into the Runtime unchanged from a complete Human-authored artifact. An Installed capability is provisioned by the Agent Native through its own native mechanism from an external source such as a marketplace, package registry, or MCP server, and is never built or transferred. This distinction applies to every Component, not only to Skills, so a newly declared capability of any kind has a defined place and a defined realization path. Because external sources differ by Agent Native, a declaration may carry optional per-Agent-Native identity for an Installed capability so the selected Native can locate and provision it. That identity helps the Native find an external artifact; it never prescribes the Native's own structure, format, or mechanism, and Agent Sync treats it as an aid rather than an authority.

Together, these Components form the Agent Preferences within the complete Agent Module. Explicit Agent Sync is the only bridge from that reusable declaration to the currently selected compatible Runtime: it understands the complete Agent Module, learns the Native Runtime's own conventions, realizes the Module through that Runtime's Agent Native, Agent Instances, Rules, Skills, settings, and other capabilities, and verifies the result. The active Agent Native and its Agent Instances then operate from the synchronized Runtime realization without requiring the Human to restate the Agent philosophy.
<br>

## What belongs here

Every view, rule, limit, and responsibility that concerns the Agent, and would remain true if the Target or the Implementation were replaced. A rule such as "never commit or push until the Human explicitly asks" is an Agent rule: it is a rule between the Human and the Agent, not a property of any project. The Module records it, and the Agent Native enforces it through whichever native mechanism it has (a permission rule, a hook, a persistent instruction).

What does not belong here: the meaning of the Target, the engineering philosophy of the Implementation, the shape of generated Config, and any vendor's file layout, command names, or configuration format.

<br>

## Principles and Preferences

Each Agent Component has two files.

- `principles.md` states the Human's view and philosophy of that Component. It contains no technology, package, provider, or Agent Native. It is portable: the same file can be handed to another project or another Agent unchanged.
- `preferences.yaml` holds the parameters that support that view: current selections, declared resources, explicit empty categories, and — when a view needs a helper for one Agent Native — a block declared for that Native only (for example `native.claude`). Preferences are in effect a preferences file; it never weakens a Principle.

When the Agent Native changes, Principles stay as they are. Only the Native-specific helper blocks in Preferences may change.

<br>

## Components

The Module has ten Components: Runtime, Agent, Personality, Rule, Skill, Command, Tool, Permission, Connection, and Context. On 2026-09-17 the Human reduced the earlier seventeen to these ten so that every Component is a general capability any Agent must honor, rather than a mechanism of one particular Agent Native. Role and Coordination merged into Agent; Interaction, Observability, and Session merged into Rule; Integration and Extension merged into Connection; Hook merged into Permission; Settings dissolved into the Agent Preferences Schema (its general rules) and Runtime (its Claude-specific mechanics). Nothing was dropped: every absorbed Principle keeps its former number in a note, and every absorbed Preferences lives under a named key of its new Preferences. The Agent Native chooses how to realize each concept with its own mechanisms; where the Human knows a particular Native well, the Preferences may suggest a realization under `settings.native.<agent-native>` — a hint that narrows discovery, never an authority. This set is the Human's default structure — the set that was sufficient to hold every view the Human had about an Agent. It is not a requirement that every Agent Native supports every Component. Agent Sync takes the Understanding of each Component and places it into whatever the selected Agent Native actually offers; a Component the Native cannot realize exactly is realized through the nearest equivalent and reported as approximated, and an explicitly empty category stays empty.

```text
Agent Components
├── Runtime
│   ├── Principles  → .interface/agent/runtime/principles.md
│   └── Preferences     → .interface/agent/runtime/preferences.yaml
├── Agent
│   ├── Principles  → .interface/agent/agent/principles.md
│   └── Preferences     → .interface/agent/agent/preferences.yaml
├── Personality
│   ├── Principles  → .interface/agent/personality/principles.md
│   ├── Preferences     → .interface/agent/personality/preferences.yaml
│   └── Definitions → .interface/agent/personality/definitions/<personality>.md
├── Rule
│   ├── Principles  → .interface/agent/rule/principles.md
│   └── Preferences     → .interface/agent/rule/preferences.yaml
├── Skill
│   ├── Principles  → .interface/agent/skill/principles.md
│   ├── Preferences     → .interface/agent/skill/preferences.yaml
│   ├── Contracts   → .interface/agent/skill/contracts/<interface-owned-skill>.md
│   └── Files       → .interface/agent/skill/files/<declared-skill-stable-key>[.md | /]
├── Command
│   ├── Principles  → .interface/agent/command/principles.md
│   └── Preferences     → .interface/agent/command/preferences.yaml
├── Tool
│   ├── Principles  → .interface/agent/tool/principles.md
│   └── Preferences     → .interface/agent/tool/preferences.yaml
├── Permission
│   ├── Principles  → .interface/agent/permission/principles.md
│   └── Preferences     → .interface/agent/permission/preferences.yaml
├── Connection
│   ├── Principles  → .interface/agent/connection/principles.md
│   └── Preferences     → .interface/agent/connection/preferences.yaml
└── Context
    ├── Principles  → .interface/agent/context/principles.md
    └── Preferences     → .interface/agent/context/preferences.yaml
```

The complete Agent Module is read exclusively during an explicit Agent Native Skill invocation. Agent Sync first learns the selected Agent Native's own documentation, conventions, capabilities, and limitations, then reads every Module source and Interface-owned Skill Contract, and realizes each required Rule, Constructed Skill, Agent Instance, Command, Setting, Hook, permission, integration, and other capability as a self-contained Runtime artifact. the install mode of the Agent Native Skill resolves any optional prepared Skill file by exact declared stable key: a matching prepared Markdown file supplies that Skill's preserved native instruction content and is materialized as a Prepared Skill, and a Skill under an external provider declaration is provisioned as an Installed Skill; a Skill with neither follows its Contract-based realization path through Agent Sync. Every other Skill, supporting Agent Instance, coordinator, startup routine, and Understanding workflow is forbidden from entering, resolving, or using Agent Module sources and consumes only the last synchronized Runtime realization. A changed Agent Module declaration remains dormant until the Human explicitly invokes Agent Sync.

Each Agent Component below has its own Principles and Preferences. Principles define the Component's mandatory philosophy, responsibilities, rules, and boundaries; Preferences define its current selections, resources, portable realization requirements, default settings, and optional per-Native realization hints.

### Runtime

Runtime identity, provider, model, compatibility, and native capability mapping. Absorbs the former Settings Component (2026-09-17): Settings — Configuration sources, scopes, precedence, merge behavior, environment, and reconciliation.

- [Principles](runtime/principles.md)
- [Preferences](runtime/preferences.yaml)

### Agent

The selected Agent Native and its General and Specialized Agent Instances. Absorbs the former Role, Coordination Components (2026-09-17): Role — Primary and specialized Agent Role contracts. Coordination — Delegation, teams, tasks, messaging, concurrency, and worktree isolation.

- [Principles](agent/principles.md)
- [Preferences](agent/preferences.yaml)

### Personality

The personalities an Agent can take on: who it is during a kind of work, the Actions each performs, and the models each prefers in priority order.

- [Principles](personality/principles.md)
- [Preferences](personality/preferences.yaml)
- [Definitions directory](personality/definitions/)

### Rule

Persistent global and scoped behavioral instructions. Absorbs the former Interaction, Observability, Session Components (2026-09-17): Interaction — Output Styles, progress, prompts, status presentation, artifacts, themes, and UI behavior. Observability — Validation, status, diagnostics, evidence, logs, telemetry, health, and usage. Session — Lifecycle, resume, history, background work, isolation, checkpoints, and termination.

- [Principles](rule/principles.md)
- [Preferences](rule/preferences.yaml)

### Skill

Reusable knowledge and workflows, including core, supporting, and contextual Skills.

- [Principles](skill/principles.md)
- [Preferences](skill/preferences.yaml)
- [Contracts directory](skill/contracts/)
- [Files directory](skill/files/)

The Skill directory in detail (moved here verbatim from the former `skill/guide.md` on 2026-09-17):

```text
skill/
├── guide.md
├── principles.md        ← the shared philosophy every Skill follows
├── preferences.yaml         ← the declared Skills, their invocation policy, and provider declarations
├── contracts/           ← one portable Contract per Interface-owned Skill
│   ├── configure.md
│   ├── planning.md
│   ├── developing.md
│   ├── reviewing.md
│   ├── launch.md
│   ├── implement.md
│   ├── reset.md
│   └── agent-native.md     ← modes 1 sync self · 2 sync component · 3 install (former skill-installer)
└── files/               ← optional prepared Skill files, keyed by stable Skill key (declared; currently absent)
```

A Skill has exactly one Capability Realization Kind. An Interface-owned Skill is **Constructed**: its Contract defines it completely and Agent Sync builds the native Skill from it. A Skill with a matching prepared file is **Prepared** and a Skill from an external provider is **Installed**; both belong to the install mode of the Agent Native Skill.

Three layers, each with one owner:

- **Principles** (`principles.md`) — rules shared by every Skill: one complete Contract each, proven availability, safe repeatability, fingerprints that prove staleness but never conformance, prepared files.
- **Contract** (`contracts/<skill>.md`) — the Skill's own portable behavior in the thirteen sections of the Skill Contract Schema: purpose, responsibility, trigger, inputs, outputs, required understanding, authority, workflow invariants, verification, idempotency, stopping conditions, runtime realization. Every obligation appears once; nothing vendor-specific.
- **Native adapter** (outside `.interface/`, for example `.claude/skills/<name>/SKILL.md`) — the synchronized, self-contained realization of the Contract in the selected Agent Native. It owns only runtime execution detail and never becomes a second authority.

When a conversation produces a new understanding of a Skill, the *why* is recorded in this guide and the *obligation* it implies is written into that Skill's Contract. The adapter is then brought into line by Agent Sync, never by hand — except for the Agent Sync adapter itself, once, at bootstrap.

### Command

Named and slash invocation entry points, arguments, aliases, and routing.

- [Principles](command/principles.md)
- [Preferences](command/preferences.yaml)

### Tool

Atomic built-in and externally provided executable capabilities.

- [Principles](tool/principles.md)
- [Preferences](tool/preferences.yaml)

### Permission

Authorization, allow/ask/deny, sandboxing, trust, authentication, and secrets. Absorbs the former Hook Component (2026-09-17): Hook — Deterministic event-driven lifecycle automation.

- [Principles](permission/principles.md)
- [Preferences](permission/preferences.yaml)

### Connection

External services and installable packages the Agent obtains from outside the project, with their trust boundaries and lifecycle. Absorbs the former Integration, Extension Components (2026-09-17): Integration — MCP, LSP, channels, application connectors, and external services. Extension — Plugins, marketplaces, capability packages, monitors, and extension lifecycle.

- [Principles](connection/principles.md)
- [Preferences](connection/preferences.yaml)

### Context

Persistent instructions, Understanding, Memory, imports, loading, and compaction.

- [Principles](context/principles.md)
- [Preferences](context/preferences.yaml)

Every Agent Component's Principles and Preferences are authoritative for that Component only. A runtime artifact not declared in the owning Preferences are an optional runtime capability; a required declaration not usable by the selected runtime is Agent Preferences gap.

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

**What is the difference between Principles and Preferences?**
Principles express the view and philosophy of a Component and say nothing about technology, packages, or the kind of Agent. Preferences hold supporting parameters, including helpers for a specific Agent Native such as Claude, Copilot, or Codex; they are in effect preferences. The Human noted that the Implementation Module calls the equivalent file `preferences.yaml` and that the name `preferences.yaml` is historical.

**Are the sixteen Components required for every Agent?** *(sixteen at the time of the answer; Personality became the seventeenth later the same day, and the set was then reduced to ten — see Components)*
No. They are the structure that was sufficient to hold every view the Human had. Agent Sync places the Understanding into whatever the selected Agent Native offers; the sixteen are a default, not an obligation on every Native.

**What does "Agent Sync succeeded" mean?**
That Agent Sync, from a precise Understanding of the Module, transferred everything into the Native's configuration and mechanisms as well as that Native allows — the Skills exist there, the concept and view reached it — and that in the end the Agent works the way the Human wants and has understood how it must be configured.

<br>

## Understanding record — Agent Native Skill

The following questions were put to the Human and answered on 2026-09-17.

**What is Agent Sync?**
Agent Sync is the Agent Native configuring itself. It runs inside the selected Native — Claude Code, Codex, Copilot — establishes an Understanding of the complete Agent Module, starting from the Agent Module Guide, and then, following the Native's own principles and standards, shapes the Native to match: the concepts, skills, rules, and limits declared in the Module are carried into the Native's own configuration. The Human does not know, and does not need to know, where a given Native keeps a rule or a skill; what matters is that Sync recognizes "here is a Skill that must exist", "here are rules", and the Native, being the one that runs Sync, knows where those go.

**Does Sync install anything?**
No. Sync gains an Understanding of the declared Skills and does whatever that Understanding requires, which for an Interface-owned Skill is to create it from its Contract. Nothing is installed by Sync; Prepared and Installed Skills remain with the install mode of the Agent Native Skill.

**Why two modes, `self` and `module`?**
Because a Skill that is already running cannot load a new definition of itself. So Sync first realizes its own adapter from its Contract (`self`), the Human restarts the Native, and only then does Sync realize the rest of the Module (`module`). The Human considered collapsing the two modes and updating the adapter by hand every time, and decided against it: the two modes stay, and the adapter is written by hand only once, at bootstrap.

**What happens when the Native cannot realize a declaration exactly?**
Sync reports it, realizes the nearest native equivalent, and continues. Sync does not stop. The report must state exactly how the realization differs from the declaration. Only when no equivalent exists at all, or a genuine stopping condition applies, is the item blocked.

**What about things present in the Native but declared nowhere in the Module?**
Report them, and touch nothing. "These exist in the Native and not here" is all that is needed.

**How should the restart requirement be communicated?**
As a warning that cannot be missed — visually set apart, in a box — placed prominently in the report whenever any native artifact was written.

**How thorough should verification be?**
Sync follows a loop: do the work, check it, and if the check finds a gap, do it again and check again. Whether that takes one pass, two, or three is Sync's own judgment; what is required is the process that ends only when Sync is satisfied that every concept in the Module has reached the Native.

<br>

## Decisions taken — Agent Native Skill

Recorded on 2026-09-17 and written into `contracts/agent-native.md` the same day:

- Later the same day the Skill was renamed `agent-native` with three numeric modes — `1` sync self, `2` sync component, `3` install — and the separate `skill-installer` Skill was merged into mode `3`; both Contracts were merged into `contracts/agent-native.md` with nothing dropped.

- Module Understanding starts from the Agent Module Guide (`.interface/agent/guide.md`), where the Agent Structure now lives.
- A new result status `approximated`: realized through the nearest native mechanism, with the exact difference stated; Sync continues. `blocked` is reserved for declarations with no native equivalent or a genuine stopping condition.
- The restart notice is visually set apart in the report.
- Kept unchanged, now with the Human's stated reasons: the two modes, the read-only treatment of unmanaged native capabilities, and the Understanding–Reconcile–Verify loop until convergence.

<br>

## Understanding record — Configure

Reviewed with the Human on 2026-09-17 for problems and unnecessary work. Three questions were raised and answered; the Contract was left unchanged on all three.

**Should Configure install the whole technical environment up front, before any phase is planned?**
*Revised on 2026-09-18:* No. Configure creates and reconciles the four Config files and nothing else. Every operation prepares what it needs: Developing installs the technical requirements of the phase it implements; Launch prepares the Environment of its Launch Item and raises a Blocker for what only the Human can provide. The earlier answer, kept for the record: Yes. One Configure run installs everything the Implementation and Platform Preferences declare, so no later phase is surprised and the environment has one point of truth. The cost — tools installed for phases that may change, and a Launch-host Blocker seen early — is accepted; seeing the Launch requirement early is itself useful.

**Should Configure create `application.yaml` even though every Component section is empty at that point?**
Yes. Configure creates all four Config files; an empty section is an explicit "declared, not yet published" record, consistent with the rule that empty categories are explicit. Developing fills the sections as Components come into existence.

**Does Configure read too much by reading every Implementation Principles file?**
*Revised on 2026-09-18:* moot — Configure no longer reads Implementation or Platform authorities at all; it reads Schemas, existing Config, Target phase identifiers, and published Component metadata. The earlier answer, kept for the record:
The technical selections it needs live in Preferences, so narrowing to Preferences would be possible; the Human chose to keep the current reading scope because the difference is a few file reads and the risk of missing a Preference that points back to a Principle is not worth it.

<br>

## Understanding record — Implement, Planning, Developing, Reviewing

Discussed with the Human on 2026-09-17.

**How do the four fit together?**
Planning defines the work for a phase. Developing generates the output from that Plan. Reviewing judges: it compares the generated output with the Understanding it has of the project and of that phase, using the rules its Contract already carries. If everything matches, it confirms; if not, it records what is wrong in the Review record (`review.yaml`), each Finding naming the operation that must fix it — and does nothing else. Implement watches Review's answer: not confirmed means run Planning and Developing again (they read the recorded Findings and correct their work; a changed Plan is re-implemented), then Review again, and so on until Review confirms; then Implement moves to the next phase and finally leaves the loop reporting the work done.

**Where is the loop?**
In Implement, not in Reviewing. Reviewing keeps every rule it had and loses only the right to invoke other Skills and to repeat within its own run. Implement must therefore be permitted to invoke Configure, Planning, Developing, Reviewing, and Launch through the Native's own Skill mechanism.

**What if the phase was already generated and the Target changed since — say four models were added?**
Implement enters that phase through Review first. Review compares the existing Plan and implementation with the current Understanding of the Target, so the new models appear as Findings (owned by Planning, and Developing where code no longer satisfies the Plan). Then the usual loop runs — Planning, Developing, Review — until Review is satisfied. If Review is satisfied on that first pass, nothing changed and the phase is done without any rework. A phase that was never implemented still starts with Planning, because Review has nothing to judge yet.

**When does Implement run Configure?**
Only when it was invoked without a phase number. With a phase number, Configure is skipped.

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
- Agent Sync, discussed in its own right (see "Understanding record — Agent Native Skill" above): Module Understanding starts from this guide; a declaration the Native cannot realize exactly is realized through the nearest equivalent, reported as `approximated`, and the run continues; unmanaged native capabilities are only reported; the restart notice is boxed; the two modes and the verify-until-converged loop stay.
- The Agent Module was restructured from seventeen to ten Components (see Components): a Component is a general capability; native mechanisms are Preferences hints under `settings.native.<agent-native>` or left to the Native.
- The `agent-sync` Skill became `agent-native` with three numeric modes — `1` sync self, `2` sync component, `3` install — and the separate `skill-installer` Skill was merged into mode `3`. The Operation is named Agent Native; the activity of modes 1–2 is still called Agent Sync.
- Personality refers to models by the names declared in Runtime; an Agent Instance may name an optional `personality`.
- Implement keeps a step-by-step log of every run under State's `implementation.runs` (selection, Configure run or skipped, every phase's cycles with Planning/Developing/Reviewing outcomes, stop reason, Launch decision, result). State stays the owner; no fifth Config file.
- Configure is Config-only (2026-09-18): no installation, no Environment preparation, no reading of Implementation or Platform Preferences. Developing prepares its phase's technical requirements; Launch prepares its Environment and raises a Blocker for system-level needs; Review names the right owner for each kind of drift.
- Implement enters an already-implemented phase through Review first (`entry: review-first` in the run log) and a never-implemented phase through Planning first; a satisfied first Review ends the phase without rework.
- The Planning → Developing → Reviewing loop belongs to Implement. Reviewing records Findings with their owning operation and invokes nothing; its `coordination` declaration moved to Implement, which may invoke Configure, Planning, Developing, Reviewing, and Launch. The Detailed workflow path no longer runs Review before Developing.
- Output Style is owned by the enabled plugin `adhd-output-style`; Rule Preferences select `ADHD Explanatory`, the style that plugin provides.
- Context Preferences state that the Technical Definition takes precedence over the Non-Technical Definition wherever they conflict.
- Runtime Preferences drop the undefined `required_profile_version`/`status` pair; `compatibility` is an explicit empty category.
- The Agent Module's second file is `preferences.yaml`, as in the Implementation Module; the schema is `agent-preferences.yaml`; "Preferences" replaces "Profile" throughout the Module. Implementation's own term "Component Profile" is unrelated and unchanged.
- A `git-discipline` Rule explains the boundary Permission enforces: no commit or push without an explicit request in the current message; "save" means write to disk.
- Every enforced guarantee carries a behavioral probe per Agent Native; Agent Sync runs the probes during Verification, and a failed probe means the guarantee is not realized. This is how the third success condition — observed behavior — enters the Contract.
- Personality definitions follow `schema/personality.md` (Who it is, What it does, How it judges, What it never does, Runs on). Each core Skill has a `personality` field for the Personality it works with; all are left null until the Personality definitions are complete, after which the Human assigns them (the intended pairing: configure → architect, planning → planner, developing → developer, reviewing → reviewer; launch none). Routing is by Personality alone: `models` is an ordered list of stable names declared in Runtime Preferences, first primary, rest fallbacks.
- The former Hook `read-grant` follows Permission on who may read the Module: it names the single Agent Native Skill. Applied on 2026-09-17 within the Permission Component.

<br>

## Open decisions

Recorded on 2026-09-17. Every decision listed here earlier in the day was taken the same day (see Decisions taken). What remains open:

- The content of each Personality's "How it judges" and "What it never does" sections, which are placeholders until the Human writes them.
- Assigning a Personality to each core Skill (`skill/preferences.yaml` → `personality`), once the definitions are complete.
- The concrete models to declare in Runtime Preferences (`settings.models`) and, from them, each Personality's `models` order; both are empty until the Human names them.
- Understanding records for the Target, Implementation, and Foundation guides, and for the seven other Interface-owned Skills and the install mode of Agent Native.
- The prepared-file directory `files/` is declared in `preferences.yaml` but does not exist; whether to create it empty or leave it absent until a prepared Skill exists.
