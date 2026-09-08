"""What the application does with a supported trading API standard.

Its own unit, so that a rule belonging to standard alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import TradingPlatform

from .base import ModelLogic


class TradingPlatformLogic(ModelLogic):
    """The behaviour of a supported trading API standard."""

    definition = TradingPlatform
