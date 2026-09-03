# Trading Assistant

Defines what the project is and the main parts that make up the system.

**Name:** Trading Assistant  
**Description:**  A platform for defining and managing trading information, strategies, actions, and related data.  

<br><br>

## Models

Defines the project's models.

### User

**Purpose:** Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The user's display name.
- `username` — Type: `string`; Nullable: `false`; Purpose: The username used to identify the user.
- `password` — Type: `string`; Nullable: `false`; Purpose: The password credential used by the user.
- `api_key` — Type: `string`; Nullable: `false`; Purpose: The API key assigned to the user.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the user is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the user.

### Trading Platform

**Purpose:** Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Purpose: The platform's display name.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns the trading platform configuration.
- `code` — Type: `string`; Nullable: `false`; Purpose: Identifies the implementation class the application must use for this trading platform, such as `binance` or `metatrader_5`.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the platform is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the platform.

**Relationships:**

- Belongs to one User through `user_id`.

**Rules:**

- The combination of `user_id` and `name` must be unique.

### Broker

**Purpose:** Defines a broker that the system can work with through its selected trading platform. Multiple brokers can be added so the system is not limited to a specific broker and can operate with any configured broker.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Purpose: The broker's display name.
- `user_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the user who owns the broker configuration.
- `trading_platform_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the trading platform used by the broker.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the broker is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the broker.

**Relationships:**

- Belongs to one User through `user_id`.
- Belongs to one Trading Platform through `trading_platform_id`.

**Rules:**

- The combination of `user_id` and `name` must be unique.
- `user_id` must match the `user_id` of the Trading Platform referenced by `trading_platform_id`.

### Account

**Purpose:** Defines a funded trading account through which the system executes trades and launches positions. Each account identifies its broker, account model, and login credentials so the system knows where the trade must be sent, how it must connect, and which account must be used for the operation.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The account's display name.
- `broker_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the broker that owns the account.
- `base_asset_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the default base asset used by the account.
- `username` — Type: `string`; Nullable: `false`; Purpose: The username identifier used to access the trading account.
- `password` — Type: `string`; Nullable: `false`; Purpose: The credential used to access the trading account.
- `leverage` — Type: `integer`; Nullable: `false`; Purpose: Defines the account's leverage multiplier.
- `balance` — Type: `decimal`; Nullable: `false`; Default: `0`; Purpose: Stores the account's current balance.
- `account_type` — Type: `string`; Nullable: `false`; Purpose: Identifies the account model, such as `cfd` or `spread_betting`.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the account is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the account.

**Relationships:**

- Belongs to one Broker through `broker_id`.
- Uses one Asset as its default base asset through `base_asset_id`.

### Asset

**Purpose:** Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The asset's display name.
- `symbol` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: Identifies the tradable asset, such as `EURUSD` or `XAUUSD`.
- `asset_type` — Type: `string`; Nullable: `false`; Purpose: Identifies the asset category, such as `commodity` or `currency`.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the asset is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the asset.

### Asset Detail

**Purpose:** Stores the parameters required to trade a specific asset through a specific broker. The same asset can have different parameter values for different brokers, and the system uses the matching Asset Detail when calculating and executing a trade for the selected Broker and Asset pair.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `broker_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the broker for which the asset parameters are defined.
- `asset_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the asset whose broker-specific parameters are defined.
- `parameter_1` — Type: `string`; Nullable: `true`.
- `parameter_2` — Type: `string`; Nullable: `true`.
- `parameter_3` — Type: `string`; Nullable: `true`.

**Relationships:**

- Belongs to one Broker through `broker_id`.
- Belongs to one Asset through `asset_id`.

**Rules:**

- Only one Asset Detail may exist for each Broker and Asset pair.

### Trailing Group

**Purpose:** Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The trailing group's display name.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the trailing group is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the trailing group.

### Trailing Rule

