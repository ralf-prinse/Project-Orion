from services.analysis.models import AnalysisResult, IndicatorResult


class MomentumAnalyzer:
    """
    Analyseert momentumkwaliteit op basis van berekende indicatoren.

    Verantwoordelijkheid:
    - Alleen momentumscore bepalen.
    - Alleen momentumgerelateerde analysis notes toevoegen.
    - Geen indicatoren berekenen.
    - Geen BUY/HOLD/IGNORE beslissingen nemen.
    """

    def analyze(
        self,
        indicators: IndicatorResult,
        result: AnalysisResult,
    ) -> int:
        score = 0

        rsi = indicators.get("rsi14")
        macd = indicators.get("macd")

        if rsi is not None:
            if 45 <= rsi <= 70:
                score += 40
                result.add_note("Momentum: RSI gezond voor swing trade")
            elif 35 <= rsi < 45:
                score += 20
                result.add_note("Momentum: RSI zwak maar niet extreem")
            elif rsi > 70:
                score += 10
                result.add_note("Momentum: RSI mogelijk overbought")
            else:
                result.add_note("Momentum: RSI ongunstig")

        if isinstance(macd, dict):
            macd_line = macd.get("macd")
            signal_line = macd.get("signal")
            histogram = macd.get("histogram")

            if (
                macd_line is not None
                and signal_line is not None
                and macd_line > signal_line
            ):
                score += 35
                result.add_note("Momentum: MACD boven signaallijn")
            else:
                result.add_note("Momentum: MACD onder signaallijn")

            if histogram is not None and histogram > 0:
                score += 25
                result.add_note("Momentum: MACD histogram positief")

        return min(score, 100)