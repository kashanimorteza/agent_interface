"""Broker: a broker the system supports, owned by one user."""

from .foundation import Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text
from .user import User


class Broker(ModelFoundation):
    persistence = "persistent"
    relationships = (Relationship(field="user_id", reference=User, reference_field="id", cardinality="many-to-one", optional=False),)
    unique_sets = (("user_id", "name"),)

    id: GeneratedId = None
    name: Text
    user_id: Integer
    is_active: Flag = True
    description: Text | None = None
