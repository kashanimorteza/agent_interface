# Target

This document explains the Target Module: what it is, what its files hold, who owns them, and how the rest of the Interface reads them. It is Human-owned and explains; it does not redefine. The canonical definition remains `.interface/interface.md`, and where the two disagree the Interface file is correct.

<br>

## Purpose

The Target describes **what the Interface is working on** — the application, platform, service, API, module, package, subsystem, or other development subject. The term Target is preferred over "Target Project" because the subject does not have to be an entire project. A different Target can be provided without changing the Implementation or Agent definitions; that separation is one of the central principles of Agent Interface.

<br>

## Structure

```text
Target Structure
├── Non-Technical Definition
│   └── .interface/target/non-technical.md
└── Technical Definition
    └── .interface/target/technical.md
```

The Target is defined through two complementary, Human-owned sources:

- **[Non-Technical Definition](non-technical.md)** — the Human's initial statement of intent, context, and requirements without requiring technical formulation. An empty file contributes no information.
- **[Technical Definition](technical.md)** — the Human, acting as the implementation, translates the Non-Technical Definition into this technical form without changing its meaning. It is the primary authority for the Target and takes precedence wherever the two definitions conflict.

Target definitions are intentionally not Foundation Files: they belong to the Target concept itself.

The Interface file's own statement of the Target, moved here verbatim on 2026-09-17:

The Target describes **what the Interface is working on**.


```text
Target Structure
├── Non-Technical Definition
│   └── .interface/target/non-technical.md
└── Technical Definition
    └── .interface/target/technical.md
```

The Target is defined through two complementary, human-owned sources:

- **Non-Technical Definition:** The Human's initial statement of intent, context, and requirements without requiring technical formulation; an empty file contributes no information.
- **Technical Definition:** The Human, acting as the implementation, translates the Non-Technical Definition into this technical form. It is the primary authority for the Target and takes precedence wherever the two definitions conflict.

Each Target definition has a direct link to its authoritative file:

- [Non-Technical Definition](non-technical.md)
- [Technical Definition](technical.md)

<br>

## How the Target is used

Target Understanding is one of the two kinds of Understanding a Skill establishes before acting. When a role needs Target meaning, it reads both definitions under the declared precedence — the Non-Technical Definition provides intent and context, the Technical Definition is the authority on conflict. Understanding is reconstructed from the current sources every time it is required and is never copied into Config as a second project definition.

The Technical Definition also carries the Target's Phases: the ordered stages of development, each with a stable identifier, a Component target, an enabled state, a readiness state, and a goal. Configure creates the phase records in State from those identifiers; Planning, Developing, and Review work phase by phase.

<br>

## Ownership

The Human owns both Target definitions and every other authored Interface source. No Skill writes to `.interface/target/`. Config stores operational records about the work on the Target but never defines the Target.

<br>

## Understanding record

Not yet recorded. The Human's own explanation of the Target Module — its intent, how the two definitions are meant to be written, and what a good Target definition looks like — will be captured here in a later session, in the same form as the Agent Module Guide.

<br>

## Open decisions

- The current Non-Technical Definition is empty; the Target is defined only technically. Whether that is intended for this Target, or the Human wants to record intent there, is undecided.
