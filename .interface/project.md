# Trading Assistant

Defines what the project is and the main parts that make up the system.

**Name:** Trading Assistant  
**Description:**  A platform for defining and managing trading information, strategies, actions, and related data.  

<br><br>

## Goals

- Manage trading platforms, brokers, and trading accounts.
- Manage assets and broker-specific asset settings.
- Define trading strategies, action groups, and trading actions.
- Configure trailing and partial-close rule groups.
- Execute trading actions and track positions.

<br><br>

## Models

Defines the project's domain models, their purposes, fields, keys, uniqueness constraints, relationships, and rules.

`Fields` lists the model's complete set of non-relationship fields. Every field is declared explicitly with its type and whether it is required; size, precision, default, or generation behavior is stated when applicable. Physical foreign-key fields are derived separately from `Relationships`.

### Trading Platform

**Purpose:** Defines the trading integration used to execute trades. Initial platforms include Binance and MetaTrader 5, and additional platforms may be added later. Each platform can provide its own development interface for performing trading operations through its related library.

**Fields:**

- `id` — Type: `integer`; Required: `true`; Auto Increment: `true`.
- `name` — Type: `string`; Required: `true`; Purpose: The platform's display name.
- `description` — Type: `string`; Required: `false`; Purpose: Describes the platform.
- `status` — Type: `boolean`; Required: `true`; Default: `true`; Purpose: Indicates whether the platform is active.
- `code` — Type: `string`; Required: `true`; Purpose: Identifies the platform for integrations, such as `binance` or `metatrader_5`.

**Primary Key:** `id`

**Unique:** `name`

**Relationships:** None.

**Rules:** None.

### Broker

Purpose: Defines a broker, its broker-specific parameters, and the trading platform it uses. A broker also acts as the parent under which its trading accounts are defined.

Relationships: Belongs to one Trading Platform.

### Account

Purpose: Defines a trading account, including its username identifier and password credential used to perform trading operations.

Relationships: Belongs to one Broker.

### Asset

Purpose: Defines a tradable asset and its related parameters, such as EURUSD or XAUUSD.

### Asset Detail

Purpose: Defines the broker-specific settings for an asset, allowing the same asset to have different settings for different brokers.

Relationships: Belongs to one Broker and one Asset.

Rules: Only one Asset Detail may exist for each Broker and Asset pair.

### Strategy

Purpose: Defines the trading settings and risk parameters used by an action, including values such as stop loss and take profit.

### Trailing Group

Purpose: Defines a group for managing the rules that determine when and how stop loss and take profit values should change during a trade.

### Trailing Rule

Purpose: Defines an individual rule within a trailing group. For example, when profit reaches a specified percentage of the take-profit target, the rule can adjust the take profit and stop loss.

Relationships: Belongs to one Trailing Group.

### Partial Group

Purpose: Defines a group of rules for closing all or part of a position at specified profit levels, such as closing 10%, 30%, or the entire position.

### Partial Rule

Purpose: Defines an individual rule within a partial group, including the profit threshold and the portion of the position to close when that threshold is reached.

Relationships: Belongs to one Partial Group.

### Action Group

Purpose: Groups trading actions by an operating or risk profile, such as Standard or High Risk.

### Action

Purpose: Defines a trading action within an action group by combining an asset, an account, and a strategy. For example, a High Risk action can trade EURUSD through Account A using Strategy B.

Relationships: Belongs to one Action Group, one Asset, one Account, and one Strategy.

### Position

Purpose: Tracks a trading action after it has been activated and executed, storing complete position information including its profit, current stage and state, entry price, take profit, stop loss, and the settings applied through its related groups.

Relationships: Belongs to one Action.

<br><br>

## Phases

Defines the project's implementation phases. Phases are executed step by step in their defined order, with each phase representing the next intended stage of project development.

### Phase 1

**Title:** Database

**Target:** Database

**Goal:** Create the database schema and migrations for all defined project models.

### Phase 2

**Title:** Backend API  
**Target:** Backend

**Goal:** Create and run the API for all defined project models.
