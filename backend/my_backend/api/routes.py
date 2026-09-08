"""How a request becomes a call on the behaviour beneath.

One router per kind of data, built the same way for all of them, because what
differs between them is their behaviour and not the way a request reaches it.
Each operation here decodes, calls a unit, and turns what comes back into a
response. It decides nothing else — no rule of the application lives at this
boundary.
"""

import re

# Annotations here are evaluated as they are written, not kept as text: the
# shapes a route carries are built for that kind of data at the moment its
# router is, and a name that only exists inside this function has to be a type
# rather than something to look up later.
from typing import Annotated

from fastapi import APIRouter, Body, Path, Query
from pydantic import BaseModel

from ..configuration import Listing
from ..faults import Unsupported
from ..logic import Behaviour, ModelLogic
from .representations import Shapes


class StatusChange(BaseModel):
    """Which of the two actions to apply to a record's active state."""

    action: str


def resource_path(entity_name: str) -> str:
    """The path one kind of data is reached under."""

    spaced = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "-", entity_name).lower()
    head, _, tail = spaced.rpartition("-")
    if tail.endswith("y") and not tail.endswith(("ay", "ey", "iy", "oy", "uy")):
        tail = f"{tail[:-1]}ies"
    elif tail.endswith(("s", "x", "z", "ch", "sh")):
        tail = f"{tail}es"
    else:
        tail = f"{tail}s"
    return f"{head}-{tail}" if head else tail


def router_for(unit: ModelLogic, listing: Listing) -> APIRouter:
    """Everything the contract offers for one kind of data."""

    shapes = Shapes(unit.definition)
    name = unit.definition.entity_name
    router = APIRouter(prefix=f"/{resource_path(name)}", tags=[name])

    Incoming = shapes.incoming
    Change = shapes.change
    Outgoing = shapes.outgoing
    Identifier = Annotated[int, Path(description=f"Identifies one {name}.")]

    @router.get("/", summary=f"List {name} records")
    def list_records(
        limit: Annotated[int | None, Query(ge=1, description="How many to return.")] = None,
        offset: Annotated[int | None, Query(ge=0, description="How many to skip.")] = None,
        order_by: Annotated[str | None, Query(description="A field to order by.")] = None,
    ) -> list[Outgoing]:
        chosen = min(limit or listing.default_limit, listing.maximum_limit)
        found = unit.list(limit=chosen, offset=offset, order_by=order_by)
        return [shapes.present(record) for record in found]

    @router.post("/", status_code=201, summary=f"Create one {name}")
    def create_record(supplied: Annotated[Incoming, Body()]) -> Outgoing:
        created = unit.create(supplied.model_dump(exclude_unset=True))
        return shapes.present(created)

    @router.get("/{identifier}", summary=f"Get one {name}")
    def get_record(identifier: Identifier) -> Outgoing:
        return shapes.present(unit.get(identifier))

    @router.patch("/{identifier}", summary=f"Change one {name}")
    def change_record(identifier: Identifier, supplied: Annotated[Change, Body()]) -> Outgoing:
        changed = unit.update(identifier, supplied.model_dump(exclude_unset=True))
        return shapes.present(changed)

    @router.delete("/{identifier}", status_code=204, summary=f"Remove one {name}")
    def remove_record(identifier: Identifier) -> None:
        unit.delete(identifier)

    if unit.offers_status():

        @router.post("/{identifier}/status", summary=f"Enable or disable one {name}")
        def change_status(
            identifier: Identifier, supplied: Annotated[StatusChange, Body()]
        ) -> Outgoing:
            if supplied.action not in ("enable", "disable"):
                raise Unsupported(
                    f"{supplied.action!r} is not an action; enabling and disabling are the only two"
                )
            changed = unit.set_status(identifier, enabled=supplied.action == "enable")
            return shapes.present(changed)

    return router


def routers(behaviour: Behaviour, listing: Listing) -> list[APIRouter]:
    """One router for every kind of data the project defines."""

    return [router_for(unit, listing) for unit in behaviour]


__all__ = ["StatusChange", "resource_path", "router_for", "routers"]
