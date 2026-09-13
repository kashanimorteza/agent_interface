# Platform Principles

Platform defines named Launch Items that describe how a completed Target is prepared and brought online. Each Launch Item keeps its Environment and operational Instructions together so the complete launch method can be selected as one coherent definition.

Platform owns runtime preparation and operation rather than the internal meaning or implementation of a developed Component. It uses each Component only through its public boundary.

<br>

## Terms

- **Launch Item** — one named, selectable definition for preparing and operating a completed Target.
- **Environment** — the runtime destination described inside a Launch Item.
- **Instructions** — the scoped operational changes and actions belonging to a Launch Item.
- **Operating System Instructions** — Instructions that prepare the Environment's operating system, including required package installation or removal.
- **Component Instructions** — Instructions scoped to operating one developed Component without redefining that Component's internals.
- **Binding** — a runtime value one Component needs to reach another, such as an address, port, credential reference, or shared secret reference.
- **Access Point** — a verified address through which a human or another system can reach the launched Target.

<br>

## Relationships

- **Consumes Development** — uses the declared Components, Connections, and public boundaries of the composed application.
- **Consumed by Development** — provides named Platform definitions that Development may reference without copying their contents.

<br>

Named Launch Items, their Environment values, and their Instructions belong to Platform Preferences. Implementation applies the selected Launch Item to the current Target without writing the resolved result back into Preferences.

<br>

Every statement here is mandatory. A Developer Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Platform remains separate from developed Components

**Rule:** Platform prepares and operates developed Components only through their public boundaries. Every developed Component retains ownership of its internal logic, data, presentation, source organization, and Runtime Configuration contract.

**Why:** Runtime operation and application implementation change for different reasons and remain independently replaceable.

**Boundary:** Platform may supply documented runtime inputs but never redefines a developed Component or directly depends on its private implementation.

<br>

## 2. Every Launch Item is one coherent selectable definition

**Rule:** Every supported launch method is represented by one uniquely named Launch Item in Platform Preferences. One Launch Item is selected as the default when the Target does not explicitly select another compatible item.

**Why:** A complete named definition can be selected or replaced without combining unrelated fragments implicitly.

**Boundary:** Selecting a Launch Item does not authorize applying an incompatible Environment or instruction to the Target.

<br>

## 3. Each Launch Item owns its Environment

**Rule:** Each Launch Item contains exactly one Environment describing the runtime destination to which that Launch Item's Instructions apply. The Environment is resolved as part of the Launch Item rather than selected independently from it.

**Why:** Keeping the destination with its launch method prevents an invalid combination of independently selected operational definitions.

**Boundary:** Environment describes the runtime destination; operational changes to that destination belong to Instructions.

<br>

## 4. Launch Instructions are explicit and scoped

**Rule:** A Launch Item groups Instructions by the boundary they operate. Operating System Instructions declare system packages that must be installed or removed. Component Instructions declare only the actions needed to operate their named Components. An instruction group may remain empty when that Launch Item requires no action for the scope.

**Why:** Explicit scoped Instructions make runtime changes reviewable and prevent operating-system work from being mixed with Component operation.

**Boundary:** Instructions never define application behavior, change a Component's private implementation, or imply an action that is not declared.

<br>

## 5. Launch delivers required Bindings safely

**Rule:** The selected Launch Item defines every Binding required by the composed Components and delivers each Binding to the public boundary that consumes it. Secret values remain in appropriate secret sources.

**Why:** Launch sees the operational composition and can connect independently owned Components without transferring configuration ownership.

**Boundary:** Launch does not define how a Component internally reads, stores, or validates a Binding, and no secret value is recorded in Interface files or documentation.

<br>

## 6. Launch reports only verified Access Points

**Rule:** The selected Launch Item verifies the composed Target and reports every usable Access Point exposed by the running result.

**Why:** Starting processes is not a complete operational result unless the Target is reachable and its entry points are known.

**Boundary:** Only verified addresses are reported as available, and an Access Point never exposes credentials or secret values.

<br>

## At a Glance

- **Must** — Operate every developed Component only through its public boundary while the Component retains ownership of its internals and Runtime Configuration contract. *(1)*
- **Never** — Let Platform redefine a developed Component or directly depend on its private implementation. *(1)*
- **Must** — Represent every supported launch method as one uniquely named Launch Item and select one default. *(2)*
- **Never** — Apply an Environment or instruction that is incompatible with the selected Launch Item or Target. *(2)*
- **Must** — Keep exactly one Environment inside each Launch Item and resolve it as part of that item. *(3)*
- **Never** — Put operational Environment changes outside the Launch Item's Instructions. *(3)*
- **Must** — Group Instructions by operating-system or Component scope and explicitly declare required actions. *(4)*
- **Must** — Allow an instruction group to remain empty when its scope requires no action. *(4)*
- **Never** — Let an Instruction define application behavior, modify private implementation, or imply an undeclared action. *(4)*
- **Must** — Define and deliver every required Binding to its consuming public boundary while keeping secret values in secret sources. *(5)*
- **Never** — Redefine a Component's internal Binding handling or record a secret value in Interface files or documentation. *(5)*
- **Must** — Verify the composed Target and report every usable Access Point. *(6)*
- **Never** — Report an unverified address as available or expose a credential or secret through an Access Point. *(6)*
