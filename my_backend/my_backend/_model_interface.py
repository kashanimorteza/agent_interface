"""Model Interface: Backend's only route to shared Model meaning.

Logic obtains Model types, meaning, and Credential markers only through this
boundary. It never redefines or copies Model meaning; it exposes the same
public types the Model package itself publishes.
"""

from __future__ import annotations

import my_model

BaseModel = my_model.BaseModel
User = my_model.User
TradingPlatform = my_model.TradingPlatform
Instance = my_model.Instance
Currency = my_model.Currency
Broker = my_model.Broker
Asset = my_model.Asset
AccountGroup = my_model.AccountGroup
Account = my_model.Account
TrailingGroup = my_model.TrailingGroup
TrailingRule = my_model.TrailingRule
PartialGroup = my_model.PartialGroup
PartialRule = my_model.PartialRule
ActionGroup = my_model.ActionGroup
Action = my_model.Action
Position = my_model.Position


def credential_field_names(model_type: type[my_model.BaseModel]) -> frozenset[str]:
    """Every field name the Model itself declares as a credential."""

    return frozenset(
        name
        for name, field in model_type.model_fields.items()
        if isinstance(field.json_schema_extra, dict) and field.json_schema_extra.get("credential") is True
    )
