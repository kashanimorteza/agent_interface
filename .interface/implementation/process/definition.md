# Process Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Principles](#principles)**
   - **[Process governs implementation work without becoming product implementation](#process-governs-implementation-work-without-becoming-product-implementation)**
   - **[Each operational concern has one owning Component](#each-operational-concern-has-one-owning-component)**
   - **[Operational records remain separate from their authorities](#operational-records-remain-separate-from-their-authorities)**
6. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Process is the part of Implementation that defines how work on a Target is configured, planned, reviewed, and recorded. It contains Configuration, Plan, Review, and State while remaining separate from the Development part that defines the product being built.

### Purpose

Building a product requires more than product architecture. The work also needs a stable way to prepare operational records, divide a phase into verifiable activities, judge the generated result, and preserve progress across runs. Process gives each of those concerns one owner and one reusable philosophy.

### How It Works

Configuration prepares and reconciles the operational records. Plan turns a selected Target phase into bounded work. Review compares the result of that phase with its applicable authorities and records Findings. State preserves the aggregate operational position and outcomes needed to continue the workflow.

<br>

## Terms

- **Process Component** — one Component that owns a distinct part of configuring, planning, reviewing, or recording implementation work.
- **Operational Record** — mutable information produced while the Interface workflow runs, separate from the authorities that define what the work means.

## Architecture

```text
Process
├── Configuration
├── Plan
├── Review
└── State
```

Configuration owns preparation and structural reconciliation of Config. Plan owns the decomposition of phase work. Review owns assurance outcomes and Findings. State owns aggregate workflow position, progress, history, blockers, and open questions.

## Relationships

- **Consumes Target** — uses current phase identity and intent without becoming another Target definition.
- **Consumes Development** — applies the product architecture and Component authorities relevant to the work being performed.
- **Consumed by Workflow** — provides the operational concepts and records through which implementation work proceeds and resumes.

<br>

Technical choices and defaults shared by Process belong to Process Preferences. Choices owned by Configuration, Plan, Review, or State remain in that Component's Preferences. Operational record shapes belong to their Schemas.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Process governs implementation work without becoming product implementation

**Rule:** Process defines how Target implementation work is configured, planned, reviewed, and recorded. It never owns or implements the product behaviour, source, or public interfaces governed by Development.

**Why:** Separating the way work is controlled from the product being built prevents operational records and workflow mechanics from becoming product architecture.

**Boundary:** Process may inspect Development results where its Components require them, but inspection never transfers ownership of those results.

<br>

### Each operational concern has one owning Component

**Rule:** Configuration owns Config preparation and reconciliation, Plan owns planned activities, Review owns assurance and Findings, and State owns aggregate operational position and history. No Process Component writes another's owned content unless the Interface explicitly grants that write under the owning Component's rules.

**Why:** One owner for each operational concern keeps progress, evidence, and authority consistent across separate runs.

**Boundary:** A Skill may perform work for a Process Component, but the Skill does not become the owner of the record it writes.

<br>

### Operational records remain separate from their authorities

**Rule:** An Operational Record records what happened, what exists, or where work stands. It never redefines Target intent, Development meaning, a Principle, a Preference, or a Schema.

**Why:** A mutable execution record cannot safely serve as the source of the requirements it is meant to track.

**Boundary:** Referencing an authority or recording the result of applying it does not copy ownership of that authority into Process.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Process governs implementation work without becoming product implementation**

- **Must** — Process governs configuration, planning, review, and operational recording.
- **Never** — Process owns or implements Development product behaviour, source, or public interfaces.

**Each operational concern has one owning Component**

- **Must** — Configuration, Plan, Review, and State each retain their declared ownership.
- **Never** — a Process Component writes another's owned content without explicit Interface authority under that owner's rules.

**Operational records remain separate from their authorities**

- **Must** — Operational Records state execution facts and progress.
- **Never** — an Operational Record redefines Target, Development, Principles, Preferences, or Schemas.
