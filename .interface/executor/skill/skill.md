# Agent Skill Definition

Agent Skill is the Executor Component that defines the shared Skill concept, Core Skill Contracts, and Provider Skills.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Components](#components)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[Review](#review)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Purpose

Skill provides one consistent way to describe a reusable capability without repeating its framework or its Skill-specific content.

### How It Works

Agent Native Implement builds each Core Skill in the Agent Native from its Contract and every Source the Contract names, and installs each Provider Skill as its declared package supplies it.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Core Skill** — a Skill built from a Contract and the Sources it names.
- **Provider Skill** — a self-contained Skill taken as its declared package supplies it.
- **Contract** — the declaration of one Core Skill: its identity, inputs, invocation, outputs, and Sources.

<br>

<!--------------------------------------------------------------------------------- Components --->
## Components

```text
Components
├── Core Skills
│   ├── Configure
│   ├── Plan
│   ├── Develop
│   ├── Review
│   ├── Implement
│   ├── Launch
│   └── Reset
└── Provider Skills
```

### Core Skills

Each Core Skill has one Contract in `contracts/`.

The Contract's `Source` section identifies where the Core Skill's Understanding begins. The Contract and every source it names are read together to establish the Skill's complete Meaning and Content. A Core Skill is implemented from that Understanding rather than by copying its sources verbatim.

#### Configure

→ [Contract of Configure](contracts/configure.md)<br>

#### Plan

→ [Contract of Plan](contracts/plan.md)<br>

#### Develop

→ [Contract of Develop](contracts/develop.md)<br>

#### Review

→ [Contract of Review](contracts/review.md)<br>

#### Implement

→ [Contract of Implement](contracts/implement.md)<br>

#### Launch

→ [Contract of Launch](contracts/launch.md)<br>

#### Reset

→ [Contract of Reset](contracts/reset.md)<br>

### Provider Skills

Provider Skills are self-contained: they have no Contract or `Source` section, and their content is taken as its provider supplies it.

- **graphify** — the knowledge-graph Skill supplied by the graphify package; it turns project files into a queryable graph used for codebase questions.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

This Definition carries the portable meaning and mandatory Principles of the Skill Component. Contracts carry each Core Skill's declaration. Agent Native Implement reads both and realizes them without changing their scope or authority.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns this Definition and its Contracts. Every Principle in this file is mandatory; Contracts can never override a Principle, and Agent Native Implement is the only reader authorized to realize the Component in an Agent Native.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Every Core Skill execution is logged in State

**Rule:** Every Core Skill execution creates one Log Entry in State with its ID and Skill, and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

**Why:** Each execution leaves one attributable record that later runs and the Human can inspect.

**Boundary:** A Contract may add Skill-specific logging; it never removes this record.

### Core Skills never invoke one another

**Rule:** A Core Skill never invokes another Core Skill. Only Implement invokes Core Skills, and only Configure, Plan, Develop, and Review. Every Core Skill may use any Provider Skill or other available Skill.

**Why:** Each Core Skill keeps one responsibility, and the workflow order has a single owner.

**Boundary:** This limits only Core Skills; Provider Skills and other available Skills are unaffected.

<br>

<!--------------------------------------------------------------------------------- Review --->
## Review

### Conformance

- Every Principle above is realized in the Agent Native.

### Checks

- Every Core Skill has exactly one Contract, and every Contract's Skill exists in the Agent Native under its declared Skill name.
- Every Contract's `Source` paths exist.
- Every Core Skill execution has one State Log Entry.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

**Every Core Skill execution is logged in State**

- **Must** — create and complete one State Log Entry per execution.

**Core Skills never invoke one another**

- **Must** — let only Implement invoke Configure, Plan, Develop, and Review.
- **Never** — invoke one Core Skill from another.
