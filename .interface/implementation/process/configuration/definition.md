# Configuration Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Configuration derives operational structure from current Schemas](#configuration-derives-operational-structure-from-current-schemas)**
   - **[Configuration reconciliation preserves owned records](#configuration-reconciliation-preserves-owned-records)**
   - **[Config reflects authorities and never replaces them](#config-reflects-authorities-and-never-replaces-them)**
   - **[The Application Manifest contains published public metadata only](#the-application-manifest-contains-published-public-metadata-only)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Configuration is the Process Component that prepares and structurally reconciles the operational Config records required by the Interface. It also maintains the Application Manifest as the shared projection of public Component metadata.

### Purpose

Operational work needs records with known shapes before planning, development, and review can reliably use them. Configuration creates that common starting point and keeps it compatible with current Schemas without taking ownership of the content that Plan, Review, or State governs.

### How It Works

Configuration reads current operational Schemas, existing Config, stable Target phase identities, and public metadata already published by Development Components. It creates missing structure, reconciles compatible changes, preserves meaningful owned records, and reports conflicts that cannot be resolved without losing information.

<br>

## Terms

- **Configuration Reconciliation** — bringing existing Config structure into agreement with current Schemas while preserving meaningful content owned by another Component.
- **Application Manifest** — the operational projection of public metadata that Development Components publish for composition and consumption.

## Relationships

- **Consumes Schemas** — derives Config structure and initial values from current operational formats.
- **Consumes Target** — uses stable phase identities without copying phase meaning.
- **Consumes Development** — records public Component metadata that Development already publishes.
- **Consumed by Plan, Review, and State** — provides structurally valid operational records while preserving their ownership of content.

<br>

Technical choices and defaults belong to Configuration Preferences. The exact shapes and initial values of generated Config records belong to their Schemas.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Configuration derives operational structure from current Schemas

**Rule:** Configuration creates and reconciles every operational Config record from its current Schema rather than from a remembered structure.

**Why:** Schema-derived records remain consistent when their stored format evolves.

**Boundary:** Configuration applies a Schema; it never changes the Schema or invents project meaning to populate it.

<br>

### Configuration reconciliation preserves owned records

**Rule:** Reconciliation preserves meaningful existing content owned by Plan, Review, or State. When a structural change cannot be applied without losing or reinterpreting that content, Configuration preserves it and reports the conflict.

**Why:** Preparing Config must not erase the operational history needed to understand or continue the work.

**Boundary:** Initialization defaults may be added or reconciled where no meaningful owned content would be lost.

<br>

### Config reflects authorities and never replaces them

**Rule:** Config records operational facts, progress, and projections. It never becomes a second Target, Definition, Preference, or Schema.

**Why:** Mutable workflow data cannot safely define the authorities against which it is produced.

**Boundary:** Config may identify or reference an authority without copying that authority's ownership or meaning.

<br>

### The Application Manifest contains published public metadata only

**Rule:** Configuration records only current non-secret public metadata already published by a Development Component. A declared Component receives a Manifest section even before it publishes metadata, and its empty section remains empty until that metadata exists.

**Why:** Components need one shared discovery surface without exposing private implementation or allowing Configuration to invent composition facts.

**Boundary:** The Application Manifest contains no credentials, private implementation details, undeclared dependencies, or inferred metadata, and it never replaces Development as the authority for Component identity and composition.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Configuration derives operational structure from current Schemas**

- **Must** — create and reconcile each operational Config record from its current Schema.
- **Never** — change a Schema or invent project meaning while applying it.

**Configuration reconciliation preserves owned records**

- **Must** — preserve meaningful Plan-, Review-, and State-owned content and report incompatible reconciliation.
- **Never** — discard or reinterpret meaningful owned records to force a structural update.

**Config reflects authorities and never replaces them**

- **Must** — Config records operational facts, progress, and projections.
- **Never** — Config becomes another Target, Definition, Preference, or Schema.

**The Application Manifest contains published public metadata only**

- **Must** — record only current non-secret public metadata already published by a Development Component.
- **Never** — expose secrets or private details, infer metadata, or replace Development ownership.
