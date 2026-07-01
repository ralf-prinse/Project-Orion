from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Any


class ServiceLifetime(str, Enum):
    """Supported service lifetimes for the Orion service registry."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"


@dataclass(frozen=True)
class ServiceRegistration:
    """
    Describes one registered service factory.

    The registry stores factories rather than already-created instances so the
    composition root remains explicit and deterministic. Instances are created
    only when a service is resolved.
    """

    factory: Callable[[], Any]
    lifetime: ServiceLifetime


class ServiceRegistry:
    """
    Small explicit service registry for Project Orion.

    This is intentionally not a full IoC framework. Orion favours predictable
    construction over reflection, decorators or automatic discovery. The
    registry supports only the behaviour needed by the composition root:

    - register singleton factories
    - register transient factories
    - resolve registered services deterministically
    - fail clearly when a service is missing
    """

    def __init__(self) -> None:
        self._registrations: dict[str, ServiceRegistration] = {}
        self._singletons: dict[str, Any] = {}

    def register_singleton(self, name: str, factory: Callable[[], Any]) -> None:
        self._register(
            name=name,
            factory=factory,
            lifetime=ServiceLifetime.SINGLETON,
        )

    def register_transient(self, name: str, factory: Callable[[], Any]) -> None:
        self._register(
            name=name,
            factory=factory,
            lifetime=ServiceLifetime.TRANSIENT,
        )

    def resolve(self, name: str) -> Any:
        if name not in self._registrations:
            raise KeyError(f"Service is not registered: {name}")

        registration = self._registrations[name]

        if registration.lifetime == ServiceLifetime.TRANSIENT:
            return registration.factory()

        if name not in self._singletons:
            self._singletons[name] = registration.factory()

        return self._singletons[name]

    def is_registered(self, name: str) -> bool:
        return name in self._registrations

    def registered_names(self) -> list[str]:
        return sorted(self._registrations.keys())

    def _register(
        self,
        name: str,
        factory: Callable[[], Any],
        lifetime: ServiceLifetime,
    ) -> None:
        cleaned_name = str(name).strip()
        if not cleaned_name:
            raise ValueError("Service name cannot be empty.")

        if not callable(factory):
            raise TypeError("Service factory must be callable.")

        self._registrations[cleaned_name] = ServiceRegistration(
            factory=factory,
            lifetime=lifetime,
        )
        self._singletons.pop(cleaned_name, None)
