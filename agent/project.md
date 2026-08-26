# Trading Assistant

A platform for defining trading requirements, strategies, risk parameters, and executing trades automatically through **MetaTrader 5**.

The user can add trading accounts and configure the required trading information, strategies, and risk parameters.

The platform automatically connects to MetaTrader 5 and executes orders based on the defined configuration and strategy.

The platform also provides trading information and reports, including:

- Open trades
- Closed trades
- Total number of trades
- Trading results based on the defined strategy and risk configuration

Delivered in three phases.





<br> <br>

## Phase 1 — Data entry

> Models, storage, and management APIs.

### Development

#### Backend

The backend must:

- Use Python as the programming language.
- Use the latest stable version of Python available when development starts.
- Use FastAPI for the API layer.
- Use SQLAlchemy as the ORM.
- Use SQLite as the database.
- Use a standard Python database migration framework.
- Provide APIs for managing all Phase 1 models.
- Support Add, Edit, Update, Delete, and Status operations for all models.
- Authentication is **not** required.
- Automated tests are **not** required.

#### Frontend

`To be defined`

### Models

#### 1 · Account

**Fields:** `ID`, `Name`, `Username`, `Password`, `Status`, `Description`

#### 2 · Asset

**Fields:** `ID`, `Name`, `Status`, `Description`

#### 3 · Strategy

**Fields:** `ID`, `Name`, `Risk Parameter`, `Status`, `Description`

#### 4 · Action Group

**Fields:** `ID`, `Name`, `Status`, `Description`

#### 5 · Action

**Fields:** `ID`, `Name`, `Asset ID`, `Strategy ID`, `Group ID`, `Status`, `Description`

#### 6 · Execute

**Fields:** `ID`, `Name`, `Action ID`, `Profit`, `State`, `Status`, `Description`







<br> <br>

## Phase 2 — MetaTrader 5 integration

> Connecting the platform to MT5 and executing defined tasks.

### Development

**Backend** — `To be defined`

**Frontend** — `To be defined`

### Models

`To be defined`





<br> <br>

## Phase 3 — Reporting

> Surfacing results, performance, and execution history.

### Development

**Backend** — `To be defined`

**Frontend** — `To be defined`

### Models

`To be defined`