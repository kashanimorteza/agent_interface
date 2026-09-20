# Agent Interface

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terminology](#terminology)**
3. **[Architecture](#architecture)**
4. **[Modules](#modules)**
   - **[Target](#target)**
   - **[Implementation](#implementation)**
   - **[Agent](#agent)**
5. **[Foundation Files](#foundation-files)**
6. **[Understanding](#understanding)**
7. **[Operations](#operations)**
8. **[Modes](#modes)**
9. **[Authority and Ownership](#authority-and-ownership)**
10. **[Workflow](#workflow)**


<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

The Introduction states what Agent Interface is: an implementation-oriented interface for AI-assisted software development that separates Target, Implementation, and Agent so any one can be replaced without redesigning the others, its purpose, how it works, its independence, its core idea, and its design goals.

```yaml
name: Introduction
path: .interface/foundation/introduction.md
responsibility: Overview, purpose, how it works, independence, core idea, and design goals of Agent Interface; part of every Skill's required Interface Understanding
```

→ [Introduction](foundation/introduction.md)



<br><br>

<!--------------------------------------------------------------------------------- Terminology --->
## Terminology

Terminology defines the shared vocabulary used throughout the Interface — Interface, Human, Module, Target, Implementation, Agent, Component, Principles, Preferences, Schema, Config, Plan, Task, Understanding, Operation, Workflow, Mode, Skill, the Agent Module and its Native, Instances, Preferences, Roles, and capabilities, the Agent Native Skill, and Capability Realization Kinds.

```yaml
name: Terminology
path: .interface/foundation/terminology.md
responsibility: Defines every capitalized term the Interface uses; read before any other section; part of every Skill's required Interface Understanding
```

→ [Terminology](foundation/terminology.md)



<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

Architecture shows the high-level shape of Agent Interface as one tree — the three Modules (Target, Implementation, Agent), Foundation Files, Understanding, Operations, Modes, Authority and Ownership, and Workflow — and states what each part contributes.

```yaml
name: Architecture
path: .interface/foundation/architecture.md
responsibility: The conceptual architecture tree of Agent Interface and one sentence on what each part contributes; part of every Skill's required Interface Understanding
```

→ [Architecture](foundation/architecture.md)



<br><br>

<!--------------------------------------------------------------------------------- Modules --->
## Modules

Target, Implementation, and Agent are the three primary Modules of Agent Interface. Each Module owns a distinct responsibility and documents one combined conceptual and repository Structure.

<!-------------------------- Target -->
### Target

The Target describes **what the Interface is working on**, through a Human Definition and a Technical Definition that takes precedence on conflict.

```yaml
name: Target Module Guide
path: .interface/target/guide.md
responsibility: Explains the Target Module and maps its files; the Understanding sources remain the two definition files it points to
```

→ [Target Module Guide](target/guide.md)

<!-------------------------- Implementation -->
### Implementation

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target through its ten Components.

```yaml
name: Implementation Module Definition
path: .interface/implementation/definition.md
responsibility: Defines the Implementation Module and maps every Component's Definition and Preferences; each Component's Definition remains the authority
```

→ [Implementation Module Definition](implementation/definition.md)
→ [Implementation Guide](implementation/guide.md)

<!-------------------------- Agent -->
### Agent

The Agent Module is the Human-owned, Runtime-independent declaration of how an Agent Native and its Agent Instances must operate, realized in the selected Runtime only through explicit Agent Sync; only the Agent Native Skill enters it, and every other role uses the synchronized Runtime realization.

```yaml
name: Agent Module Guide
path: .interface/agent/guide.md
responsibility: Explains the Agent Module and maps every Component's Definition and Preferences files; read only within an explicit Agent Native Skill invocation
```

→ [Agent Module Guide](agent/guide.md)



<br><br>

<!--------------------------------------------------------------------------------- Foundation Files --->
## Foundation Files

Foundation Files are the shared resources every Module and Skill depends on: the section files of this Interface, the Config records that coordinate the Workflow, and the Schemas that shape authored and generated files. They are not a Module.

```yaml
name: Foundation Guide
path: .interface/foundation/guide.md
responsibility: Explains the Foundation directory and maps the Interface section files, every Config record, and every Schema; Config records remain owned by Plan, State, and Review
```

→ [Foundation Guide](foundation/guide.md)



<br><br>

<!--------------------------------------------------------------------------------- Understanding --->
## Understanding

Understanding is the current context an Agent Native or Agent Instance establishes from authoritative sources before performing a Skill's role: Interface Understanding starts from this file and its linked Foundation files, Target Understanding from the two Target definitions, and only Agent Sync may enter the Agent Module.

```yaml
name: Understanding
path: .interface/foundation/understanding.md
responsibility: Defines Interface Understanding and Target Understanding, their sources, precedence, and the Agent Module exception; part of every Skill's required Interface Understanding
```

→ [Understanding](foundation/understanding.md)



<br><br>

<!--------------------------------------------------------------------------------- Operations --->
## Operations

Operations are the defined actions performed through the eight Interface-owned Skills — Configure, Planning, Developing, Reviewing, Launch, Implement, Reset, and Agent Native (three modes: sync self, sync component, install) — each with exactly one Skill and one summarized outcome.

```yaml
name: Operations
path: .interface/foundation/operations.md
responsibility: Defines every Operation, its Skill entry point, and the outcome that Skill is responsible for; part of every Skill's required Interface Understanding
```

→ [Operations](foundation/operations.md)



<br><br>

<!--------------------------------------------------------------------------------- Modes --->
## Modes

Modes are the operational positions recorded by State — Not Set, Configuring, Planning, Development — each with its responsibility, inputs, and output.

```yaml
name: Modes
path: .interface/foundation/modes.md
responsibility: Defines every Mode State may record, with its responsibility, inputs, and output; part of every Skill's required Interface Understanding
```

→ [Modes](foundation/modes.md)



<br><br>

<!--------------------------------------------------------------------------------- Authority and Ownership --->
## Authority and Ownership

Authority and Ownership state who owns each record (Human, Plan, State, Review) and which Skill may change it; the complete `.interface/` tree is read-only except for authorized Config records.

```yaml
name: Authority and Ownership
path: .interface/foundation/authority.md
responsibility: Defines record ownership and every Skill's write authority, including the read-only rule for the Interface tree; part of every Skill's required Interface Understanding
```

→ [Authority and Ownership](foundation/authority.md)



<br><br>

<!--------------------------------------------------------------------------------- Workflow --->
## Workflow

Workflow is the ordered path from Target definition to running software — Define Target, Configure, Plan, Develop, Review, Launch — followed through the Default, Normal, or Detailed path.

```yaml
name: Workflow
path: .interface/foundation/workflow.md
responsibility: Defines the Workflow and the Default, Normal, and Detailed invocation paths; part of every Skill's required Interface Understanding
```

→ [Workflow](foundation/workflow.md)



<br><br>
