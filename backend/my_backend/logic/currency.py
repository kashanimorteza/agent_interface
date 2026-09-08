"""What the application does with a currency the system trades in.

Its own unit, so that a rule belonging to in alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Currency

from .base import ModelLogic


class CurrencyLogic(ModelLogic):
    """The behaviour of a currency the system trades in."""

    definition = Currency
