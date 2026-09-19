# Development Understanding

How the Human explained this Component, in their own words, and what was decided along the way. The Principles state what holds; this file preserves how they were arrived at. It states no obligation: where this record and a Principle disagree, the Principle is correct.

<br>

## Documentation

**What is documentation for, in the Human's words?** Documentation is a Development concern: every new Component starts from Development, and there it must learn how to document itself. Each Component's Preferences names where its documentation lives — a path inside the Component's own project. The README goes from the general to the specific: first an overview, then the details; it always gives examples; it explains setup and how to run; it names the capabilities that can be executed; it explains the different classes and objects. Each Component does this through its own mechanism. The measure is that anyone who reads the README understands how that Component or module works.

**Where it lives, and why not a separate section.** The Principles Schema fixes the shape of every Principles file and sends the shape of a generated file to a Schema or Preferences, so the concept stays inside Development: Principle "Every Component has complete, safe, and operational documentation" carries the rule and the Human's view; Development Preferences carry the conventions once for all Components (`settings.documentation`: file, location, order, examples, per-Component fulfilment, secrets, authority) and each Component Profile carries its `documentation` path. Documentation is Development-specific for now; a Foundation-level README Schema is not needed until another Module needs the same shape.

**Why this came up.** After the first Implement run, `model/` and `database/` were generated without a README although Principle "Every Component has complete, safe, and operational documentation" required one — Planning had scoped "applicable obligations" to the phase's own Component, and the phrase "at the root selected by its Component Profile" pointed at a key the Profile did not have. Both are now closed: the Profile has the key, the Principle names it, and the Agent Module's placement rule keeps the obligation from being narrowed in the synchronized Skills.
