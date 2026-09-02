# Trading Assistant

Defines what the project is and the main parts that make up the system.

**Name:** Trading Assistant  
**Description:**  A platform for defining and managing trading information, strategies, actions, and related data.  

<br><br>

## Structure

- **Database** — owns persistent storage, schema, and migrations.
- **Backend** — manages application behavior and publishes the HTTP API by consuming the Database contract.
- **Frontend** — provides the user interface by consuming the Backend API contract.

<br><br>

## Models

Defines the core entities of the project and the data fields that belong to each entity.

### Trading Platform

Purpose: Defines the trading integration used to execute trades. Initial platforms include Binance and MetaTrader 5, and additional platforms may be added later. Each platform can provide its own development interface for performing trading operations through its related library.

Fields: ID, Name, Status, Description

### Broker

Purpose: Defines a broker, its broker-specific parameters, and the trading platform it uses. A broker also acts as the parent under which its trading accounts are defined.

Fields: ID, Name, Trading Platform ID, Status, Description

### Account

Purpose: Defines a trading account that belongs to a specific broker and is used to perform trading operations.

Fields: ID, Name, Username, Password, Broker ID, Status, Description

### Asset

Purpose: Defines a tradable asset and its related parameters, such as EURUSD or XAUUSD.

Fields: ID, Name, Status, Description

### Strategy

Purpose: Defines the trading settings used by an action, including values such as stop loss and take profit.

Fields: ID, Name, Risk Parameter, Status, Description

### Trailing Group

Purpose: Defines a group for managing the rules that determine when and how stop loss and take profit values should change during a trade.

Fields: ID, Name, Status, Description

### Trailing Rule

Purpose: Defines an individual rule within a trailing group. For example, when profit reaches a specified percentage of the take-profit target, the rule can adjust the take profit and stop loss.

Fields: ID, Name, Trailing Group ID, Status, Description

### Partial Group

Purpose: Defines a group of rules for closing all or part of a position at specified profit levels, such as closing 10%, 30%, or the entire position.

Fields: ID, Name, Status, Description

### Partial Rule

Purpose: Defines an individual rule within a partial group, including the profit threshold and the portion of the position to close when that threshold is reached.

Fields: ID, Name, Partial Group ID, Profit Threshold, Close Portion, Status, Description

### Action Group

Purpose: Groups trading actions by an operating or risk profile, such as Standard or High Risk.

Fields: ID, Name, Status, Description

### Action

Purpose: Defines a trading action within an action group by combining an asset, an account, and a strategy. For example, a High Risk action can trade EURUSD through Account A using Strategy B.

Fields: ID, Name, Asset ID, Account ID, Strategy ID, Group ID, Status, Description

### Execute

Purpose: Tracks actions that have been activated and executed, including the current stage and state of each execution.

Fields: ID, Name, Action ID, Profit, State, Status, Description

### Position

Purpose: Stores the complete information for a position created from an executed order, including its entry price, take profit, stop loss, and the settings applied through its related groups.

Fields: ID, Name, Entry Price, Take Profit, Stop Loss, Status, Description

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
