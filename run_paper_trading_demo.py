from __future__ import annotations

from services.paper_trading_demo_runner import PaperTradingDemoRunner


def main():
    runner = PaperTradingDemoRunner()

    result = runner.run(
        symbol="INGA.AS",
        initial_cash=10000.0,
        quantity=1,
    )

    session = result.run.session

    print("\n=========================================")
    print("ORION PAPER TRADING DEMO")
    print("=========================================\n")

    print(f"Initial cash:     €{result.initial_cash:.2f}")
    print(f"Final cash:       €{result.final_cash:.2f}")
    print(f"Final equity:     €{result.final_equity:.2f}")
    print(f"Profit:           €{result.profit:.2f}")
    print(f"Return:           {result.return_percent:.2f}%")
    print("")
    print(f"Total cycles:     {result.total_cycles}")
    print(f"Opened positions: {result.opened_positions}")
    print(f"Closed positions: {result.closed_positions}")

    print("\nOpen positions:")

    if not session.portfolio.positions:
        print("- None")
    else:
        for symbol, position in session.portfolio.positions.items():
            print(
                f"- {symbol}: "
                f"quantity={position.quantity}, "
                f"entry={position.entry_price:.2f}, "
                f"current={position.current_price:.2f}, "
                f"value={position.market_value:.2f}"
            )

    print("\nCycle actions:")

    for index, cycle in enumerate(result.run.cycles, start=1):
        print(
            f"{index}. {cycle.symbol} | "
            f"{cycle.action} | "
            f"{cycle.message}"
        )

    print("\n=========================================")
    print("DEMO COMPLETE")
    print("=========================================\n")


if __name__ == "__main__":
    main()