# Backend Principles

Backend is the Component that executes application Behaviour and publishes the application's API. It turns the shared domain meaning into what the application does, enforces rules that depend on application context, and exposes the result as the one contract every external consumer depends on. Its architecture is independent of any language, framework, protocol, package, database engine, or project.

Backend owns application Behaviour, the route from Behaviour to persistence, and the external API contract. It does not own domain-model meaning, physical persistence, user-interface presentation, or cross-layer composition.

## Terms

- **API** — the layer that is the external communication boundary of Backend.
- **Logic** — the layer that implements application Behaviour and Model-specific logic.
- **Data Access** — the layer that is the only Backend boundary consuming the Database interface.
- **Model Logic** — the logical unit inside Logic that belongs to one shared Model and carries its operations and Behaviour.
- **Behaviour** — what the application does and the rules under which it does it, independent of how it is requested or stored.
- **Credential** — a Model field marked as secret, accepted as input but never returned across the API boundary.

## Relationships

- **Consumes Model** — the shared logical Model definitions used by Logic, Data Access, and API.
- **Consumes Database** — the generic data-access interface, reached only through Data Access.
- **Consumes Development** — the common package standard, ownership of Backend's settings and private secrets, and the cross-cutting capabilities selected for the project.
- **Consumes Platform** — the Bindings the selected Launch delivers to Backend's boundary.
- **Consumed by Frontend** — the public API through which the user interface reaches application data and capabilities.

Technical choices and defaults belong to Backend Preferences. Backend implementation applies those choices to the current project definition.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Backend has three internal layers

**Rule:** Backend is formed from three distinct layers:

- **API** is the external communication boundary;
- **Logic** implements application Behaviour and Model-specific logic; and
- **Data Access** is the only Backend boundary that consumes the Database interface.

The dependency direction is API → Logic → Data Access → Database interface.

**Why:** Separating the outside world from what the application does, and both from how data is reached, lets any one of the three be replaced without disturbing the other two.

**Boundary:** No layer bypasses the layer immediately responsible for the next boundary.

<br>

## 2. Logic owns application Behaviour

**Rule:** Logic implements what the application does and the rules under which it does it. It enforces conditions that depend on the operation or application context and reuses the shared Model's validation for constraints determined from Model data. For partial changes, Logic ensures that validation considers the resulting domain state, including existing values needed to evaluate the applicable rules. Logic communicates with persistence only through Data Access; Database remains responsible for guaranteeing constraints that depend on stored state.

Logic determines which related data operations must succeed as one unit and requests that unit through Data Access. It does not implement the underlying transaction mechanism or treat changes to external services as part of the Database transaction.

**Why:** Behaviour expressed without transport or storage detail remains valid when the API technology or Database implementation changes.

**Boundary:** Logic is independent of HTTP, API frameworks, database engines, ORM implementations, physical storage, and transport-specific request or response shapes.

<br>

## 3. Every Model has a standard Logic surface

**Rule:** Every shared Model receives its own logical unit inside Logic, defined separately from the unit of every other Model. That unit provides a consistent baseline for common Model operations such as create, get, list, update, and delete. Common operations may be implemented in a shared base or helper and reused through inheritance or composition. Model-specific Behaviour may extend this baseline: one Model may perform validation, calculations, coordination, or other actions that another Model does not. An API request for a Model is handled by the corresponding Model Logic, which may use Data Access and may perform other Behaviour required by the Model.

The operations selected in Backend Preferences are offered only where the shared Model supports them. When status is selected, it is available only for a Model declaring the corresponding field, and its actions follow the public Database interface. A status request passes through the corresponding Model Logic and Data Access; it never creates a missing field or bypasses Model-specific Behaviour.

**Why:** Each Model retains its own unit even when it currently uses only the common baseline, so its operations and Behaviour can later be extended independently without changing another Model's Logic.

