from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from time import perf_counter

from models.portfolio import Portfolio
from services.intelligence.indicator_builder import IndicatorBuilder
from services.market_data.yahoo_historical_provider import YahooHistoricalDataProvider
from services.orchestration.trading_pipeline import TradingPipeline
from services.watchlist_service import WatchlistService


@dataclass(frozen=True)
class MarketPipelineScanResult:
    symbol: str
    decision: str
    confidence: float
    position_size: float
    expected_risk: float
    price: float
    reason: str
    pipeline_result: dict


@dataclass(frozen=True)
class MarketPipelineScannerSnapshot:
    timestamp: datetime
    symbols: tuple[str, ...]
    results: tuple[MarketPipelineScanResult, ...]
    errors: tuple[str, ...] = field(default_factory=tuple)
    duration_seconds: float = 0.0

    @property
    def total_symbols(self) -> int:
        return len(self.symbols)

    @property
    def total_results(self) -> int:
        return len(self.results)

    @property
    def buy_results(self) -> tuple[MarketPipelineScanResult, ...]:
        return tuple(
            result
            for result in self.results
            if result.decision == "BUY"
        )

    @property
    def top_buy_results(self) -> tuple[MarketPipelineScanResult, ...]:
        return tuple(
            sorted(
                self.buy_results,
                key=lambda result: result.confidence,
                reverse=True,
            )
        )

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)


class MarketPipelineScannerService:
    """
    Scans the watchlist through the TradingPipeline.

    Responsibilities
    ----------------
    - load symbols from WatchlistService
    - fetch historical candles
    - build IndicatorPack per symbol
    - run TradingPipeline per symbol
    - collect BUY/HOLD/SELL pipeline results

    This service is backend orchestration only.
    It does not render UI.
    It does not execute trades.
    It does not create duplicate BUY/HOLD/SELL logic.
    """

    def __init__(
        self,
        watchlist_service: WatchlistService | None = None,
        historical_provider: YahooHistoricalDataProvider | None = None,
        indicator_builder: IndicatorBuilder | None = None,
        trading_pipeline: TradingPipeline | None = None,
        period: str = "6mo",
        interval: str = "1d",
    ) -> None:
        self.watchlist_service = watchlist_service or WatchlistService()
        self.historical_provider = historical_provider or YahooHistoricalDataProvider()
        self.indicator_builder = indicator_builder or IndicatorBuilder()
        self.trading_pipeline = trading_pipeline or TradingPipeline()
        self.period = period
        self.interval = interval

    def scan(
        self,
        portfolio_state: Portfolio,
    ) -> MarketPipelineScannerSnapshot:
        started_at = perf_counter()
        timestamp = datetime.now()

        symbols: list[str] = []
        results: list[MarketPipelineScanResult] = []
        errors: list[str] = []

        try:
            symbols = self.watchlist_service.load_symbols()
        except Exception as error:
            errors.append(f"Watchlist error: {error}")
            return MarketPipelineScannerSnapshot(
                timestamp=timestamp,
                symbols=tuple(),
                results=tuple(),
                errors=tuple(errors),
                duration_seconds=round(perf_counter() - started_at, 3),
            )

        history_by_symbol = self.historical_provider.get_history(
            symbols=symbols,
            period=self.period,
            interval=self.interval,
        )

        for symbol in symbols:
            try:
                history = history_by_symbol.get(symbol)

                if history is None or history.empty:
                    errors.append(f"{symbol}: geen historische data beschikbaar")
                    continue

                indicator_pack = self.indicator_builder.build(
                    symbol=symbol,
                    history=history,
                )

                pipeline_result = self.trading_pipeline.run(
                    indicator_data=indicator_pack,
                    portfolio_state=portfolio_state,
                )

                pipeline_data = pipeline_result.get("pipeline", {})

                latest_price = float(history["Close"].iloc[-1])

                results.append(
                    MarketPipelineScanResult(
                        symbol=symbol,
                        decision=str(
                            pipeline_data.get("decision", "HOLD")
                        ).strip().upper(),
                        confidence=float(
                            pipeline_data.get("confidence", 0.0)
                        ),
                        position_size=float(
                            pipeline_data.get("position_size", 0.0)
                        ),
                        expected_risk=float(
                            pipeline_data.get("expected_risk", 0.0)
                        ),
                        price=latest_price,
                        reason=str(
                            pipeline_data.get("reason", "")
                        ),
                        pipeline_result=pipeline_result,
                    )
                )

            except Exception as error:
                errors.append(f"{symbol}: {error}")

        return MarketPipelineScannerSnapshot(
            timestamp=timestamp,
            symbols=tuple(symbols),
            results=tuple(results),
            errors=tuple(errors),
            duration_seconds=round(perf_counter() - started_at, 3),
        )