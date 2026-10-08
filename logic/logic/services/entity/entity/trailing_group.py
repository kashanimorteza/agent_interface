"""The Trailing Group Child Service."""

from model import interface as model

from logic.services.entity.base import BaseEntity


class TrailingGroup(BaseEntity):
    _entity = model.TrailingGroup
