from __future__ import annotations

from pathlib import Path

from services.net_expectancy_service import NetExpectancyService
from services.stores.jsonl_completed_trade_repository import (
    JsonlCompletedTradeRepository,
)


COMPLETED_TRADES_PATH = Path("data/ibkr_completed_trades.jsonl")


def _print_result(label, result) -> None:
    readiness = "SUFFICIENT" if result.sufficient_sample else "INSUFFICIENT"
    print(
        f"{label:<24} n={result.sample_size:<4} "
        f"win={result.win_rate:>6.1%} "
        f"expectancy=EUR {result.net_expectancy_per_trade:>7.2f} "
        f"net=EUR {result.total_net_profit_loss:>8.2f} "
        f"sample={readiness}"
    )


def main() -> None:
    records = JsonlCompletedTradeRepository(COMPLETED_TRADES_PATH).load_all()
    service = NetExpectancyService()
    print("ORION OFFLINE NET EXPECTANCY (never changes trading parameters)")
    print(f"Source: {COMPLETED_TRADES_PATH}")
    _print_result("ALL", service.analyze(records))
    for field in ("strategy_name", "entry_regime", "entry_volatility", "symbol"):
        print(f"\nBY {field.upper()}")
        for key, result in service.analyze_grouped(
            records,
            field_name=field,
        ).items():
            _print_result(key, result)


if __name__ == "__main__":
    main()
