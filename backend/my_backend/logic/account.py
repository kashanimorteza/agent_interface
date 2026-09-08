"""What the application does with a funded trading account.

Its own unit, so that a rule belonging to account alone has somewhere to go
without disturbing any other kind of data. Today it does what every kind of data
does; that it is separate is the point.
"""

from my_model import Account

from .base import ModelLogic


class AccountLogic(ModelLogic):
    """The behaviour of a funded trading account."""

    definition = Account
