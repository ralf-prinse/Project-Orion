from dataclasses import dataclass


@dataclass(frozen=True)
class PortfolioAnalyticsResult:
    """
    Deterministic portfolio analytics snapshot.

    This model contains calculated portfolio KPIs only.
    It does not mutate portfolio state and contains no presentation logic.
    """

    cash: float
    invested_value: float
    total_value: float
    open_positions: int
    total_exposure: float
    average_position_value: float
    largest_position_symbol: str | None
    largest_position_value: float
    currency: str