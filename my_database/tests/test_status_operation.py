from __future__ import annotations

from my_model.broker import Broker
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from my_database import interface
from my_database._base import Base
from my_database._mapping import EntityMapping, mapping_for


class _NoStatusRow(Base):
    """A synthetic row with no status column, used only to prove the generic rejection."""

    __tablename__ = "_test_no_status_row"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


def test_set_status_enables_and_disables_a_real_entity():
    from my_model.user import User

    created = interface.add(User(name="Ada", username="ada", password="x", api_key="y"))
    assert created.id is not None
    disabled = interface.set_status(User, created.id, "disable")
    assert disabled.status is False
    enabled = interface.set_status(User, created.id, "enable")
    assert enabled.status is True


def test_generic_status_check_true_for_entity_with_status_field():
    assert interface.has_status_field(mapping_for(Broker)) is True


def test_generic_status_check_false_for_entity_without_status_field():
    fake_mapping = EntityMapping(model_cls=Broker, orm_cls=_NoStatusRow)
    assert interface.has_status_field(fake_mapping) is False
