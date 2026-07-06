from services.decision.decision_models import DecisionInput


class PositionSizer:
    """
    Calculates deterministic position size from portfolio context and signal strength.

    This service performs sizing only.
    It does not make BUY / SELL / HOLD decisions.
    """

    def calculate_position_size(self, data: DecisionInput) -> float:
        signal = data.signal
        context = data.context

        cash = max(0.0, float(context.cash))

        if cash <= 0:
            return 0.0

        max_position_percentage = max(
            0.0,
            min(float(context.max_position_percentage), 1.0),
        )

        max_position_value = cash * max_position_percentage

        confidence_factor = max(
            0.10,
            min(float(signal.score), 1.0),
        )

        volatility_factor = 1.0 - max(
            0.0,
            min(float(signal.volatility), 0.80),
        )

        position_size = max_position_value * confidence_factor * volatility_factor

        return round(
            max(
                0.0,
                min(position_size, max_position_value),
            ),
            2,
        )