# Agent Interface

`interface.md` is the canonical introduction and navigation entry point of the Agent Project Interface. It explains what the Interface is, how it is structured, where every current resource lives, which external Agent Skills integrate with it, and how the human-facing Workflow proceeds.

## Document contract

| Property | Value |
| --- | --- |
| Path | `.interface/interface.md` |
| Standard | Agent Project Interface |
| Version | 9.0 |
| Updated | 2026-09-07 |
| Responsibility | Human-readable definition and complete file map of Agent Project Interface |
| Edit authority | Human only |

Agent Interface operations and supporting Agents must not edit this file. If an operation determines that the Interface document should change, it reports the required change to the human and leaves this file untouched. Live Workflow position belongs to the State Component; this document only explains and locates that Component.

Read this document in the following order:

1. **Interface** — purpose and concept.
2. **Structure** — foundational files, Layers, Components, Modes, and generated configuration.
3. **Agent Skills** — external capabilities integrated with the Interface.
4. **Workflow** — the human-facing sequence for using the Interface.

## Interface

### Description

Agent Interface is an independent interface between **Developers** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its goal is to let Developers express project requirements in natural language and transform that information into a standardized representation that Agents can understand, plan against, and use to develop the project.

### Overview

Instead of requiring an Agent to reconstruct an entire project from conversation on every operation, the Developer defines the target project in human language and the Interface converts that definition into explicit and predictable project Understanding.

The core Interface Structure is independent of any specific AI model, Agent, or external execution capability. Agent Skills are cataloged as integrations, not as parts of the Structure.

### Concept

Human project definitions are naturally flexible. Agents work more reliably when the same information is organized into stable responsibilities, rules, defaults, formats, and generated outputs. Agent Interface is the communication layer between those two forms.

## Structure

The Interface lives in `.interface/`. Its Structure consists of foundational files, three descriptive Layers, Components described through those Layers, operating Modes, and generated project configuration.

Agent Skills and the human-facing Workflow use this Structure but are not part of it.

### Foundational files

| File | Responsibility |
| --- | --- |
| `.interface/interface.md` | Canonical definition, navigation entry point, and complete file map of Agent Project Interface |
| `.interface/project.md` | Human-managed natural-language definition of the target project being built |

### Layers

Each Component has one stable file in every descriptive Layer. A Layer file may contain only its standard empty shape when the Component has no Layer-specific content; consumers then continue with the other applicable sources.

| Layer | Directory | Responsibility | Answers |
| --- | --- | --- | --- |
| Principles | `.interface/principles/` | Mandatory philosophy, responsibilities, and boundaries, independent of tools and versions | Why and under what rules |
| Preferences | `.interface/preferences/` | Supported technical choices and defaults used when the target project leaves a choice unstated; an explicit project choice wins | With what |
| Schemas | `.interface/schema/` | Shapes and validation rules of generated configuration; no Component philosophy or technical preference belongs here | In what form |

Adding content to an existing Layer file does not require changing this document. This file changes only when a Component or structural path is added, removed, or renamed. There is no global Preferences file. The shared outer shape of Interface YAML files is defined at `.interface/schema/file.yaml`.

### Components and file map

This matrix is the authoritative navigation map. To understand one Component, combine its applicable Principle, Preference, Schema, and generated configuration. Empty Layer content contributes no additional rule.

