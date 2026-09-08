"""The shared definition behaviour every entity in this package is built on."""

from .credentials import CredentialStorage
from .entity import Entity, PartialView, define_entity
from .field_spec import FieldSpec, FieldType
from .generation import GENERATE_SECURELY, Generated, awaits_generation
from .initial_records import InitialRecord
from .relationships import Cardinality, Relationship
from .resolution import applicable_defaults, complete_field, complete_fields
from .rules import DomainRule, RuleScope
from .unset import UNSET, is_stated

__all__ = [
    "Cardinality",
    "CredentialStorage",
    "DomainRule",
    "Entity",
    "FieldSpec",
    "FieldType",
    "GENERATE_SECURELY",
    "Generated",
    "InitialRecord",
    "PartialView",
    "Relationship",
    "RuleScope",
    "UNSET",
    "applicable_defaults",
    "awaits_generation",
    "complete_field",
    "complete_fields",
    "define_entity",
    "is_stated",
]
