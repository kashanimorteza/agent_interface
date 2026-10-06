# Definition File Structure

This document is the common structure every Definition file follows. It defines the shape of a Definition file, not the content of any Implementation or Executor Component. Each owner describes itself inside this shape so that every Definition file is written, read, and reasoned about the same way.

One Definition file exists per Implementation Component at `.interface/implementation/<subsystem>/<component>/<component>.md` — for example `.interface/implementation/development/model/model.md` — and per Executor Component at `.interface/executor/<component>/<component>.md`. Each file is human-owned and never written by an Interface operation. Operational Skills read applicable Implementation Definitions; only explicitly Human-invoked Agent Native Implement reads Agent Definitions, then realizes them as Runtime artifacts consumed by every other Skill.


<!--------------------------------------------------------------------------------- Purpose --->
<br>

## Purpose

A Definition file exists to raise understanding of the project. It answers what its owning Component or Module is, what responsibility it holds, and under which mandatory rules it operates, so that any reader — human or Agent — can reason about that owner without inspecting an implementation.

An Implementation or Executor Component describes its own responsibilities, boundaries, and relationships with other Components, including what it consumes and provides. What such a file may and may not carry is stated once, in Scope.


<!--------------------------------------------------------------------------------- Scope --->
<br>

## Scope

A Definition file carries two kinds of content: what a reader must understand about the Component, and the mandatory rules it operates under. It carries nothing else. It is independent of specific implementation tools, versions, providers, and any particular project. Architectural concepts such as packages, modules, layers, roles, capabilities, and their ownership and public interfaces are permitted. Agent Skill Definitions additionally name the Skills the architecture requires and state each Skill's What, Why, scope, and boundary; Operation-backed Skill behavior belongs to its owning Implementation Operation Component, while Agent Skill Preferences hold the Agent-side bridge. A conditional external Skill may name the technology it serves without selecting that technology for a Target.

A Definition file never contains:

- a specific tool, library, framework, engine, third-party package, or version selection; Implementation choices belong to Implementation Preferences and Agent declarations belong to the owning Executor Preferences, except that Agent Skill Definitions may name a required or conditional Skill and the technology category that activates it without making the technology selection;
- a technical default or resolved technical choice, which belongs to Implementation Preferences or the owning Executor Preferences;
- the shape of any generated file, including a documentation file, which belongs to the Component's Schema when one exists or to the Preferences that own that file; or
- instructions assigning roles to Skills or Agents, prescribing their Workflows, or deciding which Skill reads the Component and when.

Operation-backed Skill behavior belongs to its owning Implementation Operation Component, not to Agent Skill Preferences or Agent Skill Definitions. Agent Skill Preferences declare only the Agent-side bridge, invocation, and Runtime boundary.

Relationships between Components are permitted and belong in Relationships. They describe what each Component consumes or provides without directing a Skill's execution.

Three rules follow from this Scope and hold in every part of the file, so no part restates them. **No tool, package, version, file, directory, or layout is ever named**, except where Scope's own exception for Agent Skill Definitions applies; a part that would need one describes the concept instead. **Only a Principle states an obligation**: every other part explains, records, or maps, and a sentence a reader would have to obey belongs in a Principle's Rule wherever it was written. **A Definition describes only its own Component**: it never states how another Component uses it, and never states what another Component owns or does. A Component that consumes another describes that use in its own Definition, so each Component keeps its own identity and stays general.

A Principle is portable: the same file can be handed unchanged to another project or another Agent.


<!--------------------------------------------------------------------------------- Structure --->
<br>

## Structure

A Definition file carries these parts, in this order. A part marked *optional* is carried by a Component that has something to say there and omitted — not left empty — by one that does not:

1. **Title** — the file's single first-level heading.
2. **Opening Summary** — one short paragraph introducing the owning Module, Subsystem, or Component before the reader enters the file's map.
3. **Navigation** — the map of the file's own sections.
4. **Introduction** — everything a reader needs in order to understand the Component, in four parts:
   - **Overview** — what the Component is and what it contributes.
   - **Purpose** — the problem it solves and what is lost without it.
   - **How It Works** — how it does that work, told as a flow rather than as rules.
   - **Decisions** — how the Human explained the Component and the decisions that followed, once that explanation is folded into the three parts above. *(optional)*
