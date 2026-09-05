# Model Principles

Model is the Component that describes the domain entities and concepts from which a project is formed. It provides one shared logical meaning for data so every technical Component can implement the same concepts without redefining them.

Every statement here is mandatory. Technical defaults belong to Model Preferences, and the exact shape of the generated Model configuration belongs to the Model Schema.

<br>

## 1. Models represent domain entities

Each Model represents one meaningful entity or concept in the domain. A Model explains what that entity is, what information belongs to it, how it relates to other entities, and which domain rules govern it.

Models describe the project domain rather than source-code classes, database tables, API resources, forms, pages, or framework objects.

<br>

## 2. The logical Model connects persistence and APIs

The Model Component is the shared logical source for Components that need domain data. In particular, it connects the meaning of data persisted by the Database with the meaning of data accepted and exposed by APIs.

The Database determines how a Model is stored, related, constrained, and retrieved. An API determines how that Model is received, validated for transport, and presented to consumers. Neither side independently redefines the Model's domain meaning.

Backend, Frontend, Database, and other Components may create their own technical representations, but those representations preserve the same logical identity, fields, relationships, and rules.

A technical Component may add implementation detail needed within its own boundary, but it does not redefine the identity or meaning of a Model.

<br>

## 3. Fields express domain data

Fields describe the information carried by a Model. Their logical type, identity, uniqueness, optionality, default behaviour, and meaning may be expressed when applicable.

Field definitions remain independent of a particular programming language, storage engine, API framework, or user-interface technology. Physical columns, transport formats, widgets, and framework-specific declarations belong to their respective Components.

<br>

## 4. Relationships express domain connections

Relationships describe how Models are conceptually connected and, when needed, identify the logical field that carries that connection.

The physical realization of a relationship, including database constraints and storage-specific referential behaviour, belongs to the Database Component. API exposure and presentation belong to their respective Components.

<br>

## 5. Domain rules and initial data remain part of the Model

A Model may contain rules that constrain its valid domain state and initial records that must exist when the project begins. These remain logical declarations until the responsible technical Components resolve and implement them.

<br>

## 6. Common fields are defaults, not universal requirements

Common fields may be supplied through Model Preferences when their definitions are absent. They are conveniences for resolving an otherwise unspecified Model, not mandatory properties of every entity.

An explicit Model definition always takes precedence: it may change a default field, replace it, or state that it does not apply. Technical Components consume the resulting resolved Model rather than independently adding their own common fields.
