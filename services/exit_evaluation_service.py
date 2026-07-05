from services.analysis.models import AnalysisResult
from models.trade_lifecycle import ExitSignal, Trade


class ExitEvaluationService:
    """
    Deterministic exit-intelligence service.

    Determines whether Orion should continue holding or advise exiting
    an open trade.

    No AI.
    No UI.
    No order execution.
    """

    def evaluate(
        self,
        trade: Trade,
        analysis: AnalysisResult | None = None,
    ) -> tuple[ExitSignal, int, str, list[str], str, str, str]:
        score = 0
        reasons: list[str] = []

        if trade.current_price <= trade.stop_loss:
            return (
                ExitSignal.STOP_LOSS,
                100,
                "Stop-loss geraakt.",
                ["De huidige koers staat op of onder de ingestelde stop-loss."],
                "Niet relevant: stop-loss heeft prioriteit.",
                "Niet relevant: stop-loss heeft prioriteit.",
                "Risico actief: stop-loss geraakt.",
            )

        if trade.current_price >= trade.take_profit:
            return (
                ExitSignal.TAKE_PROFIT,
                90,
                "Winstdoel bereikt.",
                ["Het ingestelde winstdoel is bereikt."],
                "Niet relevant: winstdoel heeft prioriteit.",
                "Niet relevant: winstdoel heeft prioriteit.",
                "Winstdoel bereikt.",
            )

        profit_percent = self._profit_percent(trade)

        if profit_percent >= 10:
            score += 20
            reasons.append("De positie staat ruim in de winst; winst beschermen wordt belangrijker.")

        if profit_percent < -5:
            score += 30
            reasons.append("De positie staat meer dan 5% in de min.")

        trend_status = "Nog niet geanalyseerd"
        momentum_status = "Nog niet geanalyseerd"
        risk_status = "Prijsregels actief"

        if analysis is not None:
            trend_score = int(getattr(analysis, "trend_score", 0))
            momentum_score = int(getattr(analysis, "momentum_score", 0))
            volatility_score = int(getattr(analysis, "volatility_score", 0))
            structure_score = int(getattr(analysis, "structure_score", 0))

            trend_status = self._score_status(
                label="Trend",
                score=trend_score,
            )
            momentum_status = self._score_status(
                label="Momentum",
                score=momentum_score,
            )
            risk_status = self._risk_status(
                volatility_score=volatility_score,
                structure_score=structure_score,
            )

            if trend_score < 40:
                score += 25
                reasons.append(
                    f"Trend is zwak ({trend_score}/100). De oorspronkelijke setup verliest kwaliteit."
                )

            if momentum_score < 40:
                score += 25
                reasons.append(
                    f"Momentum is zwak ({momentum_score}/100). Koopdruk neemt af."
                )

            if structure_score < 40:
                score += 20
                reasons.append(
                    f"Marktstructuur is zwak ({structure_score}/100). De koersstructuur ondersteunt de trade minder."
                )

            if volatility_score < 35:
                score += 15
                reasons.append(
                    f"Volatiliteitsscore is zwak ({volatility_score}/100). De risico/rendement-verhouding verslechtert."
                )

        score = min(score, 100)

        if score >= 70:
            signal = ExitSignal.EXIT_DUE_TO_WEAKNESS
            summary = "De tradekwaliteit is duidelijk verslechterd."
        else:
            signal = ExitSignal.HOLD_POSITION
            summary = "De positie oogt nog houdbaar. Orion adviseert vast te houden."

        if not reasons:
            reasons.append("Geen directe exit-trigger gevonden.")

        return (
            signal,
            score,
            summary,
            reasons,
            trend_status,
            momentum_status,
            risk_status,
        )

    def _profit_percent(self, trade: Trade) -> float:
        if trade.entry_price <= 0:
            return 0.0

        return ((trade.current_price - trade.entry_price) / trade.entry_price) * 100

    def _score_status(self, label: str, score: int) -> str:
        if score >= 70:
            return f"{label} sterk ({score}/100)"

        if score >= 50:
            return f"{label} neutraal ({score}/100)"

        if score >= 40:
            return f"{label} kwetsbaar ({score}/100)"

        return f"{label} zwak ({score}/100)"

    def _risk_status(
        self,
        volatility_score: int,
        structure_score: int,
    ) -> str:
        if volatility_score >= 60 and structure_score >= 60:
            return (
                f"Risico beheersbaar. Volatiliteit {volatility_score}/100, "
                f"structuur {structure_score}/100."
            )

        if volatility_score < 35 or structure_score < 35:
            return (
                f"Risico verhoogd. Volatiliteit {volatility_score}/100, "
                f"structuur {structure_score}/100."
            )

        return (
            f"Risico neutraal. Volatiliteit {volatility_score}/100, "
            f"structuur {structure_score}/100."
        )