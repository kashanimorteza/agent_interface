"""Broker Adapter: one Endpoint for every Action of the Broker Child Service."""

from collections.abc import Sequence
from typing import Annotated, Any

from fastapi import APIRouter, Body, HTTPException, Path, Query
from logic.interface import Entity

router = APIRouter(prefix="/broker", tags=["Broker"])
service = Entity.BrokerService()


@router.post("/add")
def add(
    entity: Annotated[Any, Body(embed=True)],
    instance: Annotated[Entity.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    """Persist a complete Entity instance and return it with generated values."""
    try:
        record = service.entity.from_json(entity)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return service.add(record, instance)


@router.put("/update/{id}")
def update(
    record_id: Annotated[int, Path(alias="id")],
    entity: Annotated[Any, Body(embed=True)],
    instance: Annotated[Entity.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    """Update the record with the Entity's id; return None when no record has it."""
    try:
        record = service.entity.from_json({**entity, "id": record_id})
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    return service.update(record, instance)


@router.get("/list")
def list(
    filters: Annotated[Sequence[Any] | None, Query()] = None,
    combination: Annotated[Any | None, Query()] = None,
    orders: Annotated[Sequence[Any] | None, Query()] = None,
    limit: Annotated[int | None, Query()] = None,
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the matching Entity instances."""
    return service.list(filters, combination, orders, limit, instance)


@router.delete("/delete/{id}")
def delete(
    record_id: Annotated[int, Path(alias="id")],
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Delete a record and report whether one existed."""
    return service.delete(record_id, instance)


@router.patch("/enable/{id}")
def enable(
    record_id: Annotated[int, Path(alias="id")],
    instance: Annotated[Entity.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    """Set a record active and return it, or None when no record has the id."""
    return service.enable(record_id, instance)


@router.patch("/disable/{id}")
def disable(
    record_id: Annotated[int, Path(alias="id")],
    instance: Annotated[Entity.DatabaseInstance | None, Body(embed=True)] = None,
) -> Any:
    """Set a record inactive and return it, or None when no record has the id."""
    return service.disable(record_id, instance)


@router.get("/get_by_id/{id}")
def get_by_id(
    record_id: Annotated[int, Path(alias="id")],
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the record with the id, or None."""
    return service.get_by_id(record_id, instance)


@router.get("/count")
def count(
    filters: Annotated[Sequence[Any] | None, Query()] = None,
    combination: Annotated[Any | None, Query()] = None,
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the number of matching records."""
    return service.count(filters, combination, instance)


@router.get("/sum")
def sum(
    field: Annotated[str, Query()],
    filters: Annotated[Sequence[Any] | None, Query()] = None,
    combination: Annotated[Any | None, Query()] = None,
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the total of a Field over the matching records."""
    return service.sum(field, filters, combination, instance)


@router.get("/min")
def min(
    field: Annotated[str, Query()],
    filters: Annotated[Sequence[Any] | None, Query()] = None,
    combination: Annotated[Any | None, Query()] = None,
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the smallest value of a Field over the matching records."""
    return service.min(field, filters, combination, instance)


@router.get("/max")
def max(
    field: Annotated[str, Query()],
    filters: Annotated[Sequence[Any] | None, Query()] = None,
    combination: Annotated[Any | None, Query()] = None,
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Return the largest value of a Field over the matching records."""
    return service.max(field, filters, combination, instance)


@router.delete("/truncate")
def truncate(
    instance: Annotated[Entity.DatabaseInstance | None, Query()] = None,
) -> Any:
    """Remove every record of the bound Entity and return how many were removed."""
    return service.truncate(instance)
