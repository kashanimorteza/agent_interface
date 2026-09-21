# Configure Definition

Configure is the Operation Component that creates the structural Config records required by the Interface from their Schemas.

Responsibility: The creation and structural reconciliation of Config records from their Schemas.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Configure is the Operation Component that creates the Config records required by the Interface from their current Schemas. Configure has no Target, phase, product, Environment, or Agent responsibility.

### Purpose

The Interface needs its Config records to exist with known structures before operational work can use them. Configure creates that structural foundation and does nothing beyond producing Schema-derived records.

### How It Works

Configure establishes current Interface Understanding and Target Understanding, then reads the Config Schemas named by Configure Preferences and generates the corresponding records in the Config directory. When State already exists, it also reads the latest Configure operation log to reconcile its own previous outcome. It does not interpret Target phases, execute Workflow operations, install technical requirements, prepare an Environment, or create product Source. The Configure Skill is constructed from this Definition and its Preferences, so this Component is the source of the Skill's meaning and current Config mapping.

Configure is complete when every generated record conforms to its current Schema. Any later operational or phase content belongs to the Operation that owns it.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Config Schema** — the structure that defines one of the three Config files.
- **Config Record** — a generated Config file that conforms to its Config Schema.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Config Schemas** — reads the structures named by Configure Preferences from which Config Records are generated.

<br>

The Config Schemas own file shape and required structure. Configure Preferences own the current Config directory, record-to-Schema mapping, and the Human-only policy for those declarations.

Every Principle in this file is mandatory. An Operations Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Configure owns structural creation of Config records. The Config Schemas own their shapes, while later Operation Components own the operational content written into those records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is the authority for Configure's responsibility and limits. Its Principle is mandatory; Configure Preferences supply current mappings but cannot expand its scope.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Configure generates only the declared Config records from their Schemas

**Rule:** Configure reads only the Config Schemas declared by Configure Preferences and generates only their structurally valid Config Records.

**Why:** A single narrow responsibility gives the Interface a known operational structure without allowing Configure to interpret project meaning or perform another Operation.

**Boundary:** Configure never reads or changes Target, Agent, phase, product Source, Environment, technical requirements, Workflow content, or any file outside the declared Config Records.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configure generates only the declared Config records from their Schemas**

- **Must** — generate each declared Config Record from its current Schema.
- **Never** — perform another Operation or change anything outside those Config Records.