| Component | Responsibility | Principle | Preference | Schema | Generated configuration |
| --- | --- | --- | --- | --- | --- |
| Definition | Structured project description, conceptual Models, project Structure, Behaviours, and ordered phases | `.interface/principles/definition.md` | `.interface/preferences/definition.yaml` | `.interface/schema/definition.yaml` | `.interface/config/definition.yaml` |
| Model | Independent shared Model package and logical domain Models, including fields, relationships, rules, validation, and initial data | `.interface/principles/model.md` | `.interface/preferences/model.yaml` | `.interface/schema/model.yaml` | `.interface/config/model.yaml` |
| Development | Independent Model, Database, Backend, and Frontend layers; centralized runtime configuration; declared-interface connections; cross-cutting capabilities; and Platform composition | `.interface/principles/development.md` | `.interface/preferences/development.yaml` | `.interface/schema/development.yaml` | `.interface/config/development.yaml` |
| State | Current Workflow position, repeatable Modes, critical Blockers, and Open Questions | `.interface/principles/state.md` | `.interface/preferences/state.yaml` | `.interface/schema/state.yaml` | `.interface/config/state.yaml` |
| Task | Phase Plans, coherent Groups, atomic Tasks, progress, and Task-local history | `.interface/principles/task.md` | `.interface/preferences/task.yaml` | `.interface/schema/task.yaml` | `.interface/config/task.yaml` |
| Backend | Application and Model Logic, Database communication through Data Access, and the external API | `.interface/principles/backend.md` | `.interface/preferences/backend.yaml` | `.interface/schema/backend.yaml` | `.interface/config/backend.yaml` |
| Frontend | Component-based Presentation, user Interaction Logic, and application access through the Backend API | `.interface/principles/frontend.md` | `.interface/preferences/frontend.yaml` | `.interface/schema/frontend.yaml` | `.interface/config/frontend.yaml` |
| Database | Independent package with typed Model operations, supported Engines, selectable Instances, Model-driven mapping, and Storage Adapters | `.interface/principles/database.md` | `.interface/preferences/database.yaml` | `.interface/schema/database.yaml` | `.interface/config/database.yaml` |

### Modes

State records the active Mode. Agent Skills are external capabilities that perform the operations represented by Modes. These Modes are distinct from target-project Behaviours, which describe what the target application must do.

#### Not Set

- **State value:** `not set`
- **Phase-specific:** no
- **Responsibility:** represents the resting State before an Interface operation has been recorded.

#### Configuring

- **State value:** `configuring`
- **Phase-specific:** no
- **Responsibility:** generates complete and consistent target-project Understanding for downstream Planning and Development.
- **Inputs:** `.interface/project.md`, existing `.interface/config/`, and the applicable Component Layers located in the file map.
- **Resolution:** for every current Component, resolve target-project Understanding through its Principles and Preferences and express it in the form required by its Schema.
- **Completeness:** produce one structurally valid current configuration for every Component; an empty Layer never removes a required Component output.
- **Refresh:** rebuild a complete candidate from current sources on every run and reconcile it with existing generated configuration.
- **Preservation:** remove stale interpreter-owned information while preserving information owned by the human, runtime, or another operation according to current authorities.
- **Validation:** validate each candidate against its Schema and the complete set for cross-Component consistency before writing.
- **Idempotency:** unchanged inputs and owned generated information produce no change on another run.
- **Output:** `.interface/config/`.

The generated Understanding must allow Planning and Development to work without independently reinterpreting `.interface/project.md`.

#### Planning

- **State value:** `planning`
- **Phase-specific:** yes
- **Responsibility:** transforms generated Understanding for one requested phase into bounded, verifiable activities without prescribing implementation.
- **Inputs:** the requested phase from `.interface/config/definition.yaml`, generated Understanding under `.interface/config/`, and the Task Component authorities.
- **Scope:** the requested phase; its target selects the Component being planned.
- **Output:** `.interface/config/task.yaml`.

#### Development

- **State value:** `development`
- **Phase-specific:** yes
- **Responsibility:** executes and verifies eligible planned Tasks to produce project implementation.
- **Inputs:** generated Understanding under `.interface/config/` and planned Tasks in `.interface/config/task.yaml`.
- **Scope:** the requested phase; its target selects the Component being developed.
- **Output:** implementation inside the selected Component's resolved code boundary.

### Generated configuration

The `.interface/config/` directory is not a fourth descriptive Layer. It is the generated target-project Understanding: the project-specific result produced from `.interface/project.md`, the applicable Principles and Preferences, and the forms defined by the Schemas.

