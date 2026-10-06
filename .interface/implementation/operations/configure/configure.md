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

Configure also reconciles an existing record with its current Schema.

### Purpose

The Interface needs its Config records to exist with known structures before operational work can use them. Configure creates that structural foundation and does nothing beyond producing Schema-derived records.

### How It Works

Configure reads each declared Config Schema and writes or reconciles its record in the Config directory.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Config Schema** — the structure that defines one of the two Config files.
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

**Rule:** Configure reads only the Config Schemas declared by Configure Preferences, generates only their structurally valid Config Records, preserves the Schemas' comments in the generated records, and preserves valid operational content when reconciling an existing record. It composes each specialized Schema with the general YAML file structure, so a generated record conforms to both and a specialized Schema never copies the general structure. Configure is complete when every generated record conforms to its current Schema; it stops when a required Schema or mapping is invalid or unavailable, or when a Config record cannot be written. Later operational content in a record belongs to the Operation that owns it.

**Why:** A single narrow responsibility gives the Interface a known operational structure without allowing Configure to interpret project meaning.

**Boundary:** Configure changes only the two declared Config Records.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configure generates only the declared Config records from their Schemas**

- **Must** — generate each declared Config Record from its current Schema and preserve its comments and valid operational content during reconciliation.
- **Never** — change anything outside those Config Records.
