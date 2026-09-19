# Logic Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this file preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

## Logic

**What is Logic, in the Human's words?** Logic is the layer of reasoning: the logic, the functionality, the behaviours and the routines of the application are designed here. It is the hub of the Implementation — Model, Database and the consumers turn around it. It is not executable; it is a library.

**Who talks to it?** A consumer states what it wants done and Logic does the rest. The API is one consumer: it runs the server, receives the request and tells Logic. Tomorrow a command-line entry point, or another Component, is a consumer in the same way. Whoever wants to enter or change data for a Model asks Logic, never Database or Model directly.

**What does it talk to?** Logic talks to Model to understand the Domain Definitions and build on them, to Database to reach stored data, and later to further Components — Binance, MT5, Log, Report — each of which will be its own Component.

**How is it reached?** Nobody outside reaches Logic's internal parts. Logic has one Public Interface; it groups its Operations into Categories — Data Entry is one of them — and offers Operations: a consumer names the Operation and gives what it needs — the Model and the data for a data-entry Operation, the instrument and the parameters for opening an MT5 position — and Logic decides what to read from Model, what to ask of another Component, what to do, and what to answer. One Operation may use several internal Services.

**How does it reach the others?** Logic reaches any other Component only through that Component's Public Interface and the Operations it offers — Model for domain meaning, Database for stored data, and every Component that follows. The Service that owns a dependency holds those calls: the Database Service is where the Operations of Database's Public Interface are used, so an Action there is one call into Database. Logic has no other route out, and there are no separate Logic-side interface names for those boundaries.

**What is inside it?** Inside Logic the work is divided into Services, one per Component Logic talks to and named after it: a Database Service for the part of the reasoning that speaks to Database, and later an MT5 Service, a Binance Service, a Log Service, a Report Service. Services are internal — invisible from outside — and each performs Actions.

**Operations and Actions.** An Operation is the larger unit, offered by the Public Interface; an Action is the step a Service performs. Operations are composed of Actions. The Database Service performs create, update, enable, disable, delete, list, count, sum, min, max, truncate and execute command — the last one reaching Database's own capability-restricted command route for work the other Actions cannot express.

**The Data Entry Operations.** The Data Entry Category offers create, list, update, delete, enable, disable, count, sum, min, max and truncate. list carries the reading work: it takes filters — id among them, so reading one record needs no Operation of its own — an order_by field and direction, and a limit. enable sets is_active true and disable sets it false; they stay two Operations rather than one with a flag. count, sum, min and max each take filters, and sum, min and max also take the field they work on. truncate empties a Model of its records while leaving its structure in place. The names follow REST and data-library convention rather than Interface-invented ones.

**Decisions:**

1. Logic's architecture is the Public Interface with its Categories and Operations, and the internal Services with their Actions. This replaces an earlier structure of a Logic Foundation, one Model Logic unit per Model inheriting from it, and a separate Use Case Logic unit for cross-Model Behaviour. The internal structure of each Service stays deliberately open.
2. That architecture is Logic's own. No named external standard is selected for it — an earlier choice of Hexagonal, with Clean as an alternative, and the policy requiring conformance to it, are not kept.
3. No consumer is named or privileged. Anything can talk to Logic through its Public Interface. An earlier statement that the API Component consumes it is not kept, because it read as a restriction that does not exist.
4. Logic reaches every other Component through that Component's own Public Interface, from the Service that owns the dependency. There are no separate Logic-side names for those boundaries; earlier Model Interface and Database Interface terms are not kept.
5. Public Interface and Operation are meant to become the shared standard of every Implementation Component — Model, Database, API and the rest — declared in Development so documentation can rely on them. Recorded here as the decision that produced it; Development owns the general statement.

**Still open.** Which further Categories and Operations the Public Interface offers, the full Action list of each Service beyond Database, and the internal structure of a Service are not yet decided.
