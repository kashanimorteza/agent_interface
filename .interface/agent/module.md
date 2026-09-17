# Agent Module

This document explains the Agent Module: what it is, why it exists, how its parts relate, how it changes, and how its success is judged. It is Human-owned and records the Human's stated understanding so that this understanding is not lost between sessions or Agent Runtimes. The canonical Interface definition remains `.interface/foundation/interface.md`; this document explains, it does not redefine. Where the two disagree, the Interface file and each Component's Principles are correct.

<br>

## Purpose

Agent Interface is the interface between a developer and an AI Agent. The Agent Module is the layer inside it that holds everything about the Agent itself: its behaviors, skills, rules, restrictions, responsibilities, and view of the world. It is written once, independently of which Agent Native will run it — Claude Code, Codex, Copilot, or any other engine.

The Module does not know the Agent Native. A separate Skill, Agent Sync, establishes an Understanding of the complete Module and configures the Agent Native's own structure from that Understanding. Because Agent Sync itself runs inside the Agent Native, the Native already knows where a rule belongs, where a skill belongs, and what documentation a skill must be built with. The Module owns *what* the Agent is; the Agent Native, through Agent Sync, owns *where and how* that is realized.

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

The Module currently has sixteen Components: Runtime, Settings, Context, Role, Agent, Coordination, Skill, Command, Rule, Tool, Hook, Integration, Extension, Interaction, Permission, and Observability. This set is the Human's default structure — the set that was sufficient to hold every view the Human had about an Agent. It is not a requirement that every Agent Native supports every Component. Agent Sync takes the Understanding of each Component and places it into whatever the selected Agent Native actually offers; a Component the Native cannot realize is reported, and an explicitly empty category stays empty.

<br>

## How the Module changes

Every decision about the Agent is first written into the Agent Module, in the Component that owns it. Nothing is written into the Agent Native by hand. Once the Module is updated, the Human invokes Agent Sync — `self` to let the Agent Sync adapter realize itself from its current Contract, then `module` to realize every other declaration — and the Agent Native is brought into conformance.

There is exactly one exception. The native Agent Sync adapter must exist before Agent Sync can run at all, so the first time — and only the first time — it is written by hand from its Contract. After that bootstrap, Agent Sync updates its own adapter and every other native artifact; no further manual native change is made.

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

**Are the sixteen Components required for every Agent?**
No. They are the structure that was sufficient to hold every view the Human had. Agent Sync places the Understanding into whatever the selected Agent Native offers; the sixteen are a default, not an obligation on every Native.

**What does "Agent Sync succeeded" mean?**
That Agent Sync, from a precise Understanding of the Module, transferred everything into the Native's configuration and mechanisms as well as that Native allows — the Skills exist there, the concept and view reached it — and that in the end the Agent works the way the Human wants and has understood how it must be configured.

<br>

## Open decisions

Recorded on 2026-09-17 from the same review. Each is a Human decision that has not yet been taken; nothing here changes the Module until the Human decides.

- Whether `profile.yaml` keeps its name or becomes `preferences.yaml` to match the Implementation Module.
- Whether the third success condition — observed behavior — should become an explicit obligation in Agent Observability Principles or in the `agent-sync` Verification, with a stated form of evidence.
- Whether an explanatory Agent Rule about git commit and push should exist alongside the enforcing Permission `ask` rules.
- Native names that leaked into Profiles: `hook/profile.yaml` (event names, tool-name matchers, the `lifecycle_events` list), `agent/profile.yaml` (`allowed_tools` of `interface-reader`), and `settings/profile.yaml` (`source_precedence`). Either make them portable or move them under a `native.<agent-native>` block.
- Hook and Permission disagree about Skill Installer: Permission Principle 3 grants Agent Module reads to both `agent-sync` and `skill-installer`; the `agent-sync-read-grant` Hook declaration names only `agent-sync`.
- Permission Principle 3's At a Glance line names only `agent-sync`, while the Rule names both `agent-sync` and `skill-installer`.
- Output Style is selected in two places: `interaction/profile.yaml` selects `ADHD` as required, and `extension/profile.yaml` enables the `adhd-output-style` plugin that imposes its own style. One owner must be chosen.
- `context/profile.yaml` `target_precedence` does not state that the Technical Definition takes precedence on conflict, as `interface.md` does.
- `runtime/profile.yaml` `compatibility.required_profile_version: "1.0"` has no stated meaning while Profiles carry versions from 1.0 to 1.4.
