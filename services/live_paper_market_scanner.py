from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import (
    LivePaperCandidate,
    LivePaperTradingResult,
)
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from providers.yahoo_provider import YahooProvider
from services.intelligence.opportunity_ranking_engine import (
    OpportunityRankingEngine,
)
from services.paper_trading_pipeline_adapter import (
    PaperTradingPipelineAdapter,
)
from services.watchlist_service import WatchlistService
from services.market_session_service import MarketSessionService
from services.market_data.historical_provider import HistoricalDataProvider


class LivePaperMarketScanner:
    """
    Live paper market scanner.

    Responsibilities
    ----------------
    - Load symbols through WatchlistService
    - Download historical market data
    - Run IndicatorBuilder + TradingPipeline
    - Build ranked candidates

    Does NOT
    --------
    - Allocate portfolio capital
    - Execute trades
    - Mutate TradingSession
    - Place real broker orders
    """

    def __init__(
        self,
        config: LivePaperTradingConfig | None = None,
        provider: YahooProvider | None = None,
        adapter: PaperTradingPipelineAdapter | None = None,
        watchlist_service: WatchlistService | None = None,
        ranking_engine: OpportunityRankingEngine | None = None,
        market_session_service: MarketSessionService | None = None,
        historical_provider: HistoricalDataProvider | None = None,
        clock: Callable[[], datetime] | None = None,
    ):
        self.config = config or LivePaperTradingConfig()
        self.provider = provider or YahooProvider()
        self.adapter = adapter or PaperTradingPipelineAdapter()
        self.ranking_engine = ranking_engine or OpportunityRankingEngine()
        self.watchlist_service = (
            watchlist_service
            or WatchlistService(
                watchlist_path=str(self.config.watchlist_path),
            )
        )
        self.market_session_service = market_session_service
        self.historical_provider = historical_provider
        self.clock = clock or (lambda: datetime.now(UTC))

    def run(
        self,
        session: TradingSession | None = None,
    ) -> LivePaperTradingResult:
        started_at = time.perf_counter()

        symbols = self.watchlist_service.load_symbols()[
            : self.config.max_symbols
        ]

        current_session = session or TradingSession(
            name="Orion Live Paper Trading",
            portfolio=PaperPortfolio(
                cash=self.config.initial_cash,
            ),
        )

        candidates: list[LivePaperCandidate] = []
        failed_symbol_errors: dict[str, str] = {}
        succeeded_symbols = 0

        evaluated_at = self.clock()
        open_symbols: list[str] = []

        for symbol in symbols:
            if (
                self.market_session_service is not None
                and not self.market_session_service.is_symbol_market_open(
                    symbol=symbol,
                    now=evaluated_at,
                )
            ):
                status = self.market_session_service.get_symbol_status(
                    symbol=symbol,
                    now=evaluated_at,
                )
                failed_symbol_errors[symbol] = (
                    f"Market {status.market.code} is closed: "
                    f"{status.reason}"
                )
                continue

            open_symbols.append(symbol)

        prefetched_history = None
        if self.historical_provider is not None and open_symbols:
            prefetched_history = self.historical_provider.get_history(
                symbols=open_symbols,
                period=self.config.history_period,
                interval=self.config.history_interval,
            )

        for symbol in open_symbols:
            try:
                if prefetched_history is not None:
                    history = prefetched_history.get(symbol)
                    if history is None or history.empty:
                        raise ValueError(
                            "No batched historical market data returned "
                            f"for {symbol}."
                        )
                else:
                    history = self.provider.get_historical_data(
                        symbol=symbol,
                        period=self.config.history_period,
                        interval=self.config.history_interval,
                    )

                pipeline_result = self.adapter.run(
                    symbol=symbol,
                    history=history,
                    portfolio_state=current_session.portfolio,
                )

                candidates.append(
                    self._build_candidate(
                        symbol=symbol,
                        result=pipeline_result,
                    )
                )

                succeeded_symbols += 1

            except Exception as error:
                failed_symbol_errors[symbol] = str(error)

        scan_duration_seconds = round(
            time.perf_counter() - started_at,
            6,
        )

        return LivePaperTradingResult(
            session=current_session,
            scanned_symbols=len(symbols),
            succeeded_symbols=succeeded_symbols,
            failed_symbols=len(failed_symbol_errors),
            failed_symbol_errors=failed_symbol_errors,
            scan_duration_seconds=scan_duration_seconds,
            candidates=candidates,
            executed_trades=0,
            rejected_trades=0,
        )

    def _build_candidate(
        self,
        symbol: str,
        result,
    ) -> LivePaperCandidate:
        opportunity_ranking = self.ranking_engine.rank(result)
        score = opportunity_ranking.score

        if result.decision != "BUY":
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason=f"Decision is {result.decision}, not BUY.",
                opportunity_ranking=opportunity_ranking,
            )

        if result.confidence < self.config.min_confidence:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason="Confidence below minimum threshold.",
                opportunity_ranking=opportunity_ranking,
            )

        if result.risk_plan.entry_price > self.config.max_position_value:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason="Entry price exceeds max position value.",
                opportunity_ranking=opportunity_ranking,
            )

        return LivePaperCandidate(
            symbol=symbol,
            result=result,
            score=score,
            accepted=True,
            reason="Accepted candidate.",
            opportunity_ranking=opportunity_ranking,
        )

    def _score_result(self, result) -> float:
        return round(
            (result.confidence * 100.0) - result.expected_risk,
            6,
        )
