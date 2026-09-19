# Implementation

This document explains the Implementation Module: what it is, what its Components are, how Principles and Preferences divide its content, and how the rest of the Interface reads it. It is Human-owned and explains; it does not redefine. The canonical definition remains `.interface/interface.md`, and each Component's Principles are the authority for that Component; where this document disagrees with either, they are correct.

<br>

## Navigation

1. **[Purpose](#purpose)**
2. **[Principles and Preferences](#principles-and-preferences)**
3. **[Components](#components)**
   - **[Development](#development)**
   - **[Model](#model)**
   - **[Database](#database)**
   - **[Logic](#logic)**
   - **[API](#api)**
   - **[Presentation](#presentation)**
   - **[Platform](#platform)**
   - **[Plan](#plan)**
   - **[Review](#review)**
   - **[State](#state)**
4. **[How the Implementation is used](#how-the-implementation-is-used)**
5. **[Ownership](#ownership)**
6. **[Understanding record](#understanding-record)**
7. **[Open decisions](#open-decisions)**

<br>

## Purpose

The Implementation Module defines the reusable programming personality, standards, and engineering perspective applied to a Target — **how the implementation wants software to be built** — independently of any particular Target or Agent. A different Implementation can provide a different programming philosophy without changing the Target, and the same Implementation can be handed unchanged to another project.

<br>

## Principles and Preferences

Each Implementation Component has two files.

- `principles.md` is the authoritative expression of the Component's philosophy, responsibilities, rules, and boundaries. It follows the Principles Schema and contains no tool, library, framework, package, or version selection.
- `preferences.yaml` holds the Component's preferred engineering choices, defaults, packages, implementation conventions, and optional Agent Skill associations, used when the Target leaves a choice unspecified. It follows the Preferences Schema and can never override a Principle.
- `understanding.md` records how the Human explained the Component and the decisions that followed, including proposals that were not accepted and why. It states no obligation and is optional: a Component whose Understanding has not been recorded has no such file. It follows the Understanding Schema.

Explicit Target intent and applicable Principles guide the operational Skills; Preferences supply defaults where the Target leaves a choice unstated.

<br>

## Components

The Implementation module defines the reusable programming personality, standards, and engineering perspective applied to a Target. It expresses them through the Development, Model, Database, Logic, Presentation, Platform, Plan, Review, and State Components.

```text
Implementation Components
├── Development
├── Model
├── Database
├── Logic
├── API
├── Presentation
├── Platform
├── Plan
├── Review
└── State
```

Each Component below has its own Principles and Preferences. Principles are the authoritative expression of the Component's philosophy and view; Preferences contain its preferred choices and default settings. Follow the links to open the authoritative file for that Component.

The first seven Components describe the software being built; Plan, Review, and State are operational Components that also own records in Config (`plan.yaml`, `review.yaml`, `state.yaml`) whose storage shape is defined by the matching Schema.

### Development

Defines the layered architecture and how independent layers are composed into one system.

```yaml
name: Development
principles: .interface/implementation/development/principles.md
preferences: .interface/implementation/development/preferences.yaml
responsibility: Defines the layered architecture and how independent layers are composed into one system; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](development/principles.md)<br>
→ [Preferences](development/preferences.yaml)<br>
→ [Understanding](development/understanding.md)

### Model

Describes the domain entities and provides one shared logical meaning for domain data.

```yaml
name: Model
principles: .interface/implementation/model/principles.md
preferences: .interface/implementation/model/preferences.yaml
responsibility: Describes the domain entities and provides one shared logical meaning for domain data; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](model/principles.md)<br>
→ [Preferences](model/preferences.yaml)<br>
→ [Understanding](model/understanding.md)

### Database

Owns the persistence layer and publishes one generic interface for reading and writing.

```yaml
name: Database
principles: .interface/implementation/database/principles.md
preferences: .interface/implementation/database/preferences.yaml
responsibility: Owns the persistence layer and publishes one generic interface for reading and writing; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](database/principles.md)<br>
→ [Preferences](database/preferences.yaml)<br>
→ [Understanding](database/understanding.md)

### Logic

Implements application Behaviour as reusable Logic.

```yaml
name: Logic
principles: .interface/implementation/logic/principles.md
preferences: .interface/implementation/logic/preferences.yaml
responsibility: Implements application Behaviour as reusable Logic; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](logic/principles.md)<br>
→ [Preferences](logic/preferences.yaml)<br>
→ [Understanding](logic/understanding.md)

### API

Runs the external API process and publishes the application's public contract through Logic.

```yaml
name: API
principles: .interface/implementation/api/principles.md
preferences: .interface/implementation/api/preferences.yaml
responsibility: Runs the external API process and publishes the application's public contract through Logic; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](api/principles.md)<br>
→ [Preferences](api/preferences.yaml)

### Presentation

Presents the application to users and consumes the capabilities Logic publishes.

```yaml
name: Presentation
principles: .interface/implementation/presentation/principles.md
preferences: .interface/implementation/presentation/preferences.yaml
responsibility: Presents the application to users and consumes the capabilities Logic publishes; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](presentation/principles.md)<br>
→ [Preferences](presentation/preferences.yaml)

### Platform

Prepares a completed Target for operation and brings it online.

```yaml
name: Platform
principles: .interface/implementation/platform/principles.md
preferences: .interface/implementation/platform/preferences.yaml
responsibility: Prepares a completed Target for operation and brings it online; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](platform/principles.md)<br>
→ [Preferences](platform/preferences.yaml)

### Plan

Turns phases into bounded, verifiable activities organized as Plans, Groups, and Tasks. It also owns the operational record `foundation/config/plan.yaml`, whose storage shape is defined by `foundation/schema/plan.yaml`.

```yaml
name: Plan
principles: .interface/implementation/plan/principles.md
preferences: .interface/implementation/plan/preferences.yaml
responsibility: Turns phases into bounded, verifiable activities organized as Plans, Groups, and Tasks; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](plan/principles.md)<br>
→ [Preferences](plan/preferences.yaml)

### Review

Establishes whether implemented work satisfies what was asked, and records what it found. It also owns the operational record `foundation/config/review.yaml`, whose storage shape is defined by `foundation/schema/review.yaml`.

```yaml
name: Review
principles: .interface/implementation/review/principles.md
preferences: .interface/implementation/review/preferences.yaml
responsibility: Establishes whether implemented work satisfies what was asked, and records what it found; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](review/principles.md)<br>
→ [Preferences](review/preferences.yaml)

### State

Records active position, aggregate phase progress, implementation, launch, History, Blockers, and Open Questions. It also owns the operational record `foundation/config/state.yaml`, whose storage shape is defined by `foundation/schema/state.yaml`.

```yaml
name: State
principles: .interface/implementation/state/principles.md
preferences: .interface/implementation/state/preferences.yaml
responsibility: Records active position, aggregate phase progress, implementation, launch, History, Blockers, and Open Questions; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](state/principles.md)<br>
→ [Preferences](state/preferences.yaml)

The Component's own Principles remain the authority: when this summary and a Component's Principles disagree, the Principles are correct.

<br>

## How the Implementation is used

Every operational Skill reads the applicable Implementation Principles and Preferences for its role: Planning to define Tasks, Developing to implement and verify them, Review to evaluate the result, Configure to resolve technical requirements, and Launch to bring the Target online through Platform. Implementation sources are read directly; they are not routed through Agent Sync, because they describe how software is built rather than how the Agent behaves.

<br>

## Ownership

The Human owns every Principles and Preferences file. Plan, Review, and State own their operational records under Config and are the only Implementation Components a Skill may write on behalf of — and only inside `.interface/foundation/config/`, within the write authority the Interface states for that Skill.

<br>

## Understanding record

Not yet recorded in full. The Human's own explanation of the Implementation Module — the engineering philosophy behind the layered architecture, why these ten Components, and how Preferences are meant to be chosen — will be captured here in a later session, in the same form as the Agent Module Guide.

Component-level Understanding now lives in each Component's own `principles.md`, in its Understanding record section (moved there 2026-09-19, when the Principles file structure gained that section): Model in [model/principles.md](model/principles.md), Database in [database/principles.md](database/principles.md), Logic in [logic/principles.md](logic/principles.md), and Development's documentation Understanding in [development/principles.md](development/principles.md). What stays here is the Understanding of the Module as a whole.

<br>

## Open decisions

None recorded yet.
