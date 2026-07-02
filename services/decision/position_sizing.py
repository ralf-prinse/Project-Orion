from services.decision.decision_models import DecisionInput


class PositionSizer:
    """
    Calculates position size based on normalized signal strength,
    available cash and volatility.

    This service performs sizing only.
    It does not make BUY / SELL / HOLD decisions.
    """

    def calculate_position_size(self, data: DecisionInput) -> float:
        signal = data.signal
        context = data.context

        if context.cash <= 0:
            return 0.0

        base_position = context.cash * 0.10

        confidence_factor = max(0.10, min(signal.score, 1.0))

        volatility_factor = 1.0 - max(0.0, min(signal.volatility, 0.80))

        position_size = base_position * confidence_factor * volatility_factor

        max_position = context.cash * 0.25

        return round(max(0.0, min(position_size, max_position)), 2)