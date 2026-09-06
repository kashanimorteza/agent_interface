"""Shared Model specifications — a static transcription of .interface/config/model.yaml.

Logic derives its units and API derives its schemas from this module. It preserves Model identity,
fields, types, defaults, credential markers, and relationships exactly; nothing is redefined here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from trading_backend.errors import UnknownModelError


@dataclass(frozen=True)
class FieldSpec:
    name: str
    type: str
    nullable: bool
    primary_key: bool = False
    default: Any | None = None
    has_default: bool = False
    size: int | None = None
    credential: bool = False
    purpose: str | None = None


@dataclass(frozen=True)
class ModelSpec:
    key: str
    name: str
    purpose: str
    fields: tuple[FieldSpec, ...]
    relationships: tuple[tuple[str, str, str], ...] = ()  # (field, target Model key, relationship type)

    @property
    def primary_key(self) -> str:
        return next(f.name for f in self.fields if f.primary_key)

    def field(self, name: str) -> FieldSpec | None:
        return next((f for f in self.fields if f.name == name), None)


MODEL_SPECS: dict[str, ModelSpec] = {
    'user': ModelSpec(
        key='user',
        name='User',
        purpose='Defines an independent user of the system and enables multi-user operation. Each user can have a separate set of settings, allowing new users to be added with configurations that remain distinct from those of existing users.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The user's display name."),
            FieldSpec('username', 'string', nullable=False, purpose='The username used to identify the user.'),
            FieldSpec('password', 'string', nullable=False, credential=True, purpose='The password credential used by the user.'),
            FieldSpec('api_key', 'string', nullable=False, credential=True, purpose='The API key assigned to the user.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the user is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the user.'),
        ),
    ),
    'currency': ModelSpec(
        key='currency',
        name='Currency',
        purpose='Defines a currency that can be used by the trading system and identifies its standard code, display symbol, associated country or region, and monetary decimal precision.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The currency's full name."),
            FieldSpec('code', 'string', nullable=False, size=3, purpose="The currency's standard three-letter code, such as USD or EUR."),
            FieldSpec('symbol', 'string', nullable=True, purpose="The currency's display symbol, such as $, €, or £."),
            FieldSpec('country', 'string', nullable=True, purpose='Identifies the country or region associated with the currency.'),
            FieldSpec('decimal_digits', 'integer', nullable=False, default=2, has_default=True, purpose='Defines the number of decimal digits normally used for monetary values in the currency.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the currency is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the currency.'),
        ),
    ),
    'trading_platform': ModelSpec(
        key='trading_platform',
        name='Trading Platform',
        purpose="Defines a supported trading API standard, such as MetaTrader 5 or Binance, while keeping the system independent of any specific exchange or broker. Every trading platform implementation exposes the same application-facing trading functions through a dedicated class, while handling communication with its destination API according to that platform's own mechanism. Additional platform implementations can be added without changing the system's common trading interface.",
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The platform's display name."),
            FieldSpec('code', 'string', nullable=False, purpose='Identifies the implementation class the application must use for this trading platform, such as binance or metatrader_5.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the platform is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the platform.'),
        ),
    ),
    'broker': ModelSpec(
        key='broker',
        name='Broker',
        purpose='Defines a broker that the system can work with through its selected trading platform. Multiple brokers can be added so the system is not limited to a specific broker and can operate with any configured broker.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The broker's display name."),
            FieldSpec('user_id', 'integer', nullable=False, purpose='Identifies the user who owns the broker configuration.'),
            FieldSpec('trading_platform_id', 'integer', nullable=False, purpose='Identifies the trading platform used by the broker.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the broker is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the broker.'),
        ),
        relationships=(
            ('user_id', 'user', 'belongs_to'),
            ('trading_platform_id', 'trading_platform', 'belongs_to'),
        ),
    ),
    'account': ModelSpec(
        key='account',
        name='Account',
        purpose='Defines a funded trading account through which the system executes trades and launches positions. Each account identifies its broker, account model, and login credentials so the system knows where the trade must be sent, how it must connect, and which account must be used for the operation.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The account's display name."),
            FieldSpec('broker_id', 'integer', nullable=False, purpose='Identifies the broker that owns the account.'),
            FieldSpec('base_currency_id', 'integer', nullable=False, purpose='Identifies the base currency used by the account.'),
            FieldSpec('username', 'string', nullable=False, purpose='The username identifier used to access the trading account.'),
            FieldSpec('password', 'string', nullable=False, credential=True, purpose='The credential used to access the trading account.'),
            FieldSpec('leverage', 'integer', nullable=False, purpose="Defines the account's leverage multiplier."),
            FieldSpec('balance', 'decimal', nullable=False, default=0, has_default=True, purpose="Stores the account's current balance."),
            FieldSpec('account_type', 'string', nullable=False, purpose='Identifies the account model, such as cfd or spread_betting.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the account is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the account.'),
        ),
        relationships=(
            ('broker_id', 'broker', 'belongs_to'),
            ('base_currency_id', 'currency', 'uses'),
        ),
    ),
    'asset': ModelSpec(
        key='asset',
        name='Asset',
        purpose='Defines an asset that can be selected for trading. It provides the system with the complete set of available tradable assets and identifies the category of each asset so the system knows exactly what is being traded.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The asset's display name."),
            FieldSpec('symbol', 'string', nullable=False, purpose='Identifies the tradable asset, such as EUR/USD, XAU/USD, or USOil.'),
            FieldSpec('category', 'string', nullable=False, purpose='Identifies the asset category, such as Currency, Commodity, or Cryptocurrency.'),
            FieldSpec('point_size', 'float', nullable=False, default=0.0, has_default=True, purpose='Stores the size of one point for the asset.'),
            FieldSpec('digits', 'integer', nullable=False, default=0, has_default=True, purpose="Stores the number of decimal digits used for the asset's price."),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the asset is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the asset.'),
        ),
    ),
    'trailing_group': ModelSpec(
        key='trailing_group',
        name='Trailing Group',
        purpose='Defines an independent group for organizing the rules that manage Stop Loss and Take Profit during a trade. The group identifies the rule set, while each rule separately defines its activation condition and the changes to apply.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The trailing group's display name."),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the trailing group is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the trailing group.'),
        ),
    ),
    'trailing_rule': ModelSpec(
        key='trailing_rule',
        name='Trailing Rule',
        purpose='Defines an individual rule within a Trailing Group that tells the system when and how to manage Take Profit and Stop Loss. Each rule provides the activation condition and the parameters used to apply the required adjustments.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The trailing rule's display name."),
            FieldSpec('trailing_group_id', 'integer', nullable=False, purpose='Identifies the trailing group that contains the rule.'),
            FieldSpec('trigger_percentage', 'decimal', nullable=False, purpose='Defines the profit percentage of the take-profit target that activates the rule.'),
            FieldSpec('take_profit_adjustment', 'decimal', nullable=True, purpose='Defines the take-profit adjustment applied when the rule is activated.'),
            FieldSpec('stop_loss_adjustment', 'decimal', nullable=True, purpose='Defines the stop-loss adjustment applied when the rule is activated.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the trailing rule is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the trailing rule.'),
        ),
        relationships=(
            ('trailing_group_id', 'trailing_group', 'belongs_to'),
        ),
    ),
    'partial_group': ModelSpec(
        key='partial_group',
        name='Partial Group',
        purpose='Defines an independent group of rules for managing portions of an open trade. Its rules determine how much of the trade volume must be closed when profit or loss reaches specified thresholds.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The partial group's display name."),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the partial group is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the partial group.'),
        ),
    ),
    'partial_rule': ModelSpec(
        key='partial_rule',
        name='Partial Rule',
        purpose='Defines an individual Partial Close rule that tells the system under which condition part of an open position must be closed and how much of its volume must be closed.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The partial rule's display name."),
            FieldSpec('partial_group_id', 'integer', nullable=False, purpose='Identifies the partial group that contains the rule.'),
            FieldSpec('profit_percentage', 'decimal', nullable=False, purpose='Defines the profit percentage that activates the rule.'),
            FieldSpec('close_percentage', 'decimal', nullable=False, purpose='Defines the percentage of the position closed when the rule is activated.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the partial rule is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the partial rule.'),
        ),
        relationships=(
            ('partial_group_id', 'partial_group', 'belongs_to'),
        ),
    ),
    'action_group': ModelSpec(
        key='action_group',
        name='Action Group',
        purpose='Defines an independent grouping for trading actions based on their risk profile, such as high risk, normal risk, or low risk. Actions are assigned to these groups so trades can be organized and selected by their intended risk level.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The action group's display name."),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the action group is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the action group.'),
        ),
    ),
    'action': ModelSpec(
        key='action',
        name='Action',
        purpose="Defines how a position must be opened. An action selects the asset and account and provides the risk, Take Profit, Stop Loss, Partial Group, and Trailing Group settings that determine the position's parameters and execution behavior.",
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The action's display name."),
            FieldSpec('action_group_id', 'integer', nullable=False, purpose='Identifies the action group that contains the action.'),
            FieldSpec('asset_id', 'integer', nullable=False, purpose='Identifies the asset traded by the action.'),
            FieldSpec('account_id', 'integer', nullable=False, purpose='Identifies the account used to execute the action.'),
            FieldSpec('partial_group_id', 'integer', nullable=False, purpose='Identifies the Partial Group used by the action.'),
            FieldSpec('trailing_group_id', 'integer', nullable=False, purpose='Identifies the Trailing Group used by the action.'),
            FieldSpec('risk_by_reward', 'decimal', nullable=False, purpose='Defines the numeric risk-to-reward value used by the action.'),
            FieldSpec('take_profit', 'decimal', nullable=False, purpose='Defines the Take Profit value used by the action.'),
            FieldSpec('stop_loss', 'decimal', nullable=False, purpose='Defines the Stop Loss value used by the action.'),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the action is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the action.'),
        ),
        relationships=(
            ('action_group_id', 'action_group', 'belongs_to'),
            ('asset_id', 'asset', 'uses'),
            ('account_id', 'account', 'uses'),
            ('partial_group_id', 'partial_group', 'uses'),
            ('trailing_group_id', 'trailing_group', 'uses'),
        ),
    ),
    'position': ModelSpec(
        key='position',
        name='Position',
        purpose='Stores the complete information for every position created by the system. It allows the system to identify and track positions that have been opened as well as positions that are still pending execution.',
        fields=(
            FieldSpec('id', 'integer', nullable=False, primary_key=True),
            FieldSpec('name', 'string', nullable=False, purpose="The position's display name."),
            FieldSpec('trading_platform_id', 'integer', nullable=False, purpose='Identifies the trading platform used to execute the position.'),
            FieldSpec('broker_id', 'integer', nullable=False, purpose='Identifies the broker through which the position is executed.'),
            FieldSpec('account_id', 'integer', nullable=False, purpose='Identifies the trading account used for the position.'),
            FieldSpec('trailing_group_id', 'integer', nullable=False, purpose='Identifies the Trailing Group applied to the position.'),
            FieldSpec('partial_group_id', 'integer', nullable=False, purpose='Identifies the Partial Group applied to the position.'),
            FieldSpec('action_group_id', 'integer', nullable=False, purpose='Identifies the Action Group associated with the position.'),
            FieldSpec('action_id', 'integer', nullable=False, purpose='Identifies the action from which the position is created.'),
            FieldSpec('date', 'datetime', nullable=False, purpose="Stores the position's date and time."),
            FieldSpec('volume', 'decimal', nullable=False, purpose="Stores the position's trading volume."),
            FieldSpec('profit', 'decimal', nullable=False, default=0, has_default=True, purpose="Stores the position's current profit or loss."),
            FieldSpec('is_executed', 'boolean', nullable=False, default=False, has_default=True, purpose='Indicates whether the position has been executed.'),
            FieldSpec('order_type', 'string', nullable=False, purpose="Stores the position's order type."),
            FieldSpec('base_tp', 'decimal', nullable=False, purpose="Stores the position's initial Take Profit value."),
            FieldSpec('base_sl', 'decimal', nullable=False, purpose="Stores the position's initial Stop Loss value."),
            FieldSpec('real_tp', 'decimal', nullable=False, purpose="Stores the position's current Take Profit value."),
            FieldSpec('real_sl', 'decimal', nullable=False, purpose="Stores the position's current Stop Loss value."),
            FieldSpec('status', 'boolean', nullable=False, default=True, has_default=True, purpose='Indicates whether the position is active.'),
            FieldSpec('description', 'string', nullable=True, purpose='Describes the position.'),
        ),
        relationships=(
            ('trading_platform_id', 'trading_platform', 'uses'),
            ('broker_id', 'broker', 'uses'),
            ('account_id', 'account', 'uses'),
            ('trailing_group_id', 'trailing_group', 'uses'),
            ('partial_group_id', 'partial_group', 'uses'),
            ('action_group_id', 'action_group', 'uses'),
            ('action_id', 'action', 'belongs_to'),
        ),
    ),
}

# API resource name of each Model: the Database table name with hyphens (a Planning decision recorded in the P2 Plan).
RESOURCE_NAMES: dict[str, str] = {
    'user': 'users',
    'currency': 'currencies',
    'trading_platform': 'trading-platforms',
    'broker': 'brokers',
    'account': 'accounts',
    'asset': 'assets',
    'trailing_group': 'trailing-groups',
    'trailing_rule': 'trailing-rules',
    'partial_group': 'partial-groups',
    'partial_rule': 'partial-rules',
    'action_group': 'action-groups',
    'action': 'actions',
    'position': 'positions',
}

MODEL_KEYS: tuple[str, ...] = tuple(MODEL_SPECS)


def get_spec(key: str) -> ModelSpec:
    """The specification of one shared Model, or UnknownModelError."""
    try:
        return MODEL_SPECS[key]
    except KeyError:
        raise UnknownModelError(f"unknown Model {key!r}; known Models: {', '.join(MODEL_KEYS)}") from None
