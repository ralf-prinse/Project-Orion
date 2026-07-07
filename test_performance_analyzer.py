from __future__ import annotations

from datetime import datetime

from models.trade_journal_entry import TradeJournalEntry
from services.performance_analyzer import PerformanceAnalyzer


def _entry(
    symbol: str,
    realized_profit_loss: float,
    confidence: float,
    invested_amount: float = 100.0,
    regime: str = "BULL",
    volatility: str = "LOW",
) -> TradeJournalEntry:
    return TradeJournalEntry(
        timestamp=datetime.now(),
        symbol=symbol,
        action="OPEN_POSITION",
        decision="BUY",
        confidence=confidence,
        score=confidence * 100,
        entry_price=100.0,
        exit_price=None,
        quantity=1,
        invested_amount=invested_amount,
        realized_profit_loss=realized_profit_loss,
        unrealized_profit_loss=0.0,
        expected_risk=1.0,
        regime=regime,
        volatility=volatility,
        ai_summary="Test explanation",
        recommendation_reason="Test reason",
        cycle_number=1,
        session_id="test-session",
    )


def main():
    analyzer = PerformanceAnalyzer()

    entries = [
        _entry("AAA", realized_profit_loss=10.0, confidence=0.90),
        _entry("BBB", realized_profit_loss=-5.0, confidence=0.70),
        _entry("CCC", realized_profit_loss=15.0, confidence=0.85),
    ]

    result = analyzer.analyze(entries)

    assert result.total_trades == 3
    assert result.winning_trades == 2
    assert result.losing_trades == 1

    assert result.win_rate == 66.67
    assert result.total_realized_profit_loss == 20.0
    assert result.total_unrealized_profit_loss == 0.0

    assert result.average_realized_profit_loss == 6.67
    assert result.average_return_percent == 6.67

    assert result.best_trade_symbol == "CCC"
    assert result.best_trade_return_percent == 15.0

    assert result.worst_trade_symbol == "BBB"
    assert result.worst_trade_return_percent == -5.0

    assert result.average_confidence == 0.8167
    assert result.average_expected_risk == 1.0
    assert result.profitable_confidence_threshold == 0.85

    assert result.dominant_regime == "BULL"
    assert result.dominant_volatility == "LOW"
    assert "Analysed 3 journal entries" in result.summary

    empty = analyzer.analyze([])

    assert empty.total_trades == 0
    assert empty.summary == "No trade journal entries available."

    print("PERFORMANCE ANALYZER: PASS ✅")


if __name__ == "__main__":
    main()