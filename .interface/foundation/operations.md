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
└── Agent Native Sync
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
### Agent Native Sync

**Agent Skill:** `/my-interface-agent-native`

This Skill is performed only through explicit Human invocation. It is the sole operation permitted to inspect Agent Module sources. It reads the complete Module and the selected Agent Native's own conventions, translates the Module into Native realizations, and verifies every required declaration.

Agent Native Sync works only between the Agent Module and the Agent Native. It needs no Target Understanding and does not decide what the product should do. It only shapes the selected Agent Native to match the Human's declared view of the Agent.
