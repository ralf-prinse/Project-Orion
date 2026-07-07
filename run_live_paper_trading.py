from __future__ import annotations

from services.live_paper_market_scanner import LivePaperMarketScanner
from models.live_paper_trading_config import LivePaperTradingConfig


def main():
    config = LivePaperTradingConfig(
        initial_cash=500.0,
        max_symbols=25,
        max_open_positions=3,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    scanner = LivePaperMarketScanner(
        config=config,
    )

    result = scanner.run()

    session = result.session

    print("\n=========================================")
    print("ORION LIVE PAPER TRADING")
    print("=========================================\n")

    print(f"Initial cash:       €{config.initial_cash:.2f}")
    print(f"Final cash:         €{session.cash:.2f}")
    print(f"Final equity:       €{session.equity:.2f}")
    print(f"Open positions:     {session.open_positions}")
    print("")
    print(f"Scanned symbols:    {result.scanned_symbols}")
    print(f"Failed symbols:     {result.failed_symbols}")
    print(f"Executed trades:    {result.executed_trades}")
    print(f"Rejected trades:    {result.rejected_trades}")

    print("\nTop candidates:")

    for candidate in result.ranked_candidates[:10]:
        print(
            f"- {candidate.symbol:<10} "
            f"decision={candidate.result.decision:<5} "
            f"confidence={candidate.result.confidence:.3f} "
            f"score={candidate.score:.3f} "
            f"accepted={candidate.accepted} "
            f"reason={candidate.reason}"
        )

    print("\nOpen portfolio:")

    if not session.portfolio.positions:
        print("- None")
    else:
        for symbol, position in session.portfolio.positions.items():
            print(
                f"- {symbol:<10} "
                f"quantity={position.quantity} "
                f"entry=€{position.entry_price:.2f} "
                f"current=€{position.current_price:.2f} "
                f"value=€{position.market_value:.2f} "
                f"p/l=€{position.unrealized_profit_loss:.2f}"
            )

    print("\n=========================================")
    print("LIVE PAPER RUN COMPLETE")
    print("=========================================\n")


if __name__ == "__main__":
    main()