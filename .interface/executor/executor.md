# Executor Module Guide

The Executor Module is the Human-owned, Runtime-independent declaration of how the Agent operates, realized in an Agent Native only through Agent Native Implement.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Components](#components)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[Review](#review)**
10. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

The Executor Module is one of the three primary Interface Modules, alongside Target and Implementation. It covers the Agent's behavior, Skills, Rules, limits, responsibilities, capabilities, and boundaries.

The Guide explains the Executor Module and maps every Component's Definition, Preferences, or Contracts.

### Purpose

The Module exists so the Human defines the Agent once instead of creating a separate configuration for each Agent Native. The Human's complete view of Agent behavior is organized here through the Module's Components and can then be realized by different Native environments.

### How It Works

The Executor Module is composed of Components. Each Component has a Definition for its portable meaning and mandatory Principles; every Component except Skill has Preferences; Skill and Rule hold their declarations in Contracts, and Skill also holds ready-made Provider Skills in `providers/`.

Agent Native Implement reads the complete Module and realizes it in the Agent Native; every other role uses that realization.

The Foundation File [Agent Native Implement](../foundation/create-agent-native-implement.md) defines how an Agent Native creates and runs its Agent Native Implement Skill; changes here take effect in a Native only through Agent Native Implement.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Agent** — the AI that carries out the work; the Executor Module describes it and an Agent Native realizes it.
- **Executor Module** — the portable, Human-owned declaration of how an Agent and its capabilities operate.
- **Agent Native** — the Agent that runs Agent Native Implement and realizes the Executor Module; the Module never names one.
- **Agent Native Implement** — the Skill that reads the Executor Module and realizes it in the Agent Native.
- **Component** — one bounded part of the Executor Module with its own Definition and, where applicable, Preferences or Contracts.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

The Executor Module is organized into bounded Components.

```text
Executor
└── Components
    ├── Rule
    ├── Skill
    ├── Permission
    ├── Connection
    └── Output Style
```

<br>

<!--------------------------------------------------------------------------------- Components --->
## Components

The instructions for Agent Native Implement live in a Foundation File; Agent Native Implement is not an Executor Component.

### Rule

Persistent behavioral instructions.

→ [Definition of Rule](rule/rule.md)<br>
→ [Preferences of Rule](rule/rule.yaml)<br>
→ [Contracts of Rule](rule/contracts/)

### Skill

Reusable knowledge and workflows.

→ [Definition of Skill](skill/skill.md)<br>
→ [Contracts of Skill](skill/contracts/)<br>
→ [Provider Skills of Skill](skill/providers/)

### Permission

Access boundaries and Enforced Guarantees.

→ [Definition of Permission](permission/permission.md)<br>
→ [Preferences of Permission](permission/permission.yaml)

### Connection

Services and packages obtained from outside the project.

→ [Definition of Connection](connection/connection.md)<br>
→ [Preferences of Connection](connection/connection.yaml)

### Output Style

How the Agent's output is presented.

→ [Definition of Output Style](output-style/output-style.md)<br>
→ [Preferences of Output Style](output-style/output-style.yaml)


<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Target meaning** — belongs to Target, because it describes the project being built rather than how the Agent operates.
- **Implementation engineering philosophy** — belongs to Implementation, because it describes how the project is built rather than how the Agent operates.
- **Agent Native layout, commands, and configuration format** — belongs to Agent Native Implement, because it describes Native realization rather than the portable Executor Module.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

`<component>.md` states the portable view and philosophy; YAML files hold current selections where needed, and Skill and Rule Contracts hold their declarations.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns the Executor Module and is the only actor allowed to change its files. Agent Native Implement reads the Module read-only and realizes its declarations in the Agent Native. No other Skill, Agent Instance, or automation reads or changes the Module.

Preferences and Contracts can never override a Principle, and a Native realization may only preserve or strengthen the Module's meaning, never weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### What success means

**Rule:** Agent Native Implement succeeds only when it has understood the complete Module, transferred its meaning to the Agent Native without changing its scope or authority, and the Agent behaves accordingly.

**Why:** Existing files and loaded rules do not show that the Agent behaves as intended.

**Boundary:** Observed behavior, not the presence of artifacts, is the evidence of success.

### Each Component governs only itself

**Rule:** A Component's Principles and Preferences are authoritative for that Component only. A Native capability not declared by its owning Component is optional; a required declaration the Agent Native cannot realize is reported as a gap.

**Why:** Clear ownership lets each Component change without silently redefining another.

**Boundary:** A Component may name another Component's capability only to use it, never to redefine it.

### Declarations stay portable

**Rule:** Text that Agent Native Implement must carry as written lives in its own Contract file, and declarations are grouped by capability kind, never by an Agent Native's location or format.

**Why:** The same Module can then be realized by any Agent Native without rewriting it.

**Boundary:** How and where a declaration is realized is decided by the Agent Native during Agent Native Implement.

<br>

<!--------------------------------------------------------------------------------- Review --->
## Review

### Conformance

- The success condition under Principles holds: the Native behaves as the Module declares.

### Checks

- Every Component in Architecture has a section under Components, and every Definition, Preferences, and Contracts link it gives exists.
- Every Component's own Review passes in the Agent Native.

<br>

<!--------------------------------------------------------------------------------- At_a_Glance --->
## At a Glance

- **Human-owned** — the Executor Module is the portable source of the Agent's meaning and declarations.
- **Read-only** — only Agent Native Implement reads the Module.
- **Realized** — Agent Native Implement transfers its meaning to the Agent Native without changing its scope or authority.
- **Self-governed** — each Component is authoritative only for itself; an unrealizable required declaration is reported as a gap.
- **Portable** — declarations are grouped by capability kind, never by a Native's location or format.