**Boundary:** A definition shared by several Models does not satisfy this separation. A shared registry may import and connect the units without defining them itself. Model-specific additions remain inside that Model's Logic and never weaken the common interface expected across Models. API never substitutes direct persistence for Model Logic.

<br>

## 4. Data Access is the only Backend route to Database

**Rule:** Data Access translates the data operations requested by Logic into calls to the generic interface published by Database, and translates the results back into logical data. When Logic requests a group of related operations, Data Access connects that group to the public Database transaction boundary on one resolved Instance. Every participating operation uses that same boundary, and Data Access propagates its outcome without committing individual operations independently. Database retains ownership of commit, rollback, and connection cleanup.

**Why:** One translation point means the Database implementation can change without Logic being rewritten, and every persistence call is visible in one place.

**Boundary:** Data Access contains no application Behaviour and does not decide which operations belong together. It never owns or directly reaches into the database engine, connection, ORM, tables, schema, or migrations. Transaction access exposes no such internals to Logic or API and implies no atomicity across Instances or external services. API and Logic never bypass it to access Database.

<br>

## 5. API is the external Backend boundary

**Rule:** API receives external requests, validates their transport-level shape, invokes Logic, and converts Logic results into external responses. API owns only communication concerns such as request decoding, transport-level validation, response serialization, protocol handling, and mapping logical outcomes to API responses.

**Why:** Keeping the boundary thin means the application's behaviour is reachable through any transport, and a protocol change never becomes a behaviour change.

**Boundary:** API does not implement application Behaviour and never calls Data Access or Database directly. Model owns validation determined from its own data; Logic owns application-context checks and coordinates the validation required by the operation. API may reuse shared Model validation when decoding input, but it neither duplicates those rules nor treats transport validation as proof that the resulting domain state is valid. The existence and responsibility of API are philosophical; its framework, version, protocol, and other technical settings are resolved from the project definition and Backend Preferences.

<br>

## 6. Model definitions are shared, never copied

**Rule:** Backend obtains logical Model definitions from the project definition under the Model Component's Principles and Preferences, and consumes their shared package. Logic uses Model meaning and domain rules, Data Access uses Model identity and fields when calling Database, and API derives its data-facing input and output representations from the same shared definition.

**Why:** One shared definition is what keeps the meaning of a Model identical on both sides of the Backend boundary.

**Boundary:** Backend does not copy, redefine, or create a competing representation of Model meaning. HTTP-specific and storage-specific details remain outside Model.

<br>

## 7. API serves Model operations and project Behaviour

**Rule:** Backend is not limited to Model CRUD. Logic implements Backend-targeted project Behaviour, and API exposes the Behaviour that must be available to external consumers. Model-level API intent and externally exposed Behaviour are resolved from the project definition under Backend Principles and Preferences.

**Why:** A project's value usually lies in what it does beyond storing records, so the API surface follows the stated Behaviour rather than the Model list.

**Boundary:** That resolution fixes no endpoint paths, HTTP method mappings, file layout, or framework implementation details. Those details are implementation output.

<br>

## 8. API documentation belongs to API

**Rule:** The capability to publish a machine-readable description of available operations and data shapes belongs to the API layer.

**Why:** The layer that defines the external contract is the only one that can describe it accurately as it changes.

**Boundary:** No other Backend layer owns or generates the public API description. Whether documentation is enabled, its format, and the tool that produces it are technical choices resolved through Backend Preferences.

<br>

## 9. Credentials are write-only at the API boundary

**Rule:** A Model field marked as a credential is write-only API input. It may be accepted when required to create or update its owning Model. Its input definition, including its name, type, requiredness, and write-only nature, may appear in input schemas and API documentation so a consumer knows how to supply it. The field is excluded from API responses and response schemas. Actual credential values are never exposed in documentation, examples, error payloads, diagnostics, traces, or recorded outputs; examples use non-secret placeholders only.

**Why:** A credential that leaves the boundary even once is compromised, and the places it can leak are exactly the places that are easy to overlook.

