from services.backtesting.models import (
    BacktestCandle,
    BacktestConfig,
    BacktestTrade,
)
from services.planner.models import TradePlanResult


class TradeSimulator:
    """
    Deterministische simulator voor één bestaand handelsplan.

    De simulator doet geen analyse, geen signal generation en geen portfolio-
    mutatie. Hij beantwoordt uitsluitend de vraag: wat zou er met dit concrete
    plan zijn gebeurd binnen deze candles?
    """

    def simulate(
        self,
        symbol: str,
        trade_plan: TradePlanResult,
        candles: list[BacktestCandle],
        config: BacktestConfig,
    ) -> BacktestTrade | None:
        if trade_plan.action != "BUY":
            return None

        entry_candle_index = self._find_entry_candle_index(
            candles=candles,
            entry_price=trade_plan.entry_price,
        )

        if entry_candle_index is None:
            return None

        entry_candle = candles[entry_candle_index]
        exit_candle, exit_price, exit_reason = self._find_exit(
            candles=candles[entry_candle_index:],
            stop_loss=trade_plan.stop_loss,
            target_price=trade_plan.target_price,
            config=config,
        )

        gross_pnl = (exit_price - trade_plan.entry_price) * trade_plan.shares
        invested_amount = trade_plan.entry_price * trade_plan.shares
        return_pct = (gross_pnl / invested_amount * 100) if invested_amount > 0 else 0.0

        return BacktestTrade(
            symbol=symbol.upper(),
            action=trade_plan.action,
            entry_date=entry_candle.timestamp,
            entry_price=round(trade_plan.entry_price, config.price_precision),
            exit_date=exit_candle.timestamp,
            exit_price=round(exit_price, config.price_precision),
            shares=trade_plan.shares,
            exit_reason=exit_reason,
            gross_pnl=round(gross_pnl, 2),
            return_pct=round(return_pct, config.percentage_precision),
        )

    def _find_entry_candle_index(
        self,
        candles: list[BacktestCandle],
        entry_price: float,
    ) -> int | None:
        for index, candle in enumerate(candles):
            if candle.low <= entry_price <= candle.high:
                return index
        return None

    def _find_exit(
        self,
        candles: list[BacktestCandle],
        stop_loss: float,
        target_price: float,
        config: BacktestConfig,
    ) -> tuple[BacktestCandle, float, str]:
        for candle in candles:
            stop_hit = candle.low <= stop_loss
            target_hit = candle.high >= target_price

            if stop_hit and target_hit:
                if config.conservative_same_candle_exit:
                    return candle, stop_loss, "STOP_LOSS"
                return candle, target_price, "TARGET"

            if stop_hit:
                return candle, stop_loss, "STOP_LOSS"

            if target_hit:
                return candle, target_price, "TARGET"

        final_candle = candles[-1]
        return final_candle, final_candle.close, "END_OF_DATA"
