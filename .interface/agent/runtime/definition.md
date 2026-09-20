# Agent Runtime Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[The Agent Runtime is replaceable](#the-agent-runtime-is-replaceable)**
   - **[Runtime compatibility is explicit](#runtime-compatibility-is-explicit)**
   - **[Every effective setting has an explainable source](#every-effective-setting-has-an-explainable-source)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Runtime is the Component that supplies the Agent Native, lets it instantiate Agent Instance Definitions and execute their assigned Roles, and exposes the native mechanisms used to realize the Agent Preferences. It keeps the Interface independent of one model, provider, client, or capability format.

It owns runtime identity, compatibility, the models available on the selected Runtime, and how that Runtime's own configuration sources combine. It does not own behavioral instructions, project intent, permissions, or the capabilities implemented through the runtime.

*Absorbed from the former Agent Settings Component on 2026-09-17 — its introduction, kept verbatim:* Agent Settings is the Component that declares how Agent configuration sources are scoped, combined, selected, and reconciled. It makes the effective configuration explainable without turning runtime files into a second source of project intent. It owns configuration source precedence and reconciliation. It does not own the choices governed by other Agent Components. Technical source scopes, merge behavior, and native locations belong to Agent Settings Preferences.

### Purpose

An Agent only exists as something concrete once a Runtime hosts it: a provider, a model, a client, a set of native mechanisms, and a set of configuration sources that combine in that Runtime's own way. Those things change — a new model, a different client, another vendor entirely — and if the Module is written in their terms, every change rewrites the Module.

Runtime exists to hold that dependency in one Component so nothing else carries it. It names which Runtime is selected, which models that Runtime makes available, what compatibility the Module requires of it, and how that Runtime's own configuration sources combine into the effective settings. Everything else in the Module can then be written about an Agent in general.

Without it, the Runtime's assumptions spread: a model name appears inside a Skill, a native configuration path appears inside a Rule, and the portable Module becomes a Module for one vendor. The second Runtime then costs what the first one did.

### How It Works

One Agent Runtime is selected, and that selection is what makes the abstract Module executable: it supplies the Agent Native, lets it instantiate the Agent Instance Definitions the Agent Component declares, and exposes the native mechanisms through which every other Component's declarations are realized.

What the Module requires of a Runtime is stated as compatibility rather than assumed. A Runtime that cannot provide something a declaration needs is a fact to be reported, not a gap to be worked around silently.

Models are named here and referenced elsewhere. Personality names the models it prefers in priority order; Runtime holds what those names mean on the selected Runtime, so a model change is a change in one place.

Effective settings come from several sources — project, user, managed, runtime defaults — combining in the Runtime's own order. Runtime owns that explanation: for any effective value, which source supplied it and why it won. The mechanics of one particular Native are hints under its own block, never the authority.

<br>

## Terms

- **Agent Runtime** — the concrete execution system that supplies and hosts the Agent Native and its capabilities.
- **Agent Native** — the core operational Agent supplied by the Agent Runtime; it receives Human requests and hosts or coordinates Agent Instances.
- **Agent Instance** — one primary or specialized executable identity instantiated within the Agent Native.
- **Runtime Mapping** — the correspondence between an Interface capability and its native runtime mechanism.
- **Compatibility** — the ability to preserve a Capability Contract in a particular runtime.
- **Configuration Source** — one location or invocation layer that contributes Agent settings. *(formerly Agent Settings)*
- **Effective Setting** — the value produced after all applicable sources and merge rules are resolved. *(formerly Agent Settings)*
- **Reconciliation** — comparison of declared choices with observed runtime configuration. *(formerly Agent Settings)*

## Relationships

- **Consumes the Agent Preferences Schema's profile rules and its own `native.<agent-native>` configuration (formerly Agent Settings)** — receives the selected runtime configuration and source precedence.
- **Consumed by Agent and every executing Agent Component** — provides the execution environment and native mechanisms in which their declarations are realized.
- **Consumes every Agent Component** — receives the choices each Component owns. *(formerly Agent Settings)*
- **Consumed by Agent Runtime** — provides the configuration that the runtime applies. *(formerly Agent Settings)*
- **Consumed by Agent Rule (formerly Observability)** — provides expected values for diagnostics. *(formerly Agent Settings)*

The selected runtime and compatibility choice belong to Agent Runtime Preferences; Native-specific realization details are learned by Agent Sync from the selected Agent Native.

Every Principle in this file is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### The Agent Runtime is replaceable

**Rule:** Every Agent responsibility and Capability Contract is defined independently of a particular model, provider, client, runtime, or native capability format. A Runtime Mapping preserves those contracts without changing their meaning, authority, or boundaries.

**Why:** The same Interface must remain executable when its runtime changes.

**Boundary:** Runtime-specific paths, formats, flags, and mappings are not portable Module requirements; Agent Sync resolves them from the selected Agent Native.

<br>

### Runtime compatibility is explicit

**Rule:** A selected Agent Runtime must expose or compatibly realize every required Agent Module declaration. Agent Sync learns the Native mechanisms, destinations, activation rules, and verification obligations from the selected Agent Native and reports an unsupported or ambiguous requirement as unavailable; it never silently approximates one.

**Why:** A similar-looking native feature may have different authority or lifecycle semantics.

**Boundary:** A Module declaration need not have a dedicated native directory or a predeclared mapping. Native-provided and explicitly unused declarations remain valid when the Native Runtime makes their observation and verification unambiguous. Optional native capabilities may remain available without becoming project requirements and are preserved as unmanaged.

<br>

### Every effective setting has an explainable source

**Rule:** Configuration sources, their scopes, precedence, and merge behavior are explicit. Every Effective Setting can be traced to the sources that produced it.

**Why:** Hidden precedence makes identical project files behave differently without an actionable explanation.

**Boundary:** This Component explains resolution but does not override a stricter authority owned elsewhere.

*Formerly Settings Principle "The Agent Runtime is replaceable"; the other Settings Principles became rules of every Agent Preferences in the Agent Preferences Schema on 2026-09-17.*

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**The Agent Runtime is replaceable**

- **Must** — define Agent contracts independently of a concrete runtime
- **Must** — preserve meaning, authority, and boundaries through Runtime Mapping

**Runtime compatibility is explicit**

- **Must** — have Agent Sync resolve every required capability through the selected Native or report it unavailable
- **Never** — require a predeclared realization record or native directory for a Module declaration
- **Never** — remove an undeclared native capability merely to realize an explicitly unused Component
- **Never** — silently approximate an incompatible requirement

**Every effective setting has an explainable source**

- **Must** — make source scope, precedence, merge behavior, and effective origin explicit
