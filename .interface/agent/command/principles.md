# Agent Command Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[1. A Command is an entry point, not a second workflow](#1-a-command-is-an-entry-point-not-a-second-workflow)**
   - **[2. Command invocation is stable and discoverable](#2-command-invocation-is-stable-and-discoverable)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Command is the Component that defines named entry points through which a Human or Agent requests a built-in action or activates a Capability. It provides a stable invocation surface even when a runtime implements commands through Skills or another native mechanism.

It owns command names, arguments, routing, and discoverability. It does not own the workflow or capability invoked by a command.

### Purpose

A capability that exists is not yet reachable. A Skill can be written, a Tool connected, a Role declared, and still nobody — Human or Agent — has a way to say *do that now*. Commands are that way of saying it: named entry points with declared arguments, stable enough that a Human can learn them and an Agent can route them without guessing.

This Component exists so those entry points stay entry points. The moment a Command starts deciding things — validating beyond its arguments, applying its own policy, carrying its own version of a workflow — there are two implementations of the same behavior, and the one invoked through the Command drifts away from the one invoked any other way.

So the Component owns names, arguments, routing, and discoverability, and owns nothing that happens after the routing. What the Command reaches is owned by whoever owns that capability.

### How It Works

A Command is declared with its name, its aliases, the arguments it accepts, the Capability Contract it belongs to, and the scope in which it can be invoked. Declaring it is what makes it discoverable: a Human can list what is available, and an Agent can resolve an invocation without inferring.

An invocation arrives, its arguments are validated against the declared contract, and it is routed to the one owning Capability — a Skill, an Agent, a Tool, or the Runtime itself. The Command performs no work of its own between those two steps.

Built-in Commands come from the Agent Runtime and carry the Runtime's own contract; Custom Commands are declared by the project, the Human, or an Extension, and each maps to exactly one owning Capability. Both are declared the same way, so both are discoverable the same way.

When a name collides, or the target of a Command is unavailable, the Command reports it. It does not pick a winner, and it does not fall back to something that looked close. Portable names and argument forms are declared in Preferences; how a given Agent Native actually exposes them is resolved by Agent Sync.

<br>

## Terms

- **Command** — a named invocation entry point with a defined argument contract.
- **Built-in Command** — an entry point supplied and implemented by the Agent Runtime.
- **Custom Command** — a project, user, or extension entry point mapped to a declared capability.

## Relationships

- **Consumes Agent Skill, Agent (formerly Role), Tool, and Runtime** — routes an invocation to its implementing capability.
- **Consumed by Agent Rule (formerly Interaction)** — provides discoverable Human-facing actions.

Portable command names, aliases, and argument forms belong to Agent Command Preferences; Native mappings are resolved by Agent Sync from the selected Agent Native.

Every statement here is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory, and its number is permanent.

<br>

### 1. A Command is an entry point, not a second workflow

**Rule:** Every Custom Command maps to one owning Capability Contract and adds no competing workflow, authority, or policy. Its arguments are validated before routing.

**Why:** Duplicated behavior drifts when one copy changes.

**Boundary:** A Built-in Command may execute fixed runtime logic whose contract is supplied by the runtime.

<br>

### 2. Command invocation is stable and discoverable

**Rule:** Command names, aliases, accepted arguments, owner, availability, and invocation scope are explicit. A collision or unavailable target is reported rather than resolved by guesswork.

**Why:** Entry points are interfaces and must behave predictably.

**Boundary:** A runtime may present commands differently while preserving the declared invocation contract.

<br>

## At a Glance

- **Must** — map every Custom Command to one owning Capability Contract *(1)*
- **Never** — duplicate workflow, authority, or policy inside a Command *(1)*
- **Must** — declare command names, arguments, ownership, scope, and availability *(2)*
- **Never** — guess through a collision or unavailable command target *(2)*
