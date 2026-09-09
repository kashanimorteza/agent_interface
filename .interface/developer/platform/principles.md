# Platform Principles

Platform defines how a completed Target is prepared for operation and brought online. It begins after the required parts have been designed and developed, and it does not redefine their internal responsibilities.

Platform has two primary concepts: Instance and Launch. Each concept may provide multiple named definitions and one selected default.

## Terms

- **Platform** — the operational boundary that prepares a runtime destination and brings the completed Target online.
- **Instance** — a named runtime environment and the requirements needed to prepare it for the Target.
- **Launch** — a named method for starting, connecting, and operating the completed parts of the Target on an Instance.

## Relationships

- **Consumes Development** — receives the independently developed parts and their public boundaries.
- **Prepares an Instance** — establishes the environment required to run the Target.
- **Applies a Launch** — starts and connects the completed parts through a selected launch method.

Technical choices and defaults for Platform belong to Platform Preferences. Platform implementation applies those choices to the current Target.

Every statement here is mandatory. A Preference can never override a Principle, and a Target may only add stricter rules, never looser ones.

<br>

## 1. Platform operationalizes the completed Target

**Rule:** Platform prepares the runtime destination and brings the completed Target online through the public boundaries of its completed parts.

**Why:** Development defines and builds the parts, while Platform turns those parts into an operable system.

**Boundary:** Platform does not own or redefine the internal logic, data, or presentation responsibilities of the parts it operates.

<br>

## 2. Instance defines environment preparation

**Rule:** An Instance defines a runtime environment and the system-level requirements needed to prepare it, including its environment type, required tools, packages, services, and settings.

**Why:** Different runtime destinations require different preparation while the developed Target remains unchanged.

**Boundary:** Multiple Instance definitions may exist, but Platform selects one default when the Target does not explicitly select another.

<br>

## 3. Launch defines runtime composition

**Rule:** A Launch defines how completed parts are started, connected, and operated together on the selected Instance.

**Why:** Preparing an environment and running a composed system are separate responsibilities that may vary independently.

**Boundary:** Multiple Launch definitions may exist, but Platform selects one default when the Target does not explicitly select another. A Launch does not redefine how any part is developed.

<br>

## 4. Instance and Launch remain independently selectable

**Rule:** Instance and Launch definitions are selected independently, and their selected combination must be compatible.

**Why:** The same Target may use different launch methods on the same environment or the same launch method across compatible environments.

**Boundary:** An incompatible selection must not be applied as if it were runnable.

<br>

## At a Glance

- **Must** — prepare the selected Instance and apply the selected Launch *(1–3)*
- **Must** — support named alternatives and explicit defaults *(2–3)*
- **Must** — keep Instance and Launch independently selectable and compatible *(4)*
- **Never** — redefine the internal responsibilities of developed parts *(1, 3)*
