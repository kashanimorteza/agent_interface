# Model Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
2. **[Understanding](#understanding)**
   - **[Model](#model)**
   - **[Structure](#structure)**
   - **[Serialization](#serialization)**
3. **[Terms](#terms)**
4. **[Architecture](#architecture)**
5. **[Relationships](#relationships)**
6. **[Documentation](#documentation)**
7. **[Principles](#principles)**
   - **[Each domain concept has one authoritative Domain Definition](#each-domain-concept-has-one-authoritative-domain-definition)**
   - **[Model preserves explicit Target meaning](#model-preserves-explicit-target-meaning)**
   - **[Logical Model meaning is independent of implementation technology](#logical-model-meaning-is-independent-of-implementation-technology)**
   - **[Concrete Model realizations share one Model Foundation](#concrete-model-realizations-share-one-model-foundation)**
   - **[Model exposes an explicit and stable Public Interface](#model-exposes-an-explicit-and-stable-public-interface)**
   - **[Intrinsic validation and domain behavior are deterministic and side-effect free](#intrinsic-validation-and-domain-behavior-are-deterministic-and-side-effect-free)**
   - **[Model names express domain meaning](#model-names-express-domain-meaning)**
   - **[Model remains separate from external concerns](#model-remains-separate-from-external-concerns)**
   - **[Model declares every definition in one standard, technology-independent vocabulary](#model-declares-every-definition-in-one-standard-technology-independent-vocabulary)**
   - **[Every Domain Definition converts to and from a Plain Representation](#every-domain-definition-converts-to-and-from-a-plain-representation)**
   - **[Every Domain Definition declares whether it is persistent](#every-domain-definition-declares-whether-it-is-persistent)**
   - **[Each Domain Definition stands in its own module](#each-domain-definition-stands-in-its-own-module)**
8. **[At a Glance](#at-a-glance)**
<br>

## Introduction

### Overview

Model defines the authoritative logical meaning of the Target's domain through reusable Domain Definitions. It preserves domain identity, fields, relationships, rules, and behavior as one coherent Model boundary with an explicit Public Interface.

Model owns domain meaning and behavior determinable from its own data. It is not limited to a concept's Fields: it preserves the conceptual identity, relationships, defaults, and constraints the Target declares, and that makes it the shared language every other Component reads.

### Purpose

Every part of an application ends up carrying an opinion about what the domain means — what a User is, which of its fields may be empty, what makes two of them the same one. When no Component owns that meaning, each one forms its own: the storage layer decides a field's type from its column, the API decides it from its payload, the interface decides it from the form, and the three answers drift apart until the same record is valid in one place and rejected in another.

Model exists so the meaning is written once and read by everyone. It holds the Target's domain as Domain Definitions — identity, fields and their declared properties, relationships, and the rules that follow from the data itself — in one vocabulary that belongs to no language, no framework, and no database. Every other Component reads that vocabulary instead of inventing its own, which is what makes them agree without coordinating.

Its separation also protects the meaning from the mechanisms. A definition that carried its storage layout would change whenever the Engine changed; a definition that carried its transport shape would change whenever the API did. Model carries neither, so the domain outlives both — and a Component behind it can be replaced without the domain being renegotiated.

### How It Works

A Domain Definition is the unit Model works in: one authoritative definition for each meaningful concept the Target declares. It names the concept's fields, and for each field the properties the Target states — its logical type, whether it may be absent, its default, whether it is part of the identity, whether its value must be unique — together with the relationships it has to other Domain Definitions and the rules that can be decided from its own data alone.

Those properties are expressed in one standard vocabulary rather than in any technology's terms. A field's type is a logical type, not a column type and not a language type; a relationship names the Domain Definition it points to and its cardinality, not a storage constraint.

A consumer imports a Domain Definition through Model's Public Interface and finds both: the type it constructs and validates with, and the declaration describing it. Database reads that declaration to derive storage, Logic reads it to reason about the domain, and neither reinterprets the Target to do so.

<br>

## Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this section preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

### Model

**What is the Model for, in the Human's words?** When the Agent has an Understanding of the Target, the Target has already declared its Models with their primary keys, auto-increment, nullability, defaults, relationships, and uniqueness, in its own language. Model must express those same parameters in one standard vocabulary that belongs to no technology and no database — type, size, relationships, generated identity — so that the Model can always be understood and built. Which type or size a field gets is Model's own decision from the Target; the Interface does not fix a closed list for it. Database using that vocabulary to build storage is one of Model's uses, not its main purpose; the main purpose is that Models are the shared language between every Component of the application. There is one definition, not a Model for code and a separate schema for storage. Because Model is also a Development Component, it takes its programming language, modeling package, and Agent Skills from its Component Profile in Development.

**Decisions:**

1. The Declaration Vocabulary publishes the logical field type — a technology-independent value type, never a language type or an Engine type.
2. Model decides a field's type and size from the Target. A proposal to list the permitted types in the Interface was rejected: a closed list limits what Model can express about a domain the Interface has never seen.
3. The vocabulary is carried by the same Domain Definition that application code uses. There is no second schema artifact beside it, and every Component — Database among them — reads the declaration through the Model Public Interface.
4. Model takes its language, modeling package, Agent Skills, and Platform Reference from its Component Profile in Development and selects no technology itself.
5. A proposal to route every Target property Model cannot express through State was rejected: Principle "Model preserves explicit Target meaning" already requires preservation, and a second route would invite Model to declare a property unexpressible instead of expressing it.

<br>

### Structure

**How should the Models be laid out?** Each entity, each domain, has a separate structure of its own. This is part of the structure and the philosophy, not a preference that changes from project to project.

**Decisions:**

1. Principle "Each Domain Definition stands in its own module" states it as separation: one Domain Definition per module, never several gathered together, with the Public Interface publishing each by its own identity.
2. The Principle names no file, directory, or import mechanism. The realization — one file per definition, its name, and how it is re-exported — is stated in Model Preferences.
3. Model Foundation is not divided this way; shared mechanism stays in one place of its own.

<br>

### Serialization

**What must every Model be able to do, in the Human's words?** Every Model needs two functions. One takes an item and gives back its JSON. The other takes that JSON and gives back the Model item.

**Decisions:**

1. The conversion produces a plain structure of named values, not encoded text; building the JSON text is the consuming Component's work. A proposal to return a finished JSON string was rejected because it would put transport inside Model. The plain structure stays JSON-compatible, so the Human's intent is kept.
2. The two capabilities are named `serialize` and `deserialize`, for what they do rather than for a wire format. `to_json` and `from_json` were rejected because the output is not JSON text; `to_dictionary` and `from_dictionary` were rejected because dictionary is one language's type name.
3. `deserialize` evaluates the Domain Definition's own Intrinsic Rules and fails when the data does not satisfy them, so nothing outside Model can construct an instance the domain rules would reject.
4. A Plain Representation carries the Domain Definition's own Fields, and a Domain Relationship appears only as its declared foreign-key value. A proposal to let a consumer ask for chosen relationships to be nested was rejected as more than the domain needs.
5. Serialization withholds nothing. Removing a credential or any other Field from a response is the consuming Component's decision, and API Preferences keep that rule. A proposal to mark sensitive Fields in Model and have Serialization drop them was rejected; the consequence — that a consumer other than API calling `serialize` directly carries no such protection — is accepted.
6. Both capabilities come from Model Foundation, defined once, so every Domain Definition carries the same pair without declaring it again.

<br>

## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Field** — one named property of a Domain Definition, with its domain meaning and applicable constraints.
- **Model Foundation** — the technology-independent common foundation through which concrete Model realizations receive shared mechanisms without inheriting domain Fields or relationships.
- **Intrinsic Rule** — a domain rule that can be evaluated entirely from the data of the Domain Definition it governs.
- **Domain Relationship** — a logical association between Domain Definitions whose meaning and constraints come from the Target.
- **Declaration Vocabulary** — the one standard, technology-independent vocabulary in which every Domain Definition states its Fields, properties, relationships, and constraints.
- **Plain Representation** — a Domain Definition's data expressed as simple named values, carrying no behavior and no technology of its own.
- **Serialization** — the pair of symmetric conversions between a Domain Definition and its Plain Representation.

<br>

## Architecture

```text
Model
├── Domain Definition          ← one authoritative definition per domain concept
├── Declaration Vocabulary     ← the one language every definition is stated in
├── Model Foundation           ← the mechanisms every definition shares
└── Public Interface           ← the only surface a consumer reaches
```

**Domain Definition** stands in a module of its own and holds the meaning of one concept the Target declares: its identity, its Fields and their properties, its Domain Relationships, and the Intrinsic Rules decidable from its own data. It never holds a concept that exists only for an implementation tool, and it never reaches outside its own data to decide something.

**Declaration Vocabulary** is the single set of terms every Domain Definition states itself in — logical type, length and precision, nullability, default, identity, uniqueness, relationship and cardinality. It belongs to no language, package, or Engine, and it is carried by the same Domain Definition application code uses rather than by a separate artifact beside it.

**Model Foundation** supplies what every concrete Domain Definition shares: validation, Serialization, and the publishing of the Declaration Vocabulary. It provides mechanism only, and stands in a module of its own beside the definitions rather than above them.

**Public Interface** is the one surface through which a consumer reaches a Domain Definition, its declaration, and its Serialization pair. A consumer never depends on anything private behind it, and its evolution follows Development's change-propagation rules.

<br>

## Relationships

- **Consumes Development** — takes from it what Model does not choose for itself: its identity, its technology, and where it runs.
- **Consumed by Database** — provides the Declaration Vocabulary from which Database derives and enforces physical storage structure.
- **Consumed by Logic** — provides the Domain Definitions Logic reasons about and passes between its Services.
- **Consumed by API and Presentation** — provides the Domain Definitions they accept and return, and the Serialization pair they convert with.
- **Consumed through Development-defined Connections** — every consumer reaches Model through its Public Interface, and Model repeats neither the identities nor the internal behavior of its consumers.

<br>

<br>

Model-owned defaults and implementation conventions belong to Model Preferences. Model's configurable identity and all technical or Platform references belong to its Component Profile in Development Preferences. Implementation applies those sources to the current Target definition.

<br>

## Documentation

Model is imported, not called: a consumer adds it as a library and works with the Domain Definitions it publishes. So its documentation answers a different first question than a Component with Operations does — not *what can I ask it to do*, but *what does it give me, and what can I do with it*.

A reader must come away knowing which Domain Definitions this Model publishes and what each one represents in the domain, and for each, the Fields it declares with the properties declared on them and whether it is persistent. A Model with five definitions lists five, not a description of the idea of a definition.

Then the three things a consumer does with one, each shown with an example that runs as written: import the Model and construct an instance; turn an instance into its Plain Representation; and build an instance back from one. The documentation also states plainly what Model does not do — it stores nothing, performs no application behaviour, and offers no operations on stored data — so a reader does not go looking for a capability that lives in another Component.

<br>

Every Principle in this file is mandatory. An Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

Every Principle below is mandatory.

<br>

### Each domain concept has one authoritative Domain Definition

**Rule:** Every meaningful domain concept resolved from the Target has exactly one authoritative Domain Definition in Model. A Domain Definition originates in domain meaning rather than the needs of an implementation tool or consumer, and the same domain identity is never independently redefined elsewhere.

**Why:** One logical authority gives every authorized consumer the same meaning and prevents competing definitions from drifting apart.

**Boundary:** An implementation-only structure with no independent domain meaning does not require a Domain Definition merely because a tool or consumer uses it.

<br>

### Model preserves explicit Target meaning

**Rule:** Model preserves every explicit Domain Definition, Field, property, Domain Relationship, constraint, sensitive or credential meaning, and Intrinsic Rule stated by the Target. Model Preferences may complete only missing properties of existing Fields, property by property. A default never creates a Field, overrides an explicit value including `false` or `null`, changes meaning, or invents a relationship or behavior. Every Domain Relationship preserves the meaning and constraints declared by the Target.

What the domain *is* comes only from the Target: which Domain Definitions exist, which Fields they carry, what those Fields and relationships are named, and how they relate. How a Field is realized is a separate question. Where the Target states no technical modelling parameter for an existing Field — a representation choice, a validation detail, a constraint the Target already implies — Model chooses it under its own Principles and records a consequential choice so it can be reviewed, rather than leaving the Field underspecified. Where such a record is kept is stated in Model Preferences. Such a choice never adds, removes, or renames a Field or relationship, never overrides an explicit Target value, and never changes what a Field means.

Model also preserves each Target-declared credential classification and required at-rest treatment. Database applies that declared treatment and rejects a persisted credential whose treatment is missing or unsupported; neither Component infers credential policy from a field name.

**Why:** The Target remains authoritative for what the domain means, while the details it never speaks to can still be settled — a Model that refuses to choose anything the Target did not spell out produces an underspecified definition, which is its own kind of unfaithfulness.

**Boundary:** Project records, including Initial Data, are not Domain Definitions and are not owned or introduced by Model.

<br>

### Logical Model meaning is independent of implementation technology

**Rule:** Every Domain Definition and Intrinsic Rule remains understandable independently of a specific language, package, tool, version, runtime, or platform mechanism. A selected technology may realize Model concepts only while preserving their logical meaning.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Technology independence does not prevent the Model Component Profile in Development Preferences from selecting concrete compatible technical and Platform references.

<br>

### Concrete Model realizations share one Model Foundation

**Rule:** Every concrete Model realization receives applicable shared Model mechanisms through one Model Foundation. The Foundation may provide validation, serialization, and metadata-publishing mechanisms, but it never owns, injects, or requires a Field or Domain Relationship. Each Domain Definition declares its own complete set of Fields and relationships from the Target.

**Why:** A single common foundation keeps cross-Model mechanisms consistent without imposing fields or domain meaning on a Domain Definition.

**Boundary:** Model Foundation does not require a base class, inheritance, or any other particular realization mechanism; the selected technology determines the compatible form. Shared implementation does not imply shared domain Fields.

<br>

### Model exposes an explicit and stable Public Interface

**Rule:** Model exposes its authoritative Domain Definitions through one explicit and stable Public Interface. Consumers use that surface rather than private internal resources, and each public Domain Definition has one unambiguous public identity.

**Why:** A clear public boundary makes Model reusable while allowing its private organization to evolve.

**Boundary:** This fixes the existence of the boundary, not its shape: the import path, the re-export mechanism, and the file layout behind it belong to the selected realization and are stated in Model Preferences. Public Interface evolution remains governed by Development's change-propagation rules.

<br>

### Intrinsic validation and domain behavior are deterministic and side-effect free

**Rule:** Model validates only Intrinsic Rules. Every validation, derived value, serialization behavior, and other domain behavior depends only on the applicable Model data, produces a deterministic result for the same input, performs no external I/O, and creates no unrelated side effect.

**Why:** Local deterministic behavior keeps Model independent, predictable, reusable, and directly testable.

**Boundary:** A rule requiring external or operation-specific context is not an Intrinsic Rule, and Model never orchestrates an application workflow.

<br>

### Model names express domain meaning

**Rule:** Every Domain Definition, Field, Domain Relationship, and other public Model name expresses the meaning stated by the Target rather than an implementation tool or a consumer-specific representation.

**Why:** Domain-oriented names keep the logical model understandable without knowledge of a technical realization.

**Boundary:** This governs the meaning a name carries, not the form it is written in. How a name is spelled in the selected language, and how files and folders are named, belong to Model Preferences.

<br>

### Model remains separate from external concerns

**Rule:** Model never owns Initial Data, persistence, transport, presentation, workflow orchestration, technical selection, platform operation, or any other concern outside its logical domain boundary.

**Why:** A narrow boundary keeps Model reusable and prevents external concerns from changing or obscuring domain meaning.

**Boundary:** A separate Component may consume Model's Public Interface or realize an external concern using Model data, but that use does not transfer ownership to Model.

<br>

### Model declares every definition in one standard, technology-independent vocabulary

**Rule:** Model expresses every Domain Definition through one standard vocabulary that belongs to no language, package, or Engine: the logical field type, length and precision where the Target declares them, nullability, default, primary-key identity, generated identity, uniqueness, and single-field or composite constraints. Which type or size a field receives is Model's own decision from the Target; the Interface fixes no closed list. The vocabulary's own terms and their meanings are fixed by the Model Declaration Schema. This vocabulary is carried by the same Domain Definition that application code uses — there is no second schema artifact — and every Component reads it through the Model Public Interface. Each selected realization determines how that Domain Definition represents the vocabulary in its own technology.

Model preserves whether each Target Field is required, nullable, defaulted, generated, or otherwise allowed to be absent. An omitted Field is resolved according to the explicit Target declaration or the selected realization's compatible rules; Model never invents an absence state, default, or generation mechanism. Model defines no partial-update semantics and does not choose how a realization represents omitted values.

**Why:** One vocabulary understood without any technology lets every Component share the same definition while Model remains the single authority for domain meaning, and preserving the Target's declared presence semantics stops a generic Model rule from changing what a Field means.

**Boundary:** Model does not create tables, indexes, migrations, SQL, ORM mappings, or engine-specific constraints, and it does not enforce rules that require comparing multiple stored records. Nullability here means the domain allows a Field to have no value; recording that absence — as a null column or in any other way — belongs to whichever Component records it, and a non-persistent Domain Definition declares nullability with nothing recording it at all. Database owns physical realization and enforcement.

<br>

### A Domain Relationship carries the definition it refers to

**Rule:** Every Domain Relationship declares the Domain Definition it refers to, its cardinality, and its optionality. It carries that Domain Definition itself, not a name standing in for it: a reference that cannot be resolved is a broken declaration at the moment it is written, never a lookup that may fail later. Technology independence is independence from a language, package, or Engine — it is not an argument for leaving a reference untyped, and a realization that can carry the definition itself does so. Cardinality and optionality are stated from what the Target declares; neither is left to a default.

**Why:** A relationship named as text is checked by nobody: a renamed or misspelled definition survives every review and fails only when something tries to use it. Carrying the definition makes the relationship as verifiable as the Field it sits on.

**Boundary:** Model declares the relationship; it does not decide how the reference is stored, constrained, or indexed, and it never names that realization a foreign key. Database owns that.

<br>

### Every Domain Definition converts to and from a Plain Representation

**Rule:** Every Domain Definition offers two symmetric capabilities on its Public Interface: `serialize`, which produces the Plain Representation of one instance, and `deserialize`, which produces an instance from a Plain Representation. Both are provided once through Model Foundation so every Domain Definition carries the same pair without declaring it again. `serialize` returns simple named values, never an encoded text form; choosing a wire format is the consumer's concern. `deserialize` evaluates the same Intrinsic Rules the Domain Definition applies to any other instance and fails when the data does not satisfy them. Both are deterministic, depend only on the instance's own data, and perform no external I/O.

Conceptual example:

```text
instance      -> serialize   -> { field: value, ... }
{ field: ... } -> deserialize -> instance
```

**Why:** A Domain Definition that cannot leave and re-enter its own boundary forces every consumer to rebuild that conversion, and each rebuilt copy is a second place where domain meaning can drift. Making the return path validate closes the only remaining way to hold an instance that the domain rules would have rejected.

**Boundary:** Serialization publishes the Domain Definition's own Fields. A Domain Relationship appears only as its declared reference value, never as a nested Domain Definition, so one conversion never traverses the relationship graph. Serialization also applies no output policy of its own: withholding a credential or any other Field from a response is the consuming Component's decision, declared in that Component's Preferences. The example fixes no language, method syntax, or representation type.

<br>

### Every Domain Definition declares whether it is persistent

**Rule:** Every Domain Definition declares itself `persistent` or `non-persistent`. Database stores only the Domain Definitions Model declares persistent, and never infers persistence from a Domain Definition's existence, name, or the presence of an identity Field.

**Why:** Without a declared answer, storage is decided by whichever Component looks at the definition first, and a definition that exists only to carry meaning through the application ends up as a table nobody asked for.

**Boundary:** The declaration states that a Domain Definition is stored, not how, where, or under what physical structure it is stored. Database owns the storage decision the declaration permits.

<br>

### Each Domain Definition stands in its own module

**Rule:** Every Domain Definition is declared in a module of its own, carrying that one definition together with what belongs to it alone. A module never gathers several Domain Definitions. The Public Interface publishes each definition under its own unambiguous identity, so a consumer reaches a Domain Definition by what it is rather than by which module it was declared in.

**Why:** A concept that shares a module with others cannot be found, read, reviewed, or changed on its own, and every change to one of them becomes a change to the place all of them live. Separation keeps the boundary between two domain concepts visible in the structure itself, so the shape of the Model on disk matches the shape of the domain.

**Boundary:** This fixes separation, not layout. The module's name, where it sits, and the mechanism that publishes it through the Public Interface belong to the selected realization and are stated in Model Preferences. Shared mechanism is not divided this way: it belongs to Model Foundation, which is a module of its own and not part of any Domain Definition.

<br>

## At a Glance

Every obligation in the file, under the Principle it comes from.

**Each domain concept has one authoritative Domain Definition**

- **Must** — Give every meaningful Target domain concept exactly one authoritative Domain Definition in Model.
- **Never** — Create a Domain Definition solely for an implementation need or independently redefine the same domain identity.

**Model preserves explicit Target meaning**

- **Must** — Preserve every explicit Target definition, property, relationship, constraint, sensitive meaning, and Intrinsic Rule.
- **Must** — Apply Model defaults only to missing properties of existing Fields, property by property.
- **Never** — Let a default add a Field, override an explicit value, change meaning, or invent a relationship or behavior.
- **Never** — Treat Initial Data or another project record as a Model-owned Domain Definition.
- **Must** — Take what the domain is — which Domain Definitions and Fields exist, their names, and their relationships — only from the Target.
- **Must** — Choose an unstated technical modelling parameter of an existing Field under Model's own Principles, and record a consequential choice so it can be reviewed.
- **Never** — Let such a choice add, remove, or rename a Field or relationship, override an explicit Target value, or change what a Field means.
- **Must** — Preserve each Target-declared credential classification and its required at-rest treatment, so Database can apply it and reject a persisted credential whose treatment is missing or unsupported.
- **Never** — Infer credential policy from a field name.

**Logical Model meaning is independent of implementation technology**

- **Must** — Keep Domain Definitions and Intrinsic Rules understandable independently of implementation technology.
- **Must** — Require every selected technology to preserve logical Model meaning.
- **Must** — Take every technical and platform choice from Development; Model never selects one itself.

**Concrete Model realizations share one Model Foundation**

- **Must** — Give every concrete Model realization applicable shared mechanisms through one Model Foundation without imposing Fields or relationships.
- **Never** — Require one particular realization mechanism for Model Foundation.

**Model exposes an explicit and stable Public Interface**

- **Must** — Expose every authoritative Domain Definition with one unambiguous identity through Model's explicit, stable Public Interface.
- **Never** — Let consumers depend on Model's private internal resources.
- **Never** — Treat the conceptual example as fixed technical syntax or evolve the Public Interface outside Development's change-propagation rules.

**Intrinsic validation and domain behavior are deterministic and side-effect free**

- **Must** — Keep Intrinsic validation and domain behavior deterministic, dependent only on Model data, and free of external I/O and unrelated side effects.
- **Never** — Treat an externally contextual rule as intrinsic or let Model orchestrate a workflow.

**Model names express domain meaning**

- **Must** — Name Model concepts from Target domain meaning.
- **Never** — Name a Model concept after an implementation tool or consumer-specific representation unless that name is itself a Target concept.

**Model remains separate from external concerns**

- **Never** — Let Model own Initial Data, persistence, transport, presentation, workflow orchestration, technical selection, platform operation, or another concern outside its logical boundary.
- **Must** — Keep external realization outside Model ownership even when another Component consumes Model data or its Public Interface.

**Model declares every definition in one standard, technology-independent vocabulary**

- **Must** — Express every Domain Definition in one standard, technology-independent vocabulary: type, length and precision, nullability, default, identity, uniqueness, constraints, and relationships.
- **Never** — Fix a closed list of types or sizes; Model decides them from the Target.
- **Must** — Carry that vocabulary in the same Domain Definition that application code uses, so every Component — Database among them — reads it through the Model Public Interface.
- **Never** — Maintain a separate schema artifact beside the Domain Definition as Database's source.
- **Must** — Preserve each Target Field's declared required, nullable, default, generated, and absence semantics.
- **Never** — Invent an absence state, default, generation mechanism, or partial-update semantics.
- **Never** — Put tables, indexes, migrations, SQL, ORM mappings, or Engine-specific constraints in Model.

**A Domain Relationship carries the definition it refers to**

- **Must** — Carry the referenced Domain Definition itself in a relationship, so an unresolvable reference fails where it is written.
- **Never** — Stand a name in for a referenced Domain Definition, or treat technology independence as a reason to leave a reference untyped.
- **Must** — State each relationship's cardinality and optionality from the Target rather than leaving either to a default.

**Every Domain Definition converts to and from a Plain Representation**

- **Must** — Offer `serialize` and `deserialize` on every Domain Definition, provided once through Model Foundation.
- **Must** — Return simple named values from `serialize`, leaving the wire format to the consumer.
- **Must** — Evaluate the Domain Definition's Intrinsic Rules during `deserialize` and fail when they are not satisfied.
- **Never** — Nest a related Domain Definition in a Plain Representation; a Domain Relationship appears only as its declared reference value.
- **Never** — Withhold a Field inside Serialization; output policy belongs to the consuming Component.

**Every Domain Definition declares whether it is persistent**

- **Must** — Declare every Domain Definition as `persistent` or `non-persistent`.
- **Never** — Infer persistence from a Domain Definition's existence, name, or identity Field.
- **Never** — Decide in Model how, where, or under what structure a persistent Domain Definition is stored.

**Each Domain Definition stands in its own module**

- **Must** — Declare every Domain Definition in a module of its own, carrying that definition and what belongs to it alone.
- **Never** — Gather several Domain Definitions into one module.
- **Must** — Publish each Domain Definition through the Public Interface under its own identity, independent of the module it was declared in.
