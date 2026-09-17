# Implementation

This document explains the Implementation Module: what it is, what its Components are, how Principles and Preferences divide its content, and how the rest of the Interface reads it. It is Human-owned and explains; it does not redefine. The canonical definition remains `.interface/interface.md`, and each Component's Principles are the authority for that Component; where this document disagrees with either, they are correct.

<br>

## Purpose

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target — **how the implementation wants software to be built** — independently of any particular Target or Agent. A different Implementation can provide a different programming philosophy without changing the Target, and the same Implementation can be handed unchanged to another project.

<br>

## Principles and Preferences

Each Implementation Component has two files.

- `principles.md` is the authoritative expression of the Component's philosophy, responsibilities, rules, and boundaries. It follows the Principles Schema and contains no tool, library, framework, package, or version selection.
- `preferences.yaml` holds the Component's preferred engineering choices, defaults, packages, implementation conventions, and optional Agent Skill associations, used when the Target leaves a choice unspecified. It follows the Preferences Schema and can never override a Principle.

Explicit Target intent and applicable Principles guide the operational Skills; Preferences supply defaults where the Target leaves a choice unstated.

<br>

## Components

```text
Implementation Components
├── Development   → development/principles.md · development/preferences.yaml
├── Model         → model/principles.md · model/preferences.yaml
├── Database      → database/principles.md · database/preferences.yaml
├── Logic         → logic/principles.md · logic/preferences.yaml
├── API           → api/principles.md · api/preferences.yaml
├── Presentation  → presentation/principles.md · presentation/preferences.yaml
├── Platform      → platform/principles.md · platform/preferences.yaml
├── Plan          → plan/principles.md · plan/preferences.yaml
├── Review        → review/principles.md · review/preferences.yaml
└── State         → state/principles.md · state/preferences.yaml
```

- **Development** — defines the layered architecture and how independent layers are composed into one system. [Principles](development/principles.md) · [Preferences](development/preferences.yaml)
- **Model** — describes the domain entities and provides one shared logical meaning for domain data. [Principles](model/principles.md) · [Preferences](model/preferences.yaml)
- **Database** — owns the persistence layer and publishes one generic interface for reading and writing. [Principles](database/principles.md) · [Preferences](database/preferences.yaml)
- **Logic** — implements application Behaviour as reusable Logic and publishes the Public Logic Interface. [Principles](logic/principles.md) · [Preferences](logic/preferences.yaml)
- **API** — runs the external API process and publishes the application's public contract through Logic. [Principles](api/principles.md) · [Preferences](api/preferences.yaml)
- **Presentation** — presents the application to users and consumes the capabilities Logic publishes through the API. [Principles](presentation/principles.md) · [Preferences](presentation/preferences.yaml)
- **Platform** — prepares a completed Target for operation and brings it online. [Principles](platform/principles.md) · [Preferences](platform/preferences.yaml)
- **Plan** — turns phases into bounded, verifiable activities organized as Plans, Groups, and Tasks. [Principles](plan/principles.md) · [Preferences](plan/preferences.yaml)
- **Review** — establishes whether implemented work satisfies what was asked, and records what it found. [Principles](review/principles.md) · [Preferences](review/preferences.yaml)
- **State** — records active position, aggregate phase progress, implementation, launch, History, Blockers, and Open Questions. [Principles](state/principles.md) · [Preferences](state/preferences.yaml)

The first seven Components describe the software being built; Plan, Review, and State are operational Components that also own records in Config (`plan.yaml`, `review.yaml`, `state.yaml`) whose storage shape is defined by the matching Schema.

The Interface file's own statement of the Implementation Module, moved here verbatim on 2026-09-17:

The Implementation module defines the reusable programming personality, standards, and engineering perspective applied to a Target. It expresses them through the Development, Model, Database, Logic, Presentation, Platform, Plan, Review, and State Components.


