# Presentation

## Overview

Presentation is the web dashboard of the Trading Assistant: it gives every Entity of Model (15 today) one page, reached from one menu, where a user can list, view, search, filter, order, add, edit, delete, enable and disable its records wherever API serves the operation. Every column, filter, order and form field comes from the Entity's Declaration in Model, read when Presentation is generated, and all data is reached through API Access, the only part of Presentation that communicates with API. The page of the Currency Entity, at the location `/currency`, shows its title, an Add button, the filter editor, the order control and a table with one column for each Field of the Declaration, in the Declaration's order, followed by the actions of each record:

| Column heading (the Field's description)                                                |
| --------------------------------------------------------------------------------------- |
| id                                                                                      |
| Identifies the user who owns this currency.                                             |
| The currency's standard three-letter code, such as `USD` or `EUR`.                      |
| The currency's display symbol, such as `$`, `€`, or `£`.                                |
| Identifies the country or region associated with the currency.                          |
| Defines the number of decimal digits normally used for monetary values in the currency. |
| Indicates whether the currency is active.                                               |
| Describes the currency.                                                                 |
| Actions (View, Edit, Delete, Disable or Enable)                                         |

## Setup

Presentation needs Node.js 22 LTS or newer and a running API (see the API directory's documentation). Run these commands from the Presentation directory, with the API directory beside it:

```bash
npm install
echo "VITE_API_URL=$(grep '^url:' ../api/config.yaml | cut -d' ' -f2)" > .env
npm run dev
```

`VITE_API_URL` is the one setting Presentation needs: the Base URL API states as `url` in its `config.yaml`, including the URL Key. It is read from `.env` and is written nowhere in source. Keep `.env` out of version control, because it holds the URL Key. `npm run dev` serves Presentation at `http://localhost:5173`, where the root location opens the first Entity page with the menu beside it. `npm run build` writes the production build to `dist/` and `npm run preview` serves it.

## Use

Presentation is built from separate parts that each keep their own directory under `src/`:

| Directory                   | Part                                                                                                                                                                                |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api/`                      | API Access: the address setting, the one transport, errors as API returns them, the translation of queries and values, the read, write and change operations, and the data provider |
| `metadata/`                 | the generated description of every Entity: its Fields, Relations and dependencies                                                                                                   |
| `components/`               | the shared Components every page is built from: table, filter editor, order control, form, details and record actions                                                               |
| `pages/`                    | one unit per Entity, written out explicitly                                                                                                                                         |
| `navigation/`               | the location of every page, the framework's resources and the menu                                                                                                                  |
| `shell/`, `i18n/`, `theme/` | the page frame, the language layer and the appearance                                                                                                                               |

A page asks the framework's hooks for records; the hooks call the data provider in `api/`; the data provider calls the operations in `api/`; and only the transport there sends a request to API. The menu is built from the metadata, so it holds one entry for every Entity, and each entry leads to the location of that Entity's page. A new page belongs in `pages/`, in its own unit named from its Entity, with its location in `navigation/routes.tsx`: it exists only for an Entity of Model, and Presentation is regenerated when Model gains one. A new call to API belongs in `api/`, built on `send` and `call`, so that nothing else sends a request:

```ts
import { listRecords } from './api/read';
import { currency } from './metadata/resources.config';

const page = await listRecords(currency, {
  window: { current: 1, size: 5 },
  sorters: [{ field: 'id', order: 'asc' }],
});
console.log(page.total, page.rows.length);
```

## Verify

Each of these commands is run from the Presentation directory. Every Entity has its page when the three counts equal the number of Entities:

```bash
grep -c "^export const .*: EntityMeta" src/metadata/resources.config.ts
ls src/pages | wc -l
grep -c "path: locationOf" src/navigation/routes.tsx
```

Each prints `15`. Start Presentation as described in Setup and count the menu entries: there is one for every Entity, and choosing one shows that Entity's page. Only API Access communicates with API when no file outside `src/api/` sends a request or reads the address setting:

```bash
grep -rln "fetch(" src
grep -rln "VITE_API_URL" src
grep -rl "transport" src | grep -v "^src/api/"
```

The first prints only `src/api/transport.ts`, the second prints `src/api/address.ts` and `src/vite-env.d.ts`, and the third prints nothing.

## Troubleshooting

**Presentation stops with "The API address setting VITE_API_URL is not set."** The environment file is missing or empty. Create it as in Setup and start Presentation again, because the setting is read when it starts.

**A page shows "API could not be reached."** Nothing answers at the address. Start API, check that `url` in API's `config.yaml` is the address in `.env`, and restart Presentation.

**A page shows an error titled "Error" with the detail "Not Found" and "Status 404".** The address in `.env` lacks the URL Key, or holds a wrong one, so every request falls outside the Base URL. Copy the whole `url` value of API's `config.yaml`, key included.

**Saving shows `ExecutionError` with "UNIQUE constraint failed" and "Status 500".** The record repeats a value that must be unique, such as the name of a Trading Platform. The form shows what API returned; enter a different value and save again.

**A location shows the menu and an empty content area.** The location belongs to no Entity page. Choose an entry of the menu: a page's location is its Entity's name in lower case with hyphens between the words, such as `/trading-platform`.
