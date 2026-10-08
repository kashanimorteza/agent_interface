"""The Partial Group Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class PartialGroup(BaseEntity):
    _entity = model.PartialGroup
