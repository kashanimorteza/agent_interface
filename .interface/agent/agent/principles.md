# Agent Principles

The `Agent` Component declares the selected Agent Native and the executable Agent Instances it hosts in an Agent Profile. Each Agent Instance realizes an Agent Role through the Agent Native with bounded capabilities and configuration.

It owns Agent Native selection, Agent Instance identity, kind, Role assignment, capability assignment, native realization, and lifecycle defaults. It does not own Role responsibilities, Skill behavior, Runtime implementation, coordination protocol, or Permission policy.

## Terms

- **Agent Native** — the core operational Agent supplied by the selected Agent Runtime; it receives the Human's request and hosts or coordinates its Agent Instances.
- **Agent Instance Definition** — one portable declaration of an executable Agent Instance identity and the Role and capabilities it realizes.
- **General Agent Instance** — the primary Agent Instance accountable to the Human for the complete authorized request.
- **Specialized Agent Instance** — an Agent Instance that realizes a bounded supporting Role under delegation or direct invocation.

## Relationships

- **Consumes Agent Runtime, Role, Context, Skill, Tool, Permission, and Session** — selects the Agent Native and combines their contracts into executable Agent Instances without redefining them.
- **Consumed by Agent Coordination** — supplies the concrete Agent Instances that may be delegated, teamed, or isolated.
- **Consumed by Agent Observability** — supplies the declarations against which the Agent Native and every Agent Instance realization are validated.

Agent Native selection, Agent Instance declarations, primary Instance selection, Role assignments, models, tools, Skills, permissions, memory, isolation, and portable realization requirements belong to Agent Profile. Native paths, file formats, and runtime-specific mappings are resolved by Agent Sync from the selected Agent Native.

Every statement here is mandatory. A Profile can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Every Agent Instance has one complete definition

**Rule:** Every required Agent Instance has one stable Agent Instance Definition declaring its identity, kind, assigned Role, native realization, capability assignments, configuration overrides, lifecycle behavior, and availability requirement. The Agent Native realizes that Definition without changing the contracts it references.

**Why:** A named Agent Instance is reproducible only when another Runtime can determine what it is expected to realize.

**Boundary:** Values inherited unchanged from Role, Runtime, or shared defaults are referenced rather than copied into the Agent Instance Definition.

<br>

## 2. Agent Instance and Role remain separate

**Rule:** An Agent Instance Definition states who executes; an Agent Role states the responsibility executed. Every Agent Instance maps to at least one declared Role, and assigning a Role never transfers ownership of the Role contract into the Agent Instance.

**Why:** Several Agent Instances may realize the same Role differently, and one Agent Instance identity may be reconfigured without changing the responsibility itself.

**Boundary:** One Agent Instance may coordinate several Roles only when its assigned primary Role explicitly owns coordination of the complete outcome.

<br>

## 3. `general` is the General Agent Instance

**Rule:** The Agent Profile requires one General Agent Instance with the stable identity `general`. It realizes the primary execution Role, remains accountable to the Human, activates applicable capabilities, delegates bounded work when useful, integrates delegated evidence, and makes the final outcome claim.

**Why:** Every request needs one concrete accountable Agent Instance even when several Specialized Agent Instances contribute.

**Boundary:** General Agent Instance accountability never broadens request scope, Permission, or Component authority.

<br>

## 4. Specialized Agent Instances remain bounded

**Rule:** Every Specialized Agent Instance maps to a declared supporting Role and receives only the Context, Skills, Tools, Permission, and lifecycle behavior required for that Role. It returns its result and evidence to the accountable General Agent Instance or direct invoker without expanding its own assignment.

**Why:** Multiple Agent Instances improve focus only when their responsibilities and capabilities remain inspectable and limited.

**Boundary:** A Specialized Agent Instance may use professional judgment inside its assigned Role but never becomes the General Agent Instance by delegation.

<br>

## 5. Agent Native and Instance availability are proven in the selected Runtime

**Rule:** The Agent Native is available only when the selected Runtime exposes its core operational Agent. A required Agent Instance is available only when that Agent Native can instantiate or expose its native realization, assign its declared Role and capabilities, and successfully invoke it in the current project. A declaration or native file alone is not proof.

**Why:** Coordination cannot safely depend on an Agent Native or Agent Instance that exists only nominally.

**Boundary:** An incompatible or unavailable Agent Native or Agent Instance is reported explicitly and never approximated with broader authority.

<br>

## At a Glance

- **Must** — select one Agent Native supplied by the selected Agent Runtime *(1, 5)*
- **Must** — give every required Agent Instance one complete and stable Agent Instance Definition *(1)*
- **Never** — let the Agent Native change the contracts referenced by an Agent Instance Definition *(1)*
- **Must** — map every Agent Instance to a declared Role while keeping Instance identity and Role responsibility separate *(2)*
- **Must** — provide `general` as the General Agent Instance accountable for the complete authorized outcome *(3)*
- **Never** — let General Agent Instance accountability broaden scope, Permission, or authority *(3)*
- **Must** — keep every Specialized Agent Instance bounded to its supporting Role and required capabilities *(4)*
- **Never** — let delegation turn a Specialized Agent Instance into the General Agent Instance *(4)*
- **Must** — prove the Agent Native and every required Agent Instance are usable in the selected Runtime *(5)*
- **Never** — approximate an unavailable Agent Native or Agent Instance with broader authority *(5)*
