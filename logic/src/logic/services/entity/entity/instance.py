"""The Instance Service."""

from collections.abc import Mapping
from typing import ClassVar

from model.interface import Instance

from logic.core.credentials import Treatment
from logic.services.entity.base import EntityServiceBase


class InstanceService(EntityServiceBase[Instance]):
    """Entity-bound Actions for Instance records."""

    entity = Instance
    credentials: ClassVar[Mapping[str, Treatment]] = {
        "password": Treatment.ENCRYPTED,
        "api_key": Treatment.ENCRYPTED,
    }
