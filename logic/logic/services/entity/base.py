"""The Base of the Entity Service: one Action for every Entity Operation of Database, bound to one Entity per Child Service."""

import inspect
import re
from collections.abc import Callable
from typing import Any, ClassVar, get_origin

from database.interface import database_error, database_interface

_INSTANCE = re.compile(r"\b(?:one new|an) Entity instance\b")


def _takes_instance(method: Callable[..., Any]) -> bool:
    """Whether the Operation's entity parameter takes an Entity instance rather than the Entity class."""
    annotation = inspect.signature(method).parameters["entity"].annotation
    if annotation in (Any, inspect.Parameter.empty):
        return bool(_INSTANCE.search(method.__doc__ or ""))
    return annotation is not type and get_origin(annotation) is not type


def _action(name: str, method: Callable[..., Any]) -> Callable[..., Any]:
    """Build the Action that mirrors one Entity Operation, without the Entity class parameter."""
    parameters = list(inspect.signature(method).parameters.values())
    keeps_entity = _takes_instance(method)
    visible = parameters if keeps_entity else [parameters[0], *parameters[2:]]
    signature = inspect.Signature(visible)
    receiver = visible[0].name

    def action(self: BaseEntity, *args: Any, **kwargs: Any) -> Any:
        given = dict(signature.bind(self, *args, **kwargs).arguments)
        given.pop(receiver)
        call = getattr(self._database, name)
        if not keeps_entity:
            return call(entity=self._entity, **given)
        if not isinstance(given["entity"], self._entity):
            raise database_error.InvalidInputError(
                f"This Child Service works on {self._entity.__name__} instances only."
            )
        return call(**given)

    action.__name__ = name
    action.__qualname__ = f"BaseEntity.{name}"
    action.__doc__ = method.__doc__
    action.__signature__ = signature  # ty: ignore[unresolved-attribute]
    return action


class BaseEntity:
    """The shared structure every Child Service receives; each Child Service binds one Entity."""

    _entity: ClassVar[type]

    def __init__(self) -> None:
        self._database = database_interface()


for _name, _method in vars(database_interface).items():
    if (
        inspect.isfunction(_method)
        and not _name.startswith("_")
        and list(inspect.signature(_method).parameters)[1:2] == ["entity"]
    ):
        setattr(BaseEntity, _name, _action(_name, _method))
