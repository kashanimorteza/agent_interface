# Agent Context Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Layering](#layering)**
5. **[Authority](#authority)**
6. **[Principles](#principles)**
   - **[Every action begins from current Understanding](#every-action-begins-from-current-understanding)**
   - **[Context distinguishes authority from assistance](#context-distinguishes-authority-from-assistance)**
   - **[Context lifecycle preserves required instructions](#context-lifecycle-preserves-required-instructions)**
7. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Context is the Component that establishes the current information available to an Agent Instance while it performs an assigned Role. It governs persistent instructions, loaded project knowledge, memory, imports, and context preservation across runtime lifecycle events.

It owns context composition and freshness. It does not own the meaning of Target, Implementation, or Agent sources and never replaces those authorities with remembered summaries.

### Purpose

An Agent's output is a function of what it was looking at. Everything else — the Role, the Skill, the Tools — operates on whatever information happened to be loaded, which makes context the quietest way for the whole system to go wrong. Nothing errors. The Agent reasons well about a version of the project that no longer exists.

This Component exists to make the starting information deliberate. It decides what is loaded before work begins, from which authoritative sources, in what precedence, and what survives a lifecycle event that would otherwise drop it.

It also exists to keep a distinction that loading tends to erase. Persistent instructions, project knowledge, memory, and current owned records all arrive as text in the same window, and once there they look equally true. They are not. A remembered summary is assistance; a current source is authority. This Component is where that difference is preserved.

### How It Works

Before acting, a Role establishes current Interface Understanding, and current Target Understanding whenever its responsibility requires it. Which sources that means, and in what precedence, comes from the `understanding_sources` settings in Preferences rather than from habit. Memory, operational records, conversation history, and earlier summaries are never a substitute for reading the current source.

A Role loads what its bounded responsibility needs and no more. Agent Module sources are the one context nothing ordinary may include: only Agent Sync loads them, and every other Role works from the synchronized Runtime realizations.

Each loaded source keeps its origin and its authority class. Persistent instructions and Memory may guide how work is done, but they never override a Principle, an explicit project decision, or a current owned record. Ordering can change what a reader sees first; it cannot change what outranks what.

Across session start, resume, compaction, delegation, and isolation, every instruction the receiving Role requires is preserved or reloaded. If something required is missing, that is reported before dependent work continues, while supporting material that nothing currently depends on may be loaded only when it is needed.

<br>

## Terms

- **Context** — the information currently available to an Agent Role for reasoning and action.
- **Persistent Instruction** — project or organizational guidance loaded across sessions.
- **Memory** — retained supporting knowledge that may help future work but is not authoritative intent.

## Relationships

- **Consumes Target and Implementation Modules for ordinary roles** — loads current authoritative sources required by the active role; Agent Module sources are loaded only for explicit Agent Sync.
- **Consumes Agent Rule** — loads applicable persistent and scoped instructions.
- **Consumed by Agent (formerly Role), Skill, and Rule (formerly Session)** — supplies the current information they use.

Technical loading sources, memory behavior, imports, and limits belong to Agent Context Preferences.

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Layering

This Definition carries the portable meaning and mandatory Principles of the Context Component. Preferences carry current context selections, declarations, and Native realization hints. Agent Sync reads both and realizes them without changing their scope or authority.

<br>

## Authority

The Human owns this Definition and its Preferences. Every Principle in this file is mandatory; Preferences can never override a Principle, and Agent Sync is the only reader authorized to realize the Component in an Agent Native.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every action begins from current Understanding

**Rule:** An Agent Role establishes current Interface Understanding before acting and current Target Understanding whenever its responsibility requires it. It resolves the starting sources and their precedence from the Context Preferences's `understanding_sources` settings. Memory, operational records, conversation history, and prior summaries never substitute for current authoritative sources.

**Why:** Long-lived or resumed sessions otherwise act on stale assumptions.

**Boundary:** A role reads only the context necessary for its bounded responsibility. Agent Sync is the sole role context permitted to include Agent Module sources; every other role uses synchronized Runtime realizations and never enters that module.

<br>

### Context distinguishes authority from assistance

**Rule:** Every context source retains its authority class and origin. Persistent instructions and Memory may guide execution but never override Principles, explicit project decisions, or current owned records.

**Why:** Loading information together must not flatten its precedence.

**Boundary:** Context ordering may affect presentation but not declared authority.

<br>

### Context lifecycle preserves required instructions

**Rule:** Session start, resume, compaction, delegation, and isolation preserve or reload every instruction required by the receiving role. Missing required context is reported before dependent work proceeds.

**Why:** A lifecycle transition must not silently weaken the execution contract.

**Boundary:** Supporting material may be loaded lazily when no current action depends on it.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every action begins from current Understanding**

- **Must** — establish current Interface and role-required Target Understanding before acting
- **Must** — load Agent Module sources only for explicit Agent Sync and use synchronized Runtime artifacts for every other role
- **Never** — substitute memory or prior summaries for current authorities

**Context distinguishes authority from assistance**

- **Must** — retain each context source's origin and authority
- **Never** — let instructions or Memory override owned sources

**Context lifecycle preserves required instructions**

- **Must** — preserve or reload required context across lifecycle transitions
