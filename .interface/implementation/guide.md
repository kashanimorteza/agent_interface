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
→ [Preferences](development/preferences.yaml)

### Model

Describes the domain entities and provides one shared logical meaning for domain data.

```yaml
name: Model
principles: .interface/implementation/model/principles.md
preferences: .interface/implementation/model/preferences.yaml
responsibility: Describes the domain entities and provides one shared logical meaning for domain data; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](model/principles.md)<br>
→ [Preferences](model/preferences.yaml)

### Database

Owns the persistence layer and publishes one generic interface for reading and writing.

```yaml
name: Database
principles: .interface/implementation/database/principles.md
preferences: .interface/implementation/database/preferences.yaml
responsibility: Owns the persistence layer and publishes one generic interface for reading and writing; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](database/principles.md)<br>
→ [Preferences](database/preferences.yaml)

### Logic

Implements application Behaviour as reusable Logic.

```yaml
name: Logic
principles: .interface/implementation/logic/principles.md
preferences: .interface/implementation/logic/preferences.yaml
responsibility: Implements application Behaviour as reusable Logic; the Principles are the authority, the Preferences supply defaults where the Target is silent
```

→ [Principles](logic/principles.md)<br>
→ [Preferences](logic/preferences.yaml)

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

### Model (recorded 2026-09-18)

**What is the Model for, in the Human's words?** When the Agent has an Understanding of the Target, the Target has already declared its Models with their primary keys, auto-increment, nullability, defaults, relationships, and uniqueness, in its own language. Model must express those same parameters in one standard vocabulary that belongs to no technology and no database — type, size, relationships, generated identity — so that the Model can always be understood and built. Which type or size a field gets is Model's own decision from the Target; the Interface does not fix a closed list for it. Database using that vocabulary to build storage is one of Model's uses, not its main purpose; the main purpose is that Models are the shared language between every Component of the application. There is one definition, not a Model for code and a separate schema for storage. Because Model is also a Development Component, it takes its programming language, modeling package, and Agent Skills from its Component Profile in Development.

**Decisions taken on 2026-09-18 (reviewed item by item):**

1. The introduction and its Note already state this goal — unchanged.
2. Logical field type was missing from the published metadata (Principle 9 and the field vocabulary in Preferences); added as a technology-independent value type, never a language or Engine type.
3. Principle 9 now states explicitly that the metadata is carried by the same Domain Definition application code uses, with no second schema artifact; Database reads it through the Model Public Interface.
4. Former Principle 6 (field presence and absence semantics) overlapped with Principle 10 and was merged into it; Principles 7–10 became 6–9. Nothing was dropped.
5. `preferences.yaml`: `settings` made an explicit empty map; version 3.4.
6. Terms, Relationships, and the remaining Principles — unchanged.
7. Must line added: Model takes its language, modeling package, Agent Skills, and Platform Reference from its Component Profile in Development (Principle 3).
8. Introduction and Note reframed: every Component reads the same definition; Database is one consumer.
9. Principle 9 reframed from "storage-relevant constraints" to "one standard, technology-independent vocabulary".
10. `persistence_contract` renamed `declaration_vocabulary`; `length` and `precision` added; no closed list of types — Model decides type and size from the Target.
11. A rule forcing unexpressible Target properties through State was proposed and rejected as limiting Model; Principle 2 already covers preservation.

<br>

## Open decisions

None recorded yet.
