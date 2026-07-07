from __future__ import annotations

from models.autonomous_paper_trading_config import (
    AutonomousPaperTradingConfig,
)
from models.live_paper_trading_config import LivePaperTradingConfig
from services.autonomous_paper_trading_runner import (
    AutonomousPaperTradingRunner,
)


def main():
    live_config = LivePaperTradingConfig(
        initial_cash=500.0,
        max_symbols=25,
        max_open_positions=3,
        min_confidence=0.75,
        max_position_value=150.0,
    )

    config = AutonomousPaperTradingConfig(
        live_config=live_config,
        cycles=3,
        sleep_seconds=0.0,
        stop_on_exception=False,
        print_cycle_summary=True,
    )

    runner = AutonomousPaperTradingRunner(
        config=config,
    )

    result = runner.run()

    session = result.session

    print("\n=========================================")
    print("ORION AUTONOMOUS PAPER TRADING")
    print("=========================================\n")

    print(f"Initial cash:       €{result.initial_cash:.2f}")
    print(f"Final cash:         €{result.final_cash:.2f}")
    print(f"Final equity:       €{result.final_equity:.2f}")
    print(f"Profit:             €{result.profit:.2f}")
    print(f"Return:             {result.return_percent:.2f}%")
    print("")
    print(f"Completed cycles:   {result.completed_cycles}")
    print(f"Failed cycles:      {result.failed_cycles}")
    print(f"Executed trades:    {result.total_executed_trades}")
    print(f"Rejected trades:    {result.total_rejected_trades}")
    print(f"Failed symbols:     {result.total_failed_symbols}")
    print(f"Open positions:     {session.open_positions}")

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

    print("\nCycle allocation summary:")

    for index, cycle in enumerate(result.cycle_results, start=1):
        print(
            f"- Cycle {index}: "
            f"approved={cycle.allocation.approved_count}, "
            f"rejected={cycle.allocation.rejected_count}, "
            f"executed={cycle.executed_trades}"
        )

    print("\n=========================================")
    print("AUTONOMOUS PAPER RUN COMPLETE")
    print("=========================================\n")


if __name__ == "__main__":
    main()