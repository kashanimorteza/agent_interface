# Agent Personality Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Every Personality is one bounded stance](#every-personality-is-one-bounded-stance)**
   - **[Model Preference is a Preferences file choice](#model-preference-is-a-preferences-file-choice)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Personality is the Component that defines the personalities an Agent can take on while it works: who the Agent is during a kind of work, the stance and judgment it applies, and the kinds of work it performs in that stance. It is independent of any Agent Native, model, or provider.

It owns personality identity, stance, and the actions each personality performs. It does not own Role responsibility contracts, Skill workflows, Runtime identity, or Permission policy.

### Purpose

The same Agent doing different kinds of work should not behave the same way. Planning wants breadth and doubt; reviewing wants suspicion and evidence; implementing wants focus and completion. An Agent with one undifferentiated manner does all three the same way, which means it does at least two of them badly.

Personality exists to make that stance explicit rather than accidental. It declares who the Agent is during a kind of work — how it judges, what it refuses to do, what it prefers — so the difference between planning and reviewing is a declared thing the Human controls, not a side effect of how a prompt happened to be phrased.

It is also where model preference belongs. A stance and the model best suited to it travel together; keeping the preference with the Personality means changing the stance changes the model with it, instead of the two drifting apart in separate files.

### How It Works

A Personality is declared as one bounded stance with its own definition file: who it is during that kind of work, what it does, how it judges, what it never does, and which models it prefers in priority order.

The definitions live beside the Component rather than inside it, one file per Personality, so a stance is written as prose the Agent reads rather than compressed into keys. Agent Sync places that content into whatever the selected Native offers for it.

Model preference is a Preferences choice, not a Principle: the stance is portable, the models that realize it are current selections. The names it lists are the model names Runtime declares, first as primary and the rest as fallbacks.

Nothing about a Personality expands what an Agent may do. It shapes how work is approached inside the Role, the Skills, the Tools, and the Permissions that already apply.

<br>

## Terms

- **Personality** — one named way of working: a stance, a set of priorities, and the judgment applied while performing its actions.
- **Action** — one kind of work a Personality performs, such as developing, planning, analyzing, or reviewing.
- **Model Preference** — the ordered list of models a Personality prefers to run on, from highest to lowest priority.

## Relationships

- **Consumes Agent (formerly Role), Context, Skill, Tool, and Permission** — a Personality acts within their contracts.
- **Consumed by Agent (including former Coordination)** — supplies the stance an Agent Instance takes and the way delegated work is performed.

Personality definitions, their Actions, and Model Preferences belong to Agent Personality Preferences and its definition files; Native realization is resolved by Agent Sync from the selected Agent Native.

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every Personality is one bounded stance

**Rule:** Every Personality declares one identity, the stance and priorities it applies, and the Actions it performs. A Personality never performs an Action it does not declare.

**Why:** A named way of working is predictable only when what it does is stated.

**Boundary:** Declaring an Action never grants authority beyond the active Role, Permission, and request.

<br>

### Model Preference is a Preferences file choice

**Rule:** Which models a Personality runs on, and in what order, is declared in its Preferences as an ordered list of model names that the Agent Runtime Preferences declare, never in its Principles or definition prose.

**Why:** Model and provider names are runtime-specific and change independently of the Personality's meaning.

**Boundary:** A Native that cannot honor a declared preference reports it; it never silently substitutes.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Personality is one bounded stance**

- **Must** — give every Personality one identity, stance, and declared set of Actions
- **Never** — let a Personality perform an undeclared Action or gain authority from one

**Model Preference is a Preferences file choice**

- **Must** — declare Model Preference in the Preferences, in priority order
- **Never** — place model or provider names in Principles or definition prose
