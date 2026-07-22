from types import SimpleNamespace

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner


class FixedRankingEngine:
    def __init__(self, score: float = 80.0) -> None:
        self.score = score

    def rank(self, result):
        return SimpleNamespace(score=self.score)


def test_selectivity_gate_rejects_legacy_buy_with_weak_trend() -> None:
    scanner = _scanner()
    result = _result(trend=0.20)

    candidate = scanner._build_candidate("TEST", result)

    assert candidate.accepted is False
    assert "trend factor 0.20 is below 0.40" in candidate.reason


def test_selectivity_gate_rejects_watch_thesis_despite_legacy_buy() -> None:
    scanner = _scanner()
    result = _result(stance="WATCH")

    candidate = scanner._build_candidate("TEST", result)

    assert candidate.accepted is False
    assert "thesis stance is WATCH, not BUY" in candidate.reason


def test_selectivity_gate_accepts_independently_confirmed_buy() -> None:
    scanner = _scanner()

    candidate = scanner._build_candidate("TEST", _result())

    assert candidate.accepted is True
    assert candidate.reason == "Accepted candidate."


def _scanner() -> LivePaperMarketScanner:
    return LivePaperMarketScanner(
        config=LivePaperTradingConfig(
            min_confidence=0.75,
            min_opportunity_score=70.0,
            min_thesis_conviction=68.0,
            min_trend_factor=0.40,
            min_momentum_factor=0.50,
            min_pressure_confirmation_factor=0.55,
            max_position_value=500.0,
        ),
        ranking_engine=FixedRankingEngine(),
    )


def _result(*, stance="BUY", trend=0.70):
    factors = tuple(
        SimpleNamespace(name=name, score=score)
        for name, score in {
            "trend": trend,
            "momentum": 0.70,
            "pressure_confirmation": 0.75,
        }.items()
    )
    thesis = SimpleNamespace(
        stance=stance,
        conviction=80.0,
        factors=factors,
    )
    risk_plan = SimpleNamespace(entry_price=100.0)
    return SimpleNamespace(
        decision="BUY",
        confidence=0.90,
        risk_plan=risk_plan,
        investment_thesis=thesis,
    )