| File | Responsibility |
| --- | --- |
| `.interface/config/definition.yaml` | Project description, conceptual Models, project Structure, Behaviours, and ordered phases |
| `.interface/config/model.yaml` | Resolved Model package, modeling technology, public interface, Models, fields, relationships, rules, and initial data |
| `.interface/config/development.yaml` | Application layers, centralized runtime configuration, packages, declared-interface connections, cross-cutting capabilities, and Platform composition and deployment |
| `.interface/config/state.yaml` | Available Modes, current active State, critical Blockers, and Open Questions |
| `.interface/config/task.yaml` | Plans, contextual Groups, independently understandable Tasks, progress, and Task-local history |
| `.interface/config/backend.yaml` | Backend technology and resolved Logic, Data Access, and API configuration |
| `.interface/config/frontend.yaml` | Resolved Presentation, Interaction Logic, API Access, and visual-system configuration |
| `.interface/config/database.yaml` | Resolved Database package, Engines, Instances, default Instance, typed Model interface, mapping rules, and Storage Adapter configuration |

Development defines the target project's runtime-configuration boundary. By default, non-secret user-editable settings and Layer bindings live in `application.yaml`, while `.env` supplies secret values and private environment settings. Platform validates these sources and injects only the applicable section and declared bindings into each package.

Project phases remain the units of Planning and Development. A phase target selects the Component developed by that phase; Development independently describes how the selected technical Components connect and operate together.

## Agent Skills

Agent Skills are external capabilities that execute Interface Modes or supporting operations. Their integration metadata does not define the Interface Structure, grant authority, or replace the instructions and shared rules owned by the Claude configuration layer.

| Integration | Skill | Path | Invocation | Responsibility | Mode |
| --- | --- | --- | --- | --- | --- |
| Interpreter | `my-interface-interpreter` | `.claude/skills/my-interface-interpreter/SKILL.md` | `/my-interface-interpreter` | Generate or refresh complete target-project Understanding for every current Component and reconcile it for Planning and Development | Configuring |
| Tasker | `my-interface-tasker` | `.claude/skills/my-interface-tasker/SKILL.md` | `/my-interface-tasker <phase-number>` | Create or reconcile an activity Plan with expected results and verification without prescribing implementation | Planning |
| Developer | `my-interface-developer` | `.claude/skills/my-interface-developer/SKILL.md` | `/my-interface-developer <phase-number>` | Implement and verify eligible planned Tasks for one requested phase | Development |
| Reviewer | `my-interface-reviewer` | `.claude/skills/my-interface-reviewer/SKILL.md` | `/my-interface-reviewer <phase-number>` | Review one implemented phase and report evidence-based findings without repairing it | — |
| Reset | `my-interface-reset` | `.claude/skills/my-interface-reset/SKILL.md` | `/my-interface-reset <1\|2\|3>` | Preview and, after human confirmation, reset Interpreter output, Task output, or developed implementation | — |
| Skill Installer | `my-interface-skill-installer` | `.claude/skills/my-interface-skill-installer/SKILL.md` | `/my-interface-skill-installer` | Discover and install compatible Agent Skills for technologies detected in configured target-project Understanding | — |

The reset stages are:

1. **Interpreter:** remove root implementation directories when present and clear every entry inside `.interface/config/`.
2. **Task:** remove root implementation directories, clear Groups and Tasks while preserving phase Plan shells, set active State to `not set`, and clear the active phase.
3. **Develop:** remove root implementation directories, preserve Tasks and their history while returning every Task to `todo`, set active State to `planning`, and clear the active phase.

The fixed root implementation directories currently recognized by Reset are `model/`, `database/`, `backend/`, `frontend/`, and `developer/`.

## Workflow

| Order | Step | Actor or Skill | Action |
| --- | --- | --- | --- |
| 1 | Define the Project | Developer | Define the target project, its Models, and its ordered phases in `.interface/project.md` |
| 2 | Interpret the Project | `/my-interface-interpreter` | Generate or refresh target-project Understanding in `.interface/config/` |
| 3 | Generate Tasks | `/my-interface-tasker <phase-number>` | Create or reconcile the Plan for the requested phase |
| 4 | Develop the Tasks | `/my-interface-developer <phase-number>` | Implement and verify eligible Tasks for the requested phase |
