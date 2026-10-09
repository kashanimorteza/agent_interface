"""The Entity Group: Entity Service as HTTP."""

from importlib import import_module

from logic.interface import Entity

from api.endpoints import Adapter, segment

ROLE = "entity"
NAME = "Entity"
SOURCE = Entity

ADAPTERS: dict[str, Adapter] = {
    segment(child): import_module(f"api.groups.entity.{segment(child)}").router
    for child, kind in vars(SOURCE.Service).items()
    if isinstance(kind, type) and not child.startswith("_")
}
