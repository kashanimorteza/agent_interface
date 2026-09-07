# Frontend Principles

Frontend is the Component that presents the application to users, manages user interaction, and consumes the capabilities published by Backend. It is where the project becomes something a person can see and act on, and it keeps that experience coherent by resolving its appearance and its interface behaviour once rather than page by page. Its architecture is independent of any language, library, framework, package manager, API protocol, or project.

## Terms

- **Presentation** — the layer that renders pages and views by composing reusable user-interface Components.
- **Interaction Logic** — the layer that manages user-interface state, input, interaction flows, and presentation decisions.
- **API Access** — the layer that is the only Frontend boundary consuming the API published by Backend.
- **Component (user-interface)** — one focused, composable unit of Presentation, reused wherever the same user-interface concept appears.
- **Theme** — the coherent visual system whose colours, typography, spacing, direction, and display mode are resolved once and consumed by every Component.

## Relationships

- **Consumes Backend** — the public API through which all application data and application capabilities are reached.
- **Consumes Model** — the shared logical domain-model set whose meaning Presentation, Interaction Logic, and API Access all preserve.
- **Consumes Development** — the common package standard and the cross-cutting capabilities selected for the project.
- **Consumed by no other Component** — Frontend is an outermost layer, and nothing in the architecture depends on it.

Technical choices and defaults belong to Frontend Preferences. Frontend implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Frontend has three internal layers

**Rule:** Frontend is formed from three distinct layers:

- **Presentation** renders pages and views by composing reusable user-interface Components;
- **Interaction Logic** manages user-interface state, input, interaction flows, and presentation decisions; and
- **API Access** is the only Frontend boundary that consumes the API published by Backend.

The dependency direction is Presentation → Interaction Logic → API Access → Backend API.

**Why:** Separating what the user sees from how the interface behaves and from how application data is fetched lets any one of the three change without disturbing the other two.

**Boundary:** No layer bypasses the layer immediately responsible for the next boundary.

<br>

## 2. Presentation is component-based

**Rule:** Presentation is assembled from focused, composable Components rather than monolithic pages or duplicated interface fragments. Reusable Components preserve consistent behaviour and appearance wherever the same user-interface concept is needed.

**Why:** One definition per user-interface concept keeps the interface consistent as it grows and keeps a change to that concept in one place.

**Boundary:** A page or view coordinates Components; it does not absorb unrelated interaction or application logic. Project-specific composition may vary without changing this architectural rule.

<br>

## 3. Interaction Logic owns user-interface behaviour

**Rule:** Interaction Logic manages state that exists for the user experience, including user input, form state, selection, navigation intent, loading state, and coordination between Presentation Components. It may perform interaction-level validation and transform resolved data for presentation.

**Why:** Interface state has a different lifetime and a different owner than application state, so keeping it in its own layer prevents the two from being confused for each other.

**Boundary:** It does not implement authoritative application rules or persistence decisions. Application Behaviour and Model-specific business logic remain owned by Backend Logic.

<br>

## 4. API Access is the only door to application data

**Rule:** Frontend reaches application data and application capabilities only through the public API implemented by Backend. API Access owns the Frontend-side client boundary, request and response transport, and translation between API representations and the data used by Interaction Logic. It consumes the resolved Backend API and its machine-readable description when one is available.

**Why:** A single door means the application's rules are enforced in one place, and the transport can change without touching how the interface behaves.

**Boundary:** Frontend never connects to Database, imports Backend implementation code, or bypasses Backend Logic. Presentation never performs API communication directly. The protocol, client technology, and transport settings are technical choices rather than Frontend philosophy.

<br>

## 5. Domain Models are shared, never copied

**Rule:** The shared logical domain-model set comes from the Model Component. Frontend implementation may use it, but it never copies, redefines, or creates a competing definition of Model meaning. Presentation uses Models to describe what users see and edit, Interaction Logic uses their logical meaning, and API Access preserves their identity across the Backend boundary.

**Why:** A copied definition drifts, and the interface then shows the user something the rest of the system no longer means.

**Boundary:** User-interface state and display formatting may extend a view without changing the shared Model.

<br>

## 6. Frontend implements only Frontend-targeted project Behaviour

**Rule:** Frontend may implement project Behaviour concerned with presentation and user interaction. Presentation determines how that Behaviour is exposed to the user, Interaction Logic coordinates its user-facing flow, and API Access consumes any Backend capability it requires.

**Why:** Behaviour that belongs to the user's experience is best expressed where the experience lives, while authoritative behaviour has exactly one home.

**Boundary:** A Frontend Behaviour never becomes a second implementation of authoritative Backend Behaviour. When an outcome depends on application rules, Frontend requests that outcome through Backend API and presents the returned result.

<br>

## 7. Appearance is governed by one coherent visual system

**Rule:** Frontend uses a coherent Theme and shared visual rules across its Components. Colours, typography, spacing, direction, display mode, and other visual decisions are resolved once and consumed consistently rather than being independently invented by each page or Component.

**Why:** Resolving appearance once is what makes an interface read as one product, and it makes a change to the visual system take effect everywhere at once.

**Boundary:** The existence and responsibility of this visual system are philosophical. The selected Theme, its values, styling technology, and other appearance defaults are technical choices resolved from the project definition and Frontend Preferences.

<br>

## 8. Frontend preserves its boundary

**Rule:** Frontend owns presentation, user-interface interaction, its API client boundary, and its visual system.

**Why:** A Component that states what it owns can be trusted by the Components around it, and can be replaced without redistributing responsibilities.

**Boundary:** Frontend does not own application persistence, Database access, authoritative application Behaviour, Backend API implementation, or cross-layer composition. Cross-cutting capabilities selected by Development are consumed through explicit boundaries and do not become additional mandatory Frontend layers.

<br>

## At a Glance

- **Must** — Frontend is formed from Presentation, Interaction Logic, and API Access, in that dependency direction *(1)*
- **Never** — a layer bypasses the layer immediately responsible for the next boundary *(1)*
- **Must** — Presentation is assembled from focused, composable, reusable Components *(2)*
- **Never** — a page or view absorbs unrelated interaction or application logic *(2)*
- **Must** — Interaction Logic owns user-interface state, input, flows, and coordination between Components *(3)*
- **Never** — Interaction Logic implements authoritative application rules or persistence decisions *(3)*
- **Must** — application data and capabilities are reached only through the public Backend API, through API Access *(4)*
- **Never** — Frontend connects to Database, imports Backend implementation code, or bypasses Backend Logic *(4)*
- **Never** — Presentation performs API communication directly *(4)*
- **Must** — every Frontend representation preserves the identity and meaning of the shared Models *(5)*
- **Never** — Frontend copies, redefines, or creates a competing definition of Model meaning *(5)*
- **Must** — an outcome that depends on application rules is requested from Backend and presented as returned *(6)*
- **Never** — a Frontend Behaviour becomes a second implementation of authoritative Backend Behaviour *(6)*
- **Must** — appearance is resolved once as one coherent Theme and consumed consistently *(7)*
- **Never** — a page or Component invents its own visual decisions *(7)*
- **Never** — Frontend owns persistence, Database access, authoritative Behaviour, API implementation, or cross-layer composition *(8)*
- **Never** — a cross-cutting capability becomes an additional mandatory Frontend layer *(8)*
