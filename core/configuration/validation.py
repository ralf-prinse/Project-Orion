from dataclasses import dataclass, field

from core.configuration.models import OrionConfiguration


@dataclass(frozen=True)
class ConfigurationValidationResult:
    """
    Validation result for an OrionConfiguration.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors


class ConfigurationValidator:
    """
    Deterministic validation for user-facing Orion configuration profiles.

    The validator protects the application from invalid settings but does not
    make trading decisions. Domain-level risk checks still remain inside the
    Risk Manager and Decision Layer.
    """

    def validate(self, configuration: OrionConfiguration) -> ConfigurationValidationResult:
        errors: list[str] = []
        warnings: list[str] = []

        self._validate_profile_identity(configuration, errors)
        self._validate_scan(configuration, errors)
        self._validate_trading_risk(configuration, errors, warnings)
        self._validate_planner(configuration, errors)
        self._validate_presentation(configuration, errors)

        return ConfigurationValidationResult(errors=errors, warnings=warnings)

    def _validate_profile_identity(
        self,
        configuration: OrionConfiguration,
        errors: list[str],
    ) -> None:
        if not configuration.profile_name.strip():
            errors.append("profile_name is required.")

    def _validate_scan(
        self,
        configuration: OrionConfiguration,
        errors: list[str],
    ) -> None:
        if configuration.scan.max_opportunities < 0:
            errors.append("scan.max_opportunities must be zero or greater.")

    def _validate_trading_risk(
        self,
        configuration: OrionConfiguration,
        errors: list[str],
        warnings: list[str],
    ) -> None:
        risk = configuration.trading_risk

        if risk.account_equity <= 0:
            errors.append("trading_risk.account_equity must be greater than zero.")

        if risk.risk_per_trade <= 0:
            errors.append("trading_risk.risk_per_trade must be greater than zero.")

        if risk.risk_per_trade > 0.05:
            warnings.append("trading_risk.risk_per_trade is above 5%.")

        if risk.max_position_value is not None and risk.max_position_value <= 0:
            errors.append("trading_risk.max_position_value must be greater than zero when configured.")

    def _validate_planner(
        self,
        configuration: OrionConfiguration,
        errors: list[str],
    ) -> None:
        planner = configuration.planner

        if planner.minimum_reward_risk_ratio <= 0:
            errors.append("planner.minimum_reward_risk_ratio must be greater than zero.")

        if planner.default_stop_loss_pct <= 0:
            errors.append("planner.default_stop_loss_pct must be greater than zero.")

        if planner.default_target_pct <= 0:
            errors.append("planner.default_target_pct must be greater than zero.")

    def _validate_presentation(
        self,
        configuration: OrionConfiguration,
        errors: list[str],
    ) -> None:
        if configuration.presentation.max_explanation_bullets < 0:
            errors.append("presentation.max_explanation_bullets must be zero or greater.")
