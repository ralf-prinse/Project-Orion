from models.investment_thesis import InvestmentThesis, ThesisFactor
from models.risk_plan import RiskPlan
from models.trading_pipeline_result import TradingPipelineResult
from services.intelligence.opportunity_ranking_engine import OpportunityRankingEngine


def _result(symbol: str, decision: str, confidence: float, momentum: float):
    factors = (
        ThesisFactor("trend", 0.8, 0.22, 0.176, "trend"),
        ThesisFactor("momentum", momentum, 0.18, momentum * 0.18, "momentum"),
        ThesisFactor("pressure_confirmation", 0.8, 0.15, 0.12, "pressure"),
        ThesisFactor("market_regime", 1.0, 0.15, 0.15, "regime"),
        ThesisFactor("rsi_context", 0.8, 0.10, 0.08, "rsi"),
        ThesisFactor("volatility_quality", 1.0, 0.08, 0.08, "volatility"),
        ThesisFactor("risk_reward", 1.0, 0.12, 0.12, "rr"),
    )
    thesis = InvestmentThesis(symbol, "BUY", 80, 0.8, factors, (), (), (), "test")
    risk = RiskPlan(symbol, 100, 97, 103, 106, 109, 3, 9, 3, confidence, "test")
    return TradingPipelineResult(symbol, decision, confidence, 100, 3, risk, None, None, None, thesis)


def main():
    engine = OpportunityRankingEngine()
    strong = engine.rank(_result("AAA", "BUY", 0.9, 0.9))
    weak = engine.rank(_result("BBB", "HOLD", 0.6, 0.3))
    assert strong.score > weak.score
    assert strong.rank_band in {"TOP", "STRONG"}
    assert len(strong.factors) == 7
    assert strong.symbol == "AAA"
    print("OPPORTUNITY RANKING ENGINE: PASS ✅")


if __name__ == "__main__":
    main()
