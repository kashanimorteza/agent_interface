# Agent Personality Principles

Agent Personality is the Component that defines the personalities an Agent can take on while it works: who the Agent is during a kind of work, the stance and judgment it applies, and the kinds of work it performs in that stance. It is independent of any Agent Native, model, or provider.

It owns personality identity, stance, and the actions each personality performs. It does not own Role responsibility contracts, Skill workflows, Runtime identity, or Permission policy.

## Terms

- **Personality** — one named way of working: a stance, a set of priorities, and the judgment applied while performing its actions.
- **Action** — one kind of work a Personality performs, such as developing, planning, analyzing, or reviewing.
- **Model Preference** — the ordered list of models a Personality prefers to run on, from highest to lowest priority.

## Relationships

- **Consumes Agent Role, Context, Skill, Tool, and Permission** — a Personality acts within their contracts.
- **Consumed by Agent and Coordination** — supplies the stance an Agent Instance takes and the way delegated work is performed.

Personality definitions, their Actions, and Model Preferences belong to Agent Personality Preferences and its definition files; Native realization is resolved by Agent Sync from the selected Agent Native.

Every statement here is mandatory. Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Personality is one bounded stance

**Rule:** Every Personality declares one identity, the stance and priorities it applies, and the Actions it performs. A Personality never performs an Action it does not declare.

**Why:** A named way of working is predictable only when what it does is stated.

**Boundary:** Declaring an Action never grants authority beyond the active Role, Permission, and request.

<br>

## 2. Model Preference is a Preferences file choice

**Rule:** Which models a Personality runs on, and in what order, is declared in its Preferences as an ordered list of model names that the Agent Runtime Preferences declare, never in its Principles or definition prose.

**Why:** Model and provider names are runtime-specific and change independently of the Personality's meaning.

**Boundary:** A Native that cannot honor a declared preference reports it; it never silently substitutes.

<br>

## At a Glance

- **Must** — give every Personality one identity, stance, and declared set of Actions *(1)*
- **Never** — let a Personality perform an undeclared Action or gain authority from one *(1)*
- **Must** — declare Model Preference in the Preferences, in priority order *(2)*
- **Never** — place model or provider names in Principles or definition prose *(2)*
