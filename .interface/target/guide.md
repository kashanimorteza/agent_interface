# Target Guide

This Guide explains the Target Module and its authoritative definitions.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**
10. **[Understanding record](#understanding-record)**
11. **[Open decisions](#open-decisions)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

This Guide explains the Target Module: what it is, what its files hold, who owns them, and how the rest of the Interface reads them. It is Human-owned and explains; it does not redefine. The canonical definition remains `.interface/interface.md`, and where the two disagree the Interface file is correct.

The Target describes what the Interface is working on: an application, platform, service, API, module, package, subsystem, or other development subject.

### Purpose

A different Target can be provided without changing the Implementation or Agent definitions. That separation is one of the central principles of Agent Interface.

### How It Works

Target Understanding reads the two complementary Target definitions under their declared precedence. Config records operational work on the Target but never become a second Target definition.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Target** — the subject the Interface is working on.
- **Non-Technical Definition** — the Human's intent, context, and requirements without requiring technical formulation.
- **Technical Definition** — the Human's technical translation of the Non-Technical Definition and the primary authority when they conflict.
- **Phase** — an ordered Target stage with a stable identifier, Component target, enabled state, readiness state, and goal.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Target Structure
├── Non-Technical Definition
│   └── .interface/target/non-technical.md
└── Technical Definition
    └── .interface/target/technical.md
```

The Target is defined through two complementary, Human-owned sources. Each Target definition has a direct link to its authoritative file.

### Non-Technical Definition

The Human's initial statement of intent, context, and requirements without requiring technical formulation. An empty file contributes no information.

Responsibility: The Human's initial statement of intent, context, and requirements without requiring technical formulation; an empty file contributes no information.

→ [Read more about Non-Technical Definition](non-technical.md)

### Technical Definition

The Human, acting as the implementation, translates the Non-Technical Definition into this technical form without changing its meaning. It is the primary authority for the Target and takes precedence wherever the two definitions conflict.

Responsibility: The Human's technical translation of the Non-Technical Definition without changing its meaning; the primary authority on conflict.

→ [Read more about Technical Definition](technical.md)

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumed by Target Understanding** — supplies the current meaning of the Target.
- **Consumed by Implementation** — supplies intent and phase requirements without becoming Implementation policy.
- **Recorded by Config** — supplies phase identifiers for operational records; Config does not define the Target.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

Target definitions do not contain Implementation philosophy, Agent behavior, generated Config, or runtime state. Target definitions are intentionally not Foundation Files: they belong to the Target concept itself.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

The Non-Technical Definition provides intent and context. The Technical Definition provides the technical translation and takes precedence wherever the two conflict.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns both Target definitions and every other authored Interface source. No Skill writes to `.interface/target/`. The Interface file remains the canonical navigation authority.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

The Target definitions are the authorities for Target meaning. This Guide explains and maps them; it does not introduce a second Target definition.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

- **Must** — read both Target definitions when Target Understanding is required.
- **Must** — use the Technical Definition as the authority on conflict.
- **Never** — copy Target meaning into Config or treat operational records as a Target definition.

<br>

<!--------------------------------------------------------------------------------- Understanding record --->
## Understanding record

Not yet recorded. The Human's own explanation of the Target Module — its intent, how the two definitions are meant to be written, and what a good Target definition looks like — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

<!--------------------------------------------------------------------------------- Open decisions --->
## Open decisions

- The current Non-Technical Definition is empty; the Target is defined only technically. Whether that is intended for this Target, or the Human wants to record intent there, is undecided.
