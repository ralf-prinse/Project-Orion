from dataclasses import dataclass


@dataclass
class DecisionContext:
    """
    Context die de Decision Layer gebruikt naast het technische signaal.

    Sprint 8.3.1:
    Deze velden worden nog beperkt gebruikt, maar leggen alvast de interface
    vast voor Portfolio Engine, Risk Manager en Position Sizing.
    """

    available_cash: float = 0.0
    portfolio_value: float = 0.0
    open_positions: int = 0
    max_positions: int = 0
    risk_profile: str = "default"