# Agent Integration Principles

Agent Integration is the Component that connects the Agent Runtime to external capability providers and protocols, including tool servers, code-intelligence services, communication channels, and external applications.

It owns connection declarations, trust boundaries, compatibility, and activation state. It does not own external systems, credentials, or the Tools supplied through a connection.

## Terms

- **Integration** — a declared connection between the Agent Runtime and an external capability provider.
- **Trust Boundary** — the point at which data or authority crosses between the project and an external system.
- **Connection State** — the observed availability, authentication, and health of an Integration.

## Relationships

- **Consumes Agent Runtime and Permission** — connects through supported mechanisms within security policy.
- **Consumed by Agent Tool, Hook, and Extension** — exposes external capabilities and package-provided connections.
- **Consumed by Agent Observability** — supplies connection health and activation evidence.

Technical MCP, LSP, channel, application, transport, and authentication-reference choices belong to Agent Integration Profile.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

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

## At a Glance

- **Must** — declare every Integration's provider, data, actions, scope, authentication, and trust boundary *(1)*
- **Never** — store credentials or secret values in project declarations *(1)*
- **Must** — prove trust, compatibility, authentication, connection, and usability *(2)*
- **Never** — treat validation as authority to activate an Integration *(2)*
- **Never** — convert project permission into external-system authority *(3)*
