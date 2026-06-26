from models.technical_analysis import TechnicalAnalysis


class DecisionEngine:
    """
    Vertaalt analyse naar één eindactie voor de gebruiker.

    Mogelijke acties:
    - BUY
    - HOLD
    - SELL
    - NONE
    """

    def decide(
        self,
        technical_analysis: TechnicalAnalysis,
        has_position: bool = False,
    ) -> str:
        if has_position:
            return self._decide_for_existing_position(technical_analysis)

        return self._decide_for_new_position(technical_analysis)

    def _decide_for_new_position(self, technical_analysis: TechnicalAnalysis) -> str:
        if (
            technical_analysis.rsi_signal == "oversold"
            and technical_analysis.trend_signal == "uptrend"
        ):
            return "BUY"

        return "NONE"

    def _decide_for_existing_position(self, technical_analysis: TechnicalAnalysis) -> str:
        if technical_analysis.rsi_signal == "overbought":
            return "SELL"

        return "HOLD"