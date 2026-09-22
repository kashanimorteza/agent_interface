# Agent Skill Definition

Agent Skill is the Agent Component that defines a Skill's portable meaning and per-Skill Contract.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Layering](#layering)**
4. **[Authority](#authority)**




<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Skill is a reusable capability an Agent can activate to perform a defined kind of work.

### Purpose

Skill provides one consistent way to describe a reusable capability without repeating its framework or its Skill-specific content.

### How It Works

Each Skill has one Contract. The Contract holds its framework: inputs, outputs, invocation rules, boundaries, and declarations specific to that Skill.

For a Core Skill, the Contract's `Source` section identifies the starting point for Understanding. The Contract and the path beginning at that Source are read together to establish the Skill's complete Meaning and Content. A Core Skill is implemented from that Understanding rather than by copying its sources verbatim.

A Provider Skill has no `Source` section because its Contract and directory already contain everything it needs. Provider content is copied as it stands from `providers/`. When a Skill is implemented again, declared changes are applied; when nothing changed, the valid existing implementation is preserved.




<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Skill** — a reusable capability activated explicitly or by a declared coordinator.
- **Skill Contract** — the per-Skill framework, including its invocation rules and Understanding sources.
- **Provider Skill** — a self-contained Skill held in `providers/` without a Source section.




<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Skill-specific behavior belongs to the sources named by the Skill Contract. The Contract carries the Skill framework and mappings.

The Definition carries the shared portable Skill concept; each Contract carries one Skill's framework, source references, and any Skill-specific declarations.




<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is authoritative for the shared Skill concept. A Contract provides the framework and declarations of one Skill; the Source path identified by a Core Skill's Contract provides its Meaning and Content.



