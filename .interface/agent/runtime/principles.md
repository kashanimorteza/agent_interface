# Agent Runtime Principles

Agent Runtime is the Component that instantiates Agent Definitions, executes their assigned Roles, and exposes the native mechanisms used to realize the Agent Profile. It keeps the Interface independent of one model, provider, client, or capability format.

It owns runtime identity and compatibility. It does not own behavioral instructions, project intent, permissions, or the capabilities implemented through the runtime.

## Terms

- **Agent Runtime** — the concrete execution system that hosts Native Agents, their assigned Roles, and Capabilities.
- **Runtime Mapping** — the correspondence between an Interface capability and its native runtime mechanism.
- **Compatibility** — the ability to preserve a Capability Contract in a particular runtime.

## Relationships

- **Consumes Agent Settings** — receives the selected runtime configuration and source precedence.
- **Consumed by Agent and every executing Agent Component** — provides the execution environment and native mechanisms in which their declarations are realized.

Technical runtime choices belong to Agent Runtime Preferences; implementation maps them to the selected runtime.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The Agent Runtime is replaceable

**Rule:** Every Agent responsibility and Capability Contract is defined independently of a particular model, provider, client, runtime, or native capability format. A Runtime Mapping preserves those contracts without changing their meaning, authority, or boundaries.

**Why:** The same Interface must remain executable when its runtime changes.

**Boundary:** Runtime-specific paths, versions, flags, and mappings belong to Preferences.

<br>

## 2. Runtime compatibility is explicit

**Rule:** A selected Agent Runtime must expose or compatibly map every required capability. An unmapped or incompatible requirement is reported as unavailable and never silently approximated.

**Why:** A similar-looking native feature may have different authority or lifecycle semantics.

**Boundary:** Optional native capabilities may remain available without becoming project requirements.

<br>

## At a Glance

- **Must** — define Agent contracts independently of a concrete runtime *(1)*
- **Must** — preserve meaning, authority, and boundaries through Runtime Mapping *(1)*
- **Must** — explicitly map every required capability or report it unavailable *(2)*
- **Never** — silently approximate an incompatible requirement *(2)*
