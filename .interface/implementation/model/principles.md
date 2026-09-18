# Model Principles

Model defines the authoritative logical meaning of the Target's domain through reusable Domain Definitions. It preserves domain identity, fields, relationships, rules, and behavior as one coherent Model boundary with an explicit Public Interface.

Model owns domain meaning and behavior determinable from its own data. Model is the shared language between every Component of the application.

<br>

> **Note:** Model is not limited to Domain Fields. It preserves the conceptual identity, relationships, defaults, and field constraints declared by the Target, expressed in one standard technology-independent vocabulary, so that every Component — Logic, API, Presentation, and Database alike — reads the same definition. Database deriving its persistence structure from Model is one use of that vocabulary, not its purpose.

<br>

## Terms

- **Domain Definition** — the authoritative logical definition of one meaningful concept in the Target's domain.
- **Field** — one named property of a Domain Definition, with its domain meaning and applicable constraints.
- **Model Foundation** — the technology-independent common foundation through which concrete Model realizations receive shared mechanisms without inheriting domain Fields or relationships.
- **Intrinsic Rule** — a domain rule that can be evaluated entirely from the data of the Domain Definition it governs.
- **Domain Relationship** — a logical association between Domain Definitions whose meaning and constraints come from the Target.

<br>

## Relationships

- **Consumes Development** — uses its Component Profile, shared rules, technical items, and Platform Reference.
- **Consumed through Development-defined Connections** — provides its Public Interface without repeating the identities or internal behavior of its consumers.

<br>

Model-owned defaults and implementation conventions belong to Model Preferences. Model's configurable identity and all technical or Platform references belong to its Component Profile in Development Preferences. Implementation applies those sources to the current Target definition.

<br>

Every statement here is mandatory. A Implementation Preference can never override a Principle, and a project may only add stricter rules, never looser ones.

<br>

## 1. Each domain concept has one authoritative Domain Definition

**Rule:** Every meaningful domain concept resolved from the Target has exactly one authoritative Domain Definition in Model. A Domain Definition originates in domain meaning rather than the needs of an implementation tool or consumer, and the same domain identity is never independently redefined elsewhere.

**Why:** One logical authority gives every authorized consumer the same meaning and prevents competing definitions from drifting apart.

**Boundary:** An implementation-only structure with no independent domain meaning does not require a Domain Definition merely because a tool or consumer uses it.

<br>

## 2. Model preserves explicit Target meaning and invents nothing

**Rule:** Model preserves every explicit Domain Definition, Field, property, Domain Relationship, constraint, sensitive or credential meaning, and Intrinsic Rule stated by the Target. Model Preferences may complete only missing properties of existing Fields, property by property. A default never creates a Field, overrides an explicit value including `false` or `null`, changes meaning, or invents a relationship or behavior. Every Domain Relationship preserves the meaning and constraints declared by the Target.

**Why:** The Target remains authoritative for what the domain means while reusable defaults can safely complete genuinely unstated details.

**Boundary:** Project records, including Initial Data, are not Domain Definitions and are not owned or introduced by Model.

<br>

## 3. Logical Model meaning is independent of implementation technology

**Rule:** Every Domain Definition and Intrinsic Rule remains understandable independently of a specific language, package, tool, version, runtime, or platform mechanism. A selected technology may realize Model concepts only while preserving their logical meaning.

**Why:** Technology can change without redefining the Target's domain.

**Boundary:** Technology independence does not prevent the Model Component Profile in Development Preferences from selecting concrete compatible technical and Platform references.

<br>

## 4. Concrete Model realizations share one Model Foundation

**Rule:** Every concrete Model realization receives applicable shared Model mechanisms through one Model Foundation. The Foundation may provide validation, serialization, and metadata-publishing mechanisms, but it never owns, injects, or requires a Field or Domain Relationship. Each Domain Definition declares its own complete set of Fields and relationships from the Target.

