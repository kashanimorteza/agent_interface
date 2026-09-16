# Logic Principles

Logic is the independent Logic Component that implements the Target's application Behaviour as a reusable library. It consumes Model and Database Public Interfaces and publishes a Logic Public Interface for the API Component.

These Principles are Target- and technology-independent. Concrete language, package, framework, and Package Management choices belong to Development; API transport and process ownership belong to the API Component.

## Terms

- **Logic** — the Logic part that owns application Behaviour and operation-dependent rules.
- **Logic Foundation** — the shared Logic unit supplying standard Model operations.
- **Model Logic** — one Logic unit centered on one shared Model.
- **Use Case Logic** — a Logic unit coordinating Behaviour across multiple Models or services.
- **Model Interface** — Logic's boundary onto Model's Public Interface.
- **Database Interface** — Logic's boundary onto Database's Public Interface.
- **Application Outcome** — a logical success or expected failure independent of transport and persistence.

## 1. Logic is a reusable library

**Rule:** Logic owns application Behaviour and exposes it through a public Logic Interface. It does not start an HTTP process, own transport schemas, or depend on an API framework.

## 2. Logic owns Behaviour

**Rule:** Logic validates domain state, applies operation and application-context rules, and returns Application Outcomes. Behaviour remains independent of transport and storage.

## 3. Standard Model operations come from one foundation

**Rule:** Each shared Model has one Model Logic unit. The Logic Foundation supplies create, get-by-identifier, list, search, update, enable, disable, and delete when selected by the Model and Target.

## 4. Use Case Logic owns cross-Model Behaviour

**Rule:** Behaviour spanning multiple Models or services belongs to a distinct Use Case Logic unit and never bypasses Model or Database Interfaces.

## 5. Persistence has one boundary

**Rule:** Database Interface is Logic's only route to persistence and forwards grouped operations through Database's transaction boundary. Logic never exposes engines, sessions, mappings, or schema details.

## 6. Model meaning has one boundary

**Rule:** Model Interface imports authoritative public definitions. Logic never copies or redefines Domain Definitions.

## 7. Supporting services remain explicit

**Rule:** Logic consumes only the supporting services and cross-cutting capabilities selected by Development, through explicit interfaces and only where Behaviour requires them.

## 8. Runtime configuration stays private

**Rule:** Logic defines the configuration contract required by its Logic and validates required values before use. Platform supplies runtime values; secrets never enter source, errors, or public interfaces.

## 9. Logic verification covers Logic boundaries

**Rule:** Verification covers isolated Logic, Model Interface, Database Interface, transaction behaviour, outcomes, and every public Logic operation without requiring a live API process.
