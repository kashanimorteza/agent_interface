"""The AccountGroup Service."""

from model.interface import AccountGroup

from logic.services.entity.base import EntityServiceBase


class AccountGroupService(EntityServiceBase[AccountGroup]):
    """Entity-bound Actions for AccountGroup records."""

    entity = AccountGroup
