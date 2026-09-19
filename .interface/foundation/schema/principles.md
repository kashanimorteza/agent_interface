# Principles File Structure

This document is the common structure every Principles file follows. It defines the shape of a Principles file, not the content of any Implementation or Agent Component. Each owner describes itself inside this shape so that every Principles file is written, read, and reasoned about the same way.

One Principles file exists per Implementation Component at `.interface/implementation/<component>/principles.md` and per Agent Component at `.interface/agent/<component>/principles.md`. Each file is human-owned and never written by an Interface operation. Operational Skills read applicable Implementation Principles; only explicitly Human-invoked Agent Sync reads Agent Principles, then realizes them as Runtime artifacts consumed by every other Skill.


<!--------------------------------------------------------------------------------- Purpose --->
<br>

## Purpose

A Principles file exists to raise understanding of the project. It answers what its owning Component or Module is, what responsibility it holds, and under which mandatory rules it operates, so that any reader — human or Agent — can reason about that owner without inspecting an implementation.

An Implementation or Agent Component describes its own responsibilities, boundaries, and relationships with other Components, including what it consumes and provides. A Principles file does not prescribe a concrete Skill workflow, name current runtime resources, or decide which Skill reads it and when. Interface-owned Skill behavior belongs to its declared Skill Contract conforming to the Skill Contract Schema, not to Agent Skill Principles.


<!--------------------------------------------------------------------------------- Scope --->
<br>

## Scope

A Principles file carries two kinds of content: what a reader must understand about the Component, and the mandatory rules it operates under. It carries nothing else. It is independent of specific implementation tools, versions, providers, and any particular project. Architectural concepts such as packages, modules, layers, roles, capabilities, and their ownership and public interfaces are permitted. Agent Skill Principles additionally name the Skills the architecture requires and state each Skill's What, Why, scope, and boundary; each Interface-owned Skill's complete portable behavior belongs to its Skill Contract. A conditional external Skill may name the technology it serves without selecting that technology for a Target.

A Principles file never contains:

- a specific tool, library, framework, engine, third-party package, or version selection; Implementation choices belong to Implementation Preferences and Agent declarations belong to the owning Agent Preferences, except that Agent Skill Principles may name a required or conditional Skill and the technology category that activates it without making the technology selection;
- a technical default or resolved technical choice, which belongs to Implementation Preferences or the owning Agent Preferences;
- the shape of a generated file, which belongs to the Component's Schema when one exists; or
- instructions assigning roles to Skills or Agents, prescribing their Workflows, or deciding which Skill reads the Component and when.

Relationships between Components are permitted and belong in Relationships. They describe what each Component consumes or provides without directing a Skill's execution.

Introduction's Understanding is the one part that states no obligation: it records how the Human explained the Component, and a reader follows the Principles, not the record.

Documentation states what a reader of the Component's documentation must come away with. The shape of that documentation file, like the shape of any generated file, still belongs elsewhere.

A Principle is portable: the same file can be handed unchanged to another project or another Agent.


<!--------------------------------------------------------------------------------- Structure --->
<br>

## Structure

A Principles file carries these parts, in this order. A part marked *optional* is carried by a Component that has something to say there and omitted — not left empty — by one that does not:

1. **Title** — the file's single first-level heading.
2. **Navigation** — the map of the file's own sections.
3. **Introduction** — everything a reader needs in order to understand the Component, in four parts:
   - **Overview** — what the Component is and what it contributes.
   - **Purpose** — the problem it solves and what is lost without it.
   - **How It Works** — how it does that work, told as a flow rather than as rules.
   - **Understanding** — how the Human explained it, in their own words, with the decisions that followed. *(optional)*
4. **Terms** — the vocabulary the Component owns.
5. **Architecture** — the named parts the Component is formed from. *(optional)*
6. **Relationships** — what it consumes and what consumes it.
7. **Boundaries** — the work that looks like this Component's but belongs elsewhere. *(optional)*
8. **Layering** — where the Component's technical choices live instead.
9. **Documentation** — what this Component's own documentation must convey. *(optional)*
10. **Authority** — the binding force of the file and its precedence.
11. **Principles** — the mandatory rules.
12. **At a Glance** — the derived list of every obligation in the file.

Understanding is everything a reader has to take in before the rules mean anything, so it comes first, gathered under Introduction rather than scattered through the file. What follows Introduction is reference: the vocabulary, the parts, the edges, and the rules themselves.

