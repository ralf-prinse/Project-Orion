from __future__ import annotations

from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult


def main():
    risk_plan = RiskPlan(
        symbol="INGA.AS",
        entry_price=25.00,
        stop_loss=24.00,
        target_1=26.00,
        target_2=27.00,
        target_3=28.00,
        risk_percent=4.0,
        reward_percent=12.0,
        risk_reward_ratio=3.0,
        confidence=0.82,
        notes="Adaptive risk plan",
    )

    pipeline_output = {
        "symbol": "INGA.AS",
        "decision": "BUY",
        "confidence": 0.82,
    }

    result = TradingPipelineResult(
        symbol="INGA.AS",
        decision="BUY",
        confidence=0.82,
        position_size=100,
        expected_risk=250.0,
        risk_plan=risk_plan,
        market_intelligence=None,
        ai_context="Bullish context",
        explanation="Trend and momentum aligned.",
        pipeline_output=pipeline_output,
    )

    assert result.symbol == "INGA.AS"
    assert result.decision == "BUY"
    assert result.confidence == 0.82
    assert result.position_size == 100
    assert result.expected_risk == 250.0
    assert result.risk_plan is risk_plan

    assert result.legacy_output is pipeline_output
    assert result.legacy_output["decision"] == "BUY"

    exported = result.to_dict()

    assert exported["pipeline"] is pipeline_output
    assert exported["ai_context"] == "Bullish context"
    assert exported["explanation"] == "Trend and momentum aligned."

    assert result["pipeline"] is pipeline_output
    assert "pipeline" in result
    assert list(result.keys()) == ["pipeline", "ai_context", "explanation"]

    print("TRADING PIPELINE RESULT: PASS ✅")


if __name__ == "__main__":
    main()