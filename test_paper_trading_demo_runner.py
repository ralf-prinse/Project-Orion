from __future__ import annotations

from services.paper_trading_demo_runner import (
    PaperTradingDemoRunner,
)


def main():
    print("\n=========================================")
    print("ORION PAPER TRADING DEMO TEST")
    print("=========================================\n")

    runner = PaperTradingDemoRunner()

    result = runner.run()

    assert result.initial_cash == 10000.0
    assert result.final_cash >= 0.0
    assert result.final_equity >= 0.0

    assert result.total_cycles == 3

    assert result.opened_positions >= 0
    assert result.closed_positions >= 0

    assert result.return_percent == round(
        (result.profit / result.initial_cash) * 100,
        2,
    )

    session = result.run.session

    assert session is not None
    assert session.portfolio is not None

    assert result.final_equity == session.equity
    assert result.final_cash == session.cash

    print("PAPER TRADING DEMO: PASS ✅")


if __name__ == "__main__":
    main()