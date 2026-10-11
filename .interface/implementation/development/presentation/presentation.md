# Presentation Definition

Presentation is the Development Component that renders the user experience and consumes application capabilities through API.

<br>

<!--------------------------------------------------------------------------------- Navigation --->
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Authority](#authority)**
7. **[Principles](#principles)**
8. **[At a Glance](#at-a-glance)**

<br>

<!--------------------------------------------------------------------------------- Introduction --->
## Introduction

### Overview

Presentation is the Component that presents the application to users, manages user interaction, and consumes the capabilities published by API. It is where the project becomes something a person can see and act on, and it keeps that experience coherent by resolving its appearance and its interface behavior once rather than page by page. It presents every Group API serves as an Area, so that, for example, a user can list, filter, order, add, edit, and delete the records of every Entity. Its architecture is independent of any language, library, framework, package manager, API protocol, or project.

### Purpose

Decisions about appearance and interface behavior are made once and reused everywhere, so the interface stays coherent as it grows. Presentation reaches the application only through API, so domain meaning and application rules are never decided a second time in the interface.

### How It Works

A user sees pages and views composed from reusable Components; Interaction Logic behind them owns the interface's behavior; API Access is the single door through which every piece of application data enters and leaves; and the Theme resolves appearance for all of it. Together they build one Area for every API Group, with one Section for every Adapter.

<br>

<!--------------------------------------------------------------------------------- Terms --->
## Terms

- **Presentation** — the Component that presents the application to users, manages user interaction, and consumes the capabilities published by API.
- **View Layer** — the Presentation layer that renders pages and views by composing reusable user-interface Components.
- **Interaction Logic** — the layer that manages user-interface state, input, interaction flows, and presentation decisions.
- **API Access** — the layer that is the only Presentation boundary consuming the API published by the API Component.
- **Component (user-interface)** — one focused, composable unit of Presentation, reused wherever the same user-interface concept appears.
- **Theme** — the coherent visual system whose colors, typography, spacing, direction, and display mode are resolved once and consumed by every Component.
- **Area** — the part of Presentation that presents one API Group to users.
- **Section** — the part of an Area that presents one Adapter of its Group, with one action for every Endpoint of that Adapter.

<br>

<!--------------------------------------------------------------------------------- Architecture --->
## Architecture

```text
Presentation
├── View Layer
├── Interaction Logic
├── API Access
├── Theme
├── Areas
└── Documentation
```

Every entity below is declared in `architecture` in Presentation Preferences, which also own the language, packages, realization, and documentation choices; these selections realize the responsibilities below without changing them. The dependency direction is View Layer → Interaction Logic → API Access → API Component. No layer bypasses the layer responsible for the next boundary.

Presentation owns rendering, user interaction, API access, and the visual system. Development supplies its technical selections; Presentation Preferences carry its component-owned defaults and conventions. API owns the external contract.

<!-------------------------- View Layer -->
### View Layer

```text
View Layer
├── Pages and views
└── Components
```

The layer that renders pages and views by composing reusable user-interface Components. Each Component is one focused unit responsible for one interface concept: it takes what it needs and renders it, and it does not fetch or decide application rules. A page or view coordinates Components.

<!-------------------------- Interaction Logic -->
### Interaction Logic

The layer behind the View Layer that owns user-interface behavior: interface state, input, form state, selection, navigation intent, loading state, interaction flows, and coordination between Components. It is the only layer that reasons about the interface.

<!-------------------------- API Access -->
### API Access

The single door outwards. It owns the Presentation-side client boundary, request and response transport, and translation between API representations and the data Interaction Logic uses. Its contract source and whether client types are generated from it come from Presentation Preferences.

<!-------------------------- Theme -->
### Theme

```text
Theme
├── Colors
├── Typography
├── Spacing
├── Direction
└── Display mode
```

The one coherent visual system every Component consumes. The selected Theme and its values come from Presentation Preferences.

<!-------------------------- Areas -->
### Areas

```text
Areas
└── Entity Area
```

What Presentation offers its users, organized like API: one Area for every Group API serves, presenting exactly what that Group serves. An Area is built from the layers above: its pages and views in the View Layer, its behavior in Interaction Logic, its calls in API Access, and its appearance from the Theme. Every Area follows the same Area contract:

- **Source** — the API Group it presents, read from API's machine-readable description or, when none is available, from API-owned public definitions and documentation.
- **Sections** — one Section for every Adapter of that Group, named from the Adapter; an Adapter added or removed adds or removes its Section.
- **Actions** — one user action for every Endpoint of the Adapter; an Endpoint that does not exist has no action.
- **Fields** — every form field, list column, Filter, and Order a Section offers comes from the API contract, never listed by hand.
- **Behavior** — every action calls its Endpoint through API Access and presents the result, or the returned error, as API returns it; no action decides an application rule.

Every Section is standalone: it writes its pages and actions out explicitly and shares no generated or dynamic page with another Section, while still composing shared Components and the Theme.

#### Entity Area

The Area of API's Entity Group: one Section for every Entity, through which a user works with that Entity's records. Its actions follow the Endpoints the Entity's Adapter offers:

- **List** — the Entity's records, with Filters on any Field and their combination, ordering by any Field and direction, and a limit.
- **View** — one record by its id.
- **Add** — a form built from the Entity's Fields.
- **Edit** — the same form, filled with the record, saved as an update.
- **Enable, Disable, and Delete** — on one record.
- **Count and aggregates** — wherever the Adapter offers them.

<!-------------------------- Documentation -->
### Documentation

```text
Documentation
├── Overview
├── Setup
├── Use
├── Verify
└── Troubleshooting
```

The root documentation, in the file, location, and format Presentation Preferences name. Its sections, in this order:

1. **Overview** — What Presentation is, in one paragraph, with one screen or flow as an example.
2. **Setup** — How to install and start Presentation, and the API address it needs.
3. **Use** — How the layers fit together, how each Area and Section presents its API Group, where a new page, Component, interaction, or API call belongs, and how the Theme is applied.
4. **Verify** — How to see that every page renders, only API Access calls API, and every Component uses the Theme.
5. **Troubleshooting** — Real problems a user or developer can meet and how to fix them.

<!-------------------------- Directory Structure -->
### Directory Structure

```text
Directory Structure
├── presentation/
│   ├── view/
│   ├── interaction/
│   ├── api/
│   ├── theme/
│   └── areas/
│       └── entity/
└── README
```

The root of this tree is the Component directory; it and the package directory take their names from `settings` in Presentation Preferences. `view/` holds the View Layer, `interaction/` Interaction Logic, `api/` API Access, `theme/` the Theme, and `areas/` every Area in its own directory, with one unit per Section; a directory the selected framework requires is placed as the language profile in Presentation Preferences states, without moving a layer out of its own directory.

<br>

<!--------------------------------------------------------------------------------- Relationships --->
## Relationships

- **Consumes API** — the public API, its Groups, and its machine-readable description when one is available, through which all application data and application capabilities are reached.
- **Consumes Development** — the common package standard and the cross-cutting capabilities selected for the project.

<br>

<!--------------------------------------------------------------------------------- Boundaries --->
## Boundaries

- **Application persistence** — is not Presentation's, because data is stored behind API, not in the interface.
- **Authoritative application behavior and rules** — are not Presentation's, because they have one home behind API; Presentation requests their outcome and presents it.
- **Cross-layer composition** — is not Presentation's, because Presentation owns only its own layers.
- **The external API contract** — is not Presentation's, because API owns it.

<br>

<!--------------------------------------------------------------------------------- Authority --->
## Authority

Presentation Definition Principles are mandatory. Presentation Preferences provide configurable defaults and conventions, while explicit Target meaning and applicable Principles take precedence. Preferences may make a rule stricter but may not weaken it.

<br>

<!--------------------------------------------------------------------------------- Principles --->
## Principles

Every Principle below is mandatory and belongs to the Architecture category that owns it.

### General

#### Presentation has three internal layers

**Rule:** Presentation is formed from three distinct layers:

- **View Layer** renders pages and views by composing reusable user-interface Components;
- **Interaction Logic** manages user-interface state, input, interaction flows, and presentation decisions; and
- **API Access** is the only Presentation boundary that consumes the API published by the API Component.

The dependency direction is View Layer → Interaction Logic → API Access → API Component.
**Why:** Separating what the user sees from how the interface behaves and from how application data is fetched lets any one of the three change without disturbing the other two.
**Boundary:** No layer bypasses the layer immediately responsible for the next boundary.

#### Presentation implements only Presentation-targeted project Behavior

**Rule:** Presentation may implement project Behavior concerned with presentation and user interaction. Presentation determines how that Behavior is exposed to the user, Interaction Logic coordinates its user-facing flow, and API Access consumes the API capability it requires.
**Why:** Behavior that belongs to the user's experience is best expressed where the experience lives, while authoritative behavior has exactly one home.
**Boundary:** When an outcome depends on application rules, Presentation requests that outcome through the API Component and presents the returned result.

#### Presentation preserves its boundary

**Rule:** Presentation owns presentation, user-interface interaction, its API client boundary, and its visual system.
**Why:** A Component that states what it owns can be trusted by the Components around it, and can be replaced without redistributing responsibilities.
**Boundary:** Presentation does not own application persistence, authoritative application Behavior, or cross-layer composition, as Boundaries states. Cross-cutting capabilities selected by Development are consumed through explicit boundaries and do not become additional mandatory Presentation layers.

<br>

### View Layer

#### Presentation is component-based

**Rule:** Presentation is assembled from focused, composable Components rather than monolithic pages or duplicated interface fragments. Reusable Components preserve consistent behavior and appearance wherever the same user-interface concept is needed.
**Why:** One definition per user-interface concept keeps the interface consistent as it grows and keeps a change to that concept in one place.
**Boundary:** A page or view coordinates Components; it does not absorb unrelated interaction or application logic. Project-specific composition may vary without changing this architectural rule.

<br>

### Interaction Logic

#### Interaction Logic owns user-interface behavior

**Rule:** Interaction Logic manages state that exists for the user experience, including user input, form state, selection, navigation intent, loading state, and coordination between Presentation Components. It may perform interaction-level validation and transform resolved data for presentation.
**Why:** Interface state has a different lifetime and a different owner than application state, so keeping it in its own layer prevents the two from being confused for each other.
**Boundary:** It does not implement authoritative application rules or persistence decisions.

<br>

### API Access

#### API Access is the only door to application data

**Rule:** Presentation reaches application data and application capabilities only through the public API implemented by the API Component. API Access owns the Presentation-side client boundary, request and response transport, and translation between API representations and the data used by Interaction Logic. It consumes the resolved API contract and its machine-readable description when one is available.

When a machine-readable description is unavailable, API Access derives its client representations from the current public API definitions and documentation that API owns. Missing documentation does not authorize Presentation to invent endpoints, fields, or response behavior. Any ambiguity that prevents a correct client is reported for the affected integration, while independently defined work may continue.
**Why:** A single door means the application's rules are enforced in one place, and the transport can change without touching how the interface behaves.
**Boundary:** API Access is the only Presentation layer that performs API communication; no other Presentation layer bypasses it. The protocol, client technology, and transport settings are technical choices rather than Presentation philosophy.

<br>

### Theme

#### Appearance is governed by one coherent visual system

**Rule:** Presentation uses a coherent Theme and shared visual rules across its Components. Colors, typography, spacing, direction, display mode, and other visual decisions are resolved once and consumed consistently rather than being independently invented by each page or Component.
**Why:** Resolving appearance once is what makes an interface read as one product, and it makes a change to the visual system take effect everywhere at once.
**Boundary:** The existence and responsibility of this visual system are philosophical. Presentation Preferences resolve the selected Theme and its values; Development resolves styling technology and other shared technical selections.

<br>

### Areas

#### Every API Group has one Area

**Rule:** Presentation has exactly one Area for every Group API serves, with one Section for every Adapter of that Group and one action for every Endpoint of that Adapter. Every field, column, Filter, and Order comes from the API contract.
**Why:** Users reach everything API serves, and Presentation stays in step with API without a second, hand-written copy of its surface.
**Boundary:** An Endpoint that does not exist has no action, and no action is added for anything API does not serve.

#### Every Section writes its own actions

**Rule:** Every Section writes its pages and actions out explicitly in its own unit. No Section is produced by a generic page, a loop, or any dynamic mechanism, and no Section inherits from another.
**Why:** Each Entity's interface can be read, extended, or reduced on its own without touching any other.
**Boundary:** Sections still compose shared Components and the Theme; only what is specific to a Section stays inside it.

<br>

### Review

#### Presentation conformance covers every Presentation contract

**Rule:** Presentation is conformant only when its real output shows every layer and Area Architecture names with the responsibility stated there, and every observation below holds.
**Why:** A gap here lets an interface that bypasses API or breaks its own consistency look complete.
**Boundary:** Review reads API's published contract only to compare; it changes nothing outside Presentation.

#### Review observes Presentation through a fixed set of checks

**Rule:** Review establishes Presentation conformance through these observations, every one of them on every review:

- The output has the View Layer, Interaction Logic, API Access, Theme, and Areas, each in its own directory, with the dependency direction View Layer → Interaction Logic → API Access → API Component.
- No layer other than API Access communicates with API, and no layer bypasses the layer responsible for the next boundary.
- Every page or view is composed from reusable Components, and the same interface concept is one Component wherever it appears.
- No Component fetches data or decides an application rule.
- Interaction Logic implements no authoritative application rule or persistence decision.
- API Access uses only Endpoints, fields, and behavior the API contract publishes, and invents none.
- Every visual decision comes from the selected Theme; no page or Component invents its own.
- There is one Area for every API Group, one Section for every Adapter, and one action for every Endpoint, with no action for anything API does not serve.
- Every field, column, Filter, and Order a Section offers comes from the API contract.
- Every Section is written out explicitly in its own unit, with no generated page and no inheritance between Sections.
- Documentation has its sections in order.

**Why:** A fixed set of observations proves the same things on every review, so a result is never judged by a different standard from one run to the next.
**Boundary:** Each observation states what is seen, never the command, tool, or code that observes it; how it is realized belongs to the Review Operation.

<br>

<!--------------------------------------------------------------------------------- At a Glance --->
## At a Glance

Every obligation in the file, under the Principle it comes from.

### General

**Presentation has three internal layers**

- **Must** — Form Presentation from View Layer, Interaction Logic, and API Access, in that dependency direction.
- **Never** — Let a layer bypass the layer immediately responsible for the next boundary.

**Presentation implements only Presentation-targeted project Behavior**

- **Must** — Request an outcome that depends on application rules through API and present it as returned.

**Presentation preserves its boundary**

- **Never** — Own persistence, authoritative behavior, or cross-layer composition.
- **Never** — Turn a cross-cutting capability into an additional mandatory Presentation layer.

<br>

### View Layer

**Presentation is component-based**

- **Must** — Assemble Presentation from focused, composable, reusable Components.
- **Never** — Let a page or view absorb unrelated interaction or application logic.

<br>

### Interaction Logic

**Interaction Logic owns user-interface behavior**

- **Must** — Keep user-interface state, input, flows, and coordination between Components in Interaction Logic.
- **Never** — Implement authoritative application rules or persistence decisions in Interaction Logic.

<br>

### API Access

**API Access is the only door to application data**

- **Must** — Reach application data and capabilities only through the public API, through API Access.
- **Must** — Derive client representations from API-owned public definitions and documentation when a machine-readable API description is unavailable, and report unresolved integration ambiguities without inventing API behavior.
- **Never** — Let a layer other than API Access perform API communication or bypass API Access.

<br>

### Theme

**Appearance is governed by one coherent visual system**

- **Must** — Resolve appearance once as one coherent Theme and consume it consistently.
- **Never** — Let a page or Component invent its own visual decisions.

<br>

### Areas

**Every API Group has one Area**

- **Must** — Give every API Group one Area, every Adapter one Section, and every Endpoint one action, with fields from the API contract.
- **Never** — Add an action for anything API does not serve, or list fields by hand.

**Every Section writes its own actions**

- **Must** — Write every Section's pages and actions out explicitly in its own unit.
- **Never** — Produce a Section by a generic page, loop, or dynamic mechanism, or let one Section inherit from another.

<br>

### Review

**Presentation conformance covers every Presentation contract**

- **Must** — show every layer with its responsibility and every observation holding before Presentation is conformant.
- **Never** — change anything outside Presentation during review.

**Review observes Presentation through a fixed set of checks**

- **Must** — make every listed observation on every review.
- **Never** — replace an observation with a command, tool, or code, or judge by a different set.
