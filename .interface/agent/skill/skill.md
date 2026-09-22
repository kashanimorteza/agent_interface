# Agent Skill Definition

Agent Skill is the Agent Component that defines a Skill's portable meaning and per-Skill Contract.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Components](#components)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**




<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Purpose

Skill provides one consistent way to describe a reusable capability without repeating its framework or its Skill-specific content.

### How It Works

Each Core Skill has one Contract in `contracts/`. The Contract holds its framework: inputs, outputs, invocation rules, boundaries, and declarations specific to that Skill.

For a Core Skill, the Contract's `Source` section identifies the starting point for Understanding. The Contract and the path beginning at that Source are read together to establish the Skill's complete Meaning and Content. A Core Skill is implemented from that Understanding rather than by copying its sources verbatim.

A Provider Skill has no `Source` section because its Contract and directory already contain everything it needs. Provider content is copied as it stands from `providers/`. When a Skill is implemented again, declared changes are applied; when nothing changed, the valid existing implementation is preserved.




<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Skill** — a reusable capability activated explicitly or by a declared coordinator.
- **Skill Contract** — the per-Skill framework, including its invocation rules and, for a Core Skill, its Understanding Source.
- **Core Skill** — a Skill defined by a Contract in `contracts/`, whose Source section identifies the starting point for its Understanding.
- **Provider Skill** — a self-contained Skill held in `providers/` without a Source section.




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

Provider Skills are self-contained and held in [providers/](providers/). None are declared currently.




<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

For a Core Skill, Skill-specific behavior belongs to the sources named by its Contract. For a Provider Skill, it is complete in the Provider Contract and directory. Every Contract carries the Skill framework.

The Definition carries the shared portable Skill concept; each Contract carries one Skill's framework and any Skill-specific declarations. A Core Contract also carries its Source reference.




<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is authoritative for the shared Skill concept.