5. **Terms** — the vocabulary the Component owns.
6. **Architecture** — the named parts the Component is formed from. *(optional)*
7. **Relationships** — what it consumes and what consumes it.
8. **Boundaries** — the work that looks like this Component's but belongs elsewhere. *(optional)*
9. **Layering** — where the Component's technical choices live instead.
10. **Authority** — the binding force of the file and its precedence.
11. **Principles** — the mandatory rules.
12. **Operation Contract** — the operational contract of an Operation Component, when the Component is an executable Operation. *(optional)*
13. **At a Glance** — the derived list of every obligation in the file.

The Opening Summary is the file's one-line orientation: it names what the owner is and where it belongs, without explaining the file's structure or stating a Principle. Navigation follows it so the reader sees the whole shape before entering the content. Introduction is everything a reader has to take in before the rules mean anything, so it comes first, and its own Decisions part closes it, because how the Human arrived here is still context for the rules rather than one of them. What follows it is reference: the vocabulary, the parts, the edges, and the rules themselves.

Overview, Purpose, and How It Works are always carried; Decisions is carried only by a Component whose recorded decisions need to be preserved; Operation Contract is carried only by an executable Operation Component whose operational contract needs to remain explicit for its Skill. The Opening Summary is unheaded and carries no Navigation entry. Navigation, Introduction, Terms, Architecture, Relationships, Boundaries, Layering, Authority, Principles, Operation Contract, and At a Glance carry their own second-level heading. Introduction's four parts and each Principle category carry third-level headings; each Principle carries a fourth-level heading under its category. A second-level heading therefore always names a section, a third-level heading names one member or category of that section, and a fourth-level heading names one Principle. No `<br>` appears between Introduction's parts; a `<br>` separates each Principle category from the next. No `<br>` appears between sibling Principles within the same category, and no blank line or `<br>` separates a Principle's Rule, Why, and Boundary.


<!--------------------------------------------------------------------------------- Title --->
<br>

## Title

The file opens with one first-level heading naming the Component:

```markdown
# <Component> Definition
```

No other first-level heading appears in the file.


<!--------------------------------------------------------------------------------- Opening Summary --->
<br>

## Opening Summary

The Opening Summary is written as one unheaded paragraph immediately after the Title and before Navigation. It introduces the owning Module, Subsystem, or Component in one short sentence, without describing the document, repeating the Introduction, or stating an obligation. The paragraph has no Navigation entry.


<!--------------------------------------------------------------------------------- Navigation --->
<br>

## Navigation

The map of the file's own sections, so a reader — and an Agent looking for one part of it — sees the whole shape before reading any of it.

A numbered list, one line per section the file actually carries, each linking to that section's heading. Nothing else: no description beside an entry, and no entry for a section the file omits. No entry carries subentries: neither Introduction's parts nor individual Principles are listed beneath their section:

```markdown
## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[Operation Contract](#operation-contract)**
10. **[At a Glance](#at-a-glance)**
```

Navigation is rewritten whenever a section is added, removed, or renamed, like At a Glance.


<!--------------------------------------------------------------------------------- Introduction --->
<br>

## Introduction

Everything a reader needs in order to understand the Component, before any rule is stated. It carries four parts, each under its own third-level heading; the fourth is optional.

### Overview

The Component introduces itself: what it is, the responsibility it holds, what it contributes to the project, and what it is independent of. It takes as many paragraphs as that needs.

It is written about the Component, never about the document: it begins by defining the Component, not by describing what the file contains. It states what the Component *is* and *does*. Relationships with other Components belong in Relationships.

The Component's own boundary — what it does not own — is stated explicitly, either as the closing sentences of Overview or as one dedicated Principle. It is never left implicit and never stated in both places.

### Purpose

