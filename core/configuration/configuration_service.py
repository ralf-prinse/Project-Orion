import json
from pathlib import Path
from typing import Any

from core.configuration.models import OrionConfiguration
from core.configuration.profile_registry import ConfigurationProfileRegistry
from core.configuration.validation import ConfigurationValidationResult, ConfigurationValidator


class ConfigurationService:
    """
    Read, validate and write Orion configuration profiles.

    This service intentionally performs no trading calculations. It is a small
    infrastructure boundary that gives GUI, CLI and future API layers one stable
    way to work with configuration data.
    """

    def __init__(
        self,
        registry: ConfigurationProfileRegistry | None = None,
        validator: ConfigurationValidator | None = None,
    ):
        self.registry = registry or ConfigurationProfileRegistry()
        self.validator = validator or ConfigurationValidator()

    def default_configuration(self) -> OrionConfiguration:
        return self.registry.default()

    def get_profile(self, profile_name: str) -> OrionConfiguration:
        return self.registry.get(profile_name)

    def available_profiles(self) -> list[str]:
        return self.registry.list_profiles()

    def validate(self, configuration: OrionConfiguration) -> ConfigurationValidationResult:
        return self.validator.validate(configuration)

    def load_from_dict(self, data: dict[str, Any]) -> OrionConfiguration:
        configuration = OrionConfiguration.from_dict(data)
        validation = self.validate(configuration)

        if not validation.is_valid:
            raise ValueError("Invalid configuration: " + "; ".join(validation.errors))

        return configuration

    def load_from_file(self, path: str | Path) -> OrionConfiguration:
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)

        if not isinstance(data, dict):
            raise ValueError("Configuration file must contain a JSON object.")

        return self.load_from_dict(data)

    def save_to_file(self, configuration: OrionConfiguration, path: str | Path) -> None:
        validation = self.validate(configuration)
        if not validation.is_valid:
            raise ValueError("Invalid configuration: " + "; ".join(validation.errors))

        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as handle:
            json.dump(configuration.to_dict(), handle, indent=2, sort_keys=True)
            handle.write("\n")
