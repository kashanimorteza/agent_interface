"""Logic Interface: the single root gateway that publishes the publication-enabled Service Interfaces."""

from logic.core.services import verify_publication as _verify_publication
from logic.services.entity import interface as Entity

__all__ = ["Entity"]

_verify_publication(__all__)
