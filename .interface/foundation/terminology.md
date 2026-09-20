# Terminology

This file carries the Terminology section of the Interface, moved here verbatim from `interface.md` on 2026-09-18. It is part of Interface Understanding: every Skill reads `interface.md` and this file before acting. The Interface file remains the canonical entry point; this file is one of its sections.

<br>

- **Interface** — the complete system described by this document; it contains the Target, Implementation, and Agent Modules together with Understanding, Operations, Foundation Files, Modes, Authority, and Workflow.
- **Human** — the person who defines the Target and owns every authored Interface source.
- **Module** — a primary conceptual boundary with a distinct responsibility inside the Interface. Target, Implementation, and Agent are the Interface Modules.
- **Target** — the application, platform, service, API, module, package, subsystem, or other development subject the Interface works on. The term is preferred over Target Project because the subject does not have to be an entire project.
- **Implementation** — the implementation's reusable programming philosophy and engineering perspective, independent of a particular Target or Agent.
- **Agent** — an AI coding system or execution unit that interacts with the Interface and maps its concepts to native capabilities.
- **Component** — one named part of the Implementation or Agent Module perspective that owns a responsibility and is described through Principles together with Implementation Preferences or Agent Preferences; some Implementation Components also own operational records.
- **Implementation Module** — the Module that defines the reusable programming philosophy, Principles, Preferences, and Component composition applied to a Target.
- **Implementation Component** — one independent Component inside the Implementation Module with a defined responsibility, Public Interface, Principles, and Implementation Preferences.
- **Logic Component** — the reusable library Component that implements application Behaviour and publishes a Public Logic Interface.
- **API Component** — the executable Component that starts the API process, owns transport concerns, and invokes Logic through its Public Interface.
- **Presentation Component** — the executable Component that presents the application to users and consumes the API Component.
- **Public Logic Interface** — the provider-owned public library surface through which API invokes application Behaviour.
- **API Contract** — the public description of API operations, transport schemas, versions, and approved outcomes.
- **Technical Purpose** — a language-level use such as modeling, API delivery, database access, ORM, or migration that may be shared by compatible Components.
- **Principles** — mandatory portable philosophy, responsibilities, rules, and boundaries owned by an Implementation or Agent Component.
- **Implementation Preferences** — preferred engineering choices, defaults, packages, implementation conventions, and optional Agent Skill associations used when the Target leaves a choice unspecified.
- **Schema** — the structure a file follows: either a standard for a Human-authored file or an operational format and initial template for a generated record.
- **Config** — mutable operational records that coordinate the Workflow and record where work stands; Config does not store what the Target means.
- **Plan** — the high-level organization of work, containing Groups, dependencies, and individual Tasks.
- **Task** — one bounded, understandable, and verifiable unit of work within a Plan.
- **Understanding** — the current context an Agent Native or Agent Instance establishes from authoritative sources before performing a Skill's role; it is either about Agent Interface itself or about the active Target.
- **Operation** — one defined action performed through an Agent Skill to configure, plan, develop, review, launch, implement, or reset work.
- **Workflow** — the ordered path from the Human's Target definition to running software: Define Target, Configure, Plan, Develop, Review, and Launch.
- **Workflow Path** — the Human's selected level of direct orchestration over that same Workflow: Default, Normal, or Detailed; it is an invocation style, not a State Mode.
- **Mode** — an operational position in the Workflow, recorded by State.
- **Skill** — an Agent capability that performs a Workflow action or provides a supporting utility; it is part of the Agent Module's integration surface, while its implementation remains outside `.interface/`.
- **Agent Module** — the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate. Bare `Agent` is never used as a substitute for this term.
- **Agent Native** — the core operational Agent supplied by the selected Agent Runtime and currently responsible for receiving the Human's request, applying synchronized Agent Module behavior, and hosting or coordinating Agent Instances.
- **Agent Instance** — one primary or specialized executable identity operating within an Agent Native, with an assigned Agent Role and bounded capabilities. One Agent Native may expose several Agent Instances.
- **Agent Preferences** — the complete portable declaration of Agent Components and their current selections, resources, empty categories, portable realization requirements, and validation expectations; Native-specific paths and formats are resolved by Agent Sync.
- **Agent Role** — one bounded execution responsibility within the Agent Preferences, including the primary role and specialized delegated roles.
- **Capability** — one declared Agent facility, such as a Skill, Rule, Command, Tool, Hook, Integration, or Extension, with an owning Component and bounded contract.
- **Agent Native Sync** — the Foundation instruction and Agent Skill `/my-interface-agent-native-sync <1=sync self | 2=sync component | 3=install>`: modes `1` (sync self) and `2` (sync component) perform Agent Sync; mode `3` performs install. It reads the Agent Module and realizes it in the selected Agent Native.
- **Capability Realization Kind** — how a declared Agent capability becomes usable in the active Runtime: **Constructed**, realized by Agent Native Sync from the Agent Module and owning Process Component; or **Installed**, provisioned by Agent Native Sync through an external provider such as a marketplace, package registry, or MCP server.
