from typing import Dict, List, Any


class BacktestVisualizer:
    """
    Converts backtest results into UI-safe chart and summary data.
    No drawing. No UI logic.
    """

    def build_equity_curve(self, backtest_result: Dict[str, Any]) -> Dict[str, Any]:
        equity_curve: List[float] = backtest_result.get("equity_curve", [])

        points = [
            {
                "x": index,
                "y": equity,
            }
            for index, equity in enumerate(equity_curve)
        ]

        return {
            "title": "Backtest Equity Curve",
            "x_label": "Timestep",
            "y_label": "Equity",
            "points": points,
            "initial_equity": backtest_result.get("initial_equity", 0.0),
            "final_equity": backtest_result.get("final_equity", 0.0),
            "net_profit": backtest_result.get("net_profit", 0.0),
            "total_trades": backtest_result.get("total_trades", 0),
        }

    def build_trade_summary(self, backtest_result: Dict[str, Any]) -> Dict[str, Any]:
        trade_log = backtest_result.get("trade_log", [])

        total_trades = len(trade_log)

        winning_trades = sum(
            1 for trade in trade_log
            if trade.get("net_pnl", 0.0) > 0
        )

        losing_trades = sum(
            1 for trade in trade_log
            if trade.get("net_pnl", 0.0) < 0
        )

        break_even_trades = total_trades - winning_trades - losing_trades

        win_rate = winning_trades / total_trades if total_trades else 0.0

        total_gross_pnl = sum(trade.get("gross_pnl", 0.0) for trade in trade_log)
        total_fees = sum(trade.get("fees", 0.0) for trade in trade_log)
        total_slippage = sum(trade.get("slippage", 0.0) for trade in trade_log)
        total_net_pnl = sum(trade.get("net_pnl", 0.0) for trade in trade_log)

        average_net_pnl = total_net_pnl / total_trades if total_trades else 0.0

        return {
            "total_trades": total_trades,
            "winning_trades": winning_trades,
            "losing_trades": losing_trades,
            "break_even_trades": break_even_trades,
            "win_rate": win_rate,
            "total_gross_pnl": round(total_gross_pnl, 6),
            "total_fees": round(total_fees, 6),
            "total_slippage": round(total_slippage, 6),
            "total_net_pnl": round(total_net_pnl, 6),
            "average_net_pnl": round(average_net_pnl, 6),
        }