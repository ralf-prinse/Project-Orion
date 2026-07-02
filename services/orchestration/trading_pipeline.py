from services.logging_service import LoggingService

from services.intelligence.signal_fusion_engine import SignalFusionEngine
from services.intelligence.intelligence_models import IndicatorPack
from services.intelligence.market_intelligence_engine import (
    MarketIntelligenceEngine,
)
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

    Flow

    IndicatorPack
            ↓
    Signal Fusion
            ↓
    Market Intelligence
            ↓
    Adaptive Decision
            ↓
    Position Sizing
            ↓
    AI Context
            ↓
    AI Explanation
            ↓
    Pipeline Result
    """

    def __init__(self):

        self.logger = LoggingService.get_logger("TradingPipeline")

        self.fusion = SignalFusionEngine()

        self.intelligence = MarketIntelligenceEngine()

        self.decision_engine = AdaptiveDecisionEngine()

        self.sizer = PositionSizer()

        self.ai_builder = AIContextBuilder()

        self.explainer = AIExplainer()

    def run(
        self,
        indicator_data: IndicatorPack,
        portfolio_state,
    ):

        self.logger.info(
            "Starting pipeline for %s",
            indicator_data.symbol,
        )

        fused = self.fusion.build(indicator_data)

        self.logger.info(
            "Signal Fusion completed | pressure=%.3f",
            fused.pressure_score,
        )

        intelligence = self.intelligence.analyze(
            indicator_data
        )

        self.logger.info(
            "Market Intelligence | regime=%s volatility=%s risk=%.4f",
            intelligence.regime,
            intelligence.volatility_state,
            intelligence.risk_score,
        )

        signal = MarketSignal(
            symbol=indicator_data.symbol,
            score=fused.pressure_score,
            trend=fused.trend,
            volatility=fused.volatility,
            momentum=fused.momentum,
        )

        decision = self.decision_engine.evaluate(signal)

        self.logger.info(
            "Decision | %s confidence=%.3f",
            decision.decision,
            decision.confidence,
        )

        context = PositionContext(
            cash=portfolio_state.cash,
            position_size=getattr(
                portfolio_state,
                "position_size",
                0.0,
            ),
            exposure=getattr(
                portfolio_state,
                "exposure",
                0.0,
            ),
        )

        decision_input = DecisionInput(
            signal=signal,
            context=context,
        )

        position_size = self.sizer.calculate_position_size(
            decision_input
        )

        expected_risk = round(
            position_size * intelligence.risk_score,
            6,
        )

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

        explanation = self.explainer.explain(
            ai_context
        )

        self.logger.info(
            "Pipeline completed for %s | %s | confidence=%.3f | position=%.2f",
            indicator_data.symbol,
            decision.decision,
            decision.confidence,
            position_size,
        )

        return {
            "pipeline": output,
            "ai_context": ai_context,
            "explanation": explanation,
        }