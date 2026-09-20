# Implementation Definition





<br><br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Implementation has Development and Process Subsystems](#implementation-has-development-and-process-subsystems)**
   - **[Each subject is defined by one Definition and one Preferences file](#each-subject-is-defined-by-one-definition-and-one-preferences-file)**
   - **[Development and Process retain separate ownership](#development-and-process-retain-separate-ownership)**
5. **[At a Glance](#at-a-glance)**





<br><br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Implementation defines the reusable philosophy and standards used to build a Target and to control the work that builds it. It is independent of any particular Target or Agent.

The Module map and the relationship between its Subsystems are described in the [Implementation Guide](guide.md).

### Purpose

Building a product requires both a coherent product architecture and a reliable way to control the work that creates it. Keeping these concerns in one Implementation Module makes the programming perspective reusable while keeping product responsibilities distinct from planning, review, configuration, and operational records.

### How It Works

Each subject in Implementation is described by a Definition and a Preferences file. The Definition is authoritative for meaning and Principles; Preferences record choices and realization conventions. Skills perform operations under the authority of the relevant subject.





<br><br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Implementation** — the reusable module that defines how a Target is built and how its implementation work is controlled.
- **Development** — the Implementation Subsystem that defines the product Components, their composition, and their technical realization.
- **Process** — the Implementation Subsystem that defines configuration, planning, review, and operational recording.
- **Definition** — the authoritative description of a subject's Understanding, relationships, boundaries, and mandatory Principles.
- **Preference** — a human-owned choice or default used where a higher authority is silent; it never overrides a Principle.
- **Subject** — any Implementation Module, Subsystem, or Component described by a Definition and Preferences file.




<br><br>
<!--------------------------------------------------------------------------------- Relationships --->

## Relationships

- **Consumes Target** — applies the current Target intent and phase requirements without becoming another Target definition.
- **Consumed by operational Skills** — supplies the Development and Process authorities used while configuring, planning, developing, reviewing, launching, and recording work.
- **Contains Development and Process Subsystems** — defines the product and operational ownership boundaries that the rest of the Interface uses.

<br>

Technical choices and defaults belong to the Preferences file of the subject that owns them. Shared choices that genuinely span Development and Process belong to Implementation Preferences. The shape of any generated operational record belongs to its Schema.

Every Principle in this file is mandatory. An Implementation Preference or Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.





<br><br>
<!--------------------------------------------------------------------------------- Principles --->

## Principles

Every Principle below is mandatory.

<br>

### Implementation has Development and Process Subsystems

**Rule:** Implementation consists of two top-level Subsystems: Development, which governs the product being built, and Process, which governs the work that configures, plans, reviews, and records that build. Neither Subsystem replaces the other.

**Why:** Product architecture and work control require different ownership while still needing one reusable Implementation perspective with explicit Subsystems.

**Boundary:** Development does not own Process records, and Process does not own product Behaviour, Source, or public interfaces.

<br>

### Each subject is defined by one Definition and one Preferences file

**Rule:** Every Implementation subject has one `definition.md` and one `preferences.yaml`. The Definition carries its Understanding and mandatory Principles; Preferences carry its choices, defaults, and realization conventions.

**Why:** A stable pair separates what the subject is and must preserve from how it is preferably realized.

**Boundary:** A subject's Preferences never override its Definition, and a child subject does not duplicate the authority of its parent or sibling.

<br>

### Development and Process retain separate ownership

**Rule:** Components within Development own product responsibilities, and Components within Process own Configuration, Plan, Review, and State responsibilities. A Skill performs an operation under these owners but does not acquire ownership by writing an authorized record.

**Why:** Explicit ownership keeps product meaning, operational progress, evidence, and workflow records from becoming interchangeable.

**Boundary:** A Component within Process may inspect Development results when its responsibility requires it, but it never changes a Development-owned result directly.





<br><br>
<!--------------------------------------------------------------------------------- At a Glance --->

## At a Glance

Every obligation in the file, under the Principle it comes from.


**Implementation has Development and Process Subsystems**

- **Must** — keep product construction in Development and implementation control in Process.
- **Never** — let either Component replace the responsibility of the other.

**Each subject is defined by one Definition and one Preferences file**

- **Must** — keep each subject's Understanding and mandatory Principles in Definition and its choices in Preferences.
- **Never** — let Preferences override Definition or duplicate another subject's authority.

**Development and Process retain separate ownership**

- **Must** — keep product responsibilities in Development and Configuration, Plan, Review, and State responsibilities in Process.
- **Never** — let a Skill acquire ownership merely by performing an operation or writing an authorized record.
