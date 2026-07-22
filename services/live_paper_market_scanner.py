from __future__ import annotations

import time
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

import pandas as pd

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

        benchmark_symbol = "SPY"
        benchmark_required = (
            self.config.require_intraday_confirmation
            and "XUSA" in self.config.allowed_entry_market_codes
            and self.market_session_service is not None
            and self.market_session_service.is_symbol_market_open(
                symbol=benchmark_symbol,
                now=evaluated_at,
            )
        )
        requested_symbols = list(open_symbols)
        if benchmark_required and benchmark_symbol not in requested_symbols:
            requested_symbols.append(benchmark_symbol)

        prefetched_history = None
        if self.historical_provider is not None and requested_symbols:
            prefetched_history = self.historical_provider.get_history(
                symbols=requested_symbols,
                period=self.config.history_period,
                interval=self.config.history_interval,
            )

        benchmark_history = None
        if benchmark_required:
            try:
                if prefetched_history is not None:
                    raw_benchmark = prefetched_history.get(benchmark_symbol)
                    if raw_benchmark is None or raw_benchmark.empty:
                        raise ValueError(
                            "No benchmark history returned for SPY."
                        )
                else:
                    raw_benchmark = self.provider.get_historical_data(
                        symbol=benchmark_symbol,
                        period=self.config.history_period,
                        interval=self.config.history_interval,
                    )
                benchmark_history = self._prepare_history(
                    symbol=benchmark_symbol,
                    history=raw_benchmark,
                    evaluated_at=evaluated_at,
                )
            except Exception:
                # Candidate confirmation below rejects fail-closed with an
                # explicit benchmark reason. A missing benchmark must not
                # turn an otherwise healthy scan into a failed cycle.
                benchmark_history = None

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

                history = self._prepare_history(
                    symbol=symbol,
                    history=history,
                    evaluated_at=evaluated_at,
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
                        history=history,
                        benchmark_history=benchmark_history,
                        evaluated_at=evaluated_at,
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

    def _prepare_history(
        self,
        *,
        symbol: str,
        history: pd.DataFrame,
        evaluated_at: datetime,
    ) -> pd.DataFrame:
        interval = self.config.history_interval.strip().lower()
        prepared = history.copy()
        prepared.attrs["interval"] = interval

        if interval != "5m":
            return prepared
        if not isinstance(prepared.index, pd.DatetimeIndex):
            raise ValueError(
                f"Intraday history for {symbol} requires a DatetimeIndex."
            )

        evaluated_timestamp = pd.Timestamp(evaluated_at)
        if evaluated_timestamp.tzinfo is None:
            evaluated_timestamp = evaluated_timestamp.tz_localize("UTC")
        else:
            evaluated_timestamp = evaluated_timestamp.tz_convert("UTC")

        timestamps = prepared.index
        if timestamps.tz is None:
            timestamps = timestamps.tz_localize("UTC")
        else:
            timestamps = timestamps.tz_convert("UTC")

        complete_before = evaluated_timestamp - timedelta(minutes=5)
        prepared = prepared.loc[timestamps <= complete_before].copy()
        prepared.attrs["interval"] = interval
        if prepared.empty:
            raise ValueError(
                f"No completed 5-minute candles available for {symbol}."
            )

        latest_timestamp = timestamps[timestamps <= complete_before][-1]
        latest_completed_at = latest_timestamp + timedelta(minutes=5)
        maximum_age = self.config.max_history_age_minutes
        if maximum_age is not None:
            age_minutes = (
                evaluated_timestamp - latest_completed_at
            ).total_seconds() / 60.0
            if age_minutes > maximum_age:
                raise ValueError(
                    f"Latest completed 5-minute candle for {symbol} is "
                    f"{age_minutes:.1f} minutes old after completion; "
                    "maximum is "
                    f"{maximum_age} minutes."
                )

        return prepared

    def _build_candidate(
        self,
        symbol: str,
        result,
        history: pd.DataFrame | None = None,
        benchmark_history: pd.DataFrame | None = None,
        evaluated_at: datetime | None = None,
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

        selectivity_reasons = self._selectivity_rejections(
            result=result,
            opportunity_score=score,
        )
        if selectivity_reasons:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason=(
                    "Selectivity gate rejected candidate; "
                    + " ".join(selectivity_reasons)
                ),
                opportunity_ranking=opportunity_ranking,
            )

        confirmation_reasons = self._entry_confirmation_rejections(
            symbol=symbol,
            history=history,
            benchmark_history=benchmark_history,
            evaluated_at=evaluated_at,
        )
        if confirmation_reasons:
            return LivePaperCandidate(
                symbol=symbol,
                result=result,
                score=score,
                accepted=False,
                reason=(
                    "Entry confirmation rejected candidate; "
                    + " ".join(confirmation_reasons)
                ),
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

    def _entry_confirmation_rejections(
        self,
        *,
        symbol: str,
        history: pd.DataFrame | None,
        benchmark_history: pd.DataFrame | None,
        evaluated_at: datetime | None,
    ) -> list[str]:
        reasons: list[str] = []
        allowed_markets = self.config.allowed_entry_market_codes

        if allowed_markets:
            if self.market_session_service is None:
                return ["market metadata is unavailable."]
            status = self.market_session_service.get_symbol_status(
                symbol=symbol,
                now=evaluated_at or self.clock(),
            )
            if status.market.code not in allowed_markets:
                return [
                    f"market {status.market.code} is not enabled for entries."
                ]
            if status.session_open is None or status.session_close is None:
                return ["official session boundaries are unavailable."]

            minutes_after_open = (
                status.local_time - status.session_open
            ).total_seconds() / 60.0
            minutes_before_close = (
                status.session_close - status.local_time
            ).total_seconds() / 60.0
            if minutes_after_open < self.config.entry_open_buffer_minutes:
                reasons.append(
                    "opening buffer is active: "
                    f"{minutes_after_open:.1f}/"
                    f"{self.config.entry_open_buffer_minutes} minutes."
                )
            if minutes_before_close < self.config.entry_close_buffer_minutes:
                reasons.append(
                    "closing buffer is active: "
                    f"{minutes_before_close:.1f}/"
                    f"{self.config.entry_close_buffer_minutes} minutes."
                )
        else:
            status = None

        if not self.config.require_intraday_confirmation:
            return reasons
        if history is None or history.empty:
            reasons.append("completed intraday history is unavailable.")
            return reasons
        if status is None:
            reasons.append("official session metadata is unavailable.")
            return reasons

        prepared = history.copy()
        timestamps = prepared.index
        if not isinstance(timestamps, pd.DatetimeIndex):
            reasons.append("intraday history has no DatetimeIndex.")
            return reasons
        if timestamps.tz is None:
            timestamps = timestamps.tz_localize("UTC")
        else:
            timestamps = timestamps.tz_convert("UTC")
        prepared.index = timestamps

        session_open_utc = pd.Timestamp(status.session_open).tz_convert("UTC")
        session_rows = prepared.loc[timestamps >= session_open_utc]
        if len(session_rows) < 2:
            reasons.append("fewer than two completed session candles exist.")
            return reasons

        latest = session_rows.iloc[-1]
        previous = session_rows.iloc[-2]
        latest_close = float(latest["Close"])
        latest_open = float(latest["Open"])
        if latest_close <= float(previous["Close"]) or latest_close <= latest_open:
            reasons.append("latest completed 5-minute candle is not bullish.")

        fifteen_minute_close = (
            session_rows["Close"]
            .resample("15min")
            .last()
            .dropna()
        )
        if len(fifteen_minute_close) < 2:
            reasons.append("15-minute trend confirmation is unavailable.")
        else:
            latest_15m = float(fifteen_minute_close.iloc[-1])
            previous_15m = float(fifteen_minute_close.iloc[-2])
            trend_average = float(
                fifteen_minute_close.tail(4).mean()
            )
            if latest_15m <= previous_15m or latest_15m <= trend_average:
                reasons.append("15-minute trend is not rising.")

        volume = session_rows["Volume"].astype(float)
        typical_price = (
            session_rows["High"].astype(float)
            + session_rows["Low"].astype(float)
            + session_rows["Close"].astype(float)
        ) / 3.0
        total_volume = float(volume.sum())
        if total_volume <= 0:
            reasons.append("session VWAP is unavailable because volume is zero.")
        else:
            session_vwap = float((typical_price * volume).sum() / total_volume)
            if latest_close <= session_vwap:
                reasons.append(
                    f"price {latest_close:.4f} is not above session VWAP "
                    f"{session_vwap:.4f}."
                )

        local_index = timestamps.tz_convert(status.market.timezone_name)
        latest_local = local_index[-1]
        same_slot = (
            (local_index.hour == latest_local.hour)
            & (local_index.minute == latest_local.minute)
            & (local_index.date < latest_local.date())
        )
        prior_slot_volume = prepared.loc[same_slot, "Volume"].astype(float)
        if len(prior_slot_volume) < 2:
            reasons.append("same-time relative-volume history is unavailable.")
        else:
            baseline_volume = float(prior_slot_volume.median())
            relative_volume = (
                float(latest["Volume"]) / baseline_volume
                if baseline_volume > 0
                else 0.0
            )
            if relative_volume < self.config.min_intraday_relative_volume:
                reasons.append(
                    "relative volume "
                    f"{relative_volume:.2f} is below "
                    f"{self.config.min_intraday_relative_volume:.2f}."
                )

        if benchmark_history is None or benchmark_history.empty:
            reasons.append("SPY relative-strength benchmark is unavailable.")
        else:
            benchmark = benchmark_history.copy()
            benchmark_index = benchmark.index
            if benchmark_index.tz is None:
                benchmark_index = benchmark_index.tz_localize("UTC")
            else:
                benchmark_index = benchmark_index.tz_convert("UTC")
            benchmark.index = benchmark_index
            benchmark = benchmark.loc[benchmark_index <= timestamps[-1]]
            if len(prepared) < 4 or len(benchmark) < 4:
                reasons.append("15-minute relative strength is unavailable.")
            else:
                symbol_return = (
                    latest_close / float(prepared["Close"].iloc[-4])
                ) - 1.0
                benchmark_return = (
                    float(benchmark["Close"].iloc[-1])
                    / float(benchmark["Close"].iloc[-4])
                ) - 1.0
                relative_strength = symbol_return - benchmark_return
                if (
                    relative_strength
                    < self.config.min_intraday_relative_strength
                ):
                    reasons.append(
                        "15-minute relative strength "
                        f"{relative_strength:.2%} is below "
                        f"{self.config.min_intraday_relative_strength:.2%}."
                    )

        return reasons

    def _selectivity_rejections(
        self,
        *,
        result,
        opportunity_score: float,
    ) -> list[str]:
        reasons: list[str] = []
        thesis = result.investment_thesis

        if opportunity_score < self.config.min_opportunity_score:
            reasons.append(
                "opportunity score "
                f"{opportunity_score:.2f} is below "
                f"{self.config.min_opportunity_score:.2f}."
            )

        if thesis is None:
            reasons.append("investment thesis is unavailable.")
            return reasons

        if (
            self.config.require_buy_thesis
            and str(thesis.stance).strip().upper() != "BUY"
        ):
            reasons.append(
                f"thesis stance is {thesis.stance}, not BUY."
            )

        if thesis.conviction < self.config.min_thesis_conviction:
            reasons.append(
                "thesis conviction "
                f"{thesis.conviction:.2f} is below "
                f"{self.config.min_thesis_conviction:.2f}."
            )

        factor_map = {
            factor.name: factor.score
            for factor in thesis.factors
        }
        thresholds = {
            "trend": self.config.min_trend_factor,
            "momentum": self.config.min_momentum_factor,
            "pressure_confirmation": (
                self.config.min_pressure_confirmation_factor
            ),
        }
        for name, minimum in thresholds.items():
            actual = factor_map.get(name)
            if actual is None:
                reasons.append(f"{name} factor is unavailable.")
            elif actual < minimum:
                reasons.append(
                    f"{name} factor {actual:.2f} is below "
                    f"{minimum:.2f}."
                )

        return reasons

    def _score_result(self, result) -> float:
        return round(
            (result.confidence * 100.0) - result.expected_risk,
            6,
        )
