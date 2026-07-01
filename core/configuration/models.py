from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ScanProfileConfig:
    """
    Deterministic scan-level configuration.

    This model controls orchestration defaults only. It does not download data,
    filter symbols, analyse securities or make trading decisions.
    """

    max_opportunities: int = 3
    continue_on_error: bool = True


@dataclass(frozen=True)
class TradingRiskProfileConfig:
    """
    Trading-risk preferences used by downstream deterministic services.

    The configuration expresses user preferences. It must never override Risk
    Manager blockers or create investment decisions by itself.
    """

    account_equity: float = 10_000.0
    risk_per_trade: float = 0.01
    max_position_value: float | None = None


@dataclass(frozen=True)
class PlannerProfileConfig:
    """
    Trade Planner preferences.
    """

    minimum_reward_risk_ratio: float = 2.0
    default_stop_loss_pct: float = 0.08
    default_target_pct: float = 0.16


@dataclass(frozen=True)
class PresentationProfileConfig:
    """
    Presentation and explanation preferences.

    These values affect display and summaries only. They do not alter trading
    logic, signal generation or deterministic decisions.
    """

    include_ai_explanation: bool = True
    max_explanation_bullets: int = 5


@dataclass(frozen=True)
class OrionConfiguration:
    """
    Central user-facing configuration profile for Project Orion.

    The profile groups configuration that was previously likely to be passed as
    scattered primitive values. It is intentionally conservative: domain engines
    remain responsible for their own calculations and validation.
    """

    profile_name: str = "balanced_swing"
    description: str = "Balanced deterministic swing-trading profile."
    scan: ScanProfileConfig = field(default_factory=ScanProfileConfig)
    trading_risk: TradingRiskProfileConfig = field(default_factory=TradingRiskProfileConfig)
    planner: PlannerProfileConfig = field(default_factory=PlannerProfileConfig)
    presentation: PresentationProfileConfig = field(default_factory=PresentationProfileConfig)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OrionConfiguration":
        if data is None:
            return cls()

        return cls(
            profile_name=str(data.get("profile_name", "balanced_swing")),
            description=str(
                data.get("description", "Balanced deterministic swing-trading profile.")
            ),
            scan=ScanProfileConfig(**dict(data.get("scan", {}))),
            trading_risk=TradingRiskProfileConfig(**dict(data.get("trading_risk", {}))),
            planner=PlannerProfileConfig(**dict(data.get("planner", {}))),
            presentation=PresentationProfileConfig(**dict(data.get("presentation", {}))),
            metadata=dict(data.get("metadata", {})),
        )
