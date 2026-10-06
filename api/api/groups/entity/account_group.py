"""The AccountGroup Adapter: an Endpoint for every Action of its Child Service."""

from typing import Annotated, Any

from fastapi import APIRouter, Body, Path, Query
from logic.interface import Entity

from api import conversion

router = APIRouter(tags=["Entity · account_group"])
service = Entity.Service.AccountGroup()
bound = Entity.Model.AccountGroup


@router.post("/add")
def add(
    entity: Annotated[Any, Body(embed=True), *conversion.entity_object(bound)],
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Store one complete new Entity instance and return the stored Entity."""
    return service.add(entity, instance)


@router.put("/update")
def update(
    entity: Annotated[Any, Body(embed=True), *conversion.entity_object(bound)],
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Replace every mutable Field of the stored record; null when no record exists."""
    return service.update(entity, instance)


@router.post("/list")
def list(
    filters: Annotated[Any, Body(embed=True), *conversion.filters(bound)] = None,
    combination: Annotated[Any, Body(embed=True), *conversion.filter_combination()] = None,
    orders: Annotated[Any, Body(embed=True), *conversion.orders(bound)] = None,
    limit: Annotated[int | None, Body(embed=True)] = None,
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Return the Entities that match; a zero or negative limit means no limit."""
    return service.list(filters, combination, orders, limit, instance)


@router.get("/get_by_id/{id}")
def get_by_id(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Query(), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Return the Entity with the given id, or null."""
    return service.get_by_id(id, instance)


@router.delete("/delete/{id}")
def delete(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Query(), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Remove the record and return the final deleted Entity, or null."""
    return service.delete(id, instance)


@router.patch("/enable/{id}")
def enable(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Set only the activity Field to true and return the final Entity, or null."""
    return service.enable(id, instance)


@router.patch("/disable/{id}")
def disable(
    id: Annotated[int, Path()],
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Set only the activity Field to false and return the final Entity, or null."""
    return service.disable(id, instance)


@router.post("/count")
def count(
    filters: Annotated[Any, Body(embed=True), *conversion.filters(bound)] = None,
    combination: Annotated[Any, Body(embed=True), *conversion.filter_combination()] = None,
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[int, conversion.RESULT]:
    """Return the number of matching records."""
    return service.count(filters, combination, instance)


@router.post("/sum")
def sum(
    field: Annotated[Any, Body(embed=True), *conversion.field_reference(bound)],
    filters: Annotated[Any, Body(embed=True), *conversion.filters(bound)] = None,
    combination: Annotated[Any, Body(embed=True), *conversion.filter_combination()] = None,
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Return the total of a numeric Field, ignoring nulls, or zero."""
    return service.sum(field, filters, combination, instance)


@router.post("/min")
def min(
    field: Annotated[Any, Body(embed=True), *conversion.field_reference(bound)],
    filters: Annotated[Any, Body(embed=True), *conversion.filters(bound)] = None,
    combination: Annotated[Any, Body(embed=True), *conversion.filter_combination()] = None,
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Return the smallest value of a comparable Field, ignoring nulls, or null."""
    return service.min(field, filters, combination, instance)


@router.post("/max")
def max(
    field: Annotated[Any, Body(embed=True), *conversion.field_reference(bound)],
    filters: Annotated[Any, Body(embed=True), *conversion.filters(bound)] = None,
    combination: Annotated[Any, Body(embed=True), *conversion.filter_combination()] = None,
    instance: Annotated[Any, Body(embed=True), *conversion.database_instance()] = None,
) -> Annotated[Any, conversion.RESULT]:
    """Return the largest value of a comparable Field, ignoring nulls, or null."""
    return service.max(field, filters, combination, instance)


@router.delete("/truncate")
def truncate(
    instance: Annotated[Any, Query(), *conversion.database_instance()] = None,
) -> Annotated[int, conversion.RESULT]:
    """Remove every record of the Entity, keep its Table, and return the deleted count."""
    return service.truncate(instance)
