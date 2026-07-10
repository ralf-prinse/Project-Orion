def _process_open_position_exits(
    self,
    session: TradingSession,
    cycle_number: int,
    session_id: str,
) -> TradingSession:
    portfolio = session.portfolio
    position_states = dict(session.position_states)
    risk_plans = dict(session.risk_plans)

    for position in list(portfolio.positions.values()):
        symbol = position.symbol.upper()
        state = position_states.get(symbol)
        risk_plan = risk_plans.get(symbol)

        if state is not None and risk_plan is not None:
            decision = self.position_monitor.evaluate_managed(
                position=position,
                state=state,
                risk_plan=risk_plan,
            )
        else:
            decision = self.position_monitor.evaluate(
                position=position,
                config=self.config.live_config,
            )

        print(
            f"Position monitor: "
            f"{decision.symbol} -> {decision.action} "
            f"({decision.unrealized_return_percent * 100:.2f}%) "
            f"{decision.reason}"
        )

        result = self.exit_engine.execute(
            portfolio=portfolio,
            decision=decision,
        )

        if not result.executed:
            continue

        print(
            f"Exit executed: "
            f"{result.symbol} -> {result.action} | "
            f"{result.reason}"
        )

        self._append_exit_journal_entry(
            position=position,
            action=result.action,
            reason=decision.reason,
            cycle_number=cycle_number,
            session_id=session_id,
        )

        closed_symbol = result.symbol.upper()
        position_states.pop(closed_symbol, None)
        risk_plans.pop(closed_symbol, None)

    return TradingSession(
        name=session.name,
        portfolio=portfolio,
        position_states=position_states,
        risk_plans=risk_plans,
        status=session.status,
    )