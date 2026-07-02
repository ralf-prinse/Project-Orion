from services.intelligence.intelligence_models import IndicatorPack
from services.decision.decision_models import MarketSignal


class IntelligenceAdapter:
    """
    Converts Market Intelligence → DecisionEngine input.
    """

    def to_market_signal(self, intel, symbol: str) -> MarketSignal:

        # intelligence → decision abstraction
        score = intel.composite_score * 100

        return MarketSignal(
            symbol=symbol,
            score=score,
            trend=intel.trend_strength,
            volatility=intel.volatility_state_to_value() if hasattr(intel, "volatility_state_to_value") else 0.5,
            momentum=intel.momentum_strength,
        )