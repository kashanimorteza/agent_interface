# Agent Tool Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Every Tool has an atomic contract](#every-tool-has-an-atomic-contract)**
   - **[Tool availability is observed](#tool-availability-is-observed)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Tool is the Component that defines atomic executable capabilities assigned to Agent Instance Definitions for use within their Roles, whether supplied by the runtime or an approved integration. Tools perform bounded actions; Skills compose them into reasoned workflows.

It owns tool identity, action boundaries, inputs, outputs, and availability. It does not own workflow decisions or permission policy.

### Purpose

Skills reason. Tools do. The separation matters because the two are governed differently: a workflow is judged by whether it reaches a good outcome, while a Tool is judged by whether one call did exactly what its contract said and nothing else. Mixing them makes both unverifiable — a workflow hidden inside a Tool cannot be reviewed, and a Tool whose effects are undeclared cannot be permissioned.

This Component exists to keep Tools atomic and honest about themselves. Every Tool declares what it takes, what it changes in the world, what it returns, how it fails, and what class of permission it needs. That declaration is what Permission constrains, what a Skill composes, and what a Role is granted.

It also exists to stop a familiar failure: treating a Tool as present because something said it was. A catalog entry is a claim. Availability is an observation.

### How It Works

A Tool is declared with an atomic contract: its inputs, its observable effects, its outputs, its failure modes, the scope it operates in, and the permission class it needs. One Tool is one capability. If a call performs several internal steps, they are steps of a single indivisible external action, not a workflow the caller cannot see.

Tools arrive from the Agent Runtime, from a Connection to an external provider, or from a packaged capability. Whatever the source, the contract is what the rest of the Agent works against — Agents and Skills invoke Tools through it, and Permission decides against it.

Availability is established by observation from the position that will actually use the Tool: the intended Role, in the required scope, able to discover and successfully call it. A Tool named in a catalog may still be disconnected, unauthenticated, incompatible, or invisible to that Role, so presence in a list never settles the question. Where a real call would be unsafe or irreversible, a non-mutating check stands in for it.

Portable Tool requirements and availability expectations live in Preferences; the Agent Native's own catalogs and mappings are resolved by Agent Sync.

<br>

## Terms

- **Tool** — an atomic callable capability exposed to an Agent Role.
- **Tool Contract** — a Tool's accepted inputs, effects, outputs, failure modes, and permission class.
- **Tool Availability** — verified discoverability and usability in the current runtime and scope.

## Relationships

- **Consumes Agent Runtime, Connection (formerly Integration), and Permission** — receives implementations, external capabilities, and execution authority.
- **Consumed by Agent (formerly Role), Skill, and Permission (formerly Hook)** — provides bounded actions they can invoke.

Portable tool requirements and availability expectations belong to Agent Tool Preferences; Native catalogs and mappings are resolved by Agent Sync from the selected Agent Native.

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every Tool has an atomic contract

**Rule:** Every Tool declares its inputs, observable effects, outputs, failure modes, scope, and permission class. A Tool performs one atomic capability and never embeds an undeclared project workflow.

**Why:** Atomic capabilities can be permissioned, composed, and verified independently.

**Boundary:** One call may perform several internal operations when they form one indivisible external action.

<br>

### Tool availability is observed

**Rule:** A Tool is available only when the intended Agent Role can discover and successfully call it in the required scope. Presence in a catalog or provider claim alone is insufficient.

**Why:** A declared Tool may still be disconnected, unauthorized, incompatible, or hidden from a role.

**Boundary:** A non-mutating capability check may substitute for a full action when the real action would be unsafe or irreversible.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Tool has an atomic contract**

- **Must** — give every Tool one atomic contract with effects and permission class
- **Never** — hide an undeclared project workflow inside a Tool

**Tool availability is observed**

- **Must** — verify Tool availability from the intended role and scope
- **Never** — infer availability from a catalog or provider claim