```text
Implementation Components
├── Development
│   ├── Principles  → .interface/implementation/development/principles.md
│   ├── Preferences → .interface/implementation/development/preferences.yaml
├── Model
│   ├── Principles  → .interface/implementation/model/principles.md
│   └── Preferences → .interface/implementation/model/preferences.yaml
├── Database
│   ├── Principles  → .interface/implementation/database/principles.md
│   └── Preferences → .interface/implementation/database/preferences.yaml
├── Logic
│   ├── Principles  → .interface/implementation/logic/principles.md
│   └── Preferences → .interface/implementation/logic/preferences.yaml
├── API
│   ├── Principles  → .interface/implementation/api/principles.md
│   └── Preferences → .interface/implementation/api/preferences.yaml
├── Presentation
│   ├── Principles  → .interface/implementation/presentation/principles.md
│   └── Preferences → .interface/implementation/presentation/preferences.yaml
├── Platform
│   ├── Principles  → .interface/implementation/platform/principles.md
│   └── Preferences → .interface/implementation/platform/preferences.yaml
├── Plan
│   ├── Principles  → .interface/implementation/plan/principles.md
│   └── Preferences → .interface/implementation/plan/preferences.yaml
├── Review
│   ├── Principles  → .interface/implementation/review/principles.md
│   └── Preferences → .interface/implementation/review/preferences.yaml
└── State
    ├── Principles  → .interface/implementation/state/principles.md
    └── Preferences → .interface/implementation/state/preferences.yaml
```

Each Component below has its own Principles and Preferences. Principles are the authoritative expression of the Component's philosophy and view; Preferences contain its preferred choices and default settings. Follow the links to open the authoritative file for that Component.

### Development

Defines the layered architecture and how independent layers are composed into one system.

- [Principles](development/principles.md)
- [Preferences](development/preferences.yaml)

### Model

Describes the domain entities and provides one shared logical meaning for domain data.

- [Principles](model/principles.md)
- [Preferences](model/preferences.yaml)

### Database

Owns the persistence layer and publishes one generic interface for reading and writing.

- [Principles](database/principles.md)
- [Preferences](database/preferences.yaml)

### Logic

Implements application Behaviour as reusable Logic.

- [Principles](logic/principles.md)
- [Preferences](logic/preferences.yaml)

### API

Runs the external API process and publishes the application's public contract through Logic.

- [Principles](api/principles.md)
- [Preferences](api/preferences.yaml)

### Presentation

Presents the application to users and consumes the capabilities Logic publishes.

- [Principles](presentation/principles.md)
- [Preferences](presentation/preferences.yaml)

### Platform

Prepares a completed Target for operation and brings it online.

- [Principles](platform/principles.md)
- [Preferences](platform/preferences.yaml)

### Plan

Turns phases into bounded, verifiable activities organized as Plans, Groups, and Tasks.

- [Principles](plan/principles.md)
- [Preferences](plan/preferences.yaml)

### Review

Establishes whether implemented work satisfies what was asked, and records what it found.

- [Principles](review/principles.md)
- [Preferences](review/preferences.yaml)

### State

Records active position, aggregate phase progress, implementation, launch, History, Blockers, and Open Questions.

- [Principles](state/principles.md)
- [Preferences](state/preferences.yaml)

The Component's own Principles remain the authority: when this summary and a Component's Principles disagree, the Principles are correct.

<br>

## How the Implementation is used

Every operational Skill reads the applicable Implementation Principles and Preferences for its role: Planning to define Tasks, Developing to implement and verify them, Review to evaluate the result, Configure to resolve technical requirements, and Launch to bring the Target online through Platform. Implementation sources are read directly; they are not routed through Agent Sync, because they describe how software is built rather than how the Agent behaves.

<br>

## Ownership

The Human owns every Principles and Preferences file. Plan, Review, and State own their operational records under Config and are the only Implementation Components a Skill may write on behalf of — and only inside `.interface/foundation/config/`, within the write authority the Interface states for that Skill.

<br>

## Understanding record

Not yet recorded. The Human's own explanation of the Implementation Module — the engineering philosophy behind the layered architecture, why these ten Components, and how Preferences are meant to be chosen — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

## Open decisions

None recorded yet.
