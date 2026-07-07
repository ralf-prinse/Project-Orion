from __future__ import annotations

from models.live_paper_trading_config import LivePaperTradingConfig
from models.live_paper_trading_result import (
    LivePaperCandidate,
    LivePaperTradingResult,
)
from models.market_snapshot import MarketSnapshot
from models.paper_portfolio import PaperPortfolio
from models.trading_session import TradingSession
from providers.yahoo_provider import YahooProvider
from services.paper_trading_pipeline_adapter import (
    PaperTradingPipelineAdapter,
)
from services.trading_cycle import TradingCycle


class LivePaperMarketScanner:
    """
    Live paper trading scanner.

    Uses real market data through YahooProvider, but only executes
    deterministic paper trades.

    Responsibilities
    ----------------
    - Load symbols from watchlist
    - Download historical market data
    - Run IndicatorBuilder + TradingPipeline
    - Rank opportunities
    - Allocate limited paper capital
    - Execute paper trades through TradingCycle

    Does NOT
    --------
    - Use real money
    - Place real broker orders
    - Bypass risk or execution validation
    """

    def __init__(
        self,
        config: LivePaperTradingConfig | None = None,
        provider: YahooProvider | None = None,
        adapter: PaperTradingPipelineAdapter | None = None,
        trading_cycle: TradingCycle | None = None,
    ):
        self.config = config or LivePaperTradingConfig()
        self.provider = provider or YahooProvider()
        self.adapter = adapter or PaperTradingPipelineAdapter()
        self.trading_cycle = trading_cycle or TradingCycle()

    def run(self) -> LivePaperTradingResult:
        symbols = self._load_symbols()

        session = TradingSession(
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
                    portfolio_state=session.portfolio,
                )

                candidate = self._build_candidate(
                    symbol=symbol,
                    result=pipeline_result,
                )

                candidates.append(candidate)

            except Exception:
                failed_symbols += 1

        ranked_candidates = sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        executed_trades = 0
        rejected_trades = 0
        current_session = session

        for candidate in ranked_candidates:
            if current_session.open_positions >= self.config.max_open_positions:
                rejected_trades += 1
                continue

            if not candidate.accepted:
                rejected_trades += 1
                continue

            quantity = self._calculate_quantity(
                current_cash=current_session.cash,
                entry_price=candidate.result.risk_plan.entry_price,
            )

            if quantity <= 0:
                rejected_trades += 1
                continue

            snapshot = MarketSnapshot(
                symbol=candidate.symbol,
                current_price=candidate.result.risk_plan.entry_price,
                pipeline_result=candidate.result,
            )

            cycle_result = self.trading_cycle.run(
                session=current_session,
                snapshot=snapshot,
                quantity=quantity,
            )

            current_session = cycle_result.session

            if cycle_result.action == "OPEN_POSITION":
                executed_trades += 1
            else:
                rejected_trades += 1

        return LivePaperTradingResult(
            session=current_session,
            scanned_symbols=len(symbols),
            failed_symbols=failed_symbols,
            candidates=candidates,
            executed_trades=executed_trades,
            rejected_trades=rejected_trades,
        )

    def _load_symbols(self) -> list[str]:
        if not self.config.watchlist_path.exists():
            raise FileNotFoundError(
                f"Watchlist not found: {self.config.watchlist_path}"
            )

        symbols: list[str] = []

        for line in self.config.watchlist_path.read_text().splitlines():
            symbol = line.strip().upper()

            if not symbol:
                continue

            if symbol.startswith("#"):
                continue

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

    def _score_result(
        self,
        result,
    ) -> float:
        return round(
            (result.confidence * 100.0) - result.expected_risk,
            6,
        )

    def _calculate_quantity(
        self,
        current_cash: float,
        entry_price: float,
    ) -> int:
        if entry_price <= 0:
            return 0

        available_value = min(
            current_cash,
            self.config.max_position_value,
        )

        return int(available_value // entry_price)