**Why:** A single common foundation keeps cross-Model mechanisms consistent without imposing fields or domain meaning on a Domain Definition.

**Boundary:** Model Foundation does not require a base class, inheritance, or any other particular realization mechanism; the selected technology determines the compatible form. Shared implementation does not imply shared domain Fields.

<br>

## 5. Model exposes an explicit and stable Public Interface

**Rule:** Model exposes its authoritative Domain Definitions through one explicit and stable Public Interface. Consumers use that surface rather than private internal resources, and each public Domain Definition has one unambiguous public identity.

Conceptual example:

```text
model.<public_module>.<ModelType>
```

**Why:** A clear public boundary makes Model reusable while allowing its private organization to evolve.

**Boundary:** The example does not fix a language, import syntax, file layout, or re-export mechanism. Public Interface evolution remains governed by Development's change-propagation rules.

<br>

## 6. Intrinsic validation and domain behavior are deterministic and side-effect free

**Rule:** Model validates only Intrinsic Rules. Every validation, derived value, serialization behavior, and other domain behavior depends only on the applicable Model data, produces a deterministic result for the same input, performs no external I/O, and creates no unrelated side effect.

**Why:** Local deterministic behavior keeps Model independent, predictable, reusable, and directly testable.

**Boundary:** A rule requiring external or operation-specific context is not an Intrinsic Rule, and Model never orchestrates an application workflow.

<br>

## 7. Model names express domain meaning

**Rule:** Every Domain Definition, Field, Domain Relationship, and other public Model name expresses the meaning stated by the Target rather than an implementation tool or a consumer-specific representation.

Conceptual example:

```text
<DomainConcept>       preferred
<DomainConcept>DTO    not a domain name unless DTO is itself a Target concept
```

**Why:** Domain-oriented names keep the logical model understandable without knowledge of a technical realization.

**Boundary:** Language-level casing and file or folder naming conventions come from the applicable Development technology profile.

<br>

## 8. Model remains separate from external concerns

**Rule:** Model never owns Initial Data, persistence, transport, presentation, workflow orchestration, technical selection, platform operation, or any other concern outside its logical domain boundary.

**Why:** A narrow boundary keeps Model reusable and prevents external concerns from changing or obscuring domain meaning.

**Boundary:** A separate Component may consume Model's Public Interface or realize an external concern using Model data, but that use does not transfer ownership to Model.

<br>

## 9. Model declares every definition in one standard, technology-independent vocabulary

**Rule:** Model expresses every Domain Definition through one standard vocabulary that belongs to no language, package, or Engine: the logical field type (for example integer, string, decimal, boolean, datetime), length and precision where the Target declares them, nullability, default, primary-key identity, generated identity, uniqueness, single-field or composite constraints, and relationships with their referenced Domain Definition, cardinality, and optionality. Which type or size a field receives is Model's own decision from the Target; the Interface fixes no closed list. This vocabulary is carried by the same Domain Definition that application code uses — there is no second schema artifact — and every Component reads it through the Model Public Interface. Each selected realization determines how that Domain Definition represents the vocabulary in its own technology. Database is one consumer of it: it derives and enforces physical storage structure from these declarations without reinterpreting the Target.

Each Domain Definition also declares whether it is `persistent` or `non-persistent`. Database stores only Domain Definitions that Model declares as persistent and never infers persistence from the existence or name of a Domain Definition.

Model preserves whether each Target Field is required, nullable, defaulted, generated, or otherwise allowed to be absent. An omitted Field is resolved according to the explicit Target declaration or the selected realization's compatible rules; Model never invents an absence state, default, or generation mechanism. Preserving the Target's declared presence semantics prevents a generic Model rule from changing Domain meaning. Model defines no partial-update semantics and does not choose how a realization represents omitted values. *(merged from former Principle 6, 2026-09-18)*

