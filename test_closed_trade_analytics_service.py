from datetime import datetime

from models.trade_journal_entry import TradeJournalEntry
from services.closed_trade_analytics_service import ClosedTradeAnalyticsService


def build_closed_trade(
    symbol: str,
    realized_profit_loss: float,
) -> TradeJournalEntry:
    return TradeJournalEntry(
        timestamp=datetime(2026, 7, 9, 12, 0, 0),
        symbol=symbol,
        action="CLOSE_POSITION",
        decision="TAKE_PROFIT" if realized_profit_loss > 0 else "STOP_LOSS",
        confidence=1.0,
        score=0.0,
        entry_price=100.0,
        exit_price=100.0 + realized_profit_loss,
        quantity=1,
        invested_amount=100.0,
        realized_profit_loss=realized_profit_loss,
        unrealized_profit_loss=0.0,
        expected_risk=0.0,
        regime="UNKNOWN",
        volatility="UNKNOWN",
        ai_summary="Closed trade analytics test.",
        recommendation_reason="Regression test.",
        cycle_number=1,
        session_id="test-session",
    )


def test_closed_trade_analytics_service_handles_empty_input():
    service = ClosedTradeAnalyticsService()

    result = service.analyze([])

    assert result.closed_trades == 0
    assert result.winning_trades == 0
    assert result.losing_trades == 0
    assert result.winrate_percent == 0.0
    assert result.closed_profit_loss == 0.0
    assert result.average_winner == 0.0
    assert result.average_loser == 0.0
    assert result.profit_factor == 0.0
    assert result.largest_winner == 0.0
    assert result.largest_loser == 0.0


def test_closed_trade_analytics_service_calculates_statistics():
    service = ClosedTradeAnalyticsService()

    entries = [
        build_closed_trade("AAA", 10.0),
        build_closed_trade("BBB", -5.0),
        build_closed_trade("CCC", 20.0),
    ]

    result = service.analyze(entries)

    assert result.closed_trades == 3
    assert result.winning_trades == 2
    assert result.losing_trades == 1
    assert result.winrate_percent == 66.67
    assert result.closed_profit_loss == 25.0
    assert result.average_winner == 15.0
    assert result.average_loser == -5.0
    assert result.profit_factor == 6.0
    assert result.largest_winner == 20.0
    assert result.largest_loser == -5.0


def main():
    print("\n=========================================")
    print("ORION CLOSED TRADE ANALYTICS SERVICE TEST")
    print("=========================================\n")

    test_closed_trade_analytics_service_handles_empty_input()
    test_closed_trade_analytics_service_calculates_statistics()

    print("CLOSED TRADE ANALYTICS SERVICE: PASS ✅")


if __name__ == "__main__":
    main()