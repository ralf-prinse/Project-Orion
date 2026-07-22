from __future__ import annotations

from dataclasses import dataclass

from models.live_paper_trading_config import LivePaperTradingConfig
from models.paper_position import PaperPosition


@dataclass(frozen=True)
class TradingCostEstimate:
    buy_commission_eur: float
    sell_commission_eur: float
    slippage_eur: float
    external_fees_eur: float
    fx_conversion_buffer_eur: float
    market_data_overhead_eur: float
    total_cost_eur: float


class TradingCostEstimator:
    """Conservative IBKR round-trip cost estimate in portfolio EUR."""

    EUROPEAN_COMMISSION_RATE = 0.0005
    US_FIXED_PER_SHARE_USD = 0.005
    US_FIXED_MINIMUM_USD = 1.0
    US_TIERED_PER_SHARE_USD = 0.0035
    US_TIERED_MINIMUM_USD = 0.35
    EU_FIXED_MINIMUM_EUR = 3.0
    EU_TIERED_MINIMUM_EUR = 1.25

    def estimate_round_trip(
        self,
        *,
        position: PaperPosition,
        config: LivePaperTradingConfig,
    ) -> TradingCostEstimate:
        currency = position.currency.strip().upper()
        buy_value_eur = position.cost_basis
        sell_value_eur = position.market_value

        if currency == "USD":
            buy_commission = self._us_commission_eur(
                quantity=position.quantity,
                fx_rate_to_base=position.fx_rate_to_base,
                pricing_plan=config.ibkr_pricing_plan,
            )
            sell_commission = buy_commission
        else:
            minimum = (
                self.EU_TIERED_MINIMUM_EUR
                if config.ibkr_pricing_plan
                == LivePaperTradingConfig.TIERED_PRICING
                else self.EU_FIXED_MINIMUM_EUR
            )
            buy_commission = max(
                minimum,
                buy_value_eur * self.EUROPEAN_COMMISSION_RATE,
            )
            sell_commission = max(
                minimum,
                sell_value_eur * self.EUROPEAN_COMMISSION_RATE,
            )

        slippage = (
            buy_value_eur + sell_value_eur
        ) * config.estimated_slippage_pct_per_side

        fx_buffer = 0.0
        if (
            currency != "EUR"
            and config.include_auto_fx_conversion_buffer
        ):
            fx_buffer = (
                buy_value_eur + sell_value_eur
            ) * config.auto_fx_conversion_pct_per_side

        market_data_overhead = (
            config.estimated_monthly_market_data_cost_eur
            / config.expected_monthly_round_trips
        )

        total = (
            buy_commission
            + sell_commission
            + slippage
            + config.estimated_external_fees_eur
            + fx_buffer
            + market_data_overhead
        )

        return TradingCostEstimate(
            buy_commission_eur=round(buy_commission, 2),
            sell_commission_eur=round(sell_commission, 2),
            slippage_eur=round(slippage, 2),
            external_fees_eur=round(
                config.estimated_external_fees_eur,
                2,
            ),
            fx_conversion_buffer_eur=round(fx_buffer, 2),
            market_data_overhead_eur=round(
                market_data_overhead + 1e-12,
                2,
            ),
            total_cost_eur=round(total, 2),
        )

    def _us_commission_eur(
        self,
        *,
        quantity: int,
        fx_rate_to_base: float,
        pricing_plan: str,
    ) -> float:
        if pricing_plan == LivePaperTradingConfig.TIERED_PRICING:
            commission_usd = max(
                self.US_TIERED_MINIMUM_USD,
                quantity * self.US_TIERED_PER_SHARE_USD,
            )
        else:
            commission_usd = max(
                self.US_FIXED_MINIMUM_USD,
                quantity * self.US_FIXED_PER_SHARE_USD,
            )

        return commission_usd * fx_rate_to_base
