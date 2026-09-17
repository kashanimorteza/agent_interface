# Agent Runtime Principles

Agent Runtime is the Component that supplies the Agent Native, lets it instantiate Agent Instance Definitions and execute their assigned Roles, and exposes the native mechanisms used to realize the Agent Preferences. It keeps the Interface independent of one model, provider, client, or capability format.

It owns runtime identity, compatibility, the models available on the selected Runtime, and how that Runtime's own configuration sources combine. It does not own behavioral instructions, project intent, permissions, or the capabilities implemented through the runtime.

*Absorbed from the former Agent Settings Component on 2026-09-17 — its introduction, kept verbatim:* Agent Settings is the Component that declares how Agent configuration sources are scoped, combined, selected, and reconciled. It makes the effective configuration explainable without turning runtime files into a second source of project intent. It owns configuration source precedence and reconciliation. It does not own the choices governed by other Agent Components. Technical source scopes, merge behavior, and native locations belong to Agent Settings Preferences.

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

- **Consumes Agent Settings** — receives the selected runtime configuration and source precedence.
- **Consumed by Agent and every executing Agent Component** — provides the execution environment and native mechanisms in which their declarations are realized.
- **Consumes every Agent Component** — receives the choices each Component owns. *(formerly Agent Settings)*
- **Consumed by Agent Runtime** — provides the configuration that the runtime applies. *(formerly Agent Settings)*
- **Consumed by Agent Observability** — provides expected values for diagnostics. *(formerly Agent Settings)*

The selected runtime and compatibility choice belong to Agent Runtime Preferences; Native-specific realization details are learned by Agent Sync from the selected Agent Native.

Every statement here is mandatory. Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. The Agent Runtime is replaceable

**Rule:** Every Agent responsibility and Capability Contract is defined independently of a particular model, provider, client, runtime, or native capability format. A Runtime Mapping preserves those contracts without changing their meaning, authority, or boundaries.

**Why:** The same Interface must remain executable when its runtime changes.

**Boundary:** Runtime-specific paths, formats, flags, and mappings are not portable Module requirements; Agent Sync resolves them from the selected Agent Native.

<br>

## 2. Runtime compatibility is explicit

**Rule:** A selected Agent Runtime must expose or compatibly realize every required Agent Module declaration. Agent Sync learns the Native mechanisms, destinations, activation rules, and verification obligations from the selected Agent Native and reports an unsupported or ambiguous requirement as unavailable; it never silently approximates one.

**Why:** A similar-looking native feature may have different authority or lifecycle semantics.

**Boundary:** A Module declaration need not have a dedicated native directory or a predeclared mapping. Native-provided and explicitly unused declarations remain valid when the Native Runtime makes their observation and verification unambiguous. Optional native capabilities may remain available without becoming project requirements and are preserved as unmanaged.

<br>

## 3. Every effective setting has an explainable source

**Rule:** Configuration sources, their scopes, precedence, and merge behavior are explicit. Every Effective Setting can be traced to the sources that produced it.

**Why:** Hidden precedence makes identical project files behave differently without an actionable explanation.

**Boundary:** This Component explains resolution but does not override a stricter authority owned elsewhere.

*Formerly Settings Principle 1; the other Settings Principles became rules of every Agent Preferences in the Agent Preferences Schema on 2026-09-17.*

<br>

## At a Glance

- **Must** — define Agent contracts independently of a concrete runtime *(1)*
- **Must** — preserve meaning, authority, and boundaries through Runtime Mapping *(1)*
- **Must** — have Agent Sync resolve every required capability through the selected Native or report it unavailable *(2)*
- **Never** — require a predeclared realization record or native directory for a Module declaration *(2)*
- **Never** — remove an undeclared native capability merely to realize an explicitly unused Component *(2)*
- **Never** — silently approximate an incompatible requirement *(2)*
- **Must** — make source scope, precedence, merge behavior, and effective origin explicit *(3)*
