from dataclasses import dataclass


@dataclass
class DecisionContext:
    """
    Context die de Decision Layer gebruikt naast het technische signaal.

    Deze context bevat uitsluitend invoerwaarden voor decision analyzers.
    Portfolio-, risk- en position-sizinglogica blijven in gespecialiseerde
    analyzers of toekomstige lagen.
    """

    available_cash: float = 0.0
    portfolio_value: float = 0.0
    open_positions: int = 0
    max_positions: int = 0
    risk_profile: str = "default"

    entry_price: float = 0.0
    stop_loss: float = 0.0
    risk_per_trade: float = 0.01
    max_position_value: float = 0.0
