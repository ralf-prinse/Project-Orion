from models.trade_lifecycle import ExitSignal, Trade


class ExitEvaluationService:
    """
    Determines whether Orion should continue holding
    or advise exiting an open trade.

    This service contains deterministic business logic only.
    No AI.
    No UI.
    """

    def evaluate(self, trade: Trade) -> tuple[ExitSignal, int, str, list[str]]:
        score = 0
        reasons: list[str] = []

        # -----------------------------
        # Stop-loss
        # -----------------------------

        if trade.current_price <= trade.stop_loss:
            score += 100
            reasons.append(
                "De huidige koers staat op of onder de ingestelde stop-loss."
            )

            return (
                ExitSignal.STOP_LOSS,
                score,
                "Stop-loss geraakt.",
                reasons,
            )

        # -----------------------------
        # Take-profit
        # -----------------------------

        if trade.current_price >= trade.take_profit:
            score += 90
            reasons.append(
                "Het ingestelde winstdoel is bereikt."
            )

            return (
                ExitSignal.TAKE_PROFIT,
                score,
                "Winstdoel bereikt.",
                reasons,
            )

        # -----------------------------
        # Winst beschermen
        # -----------------------------

        profit_percent = (
            (trade.current_price - trade.entry_price)
            / trade.entry_price
        ) * 100

        if profit_percent >= 10:
            score += 20
            reasons.append(
                "De positie staat ruim in de winst."
            )

        elif profit_percent < -5:
            score += 30
            reasons.append(
                "De positie staat meer dan 5% in de min."
            )

        # -----------------------------
        # Beslissing
        # -----------------------------

        if score >= 70:
            signal = ExitSignal.EXIT_DUE_TO_WEAKNESS
            summary = "De positie begint risico te tonen."

        else:
            signal = ExitSignal.HOLD_POSITION
            summary = (
                "De positie oogt gezond. Orion adviseert vast te houden."
            )

        return (
            signal,
            score,
            summary,
            reasons,
        )