Overview, Purpose, and How It Works are always carried. Layering and Authority are unheaded prose. Navigation, Introduction, Terms, Architecture, Relationships, Boundaries, Documentation, Principles, and At a Glance carry their own second-level heading. Introduction's four parts and each Principle carry third-level headings, so a second-level heading always names a section and a third-level heading always names one member of it. A `<br>` separates each part from the next and each Principle from the next.


<!--------------------------------------------------------------------------------- Title --->
<br>

## Title

The file opens with one first-level heading naming the Component:

```markdown
# <Component> Principles
```

No other first-level heading appears in the file.


<!--------------------------------------------------------------------------------- Navigation --->
<br>

## Navigation

The map of the file's own sections, so a reader — and an Agent looking for one part of it — sees the whole shape before reading any of it.

A numbered list, one line per section the file actually carries, each linking to that section's heading. Nothing else: no description beside an entry, and no entry for a section the file omits. The Principles are one entry, with each Principle's title listed beneath it:

```markdown
## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
   - **[Understanding](#understanding)**
2. **[Terms](#terms)**
3. **[Architecture](#architecture)**
4. **[Relationships](#relationships)**
5. **[Principles](#principles)**
   - **[<Title>](#title)**
   - **[<Title>](#title)**
6. **[At a Glance](#at-a-glance)**
```

Introduction's own parts are listed beneath it. Layering and Authority are unheaded prose and carry no entry. Navigation is rewritten whenever a section or a Principle is added or renamed, like At a Glance.


<!--------------------------------------------------------------------------------- Introduction --->
<br>

## Introduction

Everything a reader needs in order to understand the Component, before any rule is stated. It carries four parts, each under its own third-level heading.

### Overview

The Component introduces itself: what it is, the responsibility it holds, what it contributes to the project, and what it is independent of. It takes as many paragraphs as that needs.

It is written about the Component, never about the document: it begins by defining the Component, not by describing what the file contains. It states what the Component *is* and *does*. Relationships with other Components belong in Relationships; instructions about Skill roles, execution order, or when a Skill should read the Component do not belong in this file.

The Component's own boundary — what it does not own — is stated explicitly, either as the closing sentences of Overview or as one dedicated Principle. It is never left implicit and never stated in both places.

### Purpose

The reason this Component is a Component at all: the problem it solves, what its separation makes possible, and what would go wrong if its work were spread across the others instead.

It is written about the design rather than about the document, and takes as many paragraphs as the reason needs. It answers the question a reader asks before any rule makes sense — *why is this a thing of its own?* — so that every Principle that follows reads as a consequence of that reason rather than as an arbitrary constraint.

It names the cost of the alternative concretely: not "for separation of concerns", but what actually happens when the same knowledge lives in three places, or when a consumer reaches past this Component to the one behind it. A reader who understands this part can judge a case the Principles do not cover.

Each Principle's own **Why** explains that one rule. This part explains the Component. Neither repeats the other.

### How It Works

How the Component does its work, told as a flow: what reaches it, what it does with it, what it hands on, and what comes back. It is the narrative a newcomer needs in order to picture the Component in motion before meeting its vocabulary and its rules.

It stays at the level of concepts the Component owns and names no tool, package, or file layout. It states no obligation: a rule that a reader would have to obey belongs in a Principle. Where a Component's flow is genuinely trivial, this part is a short paragraph or two rather than an invented elaboration.

### Understanding

How the Human explained this Component, in their own words, and what was decided along the way.

The Principles state what holds. This part preserves how the Human arrived there, so that a later session — human or Agent — does not have to rediscover the reasoning, and so that a question already settled is not reopened as if it were new. Each entry names its subject under a fourth-level heading, gives the Human's explanation close to the words they used, and lists the decisions it produced, including the proposals that were not accepted and why:

```markdown
### Understanding

#### <Subject>

**<The question the Human is answering>** <Their explanation, in their own words.>

**Decisions:**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why — so it is not proposed again>
```

It is written close to how the Human said it, not translated into the file's formal voice, because the wording is part of what is being preserved. A proposal that was not accepted is recorded with its reason; without that, the same suggestion returns in the next session.

It carries no dates, and it is written in the present tense. It states what holds now and what it replaces, and is rewritten when the Human's understanding changes — the file is the current picture, not a log of when each part of it arrived.

