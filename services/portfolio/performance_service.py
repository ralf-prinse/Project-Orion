class PerformanceService:
    """
    Deterministic performance calculations.
    """

    def calculate(self, portfolio_state):
        history = portfolio_state.history

        equity = []
        drawdown = []

        peak = 0

        for h in history:
            value = h.total_value
            equity.append(value)

            peak = max(peak, value)
            dd = (value - peak) / peak if peak != 0 else 0
            drawdown.append(dd)

        return {
            "equity_curve": equity,
            "drawdown_curve": drawdown,
        }