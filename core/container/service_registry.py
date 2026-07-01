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
    - replace registrations for tests or future provider swaps
    - remove registrations explicitly
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

    def replace_singleton(self, name: str, factory: Callable[[], Any]) -> None:
        """Replace an existing service registration with a singleton factory."""

        self._replace(
            name=name,
            factory=factory,
            lifetime=ServiceLifetime.SINGLETON,
        )

    def replace_transient(self, name: str, factory: Callable[[], Any]) -> None:
        """Replace an existing service registration with a transient factory."""

        self._replace(
            name=name,
            factory=factory,
            lifetime=ServiceLifetime.TRANSIENT,
        )

    def resolve(self, name: str) -> Any:
        cleaned_name = self._clean_name(name)

        if cleaned_name not in self._registrations:
            raise KeyError(f"Service is not registered: {cleaned_name}")

        registration = self._registrations[cleaned_name]

        if registration.lifetime == ServiceLifetime.TRANSIENT:
            return registration.factory()

        if cleaned_name not in self._singletons:
            self._singletons[cleaned_name] = registration.factory()

        return self._singletons[cleaned_name]

    def remove(self, name: str) -> None:
        """Remove a registered service and any cached singleton instance."""

        cleaned_name = self._clean_name(name)

        if cleaned_name not in self._registrations:
            raise KeyError(f"Service is not registered: {cleaned_name}")

        self._registrations.pop(cleaned_name)
        self._singletons.pop(cleaned_name, None)

    def is_registered(self, name: str) -> bool:
        cleaned_name = self._clean_name(name)
        return cleaned_name in self._registrations

    def registered_names(self) -> list[str]:
        return sorted(self._registrations.keys())

    def clear_singletons(self) -> None:
        """Clear cached singleton instances without changing registrations."""

        self._singletons.clear()

    def _register(
        self,
        name: str,
        factory: Callable[[], Any],
        lifetime: ServiceLifetime,
    ) -> None:
        cleaned_name = self._clean_name(name)
        self._validate_factory(factory)

        self._registrations[cleaned_name] = ServiceRegistration(
            factory=factory,
            lifetime=lifetime,
        )
        self._singletons.pop(cleaned_name, None)

    def _replace(
        self,
        name: str,
        factory: Callable[[], Any],
        lifetime: ServiceLifetime,
    ) -> None:
        cleaned_name = self._clean_name(name)

        if cleaned_name not in self._registrations:
            raise KeyError(f"Service is not registered: {cleaned_name}")

        self._register(
            name=cleaned_name,
            factory=factory,
            lifetime=lifetime,
        )

    def _clean_name(self, name: str) -> str:
        cleaned_name = str(name).strip()
        if not cleaned_name:
            raise ValueError("Service name cannot be empty.")

        return cleaned_name

    def _validate_factory(self, factory: Callable[[], Any]) -> None:
        if not callable(factory):
            raise TypeError("Service factory must be callable.")
