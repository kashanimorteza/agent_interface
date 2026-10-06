# Agent Output Style Definition

Agent Output Style is the Executor Component that declares how the Agent's output is presented.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Layering](#layering)**
4. **[Authority](#authority)**
5. **[Principles](#principles)**
6. **[Review](#review)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Agent Output Style is the Executor Component that declares how the Agent's output is presented, and the only Component that does.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Output Style** — a presentation contract controlling organization, tone, and response format.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

This Definition carries the portable meaning and mandatory Principles of the Output Style Component. Preferences carry the current Output Style selection and its declarations. Agent Native Implement reads both and realizes them without changing their scope or authority.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns this Definition and its Preferences. Every Principle in this file is mandatory; Preferences can never override a Principle, and Agent Native Implement is the only reader authorized to realize the Component in an Agent Native.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Output presentation is declared only here

**Rule:** How output is presented is declared only in this Component. No other Component, Rule, or Skill Contract declares response style or format.

**Why:** One owner keeps presentation from conflicting across sources.

**Boundary:** Another Component may require what must be reported, never how it is presented.

<br>

### Presentation preserves technical substance

**Rule:** Output Style may change organization, tone, detail, and format while preserving exact technical meaning, identifiers, commands, paths, code, evidence, warnings, uncertainty, and required decisions.

**Why:** Communication may adapt to a Human without changing the work communicated.

**Boundary:** A style may shorten expression only when no required substance is lost.

<br>

<!--------------------------------------------------------------------------------- Review --->
## Review

### Conformance

- Every Principle above is realized in the Agent Native.

### Checks

- The selected Output Style is present and active.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Output presentation is declared only here**

- **Never** — declare response style or format outside this Component

**Presentation preserves technical substance**

- **Must** — preserve exact technical substance under every Output Style
- **Never** — let presentation hide evidence, warnings, uncertainty, or decisions
