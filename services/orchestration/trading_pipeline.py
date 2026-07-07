from __future__ import annotations

from models.trading_pipeline_result import TradingPipelineResult
from services.logging_service import LoggingService
from services.risk.risk_context_builder import RiskContextBuilder
from services.intelligence.signal_fusion_engine import SignalFusionEngine
from services.intelligence.intelligence_models import IndicatorPack
from services.intelligence.market_intelligence_engine import (
    MarketIntelligenceEngine,
)
from services.intelligence.ai_context_builder import AIContextBuilder
from services.intelligence.ai_explainer import AIExplainer
from services.risk.risk_plan_validator import RiskPlanValidator
from services.decision.adaptive_decision_engine import AdaptiveDecisionEngine
from services.decision.position_sizing import PositionSizer
from services.decision.decision_models import (
    MarketSignal,
    PositionContext,
    DecisionInput,
)
from services.risk.adaptive_risk_engine import AdaptiveRiskEngine


class TradingPipeline:
    """
    ORION FULL AI TRADING PIPELINE

    Input
    -----
    IndicatorPack + portfolio_state

    Output
    ------
    TradingPipelineResult
    """

    def __init__(self):
        self.logger = LoggingService.get_logger("TradingPipeline")

        self.fusion = SignalFusionEngine()
        self.intelligence = MarketIntelligenceEngine()
        self.decision_engine = AdaptiveDecisionEngine()
        self.sizer = PositionSizer()
        self.risk_engine = AdaptiveRiskEngine()
        self.risk_validator = RiskPlanValidator()
        self.risk_context_builder = RiskContextBuilder()
        self.ai_builder = AIContextBuilder()
        self.explainer = AIExplainer()

    def run(
        self,
        indicator_data: IndicatorPack,
        portfolio_state,
    ) -> TradingPipelineResult:
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
            max_position_percentage=getattr(
                portfolio_state,
                "max_position_percentage",
                1.0,
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

        risk_context = self.risk_context_builder.build(
            indicator_pack=indicator_data,
            intelligence=intelligence,
            confidence=decision.confidence,
        )

        risk_plan = self.risk_engine.build(
            risk_context
        )

        validation = self.risk_validator.validate(
            risk_plan
        )

        if not validation.is_valid:
            raise ValueError(
                "AdaptiveRiskEngine produced an invalid RiskPlan:\n"
                + "\n".join(validation.errors)
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
            "risk_plan": {
                "symbol": risk_plan.symbol,
                "entry_price": risk_plan.entry_price,
                "stop_loss": risk_plan.stop_loss,
                "target_1": risk_plan.target_1,
                "target_2": risk_plan.target_2,
                "target_3": risk_plan.target_3,
                "risk_percent": risk_plan.risk_percent,
                "reward_percent": risk_plan.reward_percent,
                "risk_reward_ratio": risk_plan.risk_reward_ratio,
                "confidence": risk_plan.confidence,
                "notes": risk_plan.notes,
            },
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

        return TradingPipelineResult(
            symbol=indicator_data.symbol,
            decision=decision.decision,
            confidence=decision.confidence,
            position_size=position_size,
            expected_risk=expected_risk,
            risk_plan=risk_plan,
            market_intelligence=intelligence,
            ai_context=ai_context,
            explanation=explanation,
            pipeline_output=output,
        )