from dataclasses import dataclass
from models.technical_analysis import TechnicalAnalysis


@dataclass
class TradeDecision:
    action: str
    reason: str
    suggested_holding_days: int = 2
    internal_confidence: float = 0.0
    internal_risk_level: str = "NORMAL"


class DecisionEngine:
    """
    Decision Engine 2.0

    Orion geeft uiteindelijk maar vier eindacties:
    - BUY
    - HOLD
    - SELL
    - NONE

    Alle technische signalen blijven intern.
    """

    def decide(
        self,
        technical_analysis: TechnicalAnalysis,
        has_position: bool = False,
    ) -> str:
        decision = self.make_decision(
            technical_analysis=technical_analysis,
            has_position=has_position,
        )
        return decision.action

    def make_decision(
        self,
        technical_analysis: TechnicalAnalysis,
        has_position: bool = False,
    ) -> TradeDecision:
        if has_position:
            return self._decide_existing_position(technical_analysis)

        return self._decide_new_position(technical_analysis)

    def _decide_new_position(
        self,
        technical_analysis: TechnicalAnalysis,
    ) -> TradeDecision:
        rsi_signal = getattr(technical_analysis, "rsi_signal", "neutral")
        trend_signal = getattr(technical_analysis, "trend_signal", "neutral")
        momentum_signal = getattr(technical_analysis, "momentum_signal", "neutral")
        volume_signal = getattr(technical_analysis, "volume_signal", "neutral")

        if trend_signal == "downtrend":
            return TradeDecision(
                action="NONE",
                reason="Trend is niet sterk genoeg voor een swing trade.",
                internal_confidence=0.20,
                internal_risk_level="HIGH",
            )

        if rsi_signal == "oversold" and trend_signal == "uptrend":
            return TradeDecision(
                action="BUY",
                reason="Sterke swing-trade kans binnen een opwaartse trend.",
                suggested_holding_days=2,
                internal_confidence=0.82,
                internal_risk_level="NORMAL",
            )

        if (
            trend_signal == "uptrend"
            and momentum_signal in ["positive", "strong", "bullish"]
            and volume_signal in ["high", "positive", "strong"]
        ):
            return TradeDecision(
                action="BUY",
                reason="Momentum en volume bevestigen een mogelijke korte swing trade.",
                suggested_holding_days=2,
                internal_confidence=0.78,
                internal_risk_level="NORMAL",
            )

        return TradeDecision(
            action="NONE",
            reason="Geen overtuigende korte termijn trade.",
            internal_confidence=0.30,
            internal_risk_level="NORMAL",
        )

    def _decide_existing_position(
        self,
        technical_analysis: TechnicalAnalysis,
    ) -> TradeDecision:
        rsi_signal = getattr(technical_analysis, "rsi_signal", "neutral")
        trend_signal = getattr(technical_analysis, "trend_signal", "neutral")
        momentum_signal = getattr(technical_analysis, "momentum_signal", "neutral")

        if rsi_signal == "overbought":
            return TradeDecision(
                action="SELL",
                reason="Winst nemen: aandeel lijkt op korte termijn oververhit.",
                suggested_holding_days=0,
                internal_confidence=0.80,
                internal_risk_level="LOW",
            )

        if trend_signal == "downtrend":
            return TradeDecision(
                action="SELL",
                reason="Verkopen: trend is verslechterd.",
                suggested_holding_days=0,
                internal_confidence=0.76,
                internal_risk_level="HIGH",
            )

        if momentum_signal in ["negative", "weak", "bearish"]:
            return TradeDecision(
                action="SELL",
                reason="Verkopen: momentum verzwakt.",
                suggested_holding_days=0,
                internal_confidence=0.70,
                internal_risk_level="NORMAL",
            )

        return TradeDecision(
            action="HOLD",
            reason="Positie vasthouden: er is nog geen verkoopsignaal.",
            suggested_holding_days=1,
            internal_confidence=0.65,
            internal_risk_level="NORMAL",
        )

    def decide_from_rsi_signal(self, rsi_signal: str) -> str:
        """
        Compatibiliteit met oudere tests.
        """
        if rsi_signal == "oversold":
            return "BUY"

        if rsi_signal == "overbought":
            return "SELL"

        return "NONE"