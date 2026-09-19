"""Action Group: an independent grouping of trading actions by risk profile."""

from .foundation import Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text
from .user import User


class ActionGroup(ModelFoundation):
    persistence = "persistent"
    relationships = (Relationship(field="user_id", reference=User, reference_field="id", cardinality="many-to-one", optional=False),)
    unique_sets = (("user_id", "name"),)

    id: GeneratedId = None
    user_id: Integer
    name: Text
    is_active: Flag = True
    description: Text | None = None
