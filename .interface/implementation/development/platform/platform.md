# Platform Definition

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[Platform remains separate from developed Components](#platform-remains-separate-from-developed-components)**
   - **[Every Launch Item is one coherent selectable definition](#every-launch-item-is-one-coherent-selectable-definition)**
   - **[Each Launch Item declares Component Runtime Requirements](#each-launch-item-declares-component-runtime-requirements)**
   - **[Component Runtime Requirements are explicit and scoped](#component-runtime-requirements-are-explicit-and-scoped)**
   - **[Launch delivers required Bindings safely](#launch-delivers-required-bindings-safely)**
   - **[Launch reports only verified Access Points](#launch-reports-only-verified-access-points)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Platform defines named Launch Items that describe how a completed Target is prepared and brought online. Each Launch Item keeps the runtime requirements for its applicable Components together so the complete launch method can be selected as one coherent definition.

Platform owns runtime preparation and operation rather than the internal meaning or implementation of a developed Component. It uses each Component only through its public boundary.

<br>

### Purpose

Software that has been built still has to be brought online: something must decide where each part runs, what it needs in order to start, what values it is given at runtime, and whether it is actually up. Those decisions belong to no Component in particular — each one knows what it needs, none of them knows how the whole is operated — and a project that leaves them implicit ends up with a system only one person can launch, on one machine, from memory.

Platform exists to hold them as named, selectable definitions. A Launch Item keeps the whole method of bringing a Target online in one place: which Components it applies to, what each requires at runtime, what bindings are delivered to them, and what counts as a verified access point. Choosing a Launch Item chooses the complete launch method rather than assembling it again from parts.

Keeping it separate from the Components is the point. Platform reaches every Component only through its public boundary, so the way something is operated can change — a different destination, a different set of runtime values — without reaching into what that Component is or how it was built.

### How It Works

A Launch Item is the unit Platform works in. It names one complete way of preparing and operating a Target, and it is selected as a whole: choosing it chooses the runtime destination, the requirements, and the delivery method together, rather than combining independent fragments that were never checked against one another.

Inside it, each applicable Component has its Component Runtime Requirements: where that Component runs and the operational values it needs in order to start. They are stated explicitly and scoped to the Component they belong to, so nothing inherits a value by accident and nothing needs a value it never declared.

At launch, Platform prepares what the selected Launch Item declares and delivers the required Bindings to each Component's boundary — the runtime values a Component's own configuration contract asks for, handed across without being published to other layers and without secrets travelling further than they must.

When the parts are running, Platform reports Access Points, and only the ones it has verified. A part that has started is not the same as a part that is reachable, and reporting the second requires observing it.

<br>

## Terms

- **Launch Item** — one named, selectable definition for preparing and operating a completed Target.
- **Component Runtime Requirements** — the runtime destination and operational values required to run one developed Component.
- **Binding** — a runtime value one Component needs to reach another, such as an address, port, credential reference, or shared secret reference.
- **Access Point** — a verified address through which a human or another system can reach the launched Target.

<br>

## Relationships

- **Consumes Development** — uses the declared Components, Connections, and public boundaries of the composed application.
- **Consumed by Development** — provides named Platform definitions that Development may reference without copying their contents.

<br>

Named Launch Items and their Component Runtime Requirements belong to Platform Preferences. Implementation applies the selected Launch Item to the current Target without writing the resolved result back into Preferences.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory.

<br>

### Platform remains separate from developed Components

**Rule:** Platform prepares and operates developed Components only through their public boundaries. Every developed Component retains ownership of its internal logic, data, presentation, source organization, and Runtime Configuration contract.

**Why:** Runtime operation and application implementation change for different reasons and remain independently replaceable.

**Boundary:** Platform may supply documented runtime inputs but never redefines a developed Component or directly depends on its private implementation.

<br>

### Every Launch Item is one coherent selectable definition

**Rule:** Every supported launch method is represented by one uniquely named Launch Item in Platform Preferences. One Launch Item is selected as the default when the Target does not explicitly select another compatible item.

**Why:** A complete named definition can be selected or replaced without combining unrelated fragments implicitly.

**Boundary:** Selecting a Launch Item does not authorize applying incompatible runtime requirements to the Target.

<br>

### Each Launch Item declares Component Runtime Requirements

**Rule:** Each Launch Item declares runtime requirements directly under each applicable Component. A Component requirement may include its operating system, transport, web server, bindings, and other values required to operate that Component.

**Why:** Keeping the destination with its launch method prevents an invalid combination of independently selected operational definitions.

**Boundary:** Component Runtime Requirements never redefine a Component's internal implementation or behavior.

<br>

### Component Runtime Requirements are explicit and scoped

**Rule:** A Launch Item groups runtime requirements by the Component they operate. Each requirement declares only the values needed to operate its named Component and may remain empty when no requirement exists for that Component.

**Why:** Explicit Component-scoped requirements make runtime configuration reviewable and prevent one Component's settings from being mixed with another's.

**Boundary:** Requirements never define application behavior, change a Component's private implementation, or imply an action that is not declared.

<br>

### Launch delivers required Bindings safely

**Rule:** The selected Launch Item defines every Binding required by the composed Components and delivers each Binding to the public boundary that consumes it. Secret values remain in appropriate secret sources.

**Why:** Launch sees the operational composition and can connect independently owned Components without transferring configuration ownership.

**Boundary:** Launch does not define how a Component internally reads, stores, or validates a Binding, and no secret value is recorded in Interface files or documentation.

<br>

### Launch reports only verified Access Points

**Rule:** The selected Launch Item verifies the composed Target and reports every usable Access Point exposed by the running result.

**Why:** Starting processes is not a complete operational result unless the Target is reachable and its entry points are known.

**Boundary:** Only verified addresses are reported as available, and an Access Point never exposes credentials or secret values.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Platform remains separate from developed Components**

- **Must** — Operate every developed Component only through its public boundary while the Component retains ownership of its internals and Runtime Configuration contract.
- **Never** — Let Platform redefine a developed Component or directly depend on its private implementation.

**Every Launch Item is one coherent selectable definition**

- **Must** — Represent every supported launch method as one uniquely named Launch Item and select one default.
- **Never** — Apply runtime requirements that are incompatible with the selected Launch Item or Target.

**Each Launch Item declares Component Runtime Requirements**

- **Must** — Declare runtime requirements directly under each applicable Component.
- **Never** — Define operational values outside the owning Component's requirement block.

**Component Runtime Requirements are explicit and scoped**

- **Must** — Group runtime requirements by Component scope and explicitly declare required values.
- **Must** — Allow a Component requirement block to remain empty when its scope requires no values.
- **Never** — Let a runtime requirement define application behavior, modify private implementation, or imply an undeclared action.

**Launch delivers required Bindings safely**

- **Must** — Define and deliver every required Binding to its consuming public boundary while keeping secret values in secret sources.
- **Never** — Redefine a Component's internal Binding handling or record a secret value in Interface files or documentation.

**Launch reports only verified Access Points**

- **Must** — Verify the composed Target and report every usable Access Point.
- **Never** — Report an unverified address as available or expose a credential or secret through an Access Point.
