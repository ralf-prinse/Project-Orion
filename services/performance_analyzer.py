from __future__ import annotations

from collections import Counter

from models.performance_analysis_result import PerformanceAnalysisResult
from models.trade_journal_entry import TradeJournalEntry


class PerformanceAnalyzer:
    """
    Deterministic self-evaluation service.

    Analyses ORION's historical trade journal entries and produces
    a performance summary.
    """

    def analyze(
        self,
        entries: list[TradeJournalEntry],
    ) -> PerformanceAnalysisResult:
        if not entries:
            return PerformanceAnalysisResult(
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0.0,
                total_realized_profit_loss=0.0,
                total_unrealized_profit_loss=0.0,
                average_realized_profit_loss=0.0,
                average_return_percent=0.0,
                best_trade_symbol=None,
                best_trade_return_percent=0.0,
                worst_trade_symbol=None,
                worst_trade_return_percent=0.0,
                average_confidence=0.0,
                average_expected_risk=0.0,
                profitable_confidence_threshold=None,
                dominant_regime=None,
                dominant_volatility=None,
                summary="No trade journal entries available.",
            )

        total_trades = len(entries)

        winning_entries = [
            entry
            for entry in entries
            if entry.realized_profit_loss > 0
        ]

        losing_entries = [
            entry
            for entry in entries
            if entry.realized_profit_loss < 0
        ]

        winning_trades = len(winning_entries)
        losing_trades = len(losing_entries)

        win_rate = round(
            (winning_trades / total_trades) * 100,
            2,
        )

        total_realized_profit_loss = round(
            sum(entry.realized_profit_loss for entry in entries),
            2,
        )

        total_unrealized_profit_loss = round(
            sum(entry.unrealized_profit_loss for entry in entries),
            2,
        )

        average_realized_profit_loss = round(
            total_realized_profit_loss / total_trades,
            2,
        )

        average_return_percent = round(
            sum(entry.total_return_percent for entry in entries)
            / total_trades,
            2,
        )

        best_trade = max(
            entries,
            key=lambda entry: entry.total_return_percent,
        )

        worst_trade = min(
            entries,
            key=lambda entry: entry.total_return_percent,
        )

        average_confidence = round(
            sum(entry.confidence for entry in entries)
            / total_trades,
            4,
        )

        average_expected_risk = round(
            sum(entry.expected_risk for entry in entries)
            / total_trades,
            6,
        )

        profitable_confidence_threshold = (
            self._profitable_confidence_threshold(entries)
        )

        dominant_regime = self._most_common(
            entry.regime
            for entry in entries
        )

        dominant_volatility = self._most_common(
            entry.volatility
            for entry in entries
        )

        summary = (
            f"Analysed {total_trades} journal entries. "
            f"Win rate: {win_rate:.2f}%. "
            f"Realized P/L: {total_realized_profit_loss:.2f}. "
            f"Unrealized P/L: {total_unrealized_profit_loss:.2f}."
        )

        return PerformanceAnalysisResult(
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            total_realized_profit_loss=total_realized_profit_loss,
            total_unrealized_profit_loss=total_unrealized_profit_loss,
            average_realized_profit_loss=average_realized_profit_loss,
            average_return_percent=average_return_percent,
            best_trade_symbol=best_trade.symbol,
            best_trade_return_percent=best_trade.total_return_percent,
            worst_trade_symbol=worst_trade.symbol,
            worst_trade_return_percent=worst_trade.total_return_percent,
            average_confidence=average_confidence,
            average_expected_risk=average_expected_risk,
            profitable_confidence_threshold=profitable_confidence_threshold,
            dominant_regime=dominant_regime,
            dominant_volatility=dominant_volatility,
            summary=summary,
        )

    def _profitable_confidence_threshold(
        self,
        entries: list[TradeJournalEntry],
    ) -> float | None:
        profitable = [
            entry.confidence
            for entry in entries
            if entry.realized_profit_loss > 0
        ]

        if not profitable:
            return None

        return round(
            min(profitable),
            4,
        )

    def _most_common(
        self,
        values,
    ) -> str | None:
        counter = Counter(values)

        if not counter:
            return None

        return counter.most_common(1)[0][0]