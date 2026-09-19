# Agent Connection Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Every Integration declares its trust boundary](#every-integration-declares-its-trust-boundary)**
   - **[Connection is proven before dependence](#connection-is-proven-before-dependence)**
   - **[External effects retain external authorization](#external-effects-retain-external-authorization)**
   - **[Extension provenance and contents are explicit](#extension-provenance-and-contents-are-explicit)**
   - **[Extension lifecycle is controlled](#extension-lifecycle-is-controlled)**
   - **[Packaged capabilities retain their owners](#packaged-capabilities-retain-their-owners)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Agent Connection is the Component that declares everything the Agent obtains from outside the project: live connections to external capability providers (MCP and LSP servers, channels, application connectors) and installable packages (plugins, marketplaces, capability bundles). On 2026-09-17 the former Integration and Extension Components were merged here: both declare Installed capabilities that the Agent Native provisions through its own mechanism from an external source, and both carry a trust boundary and per-Native identity. Nothing was dropped; each absorbed Principle keeps its former number in a note.

*Absorbed from the former Agent Integration Component on 2026-09-17 — its introduction, kept verbatim:* Agent Integration is the Component that connects the Agent Runtime to external capability providers and protocols, including tool servers, code-intelligence services, communication channels, and external applications. Every declared Integration is Installed: the Agent Native connects to it through its own native mechanism, and it is never built from a portable specification. Because a connection mechanism can differ by Agent Native even when the underlying protocol is shared, an Integration's connection details may be declared separately per Agent Native.

It owns connection declarations, trust boundaries, compatibility, and activation state. It does not own external systems, credentials, or the Tools supplied through a connection.

*Absorbed from the former Agent Extension Component on 2026-09-17 — its introduction, kept verbatim:* Agent Extension is the Component that packages and distributes related Agent capabilities through installable units and catalogs. It governs plugins, marketplaces, capability packages, and runtime-supported extension bundles. Every capability it packages is Installed: the Agent Native provisions it through its own native mechanism from an external source, and never builds it from a portable specification. Because marketplaces and package ecosystems differ by Agent Native, an Extension's identity may be declared separately per Agent Native so each Native can locate and provision it.

It owns extension identity, provenance, contents, lifecycle, and expected capabilities. It does not own the contracts of the capabilities an extension contains.

### Purpose

Everything else in the Agent Module is declared by the Human and realized from that declaration. This Component covers the opposite case: capabilities that come from outside and are taken as they are. A tool server, a language server, a channel, an application connector, a plugin, a marketplace package — none of them is built from a portable specification. The Agent Native provisions or connects to each one through its own mechanism, and what arrives is whatever the provider supplies.

That is why Integration and Extension are one Component. A live connection and an installed package differ in mechanism, not in nature: both are Installed, both cross a trust boundary, and both carry an identity that can differ from one Agent Native to the next.

The Component exists to make that crossing explicit. Something external can read project data and change systems the repository does not own, so what it touches, what it can do, and who authorized it are declared before it is used — not inferred afterwards from the fact that it worked.

### How It Works

Each Connection is declared with its provider, its protocol or source, the data it is exposed to, the actions it enables, its scope, its authentication requirement, and its Trust Boundary. Because the connection and provisioning mechanisms differ by Agent Native, identity and connection details may be declared per Native, so each one can locate what it needs. Credentials are never among the declared values; a declaration references a credential source and nothing more.

A declared Connection is not yet a usable one. It becomes available only when it is trusted, compatible, authenticated where required, actually connected, and usable by the Role that intends to use it. Any condition not met stays visible as unmet, and validating a Connection never doubles as accepting its trust or authorizing a login.

Authorization does not transfer across the boundary. An action with effects in an external system needs that system's own authorization, whatever the Agent's internal permission says.

Packaged capabilities keep their owners. An Extension declares its provenance, its version or source, and the capabilities it is expected to contribute; those capabilities remain governed by the Components that own them — a Skill it brings is still governed by Skill, a Tool by Tool, a guarantee by Permission. Provisioning — installing, enabling, updating, disabling, removing — happens within Permission, and the resulting state is declared rather than discovered.

<br>

## Terms

- **Integration** — a declared connection between the Agent Runtime and an external capability provider.
- **Trust Boundary** — the point at which data or authority crosses between the project and an external system.
- **Connection State** — the observed availability, authentication, and health of an Integration.
- **Extension** — an installable or loadable package that contributes one or more Agent capabilities.
- **Marketplace** — a catalog or source from which Extensions can be discovered.
- **Provisioning** — installation, enabling, updating, disabling, or removal of an Extension.

## Relationships

- **Consumes Agent Runtime and Permission** — connects through supported mechanisms within security policy.
- **Consumed by Agent Tool, Permission (formerly Hook), and Connection (formerly Extension)** — exposes external capabilities and package-provided connections.
- **Consumed by Agent Rule (formerly Observability)** — supplies connection health and activation evidence.
- **Consumes Agent Skill, Agent (formerly Role), Permission (formerly Hook), Connection (formerly Integration), Tool, and Rule (formerly Interaction)** — packages capabilities owned by those Components.
- **Consumes Agent Permission** — performs Provisioning within authorization.
- **Consumed by Agent Runtime (including former Settings)** — supplies runtime-loadable capability bundles and declarations.

Technical MCP, LSP, channel, application, transport, and authentication-reference choices belong to Agent Connection Preferences (formerly Integration Preferences).

Technical Extension catalogs, versions, sources, enabled state, and expected contents belong to Agent Connection Preferences (formerly Extension Preferences).

Every statement here is mandatory. An Agent Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Every Integration declares its trust boundary

**Rule:** Every Integration declares its provider, protocol, data exposed, actions enabled, scope, authentication requirement, and Trust Boundary before use. Credentials and secret values are never stored in the project declaration.

**Why:** External capabilities can disclose data or mutate systems beyond the repository.

**Boundary:** A project may reference a credential source without owning or exposing its value.

<br>

### Connection is proven before dependence

**Rule:** An Integration is available only when it is declared, trusted, compatible, authenticated when required, connected, and usable by the intended role. Every unmet condition remains explicit.

**Why:** Configuration alone does not establish a working external dependency.

**Boundary:** Validation does not authorize login, trust acceptance, or external mutation.

<br>

### External effects retain external authorization

**Rule:** An Integration never converts project permission into authority over an external account, service, recipient, or dataset. External actions follow the authorization required by their own scope and impact.

**Why:** Repository access and external-system authority are different trust decisions.

**Boundary:** Read-only discovery already authorized by the active task may proceed within declared policy.

<br>

### Extension provenance and contents are explicit

**Rule:** Every Extension declares its stable identity, source, version policy, expected capability categories, permissions, dependencies, and trust status. Marketplace presence alone establishes none of these.

**Why:** Packages can execute code and introduce capabilities from outside the project.

**Boundary:** A runtime-bundled Extension may identify its source as runtime-provided.

*Formerly Agent Extension Principle "Every Integration declares its trust boundary".*

<br>

### Extension lifecycle is controlled

**Rule:** Provisioning derives from current declared needs, previews material permissions and dependencies, obtains required authorization, verifies activation, and reconciles stale or conflicting state. Discovery alone never authorizes Provisioning.

**Why:** Capability sets must remain minimal, auditable, and reproducible.

**Boundary:** Reconciliation may report an available update without applying it.

*Formerly Agent Extension Principle "Connection is proven before dependence".*

<br>

### Packaged capabilities retain their owners

**Rule:** Packaging never changes a contained capability's contract, authority, or owning Agent Component. Extension metadata points to those contracts instead of redefining them.

**Why:** One capability must not acquire different semantics merely because it is distributed in a bundle.

**Boundary:** An Extension may add namespace and activation metadata required for distribution.

*Formerly Agent Extension Principle "External effects retain external authorization".*

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Integration declares its trust boundary**

- **Must** — declare every Integration's provider, data, actions, scope, authentication, and trust boundary
- **Never** — store credentials or secret values in project declarations

**Connection is proven before dependence**

- **Must** — prove trust, compatibility, authentication, connection, and usability
- **Never** — treat validation as authority to activate an Integration

**External effects retain external authorization**

- **Never** — convert project permission into external-system authority

**Extension provenance and contents are explicit**

- **Must** — declare Extension identity, provenance, version, contents, permissions, dependencies, and trust

**Extension lifecycle is controlled**

- **Must** — authorize and verify every material Provisioning change
- **Never** — treat discovery as authorization to provision

**Packaged capabilities retain their owners**

- **Must** — preserve each packaged capability's contract and owner
