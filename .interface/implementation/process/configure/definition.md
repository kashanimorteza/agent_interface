# Configure Definition

<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
   - **[Understanding Input](#understanding-input)**
   - **[Schema-driven Config](#schema-driven-config)**
   - **[Reconciliation](#reconciliation)**
   - **[Application Manifest](#application-manifest)**
   - **[Verification](#verification)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Principles](#principles)**
   - **[Configure establishes only the Understanding it needs](#configure-establishes-only-the-understanding-it-needs)**
   - **[Every operational Config record follows its current Schema](#every-operational-config-record-follows-its-current-schema)**
   - **[Reconciliation preserves meaningful owned records](#reconciliation-preserves-meaningful-owned-records)**
   - **[Config reflects authorities and never replaces them](#config-reflects-authorities-and-never-replaces-them)**
   - **[The Application Manifest contains published public metadata only](#the-application-manifest-contains-published-public-metadata-only)**
7. **[At a Glance](#at-a-glance)**

<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Configure is the Process Component that prepares the four operational Config records on which the Interface Workflow depends:

- `plan.yaml`
- `state.yaml`
- `review.yaml`
- `application.yaml`

It establishes Interface Understanding and only the minimal Target Understanding needed for configuration. It generates or reconciles every Config record from its current Schema, preserves meaningful existing records, and reports truthful outcomes.

Configure owns no planning, product implementation, review, launch, reset, technical-requirement installation, Environment preparation, or Target interpretation beyond the limited facts required for Config. Each other operation prepares what its own work needs: Develop installs the technical requirements of its phase, and Launch prepares the Environment of the selected Launch Item.

### Purpose

The Workflow cannot plan, develop, review, or record its position reliably until its operational records have known and current shapes. Configure creates that common starting point and keeps it structurally compatible with the current Schemas without taking ownership of the content that Plan, Review, or State governs.

The four Config files, including `application.yaml`, follow the same schema-driven generation process. None is a temporary or optional side file. When a declared Component does not yet exist, Configure leaves its Manifest section at its Schema default and reports that the Component has not yet been generated; it never creates the Component to obtain its metadata.

### How It Works

Configure accepts no phase selection. It reads the current operational Schemas, existing Config, stable Target phase identifiers, and public metadata already published by existing Development Components.

Configure activates when operational Config must be created, validated, repaired, or refreshed, and once at the start of end-to-end implementation orchestration.

It then generates or reconciles all four Config records from their current Schemas, adds missing phase records at their current initial values, preserves progress and meaningful owned content, and reports any conflict that cannot be resolved safely. It records the active Configure position and appends the outcome under State ownership.

Repeating Configure against unchanged Schemas, Target identity, and Config produces no structural mutation while still recording invocation outcomes as State permits.

Its output is the four Schema-valid Config records, truthful State position and History, and a report of created, reconciled, preserved, conflicted, and blocked results. If reconciliation would lose meaningful records or a Schema cannot be applied safely, Configure stops or preserves the affected item; independently valid items may continue. Its native adapter exposes one project-scoped Configure capability and reports Config, phase synchronization, preserved records, and blockers.

<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Config Record** — one of the four operational YAML records generated and reconciled by Configure.
- **Configuration Reconciliation** — bringing existing Config structure into agreement with current Schemas while preserving meaningful content owned by another Component.
- **Application Manifest** — the operational projection of current non-secret public metadata that Development Components publish for composition and consumption.
- **Stable Target Phase Identifier** — the phase identity Configure may use without copying the phase's meaning into Config.
- **Meaningful Owned Record** — operational content whose loss or reinterpretation would remove information owned by Plan, Review, or State.

<br><br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Configure
├── Understanding
├── Schema-driven Config
├── Reconciliation
├── Application Manifest
└── Verification
```

### Understanding Input

Configure first establishes Interface Understanding and only the Target Understanding needed to identify stable phases for Config generation. It then reads the current Config Schemas.

### Schema-driven Config

Configure creates or reconciles `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` from their current Schemas rather than from a remembered structure.

### Reconciliation

Configure preserves meaningful records, reconciles compatible structural changes, adds missing phase records at initial values, and leaves a record unchanged when a structural change would lose information.

### Application Manifest

Configure records only public, non-secret metadata already published by Development Components. A declared Component receives a Manifest section even before it publishes metadata, and that section remains at its Schema default until publication exists.

### Verification

Configure validates every Config record against its applicable Schema and verifies phase-identity reconciliation. It reports created, reconciled, preserved, conflicted, and blocked results truthfully.

<br><br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes Interface** — establishes the Interface Understanding that governs Config.
- **Consumes Target** — uses only the stable phase identities required for configuration.
- **Consumes Config Schemas** — derives the structure and initial values of all four Config records.
- **Consumes Development** — records public Component metadata already published by Development.
- **Consumed by Plan, Develop, Review, Launch, Reset, and State** — provides structurally valid operational records and a truthful Configure outcome.

<br>

Technical choices and defaults belong to Configure Preferences. The exact shapes and initial values of generated Config records belong to their Schemas. Configure never writes resolved choices back into Preferences.

Every Principle in this file is mandatory. A Process Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br><br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Planning** — belongs to Plan; Configure prepares `plan.yaml` but never creates or owns its Plan content.
- **Implementation** — belongs to Develop; Configure never creates, scaffolds, or populates a Component root, package, Source file, test, or lockfile.
- **Review** — belongs to Review; Configure does not judge implementation or Plan conformance.
- **Launch** — belongs to Launch; Configure never prepares an Environment or activates a runtime.
- **Technical requirements** — belong to Develop; Configure never installs dependencies or provisions tools.
- **Agent capabilities** — belong to the Agent Native Skill's install mode; Configure never provisions, transfers, or installs a Skill, plugin, or capability.
- **Target meaning** — belongs to Target; Configure never copies Target meaning into Config.

<br><br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Configure establishes only the Understanding it needs

**Rule:** Configure establishes complete Interface Understanding and only the minimal Target Understanding required for Config generation: stable phase identities and no more.

**Why:** Configuration needs enough authority to create truthful records without interpreting or redefining the Target.

**Boundary:** Configure never uses phase selection, Target meaning, or unrelated Understanding to perform planning, implementation, review, launch, reset, or Environment work.

<br>

### Every operational Config record follows its current Schema

**Rule:** Configure generates or reconciles all four Config records from their current Schemas rather than from remembered structure. It validates every resulting record against its applicable Schema.

**Why:** Schema-derived records remain structurally correct when their format evolves.

**Boundary:** Configure applies Schemas; it never changes a Schema or invents project meaning to populate one.

<br>

### Reconciliation preserves meaningful owned records

**Rule:** Configure preserves meaningful existing content owned by Plan, Review, or State. When a structural change cannot be applied without losing or reinterpreting that content, Configure preserves it and reports the conflict.

**Why:** Preparing Config must not erase operational history or progress needed to understand or continue the Workflow.

**Boundary:** Configure may add or reconcile initialization defaults where no meaningful owned content would be lost. A stale phase record is removed only while it contains initialization defaults; otherwise it is preserved and reported.

<br>

### Config reflects authorities and never replaces them

**Rule:** Config records operational facts, progress, projections, and outcomes. It never becomes a second Target, Definition, Preference, Principle, or Schema.

**Why:** Mutable execution records cannot safely define the authorities against which they are produced.

**Boundary:** Config may identify or reference an authority without copying that authority's ownership or meaning.

<br>

### The Application Manifest contains published public metadata only

**Rule:** Configure records only current non-secret public metadata already published by a Development Component. It never creates a Component to obtain metadata.

**Why:** Components need one shared discovery surface without exposing private implementation or allowing Configure to invent composition facts.

**Boundary:** The Application Manifest contains no credentials, private implementation details, undeclared dependencies, or inferred metadata, and it never replaces Development as the authority for Component identity and composition.

<br><br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configure establishes only the Understanding it needs**

- **Must** — establish Interface Understanding and only the minimal Target Understanding needed for Config.
- **Never** — use configuration as a reason to interpret Target meaning or perform another Process responsibility.

**Every operational Config record follows its current Schema**

- **Must** — write, generate, reconcile, and validate `plan.yaml`, `state.yaml`, `review.yaml`, and `application.yaml` as the four Config records owned by Configure.
- **Never** — use remembered structure, change a Schema, or invent project meaning.

**Reconciliation preserves meaningful owned records**

- **Must** — preserve meaningful Plan-, Review-, and State-owned content and report unsafe conflicts.
- **Never** — discard or reinterpret meaningful records to force structural reconciliation.

**Config reflects authorities and never replaces them**

- **Must** — record operational facts, progress, projections, and outcomes.
- **Never** — let Config become another Target, Definition, Preference, Principle, or Schema.

**The Application Manifest contains published public metadata only**

- **Must** — record only current non-secret metadata already published by Development Components.
- **Never** — expose secrets, private details, undeclared dependencies, inferred metadata, or replace Development ownership.
