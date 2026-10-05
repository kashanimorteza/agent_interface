# Entity Service

Entity Service gives every Model Entity its own Child Service. A caller selects a Child Service once and then calls its Actions without passing the Entity again: the Child Service adds its bound Entity to the request and hands it to Storage, and returns Storage's answer and errors unchanged. Entity Service also republishes the contracts a caller needs, so that no caller has to import Storage or Database.

```python
from logic.services.entity.interface import User

users = User()
print(users.count())
```

## Interface

`logic.services.entity.interface` publishes exactly the Child Services and the contracts of Storage's Interface (except the Storage gateway) as the identical objects. Base, the Storage gateway and every implementation are never published.

### Child Services

One for every Entity in Model's Entity Collection, each bound to its own Entity and offering every Action below.

| Child Service | Bound Entity |
| --- | --- |
| `User` | User |
| `TradingPlatform` | Trading Platform |
| `Instance` | Instance |
| `Currency` | Currency |
| `Broker` | Broker |
| `Asset` | Asset |
| `AccountGroup` | Account Group |
| `Account` | Account |
| `TrailingGroup` | Trailing Group |
| `TrailingRule` | Trailing Rule |
| `PartialGroup` | Partial Group |
| `PartialRule` | Partial Rule |
| `ActionGroup` | Action Group |
| `Action` | Action |
| `Position` | Position |

One example for each Child Service (each creates it and counts its records):

```python
from logic.services.entity.interface import (
    User,
    TradingPlatform,
    Instance,
    Currency,
    Broker,
    Asset,
    AccountGroup,
    Account,
    TrailingGroup,
    TrailingRule,
    PartialGroup,
    PartialRule,
    ActionGroup,
    Action,
    Position,
)

User().count()
TradingPlatform().count()
Instance().count()
Currency().count()
Broker().count()
Asset().count()
AccountGroup().count()
Account().count()
TrailingGroup().count()
TrailingRule().count()
PartialGroup().count()
PartialRule().count()
ActionGroup().count()
Action().count()
Position().count()
```

### Actions

Every Child Service has one Action for each Storage Action that takes an Entity, in Storage's order, with Storage's name, parameters and defaults, except that the Entity class parameter is removed because the Child Service supplies it. `add` and `update` keep their Entity instance parameter, and an instance that is not of the bound Entity is rejected with `InvalidInputError` before Storage is called.

