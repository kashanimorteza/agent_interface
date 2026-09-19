"""Asset: an asset a broker provides that can be selected for trading."""

from .broker import Broker
from .foundation import Approximate, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text


class Asset(ModelFoundation):
    persistence = "persistent"
    relationships = (Relationship(field="broker_id", reference=Broker, reference_field="id", cardinality="many-to-one", optional=False),)
    unique_sets = (("broker_id", "symbol"),)

    id: GeneratedId = None
    broker_id: Integer
    symbol: Text
    category: Text
    point_size: Approximate = 0.0
    digits: Integer = 0
    is_active: Flag = True
    description: Text | None = None
