# Agent Skill Definition

Agent Skill is the Agent Component that defines the shared Skill concept, Core Skill Contracts, and Provider Skills.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Components](#components)**
3. **[Authority](#authority)**
4. **[Principles](#principles)**
5. **[Review](#review)**
6. **[At a Glance](#at-a-glance)**




<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Purpose

Skill provides one consistent way to describe a reusable capability without repeating its framework or its Skill-specific content.

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

### Configure

→ [Contract of Configure](contracts/configure.md)<br>

### Plan

→ [Contract of Plan](contracts/plan.md)<br>

### Develop

→ [Contract of Develop](contracts/develop.md)<br>

### Review

→ [Contract of Review](contracts/review.md)<br>

### Implement

→ [Contract of Implement](contracts/implement.md)<br>

### Launch

→ [Contract of Launch](contracts/launch.md)<br>

### Reset

→ [Contract of Reset](contracts/reset.md)<br>

### Provider Skills

Provider Skills are self-contained: they have no Contract or `Source` section, and their content is taken as its provider supplies it.

- **graphify** — the knowledge-graph Skill supplied by the graphify package; it turns project files into a queryable graph used for codebase questions.




<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is authoritative for the shared Skill concept.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

### Every Core Skill execution is logged in State

**Rule:** Every Core Skill execution creates one Log Entry in State with its ID and Skill, and updates that same entry with outcome, report, and any applicable data, Open Questions, or Blockers when work completes, stops, or is blocked.

**Why:** Each execution leaves one attributable record that later runs and the Human can inspect.

**Boundary:** A Contract may add Skill-specific logging; it never removes this record.

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
