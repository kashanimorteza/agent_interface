# Operations

This file carries the Operations section of the Interface, moved here verbatim from `interface.md` on 2026-09-17. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

Operations are the defined actions performed through Interface-owned Skills. Every Interface-owned Skill has exactly one corresponding Operation; the Operation names its Skill and summarizes the outcome that Skill is responsible for. An Operation remains separate from the Mode recorded while work is in progress, and external provider Skills do not create Interface Operations.

```text
Operations
├── Configure
├── Planning
├── Developing
├── Reviewing
├── Launch
├── Implement
├── Reset
└── Agent Native
    ├── 1 — sync self
    ├── 2 — sync component
    └── 3 — install
```

<!-------------------------- Configure Operation -->
### Configure

**Agent Skill:** `/my-interface-configure`

This Operation is performed through `/my-interface-configure` to initialize and reconcile the four operational Config files and synchronize phase State. It installs nothing and prepares no Environment: Developing installs the technical requirements of the phase it implements, and Launch prepares the Environment of the selected Launch Item.

A Skill named by an `agent_skills` association reaches the Runtime through its ecosystem's own provisioning mechanism when the environment is prepared, and through Developing when Developing installs the packages that bundle it. Planning, Developing, and every other operation use such a Skill when it is discoverable and usable, and never install it. The separation exists because a package-provided Skill cannot exist before its package does, and because provisioning one never makes it an Agent Module declaration.

<!-------------------------- Planning Operation -->
### Planning

**Agent Skill:** `/my-interface-plan`

This Operation is performed through `/my-interface-plan` to convert the current Target and applicable Implementation guidance into bounded, understandable, and verifiable Tasks.

<!-------------------------- Developing Operation -->
### Developing

**Agent Skill:** `/my-interface-develop`

This Operation is performed through `/my-interface-develop [phase-number ...]` to implement and verify eligible Tasks from a valid current Plan. Review evaluates the resulting implementation afterward.

<!-------------------------- Reviewing Operation -->
### Reviewing

**Agent Skill:** `/my-interface-review`

This Operation is performed through `/my-interface-review [phase-number ...]` to assure each selected phase's Plan and existing implementation against current Interface and Target Understanding, recording every misalignment as a Finding owned by Configure, Plan, or Develop, without invoking them or repairing anything; Implement (or the Human) reruns those operations and Review until it is satisfied. With no phase input, it reviews every enabled phase.

<!-------------------------- Launch Operation -->
### Launch

**Agent Skill:** `/my-interface-launch`

This Operation is performed through `/my-interface-launch [api|logic|presentation|complete|all]` to read the selected Launch definition and its Component Runtime Requirements, start only the requested scope (or all developed parts for `complete`/`all`), verify readiness, and report access points. When no scope is supplied, the Launch Skill asks the Human to choose one.

<!-------------------------- Implement Operation -->
### Implement

**Agent Skill:** `/my-interface-implement`

This Operation is performed through `/my-interface-implement [phase-number ...]` to execute Configure once when no phase was selected, then, for each selected phase in Target order, Review first when the phase already has an implementation (so a changed Target surfaces as Findings, and an unchanged phase is confirmed without rework) or Planning first when it has none, then the Planning, Developing, and Review cycle repeated while Review records Findings and progress continues — advancing only after the phase is satisfied, and finally perform eligible Launch. With no phase input, it processes every enabled and ready phase.

<!-------------------------- Reset Operation -->
### Reset

**Agent Skill:** `/my-interface-reset`

This Operation is performed through `/my-interface-reset [phase-number ...]` to reset selected phases; with no phase input it resets every phase with generated work. `/my-interface-reset config` physically removes only operational Config files, while `/my-interface-reset complete` physically removes those Config files and the implementation outputs of all phases. Emptying or reinitializing a Config file is not removal. Every mode previews its exact impact and requires separate Human confirmation before mutation.

<!-------------------------- Agent Native Operation -->
### Agent Native

**Agent Skill:** `/my-interface-agent-native <1=sync self | 2=sync component | 3=install>`

One Skill, three modes. Modes `1` and `2` are **Agent Sync**; mode `3` is **install**, the former Skill Installer operation merged into this Skill on 2026-09-17. The Skill is named for what it does — the Agent Native configuring itself from the Agent Module — while *Agent Native* in Interface prose keeps its meaning of the core operational Agent supplied by the Runtime.

**Modes `1` and `2` — Agent Sync.** This Operation is performed only through explicit Human invocation of `/my-interface-agent-native` in one of two sync modes: mode `1` (sync self) realizes the Agent Sync adapter itself from its current Contract, and mode `2` (sync component) realizes every other declaration. It is the sole operation permitted to inspect Agent Module sources, understands the complete Module and the selected Agent Native's own conventions, translates the Module into that Native Runtime, and certifies synchronization only after all required declarations pass post-change verification and no non-Sync Runtime instruction routes back into the Agent Module.

Agent Sync works only between the Agent Module and the Agent Native, so it needs no Target Understanding and no other Interface Module: it never decides what the product should do, only how the selected Agent Native must be shaped to match the Human's declared view of the Agent. It realizes its own adapter before the rest of the Module because a running adapter cannot load a definition it did not start with.

**Mode `3` — install.** Mode `3` is performed through `/my-interface-agent-native 3` to derive Agent capability needs, discover compatible project-scoped candidates, obtain Human approval, provision only approved capabilities, and verify their activation.
