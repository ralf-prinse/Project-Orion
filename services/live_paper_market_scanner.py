from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import (
    LivePaperCandidate,
    LivePaperTradingResult,
)
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from providers.yahoo_provider import YahooProvider
from services.paper_trading_pipeline_adapter import (
    PaperTradingPipelineAdapter,
)


class LivePaperMarketScanner:
    """
    Live paper market scanner.

    Responsibilities
    ----------------
    - Load symbols from watchlist
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
    ):
        self.config = config or LivePaperTradingConfig()
        self.provider = provider or YahooProvider()
        self.adapter = adapter or PaperTradingPipelineAdapter()

    def run(
        self,
        session: TradingSession | None = None,
    ) -> LivePaperTradingResult:
        symbols = self._load_symbols()

        current_session = session or TradingSession(
            name="Orion Live Paper Trading",
            portfolio=PaperPortfolio(
                cash=self.config.initial_cash,
            ),
        )

        candidates: list[LivePaperCandidate] = []
        failed_symbols = 0

        for symbol in symbols:
            try:
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

            except Exception:
                failed_symbols += 1

        return LivePaperTradingResult(
            session=current_session,
            scanned_symbols=len(symbols),
            failed_symbols=failed_symbols,
            candidates=candidates,
            executed_trades=0,
            rejected_trades=0,
        )

    def _load_symbols(self) -> list[str]:
        if not self.config.watchlist_path.exists():
            raise FileNotFoundError(
                f"Watchlist not found: {self.config.watchlist_path}"
            )

        symbols: list[str] = []

        for line in self.config.watchlist_path.read_text().splitlines():
            symbol = line.strip().upper()

            if symbol and not symbol.startswith("#"):
                symbols.append(symbol)

        return symbols[: self.config.max_symbols]

    def _build_candidate(
        self,
        symbol: str,
        result,
    ) -> LivePaperCandidate:
        score = self._score_result(result)

        if result.decision != "BUY":
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason=f"Decision is {result.decision}, not BUY.",
            )

        if result.confidence < self.config.min_confidence:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason="Confidence below minimum threshold.",
            )

        if result.risk_plan.entry_price > self.config.max_position_value:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason="Entry price exceeds max position value.",
            )

        return LivePaperCandidate(
            symbol=symbol,
            result=result,
            score=score,
            accepted=True,
            reason="Accepted candidate.",
        )

    def _score_result(self, result) -> float:
        return round(
            (result.confidence * 100.0) - result.expected_risk,
            6,
        )