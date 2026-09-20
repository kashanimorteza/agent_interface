# Implementation Guide

This Guide explains the Implementation Module. The Interface and each subject's Definition remain authoritative.

<br>

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Implementation is the reusable programming perspective applied to a Target. It has two distinct Subsystems: Development defines the product being built, and Process controls the work that builds, evaluates, and records it.

### Purpose

This Guide explains the Module's structure and keeps the Human's understanding of its two Subsystems available to later readers.

### How It Works

The Definition is authoritative for mandatory meaning and Principles. Preferences hold current choices. Skills operate under the authority of the relevant subject.

<br>

## Terms

- **Implementation** — the reusable Module that defines how a Target is built and how implementation work is controlled.
- **Development** — the Subsystem that defines the product Components, their composition, and technical realization.
- **Process** — the Subsystem that defines configuration, planning, review, and operational recording.
- **Subsystem** — a major part of Implementation with separate ownership.
- **Component** — a bounded subject within a Subsystem with its own Definition and Preferences.

<br>

## Architecture

```text
Implementation
└── Subsystems
    ├── Development
    └── Process
```

### Development

Development defines how independent product Components form one application system. It owns their composition, Component Profiles, Connections, shared technical catalogues, and cross-cutting standards.

```yaml
name: Development
definition: .interface/implementation/development/definition.md
preferences: .interface/implementation/development/preferences.yaml
responsibility: The product composition and technical realization of the independent Components that form the Target application.
```

→ [Definition](development/definition.md)<br>
→ [Preferences](development/preferences.yaml)

Model defines shared domain meaning and Domain Definitions. Database owns persistence and the public operations for stored data. Logic owns application Behaviour and exposes it through its Public Interface. API publishes the application's external API through Logic. Presentation presents the application through capabilities published by Logic. Platform defines how completed Development Components are prepared and brought online.

### Process

Process defines how work on Development is configured, planned, reviewed, and recorded. It owns no product Behaviour or Source.

```yaml
name: Process
definition: .interface/implementation/process/definition.md
preferences: .interface/implementation/process/preferences.yaml
responsibility: The configuration, planning, review, and operational recording of Implementation work.
```

→ [Definition](process/definition.md)<br>
→ [Preferences](process/preferences.yaml)

Configure prepares the operational Config records. Plan turns Target phases into bounded, understandable, and verifiable activities. Review establishes whether selected-phase work satisfies its applicable authorities and owns recorded Findings. State records aggregate operational position, progress, outcomes, History, Blockers, and Open Questions. The remaining Process Components coordinate the lifecycle around these responsibilities.

<br>

## Relationships

- **Consumes Target** — applies current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Process authorities used while implementation work is performed.
- **Contains Development and Process** — defines the product and operational ownership boundaries used by the Interface.

<br>

## Boundaries

Development owns product responsibilities. Process owns configuration, planning, review, and operational records. Neither Subsystem replaces the other.

<br>

## Layering

Technical choices and defaults belong to the Preferences file of the subject that owns them. Shared choices that genuinely span Development and Process belong to Implementation Preferences. The shape of a generated operational record belongs to its Schema.

<br>

## Authority

The Definition and Principles of each subject are authoritative for its meaning and mandatory rules. Preferences never override them. This Guide explains and maps those sources; it does not become a second authority.

<br>

## Principles

The mandatory Principles are recorded in [Implementation Definition](definition.md). This Guide does not repeat them.

<br>

## At a Glance

- **Must** — keep product construction in Development and implementation control in Process.
- **Must** — read each subject's Definition and Preferences through the links above.
- **Never** — let this Guide replace a subject's Definition, Preferences, or Schema.
