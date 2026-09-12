# Agent Extension Principles

Agent Extension is the Component that packages and distributes related Agent capabilities through installable units and catalogs. It governs plugins, marketplaces, capability packages, and runtime-supported extension bundles.

It owns extension identity, provenance, contents, lifecycle, and expected capabilities. It does not own the contracts of the capabilities an extension contains.

## Terms

- **Extension** — an installable or loadable package that contributes one or more Agent capabilities.
- **Marketplace** — a catalog or source from which Extensions can be discovered.
- **Provisioning** — installation, enabling, updating, disabling, or removal of an Extension.

## Relationships

- **Consumes Agent Skill, Role, Hook, Integration, Tool, and Interaction** — packages capabilities owned by those Components.
- **Consumes Agent Permission** — performs Provisioning within authorization.
- **Consumed by Agent Runtime and Settings** — supplies runtime-loadable capability bundles and declarations.

Technical Extension catalogs, versions, sources, enabled state, and expected contents belong to Agent Extension Profile.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Extension provenance and contents are explicit

**Rule:** Every Extension declares its stable identity, source, version policy, expected capability categories, permissions, dependencies, and trust status. Marketplace presence alone establishes none of these.

**Why:** Packages can execute code and introduce capabilities from outside the project.

**Boundary:** A runtime-bundled Extension may identify its source as runtime-provided.

<br>

## 2. Extension lifecycle is controlled

**Rule:** Provisioning derives from current declared needs, previews material permissions and dependencies, obtains required authorization, verifies activation, and reconciles stale or conflicting state. Discovery alone never authorizes Provisioning.

**Why:** Capability sets must remain minimal, auditable, and reproducible.

**Boundary:** Reconciliation may report an available update without applying it.

<br>

## 3. Packaged capabilities retain their owners

**Rule:** Packaging never changes a contained capability's contract, authority, or owning Agent Component. Extension metadata points to those contracts instead of redefining them.

**Why:** One capability must not acquire different semantics merely because it is distributed in a bundle.

**Boundary:** An Extension may add namespace and activation metadata required for distribution.

<br>

## At a Glance

- **Must** — declare Extension identity, provenance, version, contents, permissions, dependencies, and trust *(1)*
- **Must** — authorize and verify every material Provisioning change *(2)*
- **Never** — treat discovery as authorization to provision *(2)*
- **Must** — preserve each packaged capability's contract and owner *(3)*
