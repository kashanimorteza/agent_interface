# Trading Assistant

Defines what the project is and the main parts that make up the system.

**Name:** Trading Assistant  
**Description:**  A platform for defining and managing trading information, strategies, actions, and related data.  

<br><br>

## Models

Defines the core entities of the project, their purpose, and their relationships. Standard fields are resolved from the database preferences and are not repeated here. Model-specific data requirements belong in the Purpose, while cross-model references are declared explicitly as Relationships.

### Trading Platform

Purpose: Defines the trading integration used to execute trades. Initial platforms include Binance and MetaTrader 5, and additional platforms may be added later. Each platform can provide its own development interface for performing trading operations through its related library.

### Broker

Purpose: Defines a broker, its broker-specific parameters, and the trading platform it uses. A broker also acts as the parent under which its trading accounts are defined.

Relationships: Belongs to one Trading Platform.

### Account

Purpose: Defines a trading account, including the username and password credentials used to perform trading operations.

Relationships: Belongs to one Broker.

### Asset

Purpose: Defines a tradable asset and its related parameters, such as EURUSD or XAUUSD.

### Asset Detail

Purpose: Defines the broker-specific settings for an asset, allowing the same asset to have different settings for different brokers.

Relationships: Belongs to one Broker and one Asset.

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

### Execute

Purpose: Tracks actions that have been activated and executed, including the profit and current stage and state of each execution.

Relationships: Belongs to one Action.

### Position

Purpose: Stores the complete information for a position created from an executed order, including its entry price, take profit, stop loss, and the settings applied through its related groups.

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
