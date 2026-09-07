"""Storage schema of the fourteen shared Models.

Revision ID: 0001_schema
Revises:
Create Date: 2026-09-07

One table per Model, derived from the Model definitions under the Database
Preferences: columns in field order with engine-independent generic types,
NOT NULL from nullability, the primary key on id, unique and composite-unique
constraints for the Model rules, and RESTRICT foreign keys with an index for
every relationship. Each table records the Model it implements in its comment.
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("api_key", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_users"),
        sa.UniqueConstraint('name', name="uq_users_name"),
        comment="Model: User",
    )
    op.create_table(
        "currencies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(3), nullable=False),
        sa.Column("symbol", sa.String(), nullable=True),
        sa.Column("country", sa.String(), nullable=True),
        sa.Column("decimal_digits", sa.Integer(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_currencies"),
        sa.UniqueConstraint('name', name="uq_currencies_name"),
        sa.UniqueConstraint('code', name="uq_currencies_code"),
        comment="Model: Currency",
    )
    op.create_table(
        "trading_platforms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_trading_platforms"),
        sa.UniqueConstraint('name', name="uq_trading_platforms_name"),
        comment="Model: TradingPlatform",
    )
    op.create_table(
        "brokers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("trading_platform_id", sa.Integer(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_brokers"),
        sa.UniqueConstraint('user_id', 'name', name="uq_brokers_user_id_name"),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name="fk_brokers_user_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['trading_platform_id'], ['trading_platforms.id'], name="fk_brokers_trading_platform_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: Broker",
    )
    op.create_index("ix_brokers_trading_platform_id", "brokers", ['trading_platform_id'])
    op.create_index("ix_brokers_user_id", "brokers", ['user_id'])
    op.create_table(
        "account_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_account_groups"),
        sa.UniqueConstraint('name', name="uq_account_groups_name"),
        comment="Model: AccountGroup",
    )
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("broker_id", sa.Integer(), nullable=False),
        sa.Column("base_currency_id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("leverage", sa.Integer(), nullable=False),
        sa.Column("balance", sa.Numeric(), nullable=False),
        sa.Column("account_type", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_accounts"),
        sa.UniqueConstraint('name', name="uq_accounts_name"),
        sa.ForeignKeyConstraint(['group_id'], ['account_groups.id'], name="fk_accounts_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['broker_id'], ['brokers.id'], name="fk_accounts_broker_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['base_currency_id'], ['currencies.id'], name="fk_accounts_base_currency_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: Account",
    )
    op.create_index("ix_accounts_base_currency_id", "accounts", ['base_currency_id'])
    op.create_index("ix_accounts_broker_id", "accounts", ['broker_id'])
    op.create_index("ix_accounts_group_id", "accounts", ['group_id'])
    op.create_table(
        "assets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("symbol", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("point_size", sa.Float(), nullable=False),
        sa.Column("digits", sa.Integer(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_assets"),
        sa.UniqueConstraint('name', name="uq_assets_name"),
        sa.UniqueConstraint('symbol', name="uq_assets_symbol"),
        comment="Model: Asset",
    )
    op.create_table(
        "trailing_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_trailing_groups"),
        sa.UniqueConstraint('name', name="uq_trailing_groups_name"),
        comment="Model: TrailingGroup",
    )
    op.create_table(
        "trailing_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("trailing_group_id", sa.Integer(), nullable=False),
        sa.Column("trigger_percentage", sa.Numeric(), nullable=False),
        sa.Column("take_profit_adjustment", sa.Numeric(), nullable=True),
        sa.Column("stop_loss_adjustment", sa.Numeric(), nullable=True),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_trailing_rules"),
        sa.UniqueConstraint('name', name="uq_trailing_rules_name"),
        sa.ForeignKeyConstraint(['trailing_group_id'], ['trailing_groups.id'], name="fk_trailing_rules_trailing_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: TrailingRule",
    )
    op.create_index("ix_trailing_rules_trailing_group_id", "trailing_rules", ['trailing_group_id'])
    op.create_table(
        "partial_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_partial_groups"),
        sa.UniqueConstraint('name', name="uq_partial_groups_name"),
        comment="Model: PartialGroup",
    )
    op.create_table(
        "partial_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("partial_group_id", sa.Integer(), nullable=False),
        sa.Column("profit_percentage", sa.Numeric(), nullable=False),
        sa.Column("close_percentage", sa.Numeric(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_partial_rules"),
        sa.UniqueConstraint('name', name="uq_partial_rules_name"),
        sa.ForeignKeyConstraint(['partial_group_id'], ['partial_groups.id'], name="fk_partial_rules_partial_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: PartialRule",
    )
    op.create_index("ix_partial_rules_partial_group_id", "partial_rules", ['partial_group_id'])
    op.create_table(
        "action_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_action_groups"),
        sa.UniqueConstraint('name', name="uq_action_groups_name"),
        comment="Model: ActionGroup",
    )
    op.create_table(
        "actions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("action_group_id", sa.Integer(), nullable=False),
        sa.Column("asset_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("partial_group_id", sa.Integer(), nullable=False),
        sa.Column("trailing_group_id", sa.Integer(), nullable=False),
        sa.Column("risk_by_reward", sa.Numeric(), nullable=False),
        sa.Column("take_profit", sa.Numeric(), nullable=False),
        sa.Column("stop_loss", sa.Numeric(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_actions"),
        sa.UniqueConstraint('name', name="uq_actions_name"),
        sa.ForeignKeyConstraint(['action_group_id'], ['action_groups.id'], name="fk_actions_action_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], name="fk_actions_asset_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name="fk_actions_account_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['partial_group_id'], ['partial_groups.id'], name="fk_actions_partial_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['trailing_group_id'], ['trailing_groups.id'], name="fk_actions_trailing_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: Action",
    )
    op.create_index("ix_actions_account_id", "actions", ['account_id'])
    op.create_index("ix_actions_action_group_id", "actions", ['action_group_id'])
    op.create_index("ix_actions_asset_id", "actions", ['asset_id'])
    op.create_index("ix_actions_partial_group_id", "actions", ['partial_group_id'])
    op.create_index("ix_actions_trailing_group_id", "actions", ['trailing_group_id'])
    op.create_table(
        "positions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("trading_platform_id", sa.Integer(), nullable=False),
        sa.Column("broker_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("trailing_group_id", sa.Integer(), nullable=False),
        sa.Column("partial_group_id", sa.Integer(), nullable=False),
        sa.Column("action_group_id", sa.Integer(), nullable=False),
        sa.Column("action_id", sa.Integer(), nullable=False),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("volume", sa.Numeric(), nullable=False),
        sa.Column("profit", sa.Numeric(), nullable=False),
        sa.Column("is_executed", sa.Boolean(), nullable=False),
        sa.Column("order_type", sa.String(), nullable=False),
        sa.Column("base_tp", sa.Numeric(), nullable=False),
        sa.Column("base_sl", sa.Numeric(), nullable=False),
        sa.Column("real_tp", sa.Numeric(), nullable=False),
        sa.Column("real_sl", sa.Numeric(), nullable=False),
        sa.Column("status", sa.Boolean(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id', name="pk_positions"),
        sa.UniqueConstraint('name', name="uq_positions_name"),
        sa.ForeignKeyConstraint(['trading_platform_id'], ['trading_platforms.id'], name="fk_positions_trading_platform_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['broker_id'], ['brokers.id'], name="fk_positions_broker_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], name="fk_positions_account_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['trailing_group_id'], ['trailing_groups.id'], name="fk_positions_trailing_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['partial_group_id'], ['partial_groups.id'], name="fk_positions_partial_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['action_group_id'], ['action_groups.id'], name="fk_positions_action_group_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        sa.ForeignKeyConstraint(['action_id'], ['actions.id'], name="fk_positions_action_id", ondelete="RESTRICT", onupdate="RESTRICT"),
        comment="Model: Position",
    )
    op.create_index("ix_positions_account_id", "positions", ['account_id'])
    op.create_index("ix_positions_action_group_id", "positions", ['action_group_id'])
    op.create_index("ix_positions_action_id", "positions", ['action_id'])
    op.create_index("ix_positions_broker_id", "positions", ['broker_id'])
    op.create_index("ix_positions_partial_group_id", "positions", ['partial_group_id'])
    op.create_index("ix_positions_trading_platform_id", "positions", ['trading_platform_id'])
    op.create_index("ix_positions_trailing_group_id", "positions", ['trailing_group_id'])


def downgrade() -> None:
    op.drop_index("ix_positions_account_id", table_name="positions")
    op.drop_index("ix_positions_action_group_id", table_name="positions")
    op.drop_index("ix_positions_action_id", table_name="positions")
    op.drop_index("ix_positions_broker_id", table_name="positions")
    op.drop_index("ix_positions_partial_group_id", table_name="positions")
    op.drop_index("ix_positions_trading_platform_id", table_name="positions")
    op.drop_index("ix_positions_trailing_group_id", table_name="positions")
    op.drop_table("positions")
    op.drop_index("ix_actions_account_id", table_name="actions")
    op.drop_index("ix_actions_action_group_id", table_name="actions")
    op.drop_index("ix_actions_asset_id", table_name="actions")
    op.drop_index("ix_actions_partial_group_id", table_name="actions")
    op.drop_index("ix_actions_trailing_group_id", table_name="actions")
    op.drop_table("actions")
    op.drop_table("action_groups")
    op.drop_index("ix_partial_rules_partial_group_id", table_name="partial_rules")
    op.drop_table("partial_rules")
    op.drop_table("partial_groups")
    op.drop_index("ix_trailing_rules_trailing_group_id", table_name="trailing_rules")
    op.drop_table("trailing_rules")
    op.drop_table("trailing_groups")
    op.drop_table("assets")
    op.drop_index("ix_accounts_base_currency_id", table_name="accounts")
    op.drop_index("ix_accounts_broker_id", table_name="accounts")
    op.drop_index("ix_accounts_group_id", table_name="accounts")
    op.drop_table("accounts")
    op.drop_table("account_groups")
    op.drop_index("ix_brokers_trading_platform_id", table_name="brokers")
    op.drop_index("ix_brokers_user_id", table_name="brokers")
    op.drop_table("brokers")
    op.drop_table("trading_platforms")
    op.drop_table("currencies")
    op.drop_table("users")
