# Backend Principles

Backend is the Component that executes application Behaviour and publishes the application's API. Its architecture is independent of any language, framework, protocol, package, database engine, or project.

Technical choices and defaults belong to Backend Preferences. The exact shape of the generated Backend configuration belongs to the Backend Schema.

Every statement here is mandatory. A Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Backend has three internal layers

Backend is formed from three distinct layers:

- **API** is the external communication boundary;
- **Logic** implements application Behaviour and Model-specific logic; and
- **Data Access** is the only Backend boundary that consumes the Database interface.

The dependency direction is API → Logic → Data Access → Database interface. No layer bypasses the layer immediately responsible for the next boundary.

<br>

## 2. Logic owns application Behaviour

Logic implements what the application does and the rules under which it does it. It is independent of HTTP, API frameworks, database engines, ORM implementations, physical storage, and transport-specific request or response shapes.

Logic communicates with persistence only through Data Access. It can therefore remain valid when the API technology or Database implementation changes.

<br>

## 3. Every Model has a standard Logic surface

Every shared Model receives its own logical unit inside Logic. That unit provides a consistent baseline for common Model operations such as create, get, list, update, and delete.

Model-specific Behaviour may extend this baseline. One Model may perform validation, calculations, coordination, or other actions that another Model does not. These additions remain inside that Model's Logic and never weaken the common interface expected across Models.

An API request for a Model is handled by the corresponding Model Logic. That Logic may use Data Access and may perform other Behaviour required by the Model; API never substitutes direct persistence for Model Logic.

<br>

## 4. Data Access is the only Backend route to Database

Data Access translates the data operations requested by Logic into calls to the generic interface published by Database and translates the results back into logical data.

Data Access contains no application Behaviour. It never owns or directly reaches into the database engine, connection, ORM, tables, schema, or migrations. API and Logic never bypass it to access Database.

<br>

## 5. API is the external Backend boundary

API receives external requests, validates their transport-level shape, invokes Logic, and converts Logic results into external responses. It does not implement application Behaviour and never calls Data Access or Database directly.

Domain validation remains in Logic. API owns only communication concerns such as request decoding, transport-level validation, response serialization, protocol handling, and mapping logical outcomes to API responses.

The existence and responsibility of API are philosophical. Its framework, version, protocol, and other technical settings are resolved through Backend Preferences and generated Backend configuration.

<br>

## 6. Model definitions are shared, never copied

Backend obtains logical Model definitions from the generated Model configuration. It does not copy, redefine, or create a competing representation of Model meaning.

Logic uses Model meaning and domain rules, Data Access uses Model identity and fields when calling Database, and API derives its data-facing input and output representations from the same shared definition. HTTP-specific and storage-specific details remain outside Model.

<br>

## 7. API serves Model operations and project Behaviour

Backend is not limited to Model CRUD. Logic implements Backend-targeted project Behaviour, and API exposes the Behaviour that must be available to external consumers.

Model-level API intent and externally exposed Behaviour are resolved in Backend configuration without fixing endpoint paths, HTTP method mappings, file layout, or framework implementation details. Those details are implementation output.

<br>

## 8. API documentation belongs to API

The capability to publish a machine-readable description of available operations and data shapes belongs to the API layer. No other Backend layer owns or generates the public API description.

Whether documentation is enabled, its format, and the tool that produces it are technical choices resolved through Backend Preferences. The preferred default is enabled.

<br>

## 9. Credentials are write-only at the API boundary

A Model field marked as a credential is write-only API input. It may be accepted when required to create or update its owning Model, but it is never exposed in an API response, response schema, error payload, diagnostic, trace, or recorded output.

Backend reads the credential marker from Model configuration and never guesses credential fields from their names. Database owns the credential's at-rest storage mode; Backend does not redefine it.

<br>

## 10. Logic may orchestrate resolved supporting services

Model Logic may use Data Access and may also coordinate supporting services or cross-cutting capabilities selected by Development. Such services are consumed through explicit interfaces and are used only by the Model Logic that needs them.

A supporting service does not become a fourth mandatory Backend layer and does not weaken the API → Logic → Data Access dependency path for persistence. Its availability and application scope are resolved outside Backend rather than hard-coded into Model Logic.
