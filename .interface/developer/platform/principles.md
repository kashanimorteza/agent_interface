# Platform Principles

Platform defines the operational Environment in which a Target runs and the Launch method that brings its developed parts online. Platform is separate from Development: Development builds the parts, while Platform describes runtime preparation and operation without redefining their internal responsibilities.

Platform has two primary concepts: Environment and Launch. Each concept may provide multiple named definitions and one selected default.

## Terms

- **Platform** — the operational boundary that prepares a runtime destination and brings the completed Target online.
- **Environment** — a named runtime destination and the requirements needed to prepare it for the Target.
- **Launch** — a named method for starting, connecting, and operating the completed parts of the Target on an Environment.
- **Binding** — a runtime value one part needs in order to reach another, such as an address, port, credential, or shared secret.
- **Access Point** — a verified address through which a human or another system can reach the launched Target, such as its website, API, or API documentation.

## Relationships

- **Consumes developed parts** — uses independently developed parts only through their public boundaries.
- **Consumed by Configure** — Configure resolves and prepares the selected Environment.
- **Consumed by Launch** — Launch applies the selected Launch method and reports its observable result.

Technical choices and defaults for Platform belong to Platform Preferences. Platform implementation applies those choices to the current Target.

Every statement here is mandatory. A Preference can never override a Principle, and a Target may only add stricter rules, never looser ones.

<br>

## 1. Platform is separate from Development

**Rule:** Platform owns Environment and Launch definitions; Development owns the design and implementation of application parts.

**Why:** Runtime preparation and application construction change for different reasons and must remain independently replaceable.

**Boundary:** Platform operates developed parts only through their public boundaries and never owns or redefines their internal logic, data, presentation, or source arrangement.

<br>

## 2. Environment defines runtime preparation

**Rule:** An Environment defines a runtime destination and the system-level requirements needed to prepare it, including its type, required tools, packages, services, and settings.

**Why:** Different runtime destinations require different preparation while the developed Target remains unchanged.

**Boundary:** Multiple Environment definitions may exist, but Platform selects one default when the Target does not explicitly select another.

<br>

## 3. Launch defines runtime composition

**Rule:** A Launch defines how completed parts are started, connected, and operated together on the selected Environment.

**Why:** Preparing a runtime destination and running a composed system are separate responsibilities that may vary independently.

**Boundary:** Multiple Launch definitions may exist, but Platform selects one default when the Target does not explicitly select another. A Launch does not redefine how any part is developed.

<br>

## 4. Environment and Launch remain independently selectable

**Rule:** Environment and Launch definitions are selected independently, and their selected combination must be compatible.

**Why:** The same Target may use different launch methods on the same environment or the same launch method across compatible environments.

**Boundary:** An incompatible selection must not be applied as if it were runnable.

<br>

## 5. Launch delivers the bindings between parts

**Rule:** The selected Launch defines every Binding the composed parts require and delivers each one to the boundary that consumes it.

**Why:** Each part owns its own settings, but no part can own a value that two parts must agree on; the launch is the only step that sees both sides of the connection.

**Boundary:** Launch delivers Bindings; it does not define how a part reads, stores, or validates them, and no secret value is recorded in the Target definition or in any Config.

<br>

## 6. Launch reports verified access

**Rule:** A Launch verifies the composed Target and reports every usable Access Point that the running result exposes.

**Why:** Starting processes is not a complete operational result unless the Target is reachable and its entry points are known.

**Boundary:** Only verified addresses are reported as available. Credentials and secret values are never included in Access Points.

<br>

## At a Glance

- **Must** — keep Platform separate from Development and operate parts through public boundaries *(1)*
- **Must** — prepare the selected Environment and apply the selected Launch *(2–3)*
- **Must** — support named alternatives and explicit defaults *(2–3)*
- **Must** — keep Environment and Launch independently selectable and compatible *(4)*
- **Never** — redefine the internal responsibilities of developed parts *(1, 3)*
- **Must** — the selected Launch delivers every Binding to the boundary that consumes it *(5)*
- **Never** — a secret value is recorded in the Target definition or in any Config *(5)*
- **Must** — verify and report every usable Access Point without exposing secrets *(6)*
