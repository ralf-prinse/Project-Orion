from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass(frozen=True)
class LivePaperTradingConfig:
    """
    Configuration for live paper trading.

    Uses real market data, but only paper money.
    """

    SWING: ClassVar[str] = "SWING"
    COST_AWARE_SMALL_PROFIT: ClassVar[str] = (
        "COST_AWARE_SMALL_PROFIT"
    )
    FIXED_PRICING: ClassVar[str] = "FIXED"
    TIERED_PRICING: ClassVar[str] = "TIERED"
    NEWS_DISABLED: ClassVar[str] = "DISABLED"
    NEWS_SHADOW: ClassVar[str] = "SHADOW"

    watchlist_path: Path = Path("data/universes/swing.csv")

    base_currency: str = "EUR"

    initial_cash: float = 10_000.0

    max_symbols: int = 150

    max_open_positions: int = 20

    max_new_positions_per_cycle: int = 3

    min_confidence: float = 0.75

    max_position_value: float = 500.0

    max_position_size_pct: float = 0.05

    max_portfolio_exposure: float = 0.90

    min_cash_reserve_pct: float = 0.10

    max_risk_per_trade_pct: float = 0.01

    max_portfolio_risk_pct: float = 0.06

    max_drawdown_pct: float = 0.10

    history_period: str = "3mo"
    history_interval: str = "1d"

    allow_fractional_shares: bool = False

    take_profit_percent: float = 0.08
    stop_loss_percent: float = 0.04
    trailing_stop_percent: float = 0.03
    break_even_trigger_percent: float = 0.05

    max_holding_days: int = 2

    enable_trailing_stop: bool = True
    enable_break_even: bool = True

    exit_strategy: str = SWING

    ibkr_pricing_plan: str = FIXED_PRICING

    small_profit_target_us_eur: float = 5.0
    small_profit_target_eu_eur: float = 10.0

    small_profit_max_loss_us_eur: float = 8.0
    small_profit_max_loss_eu_eur: float = 15.0

    estimated_slippage_pct_per_side: float = 0.0005
    estimated_external_fees_eur: float = 0.25
    include_auto_fx_conversion_buffer: bool = True
    auto_fx_conversion_pct_per_side: float = 0.0003

    news_mode: str = NEWS_DISABLED
    news_lookback_hours: int = 24
    news_max_articles_per_symbol: int = 10
    news_max_candidate_symbols_per_cycle: int = 20

    def __post_init__(self) -> None:
        normalized_strategy = self.exit_strategy.strip().upper()
        if normalized_strategy not in {
            self.SWING,
            self.COST_AWARE_SMALL_PROFIT,
        }:
            raise ValueError(
                "exit_strategy must be SWING or "
                "COST_AWARE_SMALL_PROFIT."
            )
        object.__setattr__(
            self,
            "exit_strategy",
            normalized_strategy,
        )

        normalized_pricing = self.ibkr_pricing_plan.strip().upper()
        if normalized_pricing not in {
            self.FIXED_PRICING,
            self.TIERED_PRICING,
        }:
            raise ValueError(
                "ibkr_pricing_plan must be FIXED or TIERED."
            )
        object.__setattr__(
            self,
            "ibkr_pricing_plan",
            normalized_pricing,
        )

        normalized_news_mode = self.news_mode.strip().upper()
        if normalized_news_mode not in {
            self.NEWS_DISABLED,
            self.NEWS_SHADOW,
        }:
            raise ValueError(
                "news_mode must be DISABLED or SHADOW."
            )
        object.__setattr__(self, "news_mode", normalized_news_mode)

        if self.max_new_positions_per_cycle < 1:
            raise ValueError(
                "max_new_positions_per_cycle must be at least 1."
            )

        if self.news_lookback_hours < 1:
            raise ValueError("news_lookback_hours must be at least 1.")
        if self.news_max_articles_per_symbol < 1:
            raise ValueError(
                "news_max_articles_per_symbol must be at least 1."
            )
        if self.news_max_candidate_symbols_per_cycle < 1:
            raise ValueError(
                "news_max_candidate_symbols_per_cycle must be at least 1."
            )

        positive_amounts = {
            "small_profit_target_us_eur": (
                self.small_profit_target_us_eur
            ),
            "small_profit_target_eu_eur": (
                self.small_profit_target_eu_eur
            ),
            "small_profit_max_loss_us_eur": (
                self.small_profit_max_loss_us_eur
            ),
            "small_profit_max_loss_eu_eur": (
                self.small_profit_max_loss_eu_eur
            ),
        }
        for name, value in positive_amounts.items():
            if value <= 0:
                raise ValueError(f"{name} must be greater than zero.")

        non_negative_amounts = {
            "estimated_slippage_pct_per_side": (
                self.estimated_slippage_pct_per_side
            ),
            "estimated_external_fees_eur": (
                self.estimated_external_fees_eur
            ),
            "auto_fx_conversion_pct_per_side": (
                self.auto_fx_conversion_pct_per_side
            ),
        }
        for name, value in non_negative_amounts.items():
            if value < 0:
                raise ValueError(f"{name} must not be negative.")
