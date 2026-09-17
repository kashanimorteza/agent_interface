# Foundation Files

This document explains the Foundation directory: what it holds, why those files are shared by the whole Interface, and who may change them. It is Human-owned and explains; it does not redefine. The canonical definition remains `interface.md`, one level above this directory, which describes the complete system; this document describes only this directory and its contents.

Foundation is not one of the three Modules (Target, Implementation, Agent). It is the set of shared resources those Modules and every Skill depend on.

<br>

## Purpose

Foundation Files provide the foundational definitions and schemas required by the Interface: the canonical Interface document that every Understanding starts from, the Schemas that define how authored and generated files are shaped, and the Config records that coordinate the Workflow.

<br>

## Structure

```text
.interface/interface.md          ← the Interface file, one level above
.interface/foundation/
├── guide.md
├── understanding.md
├── operations.md
├── modes.md
├── authority.md
├── workflow.md
├── config/
│   ├── application.yaml
│   ├── state.yaml
│   ├── plan.yaml
│   └── review.yaml
└── schema/
    ├── application.yaml
    ├── yaml.yaml
    ├── principles.md
    ├── preferences.yaml
    ├── agent-profile.yaml
    ├── skill-contract.md
    ├── state.yaml
    ├── plan.yaml
    └── review.yaml
```

<br>

## Interface file

[`interface.md`](../interface.md), one level above this directory, is the canonical definition, navigation entry point, and complete file map of Agent Interface. Interface Understanding — required by every Skill — starts exclusively from this file and follows only the routes it provides for the active role. For every operation except Agent Sync, those routes lead to Target, Implementation, Foundation, Config, and synchronized Runtime resources; seeing the Agent Structure in this file never authorizes entry into the Agent Module.

<br>

## Interface sections kept as separate files

Five sections of the Interface were moved out of `interface.md` verbatim on 2026-09-17 so that the entry file stays a map. Each is part of Interface Understanding: a Skill reads `interface.md` and then these files before acting. Introduction and Terminology remain inside `interface.md`.

- [`understanding.md`](understanding.md) — Interface Understanding and Target Understanding, their sources and precedence, and the Agent Module exception.
- [`operations.md`](operations.md) — the nine Operations and the Skill that performs each.
- [`modes.md`](modes.md) — the Modes State may record.
- [`authority.md`](authority.md) — record ownership and each Skill's write authority.
- [`workflow.md`](workflow.md) — the Workflow and its Default, Normal, and Detailed paths.

<br>

## Config

Config stores the mutable operational records used while executing the Interface. It coordinates the Workflow and records where work stands; it does not store what the Target means and never becomes a second project definition.

- [`config/application.yaml`](config/application.yaml) — **Application Manifest**: one public metadata section for every Implementation Component; sections may remain empty until their owners publish metadata.
- [`config/state.yaml`](config/state.yaml) — **State**: active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions.
- [`config/plan.yaml`](config/plan.yaml) — **Plan**: Plans, Groups, Tasks, their dependencies, status, and history.
- [`config/review.yaml`](config/review.yaml) — **Review**: reviewed phases, outcomes, Findings, evidence, and Finding status.

`config/` is the only mutable exception in the otherwise read-only `.interface/` tree. Configure creates these files from their Schemas; afterwards each Skill writes only the records it has authority over, always under the rules of the owning Component (Plan, Review, or State).

<br>

## Schema

Schemas define the structure followed by authored Interface files and generated operational records. Two kinds exist:

**Structure standards** — the shape a Human-authored file follows:

- [`schema/yaml.yaml`](schema/yaml.yaml) — the common outer frame (meta, policy, read_order, content_map, content) followed by Implementation Preferences, Agent Profiles, and Config files.
- [`schema/principles.md`](schema/principles.md) — the common Markdown structure of every Implementation and Agent Component `principles.md`.
- [`schema/preferences.yaml`](schema/preferences.yaml) — the four-section structure of every Implementation `preferences.yaml`.
- [`schema/agent-profile.yaml`](schema/agent-profile.yaml) — the three-section structure of every Agent `profile.yaml`.
- [`schema/skill-contract.md`](schema/skill-contract.md) — the portable, runtime-independent structure of every Agent Skill Contract.

**Operational formats** — the stored structure and initial template of a generated record:

- [`schema/application.yaml`](schema/application.yaml) → generates `config/application.yaml`.
- [`schema/state.yaml`](schema/state.yaml) → generates `config/state.yaml`.
- [`schema/plan.yaml`](schema/plan.yaml) → generates `config/plan.yaml`.
- [`schema/review.yaml`](schema/review.yaml) → generates `config/review.yaml`.

