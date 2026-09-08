"""What the application does with something that can be traded.

Its own unit, so that a rule belonging to traded alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Asset

from .base import ModelLogic


class AssetLogic(ModelLogic):
    """The behaviour of something that can be traded."""

    definition = Asset
