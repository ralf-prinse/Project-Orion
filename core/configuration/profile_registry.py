from core.configuration.models import (
    OrionConfiguration,
    PlannerProfileConfig,
    PresentationProfileConfig,
    ScanProfileConfig,
    TradingRiskProfileConfig,
)
from core.configuration.validation import ConfigurationValidator


class ConfigurationProfileRegistry:
    """
    Registry for deterministic Orion configuration profiles.

    Profiles centralise user preferences without moving business logic into the
    configuration layer. Engines and services may consume values from a profile,
    but they remain responsible for domain calculations and risk validation.
    """

    def __init__(self, profiles: list[OrionConfiguration] | None = None):
        self._profiles: dict[str, OrionConfiguration] = {}
        self._validator = ConfigurationValidator()

        initial_profiles = profiles if profiles is not None else self._default_profiles()
        for profile in initial_profiles:
            self.register(profile)

    def register(self, configuration: OrionConfiguration) -> None:
        validation = self._validator.validate(configuration)
        if not validation.is_valid:
            raise ValueError("Invalid configuration profile: " + "; ".join(validation.errors))

        self._profiles[configuration.profile_name] = configuration

    def get(self, profile_name: str) -> OrionConfiguration:
        try:
            return self._profiles[profile_name]
        except KeyError as exc:
            raise KeyError(f"Unknown configuration profile: {profile_name}") from exc

    def list_profiles(self) -> list[str]:
        return sorted(self._profiles.keys())

    def default(self) -> OrionConfiguration:
        return self.get("balanced_swing")

    def _default_profiles(self) -> list[OrionConfiguration]:
        return [
            OrionConfiguration(
                profile_name="conservative_swing",
                description="Conservative swing profile with lower risk per trade.",
                scan=ScanProfileConfig(max_opportunities=3, continue_on_error=True),
                trading_risk=TradingRiskProfileConfig(
                    account_equity=10_000.0,
                    risk_per_trade=0.005,
                    max_position_value=1_000.0,
                ),
                planner=PlannerProfileConfig(
                    minimum_reward_risk_ratio=2.5,
                    default_stop_loss_pct=0.06,
                    default_target_pct=0.15,
                ),
                presentation=PresentationProfileConfig(
                    include_ai_explanation=True,
                    max_explanation_bullets=4,
                ),
            ),
            OrionConfiguration(),
            OrionConfiguration(
                profile_name="aggressive_swing",
                description="Aggressive swing profile with higher risk tolerance.",
                scan=ScanProfileConfig(max_opportunities=5, continue_on_error=True),
                trading_risk=TradingRiskProfileConfig(
                    account_equity=10_000.0,
                    risk_per_trade=0.02,
                    max_position_value=2_500.0,
                ),
                planner=PlannerProfileConfig(
                    minimum_reward_risk_ratio=1.75,
                    default_stop_loss_pct=0.1,
                    default_target_pct=0.18,
                ),
                presentation=PresentationProfileConfig(
                    include_ai_explanation=True,
                    max_explanation_bullets=6,
                ),
            ),
        ]