Schema definition files use their own formats and do not follow the outer YAML frame they define.

The Interface file's own statement of the Foundation Files, moved here verbatim on 2026-09-17:

Foundation Files provide foundational definitions and schemas required by the Interface.


<!-------------------------- Foundation Structure -->
### Structure

```text
.interface/foundation/
├── interface.md
├── guide.md
├── config/
└── schema/
```

Target Definitions are intentionally **not** considered Foundation Files because they belong to the Target concept itself.


<!-------------------------- Interface Foundation File -->
### Interface File

```text
name = Interface
path = .interface/interface.md
responsibility = Canonical definition, navigation entry point, and entry point to the complete file map of Agent Interface; each Module's own files are mapped in its guide
```


<!-------------------------- Config Foundation Files -->
### Config Files

Config stores mutable operational information used while executing the Interface.

```text
.interface/foundation/config/
├── application.yaml
├── state.yaml
├── plan.yaml
└── review.yaml
```


#### Application Manifest Config

```text
name = Application Manifest Config
path = .interface/foundation/config/application.yaml
responsibility = Stores one public metadata section for every Implementation Component; sections may remain empty until their owners publish metadata
```


#### State Config

```text
name = State Config
path = .interface/foundation/config/state.yaml
responsibility = Stores active Workflow position, aggregate phase progress, Implement and Launch results, access points, History, Blockers, and Open Questions
```


#### Plan Config

```text
name = Plan Config
path = .interface/foundation/config/plan.yaml
responsibility = Stores Plans, Groups, Tasks, their dependencies, status, and history
```


#### Review Config

```text
name = Review Config
path = .interface/foundation/config/review.yaml
responsibility = Stores reviewed phases, outcomes, Findings, evidence, and Finding status
```


<!-------------------------- Schema Foundation Files -->
### Schema Files

Schemas define the structure followed by authored Interface files and generated operational records.

```text
.interface/foundation/schema/
├── application.yaml
├── yaml.yaml
├── principles.md
├── preferences.yaml
├── agent-profile.yaml
├── skill-contract.md
├── state.yaml
├── plan.yaml
└── review.yaml
```


#### Application Manifest Schema

```text
name = Application Manifest Schema
path = .interface/foundation/schema/application.yaml
kind = Operational format
generates = .interface/foundation/config/application.yaml
responsibility = Defines the shared Component metadata sections and their empty initial structure
```


#### YAML Schema

```text
name = YAML Schema
path = .interface/foundation/schema/yaml.yaml
kind = Structure standard
responsibility = Defines the common outer structure followed by Implementation Preferences, Agent Profiles, and Config files
scope = Schema definition files use their own formats and do not follow this outer structure
```


#### Principles Schema

```text
name = Principles Schema
path = .interface/foundation/schema/principles.md
kind = Structure standard
responsibility = Defines the common Markdown structure followed by every Implementation and Agent Component principles.md file
```


#### Preferences Schema

```text
name = Preferences Schema
path = .interface/foundation/schema/preferences.yaml
kind = Structure standard
responsibility = Defines the four-section structure followed by every Implementation Component preferences.yaml file
```


#### Agent Profile Schema

```text
name = Agent Profile Schema
path = .interface/foundation/schema/agent-profile.yaml
kind = Structure standard
responsibility = Defines the three-section structure followed by every Agent Component profile.yaml file
```


#### Skill Contract Schema

```text
name = Skill Contract Schema
path = .interface/foundation/schema/skill-contract.md
kind = Structure standard
responsibility = Defines the portable, runtime-independent structure followed by every declared Agent Skill Contract
```


#### State Schema

```text
name = State Schema
path = .interface/foundation/schema/state.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of State Config
generates = .interface/foundation/config/state.yaml
```


#### Plan Schema

```text
name = Plan Schema
path = .interface/foundation/schema/plan.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of Plan Config
generates = .interface/foundation/config/plan.yaml
```


#### Review Schema

```text
name = Review Schema
path = .interface/foundation/schema/review.yaml
kind = Operational format
responsibility = Defines the stored structure and initial values of Review Config
generates = .interface/foundation/config/review.yaml
```

<br>

## Ownership

The Human owns `interface.md`, this document, the five section files, and every Schema. Config records belong to the Components that own them — Plan, State, and Review — and are written only by the Skills the Interface authorizes for each record. Target definitions are intentionally not Foundation Files; they belong to the Target Module.

<br>

## Understanding record

Not yet recorded. The Human's own explanation of Foundation — why the Interface file is the single entry point, how Schemas are meant to evolve, and what Config must never become — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

## Open decisions

None recorded yet.
