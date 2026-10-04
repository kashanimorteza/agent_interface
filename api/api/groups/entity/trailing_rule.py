"""API Adapter of the TrailingRule Entity: one Endpoint for every Action of its Child Service."""

from typing import Annotated, Any

from fastapi import APIRouter, Body, Path
from logic.interface import Entity

from api.groups.entity import _wire

router = APIRouter(prefix="/trailing_rule")

service = Entity.TrailingRule


@router.post("/add")
def add_endpoint(
    entity: Annotated[dict[str, Any], Body(embed=True)],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.add(_wire.bind_entity(service, entity), instance))


@router.post("/update")
def update_endpoint(
    entity: Annotated[dict[str, Any], Body(embed=True)],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.update(_wire.bind_entity(service, entity), instance))


@router.post("/list")
def list_endpoint(
    filters: Annotated[list[_wire.FilterBody] | None, Body(embed=True)] = None,
    combination: Annotated[Entity.FilterCombination | None, Body(embed=True)] = None,
    orders: Annotated[list[_wire.OrderBody] | None, Body(embed=True)] = None,
    limit: Annotated[int | None, Body(embed=True)] = None,
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(
        child.list(
            _wire.bind_filters(service, filters),
            combination,
            _wire.bind_orders(service, orders),
            limit,
            instance,
        )
    )


@router.post("/get_by_id/{id}")
def get_by_id_endpoint(
    id: Annotated[int, Path()],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.get_by_id(id, instance))


@router.post("/delete/{id}")
def delete_endpoint(
    id: Annotated[int, Path()],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.delete(id, instance))


@router.post("/enable/{id}")
def enable_endpoint(
    id: Annotated[int, Path()],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.enable(id, instance))


@router.post("/disable/{id}")
def disable_endpoint(
    id: Annotated[int, Path()],
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.disable(id, instance))


@router.post("/count")
def count_endpoint(
    filters: Annotated[list[_wire.FilterBody] | None, Body(embed=True)] = None,
    combination: Annotated[Entity.FilterCombination | None, Body(embed=True)] = None,
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(
        child.count(_wire.bind_filters(service, filters), combination, instance)
    )


@router.post("/sum")
def sum_endpoint(
    field: Annotated[str, Body(embed=True)],
    filters: Annotated[list[_wire.FilterBody] | None, Body(embed=True)] = None,
    combination: Annotated[Entity.FilterCombination | None, Body(embed=True)] = None,
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(
        child.sum(
            _wire.bind_field(service, field),
            _wire.bind_filters(service, filters),
            combination,
            instance,
        )
    )


@router.post("/min")
def min_endpoint(
    field: Annotated[str, Body(embed=True)],
    filters: Annotated[list[_wire.FilterBody] | None, Body(embed=True)] = None,
    combination: Annotated[Entity.FilterCombination | None, Body(embed=True)] = None,
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(
        child.min(
            _wire.bind_field(service, field),
            _wire.bind_filters(service, filters),
            combination,
            instance,
        )
    )


@router.post("/max")
def max_endpoint(
    field: Annotated[str, Body(embed=True)],
    filters: Annotated[list[_wire.FilterBody] | None, Body(embed=True)] = None,
    combination: Annotated[Entity.FilterCombination | None, Body(embed=True)] = None,
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(
        child.max(
            _wire.bind_field(service, field),
            _wire.bind_filters(service, filters),
            combination,
            instance,
        )
    )


@router.post("/truncate")
def truncate_endpoint(
    instance: Annotated[_wire.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    child = service()
    return _wire.encode(child.truncate(instance))
