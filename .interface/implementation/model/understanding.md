# Model Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this file preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

## Model

**What is the Model for, in the Human's words?** When the Agent has an Understanding of the Target, the Target has already declared its Models with their primary keys, auto-increment, nullability, defaults, relationships, and uniqueness, in its own language. Model must express those same parameters in one standard vocabulary that belongs to no technology and no database — type, size, relationships, generated identity — so that the Model can always be understood and built. Which type or size a field gets is Model's own decision from the Target; the Interface does not fix a closed list for it. Database using that vocabulary to build storage is one of Model's uses, not its main purpose; the main purpose is that Models are the shared language between every Component of the application. There is one definition, not a Model for code and a separate schema for storage. Because Model is also a Development Component, it takes its programming language, modeling package, and Agent Skills from its Component Profile in Development.

**Decisions:**

1. The Declaration Vocabulary publishes the logical field type — a technology-independent value type, never a language type or an Engine type.
2. Model decides a field's type and size from the Target. A proposal to list the permitted types in the Interface was rejected: a closed list limits what Model can express about a domain the Interface has never seen.
3. The vocabulary is carried by the same Domain Definition that application code uses. There is no second schema artifact beside it, and every Component — Database among them — reads the declaration through the Model Public Interface.
4. Model takes its language, modeling package, Agent Skills, and Platform Reference from its Component Profile in Development and selects no technology itself.
5. A proposal to route every Target property Model cannot express through State was rejected: Principle "Model preserves explicit Target meaning" already requires preservation, and a second route would invite Model to declare a property unexpressible instead of expressing it.

<br>

## Structure

**How should the Models be laid out?** Each entity, each domain, has a separate structure of its own. This is part of the structure and the philosophy, not a preference that changes from project to project.

**Decisions:**

1. Principle "Each Domain Definition stands in its own module" states it as separation: one Domain Definition per module, never several gathered together, with the Public Interface publishing each by its own identity.
2. The Principle names no file, directory, or import mechanism. The realization — one file per definition, its name, and how it is re-exported — is stated in Model Preferences.
3. Model Foundation is not divided this way; shared mechanism stays in one place of its own.

<br>

## Serialization

**What must every Model be able to do, in the Human's words?** Every Model needs two functions. One takes an item and gives back its JSON. The other takes that JSON and gives back the Model item.

**Decisions:**

1. The conversion produces a plain structure of named values, not encoded text; building the JSON text is the consuming Component's work. A proposal to return a finished JSON string was rejected because it would put transport inside Model. The plain structure stays JSON-compatible, so the Human's intent is kept.
2. The two capabilities are named `serialize` and `deserialize`, for what they do rather than for a wire format. `to_json` and `from_json` were rejected because the output is not JSON text; `to_dictionary` and `from_dictionary` were rejected because dictionary is one language's type name.
3. `deserialize` evaluates the Domain Definition's own Intrinsic Rules and fails when the data does not satisfy them, so nothing outside Model can construct an instance the domain rules would reject.
4. A Plain Representation carries the Domain Definition's own Fields, and a Domain Relationship appears only as its declared foreign-key value. A proposal to let a consumer ask for chosen relationships to be nested was rejected as more than the domain needs.
5. Serialization withholds nothing. Removing a credential or any other Field from a response is the consuming Component's decision, and API Preferences keep that rule. A proposal to mark sensitive Fields in Model and have Serialization drop them was rejected; the consequence — that a consumer other than API calling `serialize` directly carries no such protection — is accepted.
6. Both capabilities come from Model Foundation, defined once, so every Domain Definition carries the same pair without declaring it again.
