# Frontend — what a person sees

`my-frontend` is the interface to Trading Assistant. It is where the platform
becomes something you can look at and work with: every kind of data the project
defines can be found, read, added to, changed and removed from here.

It reaches the application only through the contract the Backend layer
publishes. It holds no rules of its own about what the data means — when an
outcome depends on an application rule, it asks and shows what came back.

## Purpose and boundaries

**This layer does:** present the data; hold what a person is doing — what they
are looking at, what they have typed, what they have changed; check what can be
checked before sending; send a change that says exactly what changed; and tell
the person what is happening, including exactly why something was refused.

**This layer does not:** decide what the data means, whether a value is
acceptable, or how anything is stored. It never reaches the database, never
imports another layer's implementation, and never invents an operation the
contract does not offer.

## Public interface

This layer is the outermost one — nothing in the system depends on it. What it
offers is the interface itself, served over HTTP:

| Where | What |
|---|---|
| `/` | Every kind of data the project defines |
| `/data/{kind}` | What is there, and adding to it |
| `/data/{kind}/{identifier}` | One record: read it, change it, enable or disable it, remove it |

The kinds are named for the data — `/data/currencies`, `/data/accounts`,
`/data/trading-platforms`, and so on. They are not written down anywhere in the
source: they come from the contract's own description.

### How the shapes get here

Nothing about the application's data is written out by hand in this layer. The
contract describes itself, and that description is the source:

```bash
npm run contract:pull    # take the description, generate the types and the catalogue
npm run contract:check   # say whether the contract has moved on since
```

`contract:pull` writes three things under `src/api-access/contract/`: a snapshot
of the description, the generated types, and a catalogue of what can be worked
with and which fields each kind of data carries. **A field the contract accepts
but never returns is treated as write-only** — that is how a credential is
recognised here, from the contract rather than from its name. Write-only fields
can be set in a form and are never displayed.

`contract:check` fails when the live contract no longer matches the snapshot,
so a change on the other side is reported rather than discovered by a user.

### What a change sends

A change carries only the fields you altered. A field you left alone is not
sent, so it keeps its value; a field you deliberately cleared *is* sent, as
cleared. Nothing is invented to fill a gap the application would fill itself.

## Internal, and not yours to depend on

`api-access` (the only door to the application), `interaction` (what the
interface is doing) and `presentation` (the visual system, the pieces, the
views) are internal. The interface is the thing to use.

## Dependencies

Node 24, Next.js 16.3.4, React 19.2.8, TypeScript 5.9.3 and `yaml` 2.9.0, with
`openapi-typescript` 7.13.0 used only to generate the types.

TypeScript is held at 5.9.3 rather than the newest release, which the rest of
this stack does not yet support.

**It needs the Backend layer running.** That layer needs the Database layer's
structure applied and its records seeded. See each of their descriptions.

## Configuration

`frontend.yaml`, beside this file, holds the settings this layer owns: where the
interface is served, how much of a list is shown at once, and the appearance
decided once for the whole interface — whether it follows the reader's light or
dark preference, and which way it reads.

Where the application is reached is a **binding**, in `application.yaml` at the
project root, under `frontend`. Point it somewhere else and restart; nothing in
this layer is edited.

This layer requires no secret. Anything it were given would have to stay in the
server process and never reach a browser.

## Installation and startup

With the Backend layer already running:

```bash
cd frontend
npm install
npm run contract:pull
npm run build
npm start
```

For development, with reload:

```bash
npm run dev
```

Then open the address `frontend.yaml` names — by default
`http://127.0.0.1:3000`.

## Usage

Start at `/`, which lists every kind of data. Pick one to see what is there.
From a listing you can add a record; from a record you can change it, turn it on
or off where that kind of data allows it, and remove it.

When something is refused, the interface shows what the application called it
and the reason it gave, unchanged.