**Boundary:** Backend reads the credential marker from the shared Model definition and never guesses credential fields from their names. Database owns the credential's at-rest storage mode; Backend does not redefine it.

<br>

## 10. Logic may orchestrate resolved supporting services

**Rule:** Model Logic may use Data Access and may also coordinate supporting services or cross-cutting capabilities selected by Development. Such services are consumed through explicit interfaces and are used only by the Model Logic that needs them.

**Why:** Capabilities chosen for the whole project must be usable inside Behaviour without every Model being forced to depend on them.

**Boundary:** A supporting service does not become a fourth mandatory Backend layer and does not weaken the API → Logic → Data Access dependency path for persistence. Its availability and application scope are resolved outside Backend rather than hard-coded into Model Logic.

<br>

## At a Glance

- **Must** — Backend is formed from API, Logic, and Data Access, in that dependency direction *(1)*
- **Never** — a layer bypasses the layer immediately responsible for the next boundary *(1)*
- **Must** — Logic implements application Behaviour and reaches persistence only through Data Access *(2)*
- **Must** — Logic enforces operation-dependent conditions, reuses shared Model validation, and validates partial changes against the resulting domain state *(2)*
- **Must** — Database remains responsible for guaranteeing constraints that depend on stored state *(2)*
- **Must** — Logic determines the related operations that form one unit and requests it through Data Access *(2)*
- **Never** — Logic implements Database transaction mechanisms or assumes they cover external service changes *(2)*
- **Never** — Logic depends on HTTP, API frameworks, database engines, ORM implementations, or physical storage *(2)*
- **Must** — every shared Model has its own separately defined Logic unit providing the common operation baseline *(3)*
- **Must** — selected operations respect Model capabilities; status follows Database's public semantics and runs through Model Logic and Data Access only for a Model declaring the field *(3)*
- **Never** — a status operation invents a missing field or bypasses Model-specific Behaviour *(3)*
- **Never** — one definition shared by several Models stands in for their separate Logic units *(3)*
- **Never** — API substitutes direct persistence for Model Logic *(3)*
- **Must** — Data Access translates Logic's data operations into calls on the generic Database interface *(4)*
- **Must** — Data Access carries a Logic-defined group through one Instance's public transaction boundary and propagates the outcome; Database owns commit, rollback, and cleanup *(4)*
- **Never** — Data Access commits grouped operations independently, decides application grouping, or promises atomicity across Instances or external services *(4)*
- **Never** — Data Access contains application Behaviour or reaches into the engine, connection, ORM, tables, schema, or migrations *(4)*
- **Must** — API decodes requests, validates transport shape, invokes Logic, and serializes results *(5)*
- **Never** — API duplicates shared Model validation or treats transport validation as proof of valid domain state *(5)*
- **Never** — API implements application Behaviour or calls Data Access or Database directly *(5)*
- **Must** — every Backend representation of a Model derives from the shared Model definition *(6)*
- **Never** — Backend copies, redefines, or creates a competing representation of Model meaning *(6)*
- **Must** — API exposes the project Behaviour that external consumers require, not only Model operations *(7)*
- **Never** — resolution fixes endpoint paths, method mappings, file layout, or framework details *(7)*
- **Must** — the machine-readable description of the API is owned and produced by the API layer *(8)*
- **Never** — another Backend layer owns or generates the public API description *(8)*
- **Must** — a credential field is accepted as input only, and its marker is read from the shared Model definition *(9)*
- **Must** — credential definitions documented in input schemas retain their write-only nature and examples contain only non-secret placeholders *(9)*
- **Never** — a credential field appears in an API response or response schema, or its actual value appears in documentation, examples, error payloads, diagnostics, traces, or recorded outputs *(9)*
- **Never** — Backend redefines the at-rest storage mode of a credential *(9)*
- **Must** — supporting services are consumed through explicit interfaces by the Model Logic that needs them *(10)*
- **Never** — a supporting service becomes a fourth mandatory layer or weakens the persistence dependency path *(10)*