This part is a record, never an authority. It explains the Principles and never adds an obligation: an obligation that matters belongs in a Principle, where it is binding. Where the record and a Principle disagree, the Principle is correct and the record is out of date. It is optional: a Component whose Understanding has not been recorded omits it.


<!--------------------------------------------------------------------------------- Terms --->
<br>

## Terms

A short definition list of the terms the Principles owner owns — the capitalized concepts its Principles use and that a reader would otherwise have to infer from the prose.

```markdown
## Terms

- **<Term>** — <one sentence defining it within this Principles owner>
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

The tree names concepts the Component owns, not files, directories, classes, or packages: a repository layout belongs to the Component's Preferences, and the shape of a generated file belongs to its Schema. A part named here is governed by a Principle, and it is defined in Terms when this Component owns the term; a part whose term another Component owns — a Public Interface, for example — is used as that owner defines it and is not redefined in Terms. Architecture shows how the parts fit together and introduces no obligation of its own.

This part is optional. A Component formed from named parts — internal layers, services, foundations, a public boundary — carries it. A Component with no internal structure worth naming omits the section entirely rather than carrying an empty one.


<!--------------------------------------------------------------------------------- Relationships --->
<br>

## Relationships

A short list naming the Components or Modules this Principles owner consumes and the Components or Modules that consume it, each with the reason for the connection.

```markdown
## Relationships

- **Consumes <Component>** — <what it takes and why>
- **Consumed by <Component>** — <what it provides and why>
```

Relationships are stated between Components and Modules only. No Skill, operation, Mode, or Workflow step appears here. An owner that consumes nothing, or that nothing consumes, records that fact rather than inventing a connection.


<!--------------------------------------------------------------------------------- Boundaries --->
<br>

## Boundaries

The work that looks like this Component's but is not, each named with the Component that owns it and the reason the line falls there.

Relationships says what this Component consumes and provides. Boundaries says where a reader — human or Agent — is most likely to put something in the wrong place, and settles it in advance:

```markdown
## Boundaries

- **<the work that looks like this Component's>** — belongs to <Component>, because <what makes it theirs>.
```

Each entry is a case that has actually caused confusion or plausibly would: a rule that could be read as either Component's, a setting two Components could both claim, a concern whose name appears in both. An entry states the reason, not only the owner, so the same reasoning settles the next case that is not listed.

This part is optional, and it is not a restatement of the Component's boundary sentence in Introduction or of a Principle's own **Boundary**. A Component carries it when its edges are genuinely easy to cross and omits the section when they are not.


<!--------------------------------------------------------------------------------- Layering --->
<br>

## Layering

One or two paragraphs placing the Component's technical choices outside this file, and naming what holds them:

- an Implementation Component's technical choices and defaults belong to its Implementation Preferences, and an Agent Component's declarations and native mappings belong to its Agent Preferences;
- implementation applies those choices to the current project definition; and
- when the Component owns a generated file, the shape of that file belongs to its Schema.

A Component still states where its technical choices or declarations belong even when its Implementation Preferences or Agent Preferences contain no entries. Explicit absence is not a reason to omit the layering statement.


<!--------------------------------------------------------------------------------- Documentation --->
<br>

## Documentation

What this Component's own documentation must convey, beyond the shared documentation rules that Development states for every Component.

The section is short prose, and it says what a reader of that Component's documentation must come away with — never how the documentation file is laid out, which belongs to Development Preferences:

```markdown
## Documentation

<What a reader must understand from this Component's documentation, and what its
documentation must therefore cover that the shared rules do not already require.>
```

This part is optional, and it is not the place to restate the shared rules. A Component carries it when its documentation has a demand of its own — a surface that must be shown a particular way, a concept a reader cannot use the Component without — and omits the section entirely when the shared rules are enough.


<!--------------------------------------------------------------------------------- Authority --->
<br>

## Authority

One or two paragraphs, stating all three of:

- every Principle in the file is mandatory;
- an Implementation Preference or Agent Preferences can never override a Principle; and
- a project may only add stricter rules, never looser ones.

No Principles file omits or weakens any of the three.


<!--------------------------------------------------------------------------------- Principles --->
<br>

## Principles

The section that carries the file's mandatory rules. It opens with one or two short sentences stating that each rule below is mandatory, and then carries the Principles themselves.

Each Principle is a third-level heading under it, carrying its title, followed by three labelled subsections:

```markdown
## Principles

<One sentence: every Principle below is mandatory.>

### <Title>

**Rule:** <the mandatory statement>

