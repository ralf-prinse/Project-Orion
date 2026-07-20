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

    # Entry selectivity. The legacy decision remains visible in journals,
    # but a BUY may only reach allocation when the independently built
    # investment thesis and opportunity ranking confirm it.
    require_buy_thesis: bool = True
    min_thesis_conviction: float = 68.0
    min_opportunity_score: float = 70.0
    min_trend_factor: float = 0.40
    min_momentum_factor: float = 0.50
    min_pressure_confirmation_factor: float = 0.55

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

    # Execution-grade Paper controls. Native child orders and software exits
    # share a persistent trade-based OCA group so only one exit can fill.
    enable_native_protective_orders: bool = True
    enable_execution_quality_gate: bool = True
    max_bid_ask_spread_pct: float = 0.003
    max_quote_age_seconds: float = 5.0
    max_entry_slippage_pct: float = 0.0015

    # Session-level circuit breaker. It blocks new BUY orders; managed exits
    # remain active.
    max_daily_loss_pct: float = 0.02
    max_consecutive_losses: int = 3
    circuit_breaker_cooldown_minutes: int = 60
    max_consecutive_order_failures: int = 3

    # Coarse concentration controls that work without unreliable third-party
    # sector metadata. More detailed sector/correlation controls can be fed by
    # the optional instrument metadata service.
    max_positions_per_market: int = 12
    max_market_exposure_pct: float = 0.70
    max_positions_per_sector: int = 4
    max_sector_exposure_pct: float = 0.25
    max_positions_per_correlation_cluster: int = 4
    instrument_metadata_path: Path = Path("data/instrument_metadata.csv")

    # Known earnings events can block entries. Missing event data is reported
    # but does not pretend that a date is known.
    earnings_blackout_days: int = 1
    earnings_calendar_path: Path = Path("data/earnings_calendar.csv")

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

        bounded_scores = {
            "min_thesis_conviction": self.min_thesis_conviction,
            "min_opportunity_score": self.min_opportunity_score,
        }
        for name, value in bounded_scores.items():
            if not 0 <= value <= 100:
                raise ValueError(f"{name} must be between 0 and 100.")

        bounded_factors = {
            "min_trend_factor": self.min_trend_factor,
            "min_momentum_factor": self.min_momentum_factor,
            "min_pressure_confirmation_factor": (
                self.min_pressure_confirmation_factor
            ),
        }
        for name, value in bounded_factors.items():
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1.")

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

        if self.max_consecutive_losses < 1:
            raise ValueError("max_consecutive_losses must be at least 1.")
        if self.circuit_breaker_cooldown_minutes < 1:
            raise ValueError(
                "circuit_breaker_cooldown_minutes must be at least 1."
            )
        if self.max_consecutive_order_failures < 1:
            raise ValueError(
                "max_consecutive_order_failures must be at least 1."
            )
        if self.max_positions_per_market < 1:
            raise ValueError("max_positions_per_market must be at least 1.")
        if self.max_positions_per_sector < 1:
            raise ValueError("max_positions_per_sector must be at least 1.")
        if self.max_positions_per_correlation_cluster < 1:
            raise ValueError(
                "max_positions_per_correlation_cluster must be at least 1."
            )
        if self.earnings_blackout_days < 0:
            raise ValueError("earnings_blackout_days must not be negative.")

        bounded_percentages = {
            "max_bid_ask_spread_pct": self.max_bid_ask_spread_pct,
            "max_entry_slippage_pct": self.max_entry_slippage_pct,
            "max_daily_loss_pct": self.max_daily_loss_pct,
            "max_market_exposure_pct": self.max_market_exposure_pct,
            "max_sector_exposure_pct": self.max_sector_exposure_pct,
        }
        for name, value in bounded_percentages.items():
            if not 0 < value < 1:
                raise ValueError(f"{name} must be between zero and one.")
        if self.max_quote_age_seconds <= 0:
            raise ValueError("max_quote_age_seconds must be greater than zero.")

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
