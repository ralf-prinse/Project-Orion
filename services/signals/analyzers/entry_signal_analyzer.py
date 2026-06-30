from services.analysis.models import AnalysisResult
from services.signals.base_signal_analyzer import BaseSignalAnalyzer
from services.signals.config.signal_thresholds import get_signal_thresholds
from services.signals.models import Signal, SignalResult


class EntrySignalAnalyzer(BaseSignalAnalyzer):
    """
    Entry-signal analyzer voor Project Orion.

    Deze analyzer vertaalt AnalysisResult naar een eerste deterministisch
    handelssignaal.

    Verantwoordelijkheid:
    - BUY herkennen
    - WATCH herkennen
    - SELL herkennen
    - anders IGNORE

    De analyzer gebruikt centrale signaaldrempels zodat toekomstige backtests
    en strategieprofielen mogelijk blijven zonder hardcoded magic numbers.
    """

    def __init__(
        self,
        threshold_profile: str = "default",
    ):
        self.threshold_profile = threshold_profile
        self.thresholds = get_signal_thresholds(threshold_profile)

    def analyze(
        self,
        analysis_result: AnalysisResult,
        signal_result: SignalResult,
    ) -> SignalResult:
        bullish_score = self._calculate_bullish_score(analysis_result)
        bearish_score = self._calculate_bearish_score(analysis_result)
        neutral_score = self._calculate_neutral_score(
            bullish_score=bullish_score,
            bearish_score=bearish_score,
        )

        signal_result.bullish_score = bullish_score
        signal_result.bearish_score = bearish_score
        signal_result.neutral_score = neutral_score

        if self._is_buy_signal(analysis_result):
            signal_result.signal = Signal.BUY
            signal_result.confidence = bullish_score
            signal_result.add_note("BUY signal detected by EntrySignalAnalyzer.")
            return signal_result

        if self._is_sell_signal(analysis_result):
            signal_result.signal = Signal.SELL
            signal_result.confidence = bearish_score
            signal_result.add_note("SELL signal detected by EntrySignalAnalyzer.")
            return signal_result

        if self._is_watch_signal(analysis_result):
            signal_result.signal = Signal.WATCH
            signal_result.confidence = bullish_score
            signal_result.add_note("WATCH signal detected by EntrySignalAnalyzer.")
            return signal_result

        signal_result.signal = Signal.IGNORE
        signal_result.confidence = neutral_score
        signal_result.add_note("No actionable entry signal detected.")

        return signal_result

    def _is_buy_signal(
        self,
        analysis_result: AnalysisResult,
    ) -> bool:
        buy_thresholds = self.thresholds["buy"]

        return all(
            getattr(analysis_result, score_name) >= minimum_score
            for score_name, minimum_score in buy_thresholds.items()
        )

    def _is_watch_signal(
        self,
        analysis_result: AnalysisResult,
    ) -> bool:
        watch_thresholds = self.thresholds["watch"]

        return all(
            getattr(analysis_result, score_name) >= minimum_score
            for score_name, minimum_score in watch_thresholds.items()
        )

    def _is_sell_signal(
        self,
        analysis_result: AnalysisResult,
    ) -> bool:
        sell_thresholds = self.thresholds["sell"]

        return all(
            getattr(analysis_result, score_name) <= maximum_score
            for score_name, maximum_score in sell_thresholds.items()
        )

    def _calculate_bullish_score(
        self,
        analysis_result: AnalysisResult,
    ) -> int:
        bullish_components = [
            analysis_result.overall_score,
            analysis_result.trend_score,
            analysis_result.momentum_score,
            analysis_result.structure_score,
            analysis_result.volume_score,
            analysis_result.relative_strength_score,
            analysis_result.candlestick_score,
        ]

        return int(round(sum(bullish_components) / len(bullish_components)))

    def _calculate_bearish_score(
        self,
        analysis_result: AnalysisResult,
    ) -> int:
        bearish_components = [
            100 - analysis_result.overall_score,
            100 - analysis_result.trend_score,
            100 - analysis_result.momentum_score,
            100 - analysis_result.structure_score,
        ]

        return int(round(sum(bearish_components) / len(bearish_components)))

    def _calculate_neutral_score(
        self,
        bullish_score: int,
        bearish_score: int,
    ) -> int:
        return max(
            0,
            100 - max(bullish_score, bearish_score),
        )