**Why:** One vocabulary understood without any technology lets every Component share the same definition, and gives Database a precise source for persistence guarantees while Model remains the single authority for domain meaning.

**Boundary:** Model does not create tables, indexes, migrations, SQL, ORM mappings, or engine-specific constraints, and it does not enforce rules that require comparing multiple stored records. Database owns physical realization and enforcement.

Model also preserves each Target-declared credential classification and required at-rest treatment. Database applies that declared treatment and rejects a persisted credential whose treatment is missing or unsupported; neither Component infers credential policy from a field name.

<br>

## At a Glance

- **Must** — Give every meaningful Target domain concept exactly one authoritative Domain Definition in Model. *(1)*
- **Never** — Create a Domain Definition solely for an implementation need or independently redefine the same domain identity. *(1)*
- **Must** — Preserve every explicit Target definition, property, relationship, constraint, sensitive meaning, and Intrinsic Rule. *(2)*
- **Must** — Apply Model defaults only to missing properties of existing Fields, property by property. *(2)*
- **Never** — Let a default add a Field, override an explicit value, change meaning, or invent a relationship or behavior. *(2)*
- **Never** — Treat Initial Data or another project record as a Model-owned Domain Definition. *(2)*
- **Must** — Keep Domain Definitions and Intrinsic Rules understandable independently of implementation technology. *(3)*
- **Must** — Require every selected technology to preserve logical Model meaning. *(3)*
- **Must** — Take Model's language, modeling package, Agent Skills, and Platform Reference from its Component Profile in Development; Model never selects a technology itself. *(3)*
- **Must** — Give every concrete Model realization applicable shared mechanisms through one Model Foundation without imposing Fields or relationships. *(4)*
- **Never** — Require one particular realization mechanism for Model Foundation. *(4)*
- **Must** — Expose every authoritative Domain Definition with one unambiguous identity through Model's explicit, stable Public Interface. *(5)*
- **Never** — Let consumers depend on Model's private internal resources. *(5)*
- **Never** — Treat the conceptual example as fixed technical syntax or evolve the Public Interface outside Development's change-propagation rules. *(5)*
- **Must** — Keep Intrinsic validation and domain behavior deterministic, dependent only on Model data, and free of external I/O and unrelated side effects. *(6)*
- **Never** — Treat an externally contextual rule as intrinsic or let Model orchestrate a workflow. *(6)*
- **Must** — Name Model concepts from Target domain meaning. *(7)*
- **Never** — Name a Model concept after an implementation tool or consumer-specific representation unless that name is itself a Target concept. *(7)*
- **Must** — Take language-level casing and file or folder naming conventions from the applicable Development technology profile. *(7)*
- **Never** — Let Model own Initial Data, persistence, transport, presentation, workflow orchestration, technical selection, platform operation, or another concern outside its logical boundary. *(8)*
- **Must** — Keep external realization outside Model ownership even when another Component consumes Model data or its Public Interface. *(8)*
- **Must** — Express every Domain Definition in one standard, technology-independent vocabulary: type, length and precision, nullability, default, identity, uniqueness, constraints, and relationships. *(9)*
- **Never** — Fix a closed list of types or sizes; Model decides them from the Target. *(9)*
- **Must** — Carry that vocabulary in the same Domain Definition that application code uses, so every Component — Database among them — reads it through the Model Public Interface. *(9)*
- **Never** — Maintain a separate schema artifact beside the Domain Definition as Database's source. *(9)*
- **Must** — Preserve each Target Field's declared required, nullable, default, generated, and absence semantics. *(9)*
- **Never** — Invent an absence state, default, generation mechanism, or partial-update semantics. *(9)*
- **Must** — Declare every Domain Definition as `persistent` or `non-persistent`. *(9)*
- **Never** — Infer persistence from a Domain Definition's existence or name. *(9)*
- **Never** — Put tables, indexes, migrations, SQL, ORM mappings, or Engine-specific constraints in Model. *(9)*
