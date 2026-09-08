# Platform Principles

Platform is the Component that composes the independent application layers into one runnable system and keeps it runnable wherever it is meant to run. It owns the operating environment, the coordination between layers, the startup path, the networking between them, the delivery of each layer's configuration, and the deployment of the whole; it is also the resolved place the target runs, whether that is a development machine, a server, a container, or a cloud.

Platform owns composition and the environment around the layers. It does not own the application behaviour, presentation, or persistence of any layer it composes, and it never reaches inside one to change how it works.

## Terms

- **Composition** — the connection of independent layers into one system through their declared interfaces, together with everything that makes them run side by side.
- **Operating Environment** — the resolved place the target runs and everything the layers need in order to run there.
- **Binding** — a cross-layer choice that belongs to no single layer, such as which Database Instance a Backend consumes.
- **Runtime Configuration** — the settings a user or operating environment may change; each layer owns its own, and Platform coordinates their loading, validation, and delivery.
- **Secret** — a value that must stay out of general configuration, source control, and distributable artifacts; it is owned by the layer it belongs to and resolved only for that boundary.
- **Deployment** — bringing the composed system online at its destination.

## Relationships

- **Consumes Development** — the layered architecture, the declared interfaces, and the connections Platform composes.
- **Consumed by Model, Database, Backend, and Frontend** — the operating environment, the delivery of each layer's own configuration, and the bindings that connect them.

Technical choices and defaults belong to Platform Preferences. Platform implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Platform composes the complete system

**Rule:** Platform owns cross-layer composition: the operating environment, process or service coordination, startup, networking, runtime configuration delivery, and deployment of the complete project. Platform connects layers through their declared interfaces.

**Why:** With composition owned in one place, the system may run on any suitable operating system, local environment, server, container platform, cloud platform, or future destination without changing the ownership of another layer.

**Boundary:** Platform never absorbs the application, presentation, or persistence responsibilities of the layers it composes.

<br>

## 2. Each layer owns its settings and secrets; Platform owns composition

**Rule:** Configuration that a user or operating environment may change remains separate from implementation code. Each application layer owns its settings and a private area for its own secrets within its boundary. Secret values remain separate from general configuration and excluded from source control and distributable artifacts. Platform coordinates loading, validation, environment overrides, and delivery without merging the layers' secrets into a shared store. Each layer receives only its own declared settings and secrets and the references needed for its connections. Cross-layer choices, such as the Database Instance assigned to Backend, remain composition settings owned by Platform. General configuration may reference a secret by name, but its value is resolved only for the owning boundary. Frontend secrets may be used only by trusted build or server processes; browser-delivered code and assets never contain secret values.

**Why:** Keeping settings and secrets with their owning layer preserves its independence, while explicit composition settings allow connections to change without editing implementation code.

**Boundary:** A package never reads another package's configuration section, discovers another package's internals, or changes source code merely to select a different compatible provider or Instance. The concrete configuration files, formats, section names, override precedence, and delivery mechanism are technical choices resolved from the project definition and Development Preferences, then implemented by Platform.

<br>

## 3. Platform is realized with every phase, not after them

**Rule:** Platform has no phase of its own. Each phase that delivers a layer also delivers that layer's part of the composition: its own runtime settings and private secret area as needed, its declared cross-layer bindings, the process or service that runs it when applicable, and its declared connections to the layers already present. The layers delivered so far are usable together after every phase. An importable layer demonstrates use through its public interface and does not require a separate service merely to satisfy this rule.

**Why:** A composition assembled only at the end is assembled against layers that were never run together, and every integration problem surfaces at once at the point where it is most expensive. Composing as each layer arrives keeps the running system one step behind the plan at most.

**Boundary:** This decides when composition happens, not who owns it. Platform still owns the composition and each layer still owns its own implementation; a phase contributes its layer's part under Platform's rules and does not restructure what earlier phases composed. Where the target project runs — a host, a container, a cloud — is a technical choice resolved from the project definition and Development Preferences, and a phase composes for that choice rather than deciding it.

<br>

## At a Glance

- **Must** — Platform owns environment, coordination, startup, networking, configuration delivery, and deployment *(1)*
- **Never** — Platform absorbs the application, presentation, or persistence responsibilities of a layer *(1)*
- **Must** — each layer owns its settings and private secret area within its boundary; Platform owns cross-layer bindings and coordinates validation and delivery of only that layer's declared configuration *(2)*
- **Never** — layers' secrets are merged into a shared store or included in general configuration, source control, distributable artifacts, or browser-delivered code and assets *(2)*
- **Never** — a package reads another package's configuration section or changes source code to select a compatible provider or Instance *(2)*
- **Must** — every phase that delivers a layer also delivers that layer's part of the composition, so the system is runnable after every phase *(3)*
- **Never** — Platform is left to a phase of its own, or a phase restructures what earlier phases composed *(3)*
