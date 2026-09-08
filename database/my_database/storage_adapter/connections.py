"""The one place this layer reaches its engine.

Every stored operation arrives here, which is what leaves the engine
replaceable: nothing above this module knows which one it is, and where a
file-backed engine keeps its data is decided from this layer's own location
rather than from wherever a process was started.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.engine import URL

from . import secrets
from .configuration import (
    Configuration,
    ConfigurationError,
    EngineProfile,
    InstanceSetting,
    data_directory,
    load,
)


@dataclass(frozen=True, slots=True)
class Connection:
    """A resolved way of reaching one Instance."""

    instance: InstanceSetting
    profile: EngineProfile
    engine: Engine

    def dispose(self) -> None:
        self.engine.dispose()


def storage_location(instance: InstanceSetting) -> Path:
    """Where a file-backed Instance keeps its data, independent of the caller."""

    return data_directory() / f"{instance.database}.db"


def _url(instance: InstanceSetting, profile: EngineProfile) -> URL | str:
    if profile.is_file_backed:
        location = storage_location(instance)
        location.parent.mkdir(parents=True, exist_ok=True)
        return f"{profile.url_scheme}:///{location}"

    connection = {**instance.connection}
    return URL.create(
        profile.url_scheme,
        username=secrets.require(instance.secrets["username"])
        if "username" in instance.secrets
        else None,
        password=secrets.require(instance.secrets["password"])
        if "password" in instance.secrets
        else None,
        host=connection.get("host"),
        port=connection.get("port"),
        database=instance.database,
    )


def _apply_profile_settings(engine: Engine, profile: EngineProfile) -> None:
    """Put the engine profile's declared connection settings into effect."""

    if profile.connection.get("foreign_keys"):

        @event.listens_for(engine, "connect")
        def _enable_reference_enforcement(connection, _record):  # noqa: ANN001
            cursor = connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()


class Connections:
    """Opens, keeps and releases one connection per Instance."""

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._configuration = configuration or load()
        self._open: dict[str, Connection] = {}

    @property
    def configuration(self) -> Configuration:
        return self._configuration

    def for_instance(self, key: str | None = None) -> Connection:
        """The connection for a selected Instance, opening it if needed.

        A named Instance nobody declared is refused here rather than answered
        with the default, and a connection that fails stays failed: nothing
        moves the work to another Instance.
        """

        instance = self._configuration.instance(key)
        if instance.key in self._open:
            return self._open[instance.key]

        profile = self._configuration.profile_for(instance)
        arguments: dict[str, object] = {}
        if "check_same_thread" in profile.connection:
            arguments["check_same_thread"] = profile.connection["check_same_thread"]

        engine = create_engine(_url(instance, profile), connect_args=arguments, future=True)
        _apply_profile_settings(engine, profile)

        connection = Connection(instance=instance, profile=profile, engine=engine)
        self._open[instance.key] = connection
        return connection

    def release(self) -> None:
        """Let go of everything held open."""

        for connection in self._open.values():
            connection.dispose()
        self._open.clear()


__all__ = [
    "Connection",
    "Connections",
    "ConfigurationError",
    "storage_location",
]
