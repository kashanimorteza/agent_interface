# Agent Command Principles

Agent Command is the Component that defines named entry points through which a Human or Agent requests a built-in action or activates a Capability. It provides a stable invocation surface even when a runtime implements commands through Skills or another native mechanism.

It owns command names, arguments, routing, and discoverability. It does not own the workflow or capability invoked by a command.

## Terms

- **Command** — a named invocation entry point with a defined argument contract.
- **Built-in Command** — an entry point supplied and implemented by the Agent Runtime.
- **Custom Command** — a project, user, or extension entry point mapped to a declared capability.

## Relationships

- **Consumes Agent Skill, Role, Tool, and Runtime** — routes an invocation to its implementing capability.
- **Consumed by Agent Interaction** — provides discoverable Human-facing actions.

Technical command names, aliases, argument forms, and native mappings belong to Agent Command Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. A Command is an entry point, not a second workflow

**Rule:** Every Custom Command maps to one owning Capability Contract and adds no competing workflow, authority, or policy. Its arguments are validated before routing.

**Why:** Duplicated behavior drifts when one copy changes.

**Boundary:** A Built-in Command may execute fixed runtime logic whose contract is supplied by the runtime.

<br>

## 2. Command invocation is stable and discoverable

**Rule:** Command names, aliases, accepted arguments, owner, availability, and invocation scope are explicit. A collision or unavailable target is reported rather than resolved by guesswork.

**Why:** Entry points are interfaces and must behave predictably.

**Boundary:** A runtime may present commands differently while preserving the declared invocation contract.

<br>

## At a Glance

- **Must** — map every Custom Command to one owning Capability Contract *(1)*
- **Never** — duplicate workflow, authority, or policy inside a Command *(1)*
- **Must** — declare command names, arguments, ownership, scope, and availability *(2)*
- **Never** — guess through a collision or unavailable command target *(2)*
