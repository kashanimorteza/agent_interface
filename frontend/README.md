# Trading Assistant — Frontend Component

The Frontend presents Trading Assistant to users and lets them enter and manage all defined project
data. It is a Next.js 16 (App Router) application in TypeScript with three layers:

- **Presentation** — `src/app/` (root layout, home page, and the `[model]` management route) and
  `src/components/` (AppShell, Navigation, Notification, DataTable, RecordForm, FormField,
  StatusToggle, ConfirmDialog, ManagementPage), themed by the token system in `src/app/globals.css`.
- **Interaction Logic** — `src/hooks/` (`use-notification.tsx` for operation outcomes,
  `use-model-records.ts` for the list / create / edit / delete / toggle flow of one Model).
- **API Access** — `src/lib/api/` (`client.ts` Fetch client, `models.ts` Model operations,
  `schema.d.ts` types generated from the Backend's OpenAPI description) and the shared Model
  specification in `src/lib/models/model-specs.ts`.

The Frontend reaches application data only through the Backend API. It never connects to the
Database and never imports Backend code.

## Toolchain

Node.js 24 LTS (see `.node-version`) and npm 12.0.2.

```bash
npm install
```

## Runtime configuration

| Variable | Default | Meaning |
| --- | --- | --- |
| `NEXT_PUBLIC_API_BASE_URL` | `http://127.0.0.1:8000` | Base URL of the Backend API. Inlined into the browser bundle at build time, so rebuild after changing it. |

Copy `.env.example` to `.env.local` (never committed) to set it.

## Commands

```bash
npm run dev            # development server with reload at http://127.0.0.1:3000
npm run build          # production build (type-checks the project)
npm run start          # serve the production build
npm run generate:api   # regenerate src/lib/api/schema.d.ts from the running Backend
npm run lint           # ESLint
```

`npm run generate:api` needs the Backend running (see `backend/README.md`); the generated file is
committed so builds work without a live server. Regenerate it whenever the Backend API changes.

## Routes

| Route | Title | Model |
| --- | --- | --- |
| `/` | Home | — |
| `/user` | Users | user |
| `/currency` | Currencies | currency |
| `/trading-platform` | Trading Platforms | trading_platform |
| `/broker` | Brokers | broker |
| `/account` | Accounts | account |
| `/asset` | Assets | asset |
| `/trailing-group` | Trailing Groups | trailing_group |
| `/trailing-rule` | Trailing Rules | trailing_rule |
| `/partial-group` | Partial Groups | partial_group |
| `/partial-rule` | Partial Rules | partial_rule |
| `/action-group` | Action Groups | action_group |
| `/action` | Actions | action |
| `/position` | Positions | position |

Every management page lists the Model's records, creates or edits a record through a generated form,
asks for confirmation before deleting, toggles the record's status, and shows the outcome of every
operation.

Credential fields — `user.password`, `user.api_key`, `account.password` — are **write-only**: they are
entered through password inputs, never displayed, and left blank on edit to keep the stored value.
