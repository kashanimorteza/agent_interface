# Introduction

This section introduces Agent Interface as a Human-defined structure that connects Target, Implementation, and Agent through a shared software-development contract.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Overview](#overview)**
2. **[Purpose](#purpose)**
3. **[How It Works](#how-it-works)**
4. **[Independence](#independence)**
5. **[Core Idea](#core-idea)**
6. **[Design Goals](#design-goals)**

<br>

<!--------------------------------------------------------------------------------- Overview --->
## Overview

**Agent Interface** is an implementation-oriented interface for AI-assisted software development.

The core idea is to create a structured layer between an **Implementation**, an **AI Agent**, and a **Target** so that software can be understood, planned, developed, configured, and reviewed according to a consistent set of concepts.

The Interface is not tied to:

- one specific AI model,
- one specific coding agent,
- one specific implementation,
- or one specific software project.

These concepts are intentionally separated, so a different Target, Implementation, or Agent can be introduced without redesigning the others.

Skills, hooks, plugins, MCP, memory systems, multiple agents, and tools are possible Native realization mechanisms, not part of the conceptual contract itself.

The primary concern of the Interface is the **conceptual contract** between the Implementation, Agent, and Target.

<br>

<!--------------------------------------------------------------------------------- Purpose --->
## Purpose

Agent Interface is an independent interface between **Humans** and **AI Agents** for establishing a common protocol, structure, and standard for software development.

Its purpose is to let a Human define a Target in natural language, provide common Implementation Principles and Preferences for planning and developing it, and define a portable Agent Module that explicit Agent Sync realizes in the active Runtime.

<br>

<!--------------------------------------------------------------------------------- How It Works --->
## How It Works

The Human states the Target in the Non-Technical Definition and translates that intent into the Technical Definition without changing its meaning. Skills then read the current sources required by their role before acting. Planning records activities as Tasks; Development implements and verifies those Tasks; Review evaluates the result; and Launch brings the completed Target online. Mechanical actions such as Config initialization do not interpret the Target.

Config contains only the mutable operational records used to coordinate this work. Schemas define their storage format.

<br>

<!--------------------------------------------------------------------------------- Independence --->
## Independence

The core Interface Structure is independent of any specific AI model, Agent Native, or external execution capability. Portable Contracts for Interface-owned Skills belong to the Agent Module, while their self-contained native implementations remain outside `.interface/` as synchronized Runtime adapters. External Skills remain provider-owned capabilities declared by the Agent Preferences. Only explicit Agent Sync reads Agent Module sources; every other Runtime operation consumes their last synchronized realization.

Human project definitions remain flexible, while the Interface gives Agents stable responsibilities, rules, defaults, and operational records. Agent Interface is the communication boundary between those two forms.

<br>

<!--------------------------------------------------------------------------------- Core Idea --->
## Core Idea

Modern AI coding agents can generate and modify software, but an agent still needs to understand several independent things before it can reliably act:

1. **What is being built?**
2. **How does the implementation want software to be built?**
3. **What agent is performing the work and what capabilities or restrictions does it have?**
4. **What Workflow Mode or Operation is currently active?**

Agent Interface gives these concerns explicit structure.

Conceptually:

```text
Target ─────┐
Implementation ──┼── together with Understanding, Modes, and Workflow ──> Execution
Agent ──────┘
```

The resulting software is therefore influenced by all three primary entities:

```text
Target
   +
Implementation
   +
Agent
   ↓
Execution
```

<br>

<!--------------------------------------------------------------------------------- Design Goals --->
## Design Goals

The Interface should make the following substitutions possible without redesigning the entire system:

```text
Target A     → Target B
Implementation A  → Implementation B
Agent A      → Agent B
```

Changing one should not unnecessarily redefine the others.

This separation is one of the central architectural principles of the project.
