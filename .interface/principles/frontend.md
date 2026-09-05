# Frontend Principles

Frontend is the Component that presents the application to users, manages user interaction, and consumes capabilities published by Backend. Its architecture is independent of any language, library, framework, package manager, API protocol, or project.

Technical choices and defaults belong to Frontend Preferences. The exact shape of the generated Frontend configuration belongs to the Frontend Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Frontend has three internal layers

Frontend is formed from three distinct layers:

- **Presentation** renders pages and views by composing reusable user-interface Components;
- **Interaction Logic** manages user-interface state, input, interaction flows, and presentation decisions; and
- **API Access** is the only Frontend boundary that consumes the API published by Backend.

The dependency direction is Presentation → Interaction Logic → API Access → Backend API. No layer bypasses the layer immediately responsible for the next boundary.

<br>

## 2. Presentation is component-based

Presentation is assembled from focused, composable Components rather than monolithic pages or duplicated interface fragments. A page or view coordinates Components; it does not absorb unrelated interaction or application logic.

Reusable Components preserve consistent behaviour and appearance wherever the same user-interface concept is needed. Project-specific composition may vary without changing this architectural rule.

<br>

## 3. Interaction Logic owns user-interface behaviour

Interaction Logic manages state that exists for the user experience, including user input, form state, selection, navigation intent, loading state, and coordination between Presentation Components.

It may perform interaction-level validation and transform resolved data for presentation, but it does not implement authoritative application rules or persistence decisions. Application Behaviour and Model-specific business logic remain owned by Backend Logic.

<br>

## 4. API Access is the only door to application data

Frontend reaches application data and application capabilities only through the public API implemented by Backend. It never connects to Database, imports Backend implementation code, or bypasses Backend Logic.

API Access owns the Frontend-side client boundary, request and response transport, and translation between API representations and the data used by Interaction Logic. Presentation never performs API communication directly.

The protocol, client technology, and transport settings are technical choices rather than Frontend philosophy. API Access consumes the resolved Backend API and its machine-readable description when one is available.

<br>

## 5. Domain Models are shared, never copied

The shared logical domain-model set comes from the Model Component. Frontend configuration and implementation may use it, but they never copy, redefine, or create a competing definition of Model meaning.

Presentation uses Models to describe what users see and edit, Interaction Logic uses their logical meaning, and API Access preserves their identity across the Backend boundary. User-interface state and display formatting may extend a view without changing the shared Model.

<br>

## 6. Frontend implements only Frontend-targeted project Behaviour

Frontend may implement project Behaviour concerned with presentation and user interaction. Presentation determines how that Behaviour is exposed to the user, Interaction Logic coordinates its user-facing flow, and API Access consumes any Backend capability it requires.

A Frontend Behaviour never becomes a second implementation of authoritative Backend Behaviour. When an outcome depends on application rules, Frontend requests that outcome through Backend API and presents the returned result.

<br>

## 7. Appearance is governed by one coherent visual system

Frontend uses a coherent Theme and shared visual rules across its Components. Colours, typography, spacing, direction, display mode, and other visual decisions are resolved once and consumed consistently rather than being independently invented by each page or Component.

The existence and responsibility of this visual system are philosophical. The selected Theme, its values, styling technology, and other appearance defaults are technical choices resolved through Frontend Preferences and generated Frontend configuration.

<br>

## 8. Frontend preserves its boundary

Frontend owns presentation, user-interface interaction, its API client boundary, and its visual system. It does not own application persistence, Database access, authoritative application Behaviour, Backend API implementation, or cross-layer composition.

Cross-cutting capabilities selected by Development are consumed through explicit boundaries and do not become additional mandatory Frontend layers.
