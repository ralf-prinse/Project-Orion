from typing import Any

from models.trading_pipeline_result import TradingPipelineResult
from services.intelligence.intelligence_models import IndicatorPack
from services.logging_service import LoggingService
from services.orchestration.backtest_simulator import BacktestSimulator
from services.orchestration.market_scanner import MarketScanner


class BacktestEngine:
    """
    Runs Orion over historical multi-asset indicator datasets.

    Flow

    Historical Dataset
            ↓
    MarketScanner
            ↓
    Best Trade
            ↓
    BacktestSimulator
            ↓
    Equity Curve
            ↓
    Trade Log
    """

    def __init__(self):

        self.logger = LoggingService.get_logger(
            "BacktestEngine"
        )

        self.scanner = MarketScanner()

        self.simulator = BacktestSimulator()

    def run(
        self,
        dataset: list[list[IndicatorPack]],
        portfolio_state,
    ) -> dict[str, Any]:

        self.logger.info(
            "Starting backtest (%d timesteps)",
            len(dataset),
        )

        equity = portfolio_state.cash

        equity_curve = []

        trade_log = []

        for timestep, assets in enumerate(dataset):

            self.logger.info(
                "Processing timestep %d (%d assets)",
                timestep,
                len(assets),
            )

            scan_result = self.scanner.scan(
                assets,
                portfolio_state,
            )

            best_trade = scan_result.get(
                "best_trade"
            )

            if not best_trade:

                self.logger.info(
                    "No trade generated at timestep %d",
                    timestep,
                )

                equity_curve.append(equity)

                continue

            pipeline: TradingPipelineResult = best_trade["pipeline"]

            self.logger.info(
                (
                    "Selected %s | %s | "
                    "confidence=%.3f"
                ),
                pipeline.symbol,
                pipeline.decision,
                pipeline.confidence,
            )

            simulation = self.simulator.simulate_trade(
                {
                    "symbol": pipeline.symbol,
                    "decision": pipeline.decision,
                    "pressure_score": pipeline.confidence,
                    "confidence": pipeline.confidence,
                    "strength": pipeline.position_size,
                    "position_size": pipeline.position_size,
                    "expected_risk": pipeline.expected_risk,
                }
            )

            equity += simulation["net_pnl"]

            trade_log.append(
                {
                    "timestep": timestep,
                    "symbol": pipeline.symbol,
                    "decision": pipeline.decision,
                    "score": pipeline.confidence,
                    "confidence": pipeline.confidence,
                    "strength": pipeline.position_size,
                    "position_size": pipeline.position_size,
                    "expected_risk": pipeline.expected_risk,
                    "gross_pnl": simulation["gross_pnl"],
                    "fees": simulation["fees"],
                    "slippage": simulation["slippage"],
                    "net_pnl": simulation["net_pnl"],
                    "outcome": simulation["outcome"],
                    "equity": equity,
                }
            )

            self.logger.info(
                (
                    "Trade finished | "
                    "net_pnl=%.4f equity=%.2f"
                ),
                simulation["net_pnl"],
                equity,
            )

            equity_curve.append(equity)

        result = {
            "initial_equity": portfolio_state.cash,
            "final_equity": equity,
            "net_profit": equity - portfolio_state.cash,
            "equity_curve": equity_curve,
            "trade_log": trade_log,
            "total_trades": len(trade_log),
        }

        self.logger.info(
            (
                "Backtest completed | "
                "trades=%d profit=%.2f "
                "final_equity=%.2f"
            ),
            len(trade_log),
            result["net_profit"],
            result["final_equity"],
        )

        return result