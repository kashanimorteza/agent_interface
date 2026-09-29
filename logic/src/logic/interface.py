"""Interface: the only public Logic surface."""

from collections.abc import Mapping, Sequence
from typing import Any

from database.interface import (
    CommandResult,
    Database,
    Filter,
    FilterCombination,
    FilterOperator,
    Order,
    OrderDirection,
)
from model.interface import (
    Account,
    AccountGroup,
    Action,
    ActionGroup,
    Asset,
    Broker,
    Currency,
    Instance,
    PartialGroup,
    PartialRule,
    Position,
    TradingPlatform,
    TrailingGroup,
    TrailingRule,
    User,
)

from logic.core.configuration import Configuration, ConfigurationError
from logic.core.credentials import WITHHELD, CredentialProtector
from logic.core.dependency import Dependency
from logic.core.outcome import Outcome, OutcomeKind
from logic.services.database.interface import DatabaseService
from logic.services.entity.base import EntityServiceBase, Published
from logic.services.entity.interface import (
    AccountGroupService,
    AccountService,
    ActionGroupService,
    ActionService,
    AssetService,
    BrokerService,
    CurrencyService,
    InstanceService,
    PartialGroupService,
    PartialRuleService,
    PositionService,
    TradingPlatformService,
    TrailingGroupService,
    TrailingRuleService,
    UserService,
)

__all__ = [
    "WITHHELD",
    "Account",
    "AccountGroup",
    "Action",
    "ActionGroup",
    "Asset",
    "Broker",
    "CommandResult",
    "Configuration",
    "ConfigurationError",
    "Currency",
    "DatabaseCategory",
    "EntityCategory",
    "EntityOperations",
    "Filter",
    "FilterCombination",
    "FilterOperator",
    "Instance",
    "Logic",
    "Order",
    "OrderDirection",
    "Outcome",
    "OutcomeKind",
    "PartialGroup",
    "PartialRule",
    "Position",
    "TradingPlatform",
    "TrailingGroup",
    "TrailingRule",
    "User",
]