The reason this Component is a Component at all: the problem it solves, what its separation makes possible, and what would go wrong if its work were spread across the others instead.

It is written about the design rather than about the document, and takes as many paragraphs as the reason needs. It answers the question a reader asks before any rule makes sense — *why is this a thing of its own?* — so that every Principle that follows reads as a consequence of that reason rather than as an arbitrary constraint.

It names the cost of the alternative concretely: not "for separation of concerns", but what actually happens when the same knowledge lives in three places, or when a consumer reaches past this Component to the one behind it. A reader who understands this part can judge a case the Principles do not cover.

Each Principle's own **Why** explains that one rule. This part explains the Component. Neither repeats the other.

### How It Works

How the Component does its work, told as a flow: what reaches it, what it does with it, what it hands on, and what comes back. It is the narrative a newcomer needs in order to picture the Component in motion before meeting its vocabulary and its rules.

It stays at the level of concepts the Component owns. Where a Component's flow is genuinely trivial, this part is a short paragraph or two rather than an invented elaboration.

### Decisions

How the Human explained the Component, once that explanation has been folded into Overview, Purpose, and How It Works above, and the decisions it led to. This part carries only what those three do not already hold: the decisions themselves, each stated close to how the Human said it, including a proposal that was not accepted and the reason it wasn't — so it is not proposed again:

```markdown
### Decisions

**<Subject>**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why — so it is not proposed again>

**<Subject>**

...
```

One bold subject lead-in per settled question, in the order the subjects were settled, each followed by its own numbered list. It carries no dates and is written in the present tense: it states what holds now and what it replaces, and is rewritten when the Human's understanding changes — it is the current picture, not a log of when each part of it arrived.

This part is a record, never an authority: it states no obligation, and nothing in it reaches At a Glance. Where it and a Principle disagree, the Principle is correct and the record is out of date. It is optional, and a Component whose Understanding has not been recorded omits it.


<!--------------------------------------------------------------------------------- Terms --->
<br>

## Terms

A short definition list of the terms the Definition owner owns — the capitalized concepts its Principles use and that a reader would otherwise have to infer from the prose.

```markdown
## Terms

- **<Term>** — <one sentence defining it within this Definition owner>
```

A term is listed only when this Principles owner owns it. A term owned by another Component or Module is used as that owner defines it and is not redefined here. Terms defined by the Interface itself, such as Component, Principle, and Preference, are not repeated in an owner's list.


<!--------------------------------------------------------------------------------- Architecture --->
<br>

## Architecture

The named parts the Component is formed from, and how they stand in relation to one another. It answers, in one view, what is inside this Component — before Relationships answers what is outside it.

The section opens with a tree naming the parts, followed by a short paragraph or two per part stating what it owns and, where it matters, what it never does:

```markdown
## Architecture

```text
<Component>
├── <Part>
│   └── <Sub-part>
└── <Part>
    └── <Sub-part>
```

<A paragraph or two per part: what it owns, and the limit that keeps it distinct from the others.>
```

The tree names concepts the Component owns: a repository layout belongs to the Component's Preferences. A part named here is governed by a Principle, and it is defined in Terms when this Component owns the term; a part whose term another Component owns — a Public Interface, for example — is used as that owner defines it and is not redefined in Terms. Architecture shows how the parts fit together.

A Component formed from named parts — internal layers, services, foundations, a public boundary — carries it. One with no internal structure worth naming omits the section entirely rather than carrying an empty one.


<!--------------------------------------------------------------------------------- Relationships --->
<br>

## Relationships

A short list naming the Components or Modules this Definition owner consumes, each with what it takes and how. It never names the Components that consume this owner: each consumer describes that use in its own Definition.

```markdown
## Relationships

- **Consumes <Component>** — <what it takes and how>
```

Relationships are stated between Components and Modules only. No Skill, operation, Mode, or Workflow step appears here. An owner that consumes nothing records that fact rather than inventing a connection.


<!--------------------------------------------------------------------------------- Boundaries --->
<br>

## Boundaries

The work that looks like this Component's but is not, each with the reason the line falls there. The entry never names the Component that owns that work.

