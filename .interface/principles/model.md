# Model Principles

Model is the Component and independent application layer that describes the domain entities and concepts from which a project is formed. It provides one shared logical meaning and one reusable implementation boundary for domain data so technical Components can consume the same concepts without redefining them.

Every statement here is mandatory. Technical defaults belong to Model Preferences, and the exact shape of the generated Model configuration belongs to the Model Schema.

<br>

## 1. Models represent domain entities

Each Model represents one meaningful entity or concept in the domain. A Model explains what that entity is, what information belongs to it, how it relates to other entities, and which domain rules govern it.

Models describe the project domain rather than source-code classes, database tables, API resources, forms, pages, or framework objects.

<br>

## 2. Model is an independent shared package

The resolved Model set is implemented as its own package with a documented public import interface. Every resolved Model is exposed through that interface exactly once, using an ecosystem-compatible public symbol without changing its logical identity. Compatible application layers import this package rather than maintaining private copies of the same Models. A consumer that cannot import the package directly uses a representation derived from the same generated Model configuration through its declared layer interface.

The Model package owns domain representations and their validation. It does not own persistence mappings, business behaviour, API transport, user-interface presentation, or deployment. Its implementation language and modeling technology are resolved through Model Preferences, while its package identity and general package conventions are coordinated through Development.

The package can evolve independently while its public Model interface remains compatible.

<br>

## 3. The logical Model connects persistence and APIs

The Model Component is the shared logical source for Components that need domain data. In particular, it connects the meaning of data persisted by the Database with the meaning of data accepted and exposed by APIs.

The Database determines how a Model and its declared relationships and rules are physically mapped, enforced, stored, and retrieved. An API determines how that Model is received, validated for transport, and presented to consumers. Neither side independently redefines the Model's logical fields, relationships, rules, or domain meaning.

Backend, Frontend, Database, and other Components may create their own technical representations, but those representations preserve the same logical identity, fields, relationships, and rules.

A technical Component may add implementation detail needed within its own boundary, but it does not redefine the identity or meaning of a Model.

<br>

## 4. Fields express domain data

Fields describe the information carried by a Model. Their logical type, identity, uniqueness, optionality, default behaviour, credential nature, and meaning may be expressed when applicable.

Field definitions remain independent of a particular programming language, storage engine, API framework, or user-interface technology. Physical columns, transport formats, widgets, and framework-specific declarations belong to their respective Components.

<br>

## 5. Relationships express domain connections

Relationships describe how Models are conceptually connected and, when needed, identify the logical field that carries that connection.

The physical realization of a relationship, including database constraints and storage-specific referential behaviour, belongs to the Database Component. API exposure and presentation belong to their respective Components.

<br>

## 6. Domain rules and initial data remain part of the Model

A Model may contain rules that constrain its valid domain state and initial records that must exist when the project begins. These remain logical declarations until the responsible technical Components resolve and implement them.

<br>

## 7. Field defaults complete unspecified properties

Model Preferences may supply missing properties of fields already present in a Model definition. A default entry does not introduce a field into a Model or require every entity to contain it.

An explicit Model property always takes precedence over its default, including an explicit false or null value. Defaults are applied separately to each unspecified property, so a partially defined field can be completed without replacing its stated meaning. A field-name pattern alone does not define a domain relationship. Technical Components consume the resulting resolved Model rather than independently adding their own common fields.
