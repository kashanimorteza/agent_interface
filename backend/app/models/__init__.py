"""One SQLAlchemy model per project model — importing this package registers every table on Base.metadata."""
from app.models.trading_platform import TradingPlatform  # noqa: F401
from app.models.broker import Broker  # noqa: F401
from app.models.account import Account  # noqa: F401
from app.models.asset import Asset  # noqa: F401
from app.models.strategy import Strategy  # noqa: F401
from app.models.trailing_group import TrailingGroup  # noqa: F401
from app.models.trailing_rule import TrailingRule  # noqa: F401
from app.models.partial_group import PartialGroup  # noqa: F401
from app.models.partial_rule import PartialRule  # noqa: F401
from app.models.action_group import ActionGroup  # noqa: F401
from app.models.action import Action  # noqa: F401
from app.models.execute import Execute  # noqa: F401
from app.models.position import Position  # noqa: F401