**Purpose:** Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The trailing rule's display name.
- `trailing_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the trailing group that contains the rule.
- `trigger_percentage` — Type: `decimal`; Nullable: `false`; Purpose: Defines the profit percentage of the take-profit target that activates the rule.
- `take_profit_adjustment` — Type: `decimal`; Nullable: `true`; Purpose: Defines the take-profit adjustment applied when the rule is activated.
- `stop_loss_adjustment` — Type: `decimal`; Nullable: `true`; Purpose: Defines the stop-loss adjustment applied when the rule is activated.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the trailing rule is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the trailing rule.

**Relationships:**

- Belongs to one Trailing Group through `trailing_group_id`.

### Partial Group

**Purpose:** Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The partial group's display name.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the partial group is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the partial group.

### Partial Rule

**Purpose:** Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The partial rule's display name.
- `partial_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the partial group that contains the rule.
- `profit_percentage` — Type: `decimal`; Nullable: `false`; Purpose: Defines the profit percentage that activates the rule.
- `close_percentage` — Type: `decimal`; Nullable: `false`; Purpose: Defines the percentage of the position closed when the rule is activated.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the partial rule is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the partial rule.

**Relationships:**

- Belongs to one Partial Group through `partial_group_id`.

### Action Group

**Purpose:** Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The action group's display name.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the action group is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the action group.

### Action

**Purpose:** Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The action's display name.
- `action_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the action group that contains the action.
- `asset_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the asset traded by the action.
- `account_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the account used to execute the action.
- `partial_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the Partial Group used by the action.
- `trailing_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the Trailing Group used by the action.
- `risk_by_reward` — Type: `decimal`; Nullable: `false`; Purpose: Defines the numeric risk-to-reward value used by the action.
- `take_profit` — Type: `decimal`; Nullable: `false`; Purpose: Defines the Take Profit value used by the action.
- `stop_loss` — Type: `decimal`; Nullable: `false`; Purpose: Defines the Stop Loss value used by the action.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the action is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the action.

**Relationships:**

- Belongs to one Action Group through `action_group_id`.
- Uses one Asset through `asset_id`.
- Uses one Account through `account_id`.
- Uses one Partial Group through `partial_group_id`.
- Uses one Trailing Group through `trailing_group_id`.

### Position

**Purpose:** Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.

**Fields:**

- `id` — Type: `integer`; Nullable: `false`; Auto Increment: `true`; Primary Key: `true`.
- `name` — Type: `string`; Nullable: `false`; Unique: `true`; Purpose: The position's display name.
- `trading_platform_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the trading platform used to execute the position.
- `broker_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the broker through which the position is executed.
- `account_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the trading account used for the position.
- `trailing_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the Trailing Group applied to the position.
- `partial_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the Partial Group applied to the position.
- `action_group_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the Action Group associated with the position.
- `action_id` — Type: `integer`; Nullable: `false`; Purpose: Identifies the action from which the position is created.
- `date` — Type: `datetime`; Nullable: `false`; Purpose: Stores the position's date and time.
- `volume` — Type: `decimal`; Nullable: `false`; Purpose: Stores the position's trading volume.
- `profit` — Type: `decimal`; Nullable: `false`; Default: `0`; Purpose: Stores the position's current profit or loss.
- `is_executed` — Type: `boolean`; Nullable: `false`; Default: `false`; Purpose: Indicates whether the position has been executed.
- `order_type` — Type: `string`; Nullable: `false`; Purpose: Stores the position's order type.
- `base_tp` — Type: `decimal`; Nullable: `false`; Purpose: Stores the position's initial Take Profit value.
- `base_sl` — Type: `decimal`; Nullable: `false`; Purpose: Stores the position's initial Stop Loss value.
- `real_tp` — Type: `decimal`; Nullable: `false`; Purpose: Stores the position's current Take Profit value.
- `real_sl` — Type: `decimal`; Nullable: `false`; Purpose: Stores the position's current Stop Loss value.
- `status` — Type: `boolean`; Nullable: `false`; Default: `true`; Purpose: Indicates whether the position is active.
- `description` — Type: `string`; Nullable: `true`; Purpose: Describes the position.

**Relationships:**

- Uses one Trading Platform through `trading_platform_id`.
- Uses one Broker through `broker_id`.
- Uses one Account through `account_id`.
- Uses one Trailing Group through `trailing_group_id`.
- Uses one Partial Group through `partial_group_id`.
- Uses one Action Group through `action_group_id`.
- Belongs to one Action through `action_id`.

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
