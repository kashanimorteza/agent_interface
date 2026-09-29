"""Entity Child Service bound to Model's Account Group Entity."""

from model.interface import AccountGroup

from logic.services.entity.base_entity import BaseEntity


class AccountGroupService(BaseEntity):
    """Selects Account Group once and offers every shared Entity Action for it."""

    entity = AccountGroup
