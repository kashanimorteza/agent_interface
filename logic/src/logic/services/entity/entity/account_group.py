"""Child Service for the AccountGroup Entity."""

from model.interface import AccountGroup

from logic.services.entity.base_entity import BaseEntity


class AccountGroupService(BaseEntity):
    """Entity-bound Actions for AccountGroup records."""

    entity = AccountGroup
