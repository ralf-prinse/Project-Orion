from services.intelligence.signal_fusion_engine import SignalFusionEngine
from services.intelligence.intelligence_models import IndicatorPack
from services.intelligence.market_intelligence_engine import MarketIntelligenceEngine
from services.intelligence.ai_context_builder import AIContextBuilder
from services.intelligence.ai_explainer import AIExplainer

from services.decision.adaptive_decision_engine import AdaptiveDecisionEngine
from services.decision.position_sizing import PositionSizer
from services.decision.decision_models import (
    MarketSignal,
    PositionContext,
    DecisionInput,
)


class TradingPipeline:
    """
    ORION FULL AI TRADING PIPELINE

    Clean architecture flow:

    IndicatorPack
        ↓
    SignalFusionEngine
        ↓
    MarketIntelligenceEngine
        ↓
    MarketSignal
        ↓
    AdaptiveDecisionEngine
        ↓
    DecisionInput
        ↓
    PositionSizer
        ↓
    AIContextBuilder
        ↓
    AIExplainer
        ↓
    Output
    """

    def __init__(self):
        self.fusion = SignalFusionEngine()
        self.intelligence = MarketIntelligenceEngine()
        self.decision_engine = AdaptiveDecisionEngine()
        self.sizer = PositionSizer()
        self.ai_builder = AIContextBuilder()
        self.explainer = AIExplainer()

    def run(self, indicator_data: IndicatorPack, portfolio_state):
        fused = self.fusion.build(indicator_data)
        intelligence = self.intelligence.analyze(indicator_data)

        signal = MarketSignal(
            symbol=indicator_data.symbol,
            score=fused.pressure_score,
            trend=fused.trend,
            volatility=fused.volatility,
            momentum=fused.momentum,
        )

        decision = self.decision_engine.evaluate(signal)

        context = PositionContext(
            cash=portfolio_state.cash,
            position_size=getattr(portfolio_state, "position_size", 0.0),
            exposure=getattr(portfolio_state, "exposure", 0.0),
        )

        decision_input = DecisionInput(
            signal=signal,
            context=context,
        )

        position_size = self.sizer.calculate_position_size(decision_input)
        expected_risk = round(position_size * intelligence.risk_score, 6)

        output = {
            "symbol": indicator_data.symbol,

            "pressure_score": fused.pressure_score,
            "buy_pressure": fused.buy_pressure,
            "sell_pressure": fused.sell_pressure,
            "strength": fused.strength,

            "regime": intelligence.regime,
            "volatility": intelligence.volatility_state,
            "risk_score": intelligence.risk_score,

            "decision": decision.decision,
            "confidence": decision.confidence,
            "reason": decision.reason,

            "position_size": position_size,
            "expected_risk": expected_risk,

            "features": {
                "pressure_score": fused.pressure_score,
                "buy_pressure": fused.buy_pressure,
                "sell_pressure": fused.sell_pressure,
                "strength": fused.strength,
                "trend": fused.trend,
                "momentum": fused.momentum,
                "rsi": fused.rsi,
                "volatility": fused.volatility,
            },
        }

        ai_context = self.ai_builder.build(output)
        explanation = self.explainer.explain(ai_context)

        return {
            "pipeline": output,
            "ai_context": ai_context,
            "explanation": explanation,
        }