**Why:** <the reason the rule exists>

**Boundary:** <the limit of the rule>
```

### Title

The title states the rule as a claim, not as a topic: `Data Access is the only Logic route to Database`, not `Data Access`. It is read alone in a list of Principles and still communicates the rule, and it is how the Principle is cited — a Principle carries no number, so its title is its identity and is written to stay accurate if the rule is reworded.

### Rule

The mandatory statement itself, written in the present tense as something that holds rather than something to do. It uses the binding words — *is*, *must*, *only*, *never* — and remains free of tools and versions.

The Rule may be one sentence or several, and may carry a list when the rule enumerates parts, such as the layers a Component is formed from or the values a field accepts. It states the rule completely; a reader who reads only the Rule subsections of a file has read every obligation the file imposes.

### Why

The reason the rule exists: what it protects, what it makes possible, or what breaks without it. It never introduces a new obligation. A statement that a reader would have to obey belongs in Rule.

### Boundary

The limit of the rule: what it does not authorize, the adjacent responsibility it must not absorb, the case it does not reach, or the decision it leaves to another authority.

Every Principle has one, because a rule with no stated limit is read as unlimited. When the limit is that no exception exists, Boundary says so.

### Order

Principles carry no number. A Principle is identified and cited by its title, so it can be reordered, reworded, or removed without breaking a citation anywhere else.

They are ordered so that the ones establishing the Component's own shape come before the ones governing its relationships with other Components, and within that so the order follows the reading path a newcomer needs rather than importance. A new Principle is placed where it reads best rather than appended, and Navigation and At a Glance are rewritten to match.



<!--------------------------------------------------------------------------------- At a Glance --->
<br>

## At a Glance

The closing section: every obligation in the file, one line each, in Principle order.

```markdown
## At a Glance

- **Must** — <the obligation in one line>
- **Never** — <the prohibition in one line>
- **Must** — <the obligation in one line>
```

Each line is labelled **Must** or **Never**. The lines follow the order of the Principles they come from, and a Principle's lines stay together, so a reader can trace a line back by position. A Principle contributes as many lines as it has distinct obligations, and every obligation in the file appears exactly once in this list.

This section is derived, never authoritative. It introduces no rule that its Principle does not already state, and it is rewritten whenever a Principle changes. When the list and a Principle disagree, the Principle is correct.


<!--------------------------------------------------------------------------------- Template --->
<br>

## Template

```markdown
# <Component> Principles

## Navigation

1. **[Introduction](#introduction)**
   - **[Overview](#overview)**
   - **[Purpose](#purpose)**
   - **[How It Works](#how-it-works)**
   - **[Understanding](#understanding)**
2. **[Terms](#terms)**
3. **[Principles](#principles)**
   - **[1. <Title>](#1-title)**
4. **[At a Glance](#at-a-glance)**

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

### Understanding

#### <Subject>

**<The question the Human is answering>** <Their explanation, in their own words.>

**Decisions:**

1. <what holds, and what it replaces>
2. <a proposal that was not accepted, and why>

<Omit Understanding when none has been recorded.>

## Terms

- **<Term>** — <definition within this Principles owner>

## Architecture

```text
<Component>
├── <Part>
└── <Part>
```

<A paragraph or two per part: what it owns and the limit that keeps it distinct. Omit this
whole section when the Component has no internal structure worth naming.>

## Relationships

- **Consumes <Component>** — <what it takes and why>
- **Consumed by <Component>** — <what it provides and why>

## Boundaries

- **<work that looks like this Component's>** — belongs to <Component>, because <the reason>.

<Omit this whole section when this Component's edges are not easy to cross.>

<Layering: Implementation technical choices and defaults belong to <Component> Preferences;
Agent declarations and mappings belong to <Component> Preferences; implementation realizes them.>

## Documentation

<What a reader must understand from this Component's documentation. Omit this whole section
when the shared documentation rules are enough.>

Every statement here is mandatory. An Implementation Preference or Agent Preferences can never override
a Principle, and a project may only add stricter rules, never looser ones.

<br>

## Principles

<Every Principle below is mandatory.>

### <Title stating the rule as a claim>

**Rule:** <the mandatory statement>

**Why:** <the reason it exists>

**Boundary:** <the limit of the rule>

<br>

### <Title>

**Rule:** ...

**Why:** ...

**Boundary:** ...

<br>

## At a Glance

- **Must** — <obligation>
- **Never** — <prohibition>
```
