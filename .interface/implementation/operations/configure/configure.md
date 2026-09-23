# Configure Definition

Configure is the Operation Component that creates the structural Config records required by the Interface from their Schemas.  

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

Configure creates and reconciles the three declared Config Records from their current Schemas.

### Purpose

The Interface needs its Config records to exist with known structures before operational work can use them. Configure creates that structural foundation and does nothing beyond producing Schema-derived records.

### How It Works

Configure reads the three Config Schemas named by Configure Preferences and generates or reconciles the corresponding records in the Config directory, preserving the explanatory comments defined by each Schema. When a record already exists, Configure preserves its valid operational content and changes only what is required to restore Schema conformance. Once the State Config is available, Configure records the active Workflow position as `configuring` and appends one Configure Log Entry to `state.yaml`; the common execution fields are recorded in the entry and Configure-specific details are recorded in its `data`.

Configure is complete when every generated record conforms to its current Schema. It stops when a required Schema or mapping is invalid or unavailable, or when a Config record or Log Entry cannot be written. Any later operational content belongs to the Operation that owns it.

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

### Configure generates only the declared Config records from their Schemas

**Rule:** Configure reads only the Config Schemas declared by Configure Preferences, generates only their structurally valid Config Records, preserves the Schemas' comments in the generated records, and preserves valid operational content when reconciling an existing record. Once the State Config is available, Configure records the active Workflow position as `configuring` and appends its Configure Log Entry.

**Why:** A single narrow responsibility gives the Interface a known operational structure without allowing Configure to interpret project meaning or perform another Operation.

**Boundary:** Configure changes only the three declared Config Records and the Configure Log Entry appended to State.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configure generates only the declared Config records from their Schemas**

- **Must** — generate each declared Config Record from its current Schema, preserve its comments, preserve valid operational content during reconciliation, and record `configuring` with its Configure Log Entry once State is available.
- **Never** — perform another Operation or change anything outside those Config Records and its own Configure Log Entry.
