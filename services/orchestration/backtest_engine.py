from typing import List, Dict, Any

from services.orchestration.market_scanner import MarketScanner
from services.orchestration.backtest_simulator import BacktestSimulator
from services.intelligence.intelligence_models import IndicatorPack


class BacktestEngine:
    """
    Runs Orion over historical multi-asset indicator datasets.

    Uses:
    - MarketScanner for ranking opportunities
    - BacktestSimulator for deterministic trade simulation
    """

    def __init__(self):
        self.scanner = MarketScanner()
        self.simulator = BacktestSimulator()

    def run(
        self,
        dataset: List[List[IndicatorPack]],
        portfolio_state,
    ) -> Dict[str, Any]:

        equity = portfolio_state.cash
        equity_curve = []
        trade_log = []

        for timestep, assets in enumerate(dataset):
            scan_result = self.scanner.scan(assets, portfolio_state)
            best_trade = scan_result.get("best_trade")

            if not best_trade:
                equity_curve.append(equity)
                continue

            pipeline = best_trade["pipeline"]

            simulation = self.simulator.simulate_trade(pipeline)

            equity += simulation["net_pnl"]

            trade_log.append(
                {
                    "timestep": timestep,
                    "symbol": pipeline["symbol"],
                    "decision": pipeline["decision"],
                    "score": pipeline["pressure_score"],
                    "confidence": pipeline["confidence"],
                    "strength": pipeline["strength"],
                    "position_size": pipeline["position_size"],
                    "expected_risk": pipeline["expected_risk"],
                    "gross_pnl": simulation["gross_pnl"],
                    "fees": simulation["fees"],
                    "slippage": simulation["slippage"],
                    "net_pnl": simulation["net_pnl"],
                    "outcome": simulation["outcome"],
                    "equity": equity,
                }
            )

            equity_curve.append(equity)

        return {
            "initial_equity": portfolio_state.cash,
            "final_equity": equity,
            "net_profit": equity - portfolio_state.cash,
            "equity_curve": equity_curve,
            "trade_log": trade_log,
            "total_trades": len(trade_log),
        }