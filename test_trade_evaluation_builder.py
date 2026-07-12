from models.strategy.trade_evaluation_snapshot import TradeEvaluationSnapshot
from services.strategy.trade_evaluation_builder import TradeEvaluationBuilder


def test_build_snapshot():

    builder = TradeEvaluationBuilder()

    snapshot = builder.build(
        symbol="NVDA",
        phase="ENTRY",
        conviction=87.5,
        opportunity_score=91.2,
        thesis="High Momentum Breakout",
        market_regime="BULL",
        trend_score=0.92,
        momentum_score=0.95,
        volume_score=0.81,
        volatility_score=0.73,
        risk_reward=3.2,
        strengths=[
            "Momentum",
            "Trend",
            "Volume",
        ],
        weaknesses=[
            "Extended RSI",
        ],
        notes="Shadow mode",
    )

    assert isinstance(snapshot, TradeEvaluationSnapshot)

    assert snapshot.symbol == "NVDA"

    assert snapshot.phase == "ENTRY"

    assert snapshot.conviction == 87.5

    assert snapshot.opportunity_score == 91.2

    assert snapshot.thesis == "High Momentum Breakout"

    assert snapshot.market_regime == "BULL"

    assert snapshot.trend_score == 0.92

    assert snapshot.momentum_score == 0.95

    assert snapshot.volume_score == 0.81

    assert snapshot.volatility_score == 0.73

    assert snapshot.risk_reward == 3.2

    assert len(snapshot.strengths) == 3

    assert len(snapshot.weaknesses) == 1

    assert snapshot.notes == "Shadow mode"