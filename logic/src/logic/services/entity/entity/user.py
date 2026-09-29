"""The User Service."""

from collections.abc import Mapping
from typing import ClassVar

from model.interface import User

from logic.core.credentials import Treatment
from logic.services.entity.base import EntityServiceBase


class UserService(EntityServiceBase[User]):
    """Entity-bound Actions for User records."""

    entity = User
    credentials: ClassVar[Mapping[str, Treatment]] = {
        "password": Treatment.HASH,
        "api_key": Treatment.HASH,
    }
