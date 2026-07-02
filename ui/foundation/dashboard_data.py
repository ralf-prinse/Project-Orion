from dataclasses import dataclass

from services.performance.models import PerformanceResult
from services.portfolio.models import PortfolioResult, PortfolioState


@dataclass(frozen=True)
class DashboardData:
    """
    Aggregated deterministic data for Dashboard 2.0.

    This model is presentation-facing only.
    It does not calculate trading decisions, signals,
    risk outcomes, portfolio validation or AI output.
    """

    portfolio_state: PortfolioState | None = None
    portfolio_result: PortfolioResult | None = None
    performance_result: PerformanceResult | None = None
    scanner_result: object | None = None