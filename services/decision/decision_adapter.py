from services.decision.decision_models import MarketSignal, PositionContext, DecisionInput


class DecisionAdapter:
    """
    Converts existing analysis output → decision engine input.
    """

    def from_analysis(self, analysis_result, portfolio_state) -> DecisionInput:
        signal = MarketSignal(
            symbol=analysis_result.symbol,
            score=analysis_result.score,
            trend=analysis_result.trend,
            volatility=analysis_result.volatility,
            momentum=getattr(analysis_result, "momentum", 0.0),
        )

        context = PositionContext(
            cash=portfolio_state.cash,
            position_size=portfolio_state.position_size,
            exposure=getattr(portfolio_state, "exposure", 0.0),
        )

        return DecisionInput(
            signal=signal,
            context=context,
        )