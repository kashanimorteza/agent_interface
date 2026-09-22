# Agent Skill Definition

Agent Skill is the Agent Component that defines the shared Skill concept, Core Skill Contracts, and Provider Skills.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Components](#components)**
3. **[Authority](#authority)**




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
│   └── Implement
└── Provider Skills
```

### Core Skills

Each Core Skill has one Contract in `contracts/`.

The Contract's `Source` section identifies where the Core Skill's Understanding begins. The Contract and every source it names are read together to establish the Skill's complete Meaning and Content. A Core Skill is implemented from that Understanding rather than by copying its sources verbatim.

### Configure

Configure is used for configuring.

→ [Contract of Configure](contracts/configure.md)<br>


### Plan

Plan is used for planning.

→ [Contract of Plan](contracts/plan.md)<br>


### Develop

Develop is used for developing.

→ [Contract of Develop](contracts/develop.md)<br>


### Review

Review is used for reviewing.

→ [Contract of Review](contracts/review.md)<br>


### Implement

Implement is used for implementing.

→ [Contract of Implement](contracts/implement.md)<br>


### Provider Skills

Provider Skills are self-contained and held in [providers/](providers/). They have no Contract or `Source` section because their directories contain everything they need. Provider content is copied as it stands. None are declared currently.




<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is authoritative for the shared Skill concept.
