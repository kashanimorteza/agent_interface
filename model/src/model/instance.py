"""Instance: a user-owned connection through which a Trading Platform is reached."""

from .foundation import EncryptedCredential, Flag, GeneratedId, Integer, ModelFoundation, Relationship, Text
from .trading_platform import TradingPlatform
from .user import User


class Instance(ModelFoundation):
    persistence = "persistent"
    relationships = (
        Relationship(field="user_id", reference=User, reference_field="id", cardinality="many-to-one", optional=False),
        Relationship(field="trading_platform_id", reference=TradingPlatform, reference_field="id", cardinality="many-to-one", optional=False),
    )
    unique_sets = (("user_id", "name"),)

    id: GeneratedId = None
    user_id: Integer
    trading_platform_id: Integer
    name: Text
    ip: Text | None = None
    username: Text | None = None
    password: EncryptedCredential | None = None
    api_key: EncryptedCredential | None = None
    is_active: Flag = True
    description: Text | None = None