Relationships says what this Component consumes. Boundaries says where a reader — human or Agent — is most likely to put something in the wrong place, and settles it in advance:

```markdown
## Boundaries

- **<the work that looks like this Component's>** — is not this Component's, because <what puts it outside>.
```

Each entry is a case that has actually caused confusion or plausibly would: a rule that could be read as this Component's, a setting it could wrongly claim, a concern whose name suggests it belongs here. An entry states the reason, so the same reasoning settles the next case that is not listed.

It is not a restatement of the Component's boundary sentence in Introduction or of a Principle's own **Boundary**. A Component carries it when its edges are genuinely easy to cross and omits the section when they are not.


<!--------------------------------------------------------------------------------- Layering --->
<br>

## Layering

One or two paragraphs placing the Component's technical choices outside this file, and naming what holds them:

- an Implementation Component's technical choices and defaults belong to its Implementation Preferences, and an Executor Component's declarations and native mappings belong to its Executor Preferences;
- implementation applies those choices to the current project definition; and
- when the Component owns a generated file, the shape of that file belongs to its Schema.

A Component still states where its technical choices or declarations belong even when its Implementation Preferences or Executor Preferences contain no entries. Explicit absence is not a reason to omit the layering statement.

Layering may carry one third-level heading per layer, explaining what the layer is and how it is built, as concepts only. It names no language, package, file, or language construct such as a class; those details live in the development section of the Component's Preferences. An obligation about a layer is stated as a Principle, not here.


<!--------------------------------------------------------------------------------- Authority --->
<br>

## Authority

One or two paragraphs, stating all three of:

- every Principle in the file is mandatory — the claim is about the Principles, not about every sentence in the file, since Introduction, Terms, Architecture, Relationships, Boundaries, and other explanatory sections explain rather than oblige;
- an Implementation Preference or Executor Preferences can never override a Principle; and
- a project may only add stricter rules, never looser ones.

No Definition file omits or weakens any of the three.


<!--------------------------------------------------------------------------------- Principles --->
<br>

## Principles

The section that carries the file's mandatory rules. It opens with one or two short sentences stating that each rule below is mandatory, then groups the Principles by the Component parts named in Architecture and Layering. Cross-cutting Principles that belong to the Component as a whole are grouped under `General`; a Component with no Architecture groups them by coherent domain area instead. No Principle remains uncategorized.

Every Development Component also carries a `Review` category, placed last. It holds everything the Review Operation checks to establish that the Component was realized as its Principles and Introduction describe: what conformance means for this Component, and the fixed observations that prove it. Every checking or verification rule of the Component lives there and nowhere else in the file, and it states what is observed, never the command, tool, or code that observes it. The Plan and Develop Operations check nothing; Review reads this category.

Each category is a third-level heading. Each Principle is a fourth-level heading under its owning category, carrying its title followed by three labelled subsections:

```markdown
## Principles

<One sentence: every Principle below is mandatory.>

### <Category>

#### <Title>

**Rule:** <the mandatory statement>
**Why:** <the reason the rule exists>
**Boundary:** <the limit of the rule>
```

Adjacent Principles in the same category follow one another without a `<br>`. Each category after the first is preceded by one `<br>` separating it from the preceding category. Rule, Why, and Boundary remain consecutive inside one Principle, with neither a blank line nor a `<br>` between them.

### Title

The category title names the owning Architecture or Layering part exactly, or names the coherent domain area when no such part exists. The Principle title states the rule as a claim, not as a topic: `Data Access is the only Logic route to Database`, not `Data Access`. It is read alone in a list of Principles and still communicates the rule, and it is how the Principle is cited — a Principle carries no number, so its title is its identity and is written to stay accurate if the rule is reworded.

### Rule

The mandatory statement itself, written in the present tense as something that holds rather than something to do. It uses the binding words — *is*, *must*, *only*, *never*.

The Rule may be one sentence or several, and may carry a list when the rule enumerates parts, such as the layers a Component is formed from or the values a field accepts. It states the rule completely; a reader who reads only the Rule subsections of a file has read every obligation the file imposes.

