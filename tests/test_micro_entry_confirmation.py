from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pandas as pd

from models.live_paper_trading_config import LivePaperTradingConfig
from services.live_paper_market_scanner import LivePaperMarketScanner
from services.market_session_service import MarketSessionService


class FixedRankingEngine:
    def rank(self, _result):
        return SimpleNamespace(score=90.0)


class CapturingHistoricalProvider:
    def __init__(self, histories):
        self.histories = histories
        self.requested_symbols = []

    def get_history(self, *, symbols, period, interval):
        self.requested_symbols = list(symbols)
        return {
            symbol: self.histories[symbol]
            for symbol in symbols
        }


class FixedAdapter:
    def run(self, symbol, history, portfolio_state):
        return _result(symbol)


def test_micro_scan_fetches_spy_as_non_tradable_benchmark() -> None:
    evaluated_at = datetime(2026, 7, 21, 14, 15, tzinfo=UTC)
    histories = {
        "F": _history(evaluated_at, step=0.12, latest_volume=200_000),
        "SPY": _history(
            evaluated_at,
            base=400.0,
            step=0.01,
            latest_volume=200_000,
        ),
    }
    provider = CapturingHistoricalProvider(histories)
    scanner = LivePaperMarketScanner(
        config=_scanner().config,
        adapter=FixedAdapter(),
        ranking_engine=FixedRankingEngine(),
        watchlist_service=SimpleNamespace(load_symbols=lambda: ["F"]),
        market_session_service=MarketSessionService(),
        historical_provider=provider,
        clock=lambda: evaluated_at,
    )

    result = scanner.run()

    assert provider.requested_symbols == ["F", "SPY"]
    assert result.scanned_symbols == 1
    assert [candidate.symbol for candidate in result.candidates] == ["F"]
    assert result.candidates[0].accepted is True


def test_micro_entry_confirmation_accepts_confirmed_us_candidate() -> None:
    evaluated_at = datetime(2026, 7, 21, 14, 15, tzinfo=UTC)
    scanner = _scanner()

    candidate = scanner._build_candidate(
        "F",
        _result("F"),
        history=_history(evaluated_at, step=0.12, latest_volume=200_000),
        benchmark_history=_history(
            evaluated_at,
            base=400.0,
            step=0.01,
            latest_volume=200_000,
        ),
        evaluated_at=evaluated_at,
    )

    assert candidate.accepted is True
    assert candidate.reason == "Accepted candidate."


def test_micro_entry_confirmation_blocks_european_execution() -> None:
    evaluated_at = datetime(2026, 7, 21, 14, 15, tzinfo=UTC)
    scanner = _scanner()

    candidate = scanner._build_candidate(
        "ASML.AS",
        _result("ASML.AS"),
        history=_history(evaluated_at),
        benchmark_history=_history(evaluated_at, base=400.0),
        evaluated_at=evaluated_at,
    )

    assert candidate.accepted is False
    assert "market XAMS is not enabled for entries" in candidate.reason


def test_micro_entry_confirmation_blocks_us_opening_buffer() -> None:
    evaluated_at = datetime(2026, 7, 21, 13, 37, tzinfo=UTC)
    scanner = _scanner()

    candidate = scanner._build_candidate(
        "F",
        _result("F"),
        history=_history(evaluated_at, current_bars=1),
        benchmark_history=_history(
            evaluated_at,
            base=400.0,
            current_bars=1,
        ),
        evaluated_at=evaluated_at,
    )

    assert candidate.accepted is False
    assert "opening buffer is active" in candidate.reason


def test_micro_entry_confirmation_blocks_weak_relative_volume() -> None:
    evaluated_at = datetime(2026, 7, 21, 14, 15, tzinfo=UTC)
    scanner = _scanner()

    candidate = scanner._build_candidate(
        "F",
        _result("F"),
        history=_history(evaluated_at, step=0.12, latest_volume=50_000),
        benchmark_history=_history(
            evaluated_at,
            base=400.0,
            step=0.01,
        ),
        evaluated_at=evaluated_at,
    )

    assert candidate.accepted is False
    assert "relative volume 0.50 is below 1.00" in candidate.reason


def test_micro_entry_confirmation_fails_closed_without_spy() -> None:
    evaluated_at = datetime(2026, 7, 21, 14, 15, tzinfo=UTC)
    scanner = _scanner()

    candidate = scanner._build_candidate(
        "F",
        _result("F"),
        history=_history(evaluated_at, step=0.12, latest_volume=200_000),
        benchmark_history=None,
        evaluated_at=evaluated_at,
    )

    assert candidate.accepted is False
    assert "SPY relative-strength benchmark is unavailable" in candidate.reason


def _scanner() -> LivePaperMarketScanner:
    return LivePaperMarketScanner(
        config=LivePaperTradingConfig(
            allowed_entry_market_codes=("XUSA",),
            entry_open_buffer_minutes=15,
            entry_close_buffer_minutes=180,
            require_intraday_confirmation=True,
            min_intraday_relative_volume=1.0,
            min_intraday_relative_strength=0.0,
            min_confidence=0.85,
            min_opportunity_score=80.0,
            min_thesis_conviction=75.0,
            min_trend_factor=0.55,
            min_momentum_factor=0.65,
            min_pressure_confirmation_factor=0.65,
        ),
        ranking_engine=FixedRankingEngine(),
        market_session_service=MarketSessionService(),
    )


def _result(symbol: str):
    factors = tuple(
        SimpleNamespace(name=name, score=0.90)
        for name in ("trend", "momentum", "pressure_confirmation")
    )
    return SimpleNamespace(
        decision="BUY",
        confidence=0.95,
        risk_plan=SimpleNamespace(entry_price=100.0),
        investment_thesis=SimpleNamespace(
            stance="BUY",
            conviction=90.0,
            factors=factors,
        ),
    )


def _history(
    evaluated_at: datetime,
    *,
    base: float = 100.0,
    step: float = 0.05,
    latest_volume: float = 100_000,
    current_bars: int = 9,
) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    timestamps: list[datetime] = []
    current_date = evaluated_at.date()

    for day_offset in (4, 3, 2, 1):
        start = datetime.combine(
            current_date - timedelta(days=day_offset),
            datetime.min.time(),
            tzinfo=UTC,
        ) + timedelta(hours=13, minutes=30)
        for index in range(9):
            close = base + (index * step)
            timestamps.append(start + timedelta(minutes=5 * index))
            rows.append(_row(close=close, volume=100_000))

    current_start = datetime.combine(
        current_date,
        datetime.min.time(),
        tzinfo=UTC,
    ) + timedelta(hours=13, minutes=30)
    for index in range(current_bars):
        close = base + (index * step)
        volume = latest_volume if index == current_bars - 1 else 100_000
        timestamps.append(current_start + timedelta(minutes=5 * index))
        rows.append(_row(close=close, volume=volume))

    frame = pd.DataFrame(rows, index=pd.DatetimeIndex(timestamps))
    frame.attrs["interval"] = "5m"
    return frame


def _row(*, close: float, volume: float) -> dict[str, float]:
    return {
        "Open": close - 0.03,
        "High": close + 0.05,
        "Low": close - 0.05,
        "Close": close,
        "Volume": volume,
    }
