# Configure Definition

Configure is the Operation Component that creates the four structural Config records required by the Interface.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Layering](#layering)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Configure is the Operation Component that creates the four Config files required by the Interface:

- `application.yaml`
- `plan.yaml`
- `state.yaml`
- `review.yaml`

It reads their Schemas and generates one structurally valid Config file for each. Configure has no Target, phase, product, Environment, or Agent responsibility.

### Purpose

The Interface needs these four files to exist with known structures before its operational work can use them. Configure creates that structural foundation and does nothing beyond producing those four Schema-derived files.

### How It Works

Configure reads the four Config Schemas and generates the corresponding files in Config. It does not read Target or Agent content, interpret phases, execute Workflow operations, install technical requirements, prepare an Environment, or create product Source.

Configure is complete when the four generated files conform to their current Schemas. Any later Plan, State, Review, Application Manifest, or phase content belongs to the operation that owns it.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Config Schema** — the structure that defines one of the four Config files.
- **Config Record** — a generated Config file that conforms to its Config Schema.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Configure
├── application.yaml
├── plan.yaml
├── state.yaml
└── review.yaml
```

Configure has no internal operational Components. Its only responsibility is to generate these four Config Records from their corresponding Schemas.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Config Schemas** — reads the four structures from which the Config Records are generated.

<br>

The four Config Schemas own file shape and required structure. Configure Preferences are empty because Configure has no independent choices or Defaults.

Every Principle in this file is mandatory. An Operations Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

Configure owns structural creation of Config records. The Config Schemas own their shapes, while later Operation Components own the operational content written into those records.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

This Definition is the authority for Configure's responsibility and limits. Its Principle is mandatory; Configure Preferences are empty and cannot expand its scope.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Configure generates only the four Config files from their Schemas

**Rule:** Configure reads the four Config Schemas and generates only `application.yaml`, `plan.yaml`, `state.yaml`, and `review.yaml` as structurally valid Config Records.

**Why:** A single narrow responsibility gives the Interface a known operational structure without allowing Configure to interpret project meaning or perform another Operation.

**Boundary:** Configure never reads or changes Target, Agent, phase, product Source, Environment, technical requirements, Workflow content, or any file outside these four Config Records.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configure generates only the four Config files from their Schemas**

- **Must** — generate the four Config Records from their current Schemas.
- **Never** — perform another operation or change anything outside those four Config Records.