### Why

The reason the rule exists: what it protects, what it makes possible, or what breaks without it.

### Boundary

The limit of the rule: what it does not authorize, the adjacent responsibility it must not absorb, the case it does not reach, or the decision it leaves to another authority.

Every Principle has one, because a rule with no stated limit is read as unlimited. When the limit is that no exception exists, Boundary says so.

### Order

Categories and Principles carry no number. A Principle is identified and cited by its title, so it can be reordered, reworded, or removed without breaking a citation anywhere else.

Categories follow the reading order established by Architecture and Layering, with `General` first when present. Within a category, Principles are ordered so that the ones establishing the part's own shape come before the ones governing its relationships, following the reading path a newcomer needs rather than importance. A new Principle is placed in its owning category where it reads best rather than appended, and Navigation and At a Glance are rewritten to match.



<!--------------------------------------------------------------------------------- At a Glance --->
<br>

## At a Glance

The closing section: every obligation in the file, one line each, gathered under the same category and Principle it comes from.

```markdown
## At a Glance

Every obligation in the file, under the Principle it comes from.

### <Category>

**<Principle title>**

- **Must** — <the obligation in one line>
- **Never** — <the prohibition in one line>

**<Principle title>**

- **Must** — <the obligation in one line>
```

Each line is labelled **Must** or **Never** and sits under its own Principle's title inside the matching category, so a reader traces a line back by reading the category and heading above it. Categories and Principles follow their order in the Principles section. A Principle contributes as many lines as it has distinct obligations, and every obligation in the file appears exactly once in this list.

This section is derived, never authoritative, and it is rewritten whenever a Principle changes. When the list and a Principle disagree, the Principle is correct.


<!--------------------------------------------------------------------------------- Template --->
<br>

## Template

```markdown
# <Component> Definition

<One short sentence introducing the owning Component before the file's Navigation.>

## Navigation

1. **[Introduction](#introduction)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Boundaries](#boundaries)**
6. **[Layering](#layering)**
7. **[Authority](#authority)**
8. **[Principles](#principles)**
9. **[At a Glance](#at-a-glance)**

## Introduction

### Overview

<What the Component is, the responsibility it holds, what it contributes, what it is
independent of, and what it does not own. As many paragraphs as that needs.>

### Purpose

<The problem this Component solves, what its separation makes possible, and what goes
wrong when its work is spread across the others instead.>

### How It Works

<How the Component does its work, told as a flow: what reaches it, what it does with it,
what it hands on, and what comes back.>

### Decisions

<Omit this whole part when the Component's Understanding has not been recorded.>

**<Subject>**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why — so it is not proposed again>

## Terms

- **<Term>** — <definition within this Definition owner>

## Architecture

```text
<Component>
├── <Part>
└── <Part>
```

<A paragraph or two per part: what it owns and the limit that keeps it distinct. Omit this
whole section when the Component has no internal structure worth naming.>

## Relationships

- **Consumes <Component>** — <what it takes and how>

## Boundaries

- **<work that looks like this Component's>** — is not this Component's, because <the reason>.

<Omit this whole section when this Component's edges are not easy to cross.>

## Layering

<Implementation technical choices and defaults belong to <Component> Preferences; Agent
declarations and mappings belong to <Component> Preferences; implementation realizes them.>

## Authority

Every Principle in this file is mandatory. An Implementation Preference or Executor Preferences can never override
a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

<Every Principle below is mandatory.>

### <Category named from Architecture or Layering>

#### <Title stating the rule as a claim>

**Rule:** <the mandatory statement>
**Why:** <the reason it exists>
**Boundary:** <the limit of the rule>

#### <Title>

**Rule:** ...
**Why:** ...
**Boundary:** ...

<br>

### <Next category>

#### <Title>

**Rule:** ...
**Why:** ...
**Boundary:** ...

<br>

## At a Glance

### <Category>

**<Principle title>**

- **Must** — <obligation>
- **Never** — <prohibition>
```
