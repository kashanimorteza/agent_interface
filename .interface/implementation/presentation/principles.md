# Presentation Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Terms](#terms)**
3. **[Relationships](#relationships)**
4. **[Principles](#principles)**
   - **[1. Presentation has three internal layers](#1-presentation-has-three-internal-layers)**
   - **[2. Presentation is component-based](#2-presentation-is-component-based)**
   - **[3. Interaction Logic owns user-interface behaviour](#3-interaction-logic-owns-user-interface-behaviour)**
   - **[4. API Access is the only door to application data](#4-api-access-is-the-only-door-to-application-data)**
   - **[5. Domain Models are shared, never copied](#5-domain-models-are-shared-never-copied)**
   - **[6. Presentation implements only Presentation-targeted project Behaviour](#6-presentation-implements-only-presentation-targeted-project-behaviour)**
   - **[7. Appearance is governed by one coherent visual system](#7-appearance-is-governed-by-one-coherent-visual-system)**
   - **[8. Presentation preserves its boundary](#8-presentation-preserves-its-boundary)**
5. **[At a Glance](#at-a-glance)**

<br>

## Introduction

### Overview

Presentation is the Component that presents the application to users, manages user interaction, and consumes the capabilities published by API. It is where the project becomes something a person can see and act on, and it keeps that experience coherent by resolving its appearance and its interface behaviour once rather than page by page. Its architecture is independent of any language, library, framework, package manager, API protocol, or project.

### Purpose

Software that people use is judged by what they see, and what they see is assembled from hundreds of small decisions — a spacing, a colour, a label, what happens after a click. Made page by page, those decisions never agree: the same button looks different in two places, the same action behaves differently, and changing any of it means finding every copy.

Presentation exists to make those decisions once and reuse them. The visual system is resolved in one place and consumed everywhere; a user-interface concept is built once as a Component and appears wherever it is needed; interaction behaviour lives in one layer rather than scattered through views. That is what keeps an interface coherent as it grows, rather than coherent only on the day it was designed.

Its second reason is the boundary beneath it. Presentation reaches the application only through the API, which keeps it from becoming a second place where domain meaning and application rules are decided. Without that, validation gets reimplemented in forms, rules migrate into screens, and the same rule quietly disagrees with itself depending on whether the user or the server applied it.

### How It Works

What a user sees is composed from user-interface Components: focused, reusable units, each responsible for one interface concept, assembled into pages and views. A Component takes what it needs and renders it; it does not fetch, and it does not decide application rules.

Interaction Logic sits behind them and owns behaviour: interface state, input, interaction flows, what happens when something is chosen or submitted, what the user is shown while waiting. It is the only layer that reasons about the interface, which is what keeps views declarative and repeatable.

API Access is the single door outwards. Every piece of application data enters and leaves through it, using the capabilities API publishes, so Presentation has exactly one dependency on the running system and one place to change when that system changes. Domain Definitions are imported from Model rather than restated, so the shapes on screen are the shapes the application agrees on.

The Theme resolves appearance for all of it — colours, typography, spacing, direction, display mode — in one coherent system that every Component consumes rather than each deciding for itself.

<br>

## Terms

- **Presentation** — the layer that renders pages and views by composing reusable user-interface Components.
- **Interaction Logic** — the layer that manages user-interface state, input, interaction flows, and presentation decisions.
- **API Access** — the layer that is the only Presentation boundary consuming the API published by the API Component.
- **Component (user-interface)** — one focused, composable unit of Presentation, reused wherever the same user-interface concept appears.
- **Theme** — the coherent visual system whose colours, typography, spacing, direction, and display mode are resolved once and consumed by every Component.

## Relationships

- **Consumes API** — the public API through which all application data and application capabilities are reached.
- **Consumes Development** — the common package standard and the cross-cutting capabilities selected for the project.
- **Consumed by no other Component** — Presentation is an outermost layer, and nothing in the architecture depends on it.

Technical choices and defaults belong to Presentation Preferences. Presentation implementation applies those choices to the current project definition.

Every statement here is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

<br>

## Principles

Every Principle below is mandatory, and its number is permanent.

<br>

### 1. Presentation has three internal layers

**Rule:** Presentation is formed from three distinct layers:

- **Presentation** renders pages and views by composing reusable user-interface Components;
- **Interaction Logic** manages user-interface state, input, interaction flows, and presentation decisions; and
- **API Access** is the only Presentation boundary that consumes the API published by the API Component.

The dependency direction is Presentation → Interaction Logic → API Access → API Component.

**Why:** Separating what the user sees from how the interface behaves and from how application data is fetched lets any one of the three change without disturbing the other two.

**Boundary:** No layer bypasses the layer immediately responsible for the next boundary.

<br>

### 2. Presentation is component-based

**Rule:** Presentation is assembled from focused, composable Components rather than monolithic pages or duplicated interface fragments. Reusable Components preserve consistent behaviour and appearance wherever the same user-interface concept is needed.

**Why:** One definition per user-interface concept keeps the interface consistent as it grows and keeps a change to that concept in one place.

**Boundary:** A page or view coordinates Components; it does not absorb unrelated interaction or application logic. Project-specific composition may vary without changing this architectural rule.

<br>

### 3. Interaction Logic owns user-interface behaviour

**Rule:** Interaction Logic manages state that exists for the user experience, including user input, form state, selection, navigation intent, loading state, and coordination between Presentation Components. It may perform interaction-level validation and transform resolved data for presentation.

**Why:** Interface state has a different lifetime and a different owner than application state, so keeping it in its own layer prevents the two from being confused for each other.

**Boundary:** It does not implement authoritative application rules or persistence decisions. Application Behaviour and Model-specific business logic remain owned by Logic.

<br>

### 4. API Access is the only door to application data

**Rule:** Presentation reaches application data and application capabilities only through the public API implemented by the API Component. API Access owns the Presentation-side client boundary, request and response transport, and translation between API representations and the data used by Interaction Logic. It consumes the resolved API contract and its machine-readable description when one is available.

When a machine-readable description is unavailable, API Access derives its client representations from the current public API definitions and documentation that API owns. Missing documentation does not authorize Presentation to invent endpoints, fields, or response behaviour. Any ambiguity that prevents a correct client is reported for the affected integration, while independently defined work may continue.

**Why:** A single door means the application's rules are enforced in one place, and the transport can change without touching how the interface behaves.

**Boundary:** Presentation never connects to Database, imports Logic implementation code, or bypasses Logic. Presentation never performs API communication directly. The protocol, client technology, and transport settings are technical choices rather than Presentation philosophy.

<br>

### 5. Domain Models are shared, never copied

**Rule:** Presentation preserves the identity and meaning of the shared logical domain-model set through the public API contract. Presentation implementation never imports, copies, redefines, or creates a competing definition of Model meaning. API Access translates the API's representations for Interaction Logic and the user interface while preserving their traceability to the shared Model.

Presentation derives operation-specific input and output representations from the public API, preserving their traceability to the shared Model. Deriving client representations is not a second definition of domain meaning. Credential fields may be present in permitted write-only inputs but are excluded from output representations and are never expected in responses. Omitted input and explicit null remain distinct: a partial update does not send an untouched field, and sends null only as an explicit change permitted by the API. A field that API supplies through an allowed default or generation is not filled with a fabricated value merely to make the client representation appear complete.

**Why:** A copied definition drifts, and the interface then shows the user something the rest of the system no longer means.

**Boundary:** User-interface state and display formatting may extend a view without changing the shared Model.

<br>

### 6. Presentation implements only Presentation-targeted project Behaviour

**Rule:** Presentation may implement project Behaviour concerned with presentation and user interaction. Presentation determines how that Behaviour is exposed to the user, Interaction Logic coordinates its user-facing flow, and API Access consumes any Logic capability it requires.

**Why:** Behaviour that belongs to the user's experience is best expressed where the experience lives, while authoritative behaviour has exactly one home.

**Boundary:** A Presentation Behaviour never becomes a second implementation of authoritative Logic Behaviour. When an outcome depends on application rules, Presentation requests that outcome through the API Component and presents the returned result.

<br>

### 7. Appearance is governed by one coherent visual system

**Rule:** Presentation uses a coherent Theme and shared visual rules across its Components. Colours, typography, spacing, direction, display mode, and other visual decisions are resolved once and consumed consistently rather than being independently invented by each page or Component.

**Why:** Resolving appearance once is what makes an interface read as one product, and it makes a change to the visual system take effect everywhere at once.

**Boundary:** The existence and responsibility of this visual system are philosophical. The selected Theme, its values, styling technology, and other appearance defaults are technical choices resolved from the project definition and Presentation Preferences.

<br>

### 8. Presentation preserves its boundary

**Rule:** Presentation owns presentation, user-interface interaction, its API client boundary, and its visual system.

**Why:** A Component that states what it owns can be trusted by the Components around it, and can be replaced without redistributing responsibilities.

**Boundary:** Presentation does not own application persistence, Database access, authoritative application Behaviour, API implementation, or cross-layer composition. Cross-cutting capabilities selected by Development are consumed through explicit boundaries and do not become additional mandatory Presentation layers.

<br>

## At a Glance

- **Must** — Presentation is formed from Presentation, Interaction Logic, and API Access, in that dependency direction *(1)*
- **Never** — a layer bypasses the layer immediately responsible for the next boundary *(1)*
- **Must** — Presentation is assembled from focused, composable, reusable Components *(2)*
- **Never** — a page or view absorbs unrelated interaction or application logic *(2)*
- **Must** — Interaction Logic owns user-interface state, input, flows, and coordination between Components *(3)*
- **Never** — Interaction Logic implements authoritative application rules or persistence decisions *(3)*
- **Must** — application data and capabilities are reached only through the public API, through API Access *(4)*
- **Must** — when a machine-readable API description is unavailable, client representations derive from API-owned public definitions and documentation; unresolved integration ambiguities are reported without inventing API behaviour *(4)*
- **Never** — Presentation connects to Database, imports Logic implementation code, or bypasses Logic *(4)*
- **Never** — Presentation performs API communication directly *(4)*
- **Must** — every Presentation representation preserves the identity and meaning of the shared Models *(5)*
- **Must** — operation-specific input and output representations derive from the public API; credentials remain write-only inputs and are excluded from outputs *(5)*
- **Must** — partial input preserves the distinction between omission and explicit null and respects Logic-owned defaults and generation *(5)*
- **Never** — a client invents a field value to substitute for permitted omission, a default, or generation *(5)*
- **Never** — Presentation copies, redefines, or creates a competing definition of Model meaning *(5)*
- **Must** — an outcome that depends on application rules is requested from Logic and presented as returned *(6)*
- **Never** — a Presentation Behaviour becomes a second implementation of authoritative Logic Behaviour *(6)*
- **Must** — appearance is resolved once as one coherent Theme and consumed consistently *(7)*
- **Never** — a page or Component invents its own visual decisions *(7)*
- **Never** — Presentation owns persistence, Database access, authoritative Behaviour, API implementation, or cross-layer composition *(8)*
- **Never** — a cross-cutting capability becomes an additional mandatory Presentation layer *(8)*