class EntityOperations[T: Published]:
    """The Operations available for the records of one Entity; every Operation answers with an Outcome."""

    def __init__(self, service: EntityServiceBase[T]) -> None:
        """Wrap the Entity's Service; the wrapper only hands each Operation to it.

        Args:
            service (EntityServiceBase): The Entity's Service.
        """
        self._service = service

    def add(self, entity: T) -> Outcome[T]:
        """Add a record.

        Args:
            entity (T): Complete Entity instance; credential Fields hold the credentials to store.

        Returns:
            (Outcome): Success holds the created record with generated values and credentials withheld. Failures: invalid (a value breaks a declared constraint, or a credential is missing or holds the withheld marker), conflict (a unique value is already stored), broken_reference (a referred record does not exist), unavailable.
        """
        return self._service.add(entity)

    def get_by_id(self, record_id: int) -> Outcome[T]:
        """Retrieve a record by its id.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): Success holds the record with credentials withheld. Failures: not_found, invalid, unavailable.
        """
        return self._service.get_by_id(record_id)

    def update(self, entity: T) -> Outcome[T]:
        """Edit a record: every mutable Field takes the supplied value.

        Args:
            entity (T): Complete Entity instance holding the record's id. A credential Field holding the withheld marker keeps its stored value; any other value replaces it.

        Returns:
            (Outcome): Success holds the updated record with credentials withheld. Failures: not_found, invalid (also a credential an Account shares with its Instance), conflict, broken_reference, unavailable; the record is unchanged on failure.
        """
        return self._service.update(entity)

    def delete(self, record_id: int) -> Outcome[bool]:
        """Delete a record.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): Success holds True. Failures: not_found, invalid, broken_reference (another record still refers to it), unavailable.
        """
        return self._service.delete(record_id)

    def enable(self, record_id: int) -> Outcome[T]:
        """Mark a record active.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): Success holds the record with credentials withheld. Failures: not_found, invalid, unavailable.
        """
        return self._service.enable(record_id)

    def disable(self, record_id: int) -> Outcome[T]:
        """Mark a record inactive.

        Args:
            record_id (int): Id of the record.

        Returns:
            (Outcome): Success holds the record with credentials withheld. Failures: not_found, invalid, unavailable.
        """
        return self._service.disable(record_id)

    def list(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
        orders: Sequence[Order] | None = None,
        limit: int | None = None,
    ) -> Outcome[Sequence[T]]:
        """List the matching records.

        Args:
            filters (Sequence, optional): Conditions on Fields; a credential Field cannot be used.
            combination (FilterCombination, optional): How the filters combine.
            orders (Sequence, optional): Ordering instructions; a credential Field cannot be used.
            limit (int, optional): Most records to return; zero or less means no limit.

        Returns:
            (Outcome): Success holds the matching records with credentials withheld (an empty result is a success). Failures: invalid (an unknown Field, a credential Field, a wrongly typed argument), unavailable.
        """
        return self._service.list(filters, combination, orders, limit)

    def count(
        self,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[int]:
        """Count the matching records.

        Args:
            filters (Sequence, optional): Conditions on Fields; a credential Field cannot be used.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): Success holds the number of matching records. Failures: invalid, unavailable.
        """
        return self._service.count(filters, combination)

    def sum(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Total a numeric Field over the matching records.

        Args:
            field (str): Name of the Field; a credential Field cannot be used.
            filters (Sequence, optional): Conditions on Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): Success holds the total, or zero when no value is usable. Failures: invalid (an unknown, credential, or non-numeric Field), unavailable.
        """
        return self._service.sum(field, filters, combination)

    def min(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Find the smallest value of a Field over the matching records.

        Args:
            field (str): Name of the Field; a credential Field cannot be used.
            filters (Sequence, optional): Conditions on Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): Success holds the smallest value, or no value when none is usable. Failures: invalid (an unknown or credential Field), unavailable.
        """
        return self._service.min(field, filters, combination)

    def max(
        self,
        field: str,
        filters: Sequence[Filter] | None = None,
        combination: FilterCombination | None = None,
    ) -> Outcome[Any]:
        """Find the largest value of a Field over the matching records.

        Args:
            field (str): Name of the Field; a credential Field cannot be used.
            filters (Sequence, optional): Conditions on Fields.
            combination (FilterCombination, optional): How the filters combine.

        Returns:
            (Outcome): Success holds the largest value, or no value when none is usable. Failures: invalid (an unknown or credential Field), unavailable.
        """
        return self._service.max(field, filters, combination)

    def truncate(self) -> Outcome[int]:
        """Remove every record of the Entity.

        Returns:
            (Outcome): Success holds the number of removed records. Failures: broken_reference (another record still refers to one; nothing is removed), unavailable.
        """
        return self._service.truncate()


class EntityCategory:
    """The Entity Service Category: one Class Category of Operations for each Entity.

    Attributes:
        user: Operations on User records.
        trading_platform: Operations on TradingPlatform records.
        instance: Operations on Instance records.
        currency: Operations on Currency records.
        broker: Operations on Broker records.
        asset: Operations on Asset records.
        account_group: Operations on AccountGroup records.
        account: Operations on Account records.
        trailing_group: Operations on TrailingGroup records.
        trailing_rule: Operations on TrailingRule records.
        partial_group: Operations on PartialGroup records.
        partial_rule: Operations on PartialRule records.
        action_group: Operations on ActionGroup records.
        action: Operations on Action records.
        position: Operations on Position records.
    """

    def __init__(
        self,
        database: Database,
        dependency: Dependency,
        protector: CredentialProtector,
    ) -> None:
        """Gather each Entity's Operations.

        Args:
            database (Database): Database's published surface.
            dependency (Dependency): Bounded use of the dependency.
            protector (CredentialProtector): Protection of credential Fields before storage.
        """
        self.user: EntityOperations[User] = EntityOperations(
            UserService(database, dependency, protector)
        )
        self.trading_platform: EntityOperations[TradingPlatform] = EntityOperations(
            TradingPlatformService(database, dependency, protector)
        )
        self.instance: EntityOperations[Instance] = EntityOperations(
            InstanceService(database, dependency, protector)
        )
        self.currency: EntityOperations[Currency] = EntityOperations(
            CurrencyService(database, dependency, protector)
        )
        self.broker: EntityOperations[Broker] = EntityOperations(
            BrokerService(database, dependency, protector)
        )
        self.asset: EntityOperations[Asset] = EntityOperations(
            AssetService(database, dependency, protector)
        )
        self.account_group: EntityOperations[AccountGroup] = EntityOperations(
            AccountGroupService(database, dependency, protector)
        )
        self.account: EntityOperations[Account] = EntityOperations(
            AccountService(database, dependency, protector)
        )
        self.trailing_group: EntityOperations[TrailingGroup] = EntityOperations(
            TrailingGroupService(database, dependency, protector)
        )
        self.trailing_rule: EntityOperations[TrailingRule] = EntityOperations(
            TrailingRuleService(database, dependency, protector)
        )
        self.partial_group: EntityOperations[PartialGroup] = EntityOperations(
            PartialGroupService(database, dependency, protector)
        )
        self.partial_rule: EntityOperations[PartialRule] = EntityOperations(
            PartialRuleService(database, dependency, protector)
        )
        self.action_group: EntityOperations[ActionGroup] = EntityOperations(
            ActionGroupService(database, dependency, protector)
        )
        self.action: EntityOperations[Action] = EntityOperations(
            ActionService(database, dependency, protector)
        )
        self.position: EntityOperations[Position] = EntityOperations(
            PositionService(database, dependency, protector)
        )


class DatabaseCategory:
    """The Database Service Category: Operations that concern no single Entity."""

    def __init__(self, service: DatabaseService) -> None:
        """Wrap the Database Service; the wrapper only hands each Operation to it.

        Args:
            service (DatabaseService): The Database Service.
        """
        self._service = service

    def execute_command(
        self, command: str, parameters: Mapping[str, Any] | None = None
    ) -> Outcome[CommandResult]:
        """Run a SQL command with named bound parameters.

        Args:
            command (str): SQL command using :name parameter markers.
            parameters (Mapping, optional): Value for each named parameter.

        Returns:
            (Outcome): Success holds the Command Result (rows and affected count). Failures: invalid (a refused command), unavailable; the command is attempted once.
        """
        return self._service.execute_command(command, parameters)


class Logic:
    """Logic's outward Interface, organized into Service Categories.

    Attributes:
        entity: The Entity Service Category.
        database: The Database Service Category.
    """

    def __init__(
        self,
        configuration: Configuration | None = None,
        database: Database | None = None,
    ) -> None:
        """Validate the runtime configuration and gather every Operation.

        Args:
            configuration (Configuration, optional): Runtime values to use instead of the process environment.
            database (Database, optional): Database's published surface to use instead of the default.
        """
        configuration = configuration or Configuration.from_environment()
        database = database or Database()
        dependency = Dependency(configuration)
        protector = CredentialProtector(configuration)
        self.entity = EntityCategory(database, dependency, protector)
        self.database = DatabaseCategory(DatabaseService(database, dependency))
