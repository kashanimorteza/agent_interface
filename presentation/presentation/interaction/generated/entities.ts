// Generated from Model's Interface. Regenerate; do not edit.

export const entities = [
  {
    adapter: 'user',
    name: 'User',
    description:
      'Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.',
  },
  {
    adapter: 'trading_platform',
    name: 'Trading Platform',
    description:
      "Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
  },
  {
    adapter: 'instance',
    name: 'Instance',
    description:
      'Defines a user-owned connection instance through which the system accesses a supported Trading Platform.',
  },
  {
    adapter: 'currency',
    name: 'Currency',
    description:
      'Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.',
  },
  {
    adapter: 'broker',
    name: 'Broker',
    description:
      'Defines a broker supported by the system and identifies the user who owns its configuration without coupling the Broker definition to one Trading Platform.',
  },
  {
    adapter: 'asset',
    name: 'Asset',
    description:
      'Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.',
  },
  {
    adapter: 'account_group',
    name: 'Account Group',
    description:
      'Defines an independent group for organizing trading accounts owned by one user.',
  },
  {
    adapter: 'account',
    name: 'Account',
    description:
      'Defines a funded trading account through which the system executes trades and launches positions. Each Account identifies the trading account and its account-level login credentials, while its selected Instance owns the separate technical connection to the Trading Platform.',
  },
  {
    adapter: 'trailing_group',
    name: 'Trailing Group',
    description:
      'Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.',
  },
  {
    adapter: 'trailing_rule',
    name: 'Trailing Rule',
    description:
      'Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.',
  },
  {
    adapter: 'partial_group',
    name: 'Partial Group',
    description:
      'Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.',
  },
  {
    adapter: 'partial_rule',
    name: 'Partial Rule',
    description:
      'Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.',
  },
  {
    adapter: 'action_group',
    name: 'Action Group',
    description:
      'Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.',
  },
  {
    adapter: 'action',
    name: 'Action',
    description:
      "Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
  },
  {
    adapter: 'position',
    name: 'Position',
    description:
      'Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.',
  },
] as const

export type EntityKey = (typeof entities)[number]['adapter']