| Action | What it does | Signature |
| --- | --- | --- |
| `add` | Stores one complete new Entity instance of the bound Entity and returns the stored Entity. | `add(entity: Any, instance: enum.Enum | None = None) -> Any` |
| `update` | Replaces every mutable Field of the stored record the instance's id identifies. | `update(entity: Any, instance: enum.Enum | None = None) -> Any` |
| `list` | Returns the bound Entity's records that match Filters, ordered and limited. | `list(filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, orders: collections.abc.Sequence[database.core.data.Order] | None = None, limit: int | None = None, instance: enum.Enum | None = None) -> collections.abc.Sequence[typing.Any]` |
| `get_by_id` | Returns the record with that id, or None. | `get_by_id(id: int, instance: enum.Enum | None = None) -> Any` |
| `delete` | Removes the record and returns the deleted Entity, or None. | `delete(id: int, instance: enum.Enum | None = None) -> Any` |
| `enable` | Sets is_active to True and returns the Entity, or None. | `enable(id: int, instance: enum.Enum | None = None) -> Any` |
| `disable` | Sets is_active to False and returns the Entity, or None. | `disable(id: int, instance: enum.Enum | None = None) -> Any` |
| `count` | Counts the matching records. | `count(filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> int` |
| `sum` | Totals a numeric Field over the matching records. | `sum(field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `min` | Smallest value of a comparable Field, or None. | `min(field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `max` | Largest value of a comparable Field, or None. | `max(field: Any, filters: collections.abc.Sequence[database.core.data.Filter] | None = None, combination: database.core.data.FilterCombination | None = None, instance: enum.Enum | None = None) -> Any` |
| `truncate` | Removes every record of the bound Entity and returns the count. | `truncate(instance: enum.Enum | None = None) -> int` |

#### add

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.add(model.Broker(name="Entity Add", user_id=1))
```

#### update

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
stored = brokers.add(model.Broker(name="Entity Update", user_id=1))
stored.description = "changed"
brokers.update(stored)
```

#### list

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.list(
    filters=[Filter(model.Broker.is_active, FilterOperator.EQUALS, True)],
    orders=[Order(model.Broker.name, OrderDirection.DESCENDING)],
    limit=5,
)
```

#### get_by_id

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.get_by_id(1)
```

#### delete

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.delete(brokers.add(model.Broker(name="Entity Delete", user_id=1)).id)
```

#### enable

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.enable(brokers.add(model.Broker(name="Entity Enable", user_id=1)).id)
```

#### disable

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.disable(brokers.add(model.Broker(name="Entity Disable", user_id=1)).id)
```

#### count

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
brokers.count()
```

#### sum

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
currencies.sum(model.Currency.decimal_digits)
```

#### min

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
currencies.min(model.Currency.code)
```

#### max

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
currencies.max(model.Currency.code)
```

#### truncate

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

brokers, currencies, rules = Broker(), Currency(), TrailingRule()
rules.add(model.TrailingRule(name="Entity Truncate", trailing_group_id=1, trigger_percentage=Decimal("1")))
rules.truncate()
```

### Republished contracts

Each is the identical object Storage's Interface publishes.

#### CommandResult

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

print(CommandResult.__name__)
```

#### ConfigurationError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

issubclass(ConfigurationError, DatabaseError)
```

#### ConnectionFailureError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

issubclass(ConnectionFailureError, DatabaseError)
```

#### DatabaseError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

try:
    User().get_by_id("1")
except DatabaseError as error:
    print(type(error).__name__)
```

#### DatabaseInstance

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

User().count(instance=DatabaseInstance.SQLITE)
```

#### DeclarationMismatchError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

issubclass(DeclarationMismatchError, DatabaseError)
```

#### ExecutionError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

try:
    Broker().add(model.Broker(name="FxPro", user_id=1))
except ExecutionError:
    print("refused")
```

#### Filter

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

Filter(model.User.is_active, FilterOperator.EQUALS, True)
```

#### FilterCombination

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

[member.name for member in FilterCombination]
```

#### FilterOperator

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

[member.name for member in FilterOperator]
```

#### InactiveInstanceError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

issubclass(InactiveInstanceError, DatabaseError)
```

#### InvalidInputError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

try:
    Broker().add(model.User(name="x", username="y", password="p", api_key="k"))
except InvalidInputError:
    print("another Entity refused")
```

#### LifecycleError

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

issubclass(LifecycleError, DatabaseError)
```

#### LifecycleResult

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

print(LifecycleResult.__name__)
```

#### Order

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

Order(model.User.name, OrderDirection.DESCENDING)
```

#### OrderDirection

```python
from decimal import Decimal

from logic.services.entity.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    CommandResult,
    ConfigurationError,
    ConnectionFailureError,
    Currency,
    DatabaseError,
    DatabaseInstance,
    DeclarationMismatchError,
    ExecutionError,
    Filter,
    FilterCombination,
    FilterOperator,
    InactiveInstanceError,
    Instance,
    InvalidInputError,
    LifecycleError,
    LifecycleResult,
    Order,
    OrderDirection,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)
from model import interface as model

[member.name for member in OrderDirection]
```

## Use

A caller imports a Child Service and the contracts it needs from the Entity Service Interface only:

```python
from logic.services.entity.interface import Filter, FilterOperator, User
from model import interface as model

users = User()
active = users.list(filters=[Filter(model.User.is_active, FilterOperator.EQUALS, True)])
print([user.name for user in active])
```

A Child Service holds only Behaviour specific to its Entity; everything shared comes from Base. A Child Service may add an Action of its own, or override a Base Action for its own Entity, but never detaches itself from Base. For example:

```python
from logic.services.entity.interface import Broker
from model import interface as model


class ActiveBrokers(Broker):
    def names(self):
        return [broker.name for broker in self.list()]


print(ActiveBrokers().names())
```

## Verify

This shows that Entity Service matches Model's Entity Collection and Storage's Interface:

```python
import logic.services.entity.interface as entity
import logic.services.storage.interface as storage
import model.interface as model

assert sorted(entity.__all__) == sorted(
    [e.__name__ for e in model.entities] + [n for n in storage.__all__ if n != "Storage"]
)
assert all(getattr(entity, n) is getattr(storage, n) for n in storage.__all__ if n != "Storage")
assert all(getattr(entity, e.__name__)._entity is e for e in model.entities)
assert not hasattr(entity, "Storage") and not hasattr(entity, "BaseEntity")
```
