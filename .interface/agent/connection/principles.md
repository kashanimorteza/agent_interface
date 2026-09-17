# Agent Connection Principles

Agent Connection is the Component that declares everything the Agent obtains from outside the project: live connections to external capability providers (MCP and LSP servers, channels, application connectors) and installable packages (plugins, marketplaces, capability bundles). On 2026-09-17 the former Integration and Extension Components were merged here: both declare Installed capabilities that the Agent Native provisions through its own mechanism from an external source, and both carry a trust boundary and per-Native identity. Nothing was dropped; each absorbed Principle keeps its former number in a note.

*Absorbed from the former Agent Integration Component on 2026-09-17 — its introduction, kept verbatim:* Agent Integration is the Component that connects the Agent Runtime to external capability providers and protocols, including tool servers, code-intelligence services, communication channels, and external applications. Every declared Integration is Installed: the Agent Native connects to it through its own native mechanism, and it is never built from a portable specification. Because a connection mechanism can differ by Agent Native even when the underlying protocol is shared, an Integration's connection details may be declared separately per Agent Native.

It owns connection declarations, trust boundaries, compatibility, and activation state. It does not own external systems, credentials, or the Tools supplied through a connection.

*Absorbed from the former Agent Extension Component on 2026-09-17 — its introduction, kept verbatim:* Agent Extension is the Component that packages and distributes related Agent capabilities through installable units and catalogs. It governs plugins, marketplaces, capability packages, and runtime-supported extension bundles. Every capability it packages is Installed: the Agent Native provisions it through its own native mechanism from an external source, and never builds it from a portable specification. Because marketplaces and package ecosystems differ by Agent Native, an Extension's identity may be declared separately per Agent Native so each Native can locate and provision it.

It owns extension identity, provenance, contents, lifecycle, and expected capabilities. It does not own the contracts of the capabilities an extension contains.

## Terms

- **Integration** — a declared connection between the Agent Runtime and an external capability provider.
- **Trust Boundary** — the point at which data or authority crosses between the project and an external system.
- **Connection State** — the observed availability, authentication, and health of an Integration.
- **Extension** — an installable or loadable package that contributes one or more Agent capabilities.
- **Marketplace** — a catalog or source from which Extensions can be discovered.
- **Provisioning** — installation, enabling, updating, disabling, or removal of an Extension.

## Relationships

- **Consumes Agent Runtime and Permission** — connects through supported mechanisms within security policy.
- **Consumed by Agent Tool, Hook, and Extension** — exposes external capabilities and package-provided connections.
- **Consumed by Agent Observability** — supplies connection health and activation evidence.
- **Consumes Agent Skill, Role, Hook, Integration, Tool, and Interaction** — packages capabilities owned by those Components.
- **Consumes Agent Permission** — performs Provisioning within authorization.
- **Consumed by Agent Runtime and Settings** — supplies runtime-loadable capability bundles and declarations.

Technical MCP, LSP, channel, application, transport, and authentication-reference choices belong to Agent Integration Preferences.

Technical Extension catalogs, versions, sources, enabled state, and expected contents belong to Agent Extension Preferences.

Every statement here is mandatory. Preferences can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Integration declares its trust boundary

**Rule:** Every Integration declares its provider, protocol, data exposed, actions enabled, scope, authentication requirement, and Trust Boundary before use. Credentials and secret values are never stored in the project declaration.

**Why:** External capabilities can disclose data or mutate systems beyond the repository.

**Boundary:** A project may reference a credential source without owning or exposing its value.

<br>

## 2. Connection is proven before dependence

**Rule:** An Integration is available only when it is declared, trusted, compatible, authenticated when required, connected, and usable by the intended role. Every unmet condition remains explicit.

**Why:** Configuration alone does not establish a working external dependency.

**Boundary:** Validation does not authorize login, trust acceptance, or external mutation.

<br>

## 3. External effects retain external authorization

**Rule:** An Integration never converts project permission into authority over an external account, service, recipient, or dataset. External actions follow the authorization required by their own scope and impact.

**Why:** Repository access and external-system authority are different trust decisions.

**Boundary:** Read-only discovery already authorized by the active task may proceed within declared policy.

<br>

## 4. Extension provenance and contents are explicit

**Rule:** Every Extension declares its stable identity, source, version policy, expected capability categories, permissions, dependencies, and trust status. Marketplace presence alone establishes none of these.

**Why:** Packages can execute code and introduce capabilities from outside the project.

**Boundary:** A runtime-bundled Extension may identify its source as runtime-provided.

*Formerly Agent Extension Principle 1.*

<br>

## 5. Extension lifecycle is controlled

**Rule:** Provisioning derives from current declared needs, previews material permissions and dependencies, obtains required authorization, verifies activation, and reconciles stale or conflicting state. Discovery alone never authorizes Provisioning.

**Why:** Capability sets must remain minimal, auditable, and reproducible.

**Boundary:** Reconciliation may report an available update without applying it.

*Formerly Agent Extension Principle 2.*

<br>

## 6. Packaged capabilities retain their owners

**Rule:** Packaging never changes a contained capability's contract, authority, or owning Agent Component. Extension metadata points to those contracts instead of redefining them.

**Why:** One capability must not acquire different semantics merely because it is distributed in a bundle.

**Boundary:** An Extension may add namespace and activation metadata required for distribution.

*Formerly Agent Extension Principle 3.*

<br>

## At a Glance

- **Must** — declare every Integration's provider, data, actions, scope, authentication, and trust boundary *(1)*
- **Never** — store credentials or secret values in project declarations *(1)*
- **Must** — prove trust, compatibility, authentication, connection, and usability *(2)*
- **Never** — treat validation as authority to activate an Integration *(2)*
- **Never** — convert project permission into external-system authority *(3)*
- **Must** — declare Extension identity, provenance, version, contents, permissions, dependencies, and trust *(4)*
- **Must** — authorize and verify every material Provisioning change *(5)*
- **Never** — treat discovery as authorization to provision *(5)*
- **Must** — preserve each packaged capability's contract and owner *(6)*
