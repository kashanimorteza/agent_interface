# Agent Connection Definition

Agent Connection is the Executor Component that declares the external connections and installable packages an Agent obtains from outside the project.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Layering](#layering)**
4. **[Authority](#authority)**
5. **[Principles](#principles)**
6. **[Review](#review)**
7. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Agent Connection is the Component that declares everything the Agent obtains from outside the project: live connections to external capability providers (MCP and LSP servers, channels, application connectors) and installable packages (plugins, marketplaces, capability bundles, monitors). Both kinds of external capability are provisioned or connected by the Agent Native, carry a trust boundary, and may have Native-specific identity or connection details.

It owns connection declarations, trust boundaries, compatibility, and activation state, and each Extension's identity, provenance, contents, lifecycle, and expected capabilities. It does not own external systems, credentials, the Tools supplied through a connection, or the contracts of the capabilities an Extension contains.

### Purpose

Everything else in the Executor Module is declared by the Human and realized from that declaration. This Component covers the opposite case: capabilities that come from outside and are taken as they are. A tool server, a language server, a channel, an application connector, a plugin, a marketplace package — none of them is built from a portable specification. The Agent Native provisions or connects to each one through its own mechanism, and what arrives is whatever the provider supplies.

Live connections and installed packages are handled by one Component because both cross a trust boundary, depend on an external provider, and carry an identity that can differ from one Agent Native to the next.

The Component exists to make that crossing explicit. Something external can read project data and change systems the repository does not own, so what it touches, what it can do, and who authorized it are declared before it is used — not inferred afterwards from the fact that it worked.

### How It Works

Each Connection is declared with its provider, its protocol or source, the data it is exposed to, the actions it enables, its scope, its authentication requirement, and its Trust Boundary. Each package is declared by its own identity and source; an Agent Native that cannot use it reports it as unsupported. Credentials are never among the declared values; a declaration references a credential source and nothing more.

A declared Connection is not yet a usable one. It becomes available only when it is trusted, compatible, authenticated where required, actually connected, and usable by the Agent Instance that intends to use it. Any condition not met stays visible as unmet, and validating a Connection never doubles as accepting its trust or authorizing a login.

Authorization does not transfer across the boundary. An action with effects in an external system needs that system's own authorization, whatever the Agent's internal permission says.

Packaged capabilities keep their owners. An Extension declares its identity, source, and desired state, and the capabilities it contributes are read from the package itself; those capabilities remain governed by the Components that own them — a Skill it brings is still governed by Skill, a Tool by Tool, a guarantee by Permission. Provisioning — installing, enabling, updating, disabling, removing — happens within Permission, and the resulting state is declared rather than discovered.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Connection** — a declared connection between the Agent Runtime and an external capability provider.
- **Trust Boundary** — the point at which data or authority crosses between the project and an external system.
- **Connection State** — the observed availability, authentication, and health of a Connection.
- **Extension** — an installable or loadable package that contributes one or more Agent capabilities.
- **Marketplace** — a catalog or source from which Extensions can be discovered.
- **Provisioning** — installation, enabling, updating, disabling, or removal of an Extension.

<br>

<!--------------------------------------------------------------------------------- Layering --->
## Layering

This Definition carries the portable meaning and mandatory Principles of the Connection Component. Preferences carry current connection selections, declarations, and technical protocol and package choices. Agent Native Implement reads both and realizes them without changing their scope or authority.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

The Human owns this Definition and its Preferences. Every Principle in this file is mandatory; Preferences can never override a Principle, and Agent Native Implement is the only reader authorized to realize the Component in an Agent Native.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory.

<br>

### Every Connection declares its trust boundary

**Rule:** Every Connection declares its provider, protocol, data exposed, actions enabled, scope, authentication requirement, and Trust Boundary before use. Credentials and secret values are never stored in the project declaration.

**Why:** External capabilities can disclose data or mutate systems beyond the repository.

**Boundary:** A project may reference a credential source without owning or exposing its value.

<br>

### Connection is proven before dependence

**Rule:** A Connection is available only when it is declared, trusted, compatible, authenticated when required, connected, and usable by the intended Agent Instance. Every unmet condition remains explicit.

**Why:** Configuration alone does not establish a working external dependency.

**Boundary:** Validation does not authorize login, trust acceptance, or external mutation.

<br>

### External effects retain external authorization

**Rule:** A Connection never converts project permission into authority over an external account, service, recipient, or dataset. External actions follow the authorization required by their own scope and impact.

**Why:** Repository access and external-system authority are different trust decisions.

**Boundary:** Read-only discovery already authorized by the active task may proceed within declared policy.

<br>

### Extension provenance and contents are explicit

**Rule:** Every Extension declares its stable identity, source, and desired state. Its contents, permissions, and dependencies are read from the package itself at provisioning and reported before activation; an unpinned version resolves to the latest compatible version. Marketplace presence alone establishes none of these.

**Why:** Packages can execute code and introduce capabilities from outside the project.

**Boundary:** A runtime-bundled Extension may identify its source as runtime-provided.

<br>

### Extension lifecycle is controlled

**Rule:** Provisioning derives from current declared needs, previews material permissions and dependencies, obtains required authorization, verifies activation, and reconciles stale or conflicting state. Discovery alone never authorizes Provisioning.

**Why:** Capability sets must remain minimal, auditable, and reproducible.

**Boundary:** Reconciliation may report an available update without applying it.

<br>

### Packaged capabilities retain their owners

**Rule:** Packaging never changes a contained capability's contract, authority, or owning Executor Component. Extension metadata points to those contracts instead of redefining them.

**Why:** One capability must not acquire different semantics merely because it is distributed in a bundle.

**Boundary:** An Extension may add namespace and activation metadata required for distribution.

<br>

<!--------------------------------------------------------------------------------- Review --->
## Review

### Conformance

- Every Principle above is realized in the Agent Native.

### Checks

- Every declared package is in its declared state (enabled or disabled) in the Agent Native.
- Every declared marketplace resolves to its declared source.
- Every declared Connection reports its Capability Status, and none is treated as available while a condition is unmet.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

**Every Connection declares its trust boundary**

- **Must** — declare every Connection's provider, data, actions, scope, authentication, and trust boundary
- **Never** — store credentials or secret values in project declarations

**Connection is proven before dependence**

- **Must** — prove trust, compatibility, authentication, connection, and usability
- **Never** — treat validation as authority to activate a Connection

**External effects retain external authorization**

- **Never** — convert project permission into external-system authority

**Extension provenance and contents are explicit**

- **Must** — declare Extension identity, source, and desired state, and report its contents, permissions, and dependencies before activation

**Extension lifecycle is controlled**

- **Must** — authorize and verify every material Provisioning change
- **Never** — treat discovery as authorization to provision

**Packaged capabilities retain their owners**

- **Must** — preserve each packaged capability's contract and owner
