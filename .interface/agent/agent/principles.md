# Agent Principles

Agent is the Component that declares the executable Agent identities in an Agent Profile. Each declared Agent realizes an Agent Role through a selected Runtime with bounded capabilities and configuration.

It owns Agent identity, kind, Role assignment, capability assignment, native realization, and lifecycle defaults. It does not own Role responsibilities, Skill behavior, Runtime implementation, coordination protocol, or Permission policy.

## Terms

- **Agent Definition** — one portable declaration of an executable Agent identity and the Role and capabilities it realizes.
- **General Agent** — the primary Agent accountable to the Human for the complete authorized request.
- **Specialized Agent** — an Agent that realizes a bounded supporting Role under delegation or direct invocation.
- **Native Agent** — the Runtime-specific realization of an Agent Definition.

## Relationships

- **Consumes Agent Runtime, Role, Context, Skill, Tool, Permission, and Session** — combines their contracts into executable Agent identities without redefining them.
- **Consumed by Agent Coordination** — supplies the concrete Agents that may be delegated, teamed, or isolated.
- **Consumed by Agent Observability** — supplies the declaration against which each Native Agent is validated.

Technical Agent declarations, primary selection, Role assignments, models, tools, Skills, permissions, memory, isolation, and native mappings belong to Agent Preferences.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Agent has one complete definition

**Rule:** Every required Agent has one stable Agent Definition declaring its identity, kind, assigned Role, native realization, capability assignments, configuration overrides, lifecycle behavior, and availability requirement. A Native Agent realizes that Definition without changing the contracts it references.

**Why:** A named Agent is reproducible only when another Runtime can determine what it is expected to realize.

**Boundary:** Values inherited unchanged from Role, Runtime, or shared defaults are referenced rather than copied into the Agent Definition.

<br>

## 2. Agent and Role remain separate

**Rule:** An Agent Definition states who executes; an Agent Role states the responsibility executed. Every Agent maps to at least one declared Role, and assigning a Role never transfers ownership of the Role contract into the Agent.

**Why:** Several Agents may realize the same Role differently, and one Agent identity may be reconfigured without changing the responsibility itself.

**Boundary:** One Agent may coordinate several Roles only when its assigned primary Role explicitly owns coordination of the complete outcome.

<br>

## 3. `general` is the primary Agent

**Rule:** The Agent Profile requires one General Agent with the stable identity `general`. It realizes the primary execution Role, remains accountable to the Human, activates applicable capabilities, delegates bounded work when useful, integrates delegated evidence, and makes the final outcome claim.

**Why:** Every request needs one concrete accountable Agent even when several Specialized Agents contribute.

**Boundary:** Primary accountability never broadens request scope, Permission, or Component authority.

<br>

## 4. Specialized Agents remain bounded

**Rule:** Every Specialized Agent maps to a declared supporting Role and receives only the Context, Skills, Tools, Permission, and lifecycle behavior required for that Role. It returns its result and evidence to the accountable General Agent or direct invoker without expanding its own assignment.

**Why:** Multiple Agents improve focus only when their responsibilities and capabilities remain inspectable and limited.

**Boundary:** A Specialized Agent may use professional judgment inside its assigned Role but never becomes the General Agent by delegation.

<br>

## 5. Agent availability is proven in the selected Runtime

**Rule:** A required Agent is available only when the selected Runtime can instantiate or expose its Native Agent, assign its declared Role and capabilities, and successfully invoke it in the current project. A declaration or native file alone is not proof.

**Why:** Coordination cannot safely depend on an Agent that exists only nominally.

**Boundary:** An incompatible or unavailable Native Agent is reported explicitly and never approximated with broader authority.

<br>

## At a Glance

- **Must** — give every required Agent one complete and stable Agent Definition *(1)*
- **Never** — let a Native Agent change the contracts referenced by its Definition *(1)*
- **Must** — map every Agent to a declared Role while keeping Agent identity and Role responsibility separate *(2)*
- **Must** — provide `general` as the primary Agent accountable for the complete authorized outcome *(3)*
- **Never** — let General Agent accountability broaden scope, Permission, or authority *(3)*
- **Must** — keep every Specialized Agent bounded to its supporting Role and required capabilities *(4)*
- **Never** — let delegation turn a Specialized Agent into the General Agent *(4)*
- **Must** — prove every required Agent can be instantiated and invoked in the selected Runtime *(5)*
- **Never** — approximate an unavailable Agent with broader authority *(5)*
