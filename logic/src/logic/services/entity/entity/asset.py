"""Entity Child Service bound to Model's Asset Entity."""

from model.interface import Asset

from logic.services.entity.base_entity import BaseEntity


class AssetService(BaseEntity):
    """Selects Asset once and offers every shared Entity Action for it."""

    entity = Asset
